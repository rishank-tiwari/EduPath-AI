# EduPath Multi-Agent Architecture

## Architecture Overview

EduPath utilizes a goal-driven **Hierarchical Multi-Agent Architecture** centered around an **Orchestrator Agent**. Each sub-agent is responsible for a specific phase in the 7-step learning loop:

`UNDERSTAND → ANALYZE → PLAN → ACT → MEASURE → ADAPT → REPEAT`

```
                      ┌───────────────────────┐
                      │  Orchestrator Agent   │
                      └───────────┬───────────┘
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    │                             │                             │
┌───▼───────────┐         ┌───────▼───────┐             ┌───────▼───────┐
│ Profile Agent │         │ Skill Gap     │             │ Learning      │
│ (Understand)  │         │ Agent         │             │ Planner Agent │
└───────────────┘         │ (Analyze)     │             │ (Plan)        │
                          └───────────────┘             └───────────────┘
```

---

## 1. Profile Agent Specifications (Phase 1 — Task 1.1)

### Purpose & Scope
The **Profile Agent** operates during the **UNDERSTAND** phase. Its sole responsibility is answering:
> *"Who is this learner, and what concrete evidence backs their current capabilities?"*

It remains strictly independent from the future **Skill Gap Agent** (which answers: *"What is missing between this learner and their target role?"*).

### Input & Output Schemas
- **Input (`ProfileAnalysisInput`)**: `user_id`, `target_role`, `career_goal`, `raw_background`, `declared_skills`, `declared_projects`, `declared_certifications`, `declared_education`.
- **Output (`ProfileAnalysisResult`)**:
  - `user_id`, `target_role`, `career_goal`
  - `inferred_experience_level` ('Student' | 'Entry-Level' | 'Mid-Level' | 'Senior' | 'Lead')
  - `profile_summary` (Executive bio summary)
  - `technical_skills` (List of normalized skills with proficiency, evidence, and confidence scores 0.0–1.0)
  - `soft_skills` (List of identified soft competencies)
  - `projects`, `certifications`, `education`
  - `profile_completeness` (0.0 to 100.0%)

### Evidence-Backed Confidence Calculation
Skills are not arbitrary strings; confidence scores represent empirical evidence strength:
- **Unverified self-declared skill**: Base confidence `0.50` (`source_type: "manual"`).
- **Skill backed by 1 project evidence**: Confidence boosted to `0.70` (`source_type: "project"`).
- **Skill backed by multiple projects/certs**: Confidence scales up to `0.95`.

### Document Processing Abstraction
Future resume uploads, PDF parsing, and OCR processing interface with `BaseDocumentProcessor` (`app.services.document_processor`). Currently configured with `UnimplementedDocumentProcessor` to mark future integration points cleanly without fake extractions.

### Interaction with Future Agents
The Profile Agent produces the validated `LearnerProfileResponse` and persists it to the `learner_profiles` MongoDB collection.
Downstream agents consume this profile:
- **Skill Gap Agent (Task 1.2)**: Reads `technical_skills` & `confidence` scores from `LearnerProfile` to compute deficits against industry benchmarks.

---

## 2. Agent Roster Overview

| Agent Name | Loop Phase | Responsibility | Key Input | Key Output |
| :--- | :--- | :--- | :--- | :--- |
| **Profile Agent** | UNDERSTAND | Extracts structured candidate profile from resumes, projects, and career targets. | Raw Resume Text, Career Goals | `LearnerProfile` object |
| **Skill Gap Agent** | ANALYZE | Computes skill gaps against industry requirements and assigns proficiency levels. | `LearnerProfile`, Target Role | `SkillGapAnalysis` report |
| **Learning Planner** | PLAN | Builds milestone-based, time-bounded learning roadmaps tailored to gaps. | `SkillGapAnalysis`, Time budget | `LearningPlan` roadmap |
| **Resource Agent** | ACT | Discovers, filters, and ranks optimal articles, videos, and tutorials. | Topic, Skill Gap, Format | Recommended Resource list |
| **Practice Agent** | ACT | Synthesizes hands-on coding challenges and real-world scenario prompts. | Target Skill, Difficulty | `PracticeTask` specification |
| **Assessment Agent** | MEASURE | Grades task submissions against rubric criteria and details feedback. | Task Submission, Rubric | `AssessmentResult` & Score |
| **Progress Agent** | MEASURE | Calculates skill mastery curves and tracks longitudinal progress. | Assessment History | Skill Mastery Metrics |
| **Adaptation Agent** | ADAPT | Re-evaluates learning plan when weaknesses or plateauing are detected. | Mastery Metrics, Errors | Updated `LearningPlan` |
