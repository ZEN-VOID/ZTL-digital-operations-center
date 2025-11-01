import * as React from 'react';
import { cn } from '@/lib/utils/cn';

export interface ToastProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Toast ID */
  id: string;
  /** Toast title */
  title?: string;
  /** Toast description */
  description?: string;
  /** Toast variant */
  variant?: 'default' | 'success' | 'error' | 'warning' | 'info';
  /** Duration in milliseconds (0 for persistent) */
  duration?: number;
  /** On close callback */
  onClose?: (id: string) => void;
}

const Toast = React.forwardRef<HTMLDivElement, ToastProps>(
  (
    {
      className,
      id,
      title,
      description,
      variant = 'default',
      duration = 3000,
      onClose,
      ...props
    },
    ref
  ) => {
    React.useEffect(() => {
      if (duration > 0) {
        const timer = setTimeout(() => {
          onClose?.(id);
        }, duration);

        return () => clearTimeout(timer);
      }
    }, [duration, id, onClose]);

    const variantStyles = {
      default: 'border-neon-cyan bg-cyber-bg-secondary/90 shadow-[0_0_20px_rgba(0,255,255,0.3)]',
      success: 'border-neon-green bg-cyber-bg-secondary/90 shadow-[0_0_20px_rgba(0,255,0,0.3)]',
      error: 'border-neon-pink bg-cyber-bg-secondary/90 shadow-[0_0_20px_rgba(255,0,255,0.3)]',
      warning:
        'border-yellow-500 bg-cyber-bg-secondary/90 shadow-[0_0_20px_rgba(234,179,8,0.3)]',
      info: 'border-neon-purple bg-cyber-bg-secondary/90 shadow-[0_0_20px_rgba(176,0,255,0.3)]',
    };

    const iconColors = {
      default: 'text-neon-cyan',
      success: 'text-neon-green',
      error: 'text-neon-pink',
      warning: 'text-yellow-500',
      info: 'text-neon-purple',
    };

    const icons = {
      default: 'ⓘ',
      success: '✓',
      error: '✕',
      warning: '⚠',
      info: 'ⓘ',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'relative flex gap-3 w-full max-w-md p-4 rounded-lg border-2 backdrop-blur-md',
          'animate-[message-appear_0.3s_ease-out] transition-all duration-300',
          variantStyles[variant],
          className
        )}
        {...props}
      >
        {/* Icon */}
        <div
          className={cn(
            'flex-shrink-0 w-6 h-6 flex items-center justify-center font-bold text-lg',
            iconColors[variant]
          )}
        >
          {icons[variant]}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {title && <h3 className="font-semibold text-sm text-text-primary mb-1">{title}</h3>}
          {description && (
            <p className="text-sm text-text-secondary leading-relaxed">{description}</p>
          )}
        </div>

        {/* Close button */}
        <button
          onClick={() => onClose?.(id)}
          className={cn(
            'flex-shrink-0 w-6 h-6 flex items-center justify-center rounded-md',
            'hover:bg-text-secondary/10 transition-colors',
            'text-text-secondary hover:text-text-primary'
          )}
          aria-label="Close"
        >
          ✕
        </button>

        {/* Progress bar (if duration > 0) */}
        {duration > 0 && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-text-secondary/20 rounded-b-lg overflow-hidden">
            <div
              className={cn('h-full', iconColors[variant])}
              style={{
                animation: `toast-progress ${duration}ms linear`,
                width: '100%',
              }}
            />
          </div>
        )}
      </div>
    );
  }
);

Toast.displayName = 'Toast';

export { Toast };

export interface ToasterProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Toast position */
  position?: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';
}

const Toaster = React.forwardRef<HTMLDivElement, ToasterProps>(
  ({ className, position = 'top-right', ...props }, ref) => {
    const positionClasses = {
      'top-left': 'top-6 left-6',
      'top-center': 'top-6 left-1/2 -translate-x-1/2',
      'top-right': 'top-6 right-6',
      'bottom-left': 'bottom-6 left-6',
      'bottom-center': 'bottom-6 left-1/2 -translate-x-1/2',
      'bottom-right': 'bottom-6 right-6',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'fixed z-[100] flex flex-col gap-3',
          positionClasses[position],
          className
        )}
        {...props}
      />
    );
  }
);

Toaster.displayName = 'Toaster';

export { Toaster };
