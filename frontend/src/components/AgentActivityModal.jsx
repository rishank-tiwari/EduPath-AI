import React from 'react';
import { useApp } from '../context/AppContext';
import { Bot, CheckCircle, Terminal, X, Zap, Cpu, Sparkles } from 'lucide-react';
import { Button } from './Button';

export function AgentActivityModal() {
  const { isAgentModalOpen, toggleAgentModal } = useApp();

  if (!isAgentModalOpen) return null;

  const agents = [
    {
      name: 'Profile Agent',
      phase: 'UNDERSTAND',
      status: 'Active',
      description: 'Normalized background, extracted project evidence, and calculated confidence scores.',
      lastTrace: 'Confidence calculated: Python (0.90), ML (0.65)',
    },
    {
      name: 'Skill Gap Agent',
      phase: 'GAP ANALYSIS',
      status: 'Active',
      description: 'Mapped current candidate capabilities against target benchmark role (AI/ML Engineer).',
      lastTrace: 'Identified 3 target deficits: Model Evaluation, MLOps, Statistics',
    },
    {
      name: 'Learning Planner',
      phase: 'PLAN',
      status: 'Active',
      description: 'Structured adaptive weekly modules ordered by prerequisite dependencies.',
      lastTrace: 'Generated 5 module roadmap: Linear Regression -> Neural Networks -> MLOps',
    },
    {
      name: 'Assessment Agent',
      phase: 'EVALUATE',
      status: 'Active',
      description: 'Evaluated practice answers and assigned 85% score on Linear Regression.',
      lastTrace: 'Identified weak area: Loss function derivative calculation',
    },
    {
      name: 'Adaptation Agent',
      phase: 'RECALIBRATE',
      status: 'Active',
      description: 'Triggered path recalibration to reinforce probability fundamentals.',
      lastTrace: 'Injected 15-min prerequisite module: Probability & Statistics Basics',
    },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-dark/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-3xl bg-surface border border-border-subtle rounded-2xl shadow-floating overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="bg-dark text-canvas p-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-orange text-dark flex items-center justify-center font-bold">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-extrabold text-base text-canvas">How EduPath Decided</h3>
                <span className="text-[10px] px-2 py-0.5 rounded bg-skyblue text-dark font-mono font-extrabold">
                  MULTI-AGENT ENGINE
                </span>
              </div>
              <p className="text-xs text-canvas/70 font-medium">
                Autonomous agentic workflow running behind the learner interface
              </p>
            </div>
          </div>

          <button
            onClick={toggleAgentModal}
            className="p-2 rounded-lg text-canvas/70 hover:text-canvas hover:bg-surface-dark transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 bg-canvas text-dark">
          <div className="bg-orange-light border border-orange-border rounded-xl p-4 flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-orange shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <p className="font-extrabold text-dark">Agentic Intelligence Explanation</p>
              <p className="text-content-secondary leading-relaxed">
                EduPath continuously coordinates 5 specialized AI agents to analyze your background, quantify skill deficits, plan weekly goals, evaluate quizzes, and adapt your learning plan dynamically.
              </p>
            </div>
          </div>

          {/* Agent Pipeline Cards */}
          <div className="space-y-3">
            <h4 className="text-xs font-extrabold tracking-wider uppercase text-content-muted">
              Active Agent Pipeline
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {agents.map((agent, idx) => (
                <div
                  key={idx}
                  className="bg-surface border border-border-subtle rounded-xl p-4 space-y-2 hover:border-orange transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-sm text-dark">{agent.name}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-soft text-content-secondary">
                      {agent.phase}
                    </span>
                  </div>

                  <p className="text-xs text-content-secondary leading-normal">{agent.description}</p>

                  <div className="pt-2 border-t border-border-subtle flex items-center gap-1.5 text-[11px] text-skyblue-text font-mono">
                    <CheckCircle className="w-3.5 h-3.5 shrink-0 text-sage" />
                    <span className="truncate">{agent.lastTrace}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Live Trace Stream Preview */}
          <div className="bg-dark text-canvas rounded-xl p-4 font-mono text-xs space-y-2">
            <div className="flex items-center justify-between text-[11px] text-canvas/60 border-b border-canvas/15 pb-2">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-skyblue" />
                <span>Orchestrator Trace Stream</span>
              </div>
              <span>Execution ID: tr_edupath_98124</span>
            </div>

            <div className="space-y-1.5 pt-1 text-[11px] leading-relaxed">
              <p className="text-skyblue">[09:24:10] ProfileAgent -&gt; Skills normalized (3 evidence sources linked)</p>
              <p className="text-orange">[09:24:11] SkillGapAgent -&gt; Benchmark comparison: 3 missing competencies</p>
              <p className="text-canvas/90">[09:24:12] LearningPlanner -&gt; Roadmapping: 5 modules configured</p>
              <p className="text-sage">[09:24:13] AdaptationAgent -&gt; Recalibrated roadmap after score delta</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-surface border-t border-border-subtle flex justify-end">
          <Button variant="primary" size="sm" onClick={toggleAgentModal}>
            Got It
          </Button>
        </div>
      </div>
    </div>
  );
}
