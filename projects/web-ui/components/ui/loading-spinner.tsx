import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface LoadingSpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Spinner size */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Spinner variant */
  variant?: 'default' | 'neon-cyan' | 'neon-pink' | 'neon-purple';
  /** Show loading text */
  text?: string;
  /** Text position */
  textPosition?: 'bottom' | 'right';
  /** Fullscreen overlay */
  fullscreen?: boolean;
}

const LoadingSpinner = React.forwardRef<HTMLDivElement, LoadingSpinnerProps>(
  (
    {
      className,
      size = 'md',
      variant = 'neon-cyan',
      text,
      textPosition = 'bottom',
      fullscreen = false,
      ...props
    },
    ref
  ) => {
    const sizeClasses = {
      sm: 'w-4 h-4 border-2',
      md: 'w-8 h-8 border-3',
      lg: 'w-12 h-12 border-4',
      xl: 'w-16 h-16 border-4',
    };

    const variantClasses = {
      default: 'border-text-primary border-t-transparent',
      'neon-cyan': 'border-neon-cyan border-t-transparent shadow-[0_0_10px_rgba(0,255,255,0.5)]',
      'neon-pink': 'border-neon-pink border-t-transparent shadow-[0_0_10px_rgba(255,0,255,0.5)]',
      'neon-purple':
        'border-neon-purple border-t-transparent shadow-[0_0_10px_rgba(176,0,255,0.5)]',
    };

    const textColorClasses = {
      default: 'text-text-primary',
      'neon-cyan': 'text-neon-cyan',
      'neon-pink': 'text-neon-pink',
      'neon-purple': 'text-neon-purple',
    };

    const spinner = (
      <div
        className={cn(
          'rounded-full animate-spin',
          sizeClasses[size],
          variantClasses[variant]
        )}
      />
    );

    const content = (
      <div
        ref={ref}
        className={cn(
          'flex items-center gap-3',
          textPosition === 'bottom' ? 'flex-col' : 'flex-row',
          className
        )}
        {...props}
      >
        {spinner}
        {text && (
          <p
            className={cn(
              'text-sm font-medium',
              textColorClasses[variant],
              size === 'sm' && 'text-xs',
              size === 'lg' && 'text-base',
              size === 'xl' && 'text-lg'
            )}
          >
            {text}
          </p>
        )}
      </div>
    );

    if (fullscreen) {
      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-cyber-bg-primary/80 backdrop-blur-sm">
          {content}
        </div>
      );
    }

    return content;
  }
);

LoadingSpinner.displayName = 'LoadingSpinner';

export { LoadingSpinner };
