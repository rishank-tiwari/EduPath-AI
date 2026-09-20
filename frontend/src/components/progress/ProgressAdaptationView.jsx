import React from 'react';
import { Card } from '../Card';
import { Badge } from '../Badge';
import { Button } from '../Button';
import { TrendingUp, RefreshCw, CheckCircle, AlertTriangle, ArrowRight, Activity } from 'lucide-react';

export function ProgressAdaptationView({ progressList, adaptationHistory, onTriggerAdaptation }) {
  if (!progressList || progressList.length === 0) {
    return (
      <Card className="p-8 text-center space-y-4 bg-surface border-border-subtle">
        <Activity className="w-12 h-12 mx-auto text-content-muted" />
        <h3 className="text-lg font-bold text-dark">No Progress Data Recorded Yet</h3>
        <p className="text-sm text-content-secondary max-w-md mx-auto">
          Complete a learning activity to start tracking progress.
        </p>
      </Card>
    );
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'strong':
        return <Badge variant="orange">You're doing well</Badge>;
      case 'on_track':
        return <Badge variant="blue">On Track</Badge>;
      case 'needs_review':
        return <Badge variant="orange">Needs a little more practice</Badge>;
      case 'struggling':
        return <Badge variant="orange">Let's review this topic</Badge>;
      default:
        return <Badge variant="neutral">{status}</Badge>;
    }
  };

  const latestAdaptation = adaptationHistory && adaptationHistory.length > 0 ? adaptationHistory[0] : null;

  return (
    <div className="space-y-6">
      {/* Progress Overview */}
      <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border-subtle pb-4">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
              Your Learning Trajectory
            </span>
            <h2 className="text-2xl font-extrabold text-dark tracking-tight mt-1">
              Progress & Adaptive Feedback
            </h2>
          </div>
          {onTriggerAdaptation && (
            <Button
              variant="primary"
              onClick={() => onTriggerAdaptation()}
              className="text-xs flex items-center gap-1.5"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Update Learning Path</span>
            </Button>
          )}
        </div>

        {/* Adaptation Alert Banner if plan was updated */}
        {latestAdaptation ? (
          <div className="p-4 rounded-lg bg-canvas border border-border-subtle flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-orange-text shrink-0 mt-0.5" />
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-extrabold text-dark uppercase">Your learning path was updated based on your result.</span>
                <Badge variant="neutral" className="text-[10px]">
                  v{latestAdaptation.new_plan_version}
                </Badge>
              </div>
              <p className="text-xs text-content-secondary mt-1">{latestAdaptation.reason}</p>
            </div>
          </div>
        ) : (
          <div className="p-3 rounded-lg bg-canvas border border-border-subtle text-xs text-content-secondary italic">
            No learning-path changes yet.
          </div>
        )}

        {/* Skill Progress Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          {progressList.map((item, idx) => (
            <div key={item.progress_id || idx} className="p-4 rounded-lg bg-canvas border border-border-subtle space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-dark">{item.skill_name}</span>
                {getStatusBadge(item.performance_status)}
              </div>

              <div className="flex items-center justify-between text-xs text-content-secondary pt-1">
                <span>Topic: <strong className="text-dark">{item.topic}</strong></span>
                <span>Latest Score: <strong className="text-dark">{item.latest_score}%</strong></span>
              </div>

              <div className="flex items-center justify-between text-[11px] text-content-muted border-t border-border-subtle pt-2 font-mono">
                <span>Attempts: {item.total_attempts}</span>
                <span className="capitalize">Trend: {item.trend.replace('_', ' ')}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
