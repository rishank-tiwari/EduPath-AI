import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Badge } from '../components/Badge';
import { PracticeView } from '../components/practice/PracticeView';
import { ArrowRight, BookOpen, Clock, CheckCircle2, ExternalLink, Loader2, Award, RotateCcw } from 'lucide-react';

export function TodayLearningPage() {
  const navigate = useNavigate();
  const {
    userId,
    currentTask,
    setCurrentTask,
    learningPlan,
    recommendedResources,
    loadResourcesForTask,
    generatePracticeForTask,
    activePracticeSession,
    submitPracticeAnswers,
    loadingState,
    errorState,
  } = useApp();

  const [mode, setMode] = useState('learn'); // 'learn' or 'practice'

  useEffect(() => {
    if (currentTask && recommendedResources.length === 0) {
      loadResourcesForTask(currentTask);
    }
  }, [currentTask]);

  const isModuleCompleted = currentTask?.module_completed || (
    learningPlan?.modules?.some(
      (m) => (m.module_id === currentTask?.module_id || m.title === currentTask?.module_title) && (m.status === 'completed' || m.completion_status === 'completed')
    )
  );

  const completedScore = currentTask?.module_score ?? 80;

  const handleStartPractice = async () => {
    if (currentTask) {
      const res = await generatePracticeForTask(currentTask, 'module', currentTask.module_id);
      if (res && res.isCompleted) {
        // Module is already completed, show completed view
        return;
      }
      setMode('practice');
    }
  };

  const handleResetPractice = () => {
    setMode('learn');
    navigate('/my-path');
  };

  const handleContinueNextModule = () => {
    if (learningPlan && learningPlan.modules) {
      const nextMod = learningPlan.modules.find(
        (m) => m.status !== 'completed' && m.completion_status !== 'completed'
      );
      if (nextMod && nextMod.tasks && nextMod.tasks.length > 0) {
        setCurrentTask({ ...nextMod.tasks[0], module_id: nextMod.module_id, module_title: nextMod.title });
        setMode('learn');
        return;
      }
    }
    navigate('/my-path');
  };

  if (!currentTask) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center space-y-4">
        <Card className="p-8 bg-surface border-border-subtle shadow-card space-y-4">
          <BookOpen className="w-12 h-12 mx-auto text-content-muted" />
          <h2 className="text-2xl font-extrabold text-dark">No Active Learning Task</h2>
          <p className="text-sm text-content-secondary max-w-md mx-auto">
            Please complete your profile or select a milestone task from your learning path.
          </p>
          <Button variant="primary" onClick={() => navigate('/onboarding')} className="text-xs font-bold">
            Start Onboarding
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
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
      ) : isModuleCompleted && mode !== 'practice' ? (
        /* COMPLETED MODULE SUMMARY VIEW */
        <Card className="p-8 bg-surface border-border-subtle shadow-card text-center space-y-6">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-600 mx-auto flex items-center justify-center font-bold text-2xl border border-emerald-200">
            ✓
          </div>
          <div className="space-y-2">
            <Badge variant="orange" className="bg-emerald-50 text-emerald-700 border-emerald-200 text-xs uppercase tracking-wider font-extrabold">
              MODULE COMPLETED ✅
            </Badge>
            <h2 className="text-3xl font-extrabold text-dark tracking-tight mt-2">
              {currentTask.module_title || currentTask.title}
            </h2>
            <p className="text-sm text-content-secondary max-w-md mx-auto">
              You have successfully completed the required practice for this module.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-canvas border border-border-subtle max-w-md mx-auto grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-xs font-bold text-content-muted uppercase">Your Score</div>
              <div className="text-3xl font-black text-dark tracking-tight mt-1">{completedScore}%</div>
            </div>
            <div>
              <div className="text-xs font-bold text-content-muted uppercase">Questions</div>
              <div className="text-3xl font-black text-dark tracking-tight mt-1">5 / 5</div>
            </div>
          </div>

          <div className="flex flex-wrap justify-center gap-4 pt-2">
            {currentTask?.last_practice_id && (
              <Button
                variant="outline"
                onClick={() => navigate(`/practice/result/${encodeURIComponent(currentTask.last_practice_id)}`)}
                className="text-xs font-bold"
              >
                View Result
              </Button>
            )}
            <Button variant="secondary" onClick={() => navigate('/my-path')} className="text-xs font-bold">
              View All Modules
            </Button>
            <Button variant="primary" onClick={handleContinueNextModule} className="flex items-center gap-1.5 text-xs font-extrabold">
              <span>Continue to Next Module</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </Card>
      ) : mode === 'practice' ? (
        <PracticeView
          task={currentTask}
          resources={recommendedResources}
          practiceSession={activePracticeSession}
          onSubmitPractice={submitPracticeAnswers}
          onReset={handleResetPractice}
        />
      ) : (
        <div className="space-y-6">
          {/* YOUR NEXT STEP Banner */}
          <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
              <div>
                <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
                  YOUR NEXT STEP
                </span>
                <h1 className="text-2xl font-extrabold text-dark tracking-tight mt-1">
                  {currentTask.title}
                </h1>
                <p className="text-xs text-content-secondary mt-1">
                  {currentTask.description}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="orange">{currentTask.skill_name}</Badge>
                <div className="flex items-center gap-1 text-xs text-content-muted font-bold font-mono">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{currentTask.estimated_minutes} min</span>
                </div>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-canvas border border-border-subtle text-xs text-content-secondary">
              <span className="font-bold text-dark">Why you're learning this: </span>
              <span>
                {currentTask.skill_name} is one of the target skills required for your role roadmap.
              </span>
            </div>
          </Card>

          {/* STEP 8: LEARNING RESOURCES */}
          <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <div className="flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-orange-text" />
                <h3 className="text-lg font-bold text-dark uppercase tracking-wider">Learn This Topic</h3>
              </div>
              <span className="text-xs text-content-muted font-mono font-bold">
                {recommendedResources.length} Resources Available
              </span>
            </div>

            {recommendedResources.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recommendedResources.map((res, idx) => (
                  <div key={res.resource_id || idx} className="p-4 rounded-lg bg-canvas border border-border-subtle space-y-3">
                    <div className="flex items-center justify-between">
                      <Badge variant="neutral" className="text-[10px] capitalize">
                        {res.resource_type === 'video' ? 'Watch this' : 'Read this'}
                      </Badge>
                      <span className="text-xs text-content-muted font-bold font-mono">{res.estimated_minutes} min</span>
                    </div>

                    <h4 className="text-sm font-bold text-dark">{res.title}</h4>
                    <p className="text-xs text-content-secondary line-clamp-2">{res.description}</p>

                    <div className="pt-2 border-t border-border-subtle/50 flex items-center justify-between">
                      <span className="text-[11px] text-content-muted font-bold">{res.source}</span>
                      {res.url && !res.url.includes('Placeholder') ? (
                        <a
                          href={res.url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 text-xs font-extrabold text-orange-text hover:underline"
                        >
                          <span>Open Resource</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      ) : (
                        <span className="text-xs text-content-muted italic">Configured Study Material</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-xs text-content-secondary italic">
                Resources for this topic are being prepared.
              </div>
            )}
          </Card>

          {/* STEP 9: READY TO PRACTICE */}
          <Card className="p-6 bg-surface border-border-subtle shadow-card flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-extrabold text-dark">Ready to practice?</h3>
              <p className="text-xs text-content-secondary mt-0.5">
                Test your understanding with 5 targeted practice questions for {currentTask.skill_name}.
              </p>
            </div>
            <Button variant="primary" onClick={handleStartPractice} className="gap-2 font-extrabold text-xs">
              <span>Start Practice (5 Questions)</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Card>
        </div>
      )}
    </div>
  );
}
