import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { practiceService } from '../services/practiceService';
import { projectService } from '../services/projectService';
import { Button } from '../components/Button';
import { Badge } from '../components/Badge';
import { Card } from '../components/Card';
import { CheckCircle2, ArrowRight, BookOpen, Target, Clock, Code2, Sparkles } from 'lucide-react';

export function MyPathPage() {
  const navigate = useNavigate();
  const { userId, userProfile, skillGapAnalysis, learningPlan, setCurrentTask } = useApp();
  const [activeTab, setActiveTab] = useState('path'); // 'path' or 'gaps'
  const [recommendedProjects, setRecommendedProjects] = useState([]);

  const targetRole = userProfile?.target_role || skillGapAnalysis?.target_role || 'AI/ML Engineer';

  const gapsList = skillGapAnalysis?.skills || [];
  const strongSkills = gapsList.filter((s) => s.gap_status === 'strong' || s.gap_status === 'meets_requirement');
  const improveSkills = gapsList.filter((s) => s.gap_status === 'needs_improvement');
  const missingSkills = gapsList.filter((s) => s.gap_status === 'missing');

  const modules = learningPlan?.modules || [];

  useEffect(() => {
    async function fetchProjects() {
      try {
        const res = await projectService.getRecommendedProjects(userId || 'demo_user_1');
        if (res && res.projects) {
          setRecommendedProjects(res.projects);
        }
      } catch (err) {
        console.warn('Failed to load recommended projects:', err);
      }
    }
    fetchProjects();
  }, [userId]);

  const handleModuleAction = async (mod, isCompleted, isInProgress, score) => {
    const firstTask = mod.tasks && mod.tasks.length > 0 ? mod.tasks[0] : null;
    if (firstTask) {
      setCurrentTask({
        ...firstTask,
        module_id: mod.module_id,
        module_title: mod.title,
        module_completed: isCompleted,
        module_score: score,
        last_practice_id: mod.last_practice_id,
      });
    }

    if (isCompleted) {
      const practiceId = mod.last_practice_id;
      if (practiceId) {
        navigate(`/practice/result/${encodeURIComponent(practiceId)}`);
        return;
      }
      if (userId) {
        try {
          const history = await practiceService.getHistory(userId);
          const matched = history.find(
            (h) => h.module_id === mod.module_id || h.task_id === firstTask?.task_id || h.skill_name === mod.title
          );
          if (matched && (matched.practice_id || matched.result_id)) {
            navigate(`/practice/result/${encodeURIComponent(matched.practice_id || matched.result_id)}`);
            return;
          }
        } catch (err) {
          console.warn("Could not fetch practice history fallback:", err);
        }
      }
      navigate('/learn');
      return;
    }

    navigate('/learn');
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 text-xs font-bold text-orange-text uppercase tracking-wider font-mono">
          <Target className="w-4 h-4" />
          <span>YOUR PERSONALIZED ROADMAP</span>
        </div>
        <h1 className="text-3xl font-extrabold text-dark tracking-tight">
          Your {targetRole} Path
        </h1>
        <p className="text-sm text-content-secondary font-medium">
          A step-by-step learning journey customized based on your current skills and target role requirements.
        </p>

        {/* View Toggle Tabs */}
        <div className="flex items-center gap-2 pt-2 border-b border-border-subtle">
          <button
            onClick={() => setActiveTab('path')}
            className={`pb-3 px-4 text-xs font-bold transition-all border-b-2 ${
              activeTab === 'path'
                ? 'border-orange-text text-dark font-extrabold'
                : 'border-transparent text-content-secondary hover:text-dark'
            }`}
          >
            Learning Path ({modules.length} Modules)
          </button>
          <button
            onClick={() => setActiveTab('gaps')}
            className={`pb-3 px-4 text-xs font-bold transition-all border-b-2 ${
              activeTab === 'gaps'
                ? 'border-orange-text text-dark font-extrabold'
                : 'border-transparent text-content-secondary hover:text-dark'
            }`}
          >
            Skill Gap Intelligence ({gapsList.length} Benchmark Skills)
          </button>
        </div>
      </div>

      {/* VIEW 1: LEARNING PATH */}
      {activeTab === 'path' && (
        <div className="space-y-8">
          <div className="space-y-4">
            {modules.length > 0 ? (
              modules.map((mod, idx) => {
                const isCompleted = mod.status === 'completed' || mod.completion_status === 'completed';
                const isInProgress = mod.status === 'in_progress';
                const score = mod.latest_score ?? (isCompleted ? 80 : null);

                return (
                  <Card
                    key={mod.module_id || idx}
                    className={`p-5 bg-surface border border-border-subtle shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
                      isCompleted ? 'border-l-4 border-l-emerald-500' : idx === 0 ? 'border-l-4 border-l-orange-text' : ''
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <div className="w-9 h-9 rounded-xl bg-dark text-white flex items-center justify-center font-bold text-xs shrink-0">
                        Week {mod.week_number}
                      </div>

                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-extrabold text-base text-dark">{mod.title}</h3>
                          {isCompleted ? (
                            <Badge variant="orange" className="bg-emerald-50 text-emerald-700 border-emerald-200 text-[10px]">
                              ✓ Completed
                            </Badge>
                          ) : isInProgress ? (
                            <Badge variant="blue" className="text-[10px]">
                              In Progress
                            </Badge>
                          ) : (
                            <Badge variant="neutral" className="text-[10px]">
                              Not Started
                            </Badge>
                          )}
                        </div>
                        <p className="text-xs text-content-secondary leading-relaxed font-medium">
                          {mod.description}
                        </p>
                        <div className="flex items-center gap-3 text-[11px] text-content-muted font-mono pt-1">
                          <span>Est. duration: {mod.estimated_hours} hrs</span>
                          <span>• 5 Questions Practice</span>
                          {isCompleted && score !== null && (
                            <span className="font-bold text-emerald-700">• Score: {score}%</span>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="shrink-0 pt-2 sm:pt-0">
                      <Button
                        variant={isCompleted ? 'secondary' : 'primary'}
                        size="sm"
                        onClick={() => handleModuleAction(mod, isCompleted, isInProgress, score)}
                        className="gap-1.5 text-xs font-bold w-full sm:w-auto"
                      >
                        <span>{isCompleted ? 'View Result' : isInProgress ? 'Continue' : 'Start Learning'}</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Button>
                    </div>
                  </Card>
                );
              })
            ) : (
              <Card className="p-8 text-center space-y-4 bg-surface border-border-subtle">
                <BookOpen className="w-12 h-12 mx-auto text-content-muted" />
                <h3 className="text-lg font-bold text-dark">No Learning Path Found</h3>
                <p className="text-xs text-content-secondary">
                  Please complete onboarding to generate your personalized learning plan.
                </p>
              </Card>
            )}
          </div>

          {/* Recommended Portfolio Projects */}
          {recommendedProjects.length > 0 && (
            <div className="space-y-4 pt-4 border-t border-border-subtle">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-orange" />
                  <h2 className="text-lg font-extrabold text-dark">Recommended Skill Gap Projects</h2>
                </div>
                <span className="text-xs font-mono text-content-muted">Tailored to close identified gaps</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recommendedProjects.map((proj) => (
                  <Card key={proj.project_id} className="p-5 bg-surface border border-border-subtle shadow-card space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold font-mono px-2 py-0.5 rounded bg-orange-light text-orange-text">
                        {proj.difficulty}
                      </span>
                      <span className="text-[11px] font-mono text-content-muted">{proj.estimated_duration}</span>
                    </div>

                    <h3 className="font-extrabold text-sm text-dark">{proj.title}</h3>
                    <p className="text-xs text-content-secondary line-clamp-2 leading-relaxed">{proj.objective}</p>

                    <div className="flex flex-wrap gap-1.5 pt-1">
                      {proj.skills_practiced && proj.skills_practiced.map((s, i) => (
                        <span key={i} className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-soft border border-border-subtle text-skyblue-text">
                          {s}
                        </span>
                      ))}
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* VIEW 2: SKILL GAPS */}
      {activeTab === 'gaps' && (
        <div className="space-y-6">
          <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
            <h3 className="text-lg font-extrabold text-dark border-b border-border-subtle pb-3">
              Skill Deficit Breakdown for {targetRole}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Strong Skills */}
              <div className="space-y-3">
                <span className="text-xs font-extrabold text-emerald-600 uppercase tracking-wider">
                  Strong / Satisfied ({strongSkills.length})
                </span>
                <div className="space-y-2">
                  {strongSkills.map((s) => (
                    <div key={s.skill_name} className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs">
                      <div className="font-bold text-emerald-900">✓ {s.skill_name}</div>
                      <div className="text-[11px] text-emerald-700 mt-0.5">Current: {s.current_proficiency}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Needs Improvement */}
              <div className="space-y-3">
                <span className="text-xs font-extrabold text-orange-text uppercase tracking-wider">
                  Needs Practice ({improveSkills.length})
                </span>
                <div className="space-y-2">
                  {improveSkills.map((s) => (
                    <div key={s.skill_name} className="p-3 rounded-lg bg-canvas border border-border-subtle text-xs">
                      <div className="font-bold text-dark">{s.skill_name}</div>
                      <div className="text-[11px] text-content-secondary mt-0.5">Current: {s.current_proficiency} | Required: {s.required_proficiency}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="space-y-3">
                <span className="text-xs font-extrabold text-dark uppercase tracking-wider">
                  Missing Skills ({missingSkills.length})
                </span>
                <div className="space-y-2">
                  {missingSkills.map((s) => (
                    <div key={s.skill_name} className="p-3 rounded-lg bg-canvas border border-border-subtle text-xs">
                      <div className="font-bold text-dark">{s.skill_name}</div>
                      <div className="text-[11px] text-content-secondary mt-0.5">Required: {s.required_proficiency} | Priority: {s.priority}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
