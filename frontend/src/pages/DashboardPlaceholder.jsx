import React, { useState } from 'react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { Badge } from '../components/Badge';
import { ProgressBar } from '../components/ProgressBar';
import { SectionHeader } from '../components/SectionHeader';
import { Input } from '../components/Input';
import { useHealthCheck } from '../hooks/useHealthCheck';
import { profileService } from '../services/profileService';
import {
  Brain,
  Target,
  BookOpen,
  Award,
  RefreshCw,
  Server,
  Database,
  Flame,
  CheckCircle2,
  Clock,
  Zap,
  TrendingUp,
  Bot,
  User,
  Sparkles,
  ShieldCheck,
  Code2,
} from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip } from 'recharts';

export function DashboardPlaceholder() {
  const { health, loading, refetch } = useHealthCheck();

  // Profile Agent state
  const [profileLoading, setProfileLoading] = useState(false);
  const [targetRole, setTargetRole] = useState('AI/ML Engineer');
  const [careerGoal, setCareerGoal] = useState('Build production agentic systems');
  const [declaredSkills, setDeclaredSkills] = useState('Python, PyTorch, FastAPI, MongoDB');
  const [projectTitle, setProjectTitle] = useState('EduPath Learning Platform');
  const [projectTech, setProjectTech] = useState('Python, FastAPI, React');
  const [analyzedProfile, setAnalyzedProfile] = useState(null);
  const [analysisError, setAnalysisError] = useState(null);

  const handleRunProfileAgent = async (e) => {
    e.preventDefault();
    setProfileLoading(true);
    setAnalysisError(null);

    const payload = {
      user_id: 'demo_user_1',
      target_role: targetRole,
      career_goal: careerGoal,
      declared_skills: declaredSkills.split(',').map((s) => s.trim()).filter(Boolean),
      declared_projects: [
        {
          project_id: 'proj_demo_1',
          title: projectTitle,
          description: 'Production agentic learning workspace',
          technologies_used: projectTech.split(',').map((t) => t.trim()).filter(Boolean),
        },
      ],
    };

    try {
      const data = await profileService.analyzeProfile(payload);
      setAnalyzedProfile(data);
    } catch (err) {
      setAnalysisError(err.message || 'Profile analysis failed.');
    } finally {
      setProfileLoading(false);
    }
  };

  const mockProgressData = [
    { day: 'Mon', score: 62 },
    { day: 'Tue', score: 68 },
    { day: 'Wed', score: 74 },
    { day: 'Thu', score: 71 },
    { day: 'Fri', score: 82 },
    { day: 'Sat', score: 85 },
    { day: 'Sun', score: 88 },
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Top Workspace Header */}
      <SectionHeader
        title="AI Career Intelligence Workspace"
        subtitle="Phase 1 Task 1.1 • Profile Agent & Learner Intelligence Foundation"
        action={
          <Button size="sm" variant="secondary" onClick={refetch} className="gap-1.5">
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh Workspace</span>
          </Button>
        }
      />

      {/* Row 1: Profile Agent Interactive Intelligence Box */}
      <Card className="p-6 bg-surface border-border-subtle shadow-card space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-border-subtle">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-lg bg-orange text-dark flex items-center justify-center font-bold shadow-subtle">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-extrabold text-dark">Profile Agent (UNDERSTAND Phase)</h2>
                <Badge variant="blue" className="text-[10px]">
                  <Sparkles className="w-3 h-3 text-dark" /> Structured Pydantic Output
                </Badge>
              </div>
              <p className="text-xs text-content-secondary mt-0.5">
                Normalizes skills, associates project evidence, and computes evidence-backed confidence scores.
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Form Inputs */}
          <form onSubmit={handleRunProfileAgent} className="lg:col-span-5 space-y-4">
            <Input
              label="Target Role"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. AI/ML Engineer"
              required
            />
            <Input
              label="Career Goal"
              value={careerGoal}
              onChange={(e) => setCareerGoal(e.target.value)}
              placeholder="e.g. Build production LLM systems"
              required
            />
            <Input
              label="Declared Skills (comma separated)"
              value={declaredSkills}
              onChange={(e) => setDeclaredSkills(e.target.value)}
              placeholder="Python, PyTorch, FastAPI"
            />
            <div className="grid grid-cols-2 gap-2">
              <Input
                label="Sample Project Title"
                value={projectTitle}
                onChange={(e) => setProjectTitle(e.target.value)}
              />
              <Input
                label="Project Technologies"
                value={projectTech}
                onChange={(e) => setProjectTech(e.target.value)}
              />
            </div>

            <Button type="submit" variant="primary" size="md" className="w-full gap-2 font-extrabold" disabled={profileLoading}>
              <RefreshCw className={`w-4 h-4 ${profileLoading ? 'animate-spin' : ''}`} />
              <span>{profileLoading ? 'Running Profile Agent...' : 'Analyze & Build Profile'}</span>
            </Button>
            {analysisError && <p className="text-xs text-orange font-bold">{analysisError}</p>}
          </form>

          {/* Agent Analysis Output View */}
          <div className="lg:col-span-7 bg-canvas p-5 rounded-md border border-border-subtle space-y-4 font-sans text-xs">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle font-bold">
              <span className="flex items-center gap-1.5 text-dark">
                <ShieldCheck className="w-4 h-4 text-orange" /> Analyzed Learner Profile
              </span>
              <Badge variant={analyzedProfile ? 'sage' : 'neutral'}>
                {analyzedProfile ? `Completeness: ${analyzedProfile.profile_completeness}%` : 'Awaiting Analysis'}
              </Badge>
            </div>

            {analyzedProfile ? (
              <div className="space-y-4">
                <div className="p-3 rounded-md bg-surface border border-border-subtle space-y-1">
                  <div className="font-extrabold text-dark flex items-center justify-between">
                    <span>Summary ({analyzedProfile.experience_level})</span>
                    <Badge variant="blue">{analyzedProfile.target_role}</Badge>
                  </div>
                  <p className="text-content-secondary font-normal">{analyzedProfile.profile_summary}</p>
                </div>

                <div className="space-y-2">
                  <div className="font-extrabold text-dark flex items-center justify-between">
                    <span>Evidence-Backed Technical Skills</span>
                    <span className="text-[10px] text-content-muted font-mono font-bold">CONFIDENCE</span>
                  </div>
                  <div className="space-y-2">
                    {analyzedProfile.technical_skills.map((skill, idx) => (
                      <div key={idx} className="p-3 rounded-md bg-surface border border-border-subtle space-y-1.5">
                        <div className="flex items-center justify-between font-bold">
                          <span className="text-dark">{skill.name}</span>
                          <span className="font-mono text-orange font-extrabold">{Math.round(skill.confidence * 100)}%</span>
                        </div>
                        <ProgressBar value={skill.confidence * 100} variant="orange" showValue={false} />
                        {skill.evidence && skill.evidence.length > 0 && (
                          <div className="text-[10px] text-content-secondary pt-1 flex items-center gap-1 font-medium">
                            <Code2 className="w-3 h-3 text-skyblue-text" />
                            <span>Evidence: {skill.evidence[0].description}</span>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-12 text-center text-content-muted space-y-2">
                <Bot className="w-8 h-8 text-skyblue-text mx-auto" />
                <p className="font-medium">Submit form to trigger Profile Agent structured analysis &amp; MongoDB storage.</p>
              </div>
            )}
          </div>
        </div>
      </Card>

      {/* Row 2: Key Metrics (Career Readiness, Learning Streak, System Telemetry) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Card hoverEffect className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-extrabold uppercase text-content-muted">Career Readiness</span>
            <Badge variant="orange">+12% this week</Badge>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-extrabold text-dark tracking-tight">
              {analyzedProfile ? `${Math.round(analyzedProfile.profile_completeness)}%` : '85%'}
            </span>
            <span className="text-xs text-content-secondary font-bold">Target: {targetRole}</span>
          </div>
          <ProgressBar value={analyzedProfile ? analyzedProfile.profile_completeness : 85} variant="orange" label="Target Alignment Score" />
        </Card>

        <Card hoverEffect className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-extrabold uppercase text-content-muted">Learning Streak</span>
            <div className="flex items-center gap-1 text-orange font-extrabold text-xs">
              <Flame className="w-4 h-4 fill-orange text-orange" />
              <span>Active</span>
            </div>
          </div>
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-extrabold text-dark tracking-tight">14</span>
            <span className="text-xs text-content-secondary font-bold">Consecutive Days</span>
          </div>
          <div className="text-xs text-content-muted flex items-center gap-1.5 font-bold">
            <Clock className="w-3.5 h-3.5 text-content-secondary" />
            <span>Last task completed 2 hours ago</span>
          </div>
        </Card>

        <Card hoverEffect className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-extrabold uppercase text-content-muted">System Telemetry</span>
            <Badge variant={health?.status === 'ok' ? 'sage' : 'orange'}>
              {health?.status === 'ok' ? 'Operational' : 'Connecting'}
            </Badge>
          </div>
          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between py-1 border-b border-border-subtle">
              <span className="text-content-secondary flex items-center gap-1.5 font-bold">
                <Server className="w-3.5 h-3.5 text-orange" /> FastAPI Backend
              </span>
              <span className="font-mono font-extrabold text-dark">GET /api/v1/health</span>
            </div>
            <div className="flex items-center justify-between py-1">
              <span className="text-content-secondary flex items-center gap-1.5 font-bold">
                <Database className="w-3.5 h-3.5 text-skyblue-text" /> MongoDB Collection
              </span>
              <span className="font-mono font-extrabold text-content-secondary">learner_profiles</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
