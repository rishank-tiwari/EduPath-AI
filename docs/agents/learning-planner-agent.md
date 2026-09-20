# Learning Planner Agent Documentation (Task 1.3)

## Purpose
The **Learning Planner Agent** (`PLAN` phase) converts a learner's structured profile, skill gap analysis, and target role benchmark requirements into a personalized, prerequisite-ordered, weekly-chunked **Learning Plan**.

It answers:
> *"What should this learner learn next, in what order, and what daily tasks should they perform?"*

---

## Inputs & Outputs

### Inputs
1. **Learner Profile**: User target role, experience level, declared/inferred skills with confidence, and weekly available learning hours (`weekly_learning_hours`).
2. **Skill Gap Analysis**: Classified skills (`strong`, `meets_requirement`, `needs_improvement`, `missing`), deterministic priorities (`high`, `medium`, `low`), and preserved evidence.
3. **Role Requirements**: Benchmark skill list, proficiencies, and importance weights.
4. **Skill Prerequisites**: Dependency graph mappings defining skill order constraints.

### Outputs
A structured `LearningPlanResponse` containing:
- `plan_id`: Unique identifier (e.g. `plan_49c113f74089`).
- `user_id`: Target learner ID.
- `target_role`: Benchmark target role name.
- `summary`: Executive summary of the personalized roadmap.
- `total_estimated_hours`: Aggregated estimated study hours.
- `duration_weeks`: Calculated total weeks.
- `version`: Learning plan schema version (`version = 1`).
- `modules`: List of `LearningModule` items with assigned `week_number`, `prerequisites`, and `tasks` (`learn`, `practice`, `project`, `review`).

---

## Core Planning Logic & Rules

1. **Skipping Satisfied Skills**: Skills classified as `strong` or `meets_requirement` are skipped from active study modules to avoid redundant learning.
2. **Prerequisite Ordering**: Topological sorting ensures prerequisite skills (e.g., `Statistics` before `Machine Learning`, `Machine Learning` before `Deep Learning`) always precede dependent skills.
3. **Deterministic Priorities**: Active gaps are chunked in order of topological dependency, gap priority, and role importance.
4. **Weekly Chunking & Time Personalization**: Module workloads are chunked into sequential weeks based on the learner's available `weekly_learning_hours`.
5. **Task Categorization**: Each module generates manageable daily tasks using foundational task types (`learn`, `practice`, `project`, `review`).

---

## Storage & API Integration

- **MongoDB Collection**: `learning_plans` collection with `user_id` unique index and `plan_id` index.
- **Error Handling**: Missing profiles or missing skill gap analyses trigger a clear `HTTP 400 Bad Request`. Database connection failures return `HTTP 503 Service Unavailable`.
- **Endpoints**:
  - `POST /api/v1/plans/generate`: Generates personalized learning plan.
  - `GET /api/v1/plans`: Returns current/latest stored plan.
  - `GET /api/v1/plans/{plan_id}`: Returns specific plan by ID.
