# Writing Good Tests

**Read when:** writing or changing tests, adding mocks or other doubles, adding test helpers or
cleanup, working with legacy code, or doubting that a passing test can reject a plausible defect.

## Contents

- Overview
- Principle 1: Name the break
- Principle 2: Exercise the real thing
- Legacy code: characterize, then specify
- Tests ship with the implementation
- The mutation check
- Quick reference
- Warning signs

## Overview

A test exists to catch a specific break. Two principles govern everything here:

```text
1. Every test names the break it catches.
2. Every test exercises the real thing.
```

Strict TDD produces both naturally: a test written first and watched failing against real code has
already proven it can fail, and it earns a double only when the real dependency is slow or external.

## Principle 1: Name the Break

Before writing the test body, answer: **what production change should make this test fail, and is that
change a bug or a decision?** A test earns its place by catching a wrong branch, a missing side effect,
a wrong argument, a boundary case, or a broken contract.

**Derive expectations independently.** Use literals and hand-checked fixtures; table-driven tests with
literal expected values are the preferred shape. An expectation computed by the code under test, or by
its helpers, passes no matter what that code does:

```typescript
// ❌ Mirror assertion: the same builder computes both sides, so it is always true
const expected = buildSearchQuery({ tag: 'urgent' });
expect(buildSearchQuery({ tag: 'urgent' })).toBe(expected);

// ✅ Hand-derived literal
expect(buildSearchQuery({ tag: 'urgent' })).toBe('tag:"urgent"');
```

**No change detectors.** If only intentional decisions can fail a test (a constant's value, exact
message wording, private structure), it fires on redesign and sleeps through bugs. Test the behavior
that depends on the decision: not `expect(MAX_RETRIES).toBe(5)`, but "a failing call is retried five
times and a sixth attempt never happens." Exact text, ordering, and schemas are valid assertions when
they are the public contract.

**Behavior, not text.** Asserting that a script or configuration file contains an exact line proves only
that the source is the source. Run scripts against controlled inputs and assert outputs, side effects,
or exit codes. Exercise the artifact consumers actually receive. Prose written for humans earns no test.

**Your code, not the framework.** Test the contract your code makes at its boundaries: the route you
register, the query you emit, the payload you produce. Upstream mechanics are their maintainers' tests;
asserting that your router invokes a registered handler is the framework's test, not yours. When
upstream behavior genuinely surprised you, write one narrow characterization test naming the assumption.
The same boundary applies inside your code: constructors, getters, constants, and trivial forwarding earn
tests only when they validate, normalize, default, derive, enforce, or cause side effects. Otherwise,
assert the first consumer-visible result that depends on them.

### Gate Function

```text
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior
                               that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or a hand-checked fixture.
```

## Principle 2: Exercise the Real Thing

**A mock's presence earns no assertion.** An assertion that passes when the mock is present and fails
when it is absent says nothing about the component. Assert the real component's behavior. If the mock
is what you are checking, unmock it or delete the assertion. Ask: "Are we testing the behavior of a mock?"

```typescript
// ✅ Real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();

// ❌ Mock existence
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

**Mock at the right level.** Learn every side effect of the real method before replacing it. Mock the
slow or external operation, and keep real whatever the test depends on. When unsure, run the test
against the real implementation first and observe what actually needs to happen.

```typescript
// ❌ The mock swallows the config write that duplicate detection reads
vi.mock('ToolCatalog', () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
}));

// ✅ Mock only the slow server startup; the config write stays real
vi.mock('MCPServerManager');
```

**Make doubles specific.** When arguments, call counts, destinations, or ordering are part of the
contract, assert them: a notification must reach the right tenant, or a cancelled action must never be
issued. A fake that accepts anything verifies nothing. Give each branch (success, error, malformed) its
own fixture or spy, so the wrong branch cannot satisfy the expectation. A spy proves the interaction;
it does not prove delivery, durability, or wire compatibility. Use an integration check for those.

**Mirror real data completely.** Mock the complete structure as it exists in reality, with all
documented fields, not only the ones the test reads. Partial mocks fail silently when downstream code
reads an omitted field: the test passes while integration breaks. Match real nullability and failures.
A minimal fixture is acceptable only when the omitted fields cannot affect the scenario.

**Production classes carry production methods only.** Cleanup that only tests need lives in test
utilities, never as a `destroy()` on the production class. Ask: is this method called only from tests?
Does this class own this resource's lifecycle? A class that truly owns a resource still exposes its real
lifecycle operations, even if a test is their first caller.

**Prefer real components over complex mocks.** When mock setup outgrows the test logic, mocks miss
methods the real components have, or tests break when the mock changes, switch to an integration test
with real components. Ask: "Do we need to be using a mock here?"

### Gate Function

```text
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test
  depends on real, and mock the slow or external level below them.

  Mock responses mirror the complete real structure.

  A method that only tests call lives in test utilities, not production.

  Only checking that a mock or placeholder exists?
    Assert the real component's behavior, or remove the meaningless assertion.

  Checking arguments, counts, destinations, or ordering required by the contract?
    Keep the precise interaction assertion. It does not prove real delivery or durability.
```

## Legacy Code: Characterize, Then Specify

Before changing untested code, observe its current behavior and record representative cases as
characterization tests. A characterization test describes what the code does; a regression test
specifies what must change. Label a known defect as the behavior to change, not a permanent invariant.
New requirements need independently specified expectations.

## Tests Ship With the Implementation

The cycle of failing test, minimal implementation, and refactor is what "complete" means. Ship the tests
the behavior needs and only those: trivial code and human prose earn none, and a test written to satisfy
process costs maintenance forever. Use isolated fixtures, bounded external operations, and owned cleanup.
Tests must pass in parallel and in any order. Replace sleeps with the project's synchronization utilities
or a controlled clock; time-based behavior still needs timing assertions that match its contract.

## The Mutation Check

Before finishing, mentally mutate the production code. At least one test should fail for each realistic
mutation:

- Wrong constant or argument.
- Wrong branch handler.
- Missing state change or side effect.
- Empty or default return.
- Missing validation for zero, empty, nil, unauthorized, or malformed input.

A mutation nothing catches marks the behavior as unprotected, or the test as tautological. When unsure,
try the mutation in an isolated copy or use the project's existing mutation tooling. No blanket mutation
score is required. A test that fails only because setup broke does not prove its assertion works.

## Quick Reference

| When you... | Do |
| --- | --- |
| Write any test | Name the break it catches: a bug, not a decision |
| Build an expected value | Derive it by hand, never with the code under test |
| Test a script or generated artifact | Run it and assert its effects; never grep its text |
| Reach for a dependency test | Test your boundary contract, not the dependency's documented mechanics |
| Want to assert on a mocked element | Test the real component, or unmock it |
| Are about to mock a method | Learn its side effects; mock the slow or external level |
| Need to assert an interaction | Assert exact arguments, order, and counts; do not claim delivery |
| Build a mock response | Mirror the real structure completely |
| Need cleanup only tests use | Put it in test utilities |
| Watch mock setup balloon | Switch to an integration test with real components |
| Change untested legacy code | Characterize the affected path, then specify the change |
| Finish a test file | Run the mutation check |

## Warning Signs

- Setup and assertion share the same object, guaranteeing equality.
- The test can fail only through a panic, a crash, or a missing selector.
- The test fails on every intentional change and never on accidental breakage.
- Expected values are hidden behind loops, builders, or helpers.
- The test greps source text, or asserts that a removed symbol stays removed.
- The test would still matter if only the framework remained.
- The test exists for coverage and checks no side effect or outcome.
- An assertion checks a `*-mock` test ID, or fails if you remove the mock.
- A method is called only from test files.
- Mock setup is more than half the test, or you cannot explain why the mock is needed.
- Mocking "just to be safe".
- The test depends on run order, shared fixture state, or a sleep.
- The test was never selected by the run that "passed", or a wrapper swallowed its failure.
