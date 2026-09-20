export const APP_CONFIG = {
  name: 'EduPath',
  tagline: 'Your AI-powered adaptive career learning companion.',
  hackathon: 'Agentic AI Hackathon 2026',
  organizer: 'Product Space',
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  version: '0.1.0',
};

export const CORE_LOOP_STEPS = [
  { id: 'understand', name: 'UNDERSTAND', desc: 'Profile & Background Extraction' },
  { id: 'analyze', name: 'ANALYZE', desc: 'Market Skill-Gap Assessment' },
  { id: 'plan', name: 'PLAN', desc: 'Personalized Roadmap Synthesis' },
  { id: 'act', name: 'ACT', desc: 'Targeted Resources & Exercises' },
  { id: 'measure', name: 'MEASURE', desc: 'Performance & Mastery Grading' },
  { id: 'adapt', name: 'ADAPT', desc: 'Dynamic Roadmap Recalibration' },
  { id: 'repeat', name: 'REPEAT', desc: 'Continuous Career Progression' },
];
