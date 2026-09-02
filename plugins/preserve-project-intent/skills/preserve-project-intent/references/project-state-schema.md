# Project State Schema

Use this schema when initializing a continuing project, recording a material state transition, or preparing a handoff. Omit fields that truly do not apply; do not replace known values with vague prose.

## Canonical state block

Place this block near the beginning of a handoff so current truth is encountered before detailed history.

```yaml
state_version: 1
updated_at: YYYY-MM-DD

project:
  name: <project name>
  canonical_sources:
    - <authoritative file, repository, system, or decision record>

mission:
  statement: <durable value or outcome>
  success_condition: <evidence required for mission completion>
  status: NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE
  non_goals:
    - <plausible but excluded objective>

current_milestone:
  id: <stable identifier when one exists>
  statement: <measurable result currently pursued>
  success_condition: <evidence required for milestone completion>
  status: NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE
  metrics:
    <metric_name>: <current / target or current value>

active_task:
  id: <stable identifier when one exists>
  statement: <bounded current work>
  status: NOT_STARTED | IN_PROGRESS | BLOCKED | COMPLETE

blocker:
  id: <identifier or null>
  statement: <condition preventing continuation>
  blocks: <specific task or milestone activity>
  minimum_resolution: <smallest sufficient outcome>
  evidence_to_clear:
    - <observable evidence>
  status: NONE | OPEN | CLEARED
  non_goals:
    - <hardening or generalization not required to clear it>

return_point:
  id: <task or decision identifier>
  statement: <exact main-line work to resume>

completed:
  - <material completed result with evidence or metric>

not_completed:
  - <important work that a reader might otherwise assume is complete>

decisions:
  - <decision and short rationale>

parked:
  - <adjacent finding and why it is not current>

next_action:
  statement: <first action that advances or restores the current milestone>
  authorization_boundary: <read-only, draft-only, implement, production constraints, etc.>
```

## Rules

- Preserve the user's language for the mission when it is clear.
- Give mission and milestone distinct success conditions.
- Record metrics with numerator, denominator, unit, and timestamp when relevant.
- `completed` records outcomes, not effort expended.
- `not_completed` must include the higher-level work left open after a task or blocker closes.
- A cleared blocker may remain in the state for continuity, but its return point becomes active.
- History must not overwrite current truth. When facts changed, state the current value and put the old value in the history section.
- Do not place credentials, tokens, or unnecessary personal data in a handoff.

## Compact checkpoint

During an active session, a shorter checkpoint is acceptable:

```text
Mission: <statement> — <status>
Milestone: <statement> — <status and metric>
Active task: <statement> — <status>
Blocker: <statement or none> — <status>
Return point: <statement>
Completed now: <outcome>
Still not completed: <higher-level open work>
Next main-line action: <action>
```
