/**
 * Conversation Compressor - 对话压缩器
 * 压缩对话历史,保留关键消息,生成摘要
 */

import type { Message } from '@/components/chat/message-list';
import {
  MemoryExtractor,
  type ExtractedMemory,
  defaultMemoryExtractor,
} from './memory-extractor';

export interface CompressionOptions {
  keepRecentCount?: number; // 保留最近多少条 (默认20)
  keepImportantCount?: number; // 保留重要消息多少条 (默认10)
  agentContext?: string; // 智能体上下文
}

export interface CompressionResult {
  compressedMessages: Message[]; // 保留的关键消息
  summary: string; // 压缩摘要
  removedCount: number; // 删除的消息数
  memories: ExtractedMemory[]; // 提取的记忆
  compressionRatio: number; // 压缩比例 (0-1)
}

export class ConversationCompressor {
  private memoryExtractor: MemoryExtractor;

  constructor(memoryExtractor?: MemoryExtractor) {
    this.memoryExtractor = memoryExtractor || defaultMemoryExtractor;
  }

  /**
   * 压缩对话历史
   * 策略: 保留最近N条 + 关键消息,其余转为摘要和记忆
   */
  async compress(
    messages: Message[],
    options?: CompressionOptions
  ): Promise<CompressionResult> {
    const keepRecentCount = options?.keepRecentCount || 20;
    const keepImportantCount = options?.keepImportantCount || 10;

    if (messages.length <= keepRecentCount) {
      // 消息数少于保留数量,无需压缩
      return {
        compressedMessages: messages,
        summary: '无需压缩',
        removedCount: 0,
        memories: [],
        compressionRatio: 0,
      };
    }

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
      m => !importantMessages.some(im => im.id === m.id)
    );
    const summary = this.generateSummary(removedMessages, memories);

    // 5. 组合结果: 重要消息 + 最近消息
    const compressedMessages = [
      ...importantMessages,
      ...recentMessages,
    ];

    // 6. 计算压缩比例
    const compressionRatio = removedMessages.length / messages.length;

    return {
      compressedMessages,
      summary,
      removedCount: removedMessages.length,
      memories,
      compressionRatio,
    };
  }

  /**
   * 选择重要消息 (基于启发式规则)
   */
  private selectImportantMessages(
    messages: Message[],
    count: number
  ): Message[] {
    if (messages.length === 0) return [];

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
      .sort((a, b) => {
        // 保持时间顺序
        const timeA = a.timestamp?.getTime() || 0;
        const timeB = b.timestamp?.getTime() || 0;
        return timeA - timeB;
      });
  }

  /**
   * 计算消息重要性 (0-100)
   */
  private calculateImportance(message: Message): number {
    let score = 50; // 基础分

    // 长度加分 (长消息通常更重要)
    const length = message.content.length;
    if (length > 200) score += 10;
    if (length > 500) score += 10;
    if (length > 1000) score += 5;

    // 关键词加分
    const highImportanceKeywords = [
      '决定', '确定', '计划', '目标', '方案', '设计', '架构'
    ];
    const mediumImportanceKeywords = [
      'TODO', '待办', '问题', '错误', '成功', '完成',
      '重要', '关键', '核心', '必须', '建议', '注意'
    ];

    highImportanceKeywords.forEach(keyword => {
      if (message.content.includes(keyword)) score += 8;
    });

    mediumImportanceKeywords.forEach(keyword => {
      if (message.content.includes(keyword)) score += 5;
    });

    // 代码块加分 (包含代码的消息通常重要)
    if (message.content.includes('```')) score += 15;
    if (message.content.includes('```typescript') || message.content.includes('```javascript')) {
      score += 5; // 额外加分
    }

    // 列表加分 (结构化内容)
    const listMatches = message.content.match(/^[\s]*[-*\d]+\./gm);
    if (listMatches && listMatches.length > 2) score += 10;

    // 问题或请求加分
    if (message.role === 'user' && message.content.includes('?')) score += 5;
    if (message.role === 'user' && message.content.includes('请')) score += 5;

    // 系统消息降分 (除非是重要系统消息)
    if (message.role === 'system') {
      if (message.content.includes('压缩') || message.content.includes('延续')) {
        score += 10; // 压缩/延续消息很重要
      } else {
        score -= 20;
      }
    }

    // 短消息降分
    if (length < 50) score -= 15;
    if (length < 20) score -= 10;

    // 单纯的确认消息降分
    const trivialPhrases = ['好的', '知道了', '明白', '收到', 'ok', 'OK'];
    if (trivialPhrases.some(phrase => message.content.trim() === phrase)) {
      score -= 30;
    }

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

    sections.push(`# 对话压缩摘要\n`);
    sections.push(`压缩时间: ${new Date().toLocaleString('zh-CN')}`);
    sections.push(`压缩消息数: ${removedMessages.length}条\n`);

    // 添加记忆摘要
    if (memories.length > 0) {
      sections.push(`## 提取的关键记忆\n`);

      const sortedMemories = memories
        .sort((a, b) => b.importance - a.importance);

      sortedMemories.forEach(memory => {
        sections.push(`### ${this.getMemoryTypeLabel(memory.type)} (重要性: ${memory.importance}/10)`);
        sections.push(memory.content);
        sections.push('');
      });
    }

    // 添加消息统计
    const userMsgCount = removedMessages.filter(m => m.role === 'user').length;
    const assistantMsgCount = removedMessages.filter(m => m.role === 'assistant').length;
    const systemMsgCount = removedMessages.filter(m => m.role === 'system').length;

    sections.push(`## 消息统计\n`);
    sections.push(`- 用户消息: ${userMsgCount}条`);
    sections.push(`- 助手消息: ${assistantMsgCount}条`);
    sections.push(`- 系统消息: ${systemMsgCount}条`);
    sections.push(`- 总计: ${removedMessages.length}条\n`);

    sections.push(`---`);
    sections.push(`*此摘要由系统自动生成,已压缩的消息历史已存档*`);

    return sections.join('\n');
  }

  /**
   * 获取记忆类型的中文标签
   */
  private getMemoryTypeLabel(type: string): string {
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
    return labels[type] || type.toUpperCase();
  }

  /**
   * 创建压缩通知消息
   */
  createCompressionNotification(result: CompressionResult): Message {
    const summaryPreview = result.summary
      .split('\n')
      .slice(0, 10)
      .join('\n');

    const content = `
📦 **对话历史已压缩**

- 压缩消息数: ${result.removedCount}条
- 保留消息数: ${result.compressedMessages.length}条
- 提取记忆: ${result.memories.length}项
- 压缩比例: ${(result.compressionRatio * 100).toFixed(1)}%

压缩后的对话将继续保持上下文完整性。

<details>
<summary>查看压缩摘要</summary>

${summaryPreview}
</details>
    `.trim();

    return {
      id: `msg-compression-${Date.now()}`,
      role: 'system',
      content,
      timestamp: new Date(),
      metadata: {
        type: 'compression',
        removedCount: result.removedCount,
        memoriesCount: result.memories.length,
      },
    };
  }
}

// 导出默认实例
export const defaultConversationCompressor = new ConversationCompressor();
