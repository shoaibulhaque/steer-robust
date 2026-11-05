# Steer Robust

A project-local engineering baseline: essential instructions, three focused workflow skills,
ten shared guides and optional read-only helpers. No global installation is required.
Detailed principles have one owner and load only when relevant.

## Project layout

```text
project/
├── AGENTS.md
├── .agents/
│   └── skills/
│       ├── existing-project-skill/
│       ├── project-exploration/
│       │   ├── SKILL.md
│       │   ├── references/discovery.md
│       │   └── scripts/                 # four small Python files
│       ├── change-verification/
│       │   └── SKILL.md
│       └── runtime-qa/
│           ├── SKILL.md
│           └── references/              # scenarios and reviewable evidence
└── Steer-robust/                        # ten shared guides
```

- [AGENTS.md](AGENTS.md): essential obligations, project-contract discovery and conditional navigation.
- [Project exploration](.agents/skills/project-exploration/SKILL.md): product understanding, maps and teaching.
- [Change verification](.agents/skills/change-verification/SKILL.md): use the project's own proof policy.
- [Runtime QA](.agents/skills/runtime-qa/SKILL.md): exercise real product boundaries and retain reviewable evidence.
- [Principles](Steer-robust/principles.md), [design](Steer-robust/design.md) and
  [performance](Steer-robust/performance.md): reasoning, architecture, simple design and realistic complexity.
- The root also links failure/concurrency, compatibility, security, efficiency, evaluation and task recipes.

Every authored file has at most 120 physical lines; root instructions have at most 450 words,
guides/skill references 650 words and skill entrypoints 450 words. These are distribution bounds,
not new restrictions on an adopting project's code or documentation.

## Adopt in one project

1. Extract the ZIP to a staging folder, including its hidden `.agents/` directory.
   Inspect existing root/scoped instructions, contributor/AI policy, skills, templates and required checks.
2. Merge the baseline into the existing root `AGENTS.md`; use it directly only when no entrypoint exists.
   Preserve project requirements and human preferences. Resolve conflicts rather than appending contradictions.
3. Copy `Steer-robust/` beside that root. Inspect an existing same-name directory before merging anything.
4. Add the selected skill folders inside the project's existing `.agents/skills/`, alongside its own skills.
   Never replace `.agents/`, overwrite same-name skills or duplicate an equivalent project workflow.
   If reusing a project-owned skill, redirect the root pointer and check all affected links.
5. Fill `Project requirements` with actual commands and links to authoritative project guides.
   Keep substantial stack/subsystem policy with its existing owner; add scoped instructions only when needed.
6. Check relative links, applicable scope and actual instruction/skill availability in the intended client.
   Start a fresh session or use its documented refresh mechanism if the existing session has stale discovery.

Setup is once per project. Copying `AGENTS.md` alone does not provide linked resources or install skills.
These skill folders depend on the shared guides at the layout above; they are not standalone global skills.
This package deliberately has no blind installer or automatic rewrite of existing project configuration.

## Progressive disclosure

For Codex, root/scoped agent files provide applicable instructions; skill names/descriptions enable selection.
The selected `SKILL.md` supplies a workflow, with conditional links to guides and helpers.
Ordinary Markdown links require explicit reads; avoid eagerly importing every leaf or scanning for each typo.
Prefer an equivalent project-owned skill and its commands; do not run parallel copies of the same workflow.

Follow each client's current discovery behavior. When a Claude setup needs a bridge,
merge `@AGENTS.md` into its existing `CLAUDE.md` while preserving other instructions.
Verify skill availability separately; an instruction-file bridge does not establish skill discovery.
Do not create divergent copies or assume every client reads `.agents/skills/` automatically.
See [OpenAI instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[OpenAI skills](https://learn.chatgpt.com/docs/build-skills),
[Claude memory](https://code.claude.com/docs/en/memory) and [Claude skills](https://code.claude.com/docs/en/skills).

## Optional helpers

See [discovery and retrieval](.agents/skills/project-exploration/references/discovery.md) for commands and limits.
Python 3.9+ is optional; ordinary scoped searches work when it is unavailable.
Helpers find candidate paths or complete Markdown sections with scope context; they do not interpret every rule,
run setup/test commands, fetch remote content or modify the repository.
Output omissions and scan limitations are explicit. A filename inventory is not a completed project contract.

## Maintenance and limits

Prefer project-owned lint/CI checks for objective rules and concise guidance for judgment.
Preserve trigger, action, guarantee and legitimate exception when editing compressed lessons.
Keep project lessons in their project; improve shared guidance only for demonstrated, generalizable needs.
No mandatory subagents, session ledger, self-editing loop, universal test runner or script-per-task rule.
No borrowed publishing permissions or machine-specific tools. Teaching does not require a contribution.
Structural/helper tests do not prove live model adherence, every-client loading or net token savings.
The source distribution keeps research, curation and maintenance tests outside this deployable folder.

## Request runtime QA

Ask: `Use $runtime-qa to reproduce this issue, verify the repair through the real product path,
and prepare evidence for review.` The skill reuses repository commands and existing QA owners.
It selects only relevant scenarios, labels simulated/live boundaries, checks preservation and failure
behavior, and separates observed results from required-check readiness. Its references include practical
API, CLI, UI, generator, lifecycle and worker examples. No OpenClaw checkout or credentials are required.
