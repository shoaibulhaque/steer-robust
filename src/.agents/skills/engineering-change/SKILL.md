---
name: engineering-change
description: Fix, implement, refactor, migrate or optimize code, including coordinated multi-repository changes. Skip prose-only edits and product tours.
---

# Engineering change

Before editing code, read [principles](../../../Steer-robust/principles.md) and
[design](../../../Steer-robust/design.md). They own cause, simplicity, domain modeling and reader load.
Do not substitute a summary or this entrypoint for those guides.
Use an equivalent project-owned workflow when present, retaining applicable engineering guarantees.

Establish the requested behavior, first violated contract, owner and important preservation case.
Inspect actual consumers and the project's scoped rules before selecting a repair.
For a bug, seek a discriminating reproduction before editing; explain a genuine blocker.
Before adding tests, load [change-verification](../change-verification/SKILL.md) and its test-value guidance.
Choose the best justified coherent repair; preserve error, security, integration and operational guarantees.
An imagined future caller does not justify a framework; a needed abstraction must not be removed to save lines.

## Load only relevant detail

- Repeated edits, bulk work or tool decisions: read [efficiency](../../../Steer-robust/efficiency.md).
  Build or reuse a deterministic lever when it materially improves repetition or verification;
  qualify a representative unit, scope changes and verify safe reruns. A simple edit needs no new script.
- State, retries, lifecycle or concurrency: read [state/failure](../../../Steer-robust/state-and-failure.md).
  When ordering creates multiple plausible executions, load [statechart](../statechart/SKILL.md).
- External contracts, data/version transitions or multiple repos: read
  [evolution](../../../Steer-robust/evolution.md). Inspect each repo's instructions and tests separately;
  coordinate producer and consumers, compatibility and rollout. One repo's green checks prove only its boundary.
- Trust, authorization or private inputs: read [security](../../../Steer-robust/security.md).
- Scale or optimization: read [performance](../../../Steer-robust/performance.md).
- A requested review: read [evaluation](../../../Steer-robust/evaluation.md).

## Verify and finish

Load [change-verification](../change-verification/SKILL.md) for proof selection and required gates.
Pass existing context instead of restarting discovery. Follow its runtime handoff when necessary.
Inspect the final diff for cause, preserved behavior, unnecessary layers/state and unrelated work.
Do not change code simply to meet a metric. Use the optional analyzer guide linked from design when warranted.
Report concrete results and remaining gaps. No automatic commits, pushes, dependencies or extra scope.
