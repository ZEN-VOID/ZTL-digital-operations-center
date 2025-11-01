# 对话延续系统设计文档

## 1. 系统概述

### 1.1 目标
实现类似Claude Code的对话恢复机制,当对话上下文达到限制时:
- 自动压缩历史对话
- 提取关键记忆和决策点
- 生成延续会话摘要
- 无缝恢复对话状态

### 1.2 参考架构
基于全局CLAUDE.md中的MANUS上下文工程系统(上下求索技能包),实现10种上下文类型管理:

```yaml
上下文类型:
  1. focus: 当前关注点 (当前任务、目标)
  2. todo: 待办事项 (任务清单、进度)
  3. process: 工作流程 (执行步骤、方法论)
  4. error: 错误学习 (失败案例、教训)
  5. success: 成功经验 (最佳实践、解决方案)
  6. insights: 洞察发现 (关键发现、模式)
  7. patterns: 模式积累 (重复模式、规律)
  8. context: 项目背景 (需求、约束、依赖)
  9. memory: 长期记忆 (重要决策、里程碑)
  10. snapshot: 状态快照 (完整对话快照)
```

## 2. 系统架构

### 2.1 三层架构

```
┌─────────────────────────────────────────────────┐
│  Layer 1: UI Layer (React Components)          │
│  - 对话界面                                     │
│  - 延续提示UI                                   │
│  - 记忆展示面板                                 │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  Layer 2: Service Layer (Business Logic)       │
│  - ContextManager: 上下文管理                   │
│  - MemoryExtractor: 记忆提取                    │
│  - ConversationCompressor: 对话压缩             │
│  - ContinuationGenerator: 延续生成              │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  Layer 3: Storage Layer (Supabase)             │
│  - conversations: 对话会话                      │
│  - messages: 消息记录                           │
│  - conversation_memories: 对话记忆              │
│  - conversation_snapshots: 对话快照             │
└─────────────────────────────────────────────────┘
```

### 2.2 数据库Schema扩展

#### 新增表: `conversation_memories`
```sql
CREATE TABLE conversation_memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,

  -- 记忆分类 (10种类型)
  memory_type TEXT NOT NULL CHECK (memory_type IN (
    'focus', 'todo', 'process', 'error', 'success',
    'insights', 'patterns', 'context', 'memory', 'snapshot'
  )),

  -- 记忆内容
  content TEXT NOT NULL,

  -- 元数据
  metadata JSONB DEFAULT '{}',

  -- 重要性评分 (0-10)
  importance_score INTEGER DEFAULT 5 CHECK (importance_score BETWEEN 0 AND 10),

  -- 时间戳
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- 索引
  INDEX idx_conv_memories_conversation (conversation_id),
  INDEX idx_conv_memories_type (memory_type),
  INDEX idx_conv_memories_importance (importance_score DESC)
);
```

#### 新增表: `conversation_snapshots`
```sql
CREATE TABLE conversation_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,

  -- 快照触发原因
  trigger_reason TEXT NOT NULL CHECK (trigger_reason IN (
    'manual', 'auto_compact', 'context_limit', 'session_end'
  )),

  -- 快照数据
  snapshot_data JSONB NOT NULL, -- 包含完整messages + metadata

  -- 压缩后的摘要
  summary TEXT,

  -- 提取的关键记忆
  extracted_memories JSONB DEFAULT '[]',

  -- 消息数量统计
  message_count INTEGER NOT NULL DEFAULT 0,
  total_tokens INTEGER, -- 如果可计算

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  INDEX idx_conv_snapshots_conversation (conversation_id),
  INDEX idx_conv_snapshots_created (created_at DESC)
);
```

#### 扩展表: `conversations`
```sql
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS
  -- 上下文状态
  context_status TEXT DEFAULT 'normal' CHECK (context_status IN (
    'normal', 'approaching_limit', 'compacted', 'continued'
  )),

  -- 父会话ID (用于延续会话)
  parent_conversation_id UUID REFERENCES conversations(id),

  -- 延续序号 (第几次延续)
  continuation_index INTEGER DEFAULT 0,

  -- 最后压缩时间
  last_compacted_at TIMESTAMP WITH TIME ZONE,

  -- 消息数量缓存
  message_count INTEGER DEFAULT 0,

  -- 元数据
  metadata JSONB DEFAULT '{}';
```

## 3. 核心服务实现

### 3.1 ContextManager (上下文管理器)

```typescript
// lib/services/context-manager.ts

interface ContextThresholds {
  warningThreshold: number;  // 警告阈值 (如80%容量)
  compactThreshold: number;  // 压缩阈值 (如90%容量)
  maxMessages: number;       // 最大消息数
}

class ContextManager {
  private thresholds: ContextThresholds;

  constructor(thresholds?: Partial<ContextThresholds>) {
    this.thresholds = {
      warningThreshold: 50,  // 50条消息提示
      compactThreshold: 80,  // 80条消息压缩
      maxMessages: 100,      // 100条消息硬限制
      ...thresholds,
    };
  }

  /**
   * 评估上下文状态
   */
  assessContextStatus(messageCount: number): {
    status: 'normal' | 'approaching_limit' | 'should_compact' | 'must_compact';
    percentage: number;
    recommendation: string;
  } {
    const percentage = (messageCount / this.thresholds.maxMessages) * 100;

    if (messageCount >= this.thresholds.maxMessages) {
      return {
        status: 'must_compact',
        percentage,
        recommendation: '已达上下文限制,必须压缩或开启新对话',
      };
    }

    if (messageCount >= this.thresholds.compactThreshold) {
      return {
        status: 'should_compact',
        percentage,
        recommendation: '建议压缩对话历史以优化性能',
      };
    }

    if (messageCount >= this.thresholds.warningThreshold) {
      return {
        status: 'approaching_limit',
        percentage,
        recommendation: '对话历史较长,可能需要压缩',
      };
    }

    return {
      status: 'normal',
      percentage,
      recommendation: '上下文正常',
    };
  }

  /**
   * 检查是否需要自动压缩
   */
  shouldAutoCompact(messageCount: number): boolean {
    return messageCount >= this.thresholds.compactThreshold;
  }
}
```

### 3.2 MemoryExtractor (记忆提取器)

```typescript
// lib/services/memory-extractor.ts

interface ExtractedMemory {
  type: 'focus' | 'todo' | 'process' | 'error' | 'success' |
        'insights' | 'patterns' | 'context' | 'memory' | 'snapshot';
  content: string;
  importance: number; // 0-10
  metadata?: Record<string, any>;
}

class MemoryExtractor {
  /**
   * 从消息历史中提取关键记忆
   */
  async extractMemories(
    messages: Message[],
    agentContext?: string
  ): Promise<ExtractedMemory[]> {
    const memories: ExtractedMemory[] = [];

    // 1. 提取当前关注点 (focus)
    const recentMessages = messages.slice(-10);
    if (recentMessages.length > 0) {
      memories.push({
        type: 'focus',
        content: this.summarizeFocus(recentMessages),
        importance: 9,
      });
    }

    // 2. 提取待办事项 (todo)
    const todoMessages = messages.filter(m =>
      m.content.includes('TODO') ||
      m.content.includes('待办') ||
      m.content.includes('需要')
    );
    if (todoMessages.length > 0) {
      memories.push({
        type: 'todo',
        content: this.extractTodos(todoMessages),
        importance: 8,
      });
    }

    // 3. 提取错误学习 (error)
    const errorMessages = messages.filter(m =>
      m.content.includes('错误') ||
      m.content.includes('失败') ||
      m.content.includes('问题')
    );
    if (errorMessages.length > 0) {
      memories.push({
        type: 'error',
        content: this.summarizeErrors(errorMessages),
        importance: 7,
      });
    }

    // 4. 提取成功经验 (success)
    const successMessages = messages.filter(m =>
      m.content.includes('成功') ||
      m.content.includes('完成') ||
      m.content.includes('解决')
    );
    if (successMessages.length > 0) {
      memories.push({
        type: 'success',
        content: this.summarizeSuccesses(successMessages),
        importance: 7,
      });
    }

    // 5. 提取洞察发现 (insights)
    memories.push({
      type: 'insights',
      content: this.extractInsights(messages),
      importance: 6,
    });

    // 6. 提取项目背景 (context)
    const contextInfo = this.extractContextInfo(messages, agentContext);
    if (contextInfo) {
      memories.push({
        type: 'context',
        content: contextInfo,
        importance: 8,
      });
    }

    return memories;
  }

  private summarizeFocus(messages: Message[]): string {
    // 提取最近对话的主题和目标
    const contents = messages.map(m => m.content).join('\n');
    return `当前对话焦点:\n${contents.slice(0, 500)}...`;
  }

  private extractTodos(messages: Message[]): string {
    const todos = messages.map(m => `- ${m.content}`).join('\n');
    return `待办事项:\n${todos}`;
  }

  private summarizeErrors(messages: Message[]): string {
    const errors = messages.map((m, i) =>
      `${i + 1}. ${m.content.slice(0, 200)}`
    ).join('\n');
    return `遇到的问题:\n${errors}`;
  }

  private summarizeSuccesses(messages: Message[]): string {
    const successes = messages.map((m, i) =>
      `${i + 1}. ${m.content.slice(0, 200)}`
    ).join('\n');
    return `成功完成:\n${successes}`;
  }

  private extractInsights(messages: Message[]): string {
    // 简单实现: 提取包含关键词的消息
    const keywords = ['发现', '原因', '因为', '建议', '可以', '应该'];
    const insightMessages = messages.filter(m =>
      keywords.some(kw => m.content.includes(kw))
    );

    if (insightMessages.length === 0) return '无特别洞察';

    return insightMessages
      .slice(-5)
      .map(m => `- ${m.content.slice(0, 150)}`)
      .join('\n');
  }

  private extractContextInfo(
    messages: Message[],
    agentContext?: string
  ): string | null {
    if (messages.length === 0) return null;

    const firstMessages = messages.slice(0, 5);
    const summary = firstMessages
      .map(m => m.content)
      .join('\n')
      .slice(0, 500);

    return `对话背景:\n智能体: ${agentContext || '未知'}\n初始需求: ${summary}`;
  }
}
```

### 3.3 ConversationCompressor (对话压缩器)

```typescript
// lib/services/conversation-compressor.ts

interface CompressionResult {
  compressedMessages: Message[];  // 保留的关键消息
  summary: string;                // 压缩摘要
  removedCount: number;           // 删除的消息数
  memories: ExtractedMemory[];    // 提取的记忆
}

class ConversationCompressor {
  private memoryExtractor: MemoryExtractor;

  constructor() {
    this.memoryExtractor = new MemoryExtractor();
  }

  /**
   * 压缩对话历史
   * 策略: 保留最近N条 + 关键消息,其余转为摘要和记忆
   */
  async compress(
    messages: Message[],
    options?: {
      keepRecentCount?: number;    // 保留最近多少条 (默认20)
      keepImportantCount?: number; // 保留重要消息多少条 (默认10)
      agentContext?: string;
    }
  ): Promise<CompressionResult> {
    const keepRecentCount = options?.keepRecentCount || 20;
    const keepImportantCount = options?.keepImportantCount || 10;

    // 1. 从全部消息中提取记忆
    const memories = await this.memoryExtractor.extractMemories(
      messages,
      options?.agentContext
    );

    // 2. 保留最近的消息
    const recentMessages = messages.slice(-keepRecentCount);

    // 3. 从旧消息中选择重要消息
    const oldMessages = messages.slice(0, -keepRecentCount);
    const importantMessages = this.selectImportantMessages(
      oldMessages,
      keepImportantCount
    );

    // 4. 生成被压缩消息的摘要
    const removedMessages = oldMessages.filter(
      m => !importantMessages.includes(m)
    );
    const summary = this.generateSummary(removedMessages, memories);

    // 5. 组合结果: 重要消息 + 最近消息
    const compressedMessages = [
      ...importantMessages,
      ...recentMessages,
    ];

    return {
      compressedMessages,
      summary,
      removedCount: removedMessages.length,
      memories,
    };
  }

  /**
   * 选择重要消息 (基于启发式规则)
   */
  private selectImportantMessages(
    messages: Message[],
    count: number
  ): Message[] {
    // 重要性评分规则
    const scoredMessages = messages.map(msg => ({
      message: msg,
      score: this.calculateImportance(msg),
    }));

    // 按重要性排序并取前N条
    return scoredMessages
      .sort((a, b) => b.score - a.score)
      .slice(0, count)
      .map(item => item.message)
      .sort((a, b) =>
        (a.timestamp?.getTime() || 0) - (b.timestamp?.getTime() || 0)
      ); // 保持时间顺序
  }

  /**
   * 计算消息重要性 (0-100)
   */
  private calculateImportance(message: Message): number {
    let score = 50; // 基础分

    // 长度加分 (长消息通常更重要)
    if (message.content.length > 200) score += 10;
    if (message.content.length > 500) score += 10;

    // 关键词加分
    const importantKeywords = [
      '决定', '确定', '计划', '目标', '方案', '设计',
      'TODO', '待办', '问题', '错误', '成功', '完成',
      '重要', '关键', '核心', '必须', '建议'
    ];

    importantKeywords.forEach(keyword => {
      if (message.content.includes(keyword)) score += 5;
    });

    // 系统消息降分
    if (message.role === 'system') score -= 20;

    // 短消息降分
    if (message.content.length < 50) score -= 10;

    return Math.max(0, Math.min(100, score));
  }

  /**
   * 生成压缩摘要
   */
  private generateSummary(
    removedMessages: Message[],
    memories: ExtractedMemory[]
  ): string {
    const sections: string[] = [];

    sections.push(`# 对话压缩摘要`);
    sections.push(`压缩时间: ${new Date().toLocaleString('zh-CN')}`);
    sections.push(`压缩消息数: ${removedMessages.length}条\n`);

    // 添加记忆摘要
    sections.push(`## 提取的关键记忆\n`);

    memories
      .sort((a, b) => b.importance - a.importance)
      .forEach(memory => {
        sections.push(`### ${memory.type.toUpperCase()}`);
        sections.push(memory.content);
        sections.push('');
      });

    // 添加消息统计
    const userMsgCount = removedMessages.filter(m => m.role === 'user').length;
    const assistantMsgCount = removedMessages.filter(m => m.role === 'assistant').length;

    sections.push(`## 消息统计`);
    sections.push(`- 用户消息: ${userMsgCount}条`);
    sections.push(`- 助手消息: ${assistantMsgCount}条`);
    sections.push(`- 总计: ${removedMessages.length}条`);

    return sections.join('\n');
  }
}
```

### 3.4 ContinuationGenerator (延续生成器)

```typescript
// lib/services/continuation-generator.ts

interface ContinuationContext {
  conversationId: string;
  agentName: string;
  summary: string;
  memories: ExtractedMemory[];
  lastMessages: Message[];
}

class ContinuationGenerator {
  /**
   * 生成延续会话的系统提示
   */
  generateContinuationPrompt(context: ContinuationContext): string {
    const sections: string[] = [];

    sections.push('# 对话延续 - 上下文恢复\n');
    sections.push('这是一个延续的对话会话。以下是之前对话的关键信息:\n');

    // 1. 当前智能体
    sections.push(`## 当前智能体`);
    sections.push(`${context.agentName}\n`);

    // 2. 对话摘要
    sections.push(`## 对话历史摘要`);
    sections.push(context.summary);
    sections.push('');

    // 3. 关键记忆 (按重要性排序)
    const sortedMemories = context.memories
      .sort((a, b) => b.importance - a.importance);

    if (sortedMemories.length > 0) {
      sections.push(`## 关键记忆\n`);

      sortedMemories.forEach(memory => {
        sections.push(`### ${memory.type} (重要性: ${memory.importance}/10)`);
        sections.push(memory.content);
        sections.push('');
      });
    }

    // 4. 最近消息 (保持上下文连贯)
    if (context.lastMessages.length > 0) {
      sections.push(`## 最近对话`);
      sections.push('最近的对话消息 (用于保持连贯性):\n');

      context.lastMessages.slice(-5).forEach(msg => {
        const role = msg.role === 'user' ? '用户' : msg.agentName || '助手';
        sections.push(`**${role}**: ${msg.content.slice(0, 300)}${msg.content.length > 300 ? '...' : ''}`);
        sections.push('');
      });
    }

    sections.push('---');
    sections.push('请基于以上上下文继续对话。');

    return sections.join('\n');
  }

  /**
   * 创建延续会话的初始化消息
   */
  createContinuationMessage(prompt: string): Message {
    return {
      id: `msg-continuation-${Date.now()}`,
      role: 'system',
      content: prompt,
      timestamp: new Date(),
      metadata: {
        type: 'continuation',
        isRecovery: true,
      },
    };
  }
}
```

## 4. UI组件设计

### 4.1 ContextStatusBar (上下文状态栏)

显示当前对话的上下文使用情况,类似进度条:

```typescript
// components/chat/context-status-bar.tsx

interface ContextStatusBarProps {
  messageCount: number;
  maxMessages: number;
  onCompact?: () => void;
  onNewConversation?: () => void;
}

export function ContextStatusBar({
  messageCount,
  maxMessages,
  onCompact,
  onNewConversation,
}: ContextStatusBarProps) {
  const percentage = (messageCount / maxMessages) * 100;
  const status = getStatusLevel(percentage);

  return (
    <div className="context-status-bar">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-text-secondary">
          对话上下文: {messageCount}/{maxMessages} 条消息
        </span>
        <span className="text-xs font-bold" style={{ color: status.color }}>
          {status.label}
        </span>
      </div>

      <div className="h-2 bg-cyber-bg-tertiary rounded-full overflow-hidden">
        <div
          className="h-full transition-all duration-300"
          style={{
            width: `${percentage}%`,
            backgroundColor: status.color,
          }}
        />
      </div>

      {percentage >= 80 && (
        <div className="mt-3 flex gap-2">
          <button
            onClick={onCompact}
            className="btn-sm btn-primary"
          >
            压缩历史
          </button>
          <button
            onClick={onNewConversation}
            className="btn-sm btn-secondary"
          >
            开启新对话
          </button>
        </div>
      )}
    </div>
  );
}

function getStatusLevel(percentage: number) {
  if (percentage >= 90) {
    return { label: '接近上限', color: '#ff0080' }; // neon-pink
  }
  if (percentage >= 70) {
    return { label: '建议压缩', color: '#ffaa00' }; // warning-yellow
  }
  if (percentage >= 50) {
    return { label: '正常', color: '#00ffff' }; // neon-cyan
  }
  return { label: '充足', color: '#00ff88' }; // neon-green
}
```

### 4.2 MemoryPanel (记忆面板)

侧边栏展示提取的关键记忆:

```typescript
// components/chat/memory-panel.tsx

interface MemoryPanelProps {
  memories: ExtractedMemory[];
  onMemoryClick?: (memory: ExtractedMemory) => void;
}

export function MemoryPanel({ memories, onMemoryClick }: MemoryPanelProps) {
  const groupedMemories = groupBy(memories, 'type');

  return (
    <div className="memory-panel p-4 space-y-4">
      <h3 className="text-sm font-bold text-text-secondary uppercase">
        对话记忆
      </h3>

      {Object.entries(groupedMemories).map(([type, items]) => (
        <div key={type} className="memory-group">
          <h4 className="text-xs font-semibold text-neon-cyan mb-2">
            {getMemoryTypeLabel(type)}
          </h4>

          <div className="space-y-2">
            {items.map((memory, index) => (
              <div
                key={index}
                onClick={() => onMemoryClick?.(memory)}
                className="memory-item glass-panel p-2 rounded cursor-pointer hover:bg-cyber-bg-tertiary/50 transition-colors"
              >
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs text-text-secondary line-clamp-3">
                    {memory.content}
                  </p>
                  <span className="text-xs font-bold text-neon-pink whitespace-nowrap">
                    {memory.importance}/10
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function getMemoryTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    focus: '当前焦点',
    todo: '待办事项',
    process: '工作流程',
    error: '错误学习',
    success: '成功经验',
    insights: '洞察发现',
    patterns: '模式积累',
    context: '项目背景',
    memory: '长期记忆',
    snapshot: '状态快照',
  };
  return labels[type] || type;
}
```

## 5. 工作流程

### 5.1 正常对话流程

```
用户发送消息
  ↓
检查上下文状态 (ContextManager.assessContextStatus)
  ↓
状态正常? ─ YES → 正常处理消息
  │
  NO (approaching_limit)
  ↓
显示警告UI (ContextStatusBar)
  ↓
继续对话...
```

### 5.2 自动压缩流程

```
检测到超过阈值 (should_compact)
  ↓
用户确认压缩? ─ NO → 继续对话(但显示警告)
  │
  YES
  ↓
1. 创建快照 (ConversationSnapshot)
  ↓
2. 提取记忆 (MemoryExtractor.extractMemories)
  ↓
3. 压缩对话 (ConversationCompressor.compress)
  ↓
4. 保存记忆到数据库 (conversation_memories)
  ↓
5. 更新消息列表 (保留关键消息)
  ↓
6. 显示压缩摘要消息 (系统消息)
  ↓
对话恢复到正常状态
```

### 5.3 延续新会话流程

```
检测到达上限 (must_compact) 或用户主动开启新对话
  ↓
1. 创建最终快照
  ↓
2. 提取所有记忆
  ↓
3. 生成延续提示 (ContinuationGenerator.generateContinuationPrompt)
  ↓
4. 创建新会话 (parent_conversation_id = 当前会话ID)
  ↓
5. 插入延续系统消息 (包含完整上下文恢复)
  ↓
6. 用户在新会话中继续对话
  ↓
智能体接收完整上下文,无缝延续
```

## 6. 实施计划

### Phase 1: 数据库基础 (1-2小时)
- [ ] 创建新表: conversation_memories, conversation_snapshots
- [ ] 扩展conversations表
- [ ] 编写迁移脚本

### Phase 2: 核心服务 (3-4小时)
- [ ] 实现ContextManager
- [ ] 实现MemoryExtractor
- [ ] 实现ConversationCompressor
- [ ] 实现ContinuationGenerator
- [ ] 编写单元测试

### Phase 3: Supabase集成 (2-3小时)
- [ ] 扩展supabase client types
- [ ] 实现conversation-service.ts (CRUD for memories/snapshots)
- [ ] 实现存储/读取记忆的函数

### Phase 4: UI组件 (2-3小时)
- [ ] 实现ContextStatusBar
- [ ] 实现MemoryPanel
- [ ] 实现CompactDialog (压缩确认对话框)
- [ ] 实现ContinuationDialog (新对话提示)

### Phase 5: 集成到Chat页面 (2-3小时)
- [ ] 集成ContextManager到Chat状态
- [ ] 添加自动检测和警告
- [ ] 实现压缩按钮和流程
- [ ] 实现新对话延续流程
- [ ] 添加记忆面板到侧边栏

### Phase 6: 测试和优化 (2-3小时)
- [ ] 端到端测试
- [ ] 性能优化
- [ ] UI/UX调整
- [ ] 编写使用文档

**总计**: 约 12-18小时

## 7. 配置选项

### 用户可配置项

```typescript
// lib/config/conversation-config.ts

export const CONVERSATION_CONFIG = {
  // 上下文阈值
  context: {
    warningThreshold: 50,      // 50条消息警告
    compactThreshold: 80,      // 80条消息建议压缩
    maxMessages: 100,          // 100条消息硬限制
  },

  // 压缩策略
  compression: {
    keepRecentCount: 20,       // 保留最近20条
    keepImportantCount: 10,    // 保留10条重要消息
    autoCompact: true,         // 自动压缩
  },

  // 记忆设置
  memory: {
    minImportance: 5,          // 最低重要性阈值
    maxMemoriesPerType: 10,    // 每种类型最多保存10条
    enableMemoryPanel: true,   // 启用记忆面板
  },

  // 延续设置
  continuation: {
    maxContinuations: 5,       // 最多延续5次
    includeLastNMessages: 5,   // 包含最后5条消息
  },
};
```

## 8. 最佳实践

### 8.1 压缩时机
- ✅ 推荐: 在用户发送新消息前检查并提示
- ✅ 推荐: 在切换智能体时自动触发
- ❌ 避免: 在助手回复过程中压缩

### 8.2 记忆提取
- ✅ 关注质量而非数量 (重要性评分 ≥ 6)
- ✅ 保留用户明确要求记住的内容
- ✅ 记录所有错误和解决方案

### 8.3 延续会话
- ✅ 在延续消息中包含完整上下文
- ✅ 保持智能体身份连贯性
- ✅ 显示清晰的分界线 (系统消息)

## 9. 未来增强

### 9.1 智能压缩
- 使用LLM生成更高质量的摘要
- 智能识别关键决策点
- 自动提取代码片段和配置

### 9.2 跨会话记忆
- 构建用户级长期记忆库
- 智能体级知识积累
- 项目级上下文共享

### 9.3 可视化
- 对话关系图谱
- 记忆时间线
- 决策树可视化

---

**文档版本**: v1.0
**创建时间**: 2025-11-01
**作者**: Claude Code + ZTL Team
