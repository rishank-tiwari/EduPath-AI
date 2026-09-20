import React from 'react';
import { cn } from '../utils/cn';

export function Badge({ children, variant = 'orange', className, ...props }) {
  const variants = {
    orange: 'bg-orange-light text-orange-text border-orange-border',
    blue: 'bg-skyblue-light text-skyblue-text border-skyblue-border',
    dark: 'bg-dark text-canvas border-dark',
    sage: 'bg-sage-light text-sage border-sage-border',
    neutral: 'bg-surface-soft text-content-secondary border-border-subtle',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-xs font-bold border transition-colors',
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
