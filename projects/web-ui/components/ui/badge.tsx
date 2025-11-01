import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const badgeVariants = cva(
  'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-cyber-bg-tertiary text-text-primary hover:bg-cyber-bg-tertiary/80',
        secondary:
          'border-transparent bg-cyber-bg-secondary text-text-secondary hover:bg-cyber-bg-secondary/80',
        destructive:
          'border-transparent bg-red-500/20 text-red-400 hover:bg-red-500/30',
        outline: 'text-text-primary border-neon-cyan/30 hover:bg-neon-cyan/10',
        'neon-cyan':
          'border-neon-cyan/50 bg-neon-cyan/10 text-neon-cyan shadow-sm shadow-neon-cyan/20 hover:bg-neon-cyan/20',
        'neon-pink':
          'border-neon-pink/50 bg-neon-pink/10 text-neon-pink shadow-sm shadow-neon-pink/20 hover:bg-neon-pink/20',
        'neon-purple':
          'border-neon-purple/50 bg-neon-purple/10 text-neon-purple shadow-sm shadow-neon-purple/20 hover:bg-neon-purple/20',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={badgeVariants({ variant })} {...props} />
  );
}

export { Badge, badgeVariants };
