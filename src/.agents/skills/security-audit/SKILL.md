---
name: security-audit
description: Review security questions or source-grounded vulnerability candidates. Use focused scope by default; expand coverage only for an explicitly requested broader audit. Not a mandatory audit of ordinary edits.
---

# Security audit

This Steer-owned sequential workflow adapts Cloudflare's security-audit methodology.
Read [security](../../../Steer-robust/security.md) for shared trust/permission rules and
[validation/reporting](references/findings.md) for classification and falsification before judging a candidate.
[Attribution and license](NOTICE.md) apply. No subagents, extra model calls or hunting waves are required.

## Scope and coverage

Default to the requested finding, boundary or changed path. A skill activation does not authorize a full audit,
new report files, target execution or testing deployed systems.
For an explicitly requested broad audit, name the reviewed revision, entrypoints and trust boundaries;
track inspected, excluded, blocked and remaining areas in a concise report. Never claim complete coverage
from a search or a passing subset. Stop at the authorized scope and disclose incomplete areas.
Reuse exploration already performed; do not build a second architecture map or evidence framework.

Load only relevant attack detail:
- Identity, tenancy, object permissions, revocation or HTTP credentials:
  [access boundaries](references/access.md).
- Injection, filesystem access, outbound requests, tool execution or resource exhaustion:
  [input and effects](references/inputs.md).
Use existing project security guidance for specialized protocols instead of importing an exhaustive catalog.

## Trace, challenge, classify

Name the lower-trust principal/input, real entrypoint, transforms/controls, sink/resource and violated guarantee.
Read callers, owners and relevant framework/dependency contracts; show a reachable attack path with source lines.
Then try to disprove it: reconstruct the strongest validation, binding, authorization and containment controls.
Intended same-principal capabilities, missing hardening and alarming syntax are not vulnerabilities by themselves.
Separate duplicate symptoms from the responsible root cause. Keep concrete supporting and refuting evidence.
Use `confirmed`, `needs_validation` or `rejected` as defined in the reporting reference.
Source reasoning must be complete before confirming without execution; label it as source proof, not reproduction.

## Safe execution and delivery

Source inspection is the default. Execute untrusted target code only in an authorized OS-enforced sandbox:
no external network, allowlisted clean environment, no credentials/sockets/host home, read-only source/toolchain,
scratch-only writes and explicit CPU/memory/process/disk/time limits. If these cannot be enforced, do not run it;
report the execution blocker and bounded owner-validation plan. Do not install dependencies or probe live services.
Use dummy data and minimal effects. Never promote untrusted files by recursive copy or follow their symlinks.
Existing [runtime QA](../runtime-qa/SKILL.md) can supply a proof recipe only when these controls are satisfied.
Report findings and gaps; an audit does not authorize source edits, publication or escalation of access.
A same-agent challenge is valuable but is not independent verification.
