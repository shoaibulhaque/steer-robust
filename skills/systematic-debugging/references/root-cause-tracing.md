# Root-Cause Tracing

**Read when:** an error appears far from its origin, or a test passes alone but fails in the suite.

## Overview

**Core principle:** follow the invalid value or effect back to the first violated assumption.

## The Tracing Process

1. **Observe the symptom:** record the operation, input, state and relevant stack, separating fact from interpretation.
2. **Find the immediate cause:** inspect the actual failing operation and arguments.
3. **Ask what called it:** follow the caller and transformations, including deferred work or callbacks.
4. **Keep tracing:** locate where a valid value became invalid or an invalid assumption first entered.
5. **Correct the owner:** protect the meaningful invariant, then verify the affected consumer path.

For example, an empty working directory can resolve to the process directory. The fault may begin
when a fixture value is captured before setup, not in the final filesystem operation. Check lifecycle
and ownership before adding directory guards to every caller.

## Adding Evidence

Use the project's logger, debugger or trace mechanism at the boundary that distinguishes explanations.
Record safe correlation IDs, states and transitions. Do not dump environment values, credentials or
whole request bodies. Verify instrumentation is enabled and observation failures are not mistaken for
application behavior. Remove temporary diagnostics unless an operational requirement justifies them.

## Finding Test Pollution

Establish a clean disposable fixture, run the affected test alone, then compare the suite with the
same configuration and ordering. Narrow suspect predecessors or use the runner's native shuffle/seed
and selection options. Bisection requires a reliably reproducing subset; some failures require several
tests or shared processes, so a one-test-at-a-time scan may miss them.

Preserve test exit codes and distinguish a failed invocation from a clean run. Never delete a real
repository or existing state to manufacture a clean baseline. Confirm the suspected producer and
consumer together before claiming the source of contamination.

## Completion

The causal chain explains the observation and the correction rejects the failure without erasing
legitimate behavior. If a link remains unobserved, state that limit; tracing source alone is not proof
of the runtime path. Add independent defenses only where another trust, ownership or effect boundary
needs protection.


## Worked Case: "The Job Ran Twice"

An API reports a timeout, and the user sees two completed operations. It is tempting to add a delay or lower the worker concurrency. Neither explains the symptom.

**Observations to collect, without repeating live side effects:** operation identity, request timestamp, job claim identity, durable effect ID, retry or redelivery reason, and relevant worker state. Inspect existing traces and controlled test fixtures first.

Separate competing explanations:

| Hypothesis | Distinguishing observation |
| --- | --- |
| Client submitted twice | Two independently accepted requests with different operation identities |
| Broker redelivered one request | Same operation identity delivered or claimed more than once |
| External call succeeded but response was lost | One durable external effect followed by a timeout/retry |
| Two workers shared ownership | Overlapping claims with insufficient atomicity or lease fencing |

A useful probe deliberately schedules the relevant interleaving in an isolated environment, then observes the durable business effect. An ordinary successful run cannot falsify a concurrency hypothesis.

Once evidence identifies the cause, correct the component that owns request identity, claiming, or effect deduplication. Do not globally disable retries: some failures require retry for liveness. Report what the observations establish and any untested schedule or external visibility limit.
