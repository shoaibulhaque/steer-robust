# Research lessons retained in the final package

Reviewed selectively, most recently 2026-10-19; these are adaptations, not copied policy bundles.
Moving branch links identify inspected documents, not immutable snapshots. No claim of a full repo audit.
The shared guides preserve the earlier Steer engineering lessons and their exceptions.

## Engineering and architecture

| Lesson | Implemented owner |
|---|---|
| Explain the product/domain before file organization; attach rules to responsible owners | [Exploration](../src/.agents/skills/project-exploration/SKILL.md) and [design](../src/Steer-robust/design.md#model-the-domain) |
| Caller-shaped interfaces, focused entrypoints, optional capabilities at suitable edges | [Design](../src/Steer-robust/design.md#design-from-the-caller) |
| Preserve authoritative state; derive projections; justify synchronized copies and abstractions | [Design](../src/Steer-robust/design.md#model-the-domain) |
| Choose reliability mechanisms for credible failures and actual data/security guarantees | [Principles](../src/Steer-robust/principles.md#reliability-without-speculative-machinery) |
| Unknown outcomes, retry ownership, recovery, concurrency bounds and resource lifetime | [State/failure](../src/Steer-robust/state-and-failure.md) |
| Commit-dependent effects require explicit delivery semantics; rollback cannot undo external effects | [Persistence](../src/Steer-robust/state-and-failure.md#persistence-and-recovery) |
| Estimate time/space and I/O at realistic scale; remove invariant work before caching | [Performance](../src/Steer-robust/performance.md) |
| Tenant/object authority, destination encoding, current checks and privacy-safe fixtures | [Security](../src/Steer-robust/security.md) |
| Coordinate internal cutover; preserve actual external/mixed-version/data contracts | [Evolution](../src/Steer-robust/evolution.md) |

## Sources and deliberately qualified adaptations

- [OpenClaw guidance](https://github.com/openclaw/openclaw/blob/main/AGENTS.md) and
  [simplification skill](https://github.com/openclaw/openclaw/blob/main/.agents/skills/pr-simplify/SKILL.md):
  one owner, complete cutover, concrete tradeoffs and bounded proof. Retained compatibility needs a real contract.
  No universal ban on rare races, compatibility, files, older runtimes or code growth; no deletion quotas.
- [Dify web guide](https://github.com/langgenius/dify/blob/main/web/AGENTS.md),
  [backend guide](https://github.com/langgenius/dify/blob/main/api/AGENTS.md) and
  [testing skill](https://github.com/langgenius/dify/blob/main/.agents/skills/frontend-testing/SKILL.md):
  local contracts and narrow skills that route to canonical policy. A skill need not have a script or extra checklist.
  Applied in both entrypoints and [verification](../src/.agents/skills/change-verification/SKILL.md).
- [Zulip instructions](https://github.com/zulip/zulip/blob/main/AGENTS.md) and
  [testing philosophy](https://zulip.readthedocs.io/en/latest/testing/philosophy.html):
  discover cross-client rules, teach from architecture/docs, test meaningful state and preserve human obligations.
  Local `.claude/rules/testing.md` and `.claude/skills/self-review/SKILL.md` inspected at
  `e45560dfcfc40c786c689b454ef6f4e7dc0f3eaf`; no claim that this equals the moving web snapshot.
  Applied in [discovery](../src/.agents/skills/project-exploration/references/discovery.md) and verification.
- [PostHog guidance](https://github.com/PostHog/posthog/blob/master/AGENTS.md) and
  [architecture](https://github.com/PostHog/posthog/blob/master/products/architecture.md):
  use native enforcement/wrappers; selective tests need genuine isolation contracts, including dynamic dependencies.
  Shared workflow changes can affect older branches. Applied in principles, verification and evolution.
  No copied tenant model, infrastructure choice, universal runner or permission framework.
- [T3 Code guidance](https://github.com/pingdotgg/t3code/blob/main/AGENTS.md) and
  [UI testing skill](https://github.com/pingdotgg/t3code/blob/main/.agents/skills/test-t3-app/SKILL.md):
  consider affected clients/providers/modes, isolated state and task-owned resources; respect CI-owned suites.
  Applied in verification and [mapping](../src/Steer-robust/efficiency.md#build-a-scoped-map).
- [Peter's scripts](https://github.com/steipete/agent-scripts):
  doc hints, scoped maps and small deterministic helpers. Pinned selective review at
  `6232f9b84bba00bc6594b0443116f58d5654f647`; only selected guidance was inspected.
  Applied in efficiency and the read-only helpers; no personal machine, account or delegation defaults.
- [Pstack's lever](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-build-the-lever/SKILL.md):
  qualify a representative case, then automate when useful. No mandatory tool for every non-trivial edit.
  Applied in [useful automation](../src/Steer-robust/efficiency.md#build-a-useful-lever).
- [Rea guidance](https://github.com/morluto/rea/blob/main/AGENTS.md) and
  [tool design](https://github.com/morluto/rea/blob/main/docs/tool-design.md):
  capability-aware operations, retained evidence/provenance and whole-task cost; smaller replies may cost more overall.
  Applied in efficiency, explicit helper limitations and honest result reporting; no evidence-ledger framework.

## Useful techniques, with limits

- A minimal decisive probe can falsify a hypothesis cheaply; it does not replace required regression proof.
- One representative unit qualifies a bulk transformation; dry-run, preserved cases and final diff still matter.
- Source-linked maps aid navigation; inspected code and business rules support decisions.
- Bounded whole sections retain ancestor context; omissions and unsupported syntax require follow-up.
- Reuse logs while relevant inputs remain unchanged; refresh current-head and invalidated evidence.
- Use native structural checks for objective invariants; a linter cannot settle every design judgment.

## Evidence for the disclosure design

[OpenAI skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra),
[OpenAI skills](https://learn.chatgpt.com/docs/build-skills) and
[Anthropic skills](https://code.claude.com/docs/en/skills) support short metadata and conditional detail.
[Context-file research](https://arxiv.org/abs/2602.11988v3) and [SkillsBench](https://arxiv.org/abs/2602.12670v4)
justify measuring usefulness; their results do not validate this package or prescribe exactly two skills.
Runtime guides omit research catalogs so ordinary tasks do not need to read this maintenance document.
