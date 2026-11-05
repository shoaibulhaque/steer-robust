---
name: runtime-qa
description: Reproduce and verify product behavior through real runtime boundaries, with reviewable before/after evidence for fixes, features and PRs. Use when unit or static checks cannot prove the outcome; skip prose-only edits.
---

# Runtime QA

Prefer the project's QA skill and harness. Reuse established checks and context; avoid duplicate
discovery and execution. This workflow supplies behavioral scenarios and evidence.
Repository policy owns required gates.

## Choose the claim and boundary

State the trigger, observable outcome, responsible owner and guarantee to preserve.
For a bug, reproduce on the relevant base when practical. For a feature, define its acceptance case;
do not invent a failing historical baseline. Record blocked reproduction honestly.

Use [scenario selection](references/scenarios.md) for the affected surface only.
Choose the cheapest boundary that can falsify the claim. Keep the changed decision real; label every
fixture, simulated dependency and unexercised live boundary. Static inspection is not runtime proof.

## Drive and observe

1. Confirm source/build identity, intended instance, inputs and event-based readiness before driving it.
2. Exercise the user entry point and observe the completed result and consequential side effects.
   A tool returning success, queued job or early preview does not establish completion.
3. Check a relevant preservation or failure case. For lifecycle changes, establish allowed behavior
   first, then drive the competing transition and verify that forbidden downstream effects stay absent.
4. Repeat equivalent inputs after repair; compare behavior, not just aggregate scores or page height.
   Inspect screenshots when appearance matters, alongside computed/structural and interaction evidence.
5. Complete project-required checks. Classify failures before retries; retain failed attempts separately.
   Do not mix passing observations from incompatible sources, configurations or attempts.

Use isolated fixtures, accounts, ports and data appropriate to the task. Use existing authorized access;
missing credentials do not justify weakening a gate or switching to production. Subagents need human approval.
Cleanup covers partial setup and failed drives. Stop only owned resources; reconcile uncertain writes
before retrying. A cleanup failure remains visible even when assertions passed.

## Qualify and deliver

For a PR or nontrivial proof, use [reviewable evidence](references/evidence.md); scale the record to the claim.
Bind observations to the tested source, package and relevant runtime identity. Invalidate affected evidence
after changes; HEAD alone does not identify a dirty tree or installed executable.

Report verified behavior separately from required-check readiness: pass, fail, skipped, blocked and not run.
Check CI against its exact head/run; pending approval is not a pass. Finish authorized delivery and any
applicable bot re-review without treating QA as permission to publish, deploy or message others.

Stop when the contract, preservation case and required gates are resolved. Surface the precise remaining
dependency when they are not. Do not claim universal correctness or guaranteed acceptance from a sample.
