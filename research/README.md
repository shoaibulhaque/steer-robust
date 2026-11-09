# Provenance — human reference, not runtime instructions

The runtime contains only universal defaults and seven focused candidate skills. Do not load this
research folder for ordinary tasks or install it under a skill directory.

## Inputs inspected

- The supplied `portable-engineering-agents-v0.3` package: its defaults, three candidate skills,
  README, rebuild prompt, evaluation plan, and 46-rule consolidated engineering guide.
- Its `principles.json`: 419 unique entries across 13 book identifiers, parsed programmatically;
  focused inspection covered ownership, information hiding, abstraction costs, refactoring,
  complexity, domain invariants, concurrency, compatibility and distributed failure semantics.
  These are supplied paraphrases, not 419 independently verified book claims.
  At the initial rebuild, book notes and original PDFs were not inspected. The original inputs remain in the separate
  reference package; the large catalog is deliberately not bundled here.
- Previous Steer Robust research is retained under `research/previous-steer/` in the source checkout,
  outside automatic loading and excluded from the ZIP. Its implementation links are pinned to the
  historical revision; its claims do not describe the replacement toolkit.
- Existing evaluation material showed additional instruction cost without established quality gains.
  The unpublished evaluation rewrite was preserved separately during cleanup. No old run evaluates
  the new candidates, and no new comparative outcome is claimed.

## Current primary guidance

- [Skill Creator source](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md),
  inspected alongside the complete locally installed skill: assume agent capability, preserve intent,
  make discovery precise, and add resources only for a concrete workflow.
- [Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra):
  narrow descriptions, conditional reading and removal of obsolete scaffolding.
- [Testing skills systematically](https://developers.openai.com/blog/eval-skills):
  observable outcomes, captured actions, negative controls and efficiency measures.
- [Native skills](https://learn.chatgpt.com/docs/build-skills) and
  [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md):
  metadata-first discovery, optional resources, instruction scope and override behavior.

## Decisions in this rebuild

Keep durable defaults separate from design decisions, causal investigation, and explicitly requested
review. Keep test-first mechanics with the selected TDD skill; do not load competing TDD implementations. Add a project appendix without
stack assumptions. Retain concrete failure semantics only where the task affects them; do not turn
the catalog into a checklist. Ship no runtime helper, analyzer, installer, hook, or orchestration layer.
The ZIP builder is development-only. Validation proves packaging, not improved engineering behavior.

## Follow-up: actual GitHub skill implementations

Eight `SKILL.md` files were fetched at immutable revisions and read, rather than inferred from repository
descriptions. The procedures here are original wording; no upstream scripts or skill bodies are vendored.

- OpenAI at `49f948faa9258a0c61caceaf225e179651397431`:
  [CI repair](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/gh-fix-ci/SKILL.md)
  demonstrates concrete inputs, log inspection and fallbacks;
  [threat modeling](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-threat-model/SKILL.md)
  grounds boundaries and findings in repository evidence. Provider restrictions, mandatory approval
  phases and specialized report templates were not generalized into this kit.
- Superpowers at `22f0b463e7a5e579904dd6211a520321035526f7`:
  [debugging](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/systematic-debugging/SKILL.md)
  motivates working/failing comparisons, causal tracing and falsifiable predictions;
  [verification](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/verification-before-completion/SKILL.md)
  distinguishes claims from supporting observations. Blanket activation, fixed failure counts,
  forced companion skills and always-fresh full-command reruns were deliberately excluded.
- Peter Steinberger at `d210c0a77c8f9ae5e1d939b13238a75e87cdb69a`:
  [CLI design](https://github.com/steipete/agent-scripts/blob/d210c0a77c8f9ae5e1d939b13238a75e87cdb69a/skills/create-cli/SKILL.md)
  makes interface decisions and deliverables concrete. Its CLI conventions remain task-specific.
- Pstack at `2776ddd2355d6d6c8747d3964600f28daf62f049`:
  [reader load](https://github.com/cursor/plugins/blob/2776ddd2355d6d6c8747d3964600f28daf62f049/pstack/skills/principle-minimize-reader-load/SKILL.md),
  [verification](https://github.com/cursor/plugins/blob/2776ddd2355d6d6c8747d3964600f28daf62f049/pstack/skills/principle-prove-it-works/SKILL.md), and
  [the lever](https://github.com/cursor/plugins/blob/2776ddd2355d6d6c8747d3964600f28daf62f049/pstack/skills/principle-build-the-lever/SKILL.md)
  motivate tracing/state costs, artifact-level proof and useful repeatable automation. Single-caller
  boundaries may still be useful; a new script, timer threshold or delegation is not compulsory.

User-supplied examples also prompted explicit lifecycle transitions, validation at owning boundaries,
and checking related instances of a proven defect. Fixed retry counts, blanket test-edit bans and
unconditional approval gates were not adopted as universal engineering rules.

## Preventive Skill Adaptation (2026-11-09)

The [caldoai untangle-codebase skill](https://github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md)
inspired the preventive change-locality framing and the hidden/needless/surplus taxonomy. Its original
workflow calls for whole-repository redesign and repeated refactoring. The new `design-for-change`
skill instead evaluates coupling introduced by a requested implementation, stops at the task boundary,
and leaves substantial design choices and behavior-preserving restructuring to the existing owners.
Its wording and examples were rewritten for this package; the source's MIT license (2026 Maze)
is retained in the skill folder. This attribution does not imply upstream endorsement or tested
improvement in agent outcomes.

## Planning Trigger Review (2026-11-09)

All seven descriptions now cover relevant plan-only requests without requiring automatic activation on every planning task. `AGENTS.md` preserves a strict planning/execution boundary; each workflow specifies a minimal plan output and no-write behavior. The preventive skill's change-locality probes are an original adaptation of the earlier untangling concepts. Routing and outcome improvements are unmeasured; evaluation cases appear in `EVAL_PLAN.md`.

## Supplied Skill Integration

The later integration includes TDD, consolidates debugging and security, and adds focused references
for custom engineering/review workflows. See the [adaptation review](skill-adaptation-review.md) for
structure preservation, concrete corrections, selected direct book reading, licensing and limits.
The larger source book collection was located after the initial rebuild; earlier research claims
should not be read as evidence that the entire collection was reviewed.
