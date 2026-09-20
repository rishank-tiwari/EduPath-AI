# Resource Agent Documentation (Task 1.4)

## Purpose
The **Resource Agent** (`ACT` phase) discovers, ranks, and curates learning resources (documentation, courses, videos, articles, projects) matching specific learning tasks and skill gaps.

It answers:
> *"What authoritative learning materials should this learner use to study this topic?"*

---

## Inputs & Outputs

### Inputs
- `task_id`: Unique learning task identifier.
- `skill_name`: Target skill name (e.g. `"Probability"`, `"Statistics"`, `"FastAPI"`).
- `difficulty`: Desired difficulty level (`"beginner"`, `"intermediate"`, `"advanced"`).
- `user_id`: Learner identifier.

### Outputs
A structured `ResourceRecommendationResponse` containing:
- `task_id`: Task ID.
- `skill_name`: Target skill.
- `topic`: Learning topic title.
- `resources`: List of `LearningResource` items with `title`, `description`, `resource_type`, `url`, `difficulty`, `estimated_minutes`, and `source`.

---

## Resource Selection Rules
1. **Authoritative Sources**: Uses curated, verified documentation and tutorial URLs (e.g., Python Official Docs, PyTorch Tutorials, Scikit-Learn, FastAPI Docs, Khan Academy).
2. **No Fake URLs**: If no direct link exists for a rare topic, an explicit placeholder status is used instead of a synthetic link.
3. **Difficulty Matching**: Sorts curated resources matching the learner's specified difficulty level (`beginner`, `intermediate`, `advanced`).
