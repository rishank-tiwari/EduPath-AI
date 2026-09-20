# EduPath End-to-End Demo Script (3–5 Minutes)

## Objective
Demonstrate EduPath's end-to-end agentic learning loop: profile intelligence, skill gap detection, personalized roadmap generation, resource recommendation, practice evaluation, progress tracking, automatic learning-path adaptation, and context-aware AI mentorship.

---

## Step-by-Step Demo Flow

### 1. Introduction (30 seconds)
- **Goal**: Introduce the core problem EduPath solves.
- **Script**: *"Traditional learning platforms provide static video courses that treat every student the same. EduPath is a context-aware personalized learning agent that analyzes your real skills, builds a dynamic path to your target career role, tests your understanding, and automatically adapts your roadmap when you struggle."*

### 2. Learner Goal & Profile Analysis (45 seconds)
- **Action**: Click **Start Journey** on the Landing Page.
- **Inputs**:
  - Name: `Demo Learner`
  - Target Role: `AI/ML Engineer`
  - Current Skills: `Python`, `SQL`
  - Education: `B.S. Computer Science`
- **Action**: Click **Analyze Profile & Generate Path**.
- **Observation**:
  - Loading banner: *"Understanding your profile..."* $\rightarrow$ *"Checking your skills..."* $\rightarrow$ *"Building your learning path..."*.
  - AI Activity drawer records: `✓ Understood your profile` and `✓ Found your skill gaps`.

### 3. Skill Gap Intelligence & Personalized Roadmap (45 seconds)
- **Observation**:
  - Redirected to **Dashboard**. Overall role readiness calculated (e.g. `45%`).
  - **Skill Gaps**: Identifies `Python` as strong, `Statistics` as needs practice, and `Machine Learning` / `PyTorch` as missing.
  - **Your Learning Path**: Milestone modules built (`Week 1: Foundations of Machine Learning & Statistics`, `Week 2: Advanced Deep Learning`).

### 4. Learning Resource & Practice Session (60 seconds)
- **Action**: Click **Start Learning** on Today's Next Step task (`Probability & Combinatorics Fundamentals`).
- **Observation**:
  - **Learn This**: Curated resources loaded (video and documentation links).
- **Action**: Click **Start Practice**.
- **Action (Low-Score Scenario)**: Select answers deliberately yielding a low score (e.g., `2/5` = 40%).
- **Action**: Click **Check your answers**.

### 5. Automatic Plan Adaptation (45 seconds)
- **Observation**:
  - Practice result displayed: `2/5 correct (40%)`.
  - Background adaptation agent triggers: Progress status flagged as `needs_review` / `struggling`.
  - Adaptation decision event created: plan version increments from `v1` $\rightarrow$ `v2`.
  - Plan update banner appears: *"Your learning path was updated based on your result."* (Inserted foundational review step `Probability Basics Review`).
  - AI Activity drawer logs: `✓ Found a topic to review: Statistics` and `✓ Updated your next step (Plan v2)`.

### 6. Context-Aware AI Mentor Verification (60 seconds)
- **Action**: Navigate to **AI Mentor** tab.
- **Query 1**: Click suggested question chip: *"Why am I learning Statistics?"*
  - **Mentor Response**: Explains that Statistics is a required skill gap for the target `AI/ML Engineer` goal.
- **Query 2**: Ask custom question: *"Why did my learning path change?"*
  - **Mentor Response**: References actual stored practice score (`40.0%`) on `Probability Basics` and explains why EduPath inserted a review step before moving forward.
- **Query 3**: Ask *"What should I learn next?"*
  - **Mentor Response**: Points directly to the active, adapted next task in the learning plan.

### 7. Closing (15 seconds)
- **Script**: *"EduPath understands where you are today, shows where you need to go, helps you learn, and dynamically changes the path whenever you need extra help."*
