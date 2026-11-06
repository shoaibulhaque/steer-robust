# Supplied Skills: Review and Integration

Reviewed 2026-11-06. This is human-facing provenance, not a runtime checklist or proof of improved results.

## Inputs and Identity

The user supplied `skills.zip` with six skills and supporting documents. The archive is unchanged.
SHA-256: `d686f113c6f9f379319009083d0e2b4abe5626d7acfc1b21457959c8cf8dc161`.
Original wording and core flows were compared with the existing toolkit before editing. The imported
skills are revised versions, not original inventions or official upstream endorsements.

## Decisions

| Input | Treatment | Preserved structure and behavior |
| --- | --- | --- |
| test-driven-development | Integrated under its familiar name | Overview, applicability, core rule, red/verify-red/green/verify-green/refactor/repeat, good tests, rationalizations, warnings, checklist, stuck cases and debugging integration |
| writing-good-tests | Integrated as a conditional TDD reference | Two principles, independent oracle, real behavior, gate questions, mutation reasoning, quick reference and warnings |
| systematic-debugging | Consolidated with evidence-debugging | Four phases: investigation, pattern analysis, hypothesis/testing, implementation; red flags, rationalizations, quick reference, unresolved causes and supporting techniques |
| security-best-practices | Consolidated into security-engineering | Mode selection, stack discovery, overrides, evidence-backed reports, scoped fixes and general security advice |
| security-threat-model | Integrated as a conditional eight-stage workflow | System model, boundaries, attacker capabilities, abuse paths, risk, assumptions, mitigation and final quality check |
| find-skills | Omitted | Discovery tooling does not improve this engineering workflow |
| code-review | Omitted | Existing verification owns review; the supplied orchestrator adds delegation, reasoning settings and external mutation beyond this kit's needs |

The custom engineering/verification skills adopt overview, core principle, precise activation,
ordered decision points, warning signs and conditional references. Their reference owners are design,
state/failure, performance and verification fidelity; they do not duplicate the TDD cycle.

## Intentional Corrections

- Keep test-first discipline for testable behavior, but do not delete/reset user work to recreate history.
  Distinguish testable behavior changes, preservation/characterization, prose and disposable experiments.
- Replace "every function needs a test" with behavior-oriented coverage. Legitimate interaction contracts
  can use spies; a mock call alone cannot prove remote delivery or durability. Correct expectations from
  authoritative requirements, never merely to hide a failure. A passing characterization is not a failed TDD step.
- Retain causal phases without claiming that three failed attempts prove an architecture is wrong.
  Repeated unsupported fixes require revising the model, not a compulsory rewrite or arbitrary halt.
- Remove diagnostic examples that print environment values. Evidence gathering is scoped and redacted.
- Rework the supplied "validate every layer" reference into distinct owned defenses: input shape,
  domain invariants, mutable authority/effect constraints and diagnostics. Logs are not enforcement.
- Do not ship the npm-specific pollution scanner: it hides invocation failures and scans tests singly,
  missing some order-dependent interactions. Preserve the technique with native runner selection and
  explicit evidence limits. Do not ship project-specific TypeScript helpers or their unrelated imports.
- Security findings distinguish reachable vulnerabilities, conditional threats and missing hardening.
  Random IDs do not replace authorization; runtime TLS/cookie behavior needs deployment evidence.
- Originally replaced the ten stack manuals with a compact source table. Reversed in the audit below:
  the manuals retain their security rules and are read only for the matching stack. Trailing whitespace
  was normalized in four manuals.
- Retain per-skill licenses for standalone copying; omit upstream creation logs and pressure-test stories
  from runtime. No support for auto-delegation, forced companion skills, hooks or mandatory analyzers.

## Books and Principles Actually Inspected

Used the supplied 46-rule synthesis and 419-entry catalog as research indexes, then read selected
passages directly from locally supplied PDFs. Page locators below are one-based PDF pages, not printed
pages. This is targeted reading, not a claim to have read every page or independently verified all entries.

| Source | Passages inspected | Applied lesson |
| --- | --- | --- |
| Beck, TDD: By Example, supplied review draft | PDF 102–105, implementation strategies | Preserve the feedback loop; obvious implementation and step size depend on uncertainty, not ritual |
| Feathers, Working Effectively with Legacy Code | PDF 208–210, characterization | Separate actual behavior preservation from desired behavior and regression specification |
| Ousterhout, A Philosophy of Software Design | Selected passages PDF 31–35 and 166–168 | Information hiding, interface knowledge, meaningful modules and proportionate performance choices |
| Kernighan/Pike, The Practice of Programming | PDF 145–146, debugging summary | Reduce inputs, narrow the cause, inspect evidence and related faulty patterns |
| Howard/LeBlanc, Writing Secure Code, supplied selected chapters | Selected passages PDF 48–51, array indexing/conversions | Bounds, size arithmetic and representation errors can cross security boundaries; historical APIs are not current prescriptions |
| Kleppmann, Designing Data-Intensive Applications | Selected passages PDF 299–302, unreliable networks | A missing response leaves execution uncertain; test failure windows and effects |
| Fowler, Refactoring | Selected passages PDF 56–58, definitions/two hats | Keep behavior preservation distinct from adding functionality; use attributable small changes |
| Evans, Domain-Driven Design | Selected passages PDF 207–209, bounded context | Same vocabulary or shape does not imply one shared model or ownership context |

The supplied secure-coding PDF includes selected old chapters, not a complete modern security manual.
The TDD PDF is an unfinished review draft. No PDF, large catalog, reading log or raw excerpt is distributed.
The added runtime references are original paraphrases with engineering guardrails, not book quotations.

## Current Security Sources

Checked the current [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html),
[threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html),
[SSRF](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) and
[agent/prompt boundaries](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
guidance for the revised ownership and evidence rules. Nine framework documentation destinations were
checked for availability/title; that check alone does not validate their entire content or every version.
Always verify specific APIs/defaults against the actual supported stack when applying the skill.

## Licensing and Evidence Limits

The supplied security skills include identical Apache 2.0 licenses; the consolidated folder retains one
copy and a modification notice. Superpowers' upstream MIT notice is retained separately in each
TDD/debugging folder so selected-folder installation preserves attribution. The user-supplied test-quality
extensions were integrated with that material. Source: [Superpowers license](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/LICENSE).

Validation checks resources, metadata, packaging and examples. Native prompt inspection can establish
availability and lazy body loading. Neither proves automatic activation, successful teaching, better
patches or lower costs. Controlled model comparisons remain required before an improvement claim.

## Finalization Pass

Compared the skills again with the supplied originals and current authoring guidance, then
restored core logic that the earlier revision had weakened:

- TDD: the near-original core principle, an Iron Law scoped to testable behavior, mandatory
  verify-red/verify-green confirmations, the full rationalization set and the "When Stuck" table.
  The earlier correction remains: never delete or reset user work; prove detection in isolation instead.
- Debugging: the Iron Law, numbered phase steps, single-fix discipline, "say when you do not know",
  user redirection signals and the original rationalizations. The fixed three-fix threshold remains
  replaced by the revealed-coupling signal.
- Descriptions now start with "Use when", name concrete triggers and symptoms, and state the boundary.
  Every reference opens with a "Read when" condition; no reference links to another reference.
- Inline attribution footers were removed from skill bodies. Attribution is retained in each
  folder's license file, the Apache modification notice and the README license section.

- Added `refactoring` after direct reading showed a distinct, common workflow that no skill owned:
  Fowler, *Refactoring*, PDF 56–58, 62–66 and 118–120 (definition, two hats, preparatory and
  comprehension refactoring, small steps that back out on failure) and Feathers, *Working Effectively
  with Legacy Code*, PDF 41–43, 82–84, 208–213 and 334–336 (legacy change algorithm, sprout, the
  characterization-test procedure, single-goal editing and preserved signatures). Its dependency-breaking
  reference paraphrases the seam and technique entries of the supplied catalog. TDD no longer claims
  refactors, and the legacy-seam text left the design reference, so each rule has one owner.
- Debugging gained input halving and "suspect your own code before the platform" from
  *The Pragmatic Programmer*, PDF 174–178. The design reference gained pattern selection by
  applicability and consequences (GoF catalog entries).

Authoring sources: the [Agent Skills specification](https://agentskills.io/specification) (frontmatter
limits, three-level loading, references one level deep) and Anthropic's
[skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
(what-plus-when descriptions, concise bodies, consistent terms, tables of contents for long references).

Repository examples read directly (default branches, 2026-11-06): `AGENTS.md` and skills from
[sst/opencode](https://github.com/sst/opencode), [PostHog/posthog](https://github.com/PostHog/posthog),
[langfuse/langfuse](https://github.com/langfuse/langfuse) and [openclaw/openclaw](https://github.com/openclaw/openclaw).
Lessons applied: trigger-term descriptions (opencode `unit-tests`, PostHog `debugging-ci-failures`);
a "read when" clause on every link and one owner per rule (PostHog `editing-agents-md`); asking whether
a proof could pass while the task is still broken, and migrating all callers in one cutover (OpenClaw
`AGENTS.md`); a test earns its place only if it fails without the change (Langfuse `AGENTS.md`).
Repository-specific commands, tags, size budgets and tooling were not generalized. No upstream text
was copied beyond short paraphrase.

## Audit Pass

An audit compared each skill and reference with the supplied originals, mature repository skills and the
46 consolidated book rules. Findings and changes:

- **Examples:** four skills had no worked example, and several references had lost theirs. Examples now
  come only from licensed sources (Superpowers, MIT; OpenAI skills, Apache 2.0), used as written, or from
  the supplied books, paraphrased without code reproduction. Invented scenarios were removed.
- **Reference depth:** `writing-good-tests`, the three debugging references and `threat-modeling` were
  restored to the originals' depth (change detectors, framework boundary, mock level, mutation list,
  worked trace, polling helper, four-layer example, risk tiers and output contract), keeping the
  recorded corrections.
- **Security stack manuals:** the ten manuals retain their security rules and are routed one level deep from the
  skill; `stack-guidance.md` was folded into the skill body. Progressive disclosure keeps their cost at
  zero until a matching stack is in scope. Their version pins are dated; the skill requires checking
  the installed version.
- **Book coverage:** a new `code-level-decisions` reference covers rules Q18–Q25 (names, comments,
  representations, state and side effects, contracts and assertions, absence, error boundaries,
  resources). The design reference gained Q26 and Q28–Q31; the state reference gained Q38 and Q46; the
  verification reference gained Q33; AGENTS.md gained comment and error-handling defaults.
- **No citations at runtime:** agents cannot open the books, so skills carry examples without titles or
  page locators. Sources for human review:

| Example | Source (one-based PDF pages of the supplied copies) |
| --- | --- |
| Deep and shallow modules, Unix I/O, Java streams, leakage, flush rules | Ousterhout, *A Philosophy of Software Design*, PDF 32–38, 42 |
| Defining errors out of existence | Ousterhout, PDF 87–89 |
| Comments and consistent names (`block` bug) | Ousterhout, PDF 107, 134 |
| Expensive operations, hash table vs ordered map, inline records | Ousterhout, PDF 166–167 |
| Hidden session side effect, command–query separation | Martin, *Clean Code*, PDF 75–76 |
| Special-case object, null-check nesting | Martin, PDF 140–142 |
| Assertion with an iterator side effect | Hunt and Thomas, *The Pragmatic Programmer*, PDF 208–209 |
| Reproduce with the reporter (drawing-stroke crash) | Hunt and Thomas, PDF 171 |
| Bounded contexts, booking and scheduling teams | Evans, *Domain-Driven Design*, PDF 207–209 |
| Six outcomes of an unanswered request | Kleppmann, *Designing Data-Intensive Applications*, PDF 299–300 |
| Statement printed in HTML, preparatory refactoring | Fowler, *Refactoring*, PDF 8–9, 62 |
| Characterization test, sprouting `uniqueEntries` | Feathers, *Working Effectively with Legacy Code*, PDF 83–84, 209–210 |
