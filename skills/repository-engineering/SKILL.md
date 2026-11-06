---
name: repository-engineering
description: "Use when a substantial change in an existing codebase needs a design decision: where new behavior belongs, whether to add or remove an abstraction, how to change an interface or domain rule, or how a change affects state, failure handling, compatibility, or performance. Not for mechanical edits, pure refactoring, diagnosis-only, or review-only tasks."
---

# Repository Engineering

## Overview

Choose a solution that fits the repository's existing responsibilities and its actual requirements.
This skill supports consequential implementation decisions. It does not require a design document
for every edit.

**Core principle:** complexity must earn its place by reducing what callers and maintainers need to know.

## When to Use

Use for consequential design and ownership decisions in an established codebase: a new feature that
crosses modules, a changed interface or domain rule, new state or persistence, or a performance
requirement. Skip mechanical edits, pure refactoring, diagnosis-only requests, and review-only work.
When an established pattern already meets the contract, follow it without a design exercise.

## Workflow

### 1. Locate the Owner and Contract

1. Read the applicable project guidance, the affected code, its callers, and nearby tests.
2. Find a working analogue: the closest existing feature built the way this one should be.
3. Identify the extension point and the module that owns the rule being changed.
4. State the contract: intended behavior, invariants, consumers, and supported compatibility.

Follow only the dependency paths the change touches. Not every legacy behavior is a requirement;
confirm which ones consumers rely on.

### 2. Decide Whether a Design Choice Exists

If an established pattern meets the contract, use it and go to step 4. Compare alternatives only when
the choice materially affects an interface, a domain boundary, coupling, the state model, or performance.
Then compare the proposal with one plausible simpler option. A sketch or a small experiment is enough;
write a design document only when useful or required.

### 3. Choose the Boundary

- **One owner per rule.** Put knowledge that changes together in one module. Similar code in independent
  domain contexts may correctly stay separate. A shared helper that keeps gaining context flags signals
  a wrong boundary; do not add another flag.
- **Deep over shallow.** Prefer an interface that hides meaningful decisions. A forwarding method can add
  more concepts than it removes, and a larger cohesive module can be easier to understand. One caller can
  still justify a boundary that isolates volatile I/O or protects an invariant.
- **Low reader load.** Count the indirections needed to answer a question and the hidden mutable state
  needed to trust the answer. Do not reduce one by increasing the other. Derive state from its owner
  instead of synchronizing copies.
- **Representations that prevent invalid states.** Use domain vocabulary and types that make real misuse
  impossible. A folder named `domain` enforces nothing; check dependencies and mutation access.
- **Validate at the trust boundary.** Validate untrusted data where it enters, then pass validated values
  inward. Do not repeat guarantees a schema, constructor, or type already provides. Check again only at
  a new trust boundary, or when mutable state, freshness, or authorization can invalidate the guarantee.

### 4. Resolve the Affected Risks

Name the invariant the change affects and the component that must enforce it. Do not investigate
every possible failure category for an ordinary local change. Read only the reference that settles a
material question:

- [Design Decisions](references/design-decisions.md): read when domain meanings compete, or an
  abstraction, interface, or pattern choice is uncertain.
- [State and Failure](references/state-and-failure.md): read when the change affects lifecycles, shared
  state, retries, persistence, or mixed-version deployments.
- [Performance Decisions](references/performance-decisions.md): read when workload, time or space growth,
  or an optimization tradeoff is part of the requirement.
- [Code-Level Decisions](references/code-level-decisions.md): read when names, comments, representations,
  side effects, error handling, absence, assertions, or resource cleanup inside a function or module
  affect correctness or clarity.

An abstraction cannot add guarantees its implementation does not provide; respect the actual framework
and storage semantics. Do not add reliability mechanisms for a failure you cannot name.

### 5. Implement with Feedback

- Keep restructuring and behavior changes in separate, checkable steps, so a failure has one cause.
  Use the applicable testing workflow.
- When feasibility is uncertain, build one thin path through the real boundary before broadening it.
- Migrate every affected caller in the same change. Remove the superseded path, or state the contract
  that keeps it and when it will be removed.
- For repetitive or fragile transformations, reuse existing tooling or write a small deterministic script
  when it reduces total work or makes verification repeatable. Check it on one representative unit, inspect
  the diff, and make reruns safe. Do not create a script merely because the task is nontrivial.

## Examples

- **Deep over shallow.** Unix file I/O exposes five calls, and its implementation has changed radically
  behind them for decades. By contrast, reading serialized objects from a file through three stacked
  stream objects, where forgetting the buffering one silently makes I/O slow, pushes the common case
  onto every caller.
- **One owner for one decision.** When one class reads a file format and another writes it, both change
  whenever the format changes, even if neither exposes it. Put the format in one module.
- **Separate models, explicit boundary.** Two teams that casually share objects between a booking model
  and a scheduling model, without agreeing what is shared, end up with models that diverge silently.
  Draw the boundary and translate across it.

## Red Flags — Reconsider the Design

- A stack of layers that only forward calls.
- Copies of state kept in sync with no single owner.
- Context flags that select between independent rules.
- A new parallel implementation beside an existing extension point.
- Reliability machinery with no named failure it prevents.

Neither a large module nor a single caller alone proves a design defect. Judge the actual dependencies,
reader load, and required guarantees.

## Verification Checklist

- [ ] The chosen owner and interface fit the repository and its consumers.
- [ ] Each affected invariant has a named enforcing component.
- [ ] Callers are migrated together; superseded paths are removed or justified.
- [ ] Changed semantics have proportionate evidence, including relevant failure or migration paths.
- [ ] Temporary seams, compatibility paths, and task-created tools have a purpose and an end condition.
