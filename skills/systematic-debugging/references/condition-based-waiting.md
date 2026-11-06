# Condition-Based Waiting

**Read when:** a test uses sleeps (`setTimeout`, `sleep`, `time.sleep()`), flakes under load or in CI,
times out when run in parallel, or depends on async readiness, shutdown ordering, or timing.

## Contents

- Overview
- When to Use
- Core Pattern
- Quick Patterns
- Implementation
- Common Mistakes
- When an Arbitrary Delay Is Correct

## Overview

Flaky tests often guess at timing with arbitrary delays. That creates races: tests pass on fast
machines and fail under load or in CI.

**Core principle:** wait for the condition you care about, not a guess about how long it takes.

## When to Use

- **Use it** when a test waits for async work to reach a state.
- **Do not use it** when timing itself is the behavior under test, such as debounce, throttle intervals,
  leases, or backoff. Use the project's controlled clock and document any real delay (see below).
- Prefer an existing event, future, barrier, latch, or bounded wait utility in the project. Poll only
  when no notification exists and reading the state is safe.

## Core Pattern

```typescript
// ❌ BEFORE: guessing at timing
await new Promise(r => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// ✅ AFTER: waiting for the condition
await waitFor(() => getResult() !== undefined, 'result to be available');
const result = getResult();
expect(result).toBeDefined();
```

## Quick Patterns

| Scenario | Pattern |
| --- | --- |
| Wait for an event | `waitFor(() => events.find(e => e.type === 'DONE'), 'DONE event')` |
| Wait for a state | `waitFor(() => machine.state === 'ready', 'ready state')` |
| Wait for a count | `waitFor(() => items.length >= 5, 'five items')` |
| Wait for a file | `waitFor(() => fs.existsSync(path), 'output file')` |
| Complex condition | `waitFor(() => obj.ready && obj.value > 10, 'ready with value')` |

Wait for the meaningful observation:

| Scenario | Meaningful observation |
| --- | --- |
| Worker ready | It accepts the intended work, not merely that a process exists |
| Durable write | A read from the authoritative store at the required consistency |
| Cancellation | The protected effect did not occur, and owned resources were released |
| Event processing | The correct event identity reached the expected state |

## Implementation

A generic polling helper, when the project has none:

```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const start = performance.now(); // monotonic, unlike Date.now()
  while (true) {
    const result = condition();
    if (result) return result;
    if (performance.now() - start > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }
    await new Promise(r => setTimeout(r, 10)); // poll every 10 ms
  }
}
```

Choose the deadline and polling interval from the test environment and the operation's budget. Include
the last observed state in the timeout message, without sensitive data.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Polling too fast, such as every 1 ms | Poll at a modest interval, such as 10 ms |
| No timeout, so the loop can hang forever | Always include a deadline with a clear error |
| Stale data: state cached before the loop | Read fresh state inside the condition |
| Unbounded polling replacing a sleep | Bound it, and bound cleanup too |
| Waiting on a derived readiness flag while the real operation still fails | Observe the real operation |
| A predicate that consumes an event and changes the behavior | Observe without side effects |
| Retrying a side effect while "waiting" for it | A timed-out remote write may have succeeded; observe instead |
| Treating cancellation or worker errors as "not ready yet" | Surface them immediately |
| Calling a race fixed after an occasional pass | Prove it with a controlled schedule |

## When an Arbitrary Delay Is Correct

```typescript
// The tool ticks every 100 ms; two ticks are needed to verify partial output.
await waitForEvent(manager, 'TOOL_STARTED'); // first: wait for the triggering condition
await new Promise(r => setTimeout(r, 200));   // then: wait for the timed behavior
// 200 ms = 2 ticks at 100 ms intervals; documented and justified.
```

Requirements:

1. First wait for the triggering condition.
2. Base the delay on known timing, not a guess.
3. Comment why.

For debounce, leases, deadlines, or backoff, prefer a controlled clock and assert before and after the
required boundary. Polling until success can hide an early or late execution.
