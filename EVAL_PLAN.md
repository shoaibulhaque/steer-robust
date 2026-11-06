# Evaluate Before Adoption

These are proposed experiments, not completed model trials. Compare with the user's actual Codex
setup, working TDD skill and applicable repository instructions. Do not disable useful baseline
safeguards to make candidates look better. Record all active instruction/skill versions and conditions.

## Controlled Comparisons

| Condition | Difference from baseline | Main question |
| --- | --- | --- |
| A: baseline | None | What does the actual working Codex + TDD setup achieve? |
| B: defaults | Candidate AGENTS.md only | Do durable defaults add benefit without unnecessary work? |
| C: design | B plus repository-engineering | Better ownership/abstraction choices on consequential tasks? |
| D: debugging | B plus systematic-debugging | Better diagnosis of uncertain failures without slowing clear ones? |
| E: review | B plus change-verification | Better explicit review/readiness without activation during ordinary coding? |
| F: security | B plus security-engineering | Grounded scoped analysis without false audit activation or inflated findings? |
| G: packaged TDD | B with packaged TDD replacing baseline TDD | Does the packaged version improve feedback and test quality? Never load both TDD versions. |
| H: refactoring | B plus refactoring | Safer behavior-preserving steps and legacy characterization without behavior drift? |

Test the combined configuration only after useful individual results. If an existing setup already has
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
| Repository engineering | Add a substantial feature through an existing extension point; independent domain rules must stay independent | Mechanical local rename |
| Systematic debugging | Intermittent duplicate effects survive earlier fixes; response can be lost after a write | Supplied failing example with already established cause |
| TDD | Implement testable behavior with a discriminating new example | Prose-only correction; a pure refactor should not trigger it |
| Refactoring | Split a long untested function before a requested change; a latent bug must be reported, not silently fixed | A requested new feature with no restructuring |
| Change verification | Review a patch for PR readiness against actual contribution/CI rules | Routine implementation or merely running a specified test |
| Security engineering | Explicit scoped security review, secure-coding request or threat model | Ordinary feature work touching an authenticated route; still preserve security without starting a full audit |

A typo-only task should load none of these workflows. Include tasks where two responsibilities really
apply, without requiring all skills. For advanced references, check that the relevant guide is read
when needed and unrelated guides remain unloaded.

## Representative Decision Cases

- Existing extension point versus parallel implementation; duplicated syntax versus shared knowledge.
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
