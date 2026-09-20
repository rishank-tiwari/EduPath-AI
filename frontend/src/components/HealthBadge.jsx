import React from 'react';
import { useHealthCheck } from '../hooks/useHealthCheck';
import { CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';

export function HealthBadge() {
  const { health, loading, error, refetch } = useHealthCheck();

  if (loading) {
    return (
      <div className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md bg-surface-soft text-content-muted border border-border-subtle">
        <RefreshCw className="w-3 h-3 animate-spin text-orange" />
        <span className="font-semibold">Checking API...</span>
      </div>
    );
  }

  if (error || !health) {
    return (
      <button
        onClick={refetch}
        title={error || "API offline"}
        className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md bg-orange-light text-orange-text border border-orange-border hover:bg-orange-light/80 transition-colors font-bold"
      >
        <AlertTriangle className="w-3.5 h-3.5 text-orange" />
        <span>API Offline</span>
      </button>
    );
  }

  const isDbConnected = health.database === 'connected';

  return (
    <button
      onClick={refetch}
      title={`Backend: ${health.service} v${health.version} | DB: ${health.database}`}
      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md bg-sage-light text-sage border border-sage-border hover:bg-sage-light/80 transition-colors font-bold"
    >
      <CheckCircle2 className="w-3.5 h-3.5 text-sage" />
      <span>API Active</span>
      <span className="opacity-40">|</span>
      <span className="text-[10px] text-sage">{isDbConnected ? 'DB Connected' : 'DB Degraded'}</span>
    </button>
  );
}
