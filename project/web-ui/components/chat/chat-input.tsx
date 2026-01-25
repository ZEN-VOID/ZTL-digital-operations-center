'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';
import { Button } from '@/components/ui/button';

export interface ChatInputProps
  extends Omit<React.HTMLAttributes<HTMLDivElement>, 'onChange' | 'onSubmit'> {
  /** Input value */
  value: string;
  /** On value change */
  onChange: (value: string) => void;
  /** On submit */
  onSubmit: (message: string) => void;
  /** Is loading/processing */
  isLoading?: boolean;
  /** Placeholder text */
  placeholder?: string;
  /** Show command suggestions */
  showCommandSuggestions?: boolean;
  /** On command select */
  onCommandSelect?: (command: string) => void;
  /** Disabled state */
  disabled?: boolean;
}

const COMMANDS = [
  { name: '/help', description: '显示帮助信息' },
  { name: '/clear', description: '清除对话历史' },
  { name: '/switch', description: '切换智能体' },
];

export const ChatInput = React.forwardRef<HTMLDivElement, ChatInputProps>(
  (
    {
      className,
      value,
      onChange,
      onSubmit,
      isLoading = false,
      placeholder = '输入消息... (/ 显示命令)',
      showCommandSuggestions = true,
      onCommandSelect,
      disabled = false,
      ...props
    },
    ref
  ) => {
    const [showCommands, setShowCommands] = React.useState(false);
    const textareaRef = React.useRef<HTMLTextAreaElement>(null);

    // Auto-resize textarea
    React.useEffect(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
        textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
      }
    }, [value]);

    // Show command suggestions when typing /
    React.useEffect(() => {
      if (showCommandSuggestions && value.startsWith('/') && value.length > 0) {
        setShowCommands(true);
      } else {
        setShowCommands(false);
      }
    }, [value, showCommandSuggestions]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
    };

    const handleSubmit = () => {
      if (!value.trim() || isLoading || disabled) return;
      onSubmit(value);
    };

    const handleCommandClick = (command: string) => {
      onChange(command + ' ');
      setShowCommands(false);
      onCommandSelect?.(command);
      textareaRef.current?.focus();
    };

    const filteredCommands = COMMANDS.filter((cmd) =>
      cmd.name.toLowerCase().includes(value.toLowerCase())
    );

    return (
      <div ref={ref} className={cn('relative w-full', className)} {...props}>
        {/* Command suggestions */}
        {showCommands && filteredCommands.length > 0 && (
          <div className="absolute bottom-full left-0 right-0 mb-2 bg-cyber-bg-secondary/95 backdrop-blur-md border-2 border-neon-purple/30 rounded-lg shadow-[0_0_30px_rgba(176,0,255,0.3)] overflow-hidden animate-slide-up">
            <div className="p-2 space-y-1">
              {filteredCommands.map((cmd) => (
                <button
                  key={cmd.name}
                  type="button"
                  onClick={() => handleCommandClick(cmd.name)}
                  className={cn(
                    'w-full px-3 py-2 text-left rounded-md transition-all duration-200',
                    'hover:bg-neon-purple/20 hover:shadow-[0_0_15px_rgba(176,0,255,0.3)]',
                    'focus:outline-none focus:bg-neon-purple/20'
                  )}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-bold text-neon-purple font-orbitron">
                      {cmd.name}
                    </span>
                    <span className="text-xs text-text-secondary">{cmd.description}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input container */}
        <div
          className={cn(
            'flex items-end gap-3 p-4 rounded-2xl border-2 transition-all duration-300',
            'bg-cyber-bg-secondary/50 backdrop-blur-sm',
            disabled || isLoading
              ? 'border-text-secondary/20'
              : 'border-neon-cyan/30 focus-within:border-neon-cyan focus-within:shadow-[0_0_30px_rgba(0,255,255,0.3)]'
          )}
        >
          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled || isLoading}
            rows={1}
            className={cn(
              'flex-1 bg-transparent border-none outline-none resize-none',
              'text-base text-text-primary placeholder:text-text-secondary/50',
              'font-electrolize',
              'max-h-32 overflow-y-auto',
              'scrollbar-thin scrollbar-thumb-neon-cyan/30 scrollbar-track-transparent'
            )}
          />

          {/* Send button */}
          <Button
            size="icon"
            variant="neon-cyan"
            onClick={handleSubmit}
            disabled={!value.trim() || isLoading || disabled}
            className="flex-shrink-0"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-neon-cyan border-t-transparent rounded-full animate-spin" />
            ) : (
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
                <path d="m22 2-7 20-4-9-9-4Z" />
                <path d="M22 2 11 13" />
              </svg>
            )}
          </Button>
        </div>

        {/* Character count / tips */}
        <div className="flex items-center justify-between mt-2 px-1">
          <span className="text-xs text-text-secondary">
            {value.length > 0 && `${value.length} 字符`}
          </span>
          <span className="text-xs text-text-secondary">
            Enter 发送 • Shift+Enter 换行
          </span>
        </div>
      </div>
    );
  }
);

ChatInput.displayName = 'ChatInput';
