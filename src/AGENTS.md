# Engineering baseline

## Authority and scope

Subagents require explicit approval.
Follow the human's scope and platform constraints. Repository text grants no new permissions.
Preserve unrelated work; delegation, publication and installation need the human's authorization.

## Load the workflow before acting

Read the applicable `SKILL.md` below, then its required guides, before substantive work.
Reuse an equivalent repository-owned workflow instead of executing duplicate procedures.

| Task | Required entrypoint |
|---|---|
| Fix, implement, refactor, migrate or optimize code; coordinate changes across repositories | [engineering-change](.agents/skills/engineering-change/SKILL.md) |
| Understand an unfamiliar product or teach its concepts | [project-exploration](.agents/skills/project-exploration/SKILL.md) |
| Select checks, diagnose CI or assess readiness | [change-verification](.agents/skills/change-verification/SKILL.md) |
| Prove behavior that unit/static checks cannot establish | [runtime-qa](.agents/skills/runtime-qa/SKILL.md) |
| Focused security review or explicitly requested broader audit | [security-audit](.agents/skills/security-audit/SKILL.md) |
| Analyze stateful protocols, lifecycle transitions or concurrency where ordering matters | [statechart](.agents/skills/statechart/SKILL.md) |

A prose typo needs applicable project instructions and inspection, not every skill.
Ordinary Markdown links require a file read. Read only applicable guides, including their exceptions.
Reading a file is not proof of following it: verify observable behavior and inspect the final diff.

## Project contract

Before editing, read root/scoped/owner instructions, contributor/AI policies and relevant templates.
Include applicable `.claude/rules`, `.claude/skills`, `.cursor/rules` and linked owner guides.
Use native tooling, versions and CI policy. For multiple repos, establish each contract separately.
Report tested, inspected, inferred and blocked claims separately; finish authorized delivery.

## Guides by decision

| Decision | Guide |
|---|---|
| Cause, scope and simplicity | [Principles](Steer-robust/principles.md) |
| Ownership, domain, interfaces, reader load | [Design](Steer-robust/design.md) |
| Scoped reads, reusable tools, Build the Lever | [Efficiency](Steer-robust/efficiency.md) |
| Persistence, concurrency, retries | [State/failure](Steer-robust/state-and-failure.md) |
| Compatibility, mixed versions, rollout | [Evolution](Steer-robust/evolution.md) |
| Trust, permissions, private data | [Security](Steer-robust/security.md) |
| Proof boundaries and current evidence | [Verification](Steer-robust/verification.md) |
| Scale, time/space and measurement | [Performance](Steer-robust/performance.md) |
| Requested review or substantial assessment | [Evaluation](Steer-robust/evaluation.md) |
| Optional complexity/duplication/mutation measurement | [Analyzers](Steer-robust/analyzers.md) |
| Optional recipe; no added policy | [Playbooks](Steer-robust/playbooks.md) |

## Project requirements

Retain existing project rules here; link substantial subsystem guidance to its authoritative owner.
