'use client';

/**
 * Compact Dialog - 压缩对话对话框
 * 显示压缩选项和压缩结果
 */

import React, { useState } from 'react';
import type { Message } from './message-list';
import type { CompressionResult } from '@/lib/services';

interface CompactDialogProps {
  isOpen: boolean;
  onClose: () => void;
  messages: Message[];
  agentName: string;
  onConfirm: (options: {
    keepRecentCount: number;
    keepImportantCount: number;
  }) => Promise<CompressionResult>;
  onApply: (result: CompressionResult) => void;
}

export function CompactDialog({
  isOpen,
  onClose,
  messages,
  agentName,
  onConfirm,
  onApply,
}: CompactDialogProps) {
  const [keepRecentCount, setKeepRecentCount] = useState(20);
  const [keepImportantCount, setKeepImportantCount] = useState(10);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<CompressionResult | null>(null);
  const [step, setStep] = useState<'options' | 'result'>('options');

  if (!isOpen) return null;

  const handleCompress = async () => {
    setIsProcessing(true);
    try {
      const compressionResult = await onConfirm({
        keepRecentCount,
        keepImportantCount,
      });
      setResult(compressionResult);
      setStep('result');
    } catch (error) {
      console.error('压缩失败:', error);
      alert('压缩失败,请重试');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleApply = () => {
    if (result) {
      onApply(result);
      onClose();
    }
  };

  const handleCancel = () => {
    setStep('options');
    setResult(null);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
      <div className="w-full max-w-2xl bg-gray-900 border border-gray-700 rounded-xl shadow-2xl overflow-hidden">
        {/* 标题栏 */}
        <div className="px-6 py-4 bg-gray-800 border-b border-gray-700">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <span>📦</span>
            <span>压缩对话历史</span>
          </h2>
          <p className="text-sm text-gray-400 mt-1">
            智能压缩对话历史,保留重要信息,释放上下文空间
          </p>
        </div>

        {/* 内容区域 */}
        <div className="px-6 py-6">
          {step === 'options' && (
            <div className="space-y-6">
              {/* 当前状态 */}
              <div className="p-4 bg-gray-800/50 rounded-lg">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-400">当前消息数:</span>
                    <span className="ml-2 text-white font-medium">{messages.length} 条</span>
                  </div>
                  <div>
                    <span className="text-gray-400">智能体:</span>
                    <span className="ml-2 text-white font-medium">{agentName}</span>
                  </div>
                </div>
              </div>

              {/* 压缩选项 */}
              <div className="space-y-4">
                {/* 保留最近消息数 */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    保留最近消息数
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min="10"
                      max="50"
                      step="5"
                      value={keepRecentCount}
                      onChange={e => setKeepRecentCount(Number(e.target.value))}
                      className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-white font-mono text-sm w-12 text-right">
                      {keepRecentCount}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    保留最近的对话消息,确保上下文连续性
                  </p>
                </div>

                {/* 保留重要消息数 */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    保留重要历史消息数
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min="5"
                      max="30"
                      step="5"
                      value={keepImportantCount}
                      onChange={e => setKeepImportantCount(Number(e.target.value))}
                      className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-white font-mono text-sm w-12 text-right">
                      {keepImportantCount}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    从历史消息中选择最重要的内容保留
                  </p>
                </div>
              </div>

              {/* 预估结果 */}
              <div className="p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                <p className="text-sm text-blue-300">
                  <span className="font-medium">预估:</span>
                  <span className="ml-2">
                    保留约 {keepRecentCount + keepImportantCount} 条消息,
                    压缩约 {Math.max(0, messages.length - keepRecentCount - keepImportantCount)} 条
                  </span>
                </p>
              </div>
            </div>
          )}

          {step === 'result' && result && (
            <div className="space-y-4">
              {/* 压缩结果统计 */}
              <div className="grid grid-cols-3 gap-4">
                <div className="p-4 bg-gray-800/50 rounded-lg text-center">
                  <div className="text-2xl font-bold text-green-400">
                    {result.compressedMessages.length}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">保留消息</div>
                </div>
                <div className="p-4 bg-gray-800/50 rounded-lg text-center">
                  <div className="text-2xl font-bold text-orange-400">
                    {result.removedCount}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">压缩消息</div>
                </div>
                <div className="p-4 bg-gray-800/50 rounded-lg text-center">
                  <div className="text-2xl font-bold text-blue-400">
                    {result.memories.length}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">提取记忆</div>
                </div>
              </div>

              {/* 压缩比例 */}
              <div className="p-4 bg-gray-800/50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-400">压缩比例</span>
                  <span className="text-sm text-white font-medium">
                    {(result.compressionRatio * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-500 to-blue-500 rounded-full"
                    style={{ width: `${result.compressionRatio * 100}%` }}
                  />
                </div>
              </div>

              {/* 记忆类型分布 */}
              {result.memories.length > 0 && (
                <div className="p-4 bg-gray-800/50 rounded-lg">
                  <h3 className="text-sm font-medium text-gray-300 mb-3">
                    提取的记忆类型
                  </h3>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    {Array.from(new Set(result.memories.map(m => m.type))).map(type => {
                      const count = result.memories.filter(m => m.type === type).length;
                      return (
                        <div key={type} className="flex items-center justify-between">
                          <span className="text-gray-400">{type}</span>
                          <span className="text-white font-medium">{count} 项</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 成功提示 */}
              <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-lg">
                <p className="text-sm text-green-300">
                  ✓ 压缩完成! 对话历史已优化,关键信息已提取保存。
                </p>
              </div>
            </div>
          )}
        </div>

        {/* 操作按钮 */}
        <div className="px-6 py-4 bg-gray-800 border-t border-gray-700 flex justify-end gap-3">
          {step === 'options' && (
            <>
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-sm text-gray-300 hover:text-white transition-colors"
                disabled={isProcessing}
              >
                取消
              </button>
              <button
                onClick={handleCompress}
                disabled={isProcessing}
                className="
                  px-4 py-2 text-sm font-medium
                  bg-blue-600 hover:bg-blue-500
                  text-white rounded-lg
                  disabled:opacity-50 disabled:cursor-not-allowed
                  transition-colors
                "
              >
                {isProcessing ? '压缩中...' : '开始压缩'}
              </button>
            </>
          )}

          {step === 'result' && (
            <>
              <button
                onClick={handleCancel}
                className="px-4 py-2 text-sm text-gray-300 hover:text-white transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleApply}
                className="
                  px-4 py-2 text-sm font-medium
                  bg-green-600 hover:bg-green-500
                  text-white rounded-lg
                  transition-colors
                "
              >
                应用压缩
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
