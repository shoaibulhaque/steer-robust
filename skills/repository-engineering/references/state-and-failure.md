# State, Failure and Compatibility

**Read when:** changes affect lifecycles, concurrent state, persistence, retries, remote calls, or rolling
data or API transitions, or add runtime work that must be observed, shut down, and recovered. Stateless
edits do not need this workflow.

## Overview

**Core principle:** choose guarantees from the invariant and credible failure model. Neither a retry,
a database transaction nor a framework label proves the entire workflow correct.

## Make the Implicit State Model Visible

Name states, triggering events, guards, effects and allowed transitions. Identify invalid combinations
hidden by correlated flags, and what happens on duplicate, delayed or out-of-order events. State which
component owns a transition and which state is authoritative.

For a job, distinguish accepted, executing, effect committed and acknowledged. An acknowledgement lost
after commit is different from a job that never executed. Use an explicit state representation when
it removes ambiguity; no state-machine library, diagram or formal checker is required by this guide.

## Protect the Actual Consistency Rule

State the invariant across the relevant records and operations. Separate atomicity, isolation and
durability. A read followed by a write can race even inside a transaction; choose the supported lock,
checked version, constraint, atomic operation or isolation level that prevents the actual anomaly.

A useful probe schedules conflicting decisions deliberately rather than hoping a stress run reveals
them. Test both acceptance of a valid operation and rejection/preservation when the conflict occurs.

## Treat Unknown Outcomes Explicitly

When a request gets no response, the sender cannot tell which of these happened:

1. The request was lost.
2. The request is queued and will be delivered later.
3. The remote node failed.
4. The remote node paused, for example for garbage collection, and will respond later.
5. The remote node processed the request, and the response was lost.
6. The remote node processed the request, and the response is delayed.

A timeout ends the wait but answers none of these; a queued request may still arrive after the sender
gives up. So a timeout does not establish whether the remote effect happened. Define retry
eligibility, stable operation identity, deduplication ownership and reconciliation. Protect the durable
effect with the duplicate decision where the system's storage semantics allow it. Local rollback
cannot undo an already-issued external action.

Distinguish broker delivery, handler execution and durable business effect; an exactly-once setting
in one layer is not an end-to-end guarantee. Define recovery or compensation for the real remaining
window instead of adding an unbounded retry loop.

## Give Resources and Authority a Lifetime

Track acquisition, ownership, release and failure/cancellation behavior for workers, subscriptions,
files, sockets and locks. A cancelled caller may leave remote work running. A paused worker may resume
after lease expiry; correctness may require the protected resource to reject stale ownership.

Use appropriate local clocks for elapsed time. Do not infer cross-machine ordering or current authority
from unrelated timestamps. Avoid synchronized derived state without a clear update/invalidation policy.

## Evolve Readers and Writers Together

List supported clients, stored versions, old/new readers and writers, deployment order and rollback
obligations. Decide whether a complete cutover is possible or a staged bridge is required. Verify the
mixed-version combinations the contract actually supports; do not retain compatibility paths forever
without an owner and end condition.

For replayable or derived data, identify authoritative input, checkpoints, retention and effects during
replay. Consider late/out-of-order data and personal-data deletion when affected. A successful all-new
installation does not establish upgrade, replay or rollback correctness.

## Operate and Recover

A feature that works once but cannot be observed, shut down, or recovered may not meet its contract.
For new runtime work, decide:

- **Observability:** which failures are visible, and how an operator tells "slow" from "stuck".
- **Overload:** bounded queues, timeouts, and backpressure instead of unbounded growth.
- **Shutdown:** in-flight work drains, hands off, or stops at a safe point; restarts resume correctly.
- **Cleanup:** temporary resources are released on failure and cancellation, not only on success.

Logs, caches, analytics events, and backups can keep personal data after the primary record changes.
When the change handles personal data, include those copies in retention and deletion.

## Completion

The intended transition and affected failure schedule preserve the named invariant, relevant recovery
is observable, and remaining unsupported schedules are stated. Add mechanisms only for a concrete
protection requirement; do not dismiss a serious integrity failure merely because it is uncommon.
