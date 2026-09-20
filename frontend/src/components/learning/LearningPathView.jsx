import React, { useState } from 'react';
import { Card } from '../Card';
import { Badge } from '../Badge';
import { Button } from '../Button';
import { Clock, CheckCircle2, Circle, ArrowRight, BookOpen, Layers } from 'lucide-react';

export function LearningPathView({ plan }) {
  const [selectedWeek, setSelectedWeek] = useState(1);

  if (!plan || !plan.modules) {
    return (
      <Card className="p-8 text-center space-y-4 bg-surface border-border-subtle">
        <Layers className="w-12 h-12 mx-auto text-content-muted" />
        <h3 className="text-lg font-bold text-dark">No Learning Path Generated Yet</h3>
        <p className="text-sm text-content-secondary max-w-md mx-auto">
          Complete your profile and run a skill gap analysis to generate your personalized learning path.
        </p>
      </Card>
    );
  }

  const currentModule = plan.modules.find((m) => m.week_number === selectedWeek) || plan.modules[0];

  return (
    <div className="space-y-6">
      {/* Overview Banner */}
      <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
              Your Learning Path
            </span>
            <h2 className="text-2xl font-extrabold text-dark tracking-tight mt-1">
              {plan.title || `${plan.target_role} Roadmap`}
            </h2>
            <p className="text-xs text-content-secondary mt-1 max-w-xl">
              {plan.summary}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle text-center">
              <div className="text-xs text-content-muted font-bold uppercase">Estimated Time</div>
              <div className="text-lg font-black text-dark">{plan.total_estimated_hours} hrs</div>
            </div>
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle text-center">
              <div className="text-xs text-content-muted font-bold uppercase">Duration</div>
              <div className="text-lg font-black text-dark">{plan.duration_weeks} Weeks</div>
            </div>
          </div>
        </div>
      </Card>

      {/* Week Selector Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {Array.from({ length: plan.duration_weeks }, (_, i) => i + 1).map((weekNum) => {
          const mod = plan.modules.find((m) => m.week_number === weekNum);
          const isSelected = selectedWeek === weekNum;
          return (
            <button
              key={weekNum}
              onClick={() => setSelectedWeek(weekNum)}
              className={`px-4 py-2.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap flex items-center gap-2 border ${
                isSelected
                  ? 'bg-dark text-white border-dark shadow-sm'
                  : 'bg-surface text-content-secondary border-border-subtle hover:border-dark/30'
              }`}
            >
              <span>Week {weekNum}</span>
              {mod && (
                <Badge variant={isSelected ? 'orange' : 'neutral'} className="text-[10px]">
                  {mod.skill_name}
                </Badge>
              )}
            </button>
          );
        })}
      </div>

      {/* Module Content */}
      {currentModule && (
        <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-6">
          <div className="flex items-start justify-between border-b border-border-subtle pb-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="orange">Week {currentModule.week_number}</Badge>
                <Badge variant={currentModule.priority === 'high' ? 'orange' : 'blue'}>
                  {currentModule.priority === 'high' ? 'Needs Practice' : 'Scheduled'}
                </Badge>
              </div>
              <h3 className="text-xl font-extrabold text-dark">{currentModule.title}</h3>
              <p className="text-xs text-content-secondary mt-1">{currentModule.description}</p>
            </div>
            <div className="flex items-center gap-1.5 text-xs text-content-muted font-bold">
              <Clock className="w-4 h-4" />
              <span>{currentModule.estimated_hours} hrs this week</span>
            </div>
          </div>

          {/* Prerequisite Notice if any */}
          {currentModule.prerequisites && currentModule.prerequisites.length > 0 && (
            <div className="p-3 rounded-md bg-canvas border border-border-subtle text-xs text-content-secondary flex items-center gap-2 font-medium">
              <span className="font-bold text-dark">Already Know This:</span>
              <span>Prerequisites met ({currentModule.prerequisites.join(', ')})</span>
            </div>
          )}

          {/* Tasks List */}
          <div className="space-y-3">
            <div className="text-xs font-extrabold text-dark uppercase tracking-wider">
              What to Learn (Tasks)
            </div>

            <div className="space-y-2">
              {currentModule.tasks.map((task, idx) => (
                <div
                  key={task.task_id || idx}
                  className="p-4 rounded-lg bg-canvas border border-border-subtle hover:border-dark/20 transition-all flex items-center justify-between gap-4"
                >
                  <div className="flex items-start gap-3">
                    <div className="mt-0.5 text-content-muted">
                      {task.status === 'completed' ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                      ) : (
                        <Circle className="w-5 h-5" />
                      )}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-dark">{task.title}</span>
                        <Badge variant="neutral" className="text-[10px] capitalize">
                          {task.task_type}
                        </Badge>
                      </div>
                      <p className="text-xs text-content-secondary mt-0.5">{task.description}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-xs text-content-muted font-mono font-bold flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {task.estimated_minutes} min
                    </span>
                    <Button variant="secondary" size="sm" className="text-xs">
                      Start Learning
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
