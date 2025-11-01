/**
 * Continuation Generator - 对话延续生成器
 * 生成新对话的初始化提示,用于延续压缩的历史对话
 */

import type { Message } from '@/components/chat/message-list';
import type { ExtractedMemory } from './memory-extractor';

export interface ContinuationContext {
  conversationId: string;
  agentName: string;
  summary: string; // 压缩摘要
  memories: ExtractedMemory[]; // 提取的记忆
  lastMessages: Message[]; // 最后几条消息(用于无缝衔接)
  metadata?: {
    originalMessageCount?: number;
    compressionRatio?: number;
    continuationIndex?: number;
  };
}

export class ContinuationGenerator {
  /**
   * 生成延续会话的系统提示
   * 用于在新对话开始时注入上下文
   */
  generateContinuationPrompt(context: ContinuationContext): string {
    const sections: string[] = [];

    // 1. 标题和基本信息
    sections.push('# 对话延续上下文');
    sections.push('');
    sections.push(`这是一个延续的对话会话,延续自对话ID: ${context.conversationId}`);
    sections.push(`当前智能体: ${context.agentName}`);

    if (context.metadata?.continuationIndex) {
      sections.push(`延续序号: 第${context.metadata.continuationIndex}次延续`);
    }

    sections.push('');

    // 2. 压缩摘要
    sections.push('## 对话历史摘要');
    sections.push('');
    sections.push(context.summary);
    sections.push('');

    // 3. 提取的关键记忆(按重要性排序)
    if (context.memories.length > 0) {
      sections.push('## 关键记忆');
      sections.push('');

      const sortedMemories = [...context.memories]
        .sort((a, b) => b.importance - a.importance);

      // 按类型分组显示
      const memoryByType = this.groupMemoriesByType(sortedMemories);

      Object.entries(memoryByType).forEach(([type, memories]) => {
        if (memories.length > 0) {
          sections.push(`### ${this.getMemoryTypeLabel(type)}`);
          sections.push('');
          memories.forEach(memory => {
            sections.push(memory.content);
            sections.push('');
          });
        }
      });
    }

    // 4. 最后几条消息(用于无缝衔接)
    if (context.lastMessages.length > 0) {
      sections.push('## 最近对话');
      sections.push('');
      sections.push('以下是上次对话的最后几条消息,用于保持上下文连续性:');
      sections.push('');

      context.lastMessages.forEach((msg, index) => {
        const role = this.getRoleLabel(msg.role);
        const timestamp = msg.timestamp
          ? ` (${msg.timestamp.toLocaleTimeString('zh-CN')})`
          : '';

        sections.push(`**${role}**${timestamp}:`);
        sections.push(msg.content);
        sections.push('');
      });
    }

    // 5. 延续指引
    sections.push('---');
    sections.push('');
    sections.push('## 延续指引');
    sections.push('');
    sections.push('请基于以上上下文继续对话,保持以下原则:');
    sections.push('1. **上下文连贯性**: 记住历史摘要和关键记忆中的信息');
    sections.push('2. **无缝衔接**: 自然地从最后几条消息继续对话');
    sections.push('3. **知识延续**: 应用已提取的错误学习和成功经验');
    sections.push('4. **任务延续**: 继续处理待办事项和未完成的工作');
    sections.push('');

    // 6. 元数据(可选)
    if (context.metadata) {
      sections.push('## 对话统计');
      sections.push('');
      if (context.metadata.originalMessageCount) {
        sections.push(`- 原始消息数: ${context.metadata.originalMessageCount}条`);
      }
      if (context.metadata.compressionRatio !== undefined) {
        sections.push(`- 压缩比例: ${(context.metadata.compressionRatio * 100).toFixed(1)}%`);
      }
      sections.push('');
    }

    return sections.join('\n');
  }

  /**
   * 创建延续会话的初始化消息
   * 作为新对话的第一条系统消息
   */
  createContinuationMessage(
    context: ContinuationContext
  ): Message {
    const prompt = this.generateContinuationPrompt(context);

    return {
      id: `msg-continuation-${Date.now()}`,
      role: 'system',
      content: prompt,
      timestamp: new Date(),
      metadata: {
        type: 'continuation',
        conversationId: context.conversationId,
        continuationIndex: context.metadata?.continuationIndex || 1,
      },
    };
  }

  /**
   * 创建用户可见的延续通知消息
   */
  createContinuationNotification(
    context: ContinuationContext
  ): Message {
    const continuationIndex = context.metadata?.continuationIndex || 1;
    const originalCount = context.metadata?.originalMessageCount || 0;
    const memoryCount = context.memories.length;

    const content = `
🔄 **对话已延续**

这是延续对话的第${continuationIndex}个会话。

- 原对话ID: \`${context.conversationId}\`
- 历史消息数: ${originalCount}条
- 已提取记忆: ${memoryCount}项
- 智能体: ${context.agentName}

延续对话将保持上下文连贯性,您可以继续之前的讨论。

<details>
<summary>查看上下文摘要</summary>

${context.summary.split('\n').slice(0, 15).join('\n')}

${context.summary.split('\n').length > 15 ? '...' : ''}
</details>
    `.trim();

    return {
      id: `msg-continuation-notification-${Date.now()}`,
      role: 'system',
      content,
      timestamp: new Date(),
      metadata: {
        type: 'continuation_notification',
        conversationId: context.conversationId,
      },
    };
  }

  /**
   * 从压缩结果生成延续上下文
   */
  createContextFromCompression(
    conversationId: string,
    agentName: string,
    compressionResult: {
      compressedMessages: Message[];
      summary: string;
      removedCount: number;
      memories: ExtractedMemory[];
      compressionRatio: number;
    },
    originalMessageCount: number,
    continuationIndex: number = 1
  ): ContinuationContext {
    // 取最后5条消息作为无缝衔接
    const lastMessages = compressionResult.compressedMessages.slice(-5);

    return {
      conversationId,
      agentName,
      summary: compressionResult.summary,
      memories: compressionResult.memories,
      lastMessages,
      metadata: {
        originalMessageCount,
        compressionRatio: compressionResult.compressionRatio,
        continuationIndex,
      },
    };
  }

  /**
   * 验证延续上下文的有效性
   */
  validateContinuationContext(context: ContinuationContext): {
    valid: boolean;
    errors: string[];
  } {
    const errors: string[] = [];

    if (!context.conversationId) {
      errors.push('缺少对话ID');
    }

    if (!context.agentName) {
      errors.push('缺少智能体名称');
    }

    if (!context.summary || context.summary.trim().length === 0) {
      errors.push('缺少对话摘要');
    }

    if (!context.memories || context.memories.length === 0) {
      errors.push('缺少提取的记忆');
    }

    if (!context.lastMessages || context.lastMessages.length === 0) {
      errors.push('缺少最后几条消息');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * 估算延续提示的token数量(粗略估算)
   */
  estimatePromptTokens(context: ContinuationContext): number {
    const prompt = this.generateContinuationPrompt(context);

    // 粗略估算: 中文1字 ≈ 2 tokens, 英文1词 ≈ 1.3 tokens
    const chineseChars = (prompt.match(/[\u4e00-\u9fa5]/g) || []).length;
    const englishWords = (prompt.match(/[a-zA-Z]+/g) || []).length;

    return Math.ceil(chineseChars * 2 + englishWords * 1.3);
  }

  /**
   * 获取记忆类型的中文标签
   */
  private getMemoryTypeLabel(type: string): string {
    const labels: Record<string, string> = {
      focus: '📌 当前焦点',
      todo: '✅ 待办事项',
      process: '🔄 工作流程',
      error: '❌ 错误学习',
      success: '✨ 成功经验',
      insights: '💡 洞察发现',
      patterns: '🔍 模式积累',
      context: '📋 项目背景',
      memory: '🧠 长期记忆',
      snapshot: '📸 状态快照',
    };
    return labels[type] || type.toUpperCase();
  }

  /**
   * 获取角色的中文标签
   */
  private getRoleLabel(role: string): string {
    const labels: Record<string, string> = {
      user: '用户',
      assistant: '助手',
      system: '系统',
    };
    return labels[role] || role;
  }

  /**
   * 按类型分组记忆
   */
  private groupMemoriesByType(
    memories: ExtractedMemory[]
  ): Record<string, ExtractedMemory[]> {
    const grouped: Record<string, ExtractedMemory[]> = {};

    memories.forEach(memory => {
      if (!grouped[memory.type]) {
        grouped[memory.type] = [];
      }
      grouped[memory.type].push(memory);
    });

    return grouped;
  }

  /**
   * 生成简短的延续说明(用于UI显示)
   */
  generateShortDescription(context: ContinuationContext): string {
    const memoryCount = context.memories.length;
    const continuationIndex = context.metadata?.continuationIndex || 1;

    return `延续自对话 ${context.conversationId.slice(0, 8)}... (第${continuationIndex}次延续, ${memoryCount}项记忆)`;
  }
}

// 导出默认实例
export const defaultContinuationGenerator = new ContinuationGenerator();
