---
name: systematic-debugging
description: "Use when a bug, test failure, build failure, or unexpected behavior has an unclear cause: flaky or intermittent failures, works-locally-fails-in-CI, timing or environment dependence, regressions, or a fix that did not hold. Finds the root cause before any fix is proposed. Not for a defect whose cause and failing test are already established."
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. A symptom fix hides the cause.

**Core principle:** find the root cause before you attempt a fix.

## The Iron Law

```text
NO FIXES WITHOUT ROOT-CAUSE INVESTIGATION FIRST
```

Do not propose a fix until Phase 1 identifies where and why the failure occurs. Scale the
investigation to the uncertainty: a clear error can take minutes. Keep observations, interpretations,
and assumptions separate. An authorized temporary mitigation is allowed; label it as a mitigation,
not as a root-cause fix.

## When to Use

Use when the cause is unclear, especially when:

- The failure is intermittent or depends on timing, environment, data, or order.
- A previous fix did not work, or "one quick fix" seems obvious but unproven.
- Time pressure makes guessing tempting. Pressure calls for a smaller decisive probe, not a guess.

If the cause and a failing test are already established, proceed with the correction.

## The Four Phases

Complete each phase before you start the next.

### Phase 1: Root-Cause Investigation

1. **Read the error carefully.** Read the full message, stack trace, file paths, and codes. Do not skip
   warnings. Separate harness failures and pre-existing defects from the new regression.
2. **Reproduce it.** Find the exact steps, input, revision, and environment. Reproduce at the smallest
   useful boundary; halve a large failing input until the trigger is isolated. For intermittent
   failures, prefer controlled schedules and the existing harness; a lucky pass proves little. If you
   cannot reproduce it, gather more data; do not guess.
3. **Check recent changes.** Inspect the diff, recent commits, dependency versions, and configuration.
   Bisect when the reproduction is reliable and affordable.
4. **Find the failing boundary.** In a multi-component flow (for example CI → build → signing, or
   API → service → database), observe what enters and leaves each boundary. Locate the first one where
   data, state, or configuration diverges, then investigate that component. Observe only what answers
   the question. Never print secret values or dump the environment; report presence or absence.
5. **Trace the data flow.** Follow the bad value or effect back to its origin and fix it at the source.
   Source code shows a possible path; runtime evidence shows the path that ran. When the error is deep
   in a call stack or one test contaminates another, read [Root-Cause Tracing](references/root-cause-tracing.md).

### Phase 2: Pattern Analysis

1. **Find a working example.** Locate similar code, configuration, or a run that works.
2. **Compare against the reference.** Read enough of it to understand its full contract, including
   required call order and setup. Do not skim the part you depend on.
3. **List the differences.** Compare data, configuration, versions, load, timing, and state ownership.
   List every difference, however small, before you choose one as the cause.
4. **Understand the dependencies.** Identify the components, settings, and assumptions it requires.

For correlated flags or order-dependent behavior, name the states, events, legal transitions, and
invalid combinations. A state-machine library is not required to do this.

### Phase 3: Hypothesis and Testing

1. **Form one hypothesis.** State it: "X is the root cause because Y." Name the observation that would
   support it, the one that would contradict it, and how it differs from a competing explanation.
2. **Test minimally.** Make the smallest change or probe that tests it. Change one variable at a time.
3. **Verify before continuing.** Supported? Go to Phase 4. Contradicted? Revise the model and form a
   new hypothesis; do not add another layer of the same workaround. A supporting result does not
   necessarily identify a unique cause.
4. **When you do not know, say so.** State "I do not understand X," collect the smallest missing signal,
   research, or ask a targeted question.

### Phase 4: Implementation

1. **Create a failing test.** Reproduce the explained failure with the simplest automated test, using the
   project's testing workflow. If no framework exists, use a one-off script.
2. **Implement a single fix.** Correct the root cause at its owner. Make one change. No "while I'm here"
   improvements or bundled refactoring. Preserve compatibility and failure semantics: a remote timeout
   can follow a successful effect, so do not blindly repeat the operation.
3. **Verify the fix.** The new test passes, the formerly failing case works, other tests still pass, and
   the original issue is resolved. Search related paths for the same proven faulty assumption; similar
   syntax alone does not justify changing every match.
4. **Clean up.** Remove task-created workarounds and temporary diagnostics. Preserve pre-existing edits.
5. **If the fix does not work,** stop and return to Phase 1 with the new information.

**Repeated failed fixes are a signal to question the design.** When each fix reveals new shared state,
coupling, or symptoms elsewhere, stop patching. Ask whether the pattern is sound, and discuss the
design with the user before you attempt another fix. The signal is the revealed coupling, not a fixed
attempt count. Stop the investigation when the evidence is sufficient, or when the next observation
needs access you do not have.

## Red Flags — Stop and Return to Phase 1

- "Quick fix for now, investigate later."
- "Just try changing X and see if it works."
- Several changes made at once, then tests run.
- "It's probably X" without a test that could contradict it.
- Proposing fixes before tracing the data flow.
- Adding waits, retries, or guards without evidence of the mechanism.
- Treating missing telemetry as proof that an event never happened.
- Weakening an assertion or swallowing an exception to hide the failure.
- Another fix attempt after previous fixes failed, with no new evidence.

## User Signals That You Are Guessing

"Is that not happening?", "Will it show us…?", "Stop guessing", or "We're stuck" mean the approach is
not working. Return to Phase 1 and gather evidence.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| "The issue is simple, no process needed" | Simple bugs have root causes too. The process is fast for them. |
| "Emergency, no time" | Systematic debugging is faster than guess-and-check thrashing. |
| "Just try this first, then investigate" | The first fix sets the pattern. Investigate first. |
| "I see the problem, let me fix it" | Seeing a symptom is not understanding the cause. |
| "Multiple fixes at once saves time" | You cannot tell which one worked, and you add new bugs. |
| "It works locally" | Match the CI inputs and inspect the real dependency contract. |
| "The library, compiler, or OS must be broken" | Suspect your own code first. Prove a platform fault with a minimal reproduction. |
| "One more retry will solve it" | Determine whether the operation failed, succeeded, or has an unknown outcome. |
| "No reproduction, so no bug" | State what the evidence establishes and what remains unknown. |
| "Several failed fixes prove bad architecture" | Inspect the newly revealed coupling; a count alone does not justify a rewrite. |

## Quick Reference

| Phase | Key activities | Proceed when |
| --- | --- | --- |
| 1. Root cause | Read errors, reproduce, check changes, find the failing boundary | You know where and why it fails, or the exact missing observation |
| 2. Pattern | Find a working example, compare, list differences | Relevant differences and assumptions are explicit |
| 3. Hypothesis | One hypothesis, minimal test | Evidence supports one cause without contradiction |
| 4. Implementation | Failing test, single fix, verify | The fix and affected behavior have verification |

## When the Cause Is External or Unresolved

If investigation shows the cause is environmental, timing-dependent, or outside your access:

1. Report what you investigated, the evidence, and the competing explanations.
2. Name the next decisive observation and the access it needs.
3. Implement appropriate handling only if authorized, and label it as a mitigation.
4. Add safe diagnostics for future investigation where useful.

Most "no root cause" conclusions come from incomplete investigation. Do not expand access or scope
silently.

## Supporting Techniques

- [Root-Cause Tracing](references/root-cause-tracing.md): read when an error appears far from its origin
  or a test passes alone but fails in the suite.
- [Condition-Based Waiting](references/condition-based-waiting.md): read when a test uses sleeps, flakes
  under load, or depends on async readiness or timing.
- [Defense in Depth](references/defense-in-depth.md): read after finding the cause, when deciding which
  layers should validate or enforce the violated rule.
