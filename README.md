# Steer Robust

An open-source, project-local engineering baseline for coding agents and learners.
Short essential instructions lead to focused skills and shared engineering guides only when relevant.

## What is included

- **project-exploration:** understand a product, its architecture and business rules; map or trace a flow.
- **change-verification:** select repository-required proof and diagnose CI without duplicating project policy.
- **runtime-qa:** verify behavior through real product boundaries and prepare reviewable evidence.
- **Ten guides:** principles, design, efficiency, failure/concurrency, compatibility, security,
  verification, performance, evaluation and short playbooks.
- Optional read-only Python helpers for guidance discovery and bounded Markdown retrieval.

## Package layout

```text
package/                           # merge these contents into the target project
├── AGENTS.md
├── .agents/skills/
│   ├── project-exploration/
│   │   ├── SKILL.md
│   │   ├── references/discovery.md
│   │   └── scripts/
│   ├── change-verification/SKILL.md
│   └── runtime-qa/
│       ├── SKILL.md
│       └── references/
└── Steer-robust/                    # shared engineering guides
```

Each skill has standard YAML `name`/`description` metadata in `SKILL.md` and conditional resources.
The skills intentionally share guides outside their own folders. Install this as a **project bundle**;
copying one skill into a global directory alone leaves its shared references unavailable.

## Use in a project

```sh
gh repo clone shoaibulhaque/steer-robust
cd steer-robust
```

Read the [adoption guide](package/README.md#adopt-in-one-project), then:

1. Merge [the baseline](package/AGENTS.md) into the project's existing root `AGENTS.md`.
2. Copy `package/Steer-robust/` beside that root, reconciling any existing same-name directory.
3. Add the selected folders from `package/.agents/skills/` to its existing `.agents/skills/`.
   Preserve existing skills; reuse an equivalent project-owned workflow and adjust links when appropriate.
4. Add actual project commands and owner-guide links. Verify instruction and skill availability in your client.

Do not overwrite existing project instructions or replace `.agents/`. Copy hidden directories too.
Keep the relative layout shown above. No global installation, automatic rewrite or eager loading of all guides.
Client discovery differs; the adoption guide explains the boundaries and optional bridging.

## Develop and validate

Python 3.9+ and Git are sufficient; no Python dependencies are required for the bundled checks.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate_package.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/build_package.py
```

The builder creates `dist/Steer-robust.zip`, validates extraction and executes the extracted helpers.
Generated archives and caches are ignored. The suite includes 50 tests for navigation, scope preservation,
metadata, links, distribution contents and repeatable archives. See [contributing](CONTRIBUTING.md).

## Design and limits

Every authored file is at most 120 lines. Essential/skill instructions have a 450-word budget;
shared guides and skill references have a 650-word budget. These limits apply to this distribution.
Skills prefer the adopting project's own contracts, tools and CI policy. No mandatory subagents,
self-editing loop, universal test runner or script-per-task rule is added.

Structural and helper checks do not establish live model adherence, universal client discovery,
net token savings or guaranteed accuracy. Maps and filename matches are navigation aids, not proof.
[Research notes](docs/research-lessons.md) explain selected influences and their limits.

Licensed under [MIT](LICENSE).
