# Handoff Protocol

A handoff transfers project state, not merely conversation history. Produce both the canonical handoff and a bootstrap prompt.

## Deliverable 1: canonical handoff

Use this order:

1. **Canonical State** — the YAML block from `project-state-schema.md`.
2. **Mission and boundaries** — purpose, success condition, and non-goals.
3. **Domain model and terminology** — definitions the next agent must not reinterpret.
4. **Current milestone and quantitative position**.
5. **Completed work and evidence**.
6. **Explicitly incomplete work**.
7. **Blockers and corrective work** — distinguish open from cleared.
8. **Return point and next main-line action**.
9. **Agreed workflow and acceptance conditions**.
10. **Repositories, authoritative files, environments, and operation boundaries**.
11. **Decisions, rejected options, unresolved decisions, and parked findings**.
12. **Relevant history** — only after current state is clear.
13. **Resume verification instructions**.

Be detailed enough for a capable agent with no prior conversation. Do not copy every command log when a verified outcome and authoritative artifact are enough. Preserve exact identifiers, metrics, statuses, and constraints when they affect decisions.

## Deliverable 2: bootstrap prompt

The prompt should identify the project and handoff, explicitly invoke the skill when supported, prohibit mutations during alignment, and request a structured understanding check.

Template:

```text
This is a continuation of <PROJECT>.

Read the attached or provided <HANDOFF_FILE> completely. Use
$preserve-project-intent and treat its Canonical State, Mission, Current
Milestone, completion boundaries, Return Point, and operation constraints as
the formal starting state for this session.

Do not promote the most recently discussed blocker or corrective work into the
project mission. Do not treat task or blocker completion as milestone or mission
completion.

Before making any code, data, production, document, Git, or external changes,
report:

1. Mission and success condition
2. Current milestone and metric
3. Completed scope
4. Explicitly incomplete scope
5. Blocker status
6. Return Point
7. First main-line action
8. Operation and authorization boundaries

Report contradictions rather than silently resolving them. End with:

HANDOFF_ALIGNED_WITH_ARTIFACTS, HANDOFF_INTERNALLY_CONSISTENT_ONLY,
or HANDOFF_CONFLICT_FOUND
MISSION_<STATUS>
MILESTONE_<STATUS>
RESUME_FROM_<RETURN_POINT>
```

If the target environment does not recognize `$skill-name` invocation syntax, replace that phrase with: “Follow the preserve-project-intent protocol included in the handoff/package.” Keep the same alignment requirements.

## Handoff validation

Before delivering the handoff, verify:

- Mission is an outcome, not the latest task.
- Milestone has a success condition and current status.
- Quantitative progress is current and labeled.
- Local completion is not presented as project completion.
- `not_completed` is explicit.
- Every cleared blocker has a return point.
- The next action advances or restores the milestone.
- Non-goals prevent the known plausible drift.
- Operational permissions are not enlarged by the handoff.
- The bootstrap prompt references the actual handoff name.

## Resume validation

The receiving agent reads the entire handoff, then compares the Canonical State with the detailed sections. It must not rely on the last section or the longest incident narrative.

If a named authoritative artifact is accessible and read-only inspection is authorized, perform at least one inexpensive mechanical comparison before claiming artifact alignment. Choose a check relevant to the claimed state, such as the current commit, existence or hash of a named file, PR merge state, snapshot identifier, or canonical metric. Record what was checked and the observed value.

Use exactly one evidence level:

- `HANDOFF_ALIGNED_WITH_ARTIFACTS` — internal comparison passed and at least one authoritative artifact check passed.
- `HANDOFF_INTERNALLY_CONSISTENT_ONLY` — the handoff agrees with itself, but artifacts were unavailable, unnamed, or inspection was not authorized.
- `HANDOFF_CONFLICT_FOUND` — a contradiction affects the next action, scope, completion status, metric, or safety boundary.

Never use an unqualified `HANDOFF_ALIGNED` claim. Do not perform a mutation merely to verify a handoff.

Use `HANDOFF_CONFLICT_FOUND` when a contradiction would change the next action, scope, completion status, or safety boundary. Describe the conflict and wait for resolution when necessary. Minor wording differences that do not affect action may be noted without blocking.

After alignment, continue from `return_point` or `next_action`. Do not reopen a cleared blocker without new evidence.

## Cross-session and cross-agent use

The skill contains stable behavior; the handoff contains dynamic project state. Transfer both concepts across GPT, Codex, Claude Code, or another agent environment. A platform-specific skill installation may make the behavior automatic, but the handoff remains the canonical carrier of project-specific facts.

When a file attachment is unavailable, the full handoff may be pasted after the bootstrap prompt. Do not reduce it to the bootstrap prompt alone for a complex project.
