import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { Button } from '../components/Button';
import { Badge } from '../components/Badge';
import { Card } from '../components/Card';
import { ArrowRight, Check, Target, BookOpen, Loader2, Sparkles, User, Briefcase, Award } from 'lucide-react';

export function OnboardingPage() {
  const navigate = useNavigate();
  const { runFullPipeline, loadingState, errorState } = useApp();

  const [step, setStep] = useState(1);
  const [userName, setUserName] = useState('Demo Learner');
  const [targetRole, setTargetRole] = useState('AI/ML Engineer');
  const [selectedSkills, setSelectedSkills] = useState(['Python', 'SQL']);
  const [degree, setDegree] = useState('B.S. Computer Science');
  const [fieldOfStudy, setFieldOfStudy] = useState('Computer Science');
  const [institution, setInstitution] = useState('Tech University');
  const [experienceLevel, setExperienceLevel] = useState('Entry-Level');
  const [careerGoal, setCareerGoal] = useState('Master deep learning and deploy ML models in production');

  const supportedRoles = [
    'AI/ML Engineer',
    'Backend Developer',
    'Frontend Developer',
    'Data Scientist',
  ];

  const popularSkills = [
    'Python',
    'JavaScript',
    'SQL',
    'React',
    'Machine Learning',
    'Statistics',
    'PyTorch',
    'FastAPI',
    'Git',
  ];

  const toggleSkill = (skill) => {
    setSelectedSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  const handleCompleteOnboarding = async () => {
    const payload = {
      user_id: 'demo_user_1',
      name: userName,
      target_role: targetRole,
      career_goal: careerGoal,
      experience_level: experienceLevel,
      education: [
        {
          degree: degree,
          field_of_study: fieldOfStudy,
          institution: institution,
          graduation_year: 2026,
        },
      ],
      technical_skills: selectedSkills.map((s) => ({
        name: s,
        proficiency: s === 'Python' ? 'Advanced' : 'Intermediate',
        confidence: s === 'Python' ? 0.9 : 0.6,
        evidence: [
          {
            source_type: 'project',
            source_id: 'proj_1',
            description: `Built hands-on ${s} project`,
          },
        ],
      })),
      projects: [
        {
          title: `${targetRole} Project`,
          description: `Built hands-on application using ${selectedSkills.slice(0, 2).join(', ')}`,
          technologies_used: selectedSkills.slice(0, 2),
        },
      ],
    };

    try {
      await runFullPipeline(payload);
      navigate('/dashboard');
    } catch (err) {
      console.error('Onboarding failed:', err);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10 space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <Badge variant="orange" className="px-3 py-1 text-xs">
          Start Your AI Journey
        </Badge>
        <h1 className="text-3xl font-extrabold text-dark tracking-tight">
          Let's build your personalized path.
        </h1>
        <p className="text-sm text-content-secondary">
          Step {step} of 3 • Tell EduPath about your background and target career.
        </p>
      </div>

      {/* Error Alert */}
      {errorState && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs font-bold">
          {errorState}
        </div>
      )}

      {/* Loading Overlay State */}
      {loadingState ? (
        <Card className="p-12 text-center space-y-4 bg-surface border-border-subtle shadow-card">
          <Loader2 className="w-10 h-10 mx-auto text-orange-text animate-spin" />
          <h3 className="text-xl font-extrabold text-dark">{loadingState}</h3>
          <p className="text-xs text-content-secondary max-w-md mx-auto">
            EduPath's agent engine is analyzing your background and generating your milestone roadmap.
          </p>
        </Card>
      ) : (
        <Card className="p-6 md:p-8 bg-surface border-border-subtle shadow-card space-y-6">
          {/* Step 1: Background & Target Role */}
          {step === 1 && (
            <div className="space-y-6">
              <div className="border-b border-border-subtle pb-3">
                <h3 className="text-lg font-bold text-dark flex items-center gap-2">
                  <User className="w-5 h-5 text-orange-text" />
                  <span>Tell us about yourself</span>
                </h3>
                <p className="text-xs text-content-secondary mt-1">
                  What is your name and current background?
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-dark mb-1">Your Name</label>
                  <input
                    type="text"
                    value={userName}
                    onChange={(e) => setUserName(e.target.value)}
                    className="w-full p-3 rounded-md border border-border-subtle text-xs bg-canvas text-dark focus:outline-none focus:border-dark"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-dark mb-1">Degree / Diploma</label>
                    <input
                      type="text"
                      value={degree}
                      onChange={(e) => setDegree(e.target.value)}
                      className="w-full p-3 rounded-md border border-border-subtle text-xs bg-canvas text-dark focus:outline-none focus:border-dark"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-dark mb-1">Field of Study</label>
                    <input
                      type="text"
                      value={fieldOfStudy}
                      onChange={(e) => setFieldOfStudy(e.target.value)}
                      className="w-full p-3 rounded-md border border-border-subtle text-xs bg-canvas text-dark focus:outline-none focus:border-dark"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-dark mb-1">Institution</label>
                  <input
                    type="text"
                    value={institution}
                    onChange={(e) => setInstitution(e.target.value)}
                    className="w-full p-3 rounded-md border border-border-subtle text-xs bg-canvas text-dark focus:outline-none focus:border-dark"
                  />
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <Button variant="primary" onClick={() => setStep(2)} className="flex items-center gap-1.5 text-xs">
                  <span>Next: Choose Target Role</span>
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 2: Target Role */}
          {step === 2 && (
            <div className="space-y-6">
              <div className="border-b border-border-subtle pb-3">
                <h3 className="text-lg font-bold text-dark flex items-center gap-2">
                  <Target className="w-5 h-5 text-orange-text" />
                  <span>What role are you aiming for?</span>
                </h3>
                <p className="text-xs text-content-secondary mt-1">
                  Select your target career role to load benchmark skill requirements.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {supportedRoles.map((role) => {
                  const isSelected = targetRole === role;
                  return (
                    <button
                      key={role}
                      onClick={() => setTargetRole(role)}
                      className={`p-4 rounded-lg text-left border transition-all flex items-center justify-between ${
                        isSelected
                          ? 'bg-dark text-white border-dark font-extrabold shadow-sm'
                          : 'bg-canvas text-content-secondary border-border-subtle hover:border-dark/30'
                      }`}
                    >
                      <span className="text-sm">{role}</span>
                      {isSelected && <Check className="w-4 h-4 text-orange-text" />}
                    </button>
                  );
                })}
              </div>

              <div>
                <label className="block text-xs font-bold text-dark mb-1">Specific Career Goal</label>
                <input
                  type="text"
                  value={careerGoal}
                  onChange={(e) => setCareerGoal(e.target.value)}
                  className="w-full p-3 rounded-md border border-border-subtle text-xs bg-canvas text-dark focus:outline-none focus:border-dark"
                />
              </div>

              <div className="flex justify-between pt-4">
                <Button variant="secondary" onClick={() => setStep(1)} className="text-xs">
                  Back
                </Button>
                <Button variant="primary" onClick={() => setStep(3)} className="flex items-center gap-1.5 text-xs">
                  <span>Next: Select Skills</span>
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Current Skills */}
          {step === 3 && (
            <div className="space-y-6">
              <div className="border-b border-border-subtle pb-3">
                <h3 className="text-lg font-bold text-dark flex items-center gap-2">
                  <Award className="w-5 h-5 text-orange-text" />
                  <span>What are you currently learning?</span>
                </h3>
                <p className="text-xs text-content-secondary mt-1">
                  Select skills you have already practiced or acquired.
                </p>
              </div>

              <div className="flex flex-wrap gap-2">
                {popularSkills.map((skill) => {
                  const isSelected = selectedSkills.includes(skill);
                  return (
                    <button
                      key={skill}
                      onClick={() => toggleSkill(skill)}
                      className={`px-3.5 py-2 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 border ${
                        isSelected
                          ? 'bg-dark text-white border-dark'
                          : 'bg-canvas text-content-secondary border-border-subtle hover:border-dark/30'
                      }`}
                    >
                      <span>{skill}</span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-orange-text" />}
                    </button>
                  );
                })}
              </div>

              <div className="p-4 rounded-lg bg-canvas border border-border-subtle space-y-2">
                <div className="text-xs font-bold text-dark">Summary of Selection:</div>
                <div className="text-xs text-content-secondary">
                  Target Role: <strong className="text-dark">{targetRole}</strong>
                </div>
                <div className="text-xs text-content-secondary">
                  Current Skills ({selectedSkills.length}): <strong className="text-dark">{selectedSkills.join(', ') || 'None selected'}</strong>
                </div>
              </div>

              <div className="flex justify-between pt-4">
                <Button variant="secondary" onClick={() => setStep(2)} className="text-xs">
                  Back
                </Button>
                <Button variant="primary" onClick={handleCompleteOnboarding} className="flex items-center gap-1.5 text-xs font-extrabold">
                  <Sparkles className="w-4 h-4" />
                  <span>Analyze Profile & Generate Path</span>
                </Button>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
