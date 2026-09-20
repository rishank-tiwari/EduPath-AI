import React from 'react';
import { cn } from '../utils/cn';

export function ProgressBar({ value = 0, max = 100, variant = 'orange', className, label, showValue = true }) {
  const percentage = Math.min(100, Math.max(0, Math.round((value / max) * 100)));

  const barColors = {
    orange: 'bg-orange',
    blue: 'bg-skyblue',
    dark: 'bg-dark',
    sage: 'bg-sage',
  };

  return (
    <div className={cn('w-full space-y-1.5', className)}>
      {(label || showValue) && (
        <div className="flex items-center justify-between text-xs font-bold text-dark">
          {label && <span>{label}</span>}
          {showValue && <span>{percentage}%</span>}
        </div>
      )}
      <div className="w-full h-2.5 rounded-full bg-surface-soft overflow-hidden border border-border-subtle">
        <div
          className={cn('h-full rounded-full transition-all duration-500 ease-out', barColors[variant])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
