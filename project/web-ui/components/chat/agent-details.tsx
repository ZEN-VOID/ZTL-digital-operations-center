'use client';

import * as React from 'react';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils/cn';
import type { Agent } from '@/lib/types/agent';
import { normalizeTools } from '@/lib/services/agent-service';
import { Cpu, Wrench, Zap, Lightbulb, Sparkles } from 'lucide-react';

interface AgentDetailsProps {
  agent: Agent | null;
  className?: string;
}

export const AgentDetails = React.forwardRef<HTMLDivElement, AgentDetailsProps>(
  ({ agent, className }, ref) => {
    if (!agent) {
      return (
        <div ref={ref} className={cn('text-text-secondary text-sm text-center py-8', className)}>
          未选择智能体
        </div>
      );
    }

    const tools = normalizeTools(agent.tools);
    const mcpServers = agent.mcpServers || [];
    const skills = agent.skills || [];
    const workflows = agent.workflows || [];

    return (
      <div ref={ref} className={cn('space-y-4 text-sm', className)}>
        {/* Agent Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <div
              className={cn(
                'w-8 h-8 rounded-full border flex items-center justify-center flex-shrink-0',
                'bg-gradient-to-br from-neon-cyan/20 to-neon-purple/20',
                'border-neon-cyan/50'
              )}
            >
              <Cpu className="w-4 h-4 text-neon-cyan" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-neon-cyan truncate">{agent.name}</h3>
              <p className="text-xs text-text-secondary truncate">{agent.id}</p>
            </div>
          </div>

          <div className="flex items-center gap-1.5 flex-wrap">
            <Badge
              variant="outline"
              className="border-neon-purple/50 text-neon-purple text-xs bg-neon-purple/10"
            >
              {agent.group}
            </Badge>
            {agent.model && (
              <Badge variant="outline" className="border-neon-cyan/50 text-neon-cyan text-xs bg-neon-cyan/10">
                {agent.model}
              </Badge>
            )}
          </div>
        </div>

        <Separator className="bg-gradient-to-r from-transparent via-neon-cyan/30 to-transparent" />

        {/* Description */}
        <div className="space-y-1.5">
          <div className="text-xs font-semibold text-neon-cyan uppercase tracking-wide">简介</div>
          <p className="text-xs text-text-secondary leading-relaxed line-clamp-3">{agent.description}</p>
        </div>

        {/* MCP Servers */}
        {mcpServers.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-pink/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-pink uppercase tracking-wide">
                <Zap className="w-3 h-3" />
                MCP 服务器 ({mcpServers.length})
              </div>
              <div className="space-y-1.5">
                {mcpServers.slice(0, 3).map((server, index) => (
                  <div
                    key={index}
                    className="p-2 rounded border border-neon-pink/20 bg-neon-pink/5 text-xs"
                  >
                    <div className="font-medium text-neon-pink">{server.name}</div>
                    <div className="text-text-secondary mt-0.5">{server.tools.length} 工具</div>
                  </div>
                ))}
                {mcpServers.length > 3 && (
                  <div className="text-xs text-text-secondary/70 italic">
                    ... 及其他 {mcpServers.length - 3} 个
                  </div>
                )}
              </div>
            </div>
          </>
        )}

        {/* Skills */}
        {skills.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-green/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-green uppercase tracking-wide">
                <Lightbulb className="w-3 h-3" />
                技能包 ({skills.length})
              </div>
              <div className="space-y-1.5">
                {skills.slice(0, 3).map((skill, index) => (
                  <div key={index} className="p-2 rounded border border-neon-green/20 bg-neon-green/5 text-xs">
                    <div className="font-medium text-neon-green">{skill.name}</div>
                    {skill.description && (
                      <div className="text-text-secondary mt-0.5 line-clamp-1">{skill.description}</div>
                    )}
                  </div>
                ))}
                {skills.length > 3 && (
                  <div className="text-xs text-text-secondary/70 italic">... 及其他 {skills.length - 3} 个</div>
                )}
              </div>
            </div>
          </>
        )}

        {/* Tools */}
        {tools.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-purple/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-purple uppercase tracking-wide">
                <Wrench className="w-3 h-3" />
                工具 ({tools.length})
              </div>
              <div className="flex flex-wrap gap-1">
                {tools.slice(0, 8).map((tool, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="bg-cyber-bg-tertiary/50 border-neon-purple/30 text-xs"
                  >
                    {tool}
                  </Badge>
                ))}
                {tools.length > 8 && (
                  <Badge variant="secondary" className="bg-cyber-bg-tertiary/50 border-neon-purple/30 text-xs">
                    +{tools.length - 8}
                  </Badge>
                )}
              </div>
            </div>
          </>
        )}

        {/* Workflows */}
        {workflows.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-cyan/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-cyan uppercase tracking-wide">
                <Sparkles className="w-3 h-3" />
                工作流程 ({workflows.length})
              </div>
              <div className="space-y-1">
                {workflows.slice(0, 4).map((step, index) => (
                  <div key={index} className="flex items-start gap-1.5 text-xs">
                    <span className="text-neon-cyan font-mono">{index + 1}.</span>
                    <span className="text-text-secondary flex-1 line-clamp-1">{step}</span>
                  </div>
                ))}
                {workflows.length > 4 && (
                  <div className="text-xs text-text-secondary/70 italic pl-4">
                    ... 及其他 {workflows.length - 4} 步
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    );
  }
);

AgentDetails.displayName = 'AgentDetails';
