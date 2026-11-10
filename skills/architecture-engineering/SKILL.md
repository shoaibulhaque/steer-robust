---
name: architecture-engineering
description: "Use for greenfield system design, substantial brownfield features, integrations or migrations, consequential architecture decisions, or implementation at risk of cross-module coupling. Produce justified plans or guide boundaries during coding. Not for small local edits, pure refactoring, root-cause investigation, or patch review."
---

# Architecture Engineering

## Overview

Choose the simplest defensible design for the actual requirements, then make it possible to build,
verify, operate, and change. Architecture includes the cost of understanding a system, not just its
runtime topology.

**Core principle:** make responsibilities and invariants understandable and enforceable. Choose boundaries,
coordination, abstractions and infrastructure for the real guarantees they provide and costs they impose.
Neither fewer components nor more components is inherently better.

**Decision authority:** requirements and observed system behavior govern the design. Patterns, diagrams
and examples here are hypotheses and probes, not prescribed architectures. Distributed services,
replicated state, specialized infrastructure or a direct cutover can be right when the constraints
justify them. Explain the evidence, rather than forcing an example's outcome.

## Choose the Work

| Request | Appropriate response |
| --- | --- |
| Plan a new system or substantial feature | Produce an evidence-grounded architecture and an executable sequence; do not implement |
| Plan an integration, replacement, or migration | Establish existing contracts, old/new coexistence, cutover and verification before recommending a path |
| Decide or evaluate an interface, boundary, or architecture option | Resolve the consequential decision and its rationale; avoid an unnecessary full project plan |
| Implement a cross-module feature or fix | Follow existing owners and contracts; avoid introducing scattered rules, hidden coordination, or surplus abstractions |

An isolated edit with an established owner does not need this workflow. Pure behavior-preserving
restructuring belongs to `refactoring`; unexplained failures to `systematic-debugging`; an explicitly
requested patch review to `change-verification`; and specialist security investigation to
`security-engineering`. Preserve the repository's TDD and verification practices during implementation.
Do not load another skill simply because it is named here.

**Plan-only means no implementation.** Inspect relevant evidence and propose changes, but do not edit
files, run a migration, or claim unperformed tests. For an implementation request, do not substitute a
plan for working code.

Choose **depth** independently of the project's age: a small addition to a mature application may
need only a change map, while a new system that handles money or sensitive data can require careful
failure and trust modeling. Spend the most analysis on decisions that are uncertain, consequential,
and expensive to reverse; use an established, reversible choice without prolonged comparison.

## Method

### 1. Establish the Architectural Drivers

Identify the desired outcome, indispensable behavior, constraints, stakeholders or consumers, and
acceptance evidence. Distinguish explicit requirements, observed facts, and assumptions. Ask for a
consequential missing decision only when evidence cannot settle it; otherwise proceed with a labeled
assumption.

Translate important quality attributes into scenarios: workload and latency, failure and recovery,
data consistency, privacy and authorization, deployability, operating cost, and ease of change. Select
those that could alter this design; do not invent targets or demand enterprise controls by default.

Define an important scenario as **condition → action or failure → required observable outcome**.
For example, "if the worker dies after committing an external effect but before acknowledgment,
recovery must not create a second billable effect." Identify who owns the guarantee and what evidence
could falsify it. For material uncertainty, distinguish a known fact from a hypothesis and state which
decision would change when the hypothesis is tested.

### 2. Work from the Actual Context

- **Greenfield:** model domain concepts and workflows, data authority, trust boundaries, and the first
  useful end-to-end slice. Choose technologies from constraints, not fashion.
- **Brownfield:** trace the current entry points, domain rules, consumers, stored state, tests, and
  deployed behavior. Separate required contracts from incidental legacy implementation.
- **Hybrid:** map both existing and proposed components, the authoritative writer and data model,
  supported mixed versions, migration path, and removal of the old path.

Inspect only the area and dependencies that can change the decision. If a working pattern meets the
contract, prefer extending it over building a parallel solution.

### 3. Construct and Challenge a Candidate

Construct a viable design from the drivers, not a preferred topology. Avoid complexity without material
benefit, but do not reject necessary complexity for aesthetic simplicity. Make explicit which component
enforces each invariant, how consumers interact, where authoritative state lives, and how important
failures are observed or recovered.

Compare credible alternatives **when a real choice remains**. A simpler alternative is useful only if
it can plausibly satisfy the guarantees. Where a fixed contract or observed constraint settles the
choice, verify it instead of inventing an alternative. Evaluate feasibility, growth, compatibility,
operations, reversibility and failure windows proportionately. Accept necessary stateful components.

Inspect the **boundary where the design might fail**, not merely its happy-path diagram: an
acknowledgment may be lost after a remote effect; concurrent actors may both believe they own work;
a rolling deployment may mix old and new readers; a cache may serve stale authorization. Do not
apply these examples universally—select only the realistic failure windows for the task.

Use measurements, a narrow prototype, a contract check, or documentation when evidence could change
the choice. A proposed experiment should name representative inputs, a success criterion, and the
decision that follows each outcome. Do not present estimates, mock behavior, or an unrun test as
measured feasibility.

Check change locality: can the same rule change in one authoritative place? Can an unrelated consumer
evolve without forcing other consumers to change? Many changed files are acceptable when each layer
has a distinct job; duplicated decisions and hidden coordination are not.

Recognize **hidden links** (things that must co-change but conceal their relationship), **needless
links** (independent things forced to co-change), and **surplus** (constructs without their own reason
to exist). A special case may reveal a missing design concept, but may also protect a real requirement.
Investigate its purpose rather than deleting it for aesthetic simplicity.

### 4. Deliver or Implement at the Requested Depth

For a **plan**, provide the smallest useful combination of:
- **Architectural brief:** objective, relevant evidence, assumptions, chosen design and named owners
  for important data, contracts and invariants.
- **Decision rationale:** material alternatives and tradeoffs when a choice is consequential; clearly
  separate decisions from unresolved hypotheses and describe reconsideration conditions if useful.
- **Execution map:** ordered, dependency-aware work packages. Each meaningful package states its
  expected outcome, affected contracts or owners, prerequisites and acceptance evidence; test-first
  steps belong with behavior changes.
- **Transition and operations:** supported client versions, migration, release ordering, recovery,
  monitoring and rollback versus forward-fix limits **only** where the system needs them.

Before delivery, challenge the plan: could implementation follow these steps while violating an
important requirement? Would a different engineer have to invent the data owner, failure behavior, or
cutover rule? Resolve material gaps; do not fill minor uncertainties with speculative infrastructure.

For **implementation**, separate preparatory restructuring from new behavior, use the applicable
test-first workflow, migrate affected callers, and inspect the diff for accidental coupling. Keep
the requested scope; note pre-existing problems rather than starting a general architectural cleanup.

A diagram, ADR, estimate or RFC earns its place by resolving ambiguity, meeting a project requirement
or supporting a consequential handoff. No artifact is mandatory because an example contains it. A
plan is complete when important decisions are justified, uncertainty is explicit, and another engineer
can execute and verify the intended outcome; avoid polishing an adequate plan indefinitely.

## Conditional References

Read only the reference that addresses a material question; do not load all of them.

- [Greenfield Design](references/greenfield-design.md): read when creating a system without established
  application architecture or choosing initial domain, data, and delivery boundaries.
- [Brownfield Evolution](references/brownfield-evolution.md): read when extending an existing codebase
  or assessing whether legacy behavior and conventions must be preserved.
- [Integration and Migration](references/integration-and-migration.md): read when old and new components,
  schemas, APIs, or deployments must coexist or undergo cutover.
- [Change Locality](references/change-locality.md): read when a multi-consumer feature risks duplicated
  rules, implicit dependencies, caller flags, or unnecessary layers.
- [Design Decisions](references/design-decisions.md): read when selecting a consequential owner,
  interface, abstraction, or domain boundary.
- [Architecture Evaluation](references/architecture-evaluation.md): read when the design has material
  quality-attribute tradeoffs, architectural risk, or unresolved feasibility assumptions.
- [State and Failure](references/state-and-failure.md): read when lifecycles, concurrent updates,
  retries, persistence, or partial failures affect correctness.
- [Performance Decisions](references/performance-decisions.md): read when workload, capacity, latency,
  or resource cost materially affects the choice.
- [Worked Architecture Plans](references/architecture-plan-casebook.md): read when a substantial plan
  benefits from an illustrative counterexample. Do not copy component choices, rollout strategies or
  sequence without validating their assumptions.

## Illustrative Decisions

- A new CMS property may legitimately touch schema, preview, editor, and renderer. Put its meaning
  at one authoritative boundary; don't force a one-file change or duplicate defaults independently.
- A single durable background worker may satisfy a small workload better than a broker cluster.
  Still address job acceptance, duplicate effects, and recovery if those affect the contract.
- Replacing a live API is not complete when the new service runs. Supported old clients, data
  migration, cutover conditions, and obsolete-path removal are part of the design.
