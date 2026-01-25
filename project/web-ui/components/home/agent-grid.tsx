'use client';

import * as React from 'react';
import { AgentCard } from '@/components/agent/agent-card';
import { cn } from '@/lib/utils/cn';
import type { Agent } from '@/lib/types/agent';
import { normalizeTools } from '@/lib/services/agent-service';

type ViewSize = 'small' | 'medium' | 'large';

interface AgentGridProps {
  agents: Agent[];
  onAgentSelect?: (id: string) => void;
  onAgentViewDetails?: (id: string) => void;
  viewSize?: ViewSize;
  className?: string;
}

export function AgentGrid({ agents, onAgentSelect, onAgentViewDetails, viewSize = 'medium', className }: AgentGridProps) {
  if (agents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-4">
        <div className="w-20 h-20 rounded-full bg-cyber-bg-secondary/50 border-2 border-text-secondary/30 flex items-center justify-center mb-4">
          <svg
            className="w-10 h-10 text-text-secondary"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <p className="text-text-secondary text-lg mb-2">未找到匹配的智能体</p>
        <p className="text-text-secondary/70 text-sm">请尝试其他搜索条件或筛选选项</p>
      </div>
    );
  }

  // Grid layout based on view size
  const gridClassName = cn(
    'grid',
    {
      // Small: Compact cards, more columns
      'gap-3 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6': viewSize === 'small',
      // Medium: Default layout
      'gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4': viewSize === 'medium',
      // Large: Expanded cards, fewer columns
      'gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3': viewSize === 'large',
    },
    className
  );

  return (
    <div className={gridClassName}>
      {agents.map((agent, index) => {
        const tools = normalizeTools(agent.tools);
        const variant = getCardVariant(index);

        return (
          <div
            key={agent.id}
            className="animate-message-appear"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            <AgentCard
              id={agent.id}
              name={agent.name}
              description={agent.description}
              group={agent.group}
              status={agent.status || 'idle'}
              model={agent.model}
              tools={tools}
              variant={variant}
              size={viewSize}
              onSelect={onAgentSelect}
              onViewDetails={onAgentViewDetails}
            />
          </div>
        );
      })}
    </div>
  );
}

/**
 * Get card variant based on index for visual variety
 */
function getCardVariant(index: number): 'default' | 'neon-cyan' | 'neon-pink' | 'neon-purple' {
  const variants = ['neon-cyan', 'neon-pink', 'neon-purple'] as const;
  return variants[index % 3];
}
