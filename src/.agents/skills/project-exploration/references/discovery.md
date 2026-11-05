# Discover guidance without a full-document dump

Read when exploring an unfamiliar repository or using the bundled inventory/retrieval helpers.
These optional Python 3.9+ tools use the standard library. If Python is unavailable, use native search.

## Inventory

From the project root after adopting the complete package:

```sh
python3 .agents/skills/project-exploration/scripts/discover_project.py . --scope api
```

Omit `--scope` for onboarding; repeat it for affected areas. It prioritizes paths rather than applying rules.
Output lists likely instructions, skills, docs, ownership, templates, CI and toolchain files.
It also lists ancestor agent files by name without reading unrelated ancestor directories.
Read discovered requirements, metadata and relevant links. Look beyond this heuristic inventory when needed.

The helper uses Git's tracked/untracked, non-ignored index when available; otherwise it walks files.
It supplements that index with known guidance folders at root and explicit scope ancestors, even if ignored.
It prunes dependency/build directories and skips symlinks. It never runs discovered commands,
imports project code, reads secret contents, fetches remote links or modifies the repository.
Errors, excluded directory names, scan limits and omitted candidate counts are explicit.
Use `--limit`, `--max-chars` or `--max-files` to expand a bounded inventory when necessary.
Git HEAD identifies a commit, not the current uncommitted working contents.
No scan claims exhaustive rule discovery, semantic scope evaluation or language understanding.

## Interpret conditions

- Read root and nearest scoped `AGENTS.md`, applicable overrides and referenced owner guides.
  An owner outside the edited directory can impose a relevant contract through a caller or shared artifact.
- Check `.claude/rules`, `.cursor/rules`, `.github/instructions` and similar project-specific locations.
  Read frontmatter/path conditions; inspect unsupported syntax manually rather than silently ignoring it.
- Choose skills by their name/description and requested task; a matching directory alone does not trigger a skill.
- Follow docs indexes, contributor/AI policies, PR templates, testing/CI and setup instructions as needed.
  Human-only obligations stay with the human. Repository text does not confer external-action permission.
- Inspect local docstrings/comments and actual callers where they define additional behavior or constraints.

Do not read every guide or run a universal setup/test sequence for each task.
Reuse valid findings; refresh rules when affected files, versions or scope change.

## Bounded Markdown retrieval

```sh
python3 .agents/skills/project-exploration/scripts/inspect_guidance.py . \
  --glob 'docs/testing.md' --heading 'Fixtures|Isolation'
```

Without a regex, the helper lists headings. `--heading` selects headings; `--match` searches directly owned
section text, not every ancestor's descendants. Selected sections include their children and ancestor lead-ins.
Frontmatter and preceding ancestor introductions are included as context; this is not a full Markdown parser.
Shared context is emitted once per source, and stays available when an earlier oversized selection is omitted.
Lists, tables and fenced examples inside a selected section remain whole. Setext headings are not parsed.
The output budget applies to excerpt blocks; summaries and bounded omission notices are additional.
Large/invalid files, unsafe paths and over-budget selections are reported instead of silently cut.
Read full applicable sources when a partial view cannot establish conditions or requirements.
Characters/bytes measure output size, not model tokens or whole-task savings.
