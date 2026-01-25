import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  variant?: 'default' | 'neon-cyan' | 'neon-pink' | 'neon-purple';
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, variant = 'default', type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          // Base styles
          'flex h-11 w-full rounded-lg px-4 py-2 text-base transition-all duration-300',
          'font-electrolize text-text-primary placeholder:text-text-secondary/50',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-cyber-bg-primary',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'file:border-0 file:bg-transparent file:text-sm file:font-medium',

          // Variants
          variant === 'default' &&
            'bg-cyber-bg-secondary/50 border-2 border-text-secondary/30 focus-visible:border-neon-cyan focus-visible:ring-neon-cyan/50 focus-visible:shadow-[0_0_20px_rgba(0,255,255,0.3)]',
          variant === 'neon-cyan' &&
            'bg-cyber-bg-secondary/30 border-2 border-neon-cyan/50 focus-visible:border-neon-cyan focus-visible:ring-neon-cyan focus-visible:shadow-[0_0_30px_rgba(0,255,255,0.5)]',
          variant === 'neon-pink' &&
            'bg-cyber-bg-secondary/30 border-2 border-neon-pink/50 focus-visible:border-neon-pink focus-visible:ring-neon-pink focus-visible:shadow-[0_0_30px_rgba(255,0,255,0.5)]',
          variant === 'neon-purple' &&
            'bg-cyber-bg-secondary/30 border-2 border-neon-purple/50 focus-visible:border-neon-purple focus-visible:ring-neon-purple focus-visible:shadow-[0_0_30px_rgba(176,0,255,0.5)]',

          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);

Input.displayName = 'Input';

export { Input };
