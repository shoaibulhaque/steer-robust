# Dependency Breaking

**Read when:** code you must change cannot be constructed or run in a test harness, or you must edit
it before any test protects it.

## Overview

**Core principle:** make the smallest, most conservative edit that lets a test sense the behavior.
These first edits often happen without tests, so they must not change behavior.

A test harness needs two things, and they are separate problems:

- **Sensing:** the test can observe the result or effect.
- **Separation:** the test can run without collaborators that are slow, nondeterministic, external,
  or impossible to construct.

## Find a Seam

A seam is a place where behavior can be substituted without editing the code under test. Each seam
has an enabling point, where the substitution is chosen. Prefer the least disruptive seam the language
supports:

| Seam | Enabling point | Typical use |
| --- | --- | --- |
| Object or parameter | Constructor, argument, or setter | Most object-oriented and functional code |
| Module or link | Import, dependency-injection container, build configuration | Module-level functions, compiled code |
| Configuration | Runtime setting or environment | Integration-level substitution |

## Conservative Edits Without Tests

- **Preserve signatures.** When extracting or moving code, copy parameter lists and types exactly.
  Do not clean up in the same step.
- **Lean on the compiler.** After an intentional break, let type errors list the affected callers.
  Dynamic dispatch, reflection, and string-based lookups still need manual checks.
- **One goal per edit.** Finish one dependency break, run what you can, then start the next.

## Techniques

| Problem | Technique |
| --- | --- |
| A collaborator is created inside the constructor | Pass it in as a parameter, keeping the old constructor as a default |
| A method calls a hard-to-test collaborator | Extract the call into its own method, then override it in a test subclass or pass a function |
| Code depends on a concrete class | Extract a narrow interface with only the methods this code uses |
| Code reads or writes a global or singleton | Route access through a parameter or an overridable accessor |
| A parameter type is huge or external | Adapt it to a small interface the operation actually needs |
| A long method has tangled local state | Move it into its own object, with locals as fields, then decompose it |
| A static or module function blocks testing | Wrap it in an instance delegator or inject a function |

Substitutes must preserve the behavior the test depends on and must never leak into production.
Treat test-only overrides as intermediate steps; replace them with clearer seams once tests exist.

## Adding Behavior When the Harness Is Too Costly

- **Sprout:** write the new logic as a new, tested function or class and call it from the old code.
- **Wrap:** add behavior before or after an existing operation in a wrapper with the same interface.
  Check that the ordering of effects stays correct.

Either way, a unit test of the new code does not prove the old caller invokes it correctly. Verify the
connection at an appropriate level, through the real caller.

## Find a Covering Test Point

When many changes cluster in one area, find an interception point: a narrow place where the effects of
all the intended changes can be observed. Cover it first, then move toward finer-grained tests. Do not
let every test become a slow system test once finer seams exist.

## Explore Safely

To understand a tangle, refactor freely in a disposable scratch copy. Discard it, then redo only the
validated steps through the safe workflow.
