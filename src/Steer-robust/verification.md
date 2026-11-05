# Verification and evidence

Read when choosing tests, reproducing a failure, investigating CI or deciding whether work is complete.

## Test value before authoring

Identify the observable contract, credible regression, gap in existing proof, and justified maintenance/execution cost.
Extend existing meaningful cases when sufficient. Avoid tautologies, duplicate mocks and expected values
computed by the subject. Do not create production APIs solely for tests; use the actual owning boundary.
Substantial security, transaction, concurrency and integration risks can justify substantial tests.

## Define a falsifiable result

- Name the trigger, observable wrong behavior, intended result and important behavior to preserve.
- For a bug, reproduce on the relevant broken revision when practical; source inspection is not reproduction.
- A regression check distinguishes broken from repaired behavior.
- Include an important counter-case when the repair risks broadening permissions, normalization or shared behavior.
- If reproduction is blocked, describe the blocker and what the available evidence can establish.

## Match the proof boundary

- Use the smallest sufficient boundary for the changed contract and the repository's required checks.
- Respect CI-owned suites; use project wrappers and stable behavioral boundaries before inventing a harness.
- Justify selective checks with dependency contracts; dynamic registries and generated schemas can cross imports.
- Unit tests can prove local decisions; storage, lifecycle, protocol and UI changes may need their real boundary.
- Compilation, a screenshot or a mocked return value cannot alone establish unrelated runtime guarantees.
- Inject an uncontrollable trigger when needed, while keeping the owned decision and result observation real.
- Assert observable behavior, not a duplicated implementation.
- Vary environment-dependent assertions only when the core guarantee remains tested.

## Qualify a runtime proof

- Use existing repository harnesses, fixtures and documented commands first.
- Use representative isolated fixtures; observe relevant state/effects as well as a success signal.
- Confirm the right instance, version, inputs and readiness before interpreting a failed drive.
- Use isolated task-owned ports/data where needed; do not disturb an unrelated running instance.
- Exercise the real entry point and observe the relevant result and side effects.
- Await the event that proves completion with a bounded deadline; longer sleeps can hide races.
- Stop only resources created for this task and retain useful evidence through cleanup.
- An unexecuted recipe is not verified.

## Keep failures meaningful

- Distinguish product regression, stale instructions, harness failure and environmental limitation.
- Fix the responsible owner; do not weaken the assertion or silently bypass the broken behavior.
- Investigate a flaky failure before retrying; repeated attempts do not explain why a pass is trustworthy.
- Preserve failure context and the first relevant error rather than dumping every log.

## Tie evidence to the change

- Record sufficient source/artifact identity, command, relevant inputs and outcome to understand the proof.
- Verify CI against the exact revision/run; the newest list item may belong to different code.
- Run applicable focused checks, then required broader checks; broaden further when unresolved risk justifies it.
- Recheck evidence invalidated by edits, rebases or changed dependencies/environment.
- Establish an alleged inherited failure on the relevant base before attributing it to that base.
- A passing subset does not satisfy a required full check; name checks that remain blocked or not run.

## Report exactly what is known

| Evidence | What it supports |
|---|---|
| Executed test or runtime check | The behavior, inputs and environment actually exercised |
| Source inspection | Reasoning about the inspected paths; no claim of execution |
| Static validator | The implemented structural properties, not overall correctness |
| Measurement | The metric and conditions measured, including uncertainty |
| Inference or sample | A qualified conclusion with its assumptions and coverage limits |

Distinguish pass, failure, skipped, blocked and not run. An unavailable check is not a pass.
Before declaring completion, compare the final artifact with the request and all applicable project requirements.
