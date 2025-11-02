import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'neon-cyan' | 'neon-pink' | 'neon-purple' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', asChild = false, ...props }, ref) => {
    const Comp = asChild ? 'span' : 'button';

    return (
      <Comp
        className={cn(
          // Base styles
          'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-300',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',
          'font-orbitron',

          // Variants
          variant === 'default' &&
            'bg-cyber-bg-secondary text-text-primary border-2 border-text-secondary hover:border-neon-cyan hover:text-neon-cyan hover:shadow-[0_0_20px_rgba(0,255,255,0.3)]',
          variant === 'neon-cyan' &&
            'border-2 border-neon-cyan text-neon-cyan shadow-[0_0_10px_rgba(0,255,255,0.3)] hover:bg-neon-cyan/10 hover:shadow-[0_0_30px_rgba(0,255,255,0.6)]',
          variant === 'neon-pink' &&
            'border-2 border-neon-pink text-neon-pink shadow-[0_0_10px_rgba(255,0,255,0.3)] hover:bg-neon-pink/10 hover:shadow-[0_0_30px_rgba(255,0,255,0.6)]',
          variant === 'neon-purple' &&
            'border-2 border-neon-purple text-neon-purple shadow-[0_0_10px_rgba(176,0,255,0.3)] hover:bg-neon-purple/10 hover:shadow-[0_0_30px_rgba(176,0,255,0.6)]',
          variant === 'ghost' &&
            'text-text-primary hover:bg-cyber-bg-secondary hover:text-neon-cyan',
          variant === 'outline' &&
            'border-2 border-text-secondary text-text-primary hover:border-neon-cyan hover:text-neon-cyan',

          // Sizes
          size === 'sm' && 'h-9 px-4 text-sm',
          size === 'md' && 'h-11 px-6 text-base',
          size === 'lg' && 'h-14 px-8 text-lg',
          size === 'icon' && 'h-11 w-11',

          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';

export { Button };
