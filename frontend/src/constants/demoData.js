export const SUGGESTED_ROLES = [
  'AI/ML Engineer',
  'Software Engineer',
  'Data Scientist',
  'Full-Stack Developer',
  'Data Analyst',
  'MLOps Engineer',
];

export const PRODUCT_CAPABILITY_METRICS = [
  {
    number: '01',
    title: 'Skill Intelligence',
    description: 'Deep resume parsing and real-time market demand gap quantification.',
  },
  {
    number: '02',
    title: 'Adaptive Learning',
    description: 'Dynamic roadmaps that auto-adjust when persistent weaknesses are detected.',
  },
  {
    number: '03',
    title: 'Evidence-Based Progress',
    description: 'Practical task evaluation rubrics instead of superficial multiple-choice quizzes.',
  },
  {
    number: '04',
    title: 'AI-Guided Practice',
    description: 'Context-aware coding challenges and project exercises tailored to your current gaps.',
  },
];

export const FEATURED_LEARNING_PATHS = [
  {
    id: 'aiml',
    role: 'AI/ML Engineer',
    duration: '12 Week Adaptive Path',
    readiness: 58,
    gaps: [
      { name: 'Statistics & Probability', priority: 'High' },
      { name: 'Deep Learning & Autograd', priority: 'Medium' },
      { name: 'MLOps Pipeline Deployment', priority: 'High' },
    ],
    nextStep: 'Practice Probability Distributions',
  },
  {
    id: 'swe',
    role: 'Software Engineer',
    duration: '10 Week Adaptive Path',
    readiness: 72,
    gaps: [
      { name: 'Distributed System Design', priority: 'High' },
      { name: 'Advanced DSA & Graph Algos', priority: 'Medium' },
      { name: 'Async Backend Architecture', priority: 'Low' },
    ],
    nextStep: 'Complete System Design Challenge',
  },
  {
    id: 'ds',
    role: 'Data Scientist',
    duration: '14 Week Adaptive Path',
    readiness: 64,
    gaps: [
      { name: 'Applied Bayesian Statistics', priority: 'High' },
      { name: 'Complex SQL Query Tuning', priority: 'Medium' },
      { name: 'Feature Engineering & Pipelines', priority: 'Medium' },
    ],
    nextStep: 'Review SQL Window Functions',
  },
];

export const HOW_IT_WORKS_STEPS = [
  {
    step: '01',
    title: 'Understand You',
    subtitle: 'Resume + Skills + Experience',
    desc: 'Ingests your background, project portfolio, and career ambition into a unified learner profile.',
  },
  {
    step: '02',
    title: 'Find Your Gaps',
    subtitle: 'Market Demand Comparison',
    desc: 'Compares your current capabilities against real-time target role skill expectations.',
  },
  {
    step: '03',
    title: 'Build Your Path',
    subtitle: 'Personalized Adaptive Roadmap',
    desc: 'Synthesizes milestone-driven learning modules structured specifically to eliminate your gaps.',
  },
  {
    step: '04',
    title: 'Learn & Practice',
    subtitle: 'Curated Resources + Projects',
    desc: 'Delivers high-yield tutorials, hands-on coding challenges, and practical exercises.',
  },
  {
    step: '05',
    title: 'Adapt Automatically',
    subtitle: 'Closed-Loop Optimization',
    desc: 'Re-evaluates and recalibrates your upcoming roadmap based on task performance.',
  },
];

export const AGENT_ACTIVITY_LOG = [
  { status: 'done', text: 'Analyzed resume profile & career goals' },
  { status: 'done', text: 'Quantified 5 critical skill gaps against AI/ML Engineer benchmark' },
  { status: 'done', text: 'Synthesized 12-week personalized learning roadmap' },
  { status: 'done', text: 'Evaluated Assessment #2 (Autograd Functions)' },
  { status: 'warning', text: 'Detected persistent weakness in Probability Distributions (Score: 42%)' },
  { status: 'action', text: 'Added 30-min prerequisite practice module to Week 3' },
  { status: 'done', text: 'Updated roadmap trajectory & notified learner' },
];

export const SKILL_PROFILE_DEMO = {
  targetRole: 'AI/ML Engineer',
  currentReadiness: 58,
  skills: [
    { name: 'Python Programming', level: 78, type: 'current' },
    { name: 'Machine Learning Basics', level: 52, type: 'current' },
    { name: 'Deep Learning Architectures', level: 41, type: 'gap' },
    { name: 'Statistics & Probability', level: 34, type: 'gap' },
    { name: 'MLOps & Deployment', level: 18, type: 'gap' },
  ],
};

export const ADAPTIVE_STORY_DEMO = {
  before: {
    topic: 'Statistics & Probability',
    mastery: 34,
    assessmentScore: 42,
  },
  agentDecision: {
    observation: 'Repeated difficulty detected in conditional probability questions.',
    action: 'Revisit probability fundamentals before progressing to advanced ML modules.',
  },
  updatedPlan: [
    'Probability Revision (30 mins)',
    'Guided Practice Exercise',
    'Re-assessment Quiz',
  ],
  after: {
    topic: 'Statistics & Probability',
    mastery: 52,
    assessmentScore: 84,
  },
};

export const DEMO_LEARNER_STORIES = [
  {
    id: 1,
    title: 'Target: AI/ML Engineer',
    label: 'Demo Journey 01',
    beforeStats: 'Statistics — 34%',
    afterStats: 'Statistics — 52%',
    initialReadiness: 42,
    currentReadiness: 64,
    insight: 'EduPath detected repeated difficulty in Bayesian probability and dynamically inserted prerequisite exercises before advanced neural networks.',
  },
  {
    id: 2,
    title: 'Target: Software Engineer',
    label: 'Demo Journey 02',
    beforeStats: 'System Design — 28%',
    afterStats: 'System Design — 68%',
    initialReadiness: 55,
    currentReadiness: 81,
    insight: 'Agent identified weak trade-off reasoning in load balancing tasks, triggering targeted architecture scenario challenges.',
  },
];

export const AI_MENTOR_CONVERSATION = {
  learnerMsg: 'What should I learn today?',
  mentorReply:
    'Based on your recent assessment, focus on probability distributions today. You scored 45% on this topic, so I\'ve added a 30-minute guided practice session before your next ML module.',
  recommendedAction: 'Start 30-Min Guided Practice →',
};
