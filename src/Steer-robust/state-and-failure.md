# State, failure and concurrency

Read when work persists data, crosses asynchronous boundaries or owns shared resources and side effects.

## Outcomes and retry ownership

- Distinguish success, known failure and unknown outcome. Lost acknowledgement does not prove non-execution.
- Before repeating an uncertain effect, reconcile its receipt/status or use supported idempotency semantics.
- If safe repetition cannot be established, expose the uncertainty rather than inventing a fallback.
- Proven repeat-safe operations may use their normal bounded retry policy.
- Put retry decisions at the layer that knows the operation's semantics and overall deadline.
- Bound attempts and elapsed time; classify transient failures and use backoff/jitter when appropriate.
- Account for retries already performed by clients, proxies or workers; stacked budgets multiply load.

## Persistence and recovery

- Make validation, writes, reads and recovery agree on representation and identity.
- Define normalization explicitly; do not erase meaningful differences or genuine conflicts.
- Use transaction boundaries that protect business invariants across writes.
- Consider crash points before, between and after effects, including persistence preceding acknowledgement.
- Recovery must identify committed, incomplete and conflicting work without fabricating success.
- Define replay, compensation and reconciliation; rollback cannot undo external effects.
- For commit-dependent effects, choose after-commit dispatch, an outbox or reconciliation to match delivery guarantees.
- Publish related state consistently using the project's transaction and synchronization primitives.

## Resource lifetime

- Assign ownership for acquisition, commit/rollback, cancellation and release of each resource.
- Cleanup must cover failures during setup as well as during normal work.
- Propagate deadlines and cancellation across relevant boundaries; stop work that no longer has authority.
- A timeout or cancelled caller does not itself stop a dispatched write or release its transaction.
- Reconcile uncertain effects and retain ownership until their protocol permits safe handoff or cleanup.
- A bounded diagnostic read may abandon waiting when safe, provided result delivery and cleanup remain bounded.
- Do not extend that read-only exception to uncertain writes, transactions or unbounded resource leakage.

## Bounded scheduling

- Budget concurrency at the shared scarce resource, including interactive and background demand.
- Bound admission, active work and backlog; a queue alone does not create capacity.
- Preserve per-key order when the contract requires it; independent keys may proceed separately.
- Isolate failures where appropriate without silently losing failed work or breaking required atomicity.
- Define behavior under overload, deadline expiry, cancellation and shutdown.
- Shutdown owns queued and active work; decide whether to drain, cancel or durably hand it off.
- Prefer removing unnecessary shared mutable state; synchronize legitimate sharing explicitly.

## Equivalent in-flight work

- Coalesce only work with equivalent input, resource identity, configuration and authorization context.
- Keep the shared operation with the owner of the underlying resource.
- Define whether a caller's cancellation affects only its wait or the shared operation itself.
- Handle rejection, cleanup and the next attempt; do not permanently memoize a transient failed promise.
- Never share results across tenants or credentials merely because their superficial keys match.

## Synchronization and authority

- Use the project's proven locks, channels, transactions or publication mechanisms.
- An atomic flag does not automatically publish associated data safely or make a compound transition atomic.
- Avoid assuming that a single-threaded event loop prevents interleaving across awaits.
- Revalidate mutable preconditions at the effect boundary when they can change during the operation.
- Test the relevant competing transitions, not only sequential success.

## Error classification and diagnostics

- Catch expected failures narrowly; distinguish absence from corruption, programming errors and storage failure.
- Preserve useful cause/context without leaking sensitive data or swallowing the real failure.
- Classify cache misses separately from cache errors when they imply different recovery or operator action.
- Optional diagnostics must not erase a successful primary result or disguise a failed primary operation.
- Record enough operation identity and phase to diagnose failure, subject to privacy and logging limits.
