import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Badge } from '../components/Badge';
import { ArrowRight, BookOpen, CheckCircle2, Clock, Sparkles, Target, Zap, AlertCircle, Layers } from 'lucide-react';

export function DashboardPage() {
  const navigate = useNavigate();
  const { userProfile, skillGapAnalysis, learningPlan, currentTask, loadResourcesForTask } = useApp();

  const targetRole = userProfile?.target_role || skillGapAnalysis?.target_role || 'AI/ML Engineer';
  const userName = userProfile?.name || 'Learner';

  const gapsList = skillGapAnalysis?.skills || [];
  const strongSkills = gapsList.filter((s) => s.gap_status === 'strong' || s.gap_status === 'meets_requirement');
  const improveSkills = gapsList.filter((s) => s.gap_status === 'needs_improvement');
  const missingSkills = gapsList.filter((s) => s.gap_status === 'missing');

  const handleStartTask = async () => {
    if (currentTask) {
      await loadResourcesForTask(currentTask);
      navigate('/learn');
    } else {
      navigate('/my-path');
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Goal Banner */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 sm:p-8 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <Badge variant="orange" className="text-xs font-bold">
              LEARNER DASHBOARD
            </Badge>
            <span className="text-xs text-content-muted">|</span>
            <span className="text-xs font-bold text-content-secondary">Goal: {targetRole}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-dark tracking-tight">
            Welcome back, {userName} 👋
          </h1>
          <p className="text-sm text-content-secondary font-medium">
            EduPath is guiding your journey to become an <strong className="text-dark">{targetRole}</strong>.
          </p>
        </div>

        {skillGapAnalysis && (
          <div className="flex items-center gap-4 bg-canvas p-4 rounded-xl border border-border-subtle">
            <div className="space-y-0.5 text-right">
              <div className="text-xs font-bold text-content-secondary">ROLE READINESS</div>
              <div className="text-xl font-extrabold text-dark font-mono">{skillGapAnalysis.overall_readiness}%</div>
            </div>
            <div className="w-12 h-12 rounded-full border-4 border-orange-text flex items-center justify-center font-bold text-xs text-dark bg-surface">
              {skillGapAnalysis.overall_readiness}%
            </div>
          </div>
        )}
      </div>

      {/* Dominant Primary Card: YOUR NEXT STEP */}
      <Card className="p-6 sm:p-8 bg-dark text-canvas border-dark shadow-floating space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-orange-text animate-pulse" />
            <span className="text-xs font-mono uppercase font-bold tracking-wider text-orange-text">
              YOUR NEXT STEP
            </span>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-canvas/70 font-mono">
            <Clock className="w-3.5 h-3.5 text-skyblue" />
            <span>Est. {currentTask?.estimated_minutes || 30} min</span>
          </div>
        </div>

        <div className="space-y-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-canvas tracking-tight">
            {currentTask?.title || 'Start Your First Learning Module'}
          </h2>
          <p className="text-sm text-canvas/80 leading-relaxed font-medium max-w-2xl">
            {currentTask?.description || 'Study key theoretical concepts, formulas, and practical implementations.'}
          </p>
        </div>

        <div className="pt-2 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-t border-canvas/15">
          <div className="flex items-center gap-3 text-xs text-canvas/70">
            <Badge variant="blue" className="px-2.5 py-0.5">{currentTask?.skill_name || 'Statistics'}</Badge>
            <span>Difficulty: {currentTask?.difficulty || 'Beginner'}</span>
          </div>

          <Button variant="primary" size="md" onClick={handleStartTask} className="gap-2 shadow-subtle">
            <span>Start Learning</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </Card>

      {/* Grid: Skill Gaps & Learning Path Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Skill Gap Analysis ("Where you are today") */}
        <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-5">
          <div className="flex items-center justify-between border-b border-border-subtle pb-3">
            <div>
              <span className="text-xs font-mono uppercase text-orange-text font-bold">Skill Intelligence</span>
              <h3 className="text-xl font-extrabold text-dark">Where you are today</h3>
            </div>
            <Link to="/my-path">
              <Button variant="outline" size="sm" className="text-xs">View Details</Button>
            </Link>
          </div>

          <div className="space-y-4">
            {/* Strong Skills */}
            {strongSkills.length > 0 && (
              <div className="space-y-2">
                <span className="text-xs font-extrabold text-emerald-600 uppercase">Strong Skills</span>
                <div className="flex flex-wrap gap-2">
                  {strongSkills.map((s) => (
                    <Badge key={s.skill_name} variant="neutral" className="bg-emerald-50 text-emerald-700 border-emerald-200">
                      ✓ {s.skill_name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Needs Practice */}
            {improveSkills.length > 0 && (
              <div className="space-y-2">
                <span className="text-xs font-extrabold text-orange-text uppercase">Needs Practice</span>
                <div className="flex flex-wrap gap-2">
                  {improveSkills.map((s) => (
                    <Badge key={s.skill_name} variant="orange">
                      {s.skill_name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* Needs to Learn */}
            {missingSkills.length > 0 && (
              <div className="space-y-2">
                <span className="text-xs font-extrabold text-dark uppercase">Needs to Learn</span>
                <div className="flex flex-wrap gap-2">
                  {missingSkills.map((s) => (
                    <Badge key={s.skill_name} variant="blue">
                      {s.skill_name}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Card>

        {/* Learning Path ("Your Learning Path") */}
        <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-5">
          <div className="flex items-center justify-between border-b border-border-subtle pb-3">
            <div>
              <span className="text-xs font-mono uppercase text-orange-text font-bold">Personalized Roadmap</span>
              <h3 className="text-xl font-extrabold text-dark">Your Learning Path</h3>
            </div>
            <Link to="/my-path">
              <Button variant="outline" size="sm" className="text-xs">Full Path</Button>
            </Link>
          </div>

          {learningPlan && learningPlan.modules ? (
            <div className="space-y-3">
              {learningPlan.modules.slice(0, 4).map((mod) => (
                <div key={mod.module_id} className="p-3 rounded-lg bg-canvas border border-border-subtle flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Badge variant="orange" className="text-[10px]">Week {mod.week_number}</Badge>
                    <div>
                      <div className="text-xs font-bold text-dark">{mod.title}</div>
                      <div className="text-[11px] text-content-secondary">{mod.skill_name}</div>
                    </div>
                  </div>
                  <span className="text-xs font-mono font-bold text-content-muted">{mod.estimated_hours} hrs</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-xs text-content-secondary italic">
              No learning path generated yet. Complete your profile to build a custom roadmap.
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
