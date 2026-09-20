import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { PracticeView } from '../components/practice/PracticeView';
import { Card } from '../components/Card';
import { Loader2 } from 'lucide-react';

export function PracticePage() {
  const navigate = useNavigate();
  const {
    currentTask,
    skillGapAnalysis,
    generatePracticeForTask,
    activePracticeSession,
    submitPracticeAnswers,
    loadingState,
    errorState,
  } = useApp();

  const activeSkillName = currentTask?.skill_name || skillGapAnalysis?.skills?.[0]?.skill_name || 'Machine Learning';

  useEffect(() => {
    // Automatically generate 10-question general practice session matching active skill
    if (!activePracticeSession || activePracticeSession.practice_mode !== 'general' || activePracticeSession.skill_name !== activeSkillName) {
      const taskPayload = currentTask || {
        task_id: `task_${activeSkillName.toLowerCase().replace(/\s+/g, '_')}_10`,
        skill_name: activeSkillName,
        difficulty: 'beginner',
      };
      generatePracticeForTask(taskPayload, 'general');
    }
  }, [activeSkillName, activePracticeSession]);

  const handleReset = () => {
    navigate('/my-path');
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
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
        <PracticeView
          task={currentTask || { title: 'General Skill Assessment', skill_name: 'Statistics' }}
          resources={[]}
          practiceSession={activePracticeSession}
          onSubmitPractice={submitPracticeAnswers}
          onReset={handleReset}
        />
      )}
    </div>
  );
}
