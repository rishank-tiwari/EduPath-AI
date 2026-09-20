import React from 'react';
import { Card } from './Card';
import { Badge } from './Badge';
import { AGENT_ACTIVITY_LOG } from '../constants/demoData';
import { Bot, CheckCircle2, AlertTriangle, Zap, Terminal } from 'lucide-react';

export function AgentActivity() {
  return (
    <section className="py-12 space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Left Explanation Column */}
        <div className="lg:col-span-6 space-y-4">
          <Badge variant="blue" className="px-3 py-1">
            <Bot className="w-3.5 h-3.5 text-dark" />
            <span>Agentic AI Architecture</span>
          </Badge>

          <h2 className="text-3xl font-extrabold text-dark tracking-tight leading-tight">
            Not another chatbot. <br />
            <span className="text-orange">An AI agent that manages your journey.</span>
          </h2>

          <p className="text-sm text-content-secondary leading-relaxed font-medium">
            EduPath does not wait for you to ask standard Q&amp;A questions. It actively evaluates your submissions, detects persistent weak spots, injects prerequisite modules, and recalibrates your upcoming roadmap autonomously.
          </p>

          <div className="space-y-2.5 pt-2 text-xs text-content-secondary font-bold">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-orange" />
              <span>Goal-driven multi-agent orchestration under OrchestratorAgent</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-orange" />
              <span>Stateful memory tracking across practice &amp; assessment sessions</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-orange" />
              <span>Observable trace logs detailing agent decisions and tool usage</span>
            </div>
          </div>
        </div>

        {/* Right Dark Feature Section (#25252A) */}
        <div className="lg:col-span-6">
          <Card className="p-6 bg-dark text-canvas border-dark shadow-floating space-y-4 font-mono text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-canvas/15">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-skyblue" />
                <span className="font-bold text-canvas">EduPath Agent Activity Stream</span>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded bg-skyblue text-dark font-extrabold shadow-subtle">
                LIVE AGENT
              </span>
            </div>

            <div className="space-y-3">
              {AGENT_ACTIVITY_LOG.map((log, idx) => (
                <div key={idx} className="flex items-start gap-2.5 leading-snug">
                  {log.status === 'done' && <CheckCircle2 className="w-4 h-4 text-skyblue shrink-0 mt-0.5" />}
                  {log.status === 'warning' && <AlertTriangle className="w-4 h-4 text-orange shrink-0 mt-0.5" />}
                  {log.status === 'action' && <Zap className="w-4 h-4 text-orange shrink-0 mt-0.5" />}

                  <span className={log.status === 'warning' ? 'text-orange font-bold' : log.status === 'action' ? 'text-orange font-bold' : 'text-canvas/90'}>
                    {log.text}
                  </span>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-canvas/15 text-[10px] text-canvas/60 flex items-center justify-between">
              <span>Execution Trace: tr_894129481</span>
              <span>Status: Active Optimization</span>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
}
