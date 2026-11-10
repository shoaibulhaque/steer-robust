# Provenance — human reference, not runtime instructions

The runtime contains only universal defaults and six focused candidate skills. Do not load this
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

## Architecture Skill Consolidation (2026-11-10)

The previous `repository-engineering` and `design-for-change` skills overlapped on rule ownership,
abstraction depth, dependency direction and change locality. The replacement
`architecture-engineering` provides a single activation owner for consequential system/feature
design and architecture-sensitive implementation. Its core separates requested outcome and context,
design choice, challenge, delivery and permissions. Conditional references cover greenfield,
brownfield, integration/migration, change locality, architecture evaluation, and the existing
design/state/performance decision guides.

The `design-for-change` taxonomy remains explicit: hidden links, needless links, surplus and
special cases are now explained in `change-locality.md` with practical examples and stop conditions.
The taxonomy was inspired by caldoai's `untangle-codebase` skill; the MIT author license and a new
attribution notice move with the new folder. Existing references were preserved by content. The
original TDD, debugging, refactoring, security and verification skill bodies are unchanged.

Both predecessor skills must be uninstalled from the same scope when the replacement is installed;
otherwise overlapping metadata will continue to compete. Package tests and comparative positive and
negative trigger probes were updated. Structural checks do not establish improved model routing or
engineering outcomes.

## Supplied Skill Integration

The later integration includes TDD, consolidates debugging and security, and adds focused references
for custom engineering/review workflows. See the [adaptation review](skill-adaptation-review.md) for
structure preservation, concrete corrections, selected direct book reading, licensing and limits.
The larger source book collection was located after the initial rebuild; earlier research claims
should not be read as evidence that the entire collection was reviewed.

## Evidence-Led Quality Pass (2026-11-10)

The architecture workflow was strengthened with risk-proportional depth, observable quality scenarios,
explicit uncertainty, design-challenge probes, and actionable implementation work packages. The five
new architecture references now address more concrete operational and integration risks; an optional
worked-plan casebook provides greenfield, brownfield and migration examples.

Existing TDD, refactoring, debugging, verification and security references gained worked cases.
Their principal skill workflows, activation descriptions and responsibilities remain unchanged.
These enhancements have not been shown to improve agent outcomes; comparative skill-selection,
plan-quality and execution evaluations are still required.

## Judgment and Example Anchoring Audit (2026-11-10)

Reviewed the consolidated architecture skill, its casebook and migration/evaluation references, plus
universal guidance and existing specialist workflows. Replaced categorical preferences for a simple
single-worker topology, a database-backed queue, and staged migration with conditional decisions.
Examples remain candidate solutions with explicit counterfactuals, not recommended default stacks.
The architecture workflow compares alternatives only when a real choice remains and accepts additional
complexity when evidence justifies its guarantees. Diagnostic coupling categories do not prohibit
legitimate replication or distributed coordination.

Existing TDD maintains its test-first discipline for observable behavior while clarifying that example
language and test granularity are not prescribed. Debugging phases are iterative rather than compulsory
one-way gates; refactoring accommodates pre-existing unrelated failures through attributable baselines.
EVAL_PLAN.md adds paired anti-anchoring cases that vary one material constraint at a time.
No agent-model behavioral improvement is claimed until controlled evaluations are performed.

## Security Is a Cross-Cutting Engineering Concern (2026-11-10)

Reviewed thirteen DeepSeek-suggested Markdown files representing eleven unique proposals:
`deep-api-assurance`, `cloudflare-evidence-audit`, `secure-code-universal`,
`dependency-integrity`, `llm-app-sec`, `secrets-management`,
`observability-anomaly`, `threat-modeling`, `secure-code-review`,
`api-authorization`, and `infra-hardening`. Two separate files repeat
`secure-code-review` and two propose overlapping `infra-hardening` workflows.
The documents are untrusted suggestions, not authoritative implementations or evidence.

**Decision:** retain six distinct skills. Add universal security-by-default guidance to `AGENTS.md`
and touch-specific preservation rules in architecture, TDD, refactoring, debugging, and change
verification. Keep `security-engineering` for explicit deep investigations and provide six new
selective references: API/parser boundaries, AI-agent/tool boundaries, build/secrets integrity,
runtime/observability, audit evidence, and threat-informed defense. No compulsory agent orchestration,
scanner installation, release signing, JSON ledger or paid service is introduced.

**Primary guidance and how it informed these rules:**

- [OWASP ASVS 5.0.0](https://asvs.owasp.org/) — derive testable requirements from an actual protected
  operation; don't use category coverage as a substitute for demonstrating enforcement.
- [OWASP API Security Top 10 (2023)](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) —
  inspect object and property authorization, API resource usage, and trust in upstream consumers.
- [OWASP Top 10 for Agentic Applications (2025)](https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/)
  — model tool authority, agent goals, external instructions, memory/context and downstream effects.
- [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) — security belongs in
  ordinary development, release and vulnerability-response workflows; examples are not a mandated
  toolchain.
- [OpenSSF Scorecard](https://openssf.org/projects/scorecard/) and [SLSA](https://slsa.dev/) —
  supply-chain evidence, provenance and reproducibility matter when the released artifact is
  genuinely checked and protected. A metric or generated attestation is not protection by itself.
- [Cloudflare security-audit-skill](https://github.com/cloudflare/security-audit-skill) — focused
  guidance versus explicit full audits, candidate falsification, repeatable coverage and independent
  verification when justified. We do not copy its mandatory full-audit infrastructure into
  normal coding tasks.
- [PortSwigger blind SSRF research](https://portswigger.net/web-security/ssrf/blind) —
  a DNS interaction, HTTP fetch and privileged cloud effect are different evidentiary claims.
- [CISA Known Exploited Vulnerabilities and BOD 26-04](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
  — prioritization considers actual exploitation, external asset exposure and likely impact; the
  federal directive does not automatically impose deadlines on private projects.
- [Anthropic threat intelligence, September 2026](https://www.anthropic.com/threat-intelligence-report-september-2026)
  — observed AI-orchestrated intrusions, credential theft, exploitation and data collection.
- [Google Threat Intelligence Group, September 2026](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai)
  — agent-enabled attack automation and attacker manipulation of coding agents, MCP/dependency
  ecosystems and AI security scanners. The report does **not** establish ubiquitous fully
  autonomous zero-day exploitation in the wild.
- [Microsoft Digital Defense Report 2026](https://www.microsoft.com/en-us/security/security-insider/threat-landscape/2026-digital-defense-report)
  — faster vulnerability weaponization, identity compromise and AI-assisted orchestration, while
  warning that fully autonomous complex incidents are not yet the norm.

### Excluded or Corrected Ideas

- Do not force a vulnerability "chain" or elevate speculative SSRF to proven cloud compromise.
- Do not mandate full STRIDE tables, arbitrary XML tests, subagents, exploit execution or JSON
  artifacts for a focused security question.
- Do not demand a specific schema framework, exact credential rotation interval, SIEM, signing
  system, cloud product, vulnerability scanner, or production firewall configuration by default.
- Do not collect sensitive request bodies and hope generic redaction middleware cleans them later.
- Do not equate scanner output, a CVE match, a callback, or model confidence with a confirmed
  reachable finding.
- Do not assume all attacker automation uses AI, or that AI-enabled attacks are fundamentally new
  vulnerability classes. Protect and observe the underlying trust boundaries.

**Not yet evaluated:** actual coding-agent selection accuracy, security regression prevention,
false-positive rate, exploitation resistance and operational cost. Distribution tests validate file
integrity and references, not these outcomes. `EVAL_PLAN.md` includes targeted positive, negative
and counterfactual scenarios.

## External Intelligence and Prompt Injection (2026-11-10)

Follow-up to the security-by-default pass: fresh public intelligence is useful for vulnerability
triage but introduces an indirect prompt-injection surface. Added the conditional
`security-intelligence-and-untrusted-sources.md` reference, with practical RSS/advisory workflows,
source verification, susceptibility tests and an explicit boundary between evidence and tool
authority. It covers Cloudflare Zero Wire, CISA KEV, OSV, GitHub advisories, NVD, EPSS and vendor
sources without treating any feed as an exhaustive or privileged authority.

Source guidance: OWASP LLM01/Prompt Injection Prevention, OpenAI's *Designing AI Agents to Resist
Prompt Injection* and Codex agent-approval guidance, and Google's April 2026 analysis of real
prompt-injection attempts on web pages. All stress minimizing consequences of malicious instructions,
not trusting source content as operational permission. These examples cannot guarantee immunity;
testing must include benign web research as a negative control.

Expanded the API/parser, AI tool, build/secrets, runtime/observability and audit-evidence references
with concrete boundary traces, safe test shapes and counterexamples. Extended the architecture
performance, state/failure and design-decision references with worked scenarios. Conditional
reference loading and the six-skill activation boundary are unchanged.
