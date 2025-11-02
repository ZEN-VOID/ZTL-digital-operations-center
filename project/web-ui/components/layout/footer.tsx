'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface FooterProps extends React.HTMLAttributes<HTMLElement> {
  stats?: Array<{ label: string; value: string | number }>;
}

const Footer = React.forwardRef<HTMLElement, FooterProps>(
  ({ className, stats, ...props }, ref) => {
    const defaultStats = [
      { label: '智能体', value: '60+' },
      { label: '业务组', value: '8' },
      { label: '运行时长', value: '24/7' },
    ];

    const displayStats = stats || defaultStats;

    return (
      <footer
        ref={ref}
        className={cn(
          'fixed bottom-0 left-0 right-0 z-40',
          'bg-cyber-bg-primary/80 backdrop-blur-md',
          'border-t-2 border-neon-purple/30',
          'shadow-[0_-2px_20px_rgba(176,0,255,0.1)]',
          className
        )}
        {...props}
      >
        <div className="container mx-auto px-6 py-3">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            {/* Stats */}
            <div className="flex items-center gap-6">
              {displayStats.map((stat, index) => (
                <div key={index} className="flex items-center gap-2">
                  <span className="text-sm text-text-secondary">{stat.label}:</span>
                  <span className="text-sm font-bold neon-text-purple font-orbitron">
                    {stat.value}
                  </span>
                </div>
              ))}
            </div>

            {/* Copyright */}
            <div className="text-xs text-text-secondary">
              © 2025 ZTL数智化作战中心 | Powered by Claude Code
            </div>

            {/* System Status */}
            <div className="flex items-center gap-2 text-xs">
              <div className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-neon-cyan animate-neon-pulse" />
                <span className="text-text-secondary">Next.js 16</span>
              </div>
              <span className="text-text-secondary/50">|</span>
              <div className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-neon-pink animate-neon-pulse" />
                <span className="text-text-secondary">React 19</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    );
  }
);

Footer.displayName = 'Footer';

export { Footer };
