import React from 'react';
import { Hero } from '../components/Hero';
import { HowItWorks } from '../components/HowItWorks';
import { AIMentorPreview } from '../components/AIMentorPreview';
import { MetricStrip } from '../components/MetricStrip';
import { SkillIntelligence } from '../components/SkillIntelligence';
import { AdaptiveStory } from '../components/AdaptiveStory';
import { CTASection } from '../components/CTASection';

export function LandingPage() {
  return (
    <div className="space-y-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* 01. Hero */}
      <Hero />

      {/* 02. How EduPath Works */}
      <HowItWorks />

      {/* 03. Context-Aware AI Mentor */}
      <AIMentorPreview />

      {/* 04. Product Capability Metrics */}
      <MetricStrip />

      {/* 05. Skill Intelligence Section */}
      <div id="skills">
        <SkillIntelligence />
      </div>

      {/* 06. Adaptive Learning Story */}
      <AdaptiveStory />

      {/* 07. Final Emotional CTA */}
      <CTASection />
    </div>
  );
}
