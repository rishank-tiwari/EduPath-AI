# EduPath API Specification

## Base URL
`/api/v1`

---

## 1. System Health
### `GET /api/v1/health`
Returns system status, environment, version, and database connectivity.

**Response `200 OK`**:
```json
{
  "status": "ok",
  "service": "EduPath API",
  "version": "0.1.0",
  "environment": "development",
  "database": "connected"
}
```

---

## 2. Learner Profile Intelligence (Phase 1 — Task 1.1)

### `POST /api/v1/profile`
Creates or updates a stored `LearnerProfile` document in MongoDB.

**Required Request Fields**:
- `user_id` (string, e.g. `"demo_user_1"`)
- `target_role` (string, e.g. `"AI/ML Engineer"`)
- `career_goal` (string, e.g. `"Build production LLM applications"`)

**Optional Request Fields**:
- `experience_level` (string, default: `"Entry-Level"`): Options: `"Student"`, `"Entry-Level"`, `"Mid-Level"`, `"Senior"`, `"Lead"`
- `education` (array of objects): Structured educational records
- `technical_skills` (array of objects): Skills with evidence-backed confidence
- `soft_skills` (array of strings)
- `projects` (array of objects): Portfolio project items
- `certifications` (array of objects)
- `profile_summary` (string or null)
- `profile_completeness` (float 0.0 to 100.0, automatically calculated if omitted)

**Deterministic Evidence-Backed Skill Confidence Formula**:
- Base self-declared skill (`source_type: "manual"` or `"resume"` or no evidence): `0.40`
- Project evidence (`source_type: "project"`): `+0.25` per project
- Certification evidence (`source_type: "certificate"`): `+0.20` per cert
- Assessment evidence (`source_type: "assessment"`): `+0.30` per assessment
- Capped at maximum `0.95`

**Full Request Body Example (`LearnerProfileCreate`)**:
```json
{
  "user_id": "demo_user_1",
  "target_role": "AI/ML Engineer",
  "career_goal": "Build production LLM applications",
  "experience_level": "Mid-Level",
  "education": [
    {
      "degree": "B.Tech",
      "field_of_study": "Computer Science Engineering",
      "institution": "Example University",
      "graduation_year": 2026
    }
  ],
  "technical_skills": [
    {
      "name": "Python",
      "proficiency": "Advanced",
      "confidence": 0.90,
      "evidence": [
        {
          "source_type": "project",
          "source_id": "proj_101",
          "description": "Primary backend language for LLM pipeline"
        }
      ]
    },
    {
      "name": "FastAPI",
      "proficiency": "Intermediate",
      "evidence": [
        {
          "source_type": "project",
          "source_id": "proj_101",
          "description": "REST API framework"
        }
      ]
    }
  ],
  "soft_skills": [
    "Problem Solving",
    "Technical Communication"
  ],
  "projects": [
    {
      "project_id": "proj_101",
      "title": "EduPath Platform",
      "description": "Agentic career learning engine",
      "technologies_used": ["Python", "FastAPI"],
      "repository_url": "https://github.com/example/edupath",
      "demo_url": null
    }
  ],
  "certifications": [
    {
      "cert_id": "cert_aws_1",
      "name": "AWS Certified Machine Learning Specialty",
      "issuing_organization": "Amazon Web Services",
      "issue_date": "2025-06",
      "credential_id": "AWS-123456"
    }
  ]
}
```

**Response `201 Created`**: Returns the saved `LearnerProfileResponse` document.

---

### `GET /api/v1/profile`
Retrieves a stored learner profile by `user_id`.

**Query Parameters**:
- `user_id` (string, default: `"demo_user_1"`): Target learner user ID.

**Response `200 OK`**: `LearnerProfileResponse` JSON object.
**Response `404 Not Found`**: Returned if no profile document exists for the user.

---

### `POST /api/v1/profile/analyze`
Executes Profile Agent analysis on input background information, extracts skills, calculates evidence-backed confidence scores, and persists the resulting structured profile.

**Request Body (`ProfileAnalysisInput`)**:
```json
{
  "user_id": "usr_981241",
  "target_role": "AI/ML Engineer",
  "career_goal": "Master LLM agent orchestration",
  "declared_skills": ["Python", "PyTorch", "FastAPI"],
  "declared_projects": [
    {
      "title": "RAG Search Engine",
      "description": "Built vector search with PyTorch embeddings",
      "technologies_used": ["Python", "PyTorch", "FastAPI"]
    }
  ]
}
```

**Response `200 OK`**: Returns the analyzed & stored `LearnerProfileResponse` JSON object.

---

## 3. Skill Gap Intelligence (Phase 1 — Task 1.2)

### `POST /api/v1/skill-gaps/analyze`
Executes Skill Gap Agent analysis for the learner profile of the specified `user_id`, compares evidence-backed skills against benchmark role requirements, computes gap classifications, priorities, and readiness, and persists the analysis in MongoDB.

**Query Parameters**:
- `user_id` (string, default: `"demo_user_1"`): Learner user ID to analyze.

**Response `200 OK` (`SkillGapResponse`)**:
```json
{
  "user_id": "demo_user_1",
  "target_role": "AI/ML Engineer",
  "analyzed_at": "2026-09-19T13:00:00.000000",
  "skills": [
    {
      "skill_name": "Python",
      "required_proficiency": "Intermediate",
      "current_proficiency": "Advanced",
      "gap_status": "strong",
      "priority": "low",
      "importance": "high",
      "reason": "Python exceeds the Intermediate proficiency requirement for AI/ML Engineer.",
      "evidence": [
        {
          "source_type": "project",
          "source_id": "proj_101",
          "description": "Primary backend language for LLM pipeline"
        }
      ]
    },
    {
      "skill_name": "Statistics",
      "required_proficiency": "Intermediate",
      "current_proficiency": "Beginner",
      "gap_status": "needs_improvement",
      "priority": "high",
      "importance": "high",
      "reason": "Statistics is required at Intermediate level for AI/ML Engineer. Current learner level is Beginner.",
      "evidence": []
    },
    {
      "skill_name": "Deep Learning",
      "required_proficiency": "Intermediate",
      "current_proficiency": "No evidence",
      "gap_status": "missing",
      "priority": "medium",
      "importance": "medium",
      "reason": "Deep Learning is a required Intermediate skill for AI/ML Engineer, but no evidence currently exists in the learner profile.",
      "evidence": []
    }
  ],
  "overall_readiness": 65.5,
  "summary": "Skill gap analysis for target role 'AI/ML Engineer'. Overall role readiness is 65.5%. Learner meets 4 skill requirements, needs improvement in 2, and is missing 3 required competencies."
}
```

**Response `400 Bad Request`**: Returned if the learner profile is missing or target_role is not specified.
**Response `503 Service Unavailable`**: Returned if MongoDB is disconnected.

---

### `GET /api/v1/skill-gaps`
Retrieves the latest stored skill gap analysis for a specific learner.

**Query Parameters**:
- `user_id` (string, default: `"demo_user_1"`): Target learner user ID.

**Response `200 OK`**: `SkillGapResponse` JSON object.
**Response `404 Not Found`**: Returned if no skill gap document exists for the user.

---

### `GET /api/v1/skill-gaps/{skill_name}`
Retrieves skill gap analysis item for a specific skill name.

**Query Parameters**:
- `user_id` (string, default: `"demo_user_1"`): Target learner user ID.

**Response `200 OK`**: `SkillGapItem` JSON object.
**Response `404 Not Found`**: Returned if the specified skill item does not exist in the user's latest analysis.

---

## 4. Learning Planner Foundation (Phase 1 — Task 1.3)

### `POST /api/v1/plans/generate`
Generates a personalized, prerequisite-ordered, weekly learning plan for a learner.

**Query Parameters**:
- `user_id` (string, required, e.g. `"demo_user_1"`)

**Response `200 OK`**:
```json
{
  "plan_id": "plan_49c113f74089",
  "user_id": "demo_user_1",
  "target_role": "AI/ML Engineer",
  "title": "AI/ML Engineer Learning Path",
  "summary": "Personalized 3-week learning roadmap for AI/ML Engineer.",
  "total_estimated_hours": 29.1,
  "duration_weeks": 3,
  "version": 1,
  "modules": [
    {
      "module_id": "mod_w1_stat123",
      "title": "Statistics Foundations",
      "description": "Focus on missing skill in Statistics to meet AI/ML Engineer requirements.",
      "skill_name": "Statistics",
      "priority": "high",
      "week_number": 1,
      "estimated_hours": 3.8,
      "prerequisites": ["Probability"],
      "status": "not_started",
      "tasks": [
        {
          "task_id": "task_abc123",
          "title": "Learn Statistics Core Concepts",
          "description": "Study key theoretical concepts, formulas, and architecture.",
          "task_type": "learn",
          "estimated_minutes": 60,
          "skill_name": "Statistics",
          "difficulty": "Intermediate",
          "status": "not_started"
        }
      ]
    }
  ],
  "created_at": "2026-09-19T13:23:14.000000",
  "updated_at": "2026-09-19T13:23:14.000000"
}
```

**Response `400 Bad Request`**: Returned if the learner profile or skill gap analysis does not exist for the specified `user_id`.
**Response `503 Service Unavailable`**: Returned if MongoDB is disconnected.

---

### `GET /api/v1/plans`
Retrieves the latest stored learning plan for a learner.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK`**: `LearningPlanResponse` JSON object.
**Response `404 Not Found`**: Returned if no learning plan exists for the user.

---

### `GET /api/v1/plans/{plan_id}`
Retrieves a specific learning plan document by its unique `plan_id`.

**Response `200 OK`**: `LearningPlanResponse` JSON object.
**Response `404 Not Found`**: Returned if the plan_id does not exist.

---

## 5. Resource & Practice Agent Foundation (Phase 1 — Task 1.4)

### `POST /api/v1/resources/recommend`
Recommends curated learning resources (documentation, videos, articles) matching a learning task.

**Request Body (`ResourceRecommendationRequest`)**:
```json
{
  "task_id": "task_prob_101",
  "skill_name": "Probability",
  "difficulty": "beginner",
  "user_id": "demo_user_1"
}
```

**Response `200 OK`**:
```json
{
  "task_id": "task_prob_101",
  "skill_name": "Probability",
  "topic": "Probability Learning Resources",
  "resources": [
    {
      "resource_id": "res_prob_01",
      "title": "Introduction to Probability Distributions",
      "description": "Comprehensive article explaining discrete vs continuous distributions.",
      "resource_type": "article",
      "url": "https://www.khanacademy.org/math/statistics-probability/random-variables-stats-library",
      "skill_name": "Probability",
      "difficulty": "beginner",
      "estimated_minutes": 25,
      "source": "Khan Academy"
    }
  ]
}
```

---

### `POST /api/v1/practice/generate`
Generates a practice session (MCQ & Short Answer) for a learning task.

**Request Body**:
```json
{
  "user_id": "demo_user_1",
  "task_id": "task_prob_101",
  "skill_name": "Probability",
  "difficulty": "beginner"
}
```

**Response `200 OK`**:
```json
{
  "practice_id": "prac_ae115e791b",
  "user_id": "demo_user_1",
  "task_id": "task_prob_101",
  "skill_name": "Probability",
  "topic": "Probability Practice Session",
  "difficulty": "beginner",
  "questions": [
    {
      "question_id": "q_prob_101",
      "question": "What is the probability of rolling an even number on a fair 6-sided die?",
      "question_type": "mcq",
      "options": ["1/6", "1/2", "1/3", "2/3"],
      "difficulty": "beginner"
    }
  ]
}
```

---

### `POST /api/v1/practice/{practice_id}/submit`
Evaluates submitted practice answers, computes score & percentage, and stores result in MongoDB.

**Request Body (`PracticeSubmissionRequest`)**:
```json
{
  "user_id": "demo_user_1",
  "answers": [
    {
      "question_id": "q_prob_101",
      "learner_answer": "1/2"
    }
  ]
}
```

**Response `200 OK`**:
```json
{
  "result_id": "res_d812b52b13",
  "user_id": "demo_user_1",
  "practice_id": "prac_ae115e791b",
  "task_id": "task_prob_101",
  "skill_name": "Probability",
  "topic": "Probability Practice Session",
  "difficulty": "beginner",
  "score": 1,
  "total_questions": 1,
  "percentage": 100.0,
  "question_results": [
    {
      "question_id": "q_prob_101",
      "question": "What is the probability of rolling an even number on a fair 6-sided die?",
      "correct": true,
      "learner_answer": "1/2",
      "correct_answer": "1/2",
      "explanation": "There are 3 even numbers (2, 4, 6) out of 6 possible outcomes, so 3/6 = 1/2."
    }
  ],
  "completed_at": "2026-09-19T13:37:05.000000"
}
```

---

### `GET /api/v1/practice/history`
Retrieves a learner's previous practice evaluation results.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK`**: Array of `PracticeResultRecord` objects.

---

## 6. Progress & Adaptive Learning Foundation (Phase 1 — Task 1.5)

### `POST /api/v1/progress/record`
Records a new learning or practice progress event log.

**Request Body (`ProgressRecordRequest`)**:
```json
{
  "user_id": "demo_user_1",
  "event_type": "task_completed",
  "skill_name": "Statistics",
  "topic": "Probability Distributions",
  "metadata": { "task_id": "task_stat_01" }
}
```

**Response `200 OK`**: `ProgressEvent` JSON object.

---

### `GET /api/v1/progress`
Retrieves learner progress summaries across skills and topics.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK`**: Array of `ProgressSummary` objects (`performance_status`: `strong`, `on_track`, `needs_review`, `struggling`; `trend`: `improving`, `stable`, `declining`, `insufficient_data`).

---

### `GET /api/v1/progress/skills`
Retrieves learner progress summaries grouped by skill.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK`**: Array of `SkillProgressSummary` objects.

---

### `GET /api/v1/progress/history`
Retrieves progress event logs for a learner.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK`**: Array of `ProgressEvent` objects.

---

### `POST /api/v1/adaptation/analyze`
Analyzes learner progress, applies adaptation rules, modifies learning plan, and increments plan version ($v1 \rightarrow v2$).

**Request Body (`AdaptationAnalyzeRequest`)**:
```json
{
  "user_id": "demo_user_1",
  "skill_name": "Statistics",
  "topic": "Probability Distributions"
}
```

**Response `200 OK`**:
```json
{
  "event_id": "adapt_e60620e3e9",
  "user_id": "demo_user_1",
  "trigger": "practice_result",
  "skill_name": "Statistics",
  "topic": "Probability Distributions",
  "previous_status": "struggling",
  "action": "review",
  "reason": "Learner score (0.0%) fell below requirement threshold. Inserted foundational review task and practice step.",
  "affected_plan_version": 1,
  "new_plan_version": 2,
  "created_at": "2026-09-19T14:22:11.000000"
}
```

---

### `GET /api/v1/adaptation/history`
Retrieves previous adaptation decisions and plan version history for a learner.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK`**: Array of `AdaptationDecision` objects.

---

## 7. Context-Aware AI Mentor (Phase 2 — Task 2.2)

### `POST /api/v1/mentor/chat`
Sends a query to the context-aware Mentor Agent. Constructs real-time context from stored user state and returns grounded advice and suggested actions.

**Request Body (`MentorChatRequest`)**:
```json
{
  "user_id": "demo_user_1",
  "message": "Why am I learning Statistics?"
}
```

**Response `200 OK` (`MentorResponse`)**:
```json
{
  "response": "Statistics is part of your learning path because it is currently a gap for your AI/ML Engineer goal.",
  "context_topic": "Statistics",
  "suggested_action": "Review Probability Basics",
  "response_mode": "fallback",
  "related_skill": "Statistics",
  "related_task": "Probability Basics",
  "related_gap": "Statistics & Probability",
  "created_at": "2026-09-20T13:40:00Z"
}
```

---

### `GET /api/v1/mentor/context`
Retrieves sanitized context currently compiled for the learner. Does not expose backend DB IDs, secrets, or internal keys.

**Query Parameters**:
- `user_id` (string, required): Target learner user ID.

**Response `200 OK` (`SanitizedMentorContext`)**:
```json
{
  "target_role": "AI/ML Engineer",
  "current_skills": ["Python", "FastAPI"],
  "skill_gaps": ["Statistics & Probability", "PyTorch"],
  "current_learning_task": "Probability & Combinatorics Fundamentals",
  "learning_plan_summary": ["Module 1: Foundations", "Module 2: Advanced AI"],
  "recent_practice_result": {
    "score": 40.0,
    "topic": "Probability Basics",
    "status": "needs_review"
  },
  "progress_summary": {
    "completion_rate": 25.0,
    "average_score": 65.0
  },
  "recent_adaptation": {
    "action": "review",
    "reason": "Recent quiz score indicated review needed."
  }
}
```




