/**
 * Conversation Continuation System - Service Layer Exports
 * 对话延续系统 - 服务层导出
 *
 * 此文件统一导出所有对话延续相关的服务和类型
 */

// ============================================================
// Core Services
// ============================================================

export {
  ContextManager,
  defaultContextManager,
  type ContextThresholds,
  type ContextStatus,
  type ContextAssessment,
} from './context-manager';

export {
  MemoryExtractor,
  defaultMemoryExtractor,
  type MemoryType,
  type ExtractedMemory,
} from './memory-extractor';

export {
  ConversationCompressor,
  defaultConversationCompressor,
  type CompressionOptions,
  type CompressionResult,
} from './conversation-compressor';

export {
  ContinuationGenerator,
  defaultContinuationGenerator,
  type ContinuationContext,
} from './continuation-generator';

export {
  ConversationService,
  conversationService,
  type Conversation,
  type ConversationMemory,
  type ConversationSnapshot,
  type TriggerReason,
} from './conversation-service';

// ============================================================
// Convenience Re-exports
// ============================================================

// 导出所有默认实例(便于快速使用)
export const conversationContinuationSystem = {
  contextManager: defaultContextManager,
  memoryExtractor: defaultMemoryExtractor,
  compressor: defaultConversationCompressor,
  continuationGenerator: defaultContinuationGenerator,
  service: conversationService,
};

// ============================================================
// Type Guards
// ============================================================

export function isValidMemoryType(type: string): type is MemoryType {
  return [
    'focus',
    'todo',
    'process',
    'error',
    'success',
    'insights',
    'patterns',
    'context',
    'memory',
    'snapshot',
  ].includes(type);
}

export function isValidContextStatus(status: string): status is ContextStatus {
  return ['normal', 'approaching_limit', 'should_compact', 'must_compact'].includes(status);
}

export function isValidTriggerReason(reason: string): reason is TriggerReason {
  return ['manual', 'auto_compact', 'context_limit', 'session_end'].includes(reason);
}
