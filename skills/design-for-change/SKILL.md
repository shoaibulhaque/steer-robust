---
name: design-for-change
description: "Use when implementing a feature or fix in an existing codebase that spans consumers, repeats a rule, adds shared state, or tempts caller-specific flags or extra layers. Prevent hidden co-change, needless coupling, and surplus in the changed path. Not for isolated edits, consequential design decisions, behavior-preserving refactoring, or review-only tasks."
---

# Design for Change

## Overview

Prevent the new change from making future changes harder. This is a focused implementation workflow,
not a whole-codebase audit or cleanup.

**Core principle:** put each decision with the reason it changes, and make its connections to
consumers explicit. Code that changes together should be easy to find and update together; unrelated
decisions should not be forced to change together.

## When to Use

Use during an implementation when a feature or fix introduces a rule used by multiple consumers,
threads data across modules, adds shared state, or pressures you to add variant flags, copied logic, or
new forwarding layers. Keep the check proportional to the change.

Skip an isolated edit with a clear owner. Consequential choices about contracts, domain ownership,
persistence, or architecture belong to the repository's design workflow. Pure restructuring belongs
to the refactoring workflow; an explicitly requested review belongs to change verification. This
skill does not replace test-driven development or automatically invoke other skills.

## Workflow

### 1. Trace the Change, Not the Entire Repository

1. Read the applicable instructions, the affected code path, its immediate consumers, and nearby tests.
2. Find the existing owner of the behavior and the closest working example.
3. Name the decision being introduced or modified, who relies on it, and what must remain stable.
4. Distinguish multiple *representations* of one rule from independent rules that merely look alike.

Do not inventory unrelated modules. If there is already an appropriate extension point, use it.

### 2. Check the Three Tangles

| Signal in the proposed change | What to do |
| --- | --- |
| **Hidden links:** the same decision is copied into several places; callers must know an undocumented order; separate state must be manually synchronized | Give the decision a discoverable owner; express dependencies through a clear contract or explicit coordination |
| **Needless links:** a stable component knows a caller's special vocabulary; a consumer reaches through an interface into internals; an option couples otherwise independent workflows | Keep caller-specific policy at its owner and depend on the smallest stable contract that carries the required behavior |
| **Surplus:** a new pass-through wrapper, unused extension hook, speculative configuration, or redundant stored state adds concepts without a real requirement | Omit it; prefer the existing path unless the new boundary hides meaningful volatility or enforces an invariant |

Do not deduplicate on syntax alone. Two rules with different owners or reasons to evolve can correctly
remain separate. A single consumer can justify an interface at an external or failure-prone boundary.
Judge coupling by the knowledge and coordination it imposes, not by file count or caller count.

### 3. Treat Special Cases as Questions

A new value-specific branch, caller flag, retry, sleep, swallowed exception, or disabled test may signal
a missing design concept. Ask what concrete requirement or failure mode it handles, and whether that
behavior belongs at the current boundary.

- Preserve legitimate exceptions, compatibility paths, and defensive behavior; make their purpose
  observable and testable where appropriate.
- Do not hide a repeated structural problem behind another condition or a generic framework.
- If a real ownership or contract redesign is needed, handle it as a consequential design decision
  rather than quietly broadening the task.

### 4. Implement and Inspect the Diff

Implement within the requested scope. Keep behavior changes and preparatory restructuring separately
checkable. Use the repository's applicable test-first and verification practices; do not introduce a
second testing process here.

When done, ask:

1. If this decision changes again, can someone identify its owner without searching for copies?
2. Did this patch require consumers to learn more internals, hidden state, or call ordering?
3. Are multiple changed files justified by distinct layers or contracts, rather than duplicated
   decisions?
4. Did we add an abstraction, special case, or configuration without a present need?

Correct tangles introduced by this patch. Record relevant pre-existing problems as follow-ups; do not
expand into a repository-wide refactor. Finish when the requested behavior and checks are complete,
not when the architecture is theoretically perfect.

## Example

A new content property may legitimately require edits to its schema, editor, API, and renderer. The
four-file change is not itself a tangle. Independently inventing four meanings or fallback rules for
that property is. Keep the authoritative contract explicit while respecting each layer's role.

Conversely, two integrations with similar-looking transformations may need separate implementations
when their contracts evolve independently. A shared helper with provider flags can make both harder
to change.

## Red Flags

- "One file per change" becomes the goal instead of clear ownership.
- A reusable helper requires a new flag for each consumer.
- A duplicated decision is defended as "simpler" without accounting for synchronization.
- A workaround is deleted solely because it looks like a special case.
- A requested feature becomes an unsolicited architectural rewrite.

**Stop condition:** the new change has an understandable owner, justified dependencies, no avoidable
coordination introduced by this patch, and the required behavior is verified.
