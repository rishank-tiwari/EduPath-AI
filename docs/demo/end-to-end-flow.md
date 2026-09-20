# EduPath End-to-End Demo Scenario (Task 2.1)

## Demo Scenario: Adaptive Learning Loop in Action

### Step 1: Profile Creation
- **Learner Name**: Jane Developer
- **Target Role**: `AI/ML Engineer`
- **Current Skills**: `Python` (Advanced), `Machine Learning` (Beginner)

### Step 2: Skill Gap Analysis Output
- `Python` $\rightarrow$ **Strong** (exceeds requirement)
- `Statistics` $\rightarrow$ **Missing**
- `Deep Learning` $\rightarrow$ **Missing**
- `MLOps` $\rightarrow$ **Missing**

### Step 3: Initial Learning Plan Generation (Version 1)
- **Roadmap**: Week 1: Statistics Foundations $\rightarrow$ Week 2: Machine Learning $\rightarrow$ Week 3: Deep Learning $\rightarrow$ Week 4: MLOps.
- **Active Task**: `"Learn Statistics Core Concepts"`

### Step 4: Learning & Practice Execution
- Learner opens resource: *Khan Academy — Probability & Statistics*.
- Learner starts practice session: 2 questions on Probability & Statistics.
- Learner submits answers and receives a **0% score** (0/2 correct).

### Step 5: Progress Detection & Path Adaptation (Version 2)
- **Progress Agent**: Detects performance status = **`struggling`**.
- **Adaptation Agent**: Evaluates rule and triggers action = **`review`**.
- **Reason**: *"Learner score (0.0%) fell below requirement threshold. Inserted foundational review task and practice step."*
- **Plan Version Transition**: $v1 \longrightarrow v2$.
- **New Active Next Step**: `"Review Statistics Practice Session Core Concepts"` (Prepended to Week 1 module).

---

## Result
EduPath demonstrates real agentic adaptation: when performance drops, the roadmap dynamically recalibrates without destroying historical context or presenting synthetic data.
