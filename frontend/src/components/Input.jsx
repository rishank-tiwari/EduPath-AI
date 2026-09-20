import React from 'react';
import { cn } from '../utils/cn';

export function Input({ label, error, className, icon: Icon, ...props }) {
  return (
    <div className="w-full space-y-1.5">
      {label && <label className="block text-xs font-medium text-content-primary">{label}</label>}
      <div className="relative flex items-center">
        {Icon && <Icon className="w-4 h-4 text-content-muted absolute left-3 pointer-events-none" />}
        <input
          className={cn(
            'w-full px-3 py-2 text-sm rounded-md bg-surface border border-border-subtle text-content-primary placeholder:text-content-muted transition-colors focus:outline-none focus:border-content-primary focus:ring-1 focus:ring-content-primary',
            Icon && 'pl-9',
            error && 'border-terracotta focus:border-terracotta focus:ring-terracotta',
            className
          )}
          {...props}
        />
      </div>
      {error && <p className="text-xs text-terracotta font-medium">{error}</p>}
    </div>
  );
}
