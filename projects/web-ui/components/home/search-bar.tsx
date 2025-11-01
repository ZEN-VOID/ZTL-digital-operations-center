'use client';

import * as React from 'react';
import { Search, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils/cn';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
}

export function SearchBar({ value, onChange, placeholder = '搜索智能体...', className }: SearchBarProps) {
  const inputRef = React.useRef<HTMLInputElement>(null);

  const handleClear = () => {
    onChange('');
    inputRef.current?.focus();
  };

  return (
    <div className={cn('relative group', className)}>
      <div className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary group-focus-within:text-neon-cyan transition-colors">
        <Search className="w-5 h-5" />
      </div>

      <Input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={cn(
          'pl-10 pr-10 h-12 text-base',
          'bg-cyber-bg-secondary/50 border-text-secondary/30',
          'focus:border-neon-cyan focus:ring-2 focus:ring-neon-cyan/20',
          'transition-all duration-300',
          'group-focus-within:neon-glow-cyan'
        )}
      />

      {value && (
        <Button
          variant="ghost"
          size="icon"
          onClick={handleClear}
          className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 text-text-secondary hover:text-neon-pink hover:bg-cyber-bg-tertiary"
        >
          <X className="w-4 h-4" />
        </Button>
      )}
    </div>
  );
}
