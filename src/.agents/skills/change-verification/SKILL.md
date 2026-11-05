---
name: change-verification
description: Select and execute repository-required checks, diagnose CI failures or assess readiness after substantive changes. Skip prose-only edits unless project policy requires checks.
---

# Change verification

Read [verification](../../../Steer-robust/verification.md) before selecting or interpreting proof.
That guide owns regression/preservation tests, meaningful boundaries, current evidence and failure classification.
Use the repository's existing verification skill, fixtures, wrappers and CI split first.
Do not create a parallel test policy, scan the repository again or install tools by default.

Name the changed contract and one important preservation case.
Choose tests that can fail for the original defect; exercise the owned decision instead of mocking it away.
Check that required tests actually execute assertions and that a skip is not counted as a pass.
For branch-heavy logic where assertion strength is uncertain, selectively use
[existing analyzers or mutation tools](../../../Steer-robust/analyzers.md); they are optional, not universal gates.

When local unit/static checks cannot establish the claim, load [runtime-qa](../runtime-qa/SKILL.md).
Pass the selected checks and known context. Runtime QA owns scenarios and evidence, not additional CI policy.
For ordering/protocol defects, [statechart](../statechart/SKILL.md) can expose a sequence to replay in code.
A model checker is not implementation verification.

Run relevant focused checks, then required final gates, respecting CI-only suites.
Investigate failures before retrying; never mask errors, weaken assertions or bypass gates.
Tie CI to the exact head/run and invalidate proof affected by code, fixture or environment changes.
Stop adding checks once the contract and gates are established unless a new unknown warrants more.

Inspect the final diff and project templates. Report behavior separately from gate readiness:
pass, failed, skipped, blocked and not run. Human-only obligations remain with the human.
Complete authorized feedback and re-review actions; this skill grants no publication or messaging permission.
