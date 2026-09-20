import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { profileService } from '../services/profileService';
import { skillGapService } from '../services/skillGapService';
import { planService } from '../services/planService';
import { resourceService } from '../services/resourceService';
import { practiceService } from '../services/practiceService';
import { progressService } from '../services/progressService';
import { adaptationService } from '../services/adaptationService';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [userId, setUserId] = useState(() => localStorage.getItem('edupath_user_id') || 'demo_user_1');
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('edupath_token') || 'demo_jwt_token_123');
  const [activeTab, setActiveTab] = useState('home');
  const [isAgentModalOpen, setIsAgentModalOpen] = useState(false);

  const isAuthenticated = Boolean(authToken);

  const loginUser = async (usernameOrEmail, password) => {
    const res = await authService.login(usernameOrEmail, password);
    if (res && res.access_token) {
      localStorage.setItem('edupath_token', res.access_token);
      localStorage.setItem('edupath_user_id', res.user_id);
      setAuthToken(res.access_token);
      setUserId(res.user_id);
      addAiLog(`User '${res.username}' logged in successfully`, 'success');
      return res;
    }
  };

  const registerUser = async (username, email, password) => {
    const res = await authService.register(username, email, password);
    if (res && res.access_token) {
      localStorage.setItem('edupath_token', res.access_token);
      localStorage.setItem('edupath_user_id', res.user_id);
      setAuthToken(res.access_token);
      setUserId(res.user_id);
      addAiLog(`User '${res.username}' registered successfully`, 'success');
      return res;
    }
  };

  const logoutUser = () => {
    localStorage.removeItem('edupath_token');
    localStorage.removeItem('edupath_user_id');
    setAuthToken(null);
    setUserId('demo_user_1');
    addAiLog('User logged out', 'info');
  };

  // Core Journey State
  const [userProfile, setUserProfile] = useState(null);
  const [skillGapAnalysis, setSkillGapAnalysis] = useState(null);
  const [learningPlan, setLearningPlan] = useState(null);
  const [currentTask, setCurrentTask] = useState(null);
  const [recommendedResources, setRecommendedResources] = useState([]);
  const [activePracticeSession, setActivePracticeSession] = useState(null);
  const [latestPracticeResult, setLatestPracticeResult] = useState(null);
  const [progressSummaries, setProgressSummaries] = useState([]);
  const [adaptationHistory, setAdaptationHistory] = useState([]);

  // UI States
  const [loadingState, setLoadingState] = useState(null); // e.g. "Understanding your profile..."
  const [errorState, setErrorState] = useState(null);

  // AI Activity Timeline Logs
  const [aiActivityLogs, setAiActivityLogs] = useState([
    { id: 1, title: 'EduPath AI Agent Engine Ready', time: 'Just now', type: 'system' }
  ]);

  const addAiLog = (title, type = 'info') => {
    setAiActivityLogs((prev) => [
      { id: Date.now(), title, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), type },
      ...prev,
    ]);
  };

  const toggleAgentModal = () => setIsAgentModalOpen((prev) => !prev);

  const refreshAppState = async () => {
    if (!userId) return;
    try {
      const prof = await profileService.getProfile(userId);
      if (prof && prof.user_id) {
        setUserProfile(prof);
      }
      try {
        const gaps = await skillGapService.getSkillGaps(userId);
        if (gaps) setSkillGapAnalysis(gaps);
      } catch (e) {}

      try {
        const plan = await planService.getLatestPlan(userId);
        if (plan) setLearningPlan(plan);
      } catch (e) {}
    } catch (e) {
      console.warn('refreshAppState error:', e);
    }
  };

  // Run initial data load for demo_user_1 if available
  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoadingState('Loading EduPath profile...');
        await refreshAppState();
      } catch (err) {
        console.log('No existing remote profile loaded:', err.message);
      } finally {
        setLoadingState(null);
      }
    }
    loadInitialData();
  }, [userId]);

  // Journey Action 1: Submit Profile & Execute Pipeline
  const runFullPipeline = async (profilePayload) => {
    setErrorState(null);
    try {
      // 1. Profile Creation
      setLoadingState('Understanding your profile...');
      const savedProfile = await profileService.saveProfile(profilePayload);
      setUserProfile(savedProfile);
      addAiLog('✓ Understood your profile');

      // 2. Skill Gap Analysis
      setLoadingState('Checking your skills...');
      const gaps = await skillGapService.analyzeSkillGaps(savedProfile.user_id);
      setSkillGapAnalysis(gaps);
      addAiLog('✓ Found your skill gaps');

      // 3. Learning Plan Generation
      setLoadingState('Building your learning path...');
      const plan = await planService.generatePlan(savedProfile.user_id);
      setLearningPlan(plan);
      addAiLog('✓ Built your learning path');

      if (plan && plan.modules && plan.modules.length > 0) {
        const firstMod = plan.modules[0];
        if (firstMod.tasks && firstMod.tasks.length > 0) {
          setCurrentTask(firstMod.tasks[0]);
        }
      }

      return { profile: savedProfile, gaps, plan };
    } catch (err) {
      console.error('Pipeline error:', err);
      setErrorState(err.message || 'Failed to complete profile analysis. Please check backend connection.');
      throw err;
    } finally {
      setLoadingState(null);
    }
  };

  // Journey Action 2: Load Resources for Task
  const loadResourcesForTask = async (task) => {
    if (!task) return;
    setErrorState(null);
    try {
      setLoadingState('Finding learning resources...');
      const res = await resourceService.recommendResources(
        task.task_id,
        task.skill_name,
        task.difficulty || 'beginner',
        userId
      );
      setRecommendedResources(res.resources || []);
      addAiLog(`✓ Recommended learning resource for ${task.skill_name}`);
      return res.resources;
    } catch (err) {
      console.error('Resource error:', err);
      setErrorState('Could not load resources right now. Please try again.');
    } finally {
      setLoadingState(null);
    }
  };

  // Journey Action 3: Generate Practice Session
  const generatePracticeForTask = async (task, practiceMode = 'general', moduleId = null) => {
    setErrorState(null);
    try {
      setLoadingState('Preparing your practice...');
      const targetTaskId = task?.task_id || 'task_default';
      const targetSkill = task?.skill_name || 'Statistics';
      const targetDiff = task?.difficulty || 'beginner';
      const targetModule = moduleId || task?.module_id || null;

      const session = await practiceService.generatePractice(
        userId,
        targetTaskId,
        targetSkill,
        targetDiff,
        practiceMode,
        targetModule
      );
      setActivePracticeSession(session);
      setLatestPracticeResult(null);
      const qCount = session.questions ? session.questions.length : (practiceMode === 'module' ? 5 : 10);
      addAiLog(`✓ Created ${qCount}-question practice set for ${targetSkill}`);
      return session;
    } catch (err) {
      if (err.response && err.response.status === 409) {
        return { isCompleted: true };
      }
      console.error('Practice error:', err);
      setErrorState('Could not generate practice set right now. Please try again.');
    } finally {
      setLoadingState(null);
    }
  };

  // Journey Action 4: Submit Practice & Evaluate
  const submitPracticeAnswers = async (practiceId, answers) => {
    setErrorState(null);
    try {
      const result = await practiceService.submitPractice(practiceId, userId, answers);
      setLatestPracticeResult(result);
      addAiLog(`✓ Checked your practice answers (${result.score}/${result.total_questions} correct)`);

      // Trigger adaptation automatically based on result
      try {
        const targetSkill = result.skill_name || (currentTask ? currentTask.skill_name : null);
        const decision = await adaptationService.analyzeAndAdapt(userId, targetSkill, result.topic);
        if (decision.action === 'review' || decision.action === 'add_practice') {
          addAiLog(`✓ Found a topic to review: ${decision.skill_name}`);
        } else {
          addAiLog(`✓ Advanced path step (Plan v${decision.new_plan_version})`);
        }

        // Refresh plan and next task
        const updatedPlan = await planService.getLatestPlan(userId);
        setLearningPlan(updatedPlan);
        if (updatedPlan && updatedPlan.modules && updatedPlan.modules.length > 0) {
          const firstMod = updatedPlan.modules[0];
          if (firstMod.tasks && firstMod.tasks.length > 0) {
            setCurrentTask(firstMod.tasks[0]);
          }
        }

        // Refresh adaptation history
        const hist = await adaptationService.getHistory(userId);
        setAdaptationHistory(hist);
      } catch (e) {
        console.error('Auto-adaptation error after practice submit:', e);
      }

      // Refresh progress
      try {
        const prog = await progressService.getUserProgress(userId);
        setProgressSummaries(prog);
      } catch (e) { /* ignore */ }

      return result;
    } catch (err) {
      console.error('Submission error:', err);
      setErrorState('Failed to submit practice answers. Please try again.');
      throw err;
    }
  };

  // Journey Action 5: Trigger Adaptation Analysis & Plan Update
  const triggerAdaptation = async (skillName = null, topic = null) => {
    setErrorState(null);
    try {
      setLoadingState('Checking what you should do next...');
      const targetSkill = skillName || (currentTask ? currentTask.skill_name : null);
      const decision = await adaptationService.analyzeAndAdapt(userId, targetSkill, topic);

      if (decision.action === 'review' || decision.action === 'add_practice') {
        addAiLog(`✓ Found a topic to review: ${decision.skill_name}`);
      }
      addAiLog(`✓ Updated your next step (Plan v${decision.new_plan_version})`);

      // Refresh learning plan v1 -> v2
      const updatedPlan = await planService.getLatestPlan(userId);
      setLearningPlan(updatedPlan);

      // Set new active next step
      if (updatedPlan && updatedPlan.modules && updatedPlan.modules.length > 0) {
        const firstMod = updatedPlan.modules[0];
        if (firstMod.tasks && firstMod.tasks.length > 0) {
          setCurrentTask(firstMod.tasks[0]);
        }
      }

      // Refresh adaptation history
      const hist = await adaptationService.getHistory(userId);
      setAdaptationHistory(hist);

      return decision;
    } catch (err) {
      console.error('Adaptation error:', err);
      setErrorState('Could not update learning path right now.');
    } finally {
      setLoadingState(null);
    }
  };

  const value = {
    userId,
    setUserId,
    authToken,
    isAuthenticated,
    loginUser,
    registerUser,
    logoutUser,
    activeTab,
    setActiveTab,
    isAgentModalOpen,
    setIsAgentModalOpen,
    toggleAgentModal,
    userProfile,
    setUserProfile,
    skillGapAnalysis,
    setSkillGapAnalysis,
    learningPlan,
    setLearningPlan,
    currentTask,
    setCurrentTask,
    recommendedResources,
    setRecommendedResources,
    activePracticeSession,
    setActivePracticeSession,
    latestPracticeResult,
    setLatestPracticeResult,
    progressSummaries,
    setProgressSummaries,
    adaptationHistory,
    setAdaptationHistory,
    loadingState,
    setLoadingState,
    errorState,
    setErrorState,
    aiActivityLogs,
    addAiLog,
    runFullPipeline,
    refreshAppState,
    loadResourcesForTask,
    generatePracticeForTask,
    submitPracticeAnswers,
    triggerAdaptation,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}
