---
name: change-verification
description: Select and execute repository-required proof for a non-trivial change, diagnose CI failures or assess readiness to deliver. Skip a prose typo unless project policy requires more.
---

# Change verification

Establish what the change must prove, then use the repository's owning test/review skill or documented
commands. This skill routes to policy; it does not add a second test policy or universal command sequence.
Read [verification](../../../Steer-robust/verification.md) for proof boundaries, runtime checks or CI diagnosis.
For an explicitly requested review, use [evaluation](../../../Steer-robust/evaluation.md).

## Select applicable proof

Read scoped instructions, test guidance, relevant fixtures, templates and required gates.
Check whether the repository assigns broader suites or integration tests to CI; follow that policy.
Use its runtime, package manager, wrappers and existing harness. Do not install optional tooling by default.
An unfamiliar repository may benefit from the optional discovery helper in project-exploration;
reuse known valid guidance rather than scanning the repo for each test run.

Identify the changed contract and preservation case. Local decisions may need unit tests.
When unit/static checks cannot establish runtime, persistence, lifecycle, protocol or UI behavior,
use [runtime-qa](../runtime-qa/SKILL.md), or the project's equivalent, for scenarios and evidence.
Pass on the selected checks and known context; do not repeat discovery or execute duplicate suites.

Consider affected clients, providers, entrypoints and operating modes where the product has them.
Narrow selection needs a sound dependency/contract boundary: dynamic registries, generated schemas,
plugins and migrations can reach beyond static imports. Required broader checks remain required.

## Execute and diagnose

Run focused proof while iterating, then the applicable final gates. Stop adding checks once the contract
and required gates are established unless a new change, failure or unresolved risk justifies more.
For a regression, demonstrate that the check detects broken behavior when practical; qualify blocked reproduction.
Distinguish product failure, stale guidance, harness failure and unavailable environment before retrying.
Never bypass gates, mask failing commands or weaken assertions to obtain green output.
Reuse healthy task-owned services when appropriate; stop only resources this task owns.

Tie commands/results to relevant source and environment. HEAD alone does not identify uncommitted changes.
For CI, inspect the exact run/head and relevant logs; a newer list entry can belong to different code.
Refresh evidence invalidated by edits, rebases, dependency or environment changes.

## Close the authorized task

Inspect the final diff against intent, preserved guarantees, repository contracts and template requirements.
Report pass, failure, skipped, blocked and not run accurately; CI-owned/unavailable is not locally passed.
Human review, comprehension or community-writing requirements must be completed by the human when required.
Apply authorized feedback and required bot re-review commands against the updated revision.
Perform publication, messaging, installation or merge only within the human's authorization.
