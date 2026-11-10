# Steer Robust

Portable engineering guidance for coding agents. One short `AGENTS.md` holds universal defaults for
every repository. Six focused skills load only when a task needs them.

**Status:** v0.7.0 candidate. The package tests and deterministic build passed in CI;
comparative agent-behavior evaluation is still pending. See [Evaluate before adoption](#evaluate-before-adoption).

Everything is Markdown: no runtime dependencies, hooks, scripts, installers, or orchestration.

## What Is Included

| Component | Loads when | Does not cover |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | Every session, as durable defaults | Stack commands or skill activation |
| [test-driven-development](skills/test-driven-development/SKILL.md) | Implementing testable behavior or explicitly planning test-first cases | Pure refactoring or changes without observable behavior |
| [refactoring](skills/refactoring/SKILL.md) | Planning or performing behavior-preserving restructuring, including legacy code | Adding behavior or redesigning a contract |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | Diagnosing or planning investigation of an unclear failure | Defects with an established cause and failing test |
| [architecture-engineering](skills/architecture-engineering/SKILL.md) | Greenfield/brownfield system planning, design choices, migrations, or preventing coupling in multi-module work | Routine local edits, pure refactoring, root-cause diagnosis, or patch-readiness review |
| [change-verification](skills/change-verification/SKILL.md) | Patch or PR review, merge readiness, or specific change-verification plan | Routine implementation or generic planning |
| [security-engineering](skills/security-engineering/SKILL.md) | Planning or conducting a security review, threat model, or hardening | Ordinary feature work or generic review |

Each responsibility has one owner:

- **TDD** owns the red–green–refactor cycle and test design.
- **Refactoring** owns behavior-preserving restructuring and bringing legacy code under test.
- **Debugging** owns causal investigation.
- **Architecture engineering** owns architecture planning, consequential design decisions, and preventing new coordination or coupling. Conditional references handle new systems, existing systems, migrations, change locality, and quality tradeoffs.
- **Change verification** owns requested review.
- **Security engineering** owns specialist security analysis.

A task can use more than one skill, but no skill loads another automatically.

## Planning vs. Execution

Skills apply to the *problem*, not just the act of coding. A plan-only request permits scoped investigation and proposed design, tests, or verification, **not implementation**. Architecture plans use `architecture-engineering`, refactor plans use `refactoring`, diagnosis plans `systematic-debugging`, test-first plans `test-driven-development`, specific patch verification plans `change-verification`, and security plans `security-engineering`.

Do not load every skill just because the user asks for a plan. Choose greenfield, brownfield, or hybrid guidance based on actual system context. Small plans may require none. Plans should distinguish evidence from assumptions, name meaningful owners and steps, and state how success would be checked without claiming the checks were run.

## How Loading Works

1. **Metadata.** At startup the agent sees each skill's `name` and `description`. Each description
   says when to use the skill and when not to.
2. **Body.** The agent reads a `SKILL.md` only after it selects that skill.
3. **References.** Each file in `references/` is linked with a "read when" condition and is read only
   when that condition holds. References never link to further references.

License and notice files are legal notices, not instructions.

## Install

Nothing installs itself. Inspect your existing instructions and skills first, then choose one scope
per item: personal (all projects) or project (one repository). Do not install the same defaults or the
same skill in both scopes.

### Defaults

`AGENTS.md` is the universal base. Use it unchanged across projects and append project-specific
rules after it.

| Client | Personal scope | Project scope |
| --- | --- | --- |
| Codex | `~/.codex/AGENTS.md` | `<project>/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` | `<project>/CLAUDE.md` |
| Other agents | The client's documented instruction file | `<project>/AGENTS.md` is widely read |

- Merge with any existing file; keep existing preferences and do not duplicate a rule already present.
- In Codex, a non-empty `AGENTS.override.md` in the same directory takes precedence over `AGENTS.md`.
- For repository-specific rules, copy [the project template](templates/project-instructions.md) to the
  end of the project's file, fill it in, and delete its instructions and unused sections. With personal
  defaults installed, the project file needs only the project-specific section.
- More local instruction files refine broader ones for their directory. They never grant additional
  authorization.

### Skills

Copy each selected skill as a complete folder, including `references/` and any license files.

| Client | Personal scope | Project scope |
| --- | --- | --- |
| Codex | `~/.agents/skills/<name>/` | `<project>/.agents/skills/<name>/` |
| Claude Code | `~/.claude/skills/<name>/` | `<project>/.claude/skills/<name>/` |
| Other agents | The client's documented skills directory | The client's documented skills directory |

- Stop if a skill with the same name already exists; do not merge directories blindly.
- Keep only one TDD skill per setup.
- This checkout's `skills/` directory is not a discovery location; copy from it.
- Restart the client if new skills do not appear.
- Do not copy `research/`, `dev/`, `templates/`, or `EVAL_PLAN.md` into a skills directory.

### Update and Uninstall

Compare with the installed files first. Replace only unchanged files that this kit owns, and merge
local edits by hand. Keep project appendices and unrelated skills. If an earlier version installed
`evidence-debugging`, replace it with `systematic-debugging`; do not keep both.
For v0.7, replace the kit-owned `repository-engineering` and `design-for-change` folders with
`architecture-engineering` after checking for local modifications. Preserve local customizations by
merging them deliberately. Do not keep the retired skills alongside the replacement: their overlapping
metadata can compete for the same request.

To uninstall, remove the kit's skill folders and the instruction text you added. Remove an instruction
file only if nothing else remains in it. Never remove shared directories, unrelated skills, or other
configuration.

## Repository Layout

```text
AGENTS.md                              Universal defaults
skills/<name>/SKILL.md                 Skill entrypoints
skills/<name>/references/              Conditional detail, read on demand
skills/<name>/LICENSE.txt              License for included third-party material
skills/security-engineering/NOTICE.md  Modification notice
templates/project-instructions.md      Project appendix template
EVAL_PLAN.md                           Evaluation protocol
research/                              Maintainer design notes, not runtime guidance
dev/                                   Package builder and its tests
```

## Validate and Build

Requires Python 3.9 or later; no third-party packages.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s dev -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 dev/build_package.py
```

The builder checks skill metadata, local links, code fences, and the exact set of files in each skill.
It then writes `dist/steer-robust-v0.7.0-candidate.zip` from an explicit allowlist with deterministic
metadata. The tests extract the archive and validate the extracted copy. Development files, design
notes, raw traces, and local configuration are excluded from the archive, and `dist/` is not committed.

## Evaluate Before Adoption

Structural checks show the package is well formed. They do not show that an agent selects the right
skill, follows it, or produces better changes. Before adopting a skill, compare it with your current
setup using the [evaluation protocol](EVAL_PLAN.md): positive and negative trigger probes,
outcome-based grading, and cost per accepted result.

## License

MIT; see [LICENSE](LICENSE). Skill folders that include third-party material carry its original
license in `LICENSE.txt`, plus `NOTICE.md` where the license requires one.
