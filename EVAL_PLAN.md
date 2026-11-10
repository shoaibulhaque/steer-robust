# Evaluate Before Adoption

These are proposed experiments, not completed model trials. Compare with the user's actual Codex
setup, working TDD skill and applicable repository instructions. Do not disable useful baseline
safeguards to make candidates look better. Record all active instruction/skill versions and conditions.

## Controlled Comparisons

| Condition | Difference from baseline | Main question |
| --- | --- | --- |
| A: baseline | None | What does the actual working Codex + TDD setup achieve? |
| B: defaults | Candidate AGENTS.md only | Do durable defaults add benefit without unnecessary work? |
| C: architecture | B plus architecture-engineering | Sound greenfield/brownfield/hybrid plans and better design choices without extra ceremony? |
| D: debugging | B plus systematic-debugging | Better diagnosis of uncertain failures without slowing clear ones? |
| E: review | B plus change-verification | Better explicit review/readiness without activation during ordinary coding? |
| F: security | B plus security-engineering | Grounded scoped analysis without false audit activation or inflated findings? |
| G: packaged TDD | B with packaged TDD replacing baseline TDD | Does the packaged version improve feedback and test quality? Never load both TDD versions. |
| H: refactoring | B plus refactoring | Safer behavior-preserving steps and legacy characterization without behavior drift? |
| I: consolidation | Current seven-skill kit versus proposed six-skill kit | Does consolidation improve routing, plans and cost without losing preventive change-locality discipline? |

Compare architecture cases with the existing seven-skill installation as a separate baseline. Record
whether both former architecture skills were selected and whether they contributed unique value. Run
conditions on identical fixtures without mixed installations. Test the combined configuration only
after useful individual results. If an existing setup already has
an overlapping debugging/security skill, document it and compare replacements explicitly. Do not let
competing same-name skills silently contaminate conditions or attribute a bundled gain to every component.

Use paired tasks with identical initial fixture revision, model/effort, permissions, tool availability
and environment. Run in disposable repositories and isolated profiles, without modifying installations.
Keep solutions, graders and other runs outside the evaluated checkout. Do not leak a known merged
solution into a test claiming discovery. Repeat useful cases; tiny pilots are descriptive, not causal proof.

## Positive and Negative Trigger Probes

Give the task and relevant repository evidence, not the intended solution. Do not name a skill when
testing automatic selection; test explicit invocation separately to distinguish availability from routing.

| Skill | Positive scenario | Adjacent negative control |
| --- | --- | --- |
| Architecture engineering | Plan a greenfield service with measurable constraints, or implement a multi-consumer rule without duplicating decisions | Mechanical local rename, pure refactoring, causal debugging, or PR readiness review |
| Systematic debugging | Intermittent duplicate effects survive earlier fixes; response can be lost after a write | Supplied failing example with already established cause |
| TDD | Implement testable behavior with a discriminating new example, including an access rule changed only in configuration | Prose-only correction; a pure refactor should not trigger it |
| Refactoring | Split a long untested function before a requested change; a latent bug must be reported, not silently fixed | A requested new feature with no restructuring |
| Change verification | Review a patch for PR readiness against actual contribution/CI rules | Routine implementation or merely running a specified test |
| Security engineering | Explicit scoped security review, secure-coding request or threat model | Ordinary feature work touching an authenticated route; still preserve security without starting a full audit |

A typo-only task should load none of these workflows. Include tasks where two responsibilities really
apply, without requiring all skills. For advanced references, check that the relevant guide is read
when needed and unrelated guides remain unloaded.

## Plan-Only Routing Probes

Test automatic selection without naming skills. Check that plans are actionable, proportionate, and make **no edits**.

| Prompt | Expected skill | Failure to reject |
| --- | --- | --- |
| Plan a new enrollment service with storage and realistic traffic constraints | Architecture engineering: greenfield | Choose infrastructure without workload evidence or begin implementation |
| Plan an enrollment change involving a persisted schema and deployed API | Architecture engineering: brownfield | Guess existing contracts or start implementation |
| Plan an old/new data pipeline cutover without data loss | Architecture engineering: integration/migration | Promise rollback without assessing irreversible writes |
| Plan adding a setting through schema, editor, and API without duplicated defaults | Architecture engineering: change locality | Treat legitimate multi-file edits as tangles |
| Plan safely splitting this untested legacy routine | Refactoring | Fix bugs or claim baseline passed |
| Plan how to diagnose intermittent CI-only duplicate effects | Systematic debugging | Declare an unproven root cause |
| Plan the test-first implementation of a new authorization rule | TDD | Claim that RED was observed |
| Plan verification for this specific proposed migration patch | Change verification | Declare merge-readiness without evidence |
| Plan a threat model for tenant isolation | Security engineering | Report hypotheses as confirmed vulnerabilities |
| Plan a local variable rename or ordinary content edit | None | Load all skills or create a large design report |

Include mixed-domain cases where two skills genuinely apply without expanding the plan into all workflows. Grade ownership, implementation order, decisive checks, evidence versus assumptions, tool cost, and adherence to plan-only permissions.

## Architecture Planning Quality Probes

Evaluate the **plan's ability to constrain a correct implementation**, not its length or
architecture vocabulary. Compare the previous seven-skill kit with the consolidated candidate
on identical task fixtures.

| Fixture | Wrong-plan trap | Strong-plan signal |
| --- | --- | --- |
| Greenfield worker, unknown peak load | Invent throughput or add a broker cluster | Mark unknown workload; name operation identity, recovery, and measurement |
| Brownfield CMS field crossing schema and preview | Duplicate fallback semantics, break old data | Find one rule owner; preserve draft/published and old-content behavior |
| Hybrid service replacement | Promise generic rollback or assume mixed-version safety | Map supported versions, authoritative writer, cutover and recovery |
| Shared eligibility decision | Merge independent policies by syntax | Centralize only decisions with one reason to change |
| Small formatting change | Trigger architecture analysis and diagrams | Select no unnecessary skill |

For each consequential requirement, trace **owner → implementation step → verification evidence**
that would reject a plausible incorrect implementation. Penalize invented measurements, unsupported
capacity claims, decorative diagrams, unnecessary special-skill activation, and plan-only writes.
A substantial plan may use the casebook; a routine decision should not load it automatically.

## Anti-Anchoring and Judgment Probes

Evaluate the same engineering objective under **different grounded constraints**. A strong agent
changes its recommendation when requirements change, rather than repeating the casebook's topology.
Grade justified choices and verifiable guarantees, not the appearance of a preferred stack.

| Contrasting contexts | Expected judgment |
| --- | --- |
| Low-volume jobs with a reliable platform queue vs. a system with only transactional storage | A managed queue may be better from day one in one setting; a database-backed worker in the other |
| New product with strict independent service isolation vs. a small coordinated team | Independent services can be right for one; a modular application for the other |
| Independently deployed clients vs. fully controlled clients and approved downtime | Staged compatibility may be essential in one; a validated direct cutover in the other |
| Same rule owned by one domain vs. similar syntax owned by separate jurisdictions | Centralize genuinely shared policy without coupling independent meanings |
| Technology mandated by a supported platform vs. an open greenfield choice | Respect settled constraints; compare options only if a real choice remains |
| Legacy code with unrelated pre-existing red tests vs. a passing baseline | Establish attributable behavior evidence rather than treating every existing failure as a new regression |

Use counterfactual fixtures that vary **one material assumption** (traffic, deployment, tenancy,
latency, durability, operations). Check that the design responds to material changes and is stable
against irrelevant wording. Penalize copied diagrams, categorical "one worker always" or "gradual
migration always" rules, fabricated metrics, pointless alternatives, and unnecessary artifacts.
Preserve strict safety, authorization and evidence requirements.

## Representative Decision Cases

- Existing extension point versus parallel implementation; duplicated syntax versus shared knowledge.
- Routine multi-consumer change: stable ownership of one decision versus duplicated defaults, context flags, or needless coordination; legitimate edits across layers are not penalized.
- Greenfield design meeting realistic workloads without speculative distributed infrastructure.
- Brownfield plan separating supported contracts from incidental implementation and suspected defects.
- Hybrid cutover with mixed-version readers, authoritative writes, validation, and old-path removal.
- Hidden links, needless links, surplus and special cases used as diagnostic evidence, not as a mandate to refactor unrelated code.
- A consequential interface/performance decision with a simpler alternative and representative workload.
- Legacy characterization followed by a desired behavior change; observable effects/error order matter.
- Public API or rolling data migration; old/new readers and writers have actual compatibility obligations.
- Repeated or uncertain operations; concurrent schedules and lifecycle transitions protect an invariant.
- Test doubles: legitimate interaction assertions versus claims of real delivery from a mock call.
- Security: valid versus cross-tenant access, a counterexample that defeats a scanner false positive,
  and a threat hypothesis whose deployment prerequisite is unverified. Do not conduct live exploitation.

For TDD, verify the intended behavioral assertion fails before implementation and passes afterward;
setup/import failures are not the red evidence. Observe artifact and command history, not self-reported
compliance. Include a preservation case where no new feature test is needed and a pre-existing dirty
worktree that must not be deleted to recreate an ideal sequence.

## Grade Outcomes, Not Ceremony

| Signal | Independent evidence |
| --- | --- |
| Correctness | Acceptance checks, invariants, integration behavior and regression cases |
| Plan quality | Relevant owners, ordered steps, testable acceptance, explicit uncertainty, and no unauthorized edits |
| Repository fit | Correct owner, supported conventions, actual contracts and appropriate change surface |
| Simplicity | Avoidable state/options/layers, knowledge duplication, coupling and reader burden |
| Verification | Required commands actually executed, meaningful selection/assertions, honest limits |
| Security quality | Reachability, attacker capability, actual impact, effective controls and calibrated uncertainty |
| Invocation | Actual skill/reference reads on relevant tasks, non-activation on controls |
| Efficiency | Input/output/cached tokens, tool calls, duration and cost per accepted outcome where available |

Capture deliberately run trials with `codex exec --json`; logs may contain private repository context.
Keep traces, credentials and personal settings out of source control. Record every attempted run,
blocked check and missing measurement. Never fabricate a monetary cost from a subscription percentage.

Inspect tool outputs and artifacts for actual file loading and actions. Metadata availability alone
is not activation; activation is not correct application. A command's unrelated trailing failure need
not erase an earlier valid read; resolve host skill-root aliases before interpreting file paths.
Do not grade success from keyword matches, an agent's explanation or package tests.

Acceptance checks should reject seeded wrong implementations and accept an independent correct one.
Review design/finding quality blind where practical. Report catastrophic regressions separately, and
adopt a candidate only when repeatable useful gains justify added cost and false activations.

## Low-Cost Structural Checks

In a temporary home/profile, place the defaults and selected skill folders in their documented native
locations. Where available, `codex debug prompt-input` renders context without a model response.
Check personal and repository scope, an uninstalled control, valid metadata paths and lazy body loading.
Validate extracted packages too, including all references and licenses. Ordinary CI needs no model call.

Structural checks do not establish positive/negative automatic selection, independent correctness,
teaching quality, token savings or improvement over the actual Codex + working TDD baseline. No new
benchmark framework, service, subagent orchestration or third-party analyzer is required for this pilot.
