import React from 'react';
import { Card } from './Card';
import { Badge } from './Badge';
import { ADAPTIVE_STORY_DEMO } from '../constants/demoData';
import { Sparkles, CheckCircle2, TrendingUp } from 'lucide-react';

export function AdaptiveStory() {
  return (
    <section className="py-12 space-y-8">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="text-xs font-mono uppercase tracking-wider text-orange-text font-extrabold">
          Autonomous Adaptation Engine
        </span>
        <h2 className="text-3xl font-extrabold text-dark tracking-tight">
          Your learning plan learns with you.
        </h2>
        <p className="text-sm text-content-secondary font-medium">
          Watch how EduPath dynamically adjusts learning sequences when persistent weaknesses are detected.
        </p>
      </div>

      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        {/* BEFORE CARD */}
        <Card className="md:col-span-4 p-6 bg-surface border-border-subtle shadow-card space-y-4 relative">
          <Badge variant="orange">1. INITIAL STATE</Badge>
          <div className="space-y-1">
            <h3 className="text-base font-extrabold text-dark">{ADAPTIVE_STORY_DEMO.before.topic}</h3>
            <div className="text-xs text-content-secondary font-medium">Initial Assessment Performance</div>
          </div>
          <div className="space-y-2 pt-1">
            <div className="flex items-center justify-between text-xs font-bold">
              <span className="text-content-secondary">Mastery Level</span>
              <span className="text-orange font-extrabold">{ADAPTIVE_STORY_DEMO.before.mastery}%</span>
            </div>
            <div className="flex items-center justify-between text-xs font-bold">
              <span className="text-content-secondary">Assessment Score</span>
              <span className="text-orange font-extrabold">{ADAPTIVE_STORY_DEMO.before.assessmentScore}%</span>
            </div>
          </div>
        </Card>

        {/* AGENT INTERVENTION (Sky Blue #87CEEB) */}
        <div className="md:col-span-4 text-center">
          <Card className="p-5 bg-skyblue text-dark border-skyblue-border shadow-floating space-y-3 relative">
            <div className="flex items-center justify-center gap-1.5 text-xs font-extrabold uppercase tracking-wider">
              <Sparkles className="w-4 h-4 text-dark" />
              <span>AGENT INTERVENTION</span>
            </div>
            <p className="text-xs leading-relaxed font-bold">
              "{ADAPTIVE_STORY_DEMO.agentDecision.action}"
            </p>
            <div className="pt-2 border-t border-dark/15 text-[10px] font-mono font-extrabold">
              AdaptationAgent Decision #409
            </div>
          </Card>
        </div>

        {/* AFTER CARD */}
        <Card className="md:col-span-4 p-6 bg-surface border-border-subtle shadow-card space-y-4 relative border-l-4 border-l-sage">
          <Badge variant="sage">2. RECALIBRATED STATE</Badge>
          <div className="space-y-1">
            <h3 className="text-base font-extrabold text-dark">{ADAPTIVE_STORY_DEMO.after.topic}</h3>
            <div className="text-xs text-content-secondary font-medium">Post-Prerequisite Performance</div>
          </div>
          <div className="space-y-2 pt-1">
            <div className="flex items-center justify-between text-xs font-bold">
              <span className="text-content-secondary">Mastery Level</span>
              <span className="text-sage font-extrabold flex items-center gap-1">
                {ADAPTIVE_STORY_DEMO.after.mastery}% <TrendingUp className="w-3.5 h-3.5" />
              </span>
            </div>
            <div className="flex items-center justify-between text-xs font-bold">
              <span className="text-content-secondary">Assessment Score</span>
              <span className="text-sage font-extrabold flex items-center gap-1">
                {ADAPTIVE_STORY_DEMO.after.assessmentScore}% <CheckCircle2 className="w-3.5 h-3.5" />
              </span>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
}
