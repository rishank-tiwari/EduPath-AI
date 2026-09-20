import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Badge } from '../components/Badge';
import { BookOpen, Target, CheckCircle2, ArrowRight, Lightbulb, Compass, Award } from 'lucide-react';

export function LearningGuidePage() {
  const navigate = useNavigate();
  const { userProfile, skillGapAnalysis, learningPlan, currentTask } = useApp();

  const targetRole = userProfile?.target_role || skillGapAnalysis?.target_role;
  const isProfileComplete = Boolean(targetRole && learningPlan?.modules && learningPlan.modules.length > 0);

  if (!isProfileComplete) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <Card className="p-8 bg-surface border-border-subtle shadow-card space-y-4 max-w-lg mx-auto">
          <Compass className="w-12 h-12 mx-auto text-orange-text" />
          <h2 className="text-2xl font-extrabold text-dark tracking-tight">Personalized Learning Guide</h2>
          <p className="text-xs text-content-secondary leading-relaxed">
            Complete your learner profile to get a personalized guide tailored to your career goals and skill gap analysis.
          </p>
          <Button
            variant="primary"
            onClick={() => navigate('/onboarding')}
            className="text-xs font-extrabold gap-1.5 mx-auto"
          >
            <span>Complete Learner Profile</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </Card>
      </div>
    );
  }

  const modules = learningPlan.modules || [];
  const activeModule = modules.find((m) => m.status !== 'completed' && m.completion_status !== 'completed') || modules[0];
  const gaps = skillGapAnalysis?.skills || [];
  const missing = gaps.filter((g) => g.gap_status === 'missing' || g.gap_status === 'needs_improvement');
  const strong = gaps.filter((g) => g.gap_status === 'strong' || g.gap_status === 'meets_requirement');

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center gap-2 text-xs font-mono font-extrabold text-orange-text uppercase tracking-wider">
          <BookOpen className="w-4 h-4" />
          <span>PERSONALIZED ROADMAP GUIDE</span>
        </div>
        <h1 className="text-3xl font-extrabold text-dark tracking-tight">
          Learning Guide for {targetRole}
        </h1>
        <p className="text-xs text-content-secondary font-medium">
          A customized overview of your current milestones, key benchmark requirements, and study recommendations.
        </p>
      </div>

      {/* Main Focus Card */}
      <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
        <div className="flex items-center justify-between border-b border-border-subtle pb-3">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-orange-text" />
            <h2 className="text-base font-extrabold text-dark">Current Recommended Focus</h2>
          </div>
          <Badge variant="orange" className="text-xs font-bold">
            Active Milestone
          </Badge>
        </div>

        {activeModule && (
          <div className="p-4 rounded-xl bg-canvas border border-border-subtle space-y-2">
            <span className="text-[10px] font-mono font-bold text-content-muted uppercase">
              Week {activeModule.week_number} Module
            </span>
            <h3 className="text-lg font-black text-dark">{activeModule.title}</h3>
            <p className="text-xs text-content-secondary leading-relaxed">{activeModule.description}</p>
            <div className="pt-2 flex items-center justify-between">
              <span className="text-xs font-bold text-orange-text font-mono">
                Skill: {activeModule.skill_name}
              </span>
              <Button
                variant="primary"
                size="sm"
                onClick={() => navigate('/learn')}
                className="text-xs font-bold gap-1.5"
              >
                <span>Study Module</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Button>
            </div>
          </div>
        )}
      </Card>

      {/* Benchmark Requirements & Gaps */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-3">
          <div className="flex items-center gap-2 border-b border-border-subtle pb-3">
            <Target className="w-4 h-4 text-orange-text" />
            <h3 className="text-sm font-extrabold text-dark">Priority Skill Deficits ({missing.length})</h3>
          </div>
          <div className="space-y-2">
            {missing.map((g) => (
              <div key={g.skill_name} className="p-3 rounded-lg bg-canvas border border-border-subtle text-xs space-y-1">
                <div className="font-bold text-dark">{g.skill_name}</div>
                <div className="text-[11px] text-content-secondary">
                  Target Proficiency: <span className="font-bold text-dark">{g.required_proficiency}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-3">
          <div className="flex items-center gap-2 border-b border-border-subtle pb-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <h3 className="text-sm font-extrabold text-dark">Satisfied Prerequisites ({strong.length})</h3>
          </div>
          <div className="space-y-2">
            {strong.map((g) => (
              <div key={g.skill_name} className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs space-y-1">
                <div className="font-bold text-emerald-900">✓ {g.skill_name}</div>
                <div className="text-[11px] text-emerald-700">
                  Current: <span className="font-bold">{g.current_proficiency}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Action Footer */}
      <div className="flex justify-center pt-2">
        <Button variant="secondary" onClick={() => navigate('/my-path')} className="text-xs font-bold gap-1.5">
          <span>View Complete Path Roadmap</span>
          <ArrowRight className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
