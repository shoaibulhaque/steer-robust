# Verification Across Boundaries

**Read when:** review claims depend on integration, persistence, generated/installed output, concurrency,
compatibility, or evidence whose validity is uncertain. A straightforward local patch may not need it.

## Overview

**Core principle:** verify the artifact and boundary that consumers depend on. Every check has a
scope; report that scope rather than substituting a cheaper proxy for the claim.

## 1. Connect the Claim to an Observation

| Claim | Relevant observation | Insufficient proxy |
| --- | --- | --- |
| A defect is repaired | Original trigger reaches the corrected behavior; a plausible wrong result is rejected | A new test passes without reaching the changed path |
| An external contract works | Real adapter/wire/storage semantics are exercised at appropriate fidelity | A fake returns the shape invented by the test |
| An installable artifact works | Extract/install the delivered artifact in isolation and exercise its consumer entry point | Source-tree imports or a successful archive command |
| A migration is safe | Supported old/new readers, writers and rollback cases preserve data/contracts | A clean all-new installation |
| A retry is safe | Response loss/repetition does not duplicate the protected effect | A mock was called once in the happy path |
| A lifecycle is correct | Required and forbidden transitions hold, including cancellation/failure ownership | Waiting until an eventually successful outcome |

Choose the narrowest check that can reveal the credible failure. Do not demand a full production
replica for pure logic, or claim an integration contract from unit isolation alone.

## 2. Inspect the Oracle and Harness

Confirm test selection, actual assertion results and whether setup completed. A wrapper can exit zero
after swallowing a failed test; an empty selection or skipped suite cannot establish passing behavior.
Likewise, an unrelated command failure does not erase valid earlier evidence—inspect the actual outputs.

Check independence of expectations. A wrong branch, omitted write, unauthorized access or incomplete
migration should be rejected, while a different correct implementation should still pass. Exact values
and interaction assertions are appropriate when they describe the public contract. Do not freeze
private structure or mistake high coverage for assertion strength.

Use existing selective mutation or controlled failure injection only when useful. Keep experiments in
isolated fixtures; never reset user changes or alter live systems merely to validate a test.

## 3. Establish Evidence Validity

Tie results to the actual revision, affected inputs, selected tests and relevant environment. Reuse
unchanged evidence when those assumptions remain valid; refresh it after meaningful invalidation or
when repository policy requires current-head checks. Do not rerun broad suites just for a new message.

For a multi-repository contract, inspect producer and consumer revisions and verify the supported
combination. One repository passing is not proof that its consumer has adopted the change. Include
configuration, generated outputs, platform/version obligations and delivery templates only as applicable.

## 4. Calibrate the Conclusion

Separate demonstrated defects, conditional risks, optional design suggestions and missing evidence.
A scanner lead needs reachability analysis; an unrun test is a limitation, not an automatic code defect.
Name concrete impact and a feasible trigger before escalating severity. State residual uncertainty
without turning every possible failure into a mandatory new project.

If authorized fixes follow review, inspect the new diff and recheck invalidated evidence. Preserve
still-valid observations and stop once the requested review scope is covered.
