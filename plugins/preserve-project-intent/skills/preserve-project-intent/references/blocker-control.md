# Blocker Control

Use this reference when a problem discovered during a larger project threatens to become a new project of its own.

## Classification

### BLOCKING

The main line cannot continue safely or correctly without resolution. Resolve it to the minimum sufficient condition.

Examples: production corruption risk, missing authority, an invalid core assumption, or a failing acceptance condition required by the current milestone.

### REQUIRED

Not independently blocking, but necessary to satisfy the already-agreed acceptance condition. Keep it inside the active task.

### ADJACENT

Relevant and potentially valuable, but not necessary to resume or complete the current milestone. Record it with enough context to revisit; do not silently implement it.

### OVERREACH

Adds generalized prevention, theoretical completeness, broad refactoring, or verification disproportionate to the observed problem. Simplify or stop unless the user explicitly chooses the expanded investment.

## Minimum-sufficient blocker contract

Before work begins, capture:

```yaml
problem: <observed condition>
blocks: <specific main-line work>
minimum_resolution: <smallest sufficient outcome>
evidence_to_clear:
  - <observable check>
return_point: <exact main-line work>
non_goals:
  - <plausible expansion excluded from this fix>
```

Avoid defining the resolution as “prevent every possible recurrence.” Prefer a control proportional to the observed risk and the project's existing architecture.

## Scope-expansion checkpoint

Pause and reclassify before proceeding when:

- a fix needs a new framework, subsystem, or generalized analyzer;
- review findings concern the corrective machinery rather than the original product risk;
- a finding is derived from another derived finding;
- the proposed verification surface grows faster than the original change;
- an implementation is being hardened before its necessity is re-evaluated;
- removing the corrective mechanism would be simpler and still satisfy the minimum resolution.

At the checkpoint, answer:

1. What main-line work remains blocked?
2. What evidence makes this additional work necessary?
3. Is there a simpler sufficient control?
4. What is the cost of parking it?
5. Does it change the user's agreed scope?

Proceed only when the answers support necessity. Otherwise simplify, park, or request a deliberate scope change.

## Review-loop control

A review finding is evidence about a change, not automatic authority to expand the project. For each finding:

- map it to the blocker contract or milestone acceptance condition;
- fix it if the mapping is direct;
- park it if valid but adjacent;
- reject or simplify it if it only perfects unnecessary corrective machinery;
- revisit whether the machinery should exist when repeated findings target its complexity.

Do not count review rounds as progress toward the mission.

## Closure and return

When the evidence-to-clear checks pass:

1. set the blocker to `CLEARED`;
2. state which task or milestone remains incomplete;
3. restore the return point as the active task;
4. make the next action advance that task;
5. keep adjacent findings parked unless separately prioritized.

Correct example:

```text
BLOCKER_CLEARED
MILESTONE_IN_PROGRESS
Completed now: the production execution path is constrained as required.
Still not completed: the knowledge-depth milestone.
Return point: C1-N23 reference and evidence enrichment.
```
