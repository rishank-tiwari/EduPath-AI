import React, { useEffect } from 'react';
import { X } from 'lucide-react';
import { Button } from './Button';
import { cn } from '../utils/cn';

export function Modal({ isOpen, onClose, title, children, className }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.body.style.overflow = 'auto';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-surface-dark/40 backdrop-blur-xs">
      <div className={cn('w-full max-w-lg bg-surface border border-border-subtle rounded-lg shadow-floating overflow-hidden space-y-4 p-6', className)}>
        <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
          <h3 className="text-base font-semibold text-content-primary">{title}</h3>
          <Button variant="ghost" size="sm" onClick={onClose} aria-label="Close modal">
            <X className="w-4 h-4" />
          </Button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  );
}
