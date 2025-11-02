'use client';

/**
 * Context Status Bar - 上下文状态栏组件
 * 显示对话上下文使用情况和状态
 */

import React from 'react';
import { defaultContextManager, type ContextStatus } from '@/lib/services';

interface ContextStatusBarProps {
  messageCount: number;
  onCompactClick?: () => void;
  onContinueClick?: () => void;
  className?: string;
}

export function ContextStatusBar({
  messageCount,
  onCompactClick,
  onContinueClick,
  className = '',
}: ContextStatusBarProps) {
  const assessment = defaultContextManager.assessContextStatus(messageCount);

  // 获取状态颜色(霓虹色系)
  const statusColor = defaultContextManager.getStatusColor(assessment.status);
  const statusLabel = defaultContextManager.getStatusLabel(assessment.status);

  // 决定显示哪些按钮
  const showCompactButton = assessment.status === 'should_compact' || assessment.status === 'must_compact';
  const showContinueButton = assessment.status === 'must_compact';

  // 状态图标
  const getStatusIcon = (status: ContextStatus) => {
    switch (status) {
      case 'normal':
        return '✓';
      case 'approaching_limit':
        return '⚡';
      case 'should_compact':
        return '⚠️';
      case 'must_compact':
        return '🔴';
      default:
        return '•';
    }
  };

  return (
    <div
      className={`
        flex items-center justify-between
        px-4 py-2
        bg-gray-900/50 backdrop-blur-sm
        border-b border-gray-800
        ${className}
      `}
    >
      {/* 左侧: 状态信息 */}
      <div className="flex items-center gap-3">
        {/* 状态图标 */}
        <span className="text-lg" aria-label={`状态: ${statusLabel}`}>
          {getStatusIcon(assessment.status)}
        </span>

        {/* 状态文本 */}
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <span
              className="text-sm font-medium"
              style={{ color: statusColor }}
            >
              {statusLabel}
            </span>
            <span className="text-xs text-gray-500">
              {messageCount} 条消息
            </span>
          </div>

          {/* 建议文本 */}
          {assessment.shouldShowWarning && (
            <span className="text-xs text-gray-400">
              {assessment.recommendation}
            </span>
          )}
        </div>

        {/* 进度条 */}
        <div className="flex items-center gap-2 ml-4">
          <div className="w-32 h-1.5 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full transition-all duration-300 ease-out rounded-full"
              style={{
                width: `${assessment.percentage}%`,
                backgroundColor: statusColor,
                boxShadow: `0 0 8px ${statusColor}`,
              }}
            />
          </div>
          <span className="text-xs text-gray-500 font-mono">
            {Math.round(assessment.percentage)}%
          </span>
        </div>
      </div>

      {/* 右侧: 操作按钮 */}
      <div className="flex items-center gap-2">
        {showCompactButton && onCompactClick && (
          <button
            onClick={onCompactClick}
            className="
              px-3 py-1.5 text-xs font-medium
              bg-gray-800 hover:bg-gray-700
              text-gray-300 hover:text-white
              border border-gray-700
              rounded-lg
              transition-colors
              flex items-center gap-1.5
            "
          >
            <span>📦</span>
            <span>压缩历史</span>
          </button>
        )}

        {showContinueButton && onContinueClick && (
          <button
            onClick={onContinueClick}
            className="
              px-3 py-1.5 text-xs font-medium
              bg-neon-pink/20 hover:bg-neon-pink/30
              text-neon-pink hover:text-white
              border border-neon-pink/50
              rounded-lg
              transition-colors
              flex items-center gap-1.5
            "
            style={{
              boxShadow: '0 0 12px rgba(255, 0, 128, 0.3)',
            }}
          >
            <span>🔄</span>
            <span>开启新对话</span>
          </button>
        )}
      </div>
    </div>
  );
}

/**
 * 简化版状态栏(只显示图标和百分比)
 */
export function CompactContextStatusBar({
  messageCount,
  className = '',
}: {
  messageCount: number;
  className?: string;
}) {
  const assessment = defaultContextManager.assessContextStatus(messageCount);
  const statusColor = defaultContextManager.getStatusColor(assessment.status);

  return (
    <div
      className={`
        flex items-center gap-2
        px-2 py-1
        ${className}
      `}
      title={assessment.recommendation}
    >
      <div className="w-16 h-1 bg-gray-800 rounded-full overflow-hidden">
        <div
          className="h-full transition-all duration-300"
          style={{
            width: `${assessment.percentage}%`,
            backgroundColor: statusColor,
          }}
        />
      </div>
      <span className="text-xs text-gray-500 font-mono">
        {Math.round(assessment.percentage)}%
      </span>
    </div>
  );
}
