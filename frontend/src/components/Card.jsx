import React from 'react';
import { cn } from '../utils/cn';

export function Card({ children, className, hoverEffect = false, ...props }) {
  return (
    <div
      className={cn(
        'bg-surface border border-border-subtle rounded-md p-6 shadow-card transition-all duration-200',
        hoverEffect && 'hover:border-orange-border hover:shadow-floating',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
