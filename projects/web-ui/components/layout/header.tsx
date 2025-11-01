'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface HeaderProps extends React.HTMLAttributes<HTMLElement> {
  logo?: React.ReactNode;
  navigation?: React.ReactNode;
}

const Header = React.forwardRef<HTMLElement, HeaderProps>(
  ({ className, logo, navigation, ...props }, ref) => {
    return (
      <header
        ref={ref}
        className={cn(
          'fixed top-0 left-0 right-0 z-50',
          'bg-cyber-bg-primary/80 backdrop-blur-md',
          'border-b-2 border-neon-cyan/30',
          'shadow-[0_0_20px_rgba(0,255,255,0.1)]',
          className
        )}
        {...props}
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-4">
              {logo || (
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg border-2 border-neon-cyan shadow-[0_0_10px_rgba(0,255,255,0.5)] flex items-center justify-center">
                    <span className="text-xl font-bold neon-text-cyan font-orbitron">Z</span>
                  </div>
                  <div>
                    <h1 className="text-xl font-bold neon-text-cyan font-orbitron">ZTL</h1>
                    <p className="text-xs text-text-secondary">数智化作战中心</p>
                  </div>
                </div>
              )}
            </div>

            {/* Navigation */}
            {navigation && (
              <nav className="hidden md:flex items-center gap-6">
                {navigation}
              </nav>
            )}

            {/* Status Indicator */}
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-neon-green animate-neon-pulse" />
              <span className="text-sm text-text-secondary hidden sm:inline">在线</span>
            </div>
          </div>
        </div>
      </header>
    );
  }
);

Header.displayName = 'Header';

export { Header };
