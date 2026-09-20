import { useState, useEffect, useCallback } from 'react';
import { healthService } from '../services/healthService';

export function useHealthCheck() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHealth = useCallback(async () => {
    setLoading(true);
    try {
      const data = await healthService.checkHealth();
      setHealth(data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to reach API server');
      setHealth(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHealth();
  }, [fetchHealth]);

  return { health, loading, error, refetch: fetchHealth };
}
