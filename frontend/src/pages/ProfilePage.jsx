import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { Button } from '../components/Button';
import { User, Target, Upload, FileText, CheckCircle2, ShieldCheck, AlertCircle, Sparkles } from 'lucide-react';
import { documentService } from '../services/documentService';

export function ProfilePage() {
  const { userId, userProfile, setUserProfile, refreshAppState } = useApp();
  const [selectedFile, setSelectedFile] = useState(null);
  const [portfolioText, setPortfolioText] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [evidenceData, setEvidenceData] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const activeUserId = userId || userProfile?.user_id || 'demo_user_1';

  const user = userProfile || {
    user_id: activeUserId,
    target_role: 'AI/ML Engineer',
    career_goal: 'Build production LLM and agentic AI applications',
    experience_level: 'Entry-Level',
    education: [],
    technical_skills: [],
    projects: [],
  };

  useEffect(() => {
    fetchEvidence();
  }, [activeUserId]);

  const fetchEvidence = async () => {
    try {
      const data = await documentService.getProfileEvidence(activeUserId);
      setEvidenceData(data);
    } catch (err) {
      console.warn('Could not fetch evidence cards:', err);
    }
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile && !portfolioText.trim()) {
      setErrorMessage('Please select a file (PDF, DOCX, or TXT) or paste portfolio text.');
      return;
    }
    setErrorMessage('');
    setStatusMessage('Reading your resume...');
    setIsUploading(true);

    try {
      let res;
      if (selectedFile) {
        res = await documentService.uploadDocument(selectedFile, activeUserId, 'resume');
      } else {
        res = await documentService.analyzeText(portfolioText, activeUserId, 'portfolio', 'portfolio_text.txt');
      }

      setAnalysisResult(res);
      setStatusMessage('Resume analyzed successfully');
      setSelectedFile(null);
      setPortfolioText('');

      // Refresh persistent backend state
      await refreshAppState();
      await fetchEvidence();
    } catch (err) {
      console.error(err);
      setStatusMessage('');
      setErrorMessage(err.message || "We couldn't read this file. Please try another PDF or DOCX.");
    } finally {
      setIsUploading(false);
    }
  };

  const getSourceBadge = (source) => {
    const s = (source || '').toLowerCase();
    if (s.includes('resume')) {
      return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-orange-light text-orange-text">✓ Resume</span>;
    } else if (s.includes('project') || s.includes('portfolio')) {
      return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-skyblue/20 text-skyblue-text">✓ Project</span>;
    } else if (s.includes('assessment')) {
      return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-sage/20 text-sage">✓ Assessment</span>;
    }
    return <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-surface border border-border-subtle text-content-muted">✓ Declared</span>;
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 sm:p-8 shadow-card flex items-start gap-5">
        <div className="w-14 h-14 rounded-2xl bg-orange text-dark font-extrabold text-2xl flex items-center justify-center shrink-0">
          U
        </div>
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-dark">{user.user_id}</h1>
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-orange-light text-orange-text">
              {user.experience_level}
            </span>
          </div>
          <p className="text-sm font-bold text-dark">Target Role: {user.target_role}</p>
          <p className="text-xs text-content-secondary font-medium">{user.career_goal}</p>
        </div>
      </div>

      {/* Add Your Resume Section */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 shadow-card space-y-4">
        <div className="flex items-center gap-2 border-b border-border-subtle pb-3">
          <Upload className="w-5 h-5 text-orange" />
          <h2 className="font-extrabold text-base text-dark">Add Your Resume</h2>
        </div>
        <p className="text-xs text-content-secondary">
          Upload your resume to help EduPath understand your experience.
        </p>

        <form onSubmit={handleFileUpload} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-bold text-dark block">Supported formats: PDF, DOCX, TXT</label>
              <input
                type="file"
                accept=".pdf,.docx,.doc,.txt"
                onChange={(e) => setSelectedFile(e.target.files[0] || null)}
                className="block w-full text-xs text-content-secondary file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-orange file:text-dark hover:file:opacity-90"
              />
              {selectedFile && (
                <p className="text-[11px] font-mono text-sage font-bold">Selected: {selectedFile.name}</p>
              )}
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold text-dark block">Or Paste Project / Portfolio Description</label>
              <textarea
                value={portfolioText}
                onChange={(e) => setPortfolioText(e.target.value)}
                placeholder="e.g. Built a FastAPI microservice backed by PostgreSQL and PyTorch..."
                className="w-full h-24 text-xs p-3 rounded-xl border border-border-subtle bg-surface-soft text-dark focus:outline-none focus:ring-2 focus:ring-orange"
              />
            </div>
          </div>

          {errorMessage && (
            <p className="text-xs text-red-500 flex items-center gap-1 font-bold bg-red-50 p-3 rounded-xl border border-red-200">
              <AlertCircle className="w-4 h-4 shrink-0" /> {errorMessage}
            </p>
          )}

          {statusMessage && !errorMessage && (
            <p className="text-xs text-orange-text flex items-center gap-1 font-bold bg-orange-light p-3 rounded-xl border border-orange/30">
              <CheckCircle2 className="w-4 h-4 shrink-0 text-orange" /> {statusMessage}
            </p>
          )}

          <Button type="submit" disabled={isUploading} className="w-full sm:w-auto font-bold">
            {isUploading ? 'Reading your resume...' : 'Upload Resume'}
          </Button>
        </form>

        {analysisResult && (
          <div className="p-4 rounded-xl bg-orange-light border border-orange/30 space-y-2 text-xs text-dark">
            <div className="flex items-center justify-between">
              <p className="font-extrabold flex items-center gap-1.5 text-orange-text">
                <CheckCircle2 className="w-4 h-4" /> Resume analyzed successfully
              </p>
              <span className="text-[10px] font-bold font-mono px-2 py-0.5 bg-sage text-white rounded">
                Evidence found
              </span>
            </div>
            {analysisResult.agent_traces && (
              <div className="space-y-1 font-mono text-[11px] pt-1">
                {analysisResult.agent_traces.map((trace, i) => (
                  <p key={i} className="text-dark/80">{trace}</p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Evidence from Profile Section */}
      <div className="bg-surface border border-border-subtle rounded-2xl p-6 shadow-card space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-border-subtle">
          <div>
            <h2 className="font-extrabold text-base text-dark">Evidence from your profile</h2>
            <p className="text-xs text-content-secondary">Evidence-backed confidence scoring and provenance extracted from your resume</p>
          </div>
          <span className="text-xs font-mono font-bold px-3 py-1 rounded-full bg-surface-soft border border-border-subtle text-dark">
            Completeness: {user.profile_completeness || 85}%
          </span>
        </div>

        <div className="space-y-3">
          {((user.technical_skills && user.technical_skills.length > 0) ? user.technical_skills : (evidenceData?.evidence_cards || [])).length > 0 ? (
            ((user.technical_skills && user.technical_skills.length > 0) ? user.technical_skills : (evidenceData?.evidence_cards || [])).map((skill, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-surface-soft border border-border-subtle space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="font-extrabold text-sm text-dark">{skill.skill_name || skill.name}</span>
                    {getSourceBadge(skill.source)}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold font-mono text-orange">
                      Confidence: {((skill.confidence || 0.8) * 100).toFixed(0)}%
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-surface border border-border-subtle text-content-secondary font-bold">
                      {skill.proficiency || 'Intermediate'}
                    </span>
                  </div>
                </div>

                {skill.evidence && (Array.isArray(skill.evidence) ? skill.evidence.length > 0 : Boolean(skill.evidence)) ? (
                  <div className="pt-1 text-xs text-content-secondary space-y-1">
                    {(Array.isArray(skill.evidence) ? skill.evidence : [skill.evidence]).map((ev, i) => (
                      <div key={i} className="flex items-start gap-1.5 font-mono text-[11px] text-skyblue-text">
                        <ShieldCheck className="w-3.5 h-3.5 text-sage shrink-0 mt-0.5" />
                        {typeof ev === 'object' && ev !== null ? (
                          <span>
                            <strong className="text-dark">{ev.evidence_source || ev.source_type || 'Resume'}:</strong> "{ev.description || JSON.stringify(ev)}"
                          </span>
                        ) : (
                          <span>
                            <strong className="text-dark">Resume:</strong> "{ev}"
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-[11px] font-mono text-content-muted flex items-center gap-1">
                    <AlertCircle className="w-3 h-3 text-orange" /> Needs assessment to verify confidence
                  </p>
                )}
              </div>
            ))
          ) : (
            <p className="text-xs text-content-secondary">No technical skills recorded yet. Upload a resume above!</p>
          )}
        </div>
      </div>

      {/* Education & Projects */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-surface border border-border-subtle rounded-2xl p-6 shadow-card space-y-3">
          <h3 className="font-extrabold text-sm text-dark border-b border-border-subtle pb-2">
            Education
          </h3>
          {user.education && user.education.length > 0 ? (
            user.education.map((edu, idx) => (
              <div key={idx} className="text-xs space-y-0.5">
                <p className="font-extrabold text-dark">{edu.degree} in {edu.field_of_study}</p>
                <p className="text-content-secondary">{edu.institution} ({edu.graduation_year})</p>
              </div>
            ))
          ) : (
            <p className="text-xs text-content-muted">No education records.</p>
          )}
        </div>

        <div className="bg-surface border border-border-subtle rounded-2xl p-6 shadow-card space-y-3">
          <h3 className="font-extrabold text-sm text-dark border-b border-border-subtle pb-2">
            Portfolio Projects
          </h3>
          {user.projects && user.projects.length > 0 ? (
            user.projects.map((proj, idx) => (
              <div key={idx} className="text-xs space-y-0.5 border-b border-border-subtle pb-2 last:border-b-0">
                <p className="font-extrabold text-dark">{proj.title}</p>
                <p className="text-content-secondary">{proj.description}</p>
                {proj.technologies_used && proj.technologies_used.length > 0 && (
                  <div className="flex flex-wrap gap-1 pt-1">
                    {proj.technologies_used.map((t, i) => (
                      <span key={i} className="text-[10px] font-mono px-1.5 py-0.5 bg-surface rounded text-skyblue-text">
                        {t}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))
          ) : (
            <p className="text-xs text-content-muted">No projects recorded.</p>
          )}
        </div>
      </div>
    </div>
  );
}
