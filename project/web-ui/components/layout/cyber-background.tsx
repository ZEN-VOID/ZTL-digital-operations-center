'use client';

import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface CyberBackgroundProps extends React.HTMLAttributes<HTMLDivElement> {
  showGrid?: boolean;
  showScanline?: boolean;
  showParticles?: boolean;
  intensity?: 'low' | 'medium' | 'high';
}

const CyberBackground = React.forwardRef<HTMLDivElement, CyberBackgroundProps>(
  ({
    className,
    showGrid = true,
    showScanline = true,
    showParticles = false,
    intensity = 'medium',
    children,
    ...props
  }, ref) => {
    const intensityClasses = {
      low: 'opacity-20',
      medium: 'opacity-40',
      high: 'opacity-60',
    };

    return (
      <div
        ref={ref}
        className={cn('relative min-h-screen overflow-hidden', className)}
        {...props}
      >
        {/* Animated Grid Background */}
        {showGrid && (
          <div className="fixed inset-0 cyber-grid-bg pointer-events-none" />
        )}

        {/* Scanline Effect */}
        {showScanline && (
          <div className="fixed inset-0 pointer-events-none">
            <div
              className={cn(
                'absolute inset-0 bg-gradient-to-b from-transparent via-neon-cyan/5 to-transparent animate-[grid-move_3s_linear_infinite]',
                intensityClasses[intensity]
              )}
            />
          </div>
        )}

        {/* Floating Particles (Optional) */}
        {showParticles && (
          <div className="fixed inset-0 pointer-events-none overflow-hidden">
            {[...Array(20)].map((_, i) => (
              <div
                key={i}
                className={cn(
                  'absolute w-1 h-1 rounded-full',
                  i % 3 === 0 && 'bg-neon-cyan',
                  i % 3 === 1 && 'bg-neon-pink',
                  i % 3 === 2 && 'bg-neon-purple',
                  'animate-[float_10s_ease-in-out_infinite]'
                )}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                  animationDelay: `${Math.random() * 5}s`,
                  opacity: 0.3 + Math.random() * 0.3,
                }}
              />
            ))}
          </div>
        )}

        {/* Corner Accents */}
        <div className="fixed top-0 left-0 w-32 h-32 border-l-2 border-t-2 border-neon-cyan/30 pointer-events-none" />
        <div className="fixed top-0 right-0 w-32 h-32 border-r-2 border-t-2 border-neon-pink/30 pointer-events-none" />
        <div className="fixed bottom-0 left-0 w-32 h-32 border-l-2 border-b-2 border-neon-purple/30 pointer-events-none" />
        <div className="fixed bottom-0 right-0 w-32 h-32 border-r-2 border-b-2 border-neon-cyan/30 pointer-events-none" />

        {/* Glow Orbs */}
        <div className="fixed top-1/4 left-1/4 w-96 h-96 bg-neon-cyan/10 rounded-full blur-[100px] pointer-events-none animate-pulse" />
        <div className="fixed bottom-1/4 right-1/4 w-96 h-96 bg-neon-pink/10 rounded-full blur-[100px] pointer-events-none animate-pulse" />

        {/* Content */}
        <div className="relative z-10">
          {children}
        </div>
      </div>
    );
  }
);

CyberBackground.displayName = 'CyberBackground';

export { CyberBackground };
