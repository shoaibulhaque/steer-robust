# Steer Robust project bundle

Essential instructions route to focused skills; skills explicitly load relevant engineering guides.
This is a project-local bundle for Codex and Claude Code, not independent global installs.

## Layout and ownership

```text
project/
├── AGENTS.md                         # authority, project contracts, required workflow routing
├── CLAUDE.md                         # imports AGENTS; preserve existing client instructions
├── .agents/skills/                   # canonical Codex skills
│   ├── engineering-change/SKILL.md   # coding: cause, simplicity, domain and relevant detail
│   ├── project-exploration/          # product-first explanation and optional read-only helpers
│   ├── change-verification/          # repository-owned checks and proof selection
│   ├── runtime-qa/                   # real behavior, scenarios and reviewable evidence
│   ├── statechart/                   # optional bounded TLA+/TLC safety workflow
│   └── security-audit/               # focused source-first security review
├── .claude/skills/                   # client copies generated during Claude adoption
└── Steer-robust/                     # canonical detailed guides
```

The distributed source authors skills once under `.agents/skills/`.
The generated ZIP already includes identical `.claude/skills/` copies for Claude Code.
For manual adoption from source, copy those skill folders; relative guide links work at either depth.
Generated client copies must be updated together from the canonical package; avoid divergent edits.

## Adopt in one project

1. Inspect existing root/scoped instructions, contributor/AI policy, client skills, templates and CI rules.
2. Merge [AGENTS.md](AGENTS.md) with the project root instructions, preserving its specific requirements.
   If none exist, use the baseline directly. Reconcile contradictions instead of appending duplicates.
3. Copy `Steer-robust/` beside the root. Preserve/reconcile any existing same-name directory.
4. Add selected skill folders to existing `.agents/skills/` for Codex, `.claude/skills/` for Claude, or both.
   Never replace existing client directories or overwrite conflicting skills. Prefer equivalent project owners.
5. Merge `@AGENTS.md` into existing `CLAUDE.md` for Claude. This bridge does not install skills.
6. Check all relative links after customization, then verify native availability in a fresh client session.
   A prose typo should not activate every guide; relevant nontrivial work must load its required entrypoint.

From the source repository, `python3 dev/adopt.py TARGET --client both` previews a conflict-checked copy.
Add `--apply` to copy only absent/identical paths. Any conflict stops before copying; merge it manually.
The helper is a developer convenience, not part of the distributed runtime. No global settings are changed.
The ZIP is built from the exact source manifest; optional runtime dependencies are never bundled.
Copying `AGENTS.md` alone leaves linked files missing. Preserve hidden directories when extracting the ZIP.

## Progressive disclosure

Names/descriptions advertise capabilities; root routing requires the applicable skill to be read.
Each entrypoint states which guides to read before a decision, and which are conditional.
[engineering-change](.agents/skills/engineering-change/SKILL.md) loads cause/design guidance before edits,
then relevant compatibility, security, efficiency, scale or state guidance.
[change-verification](.agents/skills/change-verification/SKILL.md) owns check selection and CI policy;
[runtime-qa](.agents/skills/runtime-qa/SKILL.md) owns scenarios and evidence when runtime proof is needed.
[statechart](.agents/skills/statechart/SKILL.md) applies only to ordering-sensitive stateful problems.
[security-audit](.agents/skills/security-audit/SKILL.md) provides focused source-grounded findings and falsification.
[project-exploration](.agents/skills/project-exploration/SKILL.md) teaches product concepts before file details.

[Principles](Steer-robust/principles.md), [design](Steer-robust/design.md), [efficiency](Steer-robust/efficiency.md),
[state/failure](Steer-robust/state-and-failure.md), [evolution](Steer-robust/evolution.md),
[security](Steer-robust/security.md), [verification](Steer-robust/verification.md),
[performance](Steer-robust/performance.md), [evaluation](Steer-robust/evaluation.md),
[playbooks](Steer-robust/playbooks.md) and [optional analyzers](Steer-robust/analyzers.md) have one owner each.
Ordinary links require explicit reads. They are not eager imports or a guarantee that a model complied.
The expensive behavioral suite checks native discovery, tool-visible reads and independently tested actions.

## Optional tools and limits

Existing project tooling takes precedence. Python 3.9+ helpers only locate guidance or retrieve sections;
see [discovery limits](.agents/skills/project-exploration/references/discovery.md).
They do not interpret every policy, index source semantics, execute discovered commands or create repo maps.
No new cache, compaction, memory system, MCP server, service or agent orchestrator is included.
Build a small lever only when it improves repeatability or proof; simple edits need no new script.
Crapper, Dryer, Mutator, language analyzers and Java/TLC are optional and never auto-installed.
Statechart checks bounded models and renders safety counterexample paths, not complete projected graphs.
Model paths must be replayed in the real implementation before claiming a product defect is proved.

Keep root/skill instructions within 450 words,
and detailed guides/skill references within 650 words. Limits describe this package, not adopting projects.
Tests cannot guarantee adherence, correctness across stacks or net token savings.
Keep research, developer tests and raw model runs outside this runtime bundle.

Licensed under [MIT](LICENSE.md); the [Cloudflare notice](.agents/skills/security-audit/NOTICE.md) applies to adapted audit guidance.
