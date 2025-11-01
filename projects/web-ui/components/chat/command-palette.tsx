'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface Command {
  id: string;
  name: string;
  description: string;
  icon?: React.ReactNode;
  shortcut?: string;
  group?: string;
  onExecute: () => void;
}

export interface CommandPaletteProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Is open */
  isOpen: boolean;
  /** On close */
  onClose: () => void;
  /** Available commands */
  commands: Command[];
  /** Search placeholder */
  searchPlaceholder?: string;
}

export const CommandPalette = React.forwardRef<HTMLDivElement, CommandPaletteProps>(
  (
    {
      className,
      isOpen,
      onClose,
      commands,
      searchPlaceholder = '搜索命令...',
      ...props
    },
    ref
  ) => {
    const [search, setSearch] = React.useState('');
    const [selectedIndex, setSelectedIndex] = React.useState(0);
    const inputRef = React.useRef<HTMLInputElement>(null);

    // Filter commands based on search
    const filteredCommands = React.useMemo(() => {
      if (!search.trim()) return commands;

      const query = search.toLowerCase();
      return commands.filter(
        (cmd) =>
          cmd.name.toLowerCase().includes(query) ||
          cmd.description.toLowerCase().includes(query) ||
          cmd.group?.toLowerCase().includes(query)
      );
    }, [commands, search]);

    // Group filtered commands
    const groupedCommands = React.useMemo(() => {
      return filteredCommands.reduce(
        (acc, cmd) => {
          const group = cmd.group || '其他';
          if (!acc[group]) {
            acc[group] = [];
          }
          acc[group].push(cmd);
          return acc;
        },
        {} as Record<string, Command[]>
      );
    }, [filteredCommands]);

    // Focus input when opened
    React.useEffect(() => {
      if (isOpen) {
        inputRef.current?.focus();
        setSearch('');
        setSelectedIndex(0);
      }
    }, [isOpen]);

    // Handle keyboard navigation
    React.useEffect(() => {
      const handleKeyDown = (e: KeyboardEvent) => {
        if (!isOpen) return;

        switch (e.key) {
          case 'ArrowDown':
            e.preventDefault();
            setSelectedIndex((prev) => Math.min(prev + 1, filteredCommands.length - 1));
            break;
          case 'ArrowUp':
            e.preventDefault();
            setSelectedIndex((prev) => Math.max(prev - 1, 0));
            break;
          case 'Enter':
            e.preventDefault();
            if (filteredCommands[selectedIndex]) {
              handleCommandExecute(filteredCommands[selectedIndex]);
            }
            break;
          case 'Escape':
            e.preventDefault();
            onClose();
            break;
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    }, [isOpen, selectedIndex, filteredCommands, onClose]);

    const handleCommandExecute = (command: Command) => {
      command.onExecute();
      onClose();
    };

    if (!isOpen) return null;

    return (
      <>
        {/* Backdrop */}
        <div
          className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm animate-fade-in"
          onClick={onClose}
          aria-hidden="true"
        />

        {/* Command palette */}
        <div
          ref={ref}
          className={cn(
            'fixed top-[20%] left-1/2 -translate-x-1/2 z-50',
            'w-full max-w-2xl',
            'bg-cyber-bg-secondary/95 backdrop-blur-md',
            'border-2 border-neon-cyan/30 rounded-2xl',
            'shadow-[0_0_60px_rgba(0,255,255,0.4)]',
            'animate-slide-down',
            className
          )}
          {...props}
        >
          {/* Search input */}
          <div className="p-4 border-b-2 border-text-secondary/10">
            <div className="relative">
              {/* Search icon */}
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
                className="absolute left-3 top-1/2 -translate-y-1/2 text-neon-cyan"
              >
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>

              <input
                ref={inputRef}
                type="text"
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setSelectedIndex(0);
                }}
                placeholder={searchPlaceholder}
                className={cn(
                  'w-full h-12 pl-11 pr-4 bg-transparent',
                  'border-none outline-none',
                  'text-base text-text-primary placeholder:text-text-secondary/50',
                  'font-electrolize'
                )}
              />
            </div>
          </div>

          {/* Commands list */}
          <div className="max-h-[400px] overflow-y-auto scrollbar-thin scrollbar-thumb-neon-cyan/30 scrollbar-track-transparent">
            {Object.keys(groupedCommands).length === 0 ? (
              // Empty state
              <div className="p-8 text-center">
                <p className="text-text-secondary">未找到匹配的命令</p>
              </div>
            ) : (
              <div className="p-2">
                {Object.entries(groupedCommands).map(([group, groupCommands]) => (
                  <div key={group} className="mb-4 last:mb-2">
                    {/* Group header */}
                    <div className="px-3 py-2 text-xs font-bold text-text-secondary uppercase tracking-wider">
                      {group}
                    </div>

                    {/* Commands */}
                    <div className="space-y-1">
                      {groupCommands.map((command, index) => {
                        const globalIndex = filteredCommands.findIndex((c) => c.id === command.id);
                        const isSelected = globalIndex === selectedIndex;

                        return (
                          <button
                            key={command.id}
                            onClick={() => handleCommandExecute(command)}
                            onMouseEnter={() => setSelectedIndex(globalIndex)}
                            className={cn(
                              'w-full px-3 py-3 rounded-lg transition-all duration-200',
                              'flex items-center gap-3',
                              'text-left',
                              isSelected
                                ? 'bg-neon-cyan/20 border-2 border-neon-cyan shadow-[0_0_20px_rgba(0,255,255,0.3)]'
                                : 'bg-transparent border-2 border-transparent hover:bg-cyber-bg-primary/50'
                            )}
                          >
                            {/* Icon */}
                            {command.icon && (
                              <div
                                className={cn(
                                  'flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center',
                                  isSelected
                                    ? 'bg-neon-cyan/20 text-neon-cyan'
                                    : 'bg-neon-purple/10 text-neon-purple'
                                )}
                              >
                                {command.icon}
                              </div>
                            )}

                            {/* Info */}
                            <div className="flex-1 min-w-0">
                              <p
                                className={cn(
                                  'text-sm font-medium truncate',
                                  isSelected ? 'text-neon-cyan' : 'text-text-primary'
                                )}
                              >
                                {command.name}
                              </p>
                              <p className="text-xs text-text-secondary truncate">
                                {command.description}
                              </p>
                            </div>

                            {/* Shortcut */}
                            {command.shortcut && (
                              <div className="flex-shrink-0 px-2 py-1 rounded bg-cyber-bg-primary/50 text-xs text-text-secondary font-mono">
                                {command.shortcut}
                              </div>
                            )}
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="p-3 border-t-2 border-text-secondary/10">
            <div className="flex items-center justify-between text-xs text-text-secondary">
              <div className="flex items-center gap-4">
                <span>↑↓ 导航</span>
                <span>Enter 执行</span>
                <span>Esc 关闭</span>
              </div>
              <span>{filteredCommands.length} 条命令</span>
            </div>
          </div>
        </div>
      </>
    );
  }
);

CommandPalette.displayName = 'CommandPalette';
