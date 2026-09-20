import React from 'react';
import { motion } from 'framer-motion';
import { Target, BrainCircuit, GitCompare, Route, TrendingUp, ChevronRight } from 'lucide-react';

export function HowItWorks() {
  const steps = [
    {
      number: '01',
      title: 'Tell Us Where You Want to Go',
      description: 'Share your career goal, skills, education, projects, and experience.',
      icon: Target,
    },
    {
      number: '02',
      title: 'We Understand Your Skills',
      description: 'EduPath looks at what you already know and the work you have done.',
      icon: BrainCircuit,
    },
    {
      number: '03',
      title: 'See What You Need to Learn',
      description: 'See which skills you already have and which ones you need to build.',
      icon: GitCompare,
    },
    {
      number: '04',
      title: 'Get Your Personal Learning Path',
      description: 'Get a simple path that shows what to learn, practice, and do next.',
      icon: Route,
    },
    {
      number: '05',
      title: 'Learn, Practice & Keep Improving',
      description: 'Learn, practice, track your progress, and get a learning path that changes as you improve.',
      icon: TrendingUp,
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.12,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 15 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4, ease: 'easeOut' },
    },
  };

  return (
    <section id="how-it-works" className="py-12 bg-canvas">
      <div className="space-y-8">
        {/* Section Title & Supporting Text */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-3xl font-extrabold text-dark tracking-tight">
            How EduPath Works
          </h2>
          <p className="text-sm text-content-secondary font-medium leading-relaxed">
            From your career goal to your next learning step, EduPath helps you understand where you are and what to do next.
          </p>
        </div>

        {/* 5-Card Horizontal Row (Desktop: 1 Row, Mobile: Stack) */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-5 gap-4 relative items-stretch"
        >
          {steps.map((step, idx) => {
            const IconComponent = step.icon;
            return (
              <div key={step.number} className="flex flex-col relative group">
                <motion.div
                  variants={cardVariants}
                  className="h-full p-5 rounded-2xl border border-border-subtle bg-surface shadow-card hover:border-orange hover:shadow-subtle transition-all flex flex-col justify-between space-y-4"
                >
                  {/* Top Step Number & Icon */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-extrabold text-orange font-mono">
                        {step.number}
                      </span>
                      <div className="w-9 h-9 rounded-xl bg-orange-light text-orange flex items-center justify-center font-bold">
                        <IconComponent className="w-5 h-5" />
                      </div>
                    </div>

                    {/* Step Title */}
                    <h3 className="text-base font-extrabold text-dark tracking-tight leading-snug">
                      {step.title}
                    </h3>
                  </div>

                  {/* Step Description */}
                  <p className="text-xs text-content-secondary leading-relaxed font-medium pt-1">
                    {step.description}
                  </p>
                </motion.div>

                {/* Subtle Desktop Connector Arrow */}
                {idx < steps.length - 1 && (
                  <div className="hidden md:flex absolute -right-3.5 top-1/2 -translate-y-1/2 z-10 w-7 h-7 rounded-full bg-surface border border-border-subtle items-center justify-center text-orange shadow-subtle">
                    <ChevronRight className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}
        </motion.div>
      </div>
    </section>
  );
}
