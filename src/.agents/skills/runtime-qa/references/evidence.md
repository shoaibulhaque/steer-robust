# Evidence a reviewer can use

Read for a nontrivial runtime claim, a contribution or requested proof. Reuse the project's report format.
A short local result can suffice; do not require a new framework, persistent ledger or public artifact service.

## Bind the claim

Retain enough identity to rerun or assess the observation:

- **Source:** revision and relevant dirty diff or file hashes. Bind the final commit to the tested bytes;
  do not relabel old evidence after a rebase or edit. Test/fixture changes can invalidate proof too.
- **Execution:** command, exit status, runtime/dependency versions and relevant configuration/input.
  Record the installed package/build and actual instance when source HEAD does not identify what ran.
- **Boundary:** real owners exercised, simulated dependencies and untested provider/account/protocol surfaces.
- **Outcome:** assertions, observed values/effects, required checks, failures, skips and cleanup result.

Match identity detail to the claim. A local utility needs no account receipt; successful fake delivery
cannot establish live account behavior. A hash connects bytes but does not establish that they executed.

## Compact report template

Adapt fields to the task; omit irrelevant ones rather than filling them with invented certainty.

```text
Claim and preservation case:
Source/build/instance and relevant inputs:
Boundary exercised; fixtures and limits:
Before: command, exit/outcome, concrete observation (or why not applicable/blocked)
After: command, exit/outcome, concrete observation
Preserved/failure case: observed state and effects
Required checks: exact local results and CI head/run
Cleanup: owned resources released; unresolved effects
Artifacts: runnable fixture/command, logs, measurements, inspected images when useful
Readiness: verified behavior; outstanding gate/owner/action
```

Keep raw attempts distinct from summaries. Label selected retries and their reasons; preserve contradictory
or failed observations. Do not assemble one passing story from unrelated attempts or silently count
not-applicable checks as exercised coverage. A queued review or workflow is pending, not approval.

## Prepare evidence for a contribution

Use the repository's PR template. Lead with the concrete problem, resulting behavior and why this owner
is responsible. Include a small before/after example, exact tested commands and material limits.
Attach the executable fixture/test and concise observations. Do not commit large captures or generated
artifacts when the project excludes them. Local screenshots may support your inspection but are not
accessible to a remote reviewer; use an authorized project-supported attachment path when needed.

Read saved screenshots and output before referencing them. Check links from the intended audience's
access level. If a bot cannot fetch an artifact, include decisive observations and commands inline;
a link alone cannot close its proof request. Verify the published body/head matches the prepared result.
Request the project's prescribed re-review only within existing messaging authority; record its actual
queued/completed state without duplicate requests or invented approval.

Review logs, images and fixture data for credentials, personal data and private content before sharing.
Redact a shareable derivative while preserving the original according to project retention rules; label
redaction rather than changing the outcome. QA does not authorize new publication, accounts or billing.

## Close honestly

Separate **behavior verified** from **ready to merge/deploy**. Passing local checks with a required CI
approval outstanding is not fully ready. Skips, unavailable live services and failed cleanup remain explicit.
Evidence supports the exercised scenarios; avoid claims about every environment or guaranteed acceptance.
