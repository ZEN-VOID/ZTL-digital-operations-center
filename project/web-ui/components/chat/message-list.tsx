'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';
import { ChatMessage } from './chat-message';
import { TypingIndicator } from './typing-indicator';

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  agentName?: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
  isStreaming?: boolean;
}

export interface MessageListProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Messages to display */
  messages: Message[];
  /** Is agent typing */
  isTyping?: boolean;
  /** Agent name for typing indicator */
  typingAgentName?: string;
  /** Auto-scroll to bottom */
  autoScroll?: boolean;
  /** Show timestamps */
  showTimestamps?: boolean;
  /** Empty state message */
  emptyMessage?: string;
}

export const MessageList = React.forwardRef<HTMLDivElement, MessageListProps>(
  (
    {
      className,
      messages,
      isTyping = false,
      typingAgentName,
      autoScroll = true,
      showTimestamps = true,
      emptyMessage = '开始对话...',
      ...props
    },
    ref
  ) => {
    const messagesEndRef = React.useRef<HTMLDivElement>(null);
    const containerRef = React.useRef<HTMLDivElement>(null);
    const [isUserScrolling, setIsUserScrolling] = React.useState(false);

    // Auto-scroll to bottom when new messages arrive
    const scrollToBottom = React.useCallback((behavior: ScrollBehavior = 'smooth') => {
      messagesEndRef.current?.scrollIntoView({ behavior });
    }, []);

    React.useEffect(() => {
      if (autoScroll && !isUserScrolling) {
        scrollToBottom();
      }
    }, [messages, isTyping, autoScroll, isUserScrolling, scrollToBottom]);

    // Detect user scrolling
    React.useEffect(() => {
      const container = containerRef.current;
      if (!container) return;

      let scrollTimeout: NodeJS.Timeout;

      const handleScroll = () => {
        const { scrollTop, scrollHeight, clientHeight } = container;
        const isAtBottom = Math.abs(scrollHeight - clientHeight - scrollTop) < 50;

        if (!isAtBottom) {
          setIsUserScrolling(true);
          clearTimeout(scrollTimeout);
          scrollTimeout = setTimeout(() => {
            setIsUserScrolling(false);
          }, 2000);
        } else {
          setIsUserScrolling(false);
        }
      };

      container.addEventListener('scroll', handleScroll, { passive: true });

      return () => {
        container.removeEventListener('scroll', handleScroll);
        clearTimeout(scrollTimeout);
      };
    }, []);

    // Scroll to bottom on initial load
    React.useEffect(() => {
      scrollToBottom('instant');
    }, [scrollToBottom]);

    return (
      <div
        ref={ref}
        className={cn('relative flex flex-col h-full', className)}
        {...props}
      >
        {/* Messages container */}
        <div
          ref={containerRef}
          className={cn(
            'flex-1 overflow-y-auto px-4 py-6',
            'scrollbar-thin scrollbar-thumb-neon-cyan/30 scrollbar-track-transparent'
          )}
        >
          {messages.length === 0 ? (
            // Empty state
            <div className="flex items-center justify-center h-full">
              <div className="text-center space-y-4 animate-fade-in">
                <div className="w-20 h-20 mx-auto rounded-2xl bg-neon-purple/10 border-2 border-neon-purple/30 flex items-center justify-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="40"
                    height="40"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="text-neon-purple"
                  >
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                  </svg>
                </div>
                <div>
                  <p className="text-lg font-medium text-text-primary font-orbitron">
                    {emptyMessage}
                  </p>
                  <p className="text-sm text-text-secondary mt-2">
                    输入消息或使用 / 命令开始
                  </p>
                </div>
              </div>
            </div>
          ) : (
            // Messages
            <div className="space-y-4">
              {messages.map((message) => (
                <ChatMessage
                  key={message.id}
                  content={message.content}
                  role={message.role}
                  agentName={message.agentName}
                  timestamp={message.timestamp}
                  showTimestamp={showTimestamps}
                  status={message.status}
                  isStreaming={message.isStreaming}
                />
              ))}

              {/* Typing indicator */}
              {isTyping && <TypingIndicator agentName={typingAgentName} />}

              {/* Scroll anchor */}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Scroll to bottom button */}
        {isUserScrolling && messages.length > 0 && (
          <button
            onClick={() => {
              scrollToBottom();
              setIsUserScrolling(false);
            }}
            className={cn(
              'absolute bottom-4 right-4 z-10',
              'w-10 h-10 rounded-full',
              'bg-neon-cyan/20 border-2 border-neon-cyan',
              'text-neon-cyan shadow-[0_0_20px_rgba(0,255,255,0.5)]',
              'hover:bg-neon-cyan/30 hover:shadow-[0_0_30px_rgba(0,255,255,0.7)]',
              'transition-all duration-300',
              'flex items-center justify-center',
              'animate-fade-in'
            )}
            aria-label="滚动到底部"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="m18 15-6 6-6-6" />
              <path d="M12 3v18" />
            </svg>
          </button>
        )}
      </div>
    );
  }
);

MessageList.displayName = 'MessageList';
