'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils/cn';
import { Home, MessageSquare, FolderOpen } from 'lucide-react';

export interface NavigationProps extends React.HTMLAttributes<HTMLElement> {
  variant?: 'header' | 'sidebar';
}

const navItems = [
  {
    href: '/home',
    label: '智能体',
    icon: Home,
    color: 'cyan',
  },
  {
    href: '/chat',
    label: '对话',
    icon: MessageSquare,
    color: 'purple',
  },
  {
    href: '/resources',
    label: '资源',
    icon: FolderOpen,
    color: 'pink',
  },
];

export const Navigation = React.forwardRef<HTMLElement, NavigationProps>(
  ({ className, variant = 'header', ...props }, ref) => {
    const pathname = usePathname();

    if (variant === 'header') {
      return (
        <nav ref={ref} className={cn('flex items-center gap-2', className)} {...props}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'px-4 py-2 rounded-lg transition-all duration-200',
                  'flex items-center gap-2 font-medium text-sm',
                  'hover:scale-105',
                  isActive
                    ? {
                        cyan: 'bg-neon-cyan/20 border-2 border-neon-cyan text-neon-cyan',
                        purple: 'bg-neon-purple/20 border-2 border-neon-purple text-neon-purple',
                        pink: 'bg-neon-pink/20 border-2 border-neon-pink text-neon-pink',
                      }[item.color]
                    : `bg-cyber-bg-tertiary/30 border border-text-secondary/20 text-text-secondary hover:border-neon-${item.color}/50 hover:text-neon-${item.color}`
                )}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      );
    }

    // Sidebar variant
    return (
      <nav ref={ref} className={cn('flex flex-col gap-2', className)} {...props}>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'px-4 py-3 rounded-lg transition-all duration-200',
                'flex items-center gap-3',
                isActive
                  ? {
                      cyan: 'bg-neon-cyan/20 border-l-4 border-neon-cyan text-neon-cyan',
                      purple: 'bg-neon-purple/20 border-l-4 border-neon-purple text-neon-purple',
                      pink: 'bg-neon-pink/20 border-l-4 border-neon-pink text-neon-pink',
                    }[item.color]
                  : 'bg-cyber-bg-tertiary/30 border-l-4 border-transparent text-text-secondary hover:border-neon-cyan/50 hover:text-neon-cyan'
              )}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    );
  }
);

Navigation.displayName = 'Navigation';
