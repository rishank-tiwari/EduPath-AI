import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';
import { LandingPage } from '../pages/LandingPage';
import { OnboardingPage } from '../pages/OnboardingPage';
import { DashboardPage } from '../pages/DashboardPage';
import { MyPathPage } from '../pages/MyPathPage';
import { TodayLearningPage } from '../pages/TodayLearningPage';
import { PracticePage } from '../pages/PracticePage';
import { PracticeResultPage } from '../pages/PracticeResultPage';
import { AIMentorPage } from '../pages/AIMentorPage';
import { ProgressPage } from '../pages/ProgressPage';
import { LoginPage } from '../pages/LoginPage';
import { ProfilePage } from '../pages/ProfilePage';
import { LearningGuidePage } from '../pages/LearningGuidePage';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { NotFoundPage } from '../pages/NotFoundPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        {/* Public Routes */}
        <Route index element={<LandingPage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="dashboard" element={<DashboardPage />} />

        {/* Protected Learner Routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="onboarding" element={<OnboardingPage />} />
          <Route path="my-path" element={<MyPathPage />} />
          <Route path="learn" element={<TodayLearningPage />} />
          <Route path="practice" element={<PracticePage />} />
          <Route path="practice/result/:practiceId" element={<PracticeResultPage />} />
          <Route path="mentor" element={<AIMentorPage />} />
          <Route path="progress" element={<ProgressPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="learning-guide" element={<LearningGuidePage />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
