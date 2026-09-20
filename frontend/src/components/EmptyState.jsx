import React from 'react';
import { Layers } from 'lucide-react';
import { cn } from '../utils/cn';

export function EmptyState({ title, description, action, icon: Icon = Layers, className }) {
  return (
    <div className={cn('flex flex-col items-center justify-center p-8 text-center bg-surface border border-border-subtle rounded-md space-y-3', className)}>
      <div className="w-10 h-10 rounded-full bg-surface-secondary flex items-center justify-center text-content-secondary">
        <Icon className="w-5 h-5" />
      </div>
      <div className="space-y-1 max-w-sm">
        <h4 className="text-sm font-semibold text-content-primary">{title}</h4>
        {description && <p className="text-xs text-content-secondary leading-relaxed">{description}</p>}
      </div>
      {action && <div className="pt-2">{action}</div>}
    </div>
  );
}
