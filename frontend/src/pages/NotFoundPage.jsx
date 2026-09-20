import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { ArrowLeft } from 'lucide-react';

export function NotFoundPage() {
  return (
    <div className="py-16 flex items-center justify-center">
      <Card className="max-w-md w-full text-center space-y-5 p-8 border-border-subtle bg-surface shadow-card">
        <h1 className="text-5xl font-extrabold text-terracotta font-mono">404</h1>
        <div className="space-y-1">
          <h2 className="text-lg font-bold text-content-primary">Page Not Found</h2>
          <p className="text-xs text-content-secondary leading-relaxed">
            The requested workspace path does not exist in the EduPath application shell.
          </p>
        </div>
        <div className="pt-2">
          <Link to="/">
            <Button variant="primary" size="md" className="gap-2">
              <ArrowLeft className="w-4 h-4" />
              <span>Return to Overview</span>
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
}
