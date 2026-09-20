import React from 'react';
import { Card } from './Card';
import { Badge } from './Badge';
import { DEMO_LEARNER_STORIES } from '../constants/demoData';

export function ProgressStories() {
  return (
    <section className="py-12 space-y-8">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
          Learner Growth Trajectory
        </span>
        <h2 className="text-3xl font-extrabold text-dark tracking-tight">
          Progress worth celebrating.
        </h2>
        <p className="text-sm text-content-secondary font-medium">
          Sample journeys demonstrating how adaptive agent intervention accelerates skill mastery.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
        {DEMO_LEARNER_STORIES.map((story) => (
          <Card key={story.id} hoverEffect className="p-6 bg-surface border-border-subtle shadow-card space-y-4">
            <div className="flex items-center justify-between">
              <Badge variant="orange">{story.label}</Badge>
              <div className="text-xs font-extrabold text-dark">{story.title}</div>
            </div>

            <div className="grid grid-cols-2 gap-3 p-3 rounded-md bg-canvas border border-border-subtle text-xs">
              <div>
                <div className="text-content-muted font-mono font-bold text-[10px]">BEFORE INTERVENTION</div>
                <div className="font-bold text-content-secondary mt-0.5">{story.beforeStats}</div>
                <div className="text-[11px] text-content-muted font-bold">Readiness: {story.initialReadiness}%</div>
              </div>
              <div className="border-l border-border-subtle pl-3">
                <div className="text-sage font-mono text-[10px] font-extrabold">AFTER ADAPTATION</div>
                <div className="font-extrabold text-dark mt-0.5">{story.afterStats}</div>
                <div className="text-[11px] text-sage font-bold">Readiness: {story.currentReadiness}%</div>
              </div>
            </div>

            <p className="text-xs text-content-secondary italic leading-relaxed font-medium">
              "{story.insight}"
            </p>
          </Card>
        ))}
      </div>

      <div className="text-center">
        <span className="text-xs text-content-muted font-mono font-bold bg-surface-soft px-3 py-1 rounded-full border border-border-subtle">
          * Labeled Sample Demo Journeys
        </span>
      </div>
    </section>
  );
}
