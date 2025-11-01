import * as React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils/cn';

export interface AgentCardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'onSelect'> {
  /** Agent unique identifier */
  id: string;
  /** Agent display name */
  name: string;
  /** Agent description */
  description: string;
  /** Agent group/team */
  group: string;
  /** Agent status */
  status?: 'online' | 'offline' | 'busy' | 'idle';
  /** Agent model */
  model?: string;
  /** Agent tools */
  tools?: string[];
  /** Card variant */
  variant?: 'default' | 'neon-cyan' | 'neon-pink' | 'neon-purple' | 'ghost';
  /** Card size */
  size?: 'small' | 'medium' | 'large';
  /** On agent select callback */
  onSelect?: (id: string) => void;
  /** On agent view details callback */
  onViewDetails?: (id: string) => void;
}

const AgentCard = React.forwardRef<HTMLDivElement, AgentCardProps>(
  (
    {
      className,
      id,
      name,
      description,
      group,
      status = 'idle',
      model,
      tools = [],
      variant = 'default',
      size = 'medium',
      onSelect,
      onViewDetails,
      ...props
    },
    ref
  ) => {
    const statusColors = {
      online: 'bg-neon-green',
      offline: 'bg-text-secondary/30',
      busy: 'bg-neon-pink',
      idle: 'bg-neon-cyan',
    };

    const statusLabels = {
      online: '在线',
      offline: '离线',
      busy: '忙碌',
      idle: '空闲',
    };

    // Small size: compact layout
    if (size === 'small') {
      return (
        <Card ref={ref} variant={variant} className={cn('group hover:scale-[1.02] transition-transform', className)} {...props}>
          <CardHeader className="p-3">
            <div className="flex items-center justify-between gap-2">
              <CardTitle className="text-sm flex items-center gap-1.5">
                <span className="truncate">{name}</span>
                <div
                  className={cn(
                    'w-1.5 h-1.5 rounded-full flex-shrink-0',
                    statusColors[status],
                    status === 'online' && 'animate-neon-pulse'
                  )}
                />
              </CardTitle>
            </div>
            <CardDescription className="text-xs line-clamp-1">{group}</CardDescription>
          </CardHeader>
          <CardFooter className="p-3 pt-0 flex gap-1.5">
            {onSelect && (
              <Button
                variant="neon-cyan"
                size="sm"
                onClick={() => onSelect(id)}
                className="flex-1 h-7 text-xs"
              >
                选择
              </Button>
            )}
            {onViewDetails && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onViewDetails(id)}
                className="flex-1 h-7 text-xs"
              >
                详情
              </Button>
            )}
          </CardFooter>
        </Card>
      );
    }

    // Large size: expanded layout with more details
    if (size === 'large') {
      return (
        <Card ref={ref} variant={variant} className={cn('group hover:scale-[1.01] transition-transform', className)} {...props}>
          <CardHeader className="p-6">
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <span className="truncate">{name}</span>
                  <div
                    className={cn(
                      'w-2.5 h-2.5 rounded-full flex-shrink-0',
                      statusColors[status],
                      status === 'online' && 'animate-neon-pulse'
                    )}
                  />
                </CardTitle>
                <CardDescription className="mt-2 text-sm">
                  {group} • {statusLabels[status]}
                </CardDescription>
              </div>
              {model && (
                <div className="px-3 py-1.5 rounded text-sm bg-cyber-bg-secondary/50 border border-neon-purple/30 text-neon-purple whitespace-nowrap">
                  {model}
                </div>
              )}
            </div>
          </CardHeader>

          <CardContent className="px-6 pb-6 space-y-4">
            <p className="text-base text-text-secondary line-clamp-4 leading-relaxed">{description}</p>

            {tools.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {tools.slice(0, 8).map((tool, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 text-sm rounded bg-cyber-bg-tertiary/50 border border-text-secondary/20 text-text-secondary"
                  >
                    {tool}
                  </span>
                ))}
                {tools.length > 8 && (
                  <span className="px-3 py-1 text-sm rounded bg-cyber-bg-tertiary/50 border border-text-secondary/20 text-text-secondary">
                    +{tools.length - 8} 更多
                  </span>
                )}
              </div>
            )}
          </CardContent>

          <CardFooter className="px-6 pb-6 flex gap-3">
            {onSelect && (
              <Button
                variant="neon-cyan"
                size="default"
                onClick={() => onSelect(id)}
                className="flex-1"
              >
                选择智能体
              </Button>
            )}
            {onViewDetails && (
              <Button
                variant="outline"
                size="default"
                onClick={() => onViewDetails(id)}
                className="flex-1"
              >
                查看详情
              </Button>
            )}
          </CardFooter>
        </Card>
      );
    }

    // Medium size: default layout
    return (
      <Card ref={ref} variant={variant} className={cn('group hover:scale-[1.02] transition-transform', className)} {...props}>
        <CardHeader>
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <CardTitle className="flex items-center gap-2">
                <span className="truncate">{name}</span>
                <div
                  className={cn(
                    'w-2 h-2 rounded-full flex-shrink-0',
                    statusColors[status],
                    status === 'online' && 'animate-neon-pulse'
                  )}
                />
              </CardTitle>
              <CardDescription className="mt-1 text-xs">
                {group} • {statusLabels[status]}
              </CardDescription>
            </div>
            {model && (
              <div className="px-2 py-1 rounded text-xs bg-cyber-bg-secondary/50 border border-neon-purple/30 text-neon-purple whitespace-nowrap">
                {model}
              </div>
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-3">
          <p className="text-sm text-text-secondary line-clamp-3">{description}</p>

          {tools.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {tools.slice(0, 5).map((tool, index) => (
                <span
                  key={index}
                  className="px-2 py-0.5 text-xs rounded bg-cyber-bg-tertiary/50 border border-text-secondary/20 text-text-secondary"
                >
                  {tool}
                </span>
              ))}
              {tools.length > 5 && (
                <span className="px-2 py-0.5 text-xs rounded bg-cyber-bg-tertiary/50 border border-text-secondary/20 text-text-secondary">
                  +{tools.length - 5}
                </span>
              )}
            </div>
          )}
        </CardContent>

        <CardFooter className="flex gap-2">
          {onSelect && (
            <Button
              variant="neon-cyan"
              size="sm"
              onClick={() => onSelect(id)}
              className="flex-1"
            >
              选择
            </Button>
          )}
          {onViewDetails && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => onViewDetails(id)}
              className="flex-1"
            >
              详情
            </Button>
          )}
        </CardFooter>
      </Card>
    );
  }
);

AgentCard.displayName = 'AgentCard';

export { AgentCard };
