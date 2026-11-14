---
name: performance-engineering
description: "Use when planning or improving execution efficiency, responsiveness, latency, throughput, resource use, or cost for a performance-sensitive feature or an observed slowdown across web, native apps, services, data, or AI. Diagnose workload bottlenecks and verify gains. Not for routine edits, speculative micro-optimization, generic architecture decisions, or patch review."
---

# Performance Engineering

## Purpose

Deliver software that does the necessary work at the right time, at the appropriate execution layer,
within the user's performance and quality constraints. A passing benchmark, fast initial load, or
simple-looking algorithm is not sufficient evidence of good user experience.

**Core principle: remove avoidable work before accelerating work that must remain.** Do not confuse
this with a rule to cache everything, defer everything, or minimize component count. Each technique
must preserve correctness, security, consistency, accessibility, and the user-visible contract.

This skill owns **performance diagnosis, measurement, improvement, and regression proof**. For a
consequential choice of domains, services or state authority, `architecture-engineering` owns the
overall design; its performance reference supports architectural decisions. For an unexplained
failure with nonperformance symptoms, `systematic-debugging` owns causal investigation. TDD owns
behavior changes; `change-verification` owns requested PR/readiness reviews. Do not load companion
skills automatically.

## Select the Right Mode

| Request | Response |
| --- | --- |
| "Build this fast from the start" for a consequential or performance-sensitive feature | Establish critical paths and plausible workload risks; choose low-overhead execution; plan relevant evidence |
| "It feels laggy, despite excellent scores" | Reproduce the experienced interaction; trace rendering, scheduling and resource contention, not only load scores |
| "Find why this API is slow" | Establish workload and causality; measure the actual query, network, compute and queueing paths |
| "Make this implementation more efficient" | Preserve semantics; compare measured work and end-to-end outcome before accepting an optimization |
| "Prevent future performance regressions" | Select repeatable, representative measurements and appropriate review/CI/field thresholds |
| Routine local edit with no meaningful performance implication | Do not perform a performance audit or load this skill solely because "efficient" appears in generic defaults |

A greenfield project lacks a measured baseline. Estimate workload drivers, inspect platform
semantics, and choose a small validation slice—**do not pretend an estimate is a benchmark**. In a
brownfield project, prefer representative field observations and a comparable baseline at the actual
running revision. If a user demands a particular library, animation, appearance or runtime behavior,
treat it as a requirement; optimize its implementation rather than silently removing it.

**Plan-only requests authorize investigation and a verification plan, not code edits or deployment.**
For implementation requests, improve the code only after enough evidence identifies the work at issue.

## Workflow

### 1. Define the Observable Performance Contract

Name the user/system action, critical path, target environment, and failure that matters:
- Time to first useful view, interaction response, animation smoothness, job completion, query
  latency, throughput, memory growth, energy, or operating cost are **different** objectives.
- Include device class, browser/runtime version, network condition, dataset, user/session state,
  concurrency, and cold/warm behavior **only where they change the result**.
- Use stated budgets and product requirements. If absent, distinguish provisional targets from facts;
  do not invent universal thresholds or demand 100/100 tooling scores.
- Preserve visuals, smooth scrolling, accessibility, data correctness, security and product behavior
  even when a shortcut makes one metric appear better.

### 2. Model Where Work Actually Happens

Trace **trigger → scheduling → computation/I/O → state change → presentation or effect**. Account for
repetition, invalidation and cancellation. Determine whether work is:
- necessary and on the critical path;
- necessary but scheduled too early or at the wrong layer;
- duplicated, obsolete, unbounded, or performed on unaffected inputs;
- waiting for CPU, memory/GC, disk, DB locks, network, a pool, GPU, rendering or another dependency.

Check real execution and resource lifecycle: listeners, timers, jobs, connections, subscriptions,
caches, buffers and background work. A static page can still block the browser main thread; an async
function can still run long synchronous computations.

### 3. Obtain Discriminating Evidence

Use the lowest-cost measurement that can decide the question. When profiling, record build/revision,
environment, scenario, sample count and major variability. Distinguish lab/synthetic checks from
real-user experience, microbenchmarks from end-to-end performance, averages from tails, and
initialization from steady-state or extended sessions.

Investigate the **actual critical path**, not merely the largest source file or most visually
expensive component. A performance report should identify the observed bottleneck, evidence for it,
competing explanations considered and any remaining uncertainty.

### 4. Choose the Appropriate Remedy

Consider these interventions **as hypotheses**, in a context-specific order:

- **Eliminate:** unused work, needless render passes, redundant requests, N+1 lookups, repeated
  invariant calculations, stale work and excessive data movement.
- **Localize:** recompute only on real input changes; co-locate data/decisions when useful; avoid
  unnecessary cross-boundary communication and synchronization.
- **Schedule:** keep latency-sensitive interactions responsive; delay noncritical work where doing
  so will not create later jank, starvation or correctness issues. Yield/cooperate when supported.
- **Bound:** apply realistic concurrency, deadlines, cancellation, backpressure, memory and queue
  limits at the owner. Parallelism without capacity analysis may amplify contention or costs.
- **Reuse or stream:** cache or batch only with a correct validity/invalidation contract; stream when
  partial availability improves the actual user flow and the transport supports it.
- **Scale or change topology:** when real constraints justify new processes, workers, infrastructure
  or algorithmic changes, account for operations, compatibility, failure windows and cost.

Some apparently "extra" work is required for security, reliability, accessibility or fidelity.
Do not optimize it away. Do not turn every item above into a task list.

### 5. Verify the Real Outcome and Stop

Check behavioral and protected invariants through representative paths. Compare before/after using
the same workload and conditions or explain why comparison is limited. Test interactions, slower
devices, prolonged sessions, burst/cold paths or failure conditions when they matter. A useful
optimization must improve the intended outcome without introducing worse tails, jank, leaks, stale
data, broken keyboard navigation or unacceptable costs elsewhere.

Close with **measured result, test conditions, tradeoffs and residual risks**. If no measurement was
possible, clearly label the proposed improvement as unverified. Stop when the requirement is met and
the added complexity no longer earns its cost; avoid optimizing for an arbitrary perfect score.

## Conditional References

Read **only** the references relevant to the workload and uncertainty; do not read them all:

- [Measurement and Performance Regressions](references/measurement-and-regressions.md) — when
  choosing metrics, profiling, comparing results, setting budgets or protecting performance over time.
- [Browser Rendering and Interaction](references/browser-rendering-and-interaction.md) — when
  diagnosing or building web UI, scroll/animation, responsiveness, hydration and browser lifecycle.
  Consult up-to-date platform guidance for actual browser support.
- [Native Application Responsiveness](references/native-app-responsiveness.md) — when working with
  mobile, desktop or embedded interactive runtimes, startup, frames, CPU, memory and energy.
- [Services and Data Paths](references/services-and-data-paths.md) — when latency, database access,
  service fan-out, queuing, throughput and resource contention matter.
- [AI, Batch and Background Work](references/ai-batch-and-background-work.md) — when optimizing
  inference, retrieval, embeddings, batch processing, durable jobs or expensive asynchronous work.
- [Worked Performance Cases](references/performance-casebook.md) — when a complex plan benefits
  from worked evidence, counterexamples and validation maps; do not copy example architectures.

## Decision Examples

- **A page scores well on Lighthouse but scrolls badly:** profile actual scroll interactions, frame
  rendering, layout and long tasks on the affected device. Do not remove required motion or assume
  image weight explains runtime jank.
- **A request becomes slow as records grow:** inspect query count, data shape, serialization and
  concurrency under representative input. Do not add a cache without evidence and invalidation rules.
- **A background AI job costs too much:** identify repeated retrieval, unchanged embeddings,
  unnecessary tokens or duplicate work. A cache is justified only if identity, freshness and
  authorization remain correct.

**A good agent prevents foreseeable waste without claiming every performance issue can be predicted
or eliminated before a system is measured in use.**
