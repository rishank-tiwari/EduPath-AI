# Skill Gap Agent Specification

## 1. Overview & Architectural Boundaries

The **Skill Gap Agent** operates during the **GAP ANALYSIS** phase of the EduPath agentic workflow. Its sole responsibility is to answer the core career question:

> *"What skills and competencies are missing between this learner's current evidence-backed abilities and their target career role benchmark?"*

```
LearnerProfile (Task 1.1)
           ↓
    Target Role
           ↓
Role Skill Requirements (RoleService)
           ↓
   Skill Gap Agent (GAP ANALYSIS Phase)
           ↓
Structured Skill Gap Analysis
           ↓
  MongoDB ('skill_gaps' Collection)
           ↓
Future Learning Planner (Task 1.3)
```

The Skill Gap Agent is completely decoupled from:
- **Profile Agent** (UNDERSTAND phase: extracts background and calculates skill evidence confidence)
- **Learning Planner** (PLAN phase: structures weekly module roadmaps based on skill gap priorities)
- **Practice / Assessment / Adaptation Agents** (EVALUATE / RECALIBRATE phases)

---

## 2. Inputs & Data Flow

- **Primary Input**: `LearnerProfileResponse` document retrieved via `ProfileService.get_profile(user_id)`.
- **Target Role Benchmark**: `RoleRequirement` dataset retrieved via `RoleRequirementService.get_role_requirements(target_role)`.

---

## 3. Foundational Role Requirements Dataset (`AI/ML Engineer`)

The initial benchmark dataset provides standard requirement benchmarks for `AI/ML Engineer`:

| Required Skill | Required Proficiency | Importance Weight | Prerequisites |
| :--- | :--- | :---: | :--- |
| **Python** | Intermediate | High | None |
| **Machine Learning** | Intermediate | High | Python |
| **Statistics** | Intermediate | High | None |
| **Probability** | Intermediate | Medium | Statistics |
| **Data Processing** | Intermediate | Medium | Python |
| **Deep Learning** | Intermediate | Medium | Machine Learning, Python |
| **Model Evaluation** | Intermediate | High | Machine Learning |
| **MLOps** | Beginner | Medium | Python |
| **Model Deployment** | Beginner | Medium | Python |

---

## 4. Skill Normalization Engine

Raw skill declarations are normalized against canonical benchmark names using `normalize_skill_name()`:
- `Python Programming`, `Python3`, `Py` $\rightarrow$ `Python`
- `ML`, `Machine Learning Algorithms` $\rightarrow$ `Machine Learning`
- `Deep Learning / Neural Networks`, `Neural Networks`, `PyTorch` $\rightarrow$ `Deep Learning`
- `Stats`, `Statistical Analysis` $\rightarrow$ `Statistics`
- `MLOps & Deployment`, `Model Serving` $\rightarrow$ `MLOps` / `Model Deployment`

---

## 5. Gap Classification Rules

Numerical proficiency levels: `No evidence` ($0$) $<$ `Beginner` ($1$) $<$ `Intermediate` ($2$) $<$ `Advanced` ($3$) $<$ `Expert` ($4$).

- **`strong`**: Learner's current proficiency $>$ Required role proficiency.
- **`meets_requirement`**: Learner's current proficiency $==$ Required role proficiency.
- **`needs_improvement`**: Learner has evidence ($>0$), but current proficiency $<$ Required role proficiency.
- **`missing`**: Learner has no evidence or skill ($0$) for this required role competency.

---

## 6. Deterministic Priority Calculation

Priority assignment is computed deterministically based on gap status and role skill importance:

| Gap Status | Skill Importance | Calculated Priority |
| :--- | :---: | :---: |
| `missing` | High | **`high`** |
| `needs_improvement` | High | **`high`** |
| `missing` | Medium | **`medium`** |
| `needs_improvement` | Medium | **`medium`** |
| `meets_requirement` / `strong` | Any | **`low`** |
| `missing` / `needs_improvement` | Low | **`low`** |

---

## 7. Evidence Traceability & Preservation

Every current learner skill preserves its original `SkillEvidence` items from Task 1.1 (`source_type`, `source_id`, `description`). For skills classified as `missing`, `evidence = []`. No fake evidence is fabricated.

---

## 8. Deterministic Overall Readiness Formula

Readiness score ($0.0\%$ to $100.0\%$) measures how closely the current learner profile matches the benchmark requirements:

$$\text{Earned Points} = \sum (\text{Match Factor} \times \text{Importance Weight})$$
$$\text{Max Points} = \sum (1.0 \times \text{Importance Weight})$$
$$\text{Overall Readiness} = \min\left(100.0, \text{Round}\left(\frac{\text{Earned Points}}{\text{Max Points}} \times 100, 1\right)\right)$$

*Where Match Factors are*:
- `strong` / `meets_requirement`: $1.0$
- `needs_improvement`: $0.5$
- `missing`: $0.0$

*And Importance Weights are*:
- `high`: $3.0$
- `medium`: $2.0$
- `low`: $1.0$

---

## 9. API Specifications

- `POST /api/v1/skill-gaps/analyze?user_id=demo_user_1`
- `GET /api/v1/skill-gaps?user_id=demo_user_1`
- `GET /api/v1/skill-gaps/{skill_name}?user_id=demo_user_1`
