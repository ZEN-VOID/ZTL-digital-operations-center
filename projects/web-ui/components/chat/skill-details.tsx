'use client';

import * as React from 'react';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils/cn';
import type { Skill } from '@/lib/types/skill';
import { normalizeTools } from '@/lib/services/skill-service';
import { Zap, Wrench, Tag, Lightbulb, Package } from 'lucide-react';

interface SkillDetailsProps {
  skill: Skill | null;
  className?: string;
}

export const SkillDetails = React.forwardRef<HTMLDivElement, SkillDetailsProps>(
  ({ skill, className }, ref) => {
    if (!skill) {
      return (
        <div ref={ref} className={cn('text-text-secondary text-sm text-center py-8', className)}>
          未选择技能包
        </div>
      );
    }

    const tools = normalizeTools(skill.tools);
    const tags = skill.tags || [];
    const capabilities = skill.capabilities || [];

    return (
      <div ref={ref} className={cn('space-y-4 text-sm', className)}>
        {/* Skill Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <div
              className={cn(
                'w-8 h-8 rounded-full border flex items-center justify-center flex-shrink-0',
                'bg-gradient-to-br from-neon-purple/20 to-neon-pink/20',
                'border-neon-purple/50'
              )}
            >
              <Package className="w-4 h-4 text-neon-purple" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-neon-purple truncate">{skill.name}</h3>
              <p className="text-xs text-text-secondary truncate">{skill.id}</p>
            </div>
          </div>

          <div className="flex items-center gap-1.5 flex-wrap">
            <Badge
              variant="outline"
              className="border-neon-pink/50 text-neon-pink text-xs bg-neon-pink/10"
            >
              {skill.category}
            </Badge>
            {skill.version && (
              <Badge variant="outline" className="border-neon-cyan/50 text-neon-cyan text-xs bg-neon-cyan/10">
                v{skill.version}
              </Badge>
            )}
          </div>
        </div>

        <Separator className="bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />

        {/* Description */}
        <div className="space-y-1.5">
          <div className="text-xs font-semibold text-neon-purple uppercase tracking-wide">简介</div>
          <p className="text-xs text-text-secondary leading-relaxed line-clamp-4">{skill.description}</p>
        </div>

        {/* Tags */}
        {tags.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-green/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-green uppercase tracking-wide">
                <Tag className="w-3 h-3" />
                标签 ({tags.length})
              </div>
              <div className="flex flex-wrap gap-1">
                {tags.slice(0, 8).map((tag, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="bg-cyber-bg-tertiary/50 border-neon-green/30 text-xs"
                  >
                    {tag}
                  </Badge>
                ))}
                {tags.length > 8 && (
                  <Badge variant="secondary" className="bg-cyber-bg-tertiary/50 border-neon-green/30 text-xs">
                    +{tags.length - 8}
                  </Badge>
                )}
              </div>
            </div>
          </>
        )}

        {/* Capabilities */}
        {capabilities.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-cyan/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-cyan uppercase tracking-wide">
                <Lightbulb className="w-3 h-3" />
                核心能力 ({capabilities.length})
              </div>
              <div className="space-y-1">
                {capabilities.slice(0, 6).map((capability, index) => (
                  <div key={index} className="flex items-start gap-1.5 text-xs">
                    <span className="text-neon-cyan font-mono">{index + 1}.</span>
                    <span className="text-text-secondary flex-1 line-clamp-2">{capability}</span>
                  </div>
                ))}
                {capabilities.length > 6 && (
                  <div className="text-xs text-text-secondary/70 italic pl-4">
                    ... 及其他 {capabilities.length - 6} 项能力
                  </div>
                )}
              </div>
            </div>
          </>
        )}

        {/* Tools */}
        {tools.length > 0 && (
          <>
            <Separator className="bg-gradient-to-r from-transparent via-neon-pink/20 to-transparent" />
            <div className="space-y-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-neon-pink uppercase tracking-wide">
                <Wrench className="w-3 h-3" />
                工具 ({tools.length})
              </div>
              <div className="flex flex-wrap gap-1">
                {tools.slice(0, 8).map((tool, index) => (
                  <Badge
                    key={index}
                    variant="secondary"
                    className="bg-cyber-bg-tertiary/50 border-neon-pink/30 text-xs"
                  >
                    {tool}
                  </Badge>
                ))}
                {tools.length > 8 && (
                  <Badge variant="secondary" className="bg-cyber-bg-tertiary/50 border-neon-pink/30 text-xs">
                    +{tools.length - 8}
                  </Badge>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    );
  }
);

SkillDetails.displayName = 'SkillDetails';
