import React from 'react';
import { Loader2 } from 'lucide-react';
import { cn } from '../utils/cn';

export function LoadingState({ message = 'Loading workspace context...', className }) {
  return (
    <div className={cn('flex flex-col items-center justify-center p-12 text-center space-y-3', className)}>
      <Loader2 className="w-6 h-6 animate-spin text-terracotta" />
      <p className="text-xs text-content-secondary font-medium">{message}</p>
    </div>
  );
}
