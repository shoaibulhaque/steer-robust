---
name: test-driven-development
description: "Use when implementing a testable feature, bug fix, or behavior change, before writing production code. Covers red-green-refactor, verifying the failure, minimal implementation, and test quality. Includes behavior expressed in configuration, such as access rules or routing. Not for behavior-preserving refactoring or changes with no behavior a test can observe, such as prose or formatting."
---

# Test-Driven Development

## Overview

Write the test first. Watch it fail for the intended reason. Write the minimal code that passes.
Then improve the design while the tests stay green.

**Core principle:** if you did not watch the test fail, you do not know whether it tests the right thing.

## When to Use

**Use the cycle for:** new behavior, bug fixes, and behavior changes that a test can observe.

**Not for a behavior-preserving refactor:** that keeps existing tests green rather than starting with
a failing one. A characterization test records what exists; a regression test specifies what must change.

**Configuration counts when it changes behavior.** Access rules, routing, validation limits, and
feature flags are testable behavior even when no code changes: use the cycle.

**Use a different check for:** changes with no behavior a test can observe, such as prose, formatting,
and disposable experiments, and for generated artifacts whose generator owns the tests. Do not invent
a meaningless test. Honor explicit project or user exceptions, and state
material verification gaps.

Use the repository's test runner, fixtures, and conventions.

## The Iron Law

```text
NO PRODUCTION CODE FOR TESTABLE BEHAVIOR WITHOUT A FAILING TEST FIRST
```

Never label tests written after the code as TDD. If task code already exists before its test:

- Preserve the work. Do not delete user code or reset the worktree to recreate an ideal sequence.
- Write the test, then prove it detects the defect: run it against the baseline in an isolated scratch
  copy, or temporarily revert only your own task change.
- Report the actual sequence.

Exploration is fine. Treat an exploratory spike as disposable, then start the real change with a test.

## Red–Green–Refactor

```text
RED → verify it fails correctly → GREEN → verify it passes → REFACTOR → verify still green → next
```

A wrong failure returns to RED. A failing GREEN returns to GREEN.

### RED — Write a Failing Test

Keep a short list of required cases. Choose one behavior that teaches something. Write the assertion
first, with an expectation derived by hand from the requirement. Exercise public behavior at the
smallest useful boundary.

**Good:** a clear name, real behavior, one thing.

```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

**Bad:** a vague name, and it checks the mock's call count instead of the result.

```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```

Requirements: one behavior, a name that states it, and real code. Use a double only at a slow,
nondeterministic, or external boundary.

### Verify RED — Watch It Fail

**Mandatory.** Run the focused test with the project's command. Confirm that:

- The test was selected and ran.
- It fails on the assertion, not with a setup, import, compile, or typo error.
- The failure message is the one you expect, because the behavior is missing.

**Test errors?** Repair the harness and rerun until the test fails correctly.
**Test passes?** Check the path and the requirement. The behavior may already exist. Do not break
correct code or manufacture a failure to complete the cycle.

### GREEN — Minimal Code

Write the simplest code that meets the contract, including its known constraints. An obvious
implementation is fine. When unsure, fake it or add a second distinguishing example.

**Good:** just enough to pass.

```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```

**Bad:** options no test asked for.

```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI
}
```

Do not add options, features, or unrelated refactoring beyond what the tests require. Do not leave a
hard-coded special case that fits only one example.

### Verify GREEN — Watch It Pass

**Mandatory.** Run the focused test and the affected existing tests. Confirm that:

- The new test passes and the expected tests were selected.
- Other affected tests still pass.
- The output has no new errors or warnings.

**Test fails?** Fix the code, not the test. Change an expectation only with an independent,
contract-based reason. Never weaken an assertion to hide a failure.
**Other tests fail?** Fix them now.

### REFACTOR — Clean Up

Only after green: improve names, ownership, and interfaces; remove duplicated knowledge and needless
indirection. Preserve observable effects, errors, and ordering. Rerun the tests. Do not add behavior
in this step; keep behavior changes separate so a failure has one cause. Existing tests protect a
refactor; do not add a new test per extracted helper.

### Repeat

Write the next failing test for the next case. Vary data only when another example distinguishes the
real rule. Before completion, run the checks the repository requires.

## Good Tests

| Quality | Good | Bad |
| --- | --- | --- |
| Focused | One behavior and its consequences; "and" in the name suggests a split | One test per private helper |
| Clear | The name states the behavior | `test1`, `works` |
| Independent oracle | Hand-checked examples or independent properties | Expected value computed by the implementation |
| Real | Real logic, controlled external boundaries | A double erases the effect being verified |
| Isolated | Owned fixtures, controlled clocks, deterministic inputs | Order dependence, shared state, sleeps |

Read [Writing Good Tests](references/writing-good-tests.md) when you choose test doubles, work with
legacy seams or difficult fixtures, or doubt that a passing test can reject a plausible defect.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| "Too simple to test" | Simple code breaks too. The test is cheap. |
| "I'll test after" | A test written after the code passes immediately and proves nothing about detection. |
| "Tests after achieve the same goal" | Tests-after answer "what does this do?"; tests-first answer "what should this do?" |
| "Already manually tested" | A manual check leaves no repeatable record and misses cases under pressure. |
| "Deleting hours of work is wasteful" | Do not delete it. Prove a new test detects the defect, and report the sequence. |
| "I need to explore first" | Fine. Treat the spike as disposable, then start with a test. |
| "Hard to test, so skip it" | Hard to test usually means hard to use. Find a smaller seam. |
| "Existing code has no tests" | Characterize the part you change before you change it. |
| "Coverage is high" | Coverage does not measure whether assertions reject wrong behavior. |
| "Testing is hard, so build a framework" | Find the smallest seam and verify its real connection. |
| "TDD means no design" | Think through consequential contracts before the next example. |

## Red Flags — Stop and Repair the Feedback

- Production code written before its test, without the detection check above.
- A new test that passes immediately, or a test that was never selected.
- A failure you cannot explain.
- An expectation that mirrors the implementation.
- An assertion changed only to get green.

Each of these means the feedback is unreliable. Repair it before you add more code.

## Verification Checklist

- [ ] Each new behavior has a test that was observed failing for the expected reason.
- [ ] Each change used minimal code to pass; no speculative options remain.
- [ ] Focused and repository-required checks pass; output shows no new errors or warnings.
- [ ] Tests use real code; doubles appear only at necessary boundaries.
- [ ] Relevant existing behavior remains protected; fixtures do not depend on test order or live secrets.
- [ ] Relevant edge cases and error paths are covered.
- [ ] Blocked or unrun checks are named in the report.

## When Stuck

| Problem | Response |
| --- | --- |
| Do not know how to test it | Write the wished-for API and the assertion first. Ask if the requirement is unclear. |
| Test is too complicated | The interface may be too complicated. Simplify it. |
| Must mock everything | The code may be too coupled. Introduce a narrow seam. |
| Setup is huge | Extract test helpers. Still huge? Reconsider the design. |
| A double cannot represent the contract | Use a focused integration test. |

A complex fixture may reveal coupling, but it does not prove the whole design is wrong.

## Example: Bug Fix

**Bug:** an empty email is accepted.

**RED**

```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**

```text
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**

```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**

```text
$ npm test
PASS
```

**REFACTOR:** extract shared validation if several fields need it, then rerun the tests.

## Debugging Integration

Bug found? Write a failing test that reproduces it, then follow the cycle. The test proves the fix and
prevents the regression. When the cause is unclear, diagnose it first; do not change code repeatedly
to make a test pass.
