import React, { useState } from 'react';
import { Card } from '../Card';
import { Badge } from '../Badge';
import { Button } from '../Button';
import { BookOpen, ExternalLink, CheckCircle2, Award, RotateCcw, ArrowRight, ArrowLeft } from 'lucide-react';

export function PracticeView({ task, resources, practiceSession, onSubmitPractice, onReset }) {
  const [userAnswers, setUserAnswers] = useState({});
  const [currentQIdx, setCurrentQIdx] = useState(0);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const questions = practiceSession?.questions || [];
  const totalQuestions = questions.length;
  const currentQuestion = questions[currentQIdx];

  const handleOptionSelect = (qId, option) => {
    setUserAnswers((prev) => ({
      ...prev,
      [qId]: option,
    }));
  };

  const handleTextChange = (qId, text) => {
    setUserAnswers((prev) => ({
      ...prev,
      [qId]: text,
    }));
  };

  const handleNext = () => {
    if (currentQIdx < totalQuestions - 1) {
      setCurrentQIdx((prev) => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentQIdx > 0) {
      setCurrentQIdx((prev) => prev - 1);
    }
  };

  const handleSubmit = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    if (!practiceSession || !onSubmitPractice || submitting) return;

    setSubmitError(null);
    setSubmitting(true);
    try {
      const answersList = Object.entries(userAnswers).map(([qId, val]) => ({
        question_id: qId,
        learner_answer: val,
      }));
      const res = await onSubmitPractice(practiceSession.practice_id, answersList);
      if (res) {
        setResult(res);
      }
    } catch (err) {
      console.error('Submission failed:', err);
      setSubmitError("We couldn't check your answers right now. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Task Header */}
      <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-2">
        <div className="flex items-center gap-2">
          <Badge variant="orange">Practice &amp; Assessment</Badge>
          <Badge variant="neutral">{task?.skill_name || 'General'}</Badge>
        </div>
        <h2 className="text-2xl font-extrabold text-dark">{task?.title || 'Test Your Knowledge'}</h2>
        <p className="text-sm text-content-secondary">
          {task?.description || 'Answer all questions to solidify your understanding and track your progress.'}
        </p>
      </Card>

      {/* Recommended Learning Resources */}
      {resources && resources.length > 0 && !result && (
        <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-orange-text" />
            <h3 className="text-lg font-bold text-dark uppercase tracking-wider">Learn This Topics</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {resources.map((res, i) => (
              <div key={res.resource_id || i} className="p-4 rounded-lg bg-canvas border border-border-subtle space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="neutral" className="text-[10px] capitalize">
                    {res.resource_type === 'video' ? 'Watch this' : 'Read this'}
                  </Badge>
                  <span className="text-xs text-content-muted font-bold">{res.estimated_minutes} min</span>
                </div>
                <h4 className="text-sm font-bold text-dark">{res.title}</h4>
                <p className="text-xs text-content-secondary line-clamp-2">{res.description}</p>
                {res.url && !res.url.includes('Placeholder') ? (
                  <a
                    href={res.url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs font-extrabold text-orange-text hover:underline pt-1"
                  >
                    <span>Open Resource</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                ) : (
                  <span className="text-xs text-content-muted italic">Configured Study Material</span>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Practice Question Session */}
      {practiceSession && !result && currentQuestion && (
        <Card className="p-6 sm:p-8 bg-surface border-border-subtle shadow-card space-y-6">
          <div className="flex items-center justify-between border-b border-border-subtle pb-3">
            <span className="text-xs font-mono font-bold text-orange-text uppercase tracking-wider">
              Question {currentQIdx + 1} of {totalQuestions}
            </span>
            <Badge variant="neutral" className="text-[10px] font-mono capitalize">
              {currentQuestion.difficulty}
            </Badge>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-canvas rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-orange-text h-1.5 transition-all duration-300"
              style={{ width: `${((currentQIdx + 1) / totalQuestions) * 100}%` }}
            />
          </div>

          <div className="space-y-4 pt-2">
            <h3 className="text-lg font-extrabold text-dark leading-snug">
              {currentQuestion.question}
            </h3>

            {currentQuestion.question_type === 'mcq' && currentQuestion.options ? (
              <div className="space-y-2.5 pt-2">
                {currentQuestion.options.map((opt, oIdx) => {
                  const isChecked = userAnswers[currentQuestion.question_id] === opt;
                  return (
                    <button
                      key={oIdx}
                      onClick={() => handleOptionSelect(currentQuestion.question_id, opt)}
                      className={`w-full text-left p-4 rounded-xl text-xs font-bold transition-all flex items-center justify-between border ${
                        isChecked
                          ? 'bg-dark text-white border-dark shadow-sm'
                          : 'bg-canvas text-content-secondary border-border-subtle hover:border-dark/30'
                      }`}
                    >
                      <span>{opt}</span>
                      {isChecked && <CheckCircle2 className="w-4 h-4 text-orange-text shrink-0" />}
                    </button>
                  );
                })}
              </div>
            ) : (
              <textarea
                rows={3}
                placeholder="Type your answer here..."
                value={userAnswers[currentQuestion.question_id] || ''}
                onChange={(e) => handleTextChange(currentQuestion.question_id, e.target.value)}
                className="w-full p-4 rounded-xl border border-border-subtle text-xs bg-canvas text-dark focus:outline-none focus:border-dark"
              />
            )}
          </div>

          {submitError && (
            <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-bold">
              {submitError}
            </div>
          )}

          <div className="pt-4 border-t border-border-subtle flex items-center justify-between">
            <Button
              variant="secondary"
              onClick={handlePrev}
              disabled={currentQIdx === 0 || submitting}
              className="flex items-center gap-1.5 text-xs font-bold"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </Button>

            {currentQIdx < totalQuestions - 1 ? (
              <Button variant="primary" onClick={handleNext} disabled={submitting} className="flex items-center gap-1.5 text-xs font-bold">
                <span>Next Question</span>
                <ArrowRight className="w-4 h-4" />
              </Button>
            ) : (
              <Button variant="primary" onClick={handleSubmit} disabled={submitting} className="font-extrabold text-xs">
                {submitting ? 'Checking...' : 'Check Your Answers'}
              </Button>
            )}
          </div>
        </Card>
      )}

      {/* Practice Results View */}
      {result && (
        <Card className="p-6 sm:p-8 bg-surface border-border-subtle shadow-card space-y-6">
          <div className="p-6 rounded-2xl bg-canvas border border-border-subtle text-center space-y-3">
            <Award className="w-12 h-12 mx-auto text-orange-text" />
            <div>
              <span className="text-xs font-mono uppercase tracking-wider font-extrabold text-content-muted">
                {task?.module_id ? 'MODULE COMPLETE ✅' : 'PRACTICE COMPLETED 🏆'}
              </span>
              <div className="text-4xl font-black text-dark tracking-tight mt-1">
                {result.score} / {result.total_questions} correct
              </div>
              <div className="text-sm font-bold text-orange-text mt-1">
                {result.percentage}% Score
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="text-xs font-extrabold text-dark uppercase tracking-wider">Review Questions &amp; Explanations</h4>
            <div className="space-y-3">
              {result.question_results.map((resItem, i) => (
                <div key={resItem.question_id || i} className="p-4 rounded-xl bg-canvas border border-border-subtle space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-dark font-mono">Question {i + 1}</span>
                    <Badge variant={resItem.correct ? 'orange' : 'neutral'}>
                      {resItem.correct ? 'Correct' : 'Needs Review'}
                    </Badge>
                  </div>
                  <p className="text-xs font-bold text-dark">{resItem.question}</p>

                  <div className="text-xs space-y-1 pt-1">
                    <div className="text-content-secondary">
                      <span className="font-bold">Your answer: </span>
                      <span>{resItem.learner_answer}</span>
                    </div>
                    {!resItem.correct && (
                      <div className="text-dark font-bold">
                        <span>Correct answer: </span>
                        <span>{resItem.correct_answer}</span>
                      </div>
                    )}
                    <div className="p-3 rounded-lg bg-surface border border-border-subtle text-xs text-content-secondary mt-2">
                      <span className="font-bold text-dark">Explanation: </span>
                      {resItem.explanation}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-center items-center pt-4 border-t border-border-subtle">
            <Button variant="primary" onClick={onReset} className="flex items-center gap-1.5 text-xs font-extrabold px-6">
              <span>More Questions</span>
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
