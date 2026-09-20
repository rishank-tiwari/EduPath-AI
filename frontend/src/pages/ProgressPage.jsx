import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Badge } from '../components/Badge';
import { ProgressAdaptationView } from '../components/progress/ProgressAdaptationView';
import { TrendingUp, RefreshCw, Loader2, ArrowRight } from 'lucide-react';

export function ProgressPage() {
  const navigate = useNavigate();
  const {
    userId,
    progressSummaries,
    adaptationHistory,
    triggerAdaptation,
    loadingState,
    errorState,
    currentTask,
    loadResourcesForTask,
  } = useApp();

  const handleStartNextStep = async () => {
    if (currentTask) {
      await loadResourcesForTask(currentTask);
      navigate('/learn');
    } else {
      navigate('/dashboard');
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <Badge variant="orange" className="text-xs font-bold">
            PROGRESS & ADAPTIVE LEARNING
          </Badge>
          <h1 className="text-3xl font-extrabold text-dark tracking-tight mt-1">
            Your Performance & Trajectory
          </h1>
          <p className="text-sm text-content-secondary">
            See how well you're retaining concepts and how your learning path adapts.
          </p>
        </div>

        <Button
          variant="primary"
          onClick={() => triggerAdaptation()}
          className="flex items-center gap-1.5 text-xs font-bold shrink-0"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Update Learning Path</span>
        </Button>
      </div>

      {/* Error Alert */}
      {errorState && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-bold">
          {errorState}
        </div>
      )}

      {/* Loading Overlay */}
      {loadingState ? (
        <Card className="p-12 text-center space-y-4 bg-surface border-border-subtle shadow-card">
          <Loader2 className="w-10 h-10 mx-auto text-orange-text animate-spin" />
          <h3 className="text-xl font-extrabold text-dark">{loadingState}</h3>
        </Card>
      ) : (
        <div className="space-y-6">
          <ProgressAdaptationView
            progressList={progressSummaries}
            adaptationHistory={adaptationHistory}
            onTriggerAdaptation={triggerAdaptation}
          />

          {/* Action CTA Banner */}
          <Card className="p-6 bg-dark text-canvas border-dark shadow-floating flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <span className="text-xs font-mono uppercase text-orange-text font-bold">NEXT STEP AVAILABLE</span>
              <h3 className="text-xl font-extrabold text-canvas mt-0.5">
                {currentTask ? currentTask.title : 'Continue Your Roadmap'}
              </h3>
              <p className="text-xs text-canvas/80 mt-1">
                {currentTask ? `Focus area: ${currentTask.skill_name}` : 'Ready for your next learning session.'}
              </p>
            </div>
            <Button variant="primary" onClick={handleStartNextStep} className="gap-2 text-xs font-extrabold shrink-0">
              <span>Start Next Step</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Card>
        </div>
      )}
    </div>
  );
}
