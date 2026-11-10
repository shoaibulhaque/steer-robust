# Writing Good Tests

**Read when:** choosing doubles, handling difficult fixtures, protecting legacy code or assessing
whether a passing test can reject a plausible defect. Keep ordinary examples simple.

## Overview

1. Name the break the test catches.
2. Exercise the real behavior at the boundary where the promise can be observed.

## Principle 1: Name the Break

Before writing the body, identify a wrong result, omitted effect, violated invariant or unsupported
boundary case that should fail. The oracle must come from a requirement, hand-checked fixture or
independent property—not from the same production function or algorithm being tested.

```python
# Weak: both sides use the implementation being checked.
expected = build_query("urgent")
assert build_query("urgent") == expected

# Stronger: a requirement-derived literal checks the public representation.
assert build_query("urgent") == 'tag:"urgent"'
```

Exact text, ordering, constants and schemas are valid assertions when they are the public contract.
Avoid freezing private structure merely because it happens to exist. Test the behavior affected by a
retry limit, not only the limit's numeric declaration. Run scripts or extracted artifacts against
controlled input; matching source text does not establish their behavior.

For legacy characterization, observe existing behavior before changing it and retain representative
cases. Label a known defect as the behavior to change, not a permanent invariant. New requirements
need independently specified expectations; characterization and specification serve different goals.

### Gate Function

- What plausible production mistake would make this fail?
- Does the assertion observe that mistake, or only repeat setup/the implementation?
- Is the expectation independent and the boundary appropriate?
- If no useful distinction exists, redesign the check or do not add it.

## Principle 2: Exercise the Real Thing

Keep the logic under test real. Substitute slow, nondeterministic or external collaborators at a
supported seam when needed, preserving the effects on which the test depends. Match the real response
contract for relevant fields, nullability and failures; a minimal fixture is acceptable when omitted
fields cannot affect the scenario. Do not fabricate a whole unrelated payload for ceremony.

**Interaction assertions can be legitimate.** Arguments, destinations, counts and order may define a
contract: a notification must be sent to the right tenant, or a cancelled action must never be issued.
A spy can observe that interaction. It does not prove delivery, durability or real wire compatibility;
use an appropriate integration check for those claims.

Place test-only fixture helpers in test support. Production resource owners should still expose real
lifecycle operations even if a test is their first caller. Classify by responsibility, not caller count.
When doubles become more complex than the behavior or miss real semantics, prefer a focused integration
check over rebuilding the dependency inside the test.

### Gate Function

- Which real effects does the scenario depend on, and does the double erase them?
- Is the asserted interaction itself a requirement, or only evidence that a mock exists?
- Which important real boundary still needs separate verification?

## Tests Ship With the Implementation

Use isolated fixtures, bounded external operations and owned cleanup. Preserve suite behavior in
parallel and different orders. Avoid sleeps for readiness; use the project's synchronization utilities
or controlled clock. Time-based behavior still needs timing assertions appropriate to its contract.

## The Mutation Check

Consider a representative wrong branch, argument, omitted write or missing rejection. Would the test
fail for that mistake while accepting an independent correct implementation? If uncertain, try a
bounded mutation in an isolated copy or use existing project tooling. No blanket mutation score or
new analyzer is required. A test failing only from broken setup does not prove its assertion works.

## Quick Reference

| Situation | Prefer |
| --- | --- |
| Repeated expected values | Independent literals or well-founded properties |
| Legacy uncertainty | Characterize the affected path, then specify the intended change |
| Slow external boundary | A faithful narrow double plus relevant real-contract evidence |
| Interaction is the requirement | Precise arguments/order/counts without claiming delivery |
| Mock setup dominates | A smaller seam or focused integration check |
| Generated/configured artifact | Exercise the artifact that consumers actually receive |

## Warning Signs

Mirrored oracles, never-selected tests, swallowed failures, fixture state shared across tests, assertions
on a mock placeholder, or a test that survives the defect it supposedly catches require reassessment.


## Worked Case: Authorization with an Observable Denied Effect

**Requirement:** a user can request a report for their own tenant but not another tenant. Do not begin by testing that a permission helper returns a boolean; the meaningful contract is what the real request path permits and prevents.

Choose independent examples: tenant A's authorized user can create a job for tenant A; tenant B's user cannot create a job owned by A. The denied case should assert **both** the rejection and absence of any persisted job or external effect.

```python
# Illustrative integration-test shape; adapt to the real framework and contract.
response = client_as(tenant_b_user).post(
    "/reports", json={"tenant_id": tenant_a_id}
)
assert response.status_code == expected_denial_status
assert not report_jobs.exists_for(tenant_a_id, requested_operation_id)
```

The expected status comes from the API contract, not from the handler's current implementation. A unit test that mocks the job creator can verify a local interaction; it cannot prove that an alternate route or database write is blocked.

A useful red test should fail because unauthorized work is accepted **or** because the expected denial is missing. After implementation, verify the allowed path still works. No extra per-helper tests are required merely because a permission function was extracted.

**Counterexample:** asserting only "the endpoint returned 403" could pass even if the endpoint already queued the job before rejecting the request. The effect assertion is what distinguishes the actual invariant.
