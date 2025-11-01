'use client';

/**
 * Continuation Dialog - 延续对话对话框
 * 显示对话延续选项和上下文摘要
 */

import React, { useState } from 'react';
import type { ContinuationContext } from '@/lib/services';

interface ContinuationDialogProps {
  isOpen: boolean;
  onClose: () => void;
  context: ContinuationContext | null;
  onConfirm: (context: ContinuationContext) => Promise<void>;
}

export function ContinuationDialog({
  isOpen,
  onClose,
  context,
  onConfirm,
}: ContinuationDialogProps) {
  const [isProcessing, setIsProcessing] = useState(false);
  const [showFullSummary, setShowFullSummary] = useState(false);

  if (!isOpen || !context) return null;

  const handleConfirm = async () => {
    setIsProcessing(true);
    try {
      await onConfirm(context);
      onClose();
    } catch (error) {
      console.error('创建延续对话失败:', error);
      alert('创建延续对话失败,请重试');
    } finally {
      setIsProcessing(false);
    }
  };

  const continuationIndex = context.metadata?.continuationIndex || 1;
  const originalCount = context.metadata?.originalMessageCount || 0;
  const compressionRatio = context.metadata?.compressionRatio || 0;

  // 按类型分组记忆
  const memoryByType = context.memories.reduce(
    (acc, memory) => {
      if (!acc[memory.type]) acc[memory.type] = [];
      acc[memory.type].push(memory);
      return acc;
    },
    {} as Record<string, typeof context.memories>
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div className="w-full max-w-3xl max-h-[90vh] bg-gray-900 border border-gray-700 rounded-xl shadow-2xl overflow-hidden flex flex-col">
        {/* 标题栏 */}
        <div className="px-6 py-4 bg-gray-800 border-b border-gray-700 shrink-0">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <span>🔄</span>
            <span>开启延续对话</span>
          </h2>
          <p className="text-sm text-gray-400 mt-1">
            当前对话已达到长度限制,系统将创建一个新对话并延续当前上下文
          </p>
        </div>

        {/* 内容区域 - 可滚动 */}
        <div className="px-6 py-6 overflow-y-auto flex-1">
          <div className="space-y-6">
            {/* 延续信息 */}
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-gray-800/50 rounded-lg">
                <div className="text-xs text-gray-400 mb-1">原对话ID</div>
                <div className="text-sm text-white font-mono">
                  {context.conversationId.slice(0, 8)}...
                </div>
              </div>
              <div className="p-4 bg-gray-800/50 rounded-lg">
                <div className="text-xs text-gray-400 mb-1">延续序号</div>
                <div className="text-sm text-white font-medium">
                  第 {continuationIndex} 次延续
                </div>
              </div>
            </div>

            {/* 统计信息 */}
            <div className="grid grid-cols-3 gap-3">
              <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-lg text-center">
                <div className="text-xl font-bold text-blue-400">{originalCount}</div>
                <div className="text-xs text-gray-400 mt-1">原始消息数</div>
              </div>
              <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg text-center">
                <div className="text-xl font-bold text-purple-400">
                  {context.memories.length}
                </div>
                <div className="text-xs text-gray-400 mt-1">提取记忆</div>
              </div>
              <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg text-center">
                <div className="text-xl font-bold text-green-400">
                  {(compressionRatio * 100).toFixed(0)}%
                </div>
                <div className="text-xs text-gray-400 mt-1">压缩比例</div>
              </div>
            </div>

            {/* 记忆类型分布 */}
            <div className="p-4 bg-gray-800/50 rounded-lg">
              <h3 className="text-sm font-medium text-gray-300 mb-3 flex items-center gap-2">
                <span>🧠</span>
                <span>已提取的关键记忆</span>
              </h3>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {Object.entries(memoryByType).map(([type, memories]) => (
                  <div
                    key={type}
                    className="flex items-center justify-between py-1.5 px-2 bg-gray-900/50 rounded"
                  >
                    <span className="text-gray-400 capitalize">{type}</span>
                    <span className="text-white font-medium">
                      {memories.length} 项
                      <span className="text-gray-500 ml-1">
                        (重要性: {Math.max(...memories.map(m => m.importance))})
                      </span>
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* 对话摘要 */}
            <div className="p-4 bg-gray-800/50 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-medium text-gray-300 flex items-center gap-2">
                  <span>📝</span>
                  <span>对话摘要</span>
                </h3>
                <button
                  onClick={() => setShowFullSummary(!showFullSummary)}
                  className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
                >
                  {showFullSummary ? '收起' : '展开全部'}
                </button>
              </div>

              <div
                className={`
                  text-xs text-gray-300 leading-relaxed
                  ${showFullSummary ? '' : 'line-clamp-4'}
                `}
              >
                <pre className="whitespace-pre-wrap font-mono">
                  {context.summary}
                </pre>
              </div>
            </div>

            {/* 延续说明 */}
            <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
              <h3 className="text-sm font-medium text-blue-300 mb-2 flex items-center gap-2">
                <span>ℹ️</span>
                <span>延续后会发生什么?</span>
              </h3>
              <ul className="text-xs text-blue-200 space-y-1.5 ml-6 list-disc">
                <li>创建一个新的对话会话,保持与原对话的关联</li>
                <li>自动注入压缩的历史摘要和关键记忆</li>
                <li>继续使用当前智能体: <span className="font-medium">{context.agentName}</span></li>
                <li>原对话保持不变,可随时查看完整历史</li>
                <li>新对话将从空白上下文开始,但包含延续提示</li>
              </ul>
            </div>

            {/* 警告信息 */}
            <div className="p-4 bg-orange-500/10 border border-orange-500/30 rounded-lg">
              <p className="text-xs text-orange-300 flex items-start gap-2">
                <span className="shrink-0">⚠️</span>
                <span>
                  延续后的新对话将无法访问原对话的完整消息历史,只能通过摘要和记忆了解之前的内容。
                  如需查看原始对话,请返回原对话会话。
                </span>
              </p>
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="px-6 py-4 bg-gray-800 border-t border-gray-700 flex justify-end gap-3 shrink-0">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm text-gray-300 hover:text-white transition-colors"
            disabled={isProcessing}
          >
            取消
          </button>
          <button
            onClick={handleConfirm}
            disabled={isProcessing}
            className="
              px-6 py-2 text-sm font-medium
              bg-gradient-to-r from-blue-600 to-purple-600
              hover:from-blue-500 hover:to-purple-500
              text-white rounded-lg
              disabled:opacity-50 disabled:cursor-not-allowed
              transition-all
              shadow-lg shadow-blue-500/20
            "
          >
            {isProcessing ? '创建中...' : '确认并创建新对话'}
          </button>
        </div>
      </div>
    </div>
  );
}
