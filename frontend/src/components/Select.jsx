import React from 'react';
import { cn } from '../utils/cn';

export function Select({ label, options = [], className, error, ...props }) {
  return (
    <div className="w-full space-y-1.5">
      {label && <label className="block text-xs font-medium text-content-primary">{label}</label>}
      <select
        className={cn(
          'w-full px-3 py-2 text-sm rounded-md bg-surface border border-border-subtle text-content-primary transition-colors focus:outline-none focus:border-content-primary focus:ring-1 focus:ring-content-primary',
          error && 'border-terracotta focus:border-terracotta focus:ring-terracotta',
          className
        )}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="text-xs text-terracotta font-medium">{error}</p>}
    </div>
  );
}
