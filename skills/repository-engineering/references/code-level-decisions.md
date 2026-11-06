# Code-Level Decisions

**Read when:** writing or reviewing the inside of a function, class, or module, and a choice about
names, comments, representations, mutable state, side effects, errors, absence, or assertions affects
correctness or how easily the code is understood.

## Contents

- Names
- Comments
- Representations
- Mutable state and side effects
- Contracts, validation, and assertions
- Absence and edge cases
- Errors at the right boundary
- Resources

## Names

- A name states what something means, including units and effects: `timeoutMs`, `deleteIfExpired`.
  Scope sets length: a loop index can be `i`; a module-level value needs a descriptive name.
- **Use one name for one purpose, consistently.** Example: a file-system bug came from the name `block`
  being used for both file-relative and disk-relative block numbers. A reader assumed one meaning where
  the code held the other. Consistent names such as `fileBlock` and `diskBlock`, with `src`/`dst`
  prefixes when two are needed, prevent it.
- Rename as understanding improves. A name that no longer fits misleads every later reader.

## Comments

Comments record what the code cannot say: why it exists, invariants, units, which end of a range is
inclusive, required call order, and the abstraction a module offers. An abstraction-level comment says
what a method guarantees afterwards, such as a bandwidth cap that holds once it returns, so callers
need not read its code. Do not restate the code. Keep
comments accurate when the code changes, and delete those that describe code that no longer exists.

## Representations

Use types that carry meaning when confusion is credible: units, ranges, identifiers that must not mix,
money, and time zones. Keep a primitive when its meaning is already clear. Choose collections by their
semantics, such as ordering, uniqueness, or keyed lookup. Make invalid states unrepresentable where the
language supports it.

## Mutable State and Side Effects

- **Keep mutation local** and give shared state one owner and a synchronization policy. Derive values
  from their owner instead of storing copies that must be kept in sync.
- **Name every effect.** Example: a password-checking function that also initializes the session. A
  caller who trusts the name can erase an existing session, and the function now has a hidden ordering
  requirement. Separate the effect, or name it.
- **Separate commands from queries.** A function that both sets an attribute and returns whether it
  succeeded reads ambiguously at the call site: is it asking or doing? A query
  should not change state; a command should not need to be read as a question.
- Do not hide I/O, initialization, or a required call order inside an innocent-looking getter.

## Contracts, Validation, and Assertions

Three different tools:

| Tool | Use for | Not for |
| --- | --- | --- |
| Types and contracts | What callers must provide and what the function guarantees | Checking untrusted input at runtime |
| Runtime validation | Untrusted or expected-bad input at a trust boundary | Re-checking values already guaranteed inside |
| Assertions | Internal states that must be impossible | Required behavior, or input a user can supply |

An assertion must never carry a required effect. Example: an assertion that advances an iterator while
checking it makes the loop silently process only half the elements. State failure behavior as part of
the contract.

## Absence and Edge Cases

- **Keep distinctions that matter:** empty data, a missing value, invalid input, and a failed operation
  need different handling. Never turn a lost write or a denied permission into "empty".
- **Define errors out of existence when the promise still holds.** A command that removes a
  variable can promise "the variable no longer exists", so removing a missing one is not an error. Unix
  deletes an open file by removing its name and keeping the data until it is closed, where Windows refuses.
  A substring function can return the overlap of the requested range instead of throwing on
  out-of-range indexes.
- **Use a special-case object when it simplifies callers.** Example: an expense total needs a
  per-diem amount when no meals were expensed; returning a per-diem object instead of throwing removes
  the special case from every caller. Returning null instead forces nested null checks, and one missing
  check fails far from its cause.
- Define behavior for zero, one, many, boundaries, duplicates, and unusual characters where the
  contract can encounter them.

## Errors at the Right Boundary

Detect a failure close to its cause and keep the context needed to act on it. Recover only where the
operation's promise can still be kept; otherwise propagate it, or stop the affected operation at a
boundary that prevents corruption. Never swallow an exception, and never report a partial failure as
success. Do not expose internal details or secrets in user-facing errors. Follow the language's and the
repository's error conventions; exceptions and result values are both valid when used consistently.

## Resources

Make acquisition, ownership, and release explicit for files, connections, locks, transactions,
subscriptions, and temporary files. Prefer scoped constructs (`with`, `using`, `defer`, try-with-
resources) so cleanup also runs on failure and cancellation. Test the failure path's cleanup, not only
the happy path.
