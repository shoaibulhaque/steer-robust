---
name: refactoring
description: "Use when restructuring code without changing its behavior (refactor, clean up, rename, extract, inline, move, split a large function or class, remove duplication) or when legacy code that lacks tests must be changed and first brought under test. Covers small behavior-preserving steps, characterization tests, and safe dependency breaking. Not for adding behavior alone or for redesigning a contract."
---

# Refactoring

## Overview

Refactoring changes the internal structure of code to make it easier to understand and cheaper to
change, without changing its observable behavior. Make a large change as a sequence of small
behavior-preserving steps. The code works after every step, so you can stop at any point.

**Core principle:** keep the code working after every step. If a step breaks it, back out the step
and take a smaller one.

## When to Use

- **Preparatory:** a requested feature or fix would be easier if the code were structured differently.
  Restructure first, then make the change.
- **Comprehension:** you understand confusing code well enough to record that understanding in names
  and structure, within the code you are changing.
- **Requested cleanup** or restructuring of a named area.
- **Legacy code:** code you must change has no tests that observe the behavior at risk.

Refactor only the code the task touches. Note unrelated problems as follow-ups. If code is broken or
its behavior must change, that is a behavior change: use the testing workflow, not this one.

## The Two Hats

At any moment, you either add behavior or refactor. Never both at once.

- **Refactoring:** add no behavior. Add a test only for a case you find was missing. Change a test only
  to follow an interface change, never to accommodate different results.
- **Adding behavior:** follow the applicable testing workflow.

Switch hats deliberately and keep each kind of change separately checkable, so a failure has one cause.
A bug you find while refactoring stays in place until the refactoring is done. Record it, and fix it
afterwards as a behavior change with its own test.

## Workflow

### 1. Establish the Safety Net

Run the relevant tests before you start; they must pass. Note any pre-existing failures. Confirm the
tests observe the behavior you will preserve, including returned values, state changes, errors, effects,
and ordering. If they do not, characterize it first.

### 2. Characterize Legacy Code

For code without adequate tests, work in this order:

1. **Identify change points:** where the code must change.
2. **Find test points:** where the effects of that change can be observed. Trace returned values,
   mutated arguments, shared state, and calls to collaborators.
3. **Break dependencies** that keep the code out of a test harness. Read
   [Dependency Breaking](references/dependency-breaking.md) when the code cannot be constructed or
   run in a test, or when you must edit it before any test exists.
4. **Write characterization tests:** run the code in a harness, assert a value you know is wrong, let
   the failure report the actual result, then set the expectation to that result. Repeat for the cases
   the change touches.
5. **Make the change and refactor** under that protection.

A characterization test documents what the code does, not what it should do. When a result looks
wrong, keep the expectation as observed and report the suspected bug. Target the code you will move
or change; one broad passing test may not exercise the risky transformation.

### 3. Take Small Steps

Apply one named refactoring per step: rename, extract, inline, move, change a signature, split a phase,
or similar. Run the focused tests after each step.

- **A step fails?** Revert it rather than debugging a large diff. Retry with smaller steps. The trickier
  the code, the smaller the steps.
- **Prefer tools:** use automated refactorings from the language server or IDE where reliable. Use the
  compiler or type checker to find affected callers; check dynamic and reflective uses separately.
- **Edit with one goal:** when you notice another needed change, write it down and finish the current
  step first.
- **Callers you cannot change atomically** (public APIs, other repositories, stored data): add the new
  form, migrate callers, then remove the old form. Keep a compatibility path only while a real contract
  needs it.

### 4. Complete the Cutover

Migrate every internal caller. Remove superseded functions, wrappers, duplicated paths, flags, and their
tests and docs. Search for remaining references. An old path that remains needs a stated contract and
a removal condition.

### 5. Verify and Review

Run the relevant suite and the repository's required checks. Review the diff as structure-only: no new
behavior, changed error, reordered effect, or weakened assertion. Check performance only where it is
part of the contract. Report the bugs you recorded.

## Choosing a Refactoring

| Signal | Consider |
| --- | --- |
| A name hides what something means | Rename it |
| A fragment needs a comment to explain what it does | Extract a function whose name states the intent |
| A layer only forwards calls | Inline it |
| The same knowledge, with the same reason to change, lives in several places | Unify it at one owner |
| Similar-looking code with different owners or reasons to change | Leave it separate |
| A function uses another module's data more than its own | Move it toward that data |
| One function performs several sequential phases | Split the phases |
| A flag argument selects between behaviors | Separate the functions |
| A type switch repeats across the code | Use polymorphism, only for real behavioral variation |
| Mutable data is shared widely | Encapsulate it behind its owner |
| A stored value can be derived | Replace it with a query |

Every refactoring has an inverse. Extract or inline, split or combine: choose whichever makes this
code easier to understand now.

## Red Flags — Stop and Back Out

- The code stays broken across several steps. That is not refactoring.
- A test needs a different expected result to pass.
- New behavior or a bug fix is mixed into the restructuring.
- "While I'm here" edits reach code the task does not touch.
- Restructuring proceeds with failing tests, or without tests that observe the behavior at risk.
- A big rewrite replaces an incremental path that was available.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| "It's a trivial refactor, no need to run tests" | Trivial edits break code. Run the focused tests after each step. |
| "I'll fix this bug while I'm here" | That changes behavior. Record it and fix it separately with a test. |
| "A rewrite is faster" | A rewrite loses behavior nobody wrote down. Characterize, then change in steps. |
| "The tests are in the way; I'll update them" | A failing test after a pure refactor means behavior changed or the test depends on internals. Find out which. |
| "Each extracted helper needs its own test" | Existing behavior tests protect a refactor. Add tests for missing cases, not per helper. |

## Verification Checklist

- [ ] Relevant tests passed before the first step and after the last.
- [ ] Behavior at risk was observed by tests, or characterized first.
- [ ] Tests changed only to follow an interface change.
- [ ] The diff contains structure only; recorded bugs are reported, not silently fixed.
- [ ] Callers are migrated and superseded code is removed or justified.
