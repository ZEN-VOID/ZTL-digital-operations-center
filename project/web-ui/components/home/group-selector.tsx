'use client';

import * as React from 'react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils/cn';
import { Badge } from '@/components/ui/badge';

interface GroupSelectorProps {
  groups: string[];
  selectedGroup: string | null;
  onGroupChange: (group: string | null) => void;
  agentCounts?: Record<string, number>;
  className?: string;
}

export function GroupSelector({
  groups,
  selectedGroup,
  onGroupChange,
  agentCounts = {},
  className,
}: GroupSelectorProps) {
  const totalCount = Object.values(agentCounts).reduce((sum, count) => sum + count, 0);

  return (
    <div className={cn('flex flex-wrap gap-2', className)}>
      <Button
        variant={selectedGroup === null ? 'neon-cyan' : 'outline'}
        size="sm"
        onClick={() => onGroupChange(null)}
        className={cn(
          'relative group transition-all duration-300',
          selectedGroup === null && 'animate-neon-pulse'
        )}
      >
        全部
        {totalCount > 0 && (
          <Badge
            variant="secondary"
            className={cn(
              'ml-2 px-1.5 min-w-[1.5rem]',
              selectedGroup === null
                ? 'bg-cyber-bg-primary/50 text-neon-cyan'
                : 'bg-cyber-bg-tertiary/50 text-text-secondary'
            )}
          >
            {totalCount}
          </Badge>
        )}
      </Button>

      {groups.map((group) => {
        const isSelected = selectedGroup === group;
        const count = agentCounts[group] || 0;

        return (
          <Button
            key={group}
            variant={isSelected ? 'neon-purple' : 'outline'}
            size="sm"
            onClick={() => onGroupChange(group)}
            className={cn(
              'relative group transition-all duration-300',
              isSelected && 'animate-neon-pulse'
            )}
          >
            {group}
            {count > 0 && (
              <Badge
                variant="secondary"
                className={cn(
                  'ml-2 px-1.5 min-w-[1.5rem]',
                  isSelected
                    ? 'bg-cyber-bg-primary/50 text-neon-purple'
                    : 'bg-cyber-bg-tertiary/50 text-text-secondary'
                )}
              >
                {count}
              </Badge>
            )}
          </Button>
        );
      })}
    </div>
  );
}
