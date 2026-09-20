import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from './Card';
import { Badge } from './Badge';
import { Button } from './Button';
import { Bot, Sparkles, ArrowRight, CheckCircle2 } from 'lucide-react';

export function AIMentorPreview() {
  const navigate = useNavigate();

  return (
    <section id="mentor" className="py-12 space-y-8">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <Badge variant="blue" className="px-3 py-1 text-xs font-mono font-extrabold uppercase">
          <Sparkles className="w-3.5 h-3.5 text-dark" />
          <span>Context-Aware Mentorship</span>
        </Badge>
        <h2 className="text-3xl font-extrabold text-dark tracking-tight">
          Your AI Mentor knows where you are in your learning journey.
        </h2>
        <p className="text-xs text-content-secondary font-medium">
          It understands your goals, skill gaps, current task, and recent progress to provide tailored guidance.
        </p>
      </div>

      <Card className="p-6 md:p-8 bg-surface border-border-subtle shadow-card max-w-3xl mx-auto space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-border-subtle">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-skyblue text-dark flex items-center justify-center font-bold shadow-subtle">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <div className="text-sm font-extrabold text-dark">EduPath AI Mentor</div>
              <div className="text-[11px] text-skyblue-text font-mono font-bold">Journey Context Active</div>
            </div>
          </div>
          <Badge variant="orange" className="text-xs font-extrabold">
            Live Companion
          </Badge>
        </div>

        <div className="space-y-4">
          <p className="text-xs font-bold text-dark">Your AI Mentor can help you with:</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span className="font-semibold text-dark">Explaining difficult topics</span>
            </div>
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span className="font-semibold text-dark">Understanding why you're learning something</span>
            </div>
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span className="font-semibold text-dark">Giving practical code &amp; math examples</span>
            </div>
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span className="font-semibold text-dark">Suggesting what to learn next</span>
            </div>
            <div className="p-3 rounded-lg bg-canvas border border-border-subtle flex items-start gap-2 sm:col-span-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span className="font-semibold text-dark">Explaining why your learning path changed after practice</span>
            </div>
          </div>
        </div>

        <div className="pt-2 flex justify-center">
          <Button
            variant="primary"
            onClick={() => navigate('/mentor')}
            className="gap-2 font-extrabold text-xs px-6 py-2.5"
          >
            <span>Ask Your AI Mentor</span>
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </Card>
    </section>
  );
}
