import React from 'react';
import { Card } from './Card';
import { Badge } from './Badge';
import { ProgressBar } from './ProgressBar';
import { SKILL_PROFILE_DEMO } from '../constants/demoData';
import { Target, ArrowRight, Brain } from 'lucide-react';

export function SkillIntelligence() {
  return (
    <section className="py-12 space-y-8">
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <span className="text-xs font-mono uppercase tracking-wider text-skyblue-text font-extrabold">
          Skill Gap Quantification
        </span>
        <h2 className="text-3xl font-extrabold text-dark tracking-tight">
          Clear sight of where you stand and what is missing.
        </h2>
        <p className="text-sm text-content-secondary font-medium">
          Visual connection mapping current competencies directly against target role standards.
        </p>
      </div>

      <Card className="p-8 bg-surface border-border-subtle shadow-card max-w-4xl mx-auto space-y-6">
        {/* Connection Flow Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-md bg-canvas border border-border-subtle text-xs font-extrabold">
          <div className="flex items-center gap-2 text-dark">
            <Brain className="w-4 h-4 text-orange" />
            <span>CURRENT SKILLS</span>
          </div>
          <ArrowRight className="w-4 h-4 text-orange hidden sm:block" />
          <div className="flex items-center gap-2 text-skyblue-text">
            <Target className="w-4 h-4 text-skyblue-text" />
            <span>QUANTIFIED GAPS</span>
          </div>
          <ArrowRight className="w-4 h-4 text-skyblue-text hidden sm:block" />
          <div className="flex items-center gap-2">
            <Badge variant="orange">TARGET: {SKILL_PROFILE_DEMO.targetRole}</Badge>
          </div>
        </div>

        {/* Skill Progress Bar Stack */}
        <div className="space-y-4">
          {SKILL_PROFILE_DEMO.skills.map((skill) => (
            <div key={skill.name} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-dark">{skill.name}</span>
                <span className="font-mono text-content-secondary">{skill.level}%</span>
              </div>
              <ProgressBar
                value={skill.level}
                variant={skill.type === 'current' ? 'orange' : 'blue'}
                showValue={false}
              />
            </div>
          ))}
        </div>
      </Card>
    </section>
  );
}
