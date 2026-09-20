import React from 'react';
import { cn } from '../utils/cn';

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  className,
  disabled,
  ...props
}) {
  const baseStyles =
    'inline-flex items-center justify-center font-bold rounded-md transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-dark/20 disabled:opacity-50 disabled:cursor-not-allowed select-none shadow-subtle';

  const variants = {
    primary:
      'bg-orange text-dark hover:bg-orange-hover active:scale-[0.99] border border-orange-hover/30',
    secondary:
      'bg-transparent text-dark border-2 border-dark hover:bg-orange-light active:scale-[0.99]',
    blue:
      'bg-skyblue text-dark hover:bg-skyblue-hover active:scale-[0.99] border border-skyblue-border',
    dark:
      'bg-dark text-canvas hover:bg-dark-hover active:scale-[0.99]',
    outline:
      'bg-surface text-dark hover:bg-surface-soft border border-border-subtle active:scale-[0.99]',
    ghost:
      'bg-transparent text-content-secondary hover:text-dark hover:bg-orange-light/60 shadow-none',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2.5',
  };

  return (
    <button
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}
