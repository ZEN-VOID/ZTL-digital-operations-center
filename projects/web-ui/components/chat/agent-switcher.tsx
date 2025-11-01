'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface Agent {
  id: string;
  name: string;
  description: string;
  avatar?: string;
  group?: string;
  color?: 'cyan' | 'purple' | 'pink';
}

export interface AgentSwitcherProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Available agents */
  agents: Agent[];
  /** Current agent ID */
  currentAgentId: string;
  /** On agent change */
  onAgentChange: (agentId: string) => void;
  /** Show agent groups */
  showGroups?: boolean;
}

export const AgentSwitcher = React.forwardRef<HTMLDivElement, AgentSwitcherProps>(
  (
    {
      className,
      agents,
      currentAgentId,
      onAgentChange,
      showGroups = true,
      ...props
    },
    ref
  ) => {
    // Track which groups are expanded
    const [expandedGroups, setExpandedGroups] = React.useState<Set<string>>(new Set());
    const currentAgent = agents.find((agent) => agent.id === currentAgentId);

    // Group agents by group
    const groupedAgents = React.useMemo(() => {
      if (!showGroups) {
        return { '全部': agents };
      }

      return agents.reduce(
        (acc, agent) => {
          const group = agent.group || '其他';
          if (!acc[group]) {
            acc[group] = [];
          }
          acc[group].push(agent);
          return acc;
        },
        {} as Record<string, Agent[]>
      );
    }, [agents, showGroups]);

    // Auto-expand group containing current agent
    React.useEffect(() => {
      if (currentAgent?.group) {
        setExpandedGroups((prev) => new Set(prev).add(currentAgent.group!));
      }
    }, [currentAgent]);

    const toggleGroup = (group: string) => {
      setExpandedGroups((prev) => {
        const next = new Set(prev);
        if (next.has(group)) {
          next.delete(group);
        } else {
          next.add(group);
        }
        return next;
      });
    };

    const handleAgentSelect = (agentId: string) => {
      onAgentChange(agentId);
    };

    const getColorClass = (color?: Agent['color']) => {
      switch (color) {
        case 'cyan':
          return 'text-neon-cyan';
        case 'pink':
          return 'text-neon-pink';
        case 'purple':
        default:
          return 'text-neon-purple';
      }
    };

    return (
      <div ref={ref} className={cn('', className)} {...props}>
        {/* Tree structure */}
        <div className="space-y-1">
          {Object.entries(groupedAgents).map(([group, groupAgents]) => {
            const isExpanded = expandedGroups.has(group);
            const hasCurrentAgent = groupAgents.some((agent) => agent.id === currentAgentId);

            return (
              <div key={group}>
                {/* Group header (Level 1) */}
                {showGroups && (
                  <button
                    onClick={() => toggleGroup(group)}
                    className={cn(
                      'w-full px-3 py-2 rounded-lg transition-all duration-200',
                      'flex items-center gap-2 group',
                      'hover:bg-cyber-bg-primary/30',
                      hasCurrentAgent && 'bg-cyber-bg-primary/20'
                    )}
                  >
                    {/* Expand/collapse icon */}
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="14"
                      height="14"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className={cn(
                        'flex-shrink-0 transition-transform text-text-secondary',
                        isExpanded && 'rotate-90'
                      )}
                    >
                      <path d="m9 18 6-6-6-6" />
                    </svg>

                    {/* Group name */}
                    <span className="text-sm font-bold text-text-primary group-hover:text-neon-cyan transition-colors">
                      {group}
                    </span>

                    {/* Agent count badge */}
                    <span className="ml-auto text-xs text-text-secondary bg-cyber-bg-primary/50 px-2 py-0.5 rounded">
                      {groupAgents.length}
                    </span>
                  </button>
                )}

                {/* Agents in group (Level 2) */}
                {isExpanded && (
                  <div className="ml-4 mt-1 space-y-1">
                    {groupAgents.map((agent) => {
                      const isActive = agent.id === currentAgentId;

                      return (
                        <button
                          key={agent.id}
                          onClick={() => handleAgentSelect(agent.id)}
                          className={cn(
                            'w-full px-3 py-2 rounded-md transition-all duration-200',
                            'flex items-center gap-3 group',
                            'hover:bg-cyber-bg-primary/50',
                            isActive && 'bg-neon-cyan/10 border-l-2 border-neon-cyan'
                          )}
                        >
                          {/* Avatar */}
                          <div
                            className={cn(
                              'flex-shrink-0 w-7 h-7 rounded-md flex items-center justify-center font-bold text-xs',
                              agent.color === 'cyan' && 'bg-neon-cyan/20 border border-neon-cyan/50 text-neon-cyan',
                              agent.color === 'pink' && 'bg-neon-pink/20 border border-neon-pink/50 text-neon-pink',
                              (!agent.color || agent.color === 'purple') &&
                                'bg-neon-purple/20 border border-neon-purple/50 text-neon-purple'
                            )}
                          >
                            {agent.id}
                          </div>

                          {/* Info */}
                          <div className="flex-1 text-left min-w-0">
                            <p
                              className={cn(
                                'text-sm font-medium truncate transition-colors',
                                isActive ? 'text-neon-cyan' : 'text-text-primary group-hover:text-neon-cyan'
                              )}
                            >
                              {agent.name}
                            </p>
                            {agent.description && (
                              <p className="text-xs text-text-secondary truncate">
                                {agent.description}
                              </p>
                            )}
                          </div>

                          {/* Active indicator */}
                          {isActive && (
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width="14"
                              height="14"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              className="flex-shrink-0 text-neon-cyan"
                            >
                              <path d="M20 6 9 17l-5-5" />
                            </svg>
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  }
);

AgentSwitcher.displayName = 'AgentSwitcher';
