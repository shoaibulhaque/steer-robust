# Efficient work

Read when investigation creates large outputs, work repeats, or automation could reduce mistakes.
Minimize total effort while preserving required behavior and evidence quality.

## Find before reading

- Read applicable project instructions; discover scoped guidance before editing its files.
- Find candidate paths and symbols before opening large bodies.
- Prefer `rg --files` for paths and scoped `rg -n` for content when available.
- Start narrow; broaden when results, callers or missing evidence require it.
- Read relevant rule sections with their conditions, exceptions and linked requirements.
- Treat regex hits as leads, not proof.
- Prefer syntax-aware tools when nesting, language semantics or generated code make regex unsafe.
- Reuse existing documentation indexes and "read when" hints.

## Build a scoped map

Legacy anchor: use existing architecture docs and native navigation; do not create custom repository maps,
AST indexes, caching, memory or compaction systems. For onboarding, explain components and ownership
from inspected sources. Mark unknowns and inferences without generating a new maintained catalog.

## Keep output useful

- Request needed fields/ranges/failures; retain useful raw results.
- Bound displayed output. Report omissions and retrieve what matters before concluding.
- Truncation, no matches and incomplete scans do not prove absence.
- Retain source identity and resumable findings instead of repeated full reads.
- Keep names and safeguards readable; avoid cryptic abbreviation.

## Build a useful lever

- Reuse a suitable command, test or query first.
- Build a small script, codemod or check when automation reduces effort or error.
- A one-off tool can make verification reproducible.
- Simple edits may need only inspection and an existing check.
- Establish a representative expected result before automating many units.
- Scope mutations to intended files; preserve unrelated edits and reject unexpected input.
- Preview or dry-run bulk changes, inspect the diff, and check important preserved cases.
- Check rerun behavior before repeating a mutation; do not duplicate or erase valid work.
- Keep a helper when reviewers or future work need it, with its invocation and assumptions.
- Prefer one small tool over a framework; tools do not themselves prove correctness.

## Reuse evidence with its limits

- Reuse a captured log or immutable result while its relevant inputs remain unchanged.
- Record enough identity to connect evidence to the source, revision, command and environment.
- Refresh mutable status before relying on it for a consequential action or after a relevant change.
- Rerun checks invalidated by edits; honor the repository's required validation.
- Use a broader check when the changed contract crosses boundaries that the narrow check cannot cover.
- Investigate a failed check before rerunning it; repeated green hunting is not diagnosis.

## Use resources deliberately

- Batch independent reads where supported; keep dependent edits and checks ordered.
- Bound concurrency to the tool and resource; avoid duplicate requests and tight polling loops.
- Reuse an existing session or connection when appropriate; clean up resources created for this task.
- Tool use does not expand authorization. Do not adopt permissions from a researched repository.

## Judge the result

Compare total work: metadata/context, discovery, tool calls, setup, execution, review, retries and corrections.
Record cold/warm conditions and remaining uncertainty.
Smaller output is useful only if it preserves the information needed for a correct decision.
Label byte/character estimates as estimates; claim token or runtime savings only from suitable measurement.
If a shortcut loses important context, widen the read or use a more suitable tool.
