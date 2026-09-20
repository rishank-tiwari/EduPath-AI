import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { practiceService } from '../services/practiceService';
import { Button } from '../components/Button';
import { Card } from '../components/Card';
import { Badge } from '../components/Badge';
import { ArrowLeft, CheckCircle2, XCircle, Award, Calendar, BookOpen, Loader2 } from 'lucide-react';

export function PracticeResultPage() {
  const { practiceId } = useParams();
  const navigate = useNavigate();

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    async function fetchResult() {
      if (!practiceId) {
        if (isMounted) {
          setError("No result identifier provided.");
          setLoading(false);
        }
        return;
      }
      try {
        setLoading(true);
        setError(null);
        const data = await practiceService.getPracticeResult(practiceId);
        if (isMounted) {
          setResult(data);
        }
      } catch (err) {
        console.error("Failed to load practice result:", err);
        if (isMounted) {
          setError("We couldn't find this result. Please return to My Path and try again.");
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchResult();
    return () => {
      isMounted = false;
    };
  }, [practiceId]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <Card className="p-12 bg-surface border-border-subtle shadow-card text-center space-y-4">
          <Loader2 className="w-10 h-10 mx-auto text-orange-text animate-spin" />
          <h2 className="text-xl font-extrabold text-dark">Loading Stored Practice Result...</h2>
        </Card>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center space-y-4">
        <Card className="p-8 bg-surface border-border-subtle shadow-card space-y-4">
          <XCircle className="w-12 h-12 mx-auto text-red-500" />
          <h2 className="text-2xl font-extrabold text-dark">Result Not Found</h2>
          <p className="text-sm text-content-secondary max-w-md mx-auto">
            {error || "We couldn't find this result. Please return to My Path and try again."}
          </p>
          <Button variant="primary" onClick={() => navigate('/my-path')} className="text-xs font-bold gap-1.5">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to My Path</span>
          </Button>
        </Card>
      </div>
    );
  }

  const isPassed = result.percentage >= 60;
  const formattedDate = result.completed_at
    ? new Date(result.completed_at).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : null;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Navigation */}
      <div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => navigate('/my-path')}
          className="gap-1.5 text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to My Path</span>
        </Button>
      </div>

      {/* Main Summary Header Card */}
      <Card className="p-8 bg-surface border-border-subtle shadow-card space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Badge variant={isPassed ? 'orange' : 'neutral'} className="text-xs font-extrabold uppercase">
                {isPassed ? 'Passed' : 'Needs Review'}
              </Badge>
              <Badge variant="blue" className="text-xs font-bold">
                {result.skill_name}
              </Badge>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black text-dark tracking-tight mt-1">
              {result.topic || `${result.skill_name} Module Practice`}
            </h1>
            <p className="text-xs text-content-muted flex items-center gap-3 pt-1 font-mono">
              <span>Task ID: {result.task_id}</span>
              {formattedDate && (
                <span className="flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5" />
                  {formattedDate}
                </span>
              )}
            </p>
          </div>

          <div className="p-4 rounded-xl bg-canvas border border-border-subtle text-center shrink-0 min-w-[140px]">
            <div className="text-[11px] font-bold text-content-muted uppercase tracking-wider">Your Score</div>
            <div className="text-3xl font-black text-dark tracking-tight mt-0.5">{result.percentage}%</div>
            <div className="text-xs font-bold text-content-secondary mt-0.5">
              {result.score} / {result.total_questions} Correct
            </div>
          </div>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-lg bg-surface-soft border border-border-subtle">
            <div className="text-[10px] font-bold text-content-muted uppercase">Status</div>
            <div className="text-sm font-extrabold text-emerald-600 mt-1 flex items-center justify-center gap-1">
              <CheckCircle2 className="w-4 h-4" />
              Completed
            </div>
          </div>
          <div className="p-4 rounded-lg bg-surface-soft border border-border-subtle">
            <div className="text-[10px] font-bold text-content-muted uppercase">Total Questions</div>
            <div className="text-sm font-extrabold text-dark mt-1">{result.total_questions}</div>
          </div>
          <div className="p-4 rounded-lg bg-surface-soft border border-border-subtle">
            <div className="text-[10px] font-bold text-content-muted uppercase">Difficulty</div>
            <div className="text-sm font-extrabold text-dark capitalize mt-1">{result.difficulty}</div>
          </div>
          <div className="p-4 rounded-lg bg-surface-soft border border-border-subtle">
            <div className="text-[10px] font-bold text-content-muted uppercase">Practice ID</div>
            <div className="text-xs font-mono font-bold text-content-secondary mt-1 truncate">{result.practice_id}</div>
          </div>
        </div>
      </Card>

      {/* Question Results Breakdown */}
      <div className="space-y-4">
        <h2 className="text-lg font-extrabold text-dark tracking-tight">Question Breakdown</h2>

        {result.question_results && result.question_results.length > 0 ? (
          result.question_results.map((q, idx) => (
            <Card
              key={q.question_id || idx}
              className={`p-6 bg-surface border shadow-subtle space-y-3 ${
                q.correct ? 'border-emerald-200 bg-emerald-50/10' : 'border-red-200 bg-red-50/10'
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <span className="text-xs font-bold text-content-muted uppercase tracking-wider font-mono">
                  Question {idx + 1} of {result.total_questions}
                </span>
                <Badge variant={q.correct ? 'orange' : 'neutral'} className={q.correct ? 'bg-emerald-100 text-emerald-800 border-emerald-200 font-bold' : 'bg-red-100 text-red-800 border-red-200 font-bold'}>
                  {q.correct ? 'Correct ✓' : 'Incorrect ✗'}
                </Badge>
              </div>

              <p className="text-sm font-bold text-dark leading-relaxed">{q.question}</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                <div className="p-3 rounded-lg bg-canvas border border-border-subtle space-y-1">
                  <span className="font-bold text-content-muted block text-[10px] uppercase">Your Answer:</span>
                  <span className={`font-semibold ${q.correct ? 'text-emerald-700' : 'text-red-700'}`}>
                    {q.learner_answer || 'No answer provided'}
                  </span>
                </div>
                <div className="p-3 rounded-lg bg-canvas border border-border-subtle space-y-1">
                  <span className="font-bold text-content-muted block text-[10px] uppercase">Correct Answer:</span>
                  <span className="font-semibold text-emerald-700">{q.correct_answer}</span>
                </div>
              </div>

              {q.explanation && (
                <div className="p-3 rounded-lg bg-surface-soft border border-border-subtle text-xs space-y-1">
                  <span className="font-bold text-content-secondary block">Explanation:</span>
                  <p className="text-content-secondary leading-relaxed">{q.explanation}</p>
                </div>
              )}
            </Card>
          ))
        ) : (
          <Card className="p-6 text-center text-xs text-content-muted">
            Detailed question responses were not recorded for this session.
          </Card>
        )}
      </div>

      {/* Footer Action */}
      <div className="flex justify-center pt-4 pb-8">
        <Button variant="primary" onClick={() => navigate('/my-path')} className="text-xs font-extrabold gap-1.5 px-6">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to My Path</span>
        </Button>
      </div>
    </div>
  );
}
