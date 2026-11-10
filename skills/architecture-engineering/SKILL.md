---
name: architecture-engineering
description: "Use when planning or designing a greenfield system, evolving an existing codebase, integrating or migrating components, evaluating architecture tradeoffs, or implementing a multi-module change with consequential ownership or coupling risks. Not for routine local edits, pure behavior-preserving refactoring, root-cause debugging, or patch-readiness reviews."
---

# Architecture Engineering

## Overview

Choose the simplest defensible design for the actual requirements, then make it possible to build,
verify, operate, and change. Architecture includes the cost of understanding a system, not just its
runtime topology.

**Core principle:** give each rule and invariant a clear owner. Introduce coordination, abstraction,
and infrastructure only when they protect a real requirement or materially reduce the cost of change.

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

## Method

### 1. Establish the Architectural Drivers

Identify the desired outcome, indispensable behavior, constraints, stakeholders or consumers, and
acceptance evidence. Distinguish explicit requirements, observed facts, and assumptions. Ask for a
consequential missing decision only when evidence cannot settle it; otherwise proceed with a labeled
assumption.

Translate important quality attributes into scenarios: workload and latency, failure and recovery,
data consistency, privacy and authorization, deployability, operating cost, and ease of change. Select
those that could alter this design; do not invent targets or demand enterprise controls by default.

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

Start with the least complex design that satisfies the drivers. Make explicit which component owns
each invariant, how consumers interact with it, where state lives, and where failures are observed.

Challenge consequential decisions with one credible simpler alternative and scenarios that could
disprove the choice. Consider feasibility, resource growth, compatibility, operational burden,
reversibility, and failure windows in proportion to the risk. Use measurements, a narrow prototype,
or documentation checks when those would change the decision; don't present estimates as results.

Check change locality: can the same rule change in one authoritative place? Can an unrelated consumer
evolve without forcing other consumers to change? Many changed files are acceptable when each layer
has a distinct job; duplicated decisions and hidden coordination are not.

Recognize **hidden links** (things that must co-change but conceal their relationship), **needless
links** (independent things forced to co-change), and **surplus** (constructs without their own reason
to exist). A special case may reveal a missing design concept, but may also protect a real requirement.
Investigate its purpose rather than deleting it for aesthetic simplicity.

### 4. Deliver or Implement at the Requested Depth

For a **plan**, provide the smallest useful combination of:
- The objective, relevant evidence, assumptions, and chosen design or boundary.
- Material alternatives and tradeoffs, when the choice is consequential.
- Ordered work that names affected owners/contracts, prerequisites, risky transitions, and checks
  that would reject an incorrect implementation.
- Deployment, data migration, recovery, and rollback conditions only where they matter.

For **implementation**, separate preparatory restructuring from new behavior, use the applicable
test-first workflow, migrate affected callers, and inspect the diff for accidental coupling. Keep
the requested scope; note pre-existing problems rather than starting a general architectural cleanup.

A diagram, ADR, capacity estimate, or detailed RFC is useful only when it resolves a real ambiguity.
A plan is complete when the important decisions are justified, the remaining uncertainty is explicit,
and another engineer can execute and verify the intended outcome. Do not continue refining an already
sufficient plan for architectural perfection.

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

## Illustrative Decisions

- A new CMS property may legitimately touch schema, preview, editor, and renderer. Put its meaning
  at one authoritative boundary; don't force a one-file change or duplicate defaults independently.
- A single durable background worker may satisfy a small workload better than a broker cluster.
  Still address job acceptance, duplicate effects, and recovery if those affect the contract.
- Replacing a live API is not complete when the new service runs. Supported old clients, data
  migration, cutover conditions, and obsolete-path removal are part of the design.
