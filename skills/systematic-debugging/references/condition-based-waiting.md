# Condition-Based Waiting

**Read when:** a test uses sleeps, flakes under load, or depends on async readiness, shutdown
ordering or timing.

## Overview

**Core principle:** observe the condition the workflow promises instead of guessing readiness from
a delay.

## When to Use

Prefer an event, future, barrier, latch or existing bounded wait utility. Poll only when the actual
condition has no suitable notification and reads are safe. Do not introduce a new utility when the
repository already owns synchronization.

## Core Pattern

`start operation → wait for meaningful condition with deadline → assert final contract → cleanup`

| Scenario | Meaningful observation |
| --- | --- |
| Worker ready | It can accept the intended work, not merely that a process exists |
| Durable write | Read from the authoritative store at the required consistency boundary |
| Cancellation | The protected effect did not occur and owned resources were released |
| Event processing | The correct operation/event identity reached the expected state |

Choose a deadline and polling cadence from the test environment and operation budget; there is no
universal interval. Use a monotonic duration source when measuring elapsed time. Include the last
observed state in timeout diagnostics without leaking sensitive data. Bound cleanup and do not swallow
cancellation or worker errors as "not ready yet".

## Testing Actual Timing Behavior

For debounce, leases, deadlines or backoff, elapsed time is part of the contract. Prefer the project's
controlled clock and explicit schedule; assert before and after the required boundary. Polling until
success alone can hide an early/late execution or an illegal transition.

## Common Mistakes

- Replacing a sleep with unbounded polling.
- Testing a derived readiness flag while the real operation still fails.
- Consuming an event destructively in the wait predicate and changing the behavior being observed.
- Retrying a side effect while pretending to observe it. A timed-out remote write may have succeeded.
- Reporting an occasional pass as proof that a race was eliminated.
