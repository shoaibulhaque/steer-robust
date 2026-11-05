---
name: statechart
description: Model and check ordering-sensitive workflows, protocols, concurrency or lifecycle transitions with TLA+/TLC and Mermaid counterexamples. Skip ordinary stateless changes.
---

# Statechart

Read [state/failure](../../../Steer-robust/state-and-failure.md) and
[model-checking instructions](references/model-checking.md) before modeling.
Use this when competing transitions or unknown outcomes make a sequence consequential, not for every change.
Prefer an existing repository-owned formal specification and tooling.

Translate actual code/contract into bounded states, named actions, initial conditions and invariants.
State omissions and connect each action/variable to its implementation owner.
Keep rules fixed while repairing the transition; never weaken an invariant to make a run green.
Use an explicit terminal stutter only for legitimate completed states, not to hide deadlocks.

Check with TLC when Java and the TLC jar are available; dependencies remain optional and are never installed
by this skill. The bundled wrapper records TLC output and renders its counterexample as Mermaid.
Missing dependencies, timeout, parse failure and incomplete exploration are blocked proof, not passes.
For multiple invariants, check separately to expose each failure; retain each original configuration.

Use one-worker BFS safety checking, or the documented iterative-deepening fallback when sandboxed TLC
cannot open its RMI listener. Retain failed attempts; never bypass sandbox controls.
Both modes search increasing safety depths; report the actual mode and finite model limits.
Do not claim shortest liveness paths, shortest real incidents or proof beyond the model's bounds.
Show the Mermaid trace, invariant, action sequence, limits and exact rerun command to the reader.
The trace is the counterexample path, not a complete state graph or an automatically validated abstraction.
Replay each relevant failing sequence against real code as regression proof; correct a mismatched model
before drawing conclusions. Recheck both model and implementation after a repair.
