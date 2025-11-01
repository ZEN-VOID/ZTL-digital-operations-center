/**
 * Memory Extractor - 对话记忆提取器
 * 从消息历史中提取关键记忆,按10种类型分类
 */

import type { Message } from '@/components/chat/message-list';

export type MemoryType =
  | 'focus' // 当前关注点
  | 'todo' // 待办事项
  | 'process' // 工作流程
  | 'error' // 错误学习
  | 'success' // 成功经验
  | 'insights' // 洞察发现
  | 'patterns' // 模式积累
  | 'context' // 项目背景
  | 'memory' // 长期记忆
  | 'snapshot'; // 状态快照

export interface ExtractedMemory {
  type: MemoryType;
  content: string;
  importance: number; // 0-10
  metadata?: Record<string, any>;
  timestamp?: Date;
}

export class MemoryExtractor {
  /**
   * 从消息历史中提取关键记忆
   */
  async extractMemories(
    messages: Message[],
    agentContext?: string
  ): Promise<ExtractedMemory[]> {
    const memories: ExtractedMemory[] = [];

    if (messages.length === 0) return memories;

    // 1. 提取当前关注点 (focus)
    const recentMessages = messages.slice(-10);
    if (recentMessages.length > 0) {
      const focusMemory = this.extractFocus(recentMessages);
      if (focusMemory) memories.push(focusMemory);
    }

    // 2. 提取待办事项 (todo)
    const todoMemory = this.extractTodos(messages);
    if (todoMemory) memories.push(todoMemory);

    // 3. 提取错误学习 (error)
    const errorMemory = this.extractErrors(messages);
    if (errorMemory) memories.push(errorMemory);

    // 4. 提取成功经验 (success)
    const successMemory = this.extractSuccesses(messages);
    if (successMemory) memories.push(successMemory);

    // 5. 提取洞察发现 (insights)
    const insightsMemory = this.extractInsights(messages);
    if (insightsMemory) memories.push(insightsMemory);

    // 6. 提取模式积累 (patterns)
    const patternsMemory = this.extractPatterns(messages);
    if (patternsMemory) memories.push(patternsMemory);

    // 7. 提取项目背景 (context)
    const contextMemory = this.extractContextInfo(messages, agentContext);
    if (contextMemory) memories.push(contextMemory);

    // 8. 提取长期记忆 (memory) - 重要决策和里程碑
    const longTermMemory = this.extractLongTermMemory(messages);
    if (longTermMemory) memories.push(longTermMemory);

    return memories.filter(m => m.content.trim().length > 0);
  }

  /**
   * 提取当前关注点
   */
  private extractFocus(messages: Message[]): ExtractedMemory | null {
    const contents = messages
      .filter(m => m.role !== 'system')
      .map(m => m.content)
      .join('\n');

    if (!contents.trim()) return null;

    // 截取最近内容作为焦点
    const focusContent = contents.slice(-500);

    return {
      type: 'focus',
      content: `当前对话焦点:\n${focusContent}${contents.length > 500 ? '...' : ''}`,
      importance: 9,
      timestamp: new Date(),
    };
  }

  /**
   * 提取待办事项
   */
  private extractTodos(messages: Message[]): ExtractedMemory | null {
    const todoKeywords = ['TODO', 'todo', '待办', '需要', '要做', '下一步'];

    const todoMessages = messages.filter(m =>
      todoKeywords.some(kw => m.content.includes(kw))
    );

    if (todoMessages.length === 0) return null;

    const todos = todoMessages
      .slice(-10) // 最多取10条
      .map((m, i) => `${i + 1}. ${m.content.slice(0, 200)}`)
      .join('\n');

    return {
      type: 'todo',
      content: `待办事项:\n${todos}`,
      importance: 8,
      timestamp: new Date(),
    };
  }

  /**
   * 提取错误学习
   */
  private extractErrors(messages: Message[]): ExtractedMemory | null {
    const errorKeywords = ['错误', '失败', '问题', '报错', 'Error', 'error'];

    const errorMessages = messages.filter(m =>
      errorKeywords.some(kw => m.content.includes(kw))
    );

    if (errorMessages.length === 0) return null;

    const errors = errorMessages
      .slice(-5) // 最多取5条
      .map((m, i) => `${i + 1}. ${m.content.slice(0, 300)}`)
      .join('\n\n');

    return {
      type: 'error',
      content: `遇到的问题:\n${errors}`,
      importance: 7,
      timestamp: new Date(),
    };
  }

  /**
   * 提取成功经验
   */
  private extractSuccesses(messages: Message[]): ExtractedMemory | null {
    const successKeywords = ['成功', '完成', '解决', '实现了', '已经'];

    const successMessages = messages.filter(m =>
      successKeywords.some(kw => m.content.includes(kw))
    );

    if (successMessages.length === 0) return null;

    const successes = successMessages
      .slice(-5) // 最多取5条
      .map((m, i) => `${i + 1}. ${m.content.slice(0, 200)}`)
      .join('\n\n');

    return {
      type: 'success',
      content: `成功完成:\n${successes}`,
      importance: 7,
      timestamp: new Date(),
    };
  }

  /**
   * 提取洞察发现
   */
  private extractInsights(messages: Message[]): ExtractedMemory | null {
    const insightKeywords = [
      '发现', '原因', '因为', '所以', '建议', '可以',
      '应该', '最好', '注意', '关键', '重要'
    ];

    const insightMessages = messages.filter(m =>
      insightKeywords.some(kw => m.content.includes(kw)) &&
      m.content.length > 50 // 有一定长度
    );

    if (insightMessages.length === 0) return null;

    const insights = insightMessages
      .slice(-5)
      .map(m => `- ${m.content.slice(0, 200)}`)
      .join('\n');

    return {
      type: 'insights',
      content: `关键洞察:\n${insights}`,
      importance: 6,
      timestamp: new Date(),
    };
  }

  /**
   * 提取模式积累
   */
  private extractPatterns(messages: Message[]): ExtractedMemory | null {
    // 查找重复出现的主题或行为模式
    const topics: Record<string, number> = {};

    messages.forEach(m => {
      // 提取关键词 (简单实现: 长度>2的中文词组)
      const words = m.content.match(/[\u4e00-\u9fa5]{2,}/g) || [];
      words.forEach(word => {
        topics[word] = (topics[word] || 0) + 1;
      });
    });

    // 找出出现3次以上的主题
    const patterns = Object.entries(topics)
      .filter(([_, count]) => count >= 3)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([topic, count]) => `- ${topic} (出现${count}次)`)
      .join('\n');

    if (!patterns) return null;

    return {
      type: 'patterns',
      content: `发现的模式:\n${patterns}`,
      importance: 5,
      timestamp: new Date(),
    };
  }

  /**
   * 提取项目背景
   */
  private extractContextInfo(
    messages: Message[],
    agentContext?: string
  ): ExtractedMemory | null {
    if (messages.length === 0) return null;

    const firstMessages = messages.slice(0, 5);
    const summary = firstMessages
      .filter(m => m.role !== 'system')
      .map(m => m.content)
      .join('\n')
      .slice(0, 500);

    if (!summary.trim()) return null;

    return {
      type: 'context',
      content: `对话背景:\n智能体: ${agentContext || '未知'}\n\n初始需求:\n${summary}`,
      importance: 8,
      timestamp: new Date(),
    };
  }

  /**
   * 提取长期记忆 (重要决策和里程碑)
   */
  private extractLongTermMemory(messages: Message[]): ExtractedMemory | null {
    const milestoneKeywords = [
      '决定', '确定', '计划', '目标', '方案', '设计',
      '架构', '策略', '最终', '结论'
    ];

    const milestoneMessages = messages.filter(m =>
      milestoneKeywords.some(kw => m.content.includes(kw)) &&
      m.content.length > 100 // 内容较长
    );

    if (milestoneMessages.length === 0) return null;

    const milestones = milestoneMessages
      .slice(-3) // 最多取3条
      .map((m, i) => `${i + 1}. ${m.content.slice(0, 300)}`)
      .join('\n\n');

    return {
      type: 'memory',
      content: `重要决策:\n${milestones}`,
      importance: 9,
      timestamp: new Date(),
    };
  }

  /**
   * 按重要性对记忆排序
   */
  sortByImportance(memories: ExtractedMemory[]): ExtractedMemory[] {
    return [...memories].sort((a, b) => b.importance - a.importance);
  }

  /**
   * 过滤低重要性记忆
   */
  filterByImportance(
    memories: ExtractedMemory[],
    minImportance: number = 5
  ): ExtractedMemory[] {
    return memories.filter(m => m.importance >= minImportance);
  }

  /**
   * 按类型分组记忆
   */
  groupByType(
    memories: ExtractedMemory[]
  ): Record<MemoryType, ExtractedMemory[]> {
    const grouped: Partial<Record<MemoryType, ExtractedMemory[]>> = {};

    memories.forEach(memory => {
      if (!grouped[memory.type]) {
        grouped[memory.type] = [];
      }
      grouped[memory.type]!.push(memory);
    });

    return grouped as Record<MemoryType, ExtractedMemory[]>;
  }
}

// 导出默认实例
export const defaultMemoryExtractor = new MemoryExtractor();
