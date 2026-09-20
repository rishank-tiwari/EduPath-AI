import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Button } from './Button';
import { Badge } from './Badge';
import { Card } from './Card';
import { ProgressBar } from './ProgressBar';
import { Sparkles, ArrowRight, BrainCircuit, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

export function Hero() {
  const navigate = useNavigate();
  const { isAuthenticated } = useApp();

  const handleBuildPath = () => {
    if (isAuthenticated) {
      navigate('/onboarding');
    } else {
      navigate('/login', { state: { from: '/onboarding' } });
    }
  };

  return (
    <section className="py-12 md:py-20">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Left Column: Headline & CTAs */}
        <div className="lg:col-span-7 space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <Badge variant="blue" className="px-3.5 py-1 text-xs font-extrabold shadow-subtle">
              <Sparkles className="w-3.5 h-3.5 text-dark" />
              <span>Agentic AI Hackathon 2026 • Product Space</span>
            </Badge>
          </motion.div>

          <motion.h1
            initial={{ opacity: 1, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="text-4xl sm:text-6xl font-extrabold text-dark tracking-tight leading-[1.1]"
          >
            Know where you want to go. <br />
            <span className="text-orange-text">We'll help you get there.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 1, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="text-base sm:text-lg text-content-secondary leading-relaxed max-w-xl font-medium"
          >
            EduPath analyzes your skills, identifies the gaps between where you are and your target career, then continuously adapts your learning path as you grow.
          </motion.p>

          <motion.div
            initial={{ opacity: 1, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="flex flex-wrap items-center gap-3 pt-2"
          >
            <Button size="lg" variant="primary" onClick={handleBuildPath} className="gap-2 font-extrabold">
              <span>Build My Learning Path</span>
              <ArrowRight className="w-4.5 h-4.5" />
            </Button>
            <a href="#how-it-works">
              <Button size="lg" variant="secondary" className="gap-2">
                <span>See How It Works</span>
              </Button>
            </a>
          </motion.div>
        </div>

        {/* Right Column: Light AI Intelligence Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-5"
        >
          <Card className="p-6 bg-surface border-border-subtle shadow-floating space-y-5 relative">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-md bg-skyblue text-dark flex items-center justify-center font-bold shadow-subtle">
                  <BrainCircuit className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-[10px] font-mono font-extrabold uppercase text-skyblue-text">AI CAREER INTELLIGENCE</div>
                  <div className="text-sm font-bold text-dark">Target Role: AI/ML Engineer</div>
                </div>
              </div>
              <Badge variant="orange">Active Agent</Badge>
            </div>

            {/* Career Readiness */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-content-secondary">Career Readiness</span>
                <span className="text-dark font-extrabold text-base">58%</span>
              </div>
              <ProgressBar value={58} variant="orange" showValue={false} />
            </div>

            {/* Top Skill Gaps List */}
            <div className="space-y-2.5 pt-1">
              <div className="text-xs font-extrabold text-dark flex items-center justify-between">
                <span>Top Skill Gaps</span>
                <span className="text-[10px] text-content-muted font-mono font-bold">PRIORITY</span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 rounded-md bg-canvas border border-border-subtle flex items-center justify-between font-bold">
                  <span className="text-dark">Statistics &amp; Probability</span>
                  <Badge variant="orange">HIGH</Badge>
                </div>
                <div className="p-3 rounded-md bg-canvas border border-border-subtle flex items-center justify-between font-bold">
                  <span className="text-dark">Deep Learning &amp; Autograd</span>
                  <Badge variant="blue">MEDIUM</Badge>
                </div>
                <div className="p-3 rounded-md bg-canvas border border-border-subtle flex items-center justify-between font-bold">
                  <span className="text-dark">MLOps &amp; Deployment</span>
                  <Badge variant="orange">HIGH</Badge>
                </div>
              </div>
            </div>

            {/* Next Recommended Step */}
            <div className="p-3.5 rounded-md bg-skyblue-light border border-skyblue-border space-y-1">
              <div className="text-[11px] font-extrabold text-skyblue-text flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-skyblue-text" />
                <span>Next Recommended Step</span>
              </div>
              <div className="text-xs font-extrabold text-dark">
                Practice Probability Distributions — 30 mins
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </section>
  );
}
