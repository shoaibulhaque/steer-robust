---
name: change-verification
description: "Use when reviewing a patch, diff, branch, or PR, judging merge readiness, or planning verification of a specific change. Check correctness, contracts, design, and evidence strength. Not for routine implementation or generic planning."
---

# Change Verification

## Overview

Assess an existing change when a review or a readiness judgment is requested. Decide whether its
behavior, design, and evidence satisfy the repository's actual contract, and report what a maintainer
needs to act on.

**Core principle:** a claim is only as strong as the behavior its evidence actually exercises.

A review request does not authorize edits, pushes, comments on a hosted PR, or a second implementation
pass. Ask before doing any of these.

## When to Use

Use for an explicitly requested review of a patch, branch, or PR, or a merge or release readiness
judgment. Ordinary implementation and routine test runs do not need this workflow.

## Plan-Only Requests

For a verification plan tied to a specific change, map acceptance claims to discriminating checks, affected consumer revisions, failure and compatibility paths, and needed test environments. Do not issue merge-readiness verdicts or fabricate findings before evidence is gathered. Generic feature planning is not patch review.

## Workflow

### 1. Establish the Change and Its Contract

- Read the full diff against the intended base, including new, deleted, renamed, and generated files.
  Confirm the revision, so findings and evidence refer to the change being assessed.
- Read enough surrounding code to understand each changed path: callers, consumers, and invariants.
- Identify the stated intent: PR description, linked issue, or the user's request. A change that is
  correct but does not do what was asked is a finding.
- Read the repository's contribution rules, review templates, test guidance, and CI definitions.
  Use them instead of a generic checklist.

For a contract shared across repositories, inspect the producer and consumer revisions. Tests in one
repository do not prove the combination works.

### 2. Hunt for Defects

Trace each changed path with concrete inputs. Prioritize:

1. **Correctness:** wrong results, missed branches, off-by-one and boundary values, empty or absent
   input, type and unit conversions, and error paths that lose or mask failures.
2. **State and effects:** ordering, partial failure, retries that duplicate effects, races on shared
   state, and resources that are not released.
3. **Contracts:** public APIs, stored formats, configuration, migrations, and backward compatibility
   for the consumers the repository supports.
4. **Trust boundaries:** authorization, input validation, secrets, and injection where the change
   touches them. A dedicated security review is a separate request.
5. **Completeness:** callers not migrated, old paths left reachable, missing docs or generated output
   the repository requires.

Confirm each candidate defect by tracing a feasible trigger. Drop it if counterevidence shows the path
is unreachable or already protected.

### Security Impact of the Diff

For touched trust boundaries, trace **actor → actual entry point → enforcement → protected effect**.
Inspect relevant allowed and rejected paths, including tenant scope, validation, serialization, and
partial failures. The evidence should fail on a plausible unsafe outcome; mocked permissions and
scanner scores cannot prove enforcement across real callers.

An ordinary review does not become a full penetration test. Report a security defect only when
there is a credible triggering path and consequence, while distinguishing unknown exposure from
verified bypass. A dedicated deep review remains the security skill's responsibility.

### 3. Challenge Consequential Design Choices

- Does an existing owner or extension point already solve this? Look for parallel paths and rules
  scattered across modules.
- Does a new abstraction hide useful complexity, or only forward it? Count the indirections a reader
  must follow and the hidden state they must hold. One caller alone does not make a boundary useless.
- Is repeated code the same knowledge with the same reason to change? A shared helper driven by context
  flags can be worse than two independent implementations. Prefer domain ownership over cosmetic
  deduplication.
- Does added state, configuration, or defensive code protect a credible requirement? Inspect failure
  behavior, compatibility, and caller consequences before recommending removal.
- When performance justifies complexity, is there a representative workload, a baseline, and a
  measured result? Metric scores, small functions, and extra layers do not establish better engineering.

Recommend a simplification only when it preserves the required guarantees and has a concrete benefit.
Do not raise speculative architecture or unrelated cleanup as findings.

### 4. Test the Evidence

For each piece of evidence, ask: **could it pass while the claimed behavior is still broken?** If it
could, it does not support the claim.

- Reuse results that still apply to the same code, inputs, and environment. Rerun checks that the
  change invalidated or that repository policy requires.
- Inspect output and test selection, not only exit codes. An empty selection, a skipped suite, a setup
  failure, or a command that never ran proves nothing.
- For a local contract, check observable outputs and affected effects. Do not require a production
  replica for pure logic, and do not accept remote delivery proven only by a local fake.
- Check that expectations are independent of the implementation. A test that recomputes the same
  formula cannot verify it; a mocked call cannot prove a durable write.
- When assertion strength is uncertain, try a representative wrong implementation in an isolated copy,
  or use an existing selective mutation tool. Do not mandate mutation testing, and never modify the
  user's working tree to prove a test can fail.
- A changed expectation needs a reason from the requirements. A weakened assertion hides failures.

Read [Verification Across Boundaries](references/verification-boundaries.md) when a claim depends on
an integration, persistence, an installed or generated artifact, compatibility, or concurrency.

### 5. Report

Lead with the verdict: ready, ready with minor changes, or not ready, and why. Then list findings,
most severe first:

| Severity | Meaning |
| --- | --- |
| Blocking | A demonstrated defect, contract break, or data or security risk with a feasible trigger |
| Should fix | A real problem with limited impact, or missing evidence for an important claim |
| Optional | A simplification or clarity improvement with a concrete benefit |
| Question | Missing context that could change a conclusion |

For each finding, give the location, the triggering condition, the consequence, and a suggested fix.
State which checks passed, failed, were blocked, or were not run, and whether failures predate the
change. No findings is not proof that untested boundaries are safe; name what was not covered.

Stop when the requested scope and the repository's required evidence are covered. Do not rerun
unchanged broad suites or start other workflows automatically. If authorized fixes follow, review the
new diff and recheck only the affected evidence instead of restarting the whole review.

## Red Flags — Check the Proof

- Compilation or type checks cited as proof of behavior.
- A mock interaction cited as proof of a remote effect or durable write.
- A clean scanner result cited as proof of security.
- Evidence from a different revision or environment, used without a validity check.
- A test that passed on the first run and was never seen to fail.

Report the actual limit of the evidence; do not escalate every gap into a blocker.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| "CI is green, so it's ready" | Green CI proves only what CI selected and asserted. Check what it exercised. |
| "The tests were updated too" | Updated tests can encode the bug. Check that each expectation comes from the requirement. |
| "It's a small diff" | Small diffs break contracts. Trace the callers. |
| "I'd have designed it differently" | Preference is not a finding. Name a concrete cost or risk. |
| "Flag everything to be safe" | Inflated findings hide real ones. Each needs a feasible trigger. |

## Verification Checklist

- [ ] The diff, intent, and repository rules were read at the assessed revision.
- [ ] Each finding has a location, a feasible trigger, a consequence, and a severity.
- [ ] Each claim of correctness rests on evidence that would fail if the claim were false.
- [ ] Checks are reported as passed, failed, blocked, or not run; coverage gaps are named.
- [ ] No edits, pushes, or hosted comments were made without authorization.
