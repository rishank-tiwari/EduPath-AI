# EduPath Demo Data & Scenario Specification

## Overview
This document specifies the local demo state and deterministic scenario expectations for EduPath.

---

## 1. Local Demo Learner Profile
- **user_id**: `demo_user_1`
- **Name**: `Demo Learner`
- **Target Role**: `AI/ML Engineer`
- **Career Goal**: `Master deep learning and deploy ML models in production`
- **Experience Level**: `Entry-Level`
- **Education**:
  - `degree`: `B.S. Computer Science`
  - `field_of_study`: `Computer Science`
  - `institution`: `Tech University`
  - `graduation_year`: `2026`
- **Current Technical Skills**:
  - `Python` (Proficiency: `Advanced`, Confidence: `0.90`)
  - `SQL` (Proficiency: `Intermediate`, Confidence: `0.60`)

---

## 2. Benchmark Skill Gap Analysis
- **Benchmark Role**: `AI/ML Engineer`
- **Expected Skill Statuses**:
  - `Python`: `meets_requirement` / `strong`
  - `SQL`: `meets_requirement`
  - `Statistics & Probability`: `needs_improvement`
  - `Machine Learning`: `missing`
  - `Model Evaluation`: `missing`
  - `MLOps`: `missing`
- **Expected Overall Readiness**: `~45%`

---

## 3. Initial Learning Plan (Version 1)
- **Module 1**: `Foundations of Machine Learning & Statistics` (Week 1, High Priority)
  - **Task 1.1**: `Probability & Combinatorics Fundamentals` (Skill: `Statistics`)
  - **Task 1.2**: `Linear Algebra for Machine Learning` (Skill: `Machine Learning`)
- **Module 2**: `Supervised Learning & Model Evaluation` (Week 2)
- **Module 3**: `Production MLOps & Model Deployment` (Week 3)

---

## 4. Adaptive Low-Score Scenario (2/5 = 40%)
- **Input**: Learner submits practice quiz on `Probability Basics` with score `2/5` (`40.0%`).
- **Progress Analysis**:
  - `performance_status`: `struggling` / `needs_review`
  - `trend`: `declining`
- **Adaptation Action**: `review`
- **Plan Modification**:
  - Version: `v1` $\rightarrow$ `v2`
  - Inserted Task: `Probability Basics Review & Remediation`
  - Action Reason: `"Learner score (40.0%) fell below requirement threshold. Inserted foundational review task and practice step."`
- **AI Mentor Response to *"Why did my learning path change?"***:
  - References the real 40.0% quiz score and explains the automatic insertion of the review step.

---

## 5. High-Score Scenario (5/5 = 100%)
- **Input**: Learner submits practice quiz with score `5/5` (`100.0%`).
- **Progress Analysis**:
  - `performance_status`: `strong`
  - `trend`: `improving`
- **Adaptation Action**: `advance` / `move_forward`
- **Plan Modification**:
  - Advances learner to next topic in roadmap without forcing unnecessary basic review steps.

---

## 6. Context-Aware AI Mentor Context Schema
```json
{
  "target_role": "AI/ML Engineer",
  "current_skills": ["Python", "SQL"],
  "skill_gaps": ["Statistics & Probability", "Machine Learning", "Model Evaluation", "MLOps"],
  "current_learning_task": "Probability & Combinatorics Fundamentals",
  "learning_plan": ["Foundations of Machine Learning & Statistics", "Supervised Learning"],
  "recent_practice_result": {
    "score": 40.0,
    "total_questions": 5,
    "topic": "Probability Basics"
  },
  "progress_summary": {
    "performance_status": "needs_review",
    "latest_score": 40.0
  },
  "recent_adaptation": {
    "action": "review",
    "reason": "Learner score (40.0%) fell below requirement threshold. Inserted foundational review task.",
    "new_plan_version": 2
  }
}
```
