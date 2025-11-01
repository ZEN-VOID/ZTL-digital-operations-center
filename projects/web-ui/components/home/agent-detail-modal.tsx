'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils/cn';
import type { Agent } from '@/lib/types/agent';
import { normalizeTools } from '@/lib/services/agent-service';
import { MessageSquare, Box, Cpu, Wrench, Zap, Lightbulb, Sparkles, Network, ArrowUpCircle, ArrowDownCircle } from 'lucide-react';

interface AgentDetailModalProps {
  agent: Agent | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AgentDetailModal({ agent, open, onOpenChange }: AgentDetailModalProps) {
  const router = useRouter();

  if (!agent) {
    return null;
  }

  const tools = normalizeTools(agent.tools);

  const handleStartChat = () => {
    onOpenChange(false);
    router.push(`/chat?agent=${encodeURIComponent(agent.id)}`);
  };

  // Get MCP servers, skills, workflows, and relationships
  const mcpServers = agent.mcpServers || [];
  const skills = agent.skills || [];
  const workflows = agent.workflows || [];
  const upstream = agent.upstream || [];
  const downstream = agent.downstream || [];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto bg-cyber-bg-secondary border-neon-cyan/30">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-3 text-2xl">
            <div
              className={cn(
                'w-12 h-12 rounded-full border-2 flex items-center justify-center',
                'bg-gradient-to-br from-neon-cyan/20 to-neon-purple/20',
                'border-neon-cyan shadow-[0_0_15px_rgba(0,255,255,0.3)]'
              )}
            >
              <Cpu className="w-6 h-6 text-neon-cyan" />
            </div>
            <div className="flex flex-col">
              <span className="neon-text-cyan">{agent.name}</span>
              <span className="text-sm text-text-secondary font-normal">{agent.id}</span>
            </div>
          </DialogTitle>
          <div className="flex items-center gap-2 mt-3">
            <Badge
              variant="outline"
              className={cn(
                'border-neon-purple/50 text-neon-purple',
                'bg-neon-purple/10 shadow-[0_0_10px_rgba(168,85,247,0.2)]'
              )}
            >
              {agent.group}
            </Badge>
            {agent.model && (
              <Badge
                variant="outline"
                className="border-neon-cyan/50 text-neon-cyan bg-neon-cyan/10"
              >
                {agent.model}
              </Badge>
            )}
          </div>
        </DialogHeader>

        <div className="space-y-5 py-4">
          {/* Description */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm font-semibold text-neon-cyan uppercase tracking-wide">
              <MessageSquare className="w-4 h-4" />
              智能体简介
            </div>
            <div className="pl-6 pr-2">
              <p className="text-text-secondary leading-relaxed text-sm line-clamp-4">
                {agent.description}
              </p>
            </div>
          </div>

          <Separator className="bg-gradient-to-r from-transparent via-neon-cyan/30 to-transparent" />

          {/* MCP Servers */}
          {mcpServers.length > 0 && (
            <>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-neon-pink uppercase tracking-wide">
                  <Zap className="w-4 h-4" />
                  关联 MCP 服务器 ({mcpServers.length})
                </div>
                <div className="pl-6 space-y-2">
                  {mcpServers.map((server, index) => (
                    <div
                      key={index}
                      className={cn(
                        'p-3 rounded-lg border border-neon-pink/30',
                        'bg-gradient-to-r from-neon-pink/5 to-transparent',
                        'hover:border-neon-pink/50 transition-all duration-300'
                      )}
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <Badge
                          variant="secondary"
                          className="bg-neon-pink/20 text-neon-pink border-neon-pink/40 font-mono text-xs"
                        >
                          {server.name}
                        </Badge>
                        <span className="text-xs text-text-secondary">
                          {server.tools.length} 工具
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-1.5 text-xs">
                        {server.tools.map((tool, toolIndex) => (
                          <span
                            key={toolIndex}
                            className="px-2 py-0.5 rounded bg-cyber-bg-tertiary/50 text-text-secondary font-mono"
                          >
                            {tool.replace('mcp__' + server.name + '__', '')}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <Separator className="bg-gradient-to-r from-transparent via-neon-pink/30 to-transparent" />
            </>
          )}

          {/* Skills */}
          {skills.length > 0 && (
            <>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-neon-green uppercase tracking-wide">
                  <Lightbulb className="w-4 h-4" />
                  关联技能包 ({skills.length})
                </div>
                <div className="pl-6 grid grid-cols-1 gap-2">
                  {skills.map((skill, index) => (
                    <div
                      key={index}
                      className={cn(
                        'p-3 rounded-lg border border-neon-green/30',
                        'bg-gradient-to-r from-neon-green/5 to-transparent',
                        'hover:border-neon-green/50 transition-all duration-300'
                      )}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-medium text-neon-green">
                              {skill.name}
                            </span>
                            {skill.category && (
                              <Badge
                                variant="outline"
                                className="text-xs border-neon-green/40 text-neon-green/80"
                              >
                                {skill.category}
                              </Badge>
                            )}
                          </div>
                          {skill.description && (
                            <p className="text-xs text-text-secondary line-clamp-2">
                              {skill.description}
                            </p>
                          )}
                        </div>
                        {skill.version && (
                          <Badge
                            variant="secondary"
                            className="text-xs bg-cyber-bg-tertiary/50"
                          >
                            v{skill.version}
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <Separator className="bg-gradient-to-r from-transparent via-neon-green/30 to-transparent" />
            </>
          )}

          {/* Tools */}
          {tools.length > 0 && (
            <>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-neon-purple uppercase tracking-wide">
                  <Wrench className="w-4 h-4" />
                  可用工具 ({tools.length})
                </div>
                <div className="flex flex-wrap gap-1.5 pl-6">
                  {tools.map((tool, index) => (
                    <Badge
                      key={index}
                      variant="secondary"
                      className={cn(
                        'bg-cyber-bg-tertiary/50 border border-neon-purple/30 text-xs',
                        'hover:border-neon-purple hover:text-neon-purple hover:scale-105',
                        'transition-all duration-200 cursor-default'
                      )}
                    >
                      {tool}
                    </Badge>
                  ))}
                </div>
              </div>
              <Separator className="bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />
            </>
          )}

          {/* Workflows */}
          {workflows.length > 0 && (
            <>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-neon-cyan uppercase tracking-wide">
                  <Sparkles className="w-4 h-4" />
                  工作流程 ({workflows.length} 步骤)
                </div>
                <div className="pl-6 space-y-1.5">
                  {workflows.slice(0, 5).map((step, index) => (
                    <div key={index} className="flex items-start gap-2 text-sm">
                      <span className="text-neon-cyan font-mono text-xs mt-0.5">
                        {index + 1}.
                      </span>
                      <span className="text-text-secondary flex-1 line-clamp-1">{step}</span>
                    </div>
                  ))}
                  {workflows.length > 5 && (
                    <span className="text-xs text-text-secondary/70 italic pl-5">
                      ... 及其他 {workflows.length - 5} 个步骤
                    </span>
                  )}
                </div>
              </div>
              <Separator className="bg-gradient-to-r from-transparent via-neon-cyan/30 to-transparent" />
            </>
          )}

          {/* Upstream Relationships */}
          {upstream.length > 0 && (
            <>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-neon-orange uppercase tracking-wide">
                  <ArrowUpCircle className="w-4 h-4" />
                  上游关系 ({upstream.length})
                </div>
                <div className="pl-6 space-y-2">
                  {upstream.map((rel, index) => (
                    <div
                      key={index}
                      className={cn(
                        'p-3 rounded-lg border border-neon-orange/30',
                        'bg-gradient-to-r from-neon-orange/5 to-transparent',
                        'hover:border-neon-orange/50 transition-all duration-300'
                      )}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <Badge
                          variant="secondary"
                          className="bg-neon-orange/20 text-neon-orange border-neon-orange/40 font-mono text-xs"
                        >
                          {rel.agentId}
                        </Badge>
                        <span className="text-sm font-medium text-text-primary">
                          {rel.agentName}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge
                          variant="outline"
                          className="text-xs border-neon-orange/30 text-neon-orange/80"
                        >
                          {rel.relationshipType === 'reports-to' ? '汇报对象' :
                           rel.relationshipType === 'orchestrates' ? '上级编排' :
                           rel.relationshipType === 'delegates' ? '任务委托' : '协作关系'}
                        </Badge>
                        {rel.description && (
                          <span className="text-xs text-text-secondary">
                            {rel.description}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <Separator className="bg-gradient-to-r from-transparent via-neon-orange/30 to-transparent" />
            </>
          )}

          {/* Downstream Relationships */}
          {downstream.length > 0 && (
            <>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm font-semibold text-neon-blue uppercase tracking-wide">
                  <ArrowDownCircle className="w-4 h-4" />
                  下游关系 ({downstream.length})
                </div>
                <div className="pl-6 space-y-2">
                  {downstream.map((rel, index) => (
                    <div
                      key={index}
                      className={cn(
                        'p-3 rounded-lg border border-neon-blue/30',
                        'bg-gradient-to-r from-neon-blue/5 to-transparent',
                        'hover:border-neon-blue/50 transition-all duration-300'
                      )}
                    >
                      <div className="flex items-center gap-2 mb-1">
                        <Badge
                          variant="secondary"
                          className="bg-neon-blue/20 text-neon-blue border-neon-blue/40 font-mono text-xs"
                        >
                          {rel.agentId}
                        </Badge>
                        <span className="text-sm font-medium text-text-primary">
                          {rel.agentName}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge
                          variant="outline"
                          className="text-xs border-neon-blue/30 text-neon-blue/80"
                        >
                          {rel.relationshipType === 'orchestrates' ? '编排执行' :
                           rel.relationshipType === 'delegates' ? '委托执行' :
                           rel.relationshipType === 'collaborates-with' ? '协作执行' : '关系'}
                        </Badge>
                        {rel.description && (
                          <span className="text-xs text-text-secondary">
                            {rel.description}
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <Separator className="bg-gradient-to-r from-transparent via-neon-blue/30 to-transparent" />
            </>
          )}

          {/* Expertise */}
          {agent.expertise && agent.expertise.length > 0 && (
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-neon-orange uppercase tracking-wide">
                <Box className="w-4 h-4" />
                专业领域
              </div>
              <div className="flex flex-wrap gap-1.5 pl-6">
                {agent.expertise.map((item, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="bg-cyber-bg-tertiary/50 border-neon-orange/30 text-xs"
                  >
                    {item}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>

        <DialogFooter className="gap-2 pt-4 border-t border-text-secondary/20">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            className="border-text-secondary/30 hover:border-text-secondary/50"
          >
            关闭
          </Button>
          <Button
            variant="neon-cyan"
            onClick={handleStartChat}
            className={cn(
              'gap-2 group',
              'shadow-[0_0_20px_rgba(0,255,255,0.3)]',
              'hover:shadow-[0_0_30px_rgba(0,255,255,0.5)]'
            )}
          >
            <MessageSquare className="w-4 h-4 group-hover:animate-neon-pulse" />
            开始对话
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
