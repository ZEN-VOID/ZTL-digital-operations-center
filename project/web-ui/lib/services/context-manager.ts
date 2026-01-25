/**
 * Context Manager - 对话上下文管理器
 * 负责监控对话长度,评估上下文状态,决定何时需要压缩
 */

export interface ContextThresholds {
  warningThreshold: number; // 警告阈值 (消息数)
  compactThreshold: number; // 压缩阈值 (消息数)
  maxMessages: number; // 最大消息数
}

export type ContextStatus =
  | 'normal' // 正常状态
  | 'approaching_limit' // 接近限制
  | 'should_compact' // 应该压缩
  | 'must_compact'; // 必须压缩

export interface ContextAssessment {
  status: ContextStatus;
  percentage: number;
  recommendation: string;
  shouldShowWarning: boolean;
  canContinue: boolean;
}

export class ContextManager {
  private thresholds: ContextThresholds;

  constructor(thresholds?: Partial<ContextThresholds>) {
    this.thresholds = {
      warningThreshold: 50, // 50条消息提示
      compactThreshold: 80, // 80条消息压缩
      maxMessages: 100, // 100条消息硬限制
      ...thresholds,
    };
  }

  /**
   * 评估上下文状态
   */
  assessContextStatus(messageCount: number): ContextAssessment {
    const percentage = (messageCount / this.thresholds.maxMessages) * 100;

    if (messageCount >= this.thresholds.maxMessages) {
      return {
        status: 'must_compact',
        percentage,
        recommendation: '已达上下文限制,必须压缩或开启新对话',
        shouldShowWarning: true,
        canContinue: false,
      };
    }

    if (messageCount >= this.thresholds.compactThreshold) {
      return {
        status: 'should_compact',
        percentage,
        recommendation: '建议压缩对话历史以优化性能',
        shouldShowWarning: true,
        canContinue: true,
      };
    }

    if (messageCount >= this.thresholds.warningThreshold) {
      return {
        status: 'approaching_limit',
        percentage,
        recommendation: '对话历史较长,可能需要压缩',
        shouldShowWarning: true,
        canContinue: true,
      };
    }

    return {
      status: 'normal',
      percentage,
      recommendation: '上下文正常',
      shouldShowWarning: false,
      canContinue: true,
    };
  }

  /**
   * 检查是否需要自动压缩
   */
  shouldAutoCompact(messageCount: number): boolean {
    return messageCount >= this.thresholds.compactThreshold;
  }

  /**
   * 检查是否可以继续发送消息
   */
  canSendMessage(messageCount: number): boolean {
    return messageCount < this.thresholds.maxMessages;
  }

  /**
   * 获取状态对应的颜色 (用于UI)
   */
  getStatusColor(status: ContextStatus): string {
    switch (status) {
      case 'normal':
        return '#00ff88'; // neon-green
      case 'approaching_limit':
        return '#00ffff'; // neon-cyan
      case 'should_compact':
        return '#ffaa00'; // warning-yellow
      case 'must_compact':
        return '#ff0080'; // neon-pink
      default:
        return '#00ffff';
    }
  }

  /**
   * 获取状态对应的标签 (用于UI)
   */
  getStatusLabel(status: ContextStatus): string {
    switch (status) {
      case 'normal':
        return '充足';
      case 'approaching_limit':
        return '正常';
      case 'should_compact':
        return '建议压缩';
      case 'must_compact':
        return '接近上限';
      default:
        return '未知';
    }
  }

  /**
   * 更新阈值配置
   */
  updateThresholds(newThresholds: Partial<ContextThresholds>): void {
    this.thresholds = {
      ...this.thresholds,
      ...newThresholds,
    };
  }

  /**
   * 获取当前阈值配置
   */
  getThresholds(): ContextThresholds {
    return { ...this.thresholds };
  }
}

// 导出默认实例
export const defaultContextManager = new ContextManager();
