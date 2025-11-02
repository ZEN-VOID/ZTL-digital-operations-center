import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface ChatMessageProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Message content */
  content: string;
  /** Message role */
  role: 'user' | 'assistant' | 'system';
  /** Agent name (for assistant messages) */
  agentName?: string;
  /** Message timestamp */
  timestamp?: Date | string;
  /** Show timestamp */
  showTimestamp?: boolean;
  /** Message status */
  status?: 'sending' | 'sent' | 'error';
  /** Is streaming (for assistant messages) */
  isStreaming?: boolean;
}

const ChatMessage = React.forwardRef<HTMLDivElement, ChatMessageProps>(
  (
    {
      className,
      content,
      role,
      agentName,
      timestamp,
      showTimestamp = true,
      status = 'sent',
      isStreaming = false,
      ...props
    },
    ref
  ) => {
    const isUser = role === 'user';
    const isSystem = role === 'system';

    const formatTimestamp = (ts: Date | string) => {
      const date = typeof ts === 'string' ? new Date(ts) : ts;
      return date.toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit',
      });
    };

    if (isSystem) {
      return (
        <div
          ref={ref}
          className={cn(
            'flex justify-center my-4 animate-message-appear',
            className
          )}
          {...props}
        >
          <div className="px-4 py-1.5 rounded-full bg-cyber-bg-secondary/30 border border-text-secondary/20 text-xs text-text-secondary">
            {content}
          </div>
        </div>
      );
    }

    return (
      <div
        ref={ref}
        className={cn(
          'flex gap-3 mb-6 animate-message-appear',
          isUser ? 'flex-row-reverse' : 'flex-row',
          className
        )}
        {...props}
      >
        {/* Avatar */}
        <div
          className={cn(
            'flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm',
            isUser
              ? 'bg-neon-cyan/20 border-2 border-neon-cyan text-neon-cyan'
              : 'bg-neon-purple/20 border-2 border-neon-purple text-neon-purple'
          )}
        >
          {isUser ? 'U' : agentName?.charAt(0) || 'A'}
        </div>

        {/* Message content */}
        <div className={cn('flex-1 flex flex-col gap-1', isUser ? 'items-end' : 'items-start')}>
          {/* Header */}
          {!isUser && agentName && (
            <div className="flex items-center gap-2 px-1">
              <span className="text-sm font-medium text-neon-purple">{agentName}</span>
              {timestamp && showTimestamp && (
                <span className="text-xs text-text-secondary">{formatTimestamp(timestamp)}</span>
              )}
            </div>
          )}

          {/* Message bubble */}
          <div
            className={cn(
              'group relative max-w-[80%] px-4 py-3 rounded-2xl transition-all duration-300',
              'backdrop-blur-sm',
              isUser
                ? 'bg-neon-cyan/10 border-2 border-neon-cyan/30 text-text-primary rounded-tr-sm'
                : 'bg-cyber-bg-secondary/50 border-2 border-neon-purple/30 text-text-primary rounded-tl-sm',
              isStreaming && 'shadow-[0_0_20px_rgba(176,0,255,0.3)] animate-streaming-pulse',
              status === 'error' && 'border-neon-pink bg-neon-pink/10'
            )}
          >
            <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">{content}</p>

            {/* Streaming indicator */}
            {isStreaming && (
              <div className="flex gap-1 mt-2">
                <div className="w-1.5 h-1.5 rounded-full bg-neon-purple animate-[neon-pulse_1s_ease-in-out_infinite]" />
                <div className="w-1.5 h-1.5 rounded-full bg-neon-purple animate-[neon-pulse_1s_ease-in-out_0.2s_infinite]" />
                <div className="w-1.5 h-1.5 rounded-full bg-neon-purple animate-[neon-pulse_1s_ease-in-out_0.4s_infinite]" />
              </div>
            )}

            {/* Status indicator */}
            {status === 'sending' && isUser && (
              <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-text-secondary/50 flex items-center justify-center">
                <div className="w-2 h-2 rounded-full border-2 border-text-primary border-t-transparent animate-spin" />
              </div>
            )}

            {status === 'error' && (
              <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-neon-pink flex items-center justify-center">
                <span className="text-xs text-white">!</span>
              </div>
            )}
          </div>

          {/* User timestamp */}
          {isUser && timestamp && showTimestamp && (
            <span className="text-xs text-text-secondary px-1">{formatTimestamp(timestamp)}</span>
          )}
        </div>
      </div>
    );
  }
);

ChatMessage.displayName = 'ChatMessage';

export { ChatMessage };
