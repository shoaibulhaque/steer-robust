# Steer Robust

A project-local engineering skill package for Codex and Claude Code.
Small entrypoints require relevant engineering guidance before decisions; detailed references load on demand.

## Workflows

| Skill | Purpose |
|---|---|
| engineering-change | Root cause, domain modeling, simplicity and coordinated code changes |
| project-exploration | Product-first understanding, ownership and teaching |
| change-verification | Native check selection, regression proof, CI and readiness |
| runtime-qa | Real product boundaries, preservation cases and reviewable evidence |
| statechart | Bounded TLA+/TLC safety checks and Mermaid counterexample paths |
| security-audit | Focused trust-boundary findings, falsification and honest classifications |

Canonical skill sources are in `src/.agents/skills/`, shared guides in `src/Steer-robust/`.
`AGENTS.md` is the essential entrypoint; skill bodies select procedures, guides own judgment,
optional scripts perform deterministic mechanics, and `dev/` plus `evals/` are development infrastructure.
Installed paths and all three original skill names remain usable. Authored templates moved from
`package/` to `src/`; developer commands moved from `tools/` to `dev/`.

## Adopt

```sh
gh repo clone shoaibulhaque/steer-robust
cd steer-robust
python3 dev/adopt.py /path/to/project --client both
```

This previews copying. `--apply` copies absent/identical files only; conflicts require manual merging.
Follow the [adoption guide](src/README.md#adopt-in-one-project) for existing project instructions.
Codex uses `.agents/skills/`; Claude uses `.claude/skills/` plus an instruction bridge.
Never overwrite project rules or install individual skill folders without their shared guides.

## Validate without model calls

Python 3.9+ and Git are sufficient. No Python package dependencies are required.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 dev/validate_package.py
PYTHONDONTWRITEBYTECODE=1 python3 dev/build_package.py
```

The builder validates/extracts `dist/Steer-robust.zip` and executes extracted helpers.
CI runs structural/helper tests. Grader controls and real CLI evaluations are opt-in, outside ordinary CI.

## Behavioral evaluation

The separate [evaluation suite](evals/README.md) runs real isolated Codex CLI tasks with and without the bundle.
Native prompt snapshots establish discovery; successful tool outputs establish actual file loading;
independent outcome and restored-bug tests check actions. Qualitative criteria are explicit; same-agent review is not independent proof.
No keyword-based success grading or worker self-report substitutes for execution.
See [research and audit](docs/refactor-research.md) for design choices and upstream implementation findings.
Measured results and limitations are recorded after actual runs; small fixture samples cannot guarantee adherence.

## Scope

Use the project's tools first. Build the Lever only when useful; metrics are evidence, not universal quotas.
Statechart uses optional supplied Java/TLC and one-worker breadth-first safety checking; model proof is not code proof.
No custom AST index, repo-map system, cache, memory/compaction machinery, MCP server or orchestration framework.
Native caching behavior is unchanged. No automatic subagents, dependencies, publishing or global installation.
Keep essential/skill instructions within 450 words and references within 650; code has no arbitrary line limits.
Distributed resources are separate from research clones, raw evaluations, private files and development tests.

[MIT license](LICENSE). Selected influences are attributed in the research notes; upstream code is not vendored.

## Repository boundaries

```text
src/             Canonical runtime instructions, skills, references and necessary helpers
dev/             Exact manifest, builder, validators, installation helper and regression tests
evals/           Public benchmark fixtures, deterministic graders and opt-in execution tools
docs/            Contributor-facing research, audit rationale and attribution
AGENTS.md        Instructions for maintaining this repository
CONTRIBUTING.md  Contributor validation commands
dist/            Generated ZIP only; ignored and never treated as authored source
```

[The exact manifest](dev/package_contract.py) names every permitted source file. New files do not
enter the archive by extension or directory membership. The build generates native `.agents/skills/`
and `.claude/skills/` from the same source, normalizes permissions and verifies extracted references,
client-copy equality, complete file sets and helper execution. It rejects unexpected files in `src/`.
No development tools, evaluator answers, raw traces, caches or local configuration belong in the ZIP.
[Repository audit](dev/audit_repo.py) inventories every tracked file and scans history for defined
credential/path patterns. This is a bounded hygiene check, not a guarantee that all secrets are detectable.
Real run data and reports stay outside the repository until an explicit review/publication decision.
