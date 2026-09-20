import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from './Card';
import { Badge } from './Badge';
import { Button } from './Button';
import { ProgressBar } from './ProgressBar';
import { FEATURED_LEARNING_PATHS } from '../constants/demoData';
import { ArrowRight, Clock, Sparkles } from 'lucide-react';

export function LearningPathPreview() {
  return (
    <section className="py-12 space-y-8">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
          Personalized Adaptive Roadmaps
        </span>
        <h2 className="text-3xl font-extrabold text-dark tracking-tight">
          Your path should adapt to you.
        </h2>
        <p className="text-sm text-content-secondary font-medium">
          EduPath turns skill gaps into a personalized learning journey.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {FEATURED_LEARNING_PATHS.map((path) => (
          <Card key={path.id} hoverEffect className="p-6 bg-surface border-border-subtle shadow-card flex flex-col justify-between space-y-5">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Badge variant="orange">{path.role}</Badge>
                <div className="flex items-center gap-1 text-[11px] text-content-muted font-mono font-bold">
                  <Clock className="w-3.5 h-3.5 text-content-muted" />
                  <span>{path.duration}</span>
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs font-bold">
                  <span className="text-content-secondary">Readiness Score</span>
                  <span className="text-dark font-extrabold">{path.readiness}%</span>
                </div>
                <ProgressBar value={path.readiness} variant="orange" showValue={false} />
              </div>

              <div className="space-y-2 pt-2">
                <div className="text-xs font-extrabold text-dark">Identified Skill Gaps</div>
                <div className="space-y-1.5">
                  {path.gaps.map((gap, i) => (
                    <div key={i} className="p-2.5 rounded bg-canvas border border-border-subtle text-xs flex items-center justify-between font-bold">
                      <span className="text-dark">{gap.name}</span>
                      <Badge variant={gap.priority === 'High' ? 'orange' : 'blue'} className="text-[10px]">
                        {gap.priority}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="pt-4 border-t border-border-subtle space-y-3">
              <div className="p-2.5 rounded-md bg-skyblue-light border border-skyblue-border text-xs">
                <div className="flex items-center gap-1 text-[10px] font-extrabold text-skyblue-text uppercase">
                  <Sparkles className="w-3 h-3 text-skyblue-text" /> AI Recommendation
                </div>
                <div className="font-extrabold text-dark mt-0.5">{path.nextStep}</div>
              </div>

              <Link to="/dashboard" className="block">
                <Button variant="secondary" size="sm" className="w-full justify-between">
                  <span>Explore This Path</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>

      <div className="text-center">
        <span className="text-xs text-content-muted font-mono font-bold bg-surface-soft px-3 py-1 rounded-full border border-border-subtle">
          * Demo Preview Data • Paths generated dynamically per learner profile
        </span>
      </div>
    </section>
  );
}
