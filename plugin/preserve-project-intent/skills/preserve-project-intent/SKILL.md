---
name: preserve-project-intent
description: Preserve the primary mission, current milestone, completion boundary, and return point across long-running projects, nested blockers, implementation gates, reviews, and session handoffs. Use when starting or resuming multi-session work, handling a problem discovered inside a larger project, deciding whether local completion means the milestone or mission is complete, or preparing/consuming a detailed handoff. Do not use for isolated one-step tasks with no continuing project state.
---

# Preserve Project Intent

Keep local work subordinate to the value the project exists to create. A blocker may interrupt the main line; it must not silently replace it.

## Establish the project stack

Maintain these levels separately:

1. **Mission** — the durable value or outcome.
2. **Milestone** — the measurable result currently pursued.
3. **Active task** — the bounded work now being performed.
4. **Blocker** — a condition that prevents safe or correct continuation.
5. **Return point** — the exact task or decision to resume after the blocker clears.

Never infer that completing a lower level completes a higher level. If the available context does not establish the stack, reconstruct it from the user's stated intent and authoritative project material before substantial work. Ask only when a missing choice would materially change the result.

For a new or materially re-scoped project, read [Project state schema](references/project-state-schema.md).

## Select the operating mode

- **INIT** — establish the stack, success conditions, metrics, non-goals, and authoritative state.
- **CONTROL** — execute or supervise work while classifying discoveries and preventing scope capture.
- **HANDOFF** — produce the canonical handoff and the next-session bootstrap prompt.
- **RESUME** — consume a handoff, verify alignment, and restart from its return point.

Use the lightest mode that fits. Do not burden ordinary short tasks with project ceremony.

## Control the active work

Before entering a blocker, record:

- what it prevents;
- the minimum sufficient resolution;
- the return point;
- explicit non-goals;
- the evidence that will show it is cleared.

Classify new findings as `BLOCKING`, `REQUIRED`, `ADJACENT`, or `OVERREACH`. Work on `BLOCKING` and `REQUIRED` findings within the current scope. Record `ADJACENT` findings for later. Decline or simplify `OVERREACH` unless the user deliberately expands scope.

Trigger a scope-expansion checkpoint when a proposed response to a finding:

- changes the milestone or its acceptance condition;
- introduces a new subsystem or generalized control not required by the original blocker;
- produces a second-order finding inside an already derived task;
- materially increases implementation or verification relative to the blocked main-line work; or
- optimizes theoretical completeness instead of restoring safe progress.

At the checkpoint, choose among: continue as necessary, use a simpler sufficient fix, park the finding, or ask the user to approve a genuine scope change. Read [Blocker control](references/blocker-control.md) when blockers, nested findings, hardening, review loops, or broad corrective work are involved.

## Preserve completion semantics

Use these statuses precisely:

- `TASK_COMPLETE`
- `BLOCKER_CLEARED`
- `MILESTONE_COMPLETE`
- `MISSION_COMPLETE`

Also state the still-open higher levels. Do not use unqualified words such as “project complete,” “finished,” or “closed” when only a task, gate, review, or blocker is complete.

After `BLOCKER_CLEARED`, make the return point the default next action. Do not propose another adjacent governance, refactor, review, or hardening task ahead of it unless new evidence shows that the main line remains blocked.

## Keep state current

After a material gate, decision, blocker transition, or measurable result, update the compact canonical state:

- mission and milestone status;
- current metric or evidence;
- completed and explicitly not completed work;
- active blocker and its status;
- return point;
- next main-line action;
- non-goals and parked findings when changed.

Treat a roadmap or handoff as current state, not a chronological work diary. Put current truth before history.

## HANDOFF mode

Produce two distinct deliverables:

1. a detailed canonical handoff in Markdown;
2. a short bootstrap prompt to paste into the next session with the handoff attached or otherwise available.

The handoff must be sufficiently self-contained for a new agent with no conversational history. It must preserve important domain definitions, quantitative state, decisions, operational boundaries, authoritative artifacts, completed and incomplete work, the return point, and the next action. The bootstrap prompt instructs the new agent how to consume that state; it is not a substitute for it.

Read and follow [Handoff protocol](references/handoff-protocol.md). Use the canonical block from [Project state schema](references/project-state-schema.md).

## RESUME mode

Read the handoff completely before changing code, data, production, documents, or external state. Then:

1. extract the canonical state;
2. compare it with the detailed body and any named authoritative artifacts available;
3. separate mission, milestone, task, blocker, and return point;
4. report contradictions instead of silently resolving them;
5. state what is complete and what is not;
6. identify the first main-line action;
7. wait for alignment when the user requested a read-only handoff check.

Use a compact alignment result such as:

```text
HANDOFF_ALIGNED
MISSION_IN_PROGRESS
MILESTONE_IN_PROGRESS
RESUME_FROM_<RETURN_POINT>
```

Do not restart a cleared blocker merely because its history is detailed. Do not reinterpret the latest incident as the project's purpose.

## Reporting invariant

For material progress or closure, state:

- **Completed now**
- **Still not completed**
- **Mission / milestone status**
- **Return point or next main-line action**

Keep the main-line metric visible when one exists. The amount of discussion devoted to a blocker must not determine its importance in the project hierarchy.
