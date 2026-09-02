# Project State Schema

Use this schema when initializing a continuing project, recording a material state transition, or preparing a handoff. Omit fields that truly do not apply; do not replace known values with vague prose.

## Canonical state block

Place this block near the beginning of a handoff so current truth is encountered before detailed history.

```yaml
state_version: 1
updated_at: YYYY-MM-DD

persistence:
  enabled: false
  state_file: <user-approved path or null>
  update_on:
    - milestone_change
    - blocker_opened
    - blocker_cleared
    - return_point_change
    - session_handoff

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
  contract_frozen_at: <timestamp or null>
  approved_revisions:
    - <old value, new value, evidence, scope effect, and user approval>
  depth1_solution: <current corrective approach or null>
  depth2_findings:
    - id: <stable identifier>
      summary: <finding produced by the current Depth 1 solution>
      status: OPEN | RESOLVED | PARKED
      disposition: <action or decision>

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
- Derive the breadth count from `depth2_findings`; do not store a separate count. Keep resolved and parked findings because accumulated breadth is the signal. If the Depth 1 solution is replaced, preserve the old findings in history or decisions before starting the new solution's list.
- History must not overwrite current truth. When facts changed, state the current value and put the old value in the history section.
- Do not place credentials, tokens, or unnecessary personal data in a handoff.

## Optional persistent state

Persistence is opt-in. During INIT, the user may approve a project-local state path such as `.preserve-intent/state.yaml` or another location appropriate to the repository. If no path is approved, keep `enabled: false` and use the handoff as the state carrier.

When enabled:

- update only on the listed material transitions, not after every command;
- keep current truth and compact evidence, not a chronological log;
- compare the existing state before writing and report conflicts rather than overwriting them;
- treat a write as a file mutation requiring the task's authorization;
- never infer permission to commit, push, deploy, or mutate external state;
- let HANDOFF point to the current state file and add the detailed context needed by a new agent.

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
