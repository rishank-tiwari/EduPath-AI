# Adaptation Agent Documentation (Task 1.5)

## Purpose
The **Adaptation Agent** (`ADAPT` phase) evaluates learner progress summaries against the current Learning Plan, applies deterministic adaptation rules, modifies learning tasks, increments the plan version ($v1 \rightarrow v2$), and sets a new recommended next step.

It answers:
> *"What should change in the learner's plan because of their performance?"*

---

## Inputs & Outputs

### Inputs
- `plan_data`: Current `LearningPlanResponse` dictionary.
- `progress_summary`: `ProgressSummary` dictionary for the skill/topic being evaluated.

### Outputs
- `decision`: An `AdaptationDecision` model detailing the action, reason, previous status, and version transition.
- `updated_plan`: The modified Learning Plan with incremented version number.

---

## Adaptation Rules & Actions

1. **`strong`** ($\ge 90\%$) $\rightarrow$ **`move_forward`**:
   - *Reason*: Learner demonstrated strong performance. Advancing directly to next milestone without redundant review.
2. **`on_track`** ($70\% - 89\%$) $\rightarrow$ **`continue`**:
   - *Reason*: Learner is on track. Continuing planned roadmap.
3. **`needs_review`** ($50\% - 69\%$) $\rightarrow$ **`add_practice`**:
   - *Reason*: Learner score indicates room for improvement. Prepends/appends targeted practice task to module.
4. **`struggling`** ($< 50\%$) $\rightarrow$ **`review`**:
   - *Reason*: Score fell below requirement threshold. Inserts a high-priority review task and a re-test task into the module, incrementing plan version ($v1 \rightarrow v2$).

---

## Plan Versioning & History Preservation
- The Adaptation Agent **never destroys** historical plan versions. Previous plan snapshots remain accessible in MongoDB.
- Every adaptation event is logged in the `adaptation_events` collection for full auditability.

---

## Storage & API Integration
- **MongoDB Collection**: `adaptation_events` collection with index on `user_id`.
- **Endpoints**:
  - `POST /api/v1/adaptation/analyze`: Analyzes performance and triggers plan adaptation.
  - `GET /api/v1/adaptation/history`: Retrieves previous adaptation decision history.
