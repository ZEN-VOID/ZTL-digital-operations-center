'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface TypingIndicatorProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Agent name */
  agentName?: string;
  /** Animation variant */
  variant?: 'dots' | 'pulse' | 'wave';
}

export const TypingIndicator = React.forwardRef<HTMLDivElement, TypingIndicatorProps>(
  ({ className, agentName = 'AI助手', variant = 'dots', ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn('flex gap-3 mb-6 animate-fade-in', className)}
        {...props}
      >
        {/* Avatar */}
        <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-neon-purple/20 border-2 border-neon-purple text-neon-purple flex items-center justify-center font-bold text-sm">
          {agentName.charAt(0)}
        </div>

        {/* Typing content */}
        <div className="flex-1 flex flex-col gap-1">
          {/* Agent name */}
          <div className="flex items-center gap-2 px-1">
            <span className="text-sm font-medium text-neon-purple">{agentName}</span>
            <span className="text-xs text-text-secondary">正在输入...</span>
          </div>

          {/* Typing animation */}
          <div className="max-w-[120px] px-4 py-3 rounded-2xl rounded-tl-sm bg-cyber-bg-secondary/50 border-2 border-neon-purple/30 shadow-[0_0_20px_rgba(176,0,255,0.3)] backdrop-blur-sm">
            {variant === 'dots' && (
              <div className="flex gap-1.5">
                <div className="w-2 h-2 rounded-full bg-neon-purple animate-[typing-dot_1.4s_ease-in-out_infinite]" />
                <div className="w-2 h-2 rounded-full bg-neon-purple animate-[typing-dot_1.4s_ease-in-out_0.2s_infinite]" />
                <div className="w-2 h-2 rounded-full bg-neon-purple animate-[typing-dot_1.4s_ease-in-out_0.4s_infinite]" />
              </div>
            )}

            {variant === 'pulse' && (
              <div className="flex gap-1">
                <div className="w-1.5 h-4 rounded-full bg-neon-purple animate-[typing-pulse_1s_ease-in-out_infinite]" />
                <div className="w-1.5 h-4 rounded-full bg-neon-purple animate-[typing-pulse_1s_ease-in-out_0.15s_infinite]" />
                <div className="w-1.5 h-4 rounded-full bg-neon-purple animate-[typing-pulse_1s_ease-in-out_0.3s_infinite]" />
              </div>
            )}

            {variant === 'wave' && (
              <div className="flex gap-1 items-center">
                <div className="w-1 h-2 rounded-full bg-neon-purple animate-[typing-wave_1.2s_ease-in-out_infinite]" />
                <div className="w-1 h-3 rounded-full bg-neon-purple animate-[typing-wave_1.2s_ease-in-out_0.1s_infinite]" />
                <div className="w-1 h-4 rounded-full bg-neon-purple animate-[typing-wave_1.2s_ease-in-out_0.2s_infinite]" />
                <div className="w-1 h-3 rounded-full bg-neon-purple animate-[typing-wave_1.2s_ease-in-out_0.3s_infinite]" />
                <div className="w-1 h-2 rounded-full bg-neon-purple animate-[typing-wave_1.2s_ease-in-out_0.4s_infinite]" />
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }
);

TypingIndicator.displayName = 'TypingIndicator';
