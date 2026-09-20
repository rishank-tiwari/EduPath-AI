import React from 'react';
import { cn } from '../utils/cn';

export function SectionHeader({ title, subtitle, action, className }) {
  return (
    <div className={cn('flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-border-subtle', className)}>
      <div>
        <h2 className="text-lg font-semibold text-content-primary tracking-tight">{title}</h2>
        {subtitle && <p className="text-xs text-content-secondary mt-0.5">{subtitle}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
