> Historical research for the previous Steer Robust framework. Implementation claims below describe that revision, not the current toolkit.

# Refactor research and audit

Research performed 2026-11-05 on shallow clones under a temporary directory outside this repository.
The following immutable revisions were inspected; sources are evidence, not imported operating permissions.

| Upstream | Revision |
|---|---|
| steipete/agent-scripts | d210c0a77c8f9ae5e1d939b13238a75e87cdb69a |
| cursor/plugins (pstack) | bb68f2365eceafa0cb2d253112f675acf5f144cc |
| unclebob/ub-mode | 3da62bf3fcfd2034de41f30d920d2739e566171f |
| unclebob/crapper | 6fd92c4c9bcc56efb64a2f8743d5a2993bcfd42d |
| unclebob/dryer | 66ff6d21a42c04afcad89c78a80066176d1294b0 |
| unclebob/mutator | a5a0cb803b66e0cdb8bf471b3b08af701d424a41 |
| unclebob/uml-viewer | f65dafe93b3cb1b4e6bb02dbe41503ed05bd9ebf |

## Actual implementations inspected

- [Peter's compact CLI skill](https://github.com/steipete/agent-scripts/blob/d210c0a77c8f9ae5e1d939b13238a75e87cdb69a/skills/create-cli/SKILL.md)
  links one conditional reference; `scripts/validate-skills` safely parses metadata and detects concrete hazards.
  Retain compact entrypoints and rerunnable checks, not the personal tool catalog or machine policies.
- [Pstack statechart](https://github.com/cursor/plugins/blob/bb68f2365eceafa0cb2d253112f675acf5f144cc/pstack/skills/statechart/SKILL.md),
  `scripts/run.ts`, `passes/paths.ts`, corpus and backend layout: TLC checking, named actions,
  shortest safety counterexamples and Mermaid projection. Its full engine installs Java/TLC with mise,
  rechecks rules and projects graphs/regions. We implement a smaller original wrapper, no auto-install,
  one-worker safety checking and faithful counterexample visualization; no claim of full graph/liveness support.
- Pstack `principle-build-the-lever`, `principle-minimize-reader-load` and `principle-prove-it-works`:
  representative units, reproducible evidence, layers-to-trace and mutable-state burden.
  Qualify these: one caller can justify a boundary; nontrivial work need not always create a script.
- [ub-mode](https://github.com/unclebob/ub-mode/blob/3da62bf3fcfd2034de41f30d920d2739e566171f/SKILL.md):
  data shape, domain vocabulary, discriminating tests, root causes and preservation during refactoring.
  Reject mandatory metrics thresholds, action logs, unconditional tools and default push-to-main.
- Crapper `src/crapper/cli.py`, coverage/runner design and README: CRAP combines complexity and coverage;
  default collection can install tools or produce 0% after failure. Our guide requires qualified inputs.
- Dryer `src/dryer/cli.py`, scan contract and README: normalized structural fingerprints and Jaccard
  candidates are review leads; they do not establish shared business responsibility.
- Mutator `src/mutator/runner.py`, worker-overlay behavior and README: use a passing baseline and isolated
  changed sources; inherited imports can accidentally run unmutated code. Compile-invalid and timed-out
  mutants must not be mistaken for evidence of assertion quality.
- UML viewer `src/uml_viewer/domain/policy.clj`, README and dependency direction: grouping and coupling
  should express domain ownership. Its Clojure/Java GUI, topology generation, tmux companion and metrics
  pipeline are deliberately not adopted. No custom AST/repository-map system was added.

## Existing tools, not a new analyzer framework

[Radon](https://radon.readthedocs.io/en/latest/intro.html) measures branch complexity;
[Complexipy](https://complexipy.com/about/) measures cognitive complexity.
[Ruff C901](https://docs.astral.sh/ruff/rules/complex-structure/) and
[ESLint complexity](https://eslint.org/docs/latest/rules/complexity) can enforce project-owned thresholds.
[Stryker](https://stryker-mutator.io/docs/) and [mutmut](https://mutmut.readthedocs.io/en/latest/)
illustrate selective assertion-strength checks; PIT and cargo-mutants fit other existing language toolchains.
No analyzer was installed or universalized. The new analyzer reference is conditional and distinguishes failure classes.

## Repository audit and redesign

Audited all three original skills, ten guides, four helpers, distribution contract/builder and existing tests.
The original root linked useful material, but no normal implementation workflow required cause/design reads.
Check selection and runtime proof repeated policy, and Claude skill discovery was left to manual inference.

- Add one implementation entrypoint requiring cause/design before editing, then only relevant detail.
- Keep old skill names, guide paths and archive adoption layout. Detail remains with one owning guide.
- Shorten the root and verification router; runtime QA consumes its proof plan rather than starting over.
- Add a focused statechart skill and one optional runner, rather than importing pstack's large engine.
- Preserve tested guidance discovery/retrieval helpers; remove custom repo-map creation instructions.
- Add conflict-preflight adoption for native Codex and Claude paths; generated copies share canonical sources.
- Keep developer tooling and opt-in real-model evaluations outside the distributed package.

## Licensing and scope

The TLC wrapper is original. Cloudflare audit methodology was used with its full MIT notice retained.
No upstream orchestration engine, analyzer implementation or full attack-reference catalog is vendored.
Attribution names the practices studied; it does not claim upstream endorsement or import its license onto our code.
Pstack has mixed plugin licensing; absent a clear applicable grant, do not copy its engine into this MIT package.
External optional Java/TLC downloads were used only in temporary live checks, never bundled or installed globally.
A real Codex sandbox blocked BFS RMI sockets. Source inspection of TLC 1.7.4 exposed a zero-exit DFID
depth-bound hazard; the wrapper supports iterative deepening and requires explicit completion in both modes.
The official TLC 1.7.4 jar was SHA-256 checked against the digest in the inspected upstream runner.

## Client contract

[Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) explains native metadata and conditional loading;
[CLI reference](https://learn.chatgpt.com/docs/cli/reference) documents JSON events and noninteractive execution.
[Claude skills](https://code.claude.com/docs/en/skills) use native `.claude/skills/` discovery.
Directory/link validation establishes layout, not live adherence. Real trials and limits are recorded separately.

## Additional research from the revised acceptance brief

| Upstream | Inspected revision | Transferable practice |
|---|---|---|
| cloudflare/security-audit-skill | c1c8a8c1471069fb0e188eeaff69b8e8db6564a8 | Boundary-first findings, falsification, coverage and honest classification |
| vercel/eve | 4693029ebed813b2de8ab3a92d3173b6f4e0ff9c | Four-question test-value gate, independent test ownership and retention exceptions |
| kestra-io/kestra | 9be71d009caaed50051d96d9c69035d4e4d79575 | Tests that fail for meaningful reasons; native architecture and repository-backed security checks |
| datahub-project/datahub | bb8f8edccef9207237f615ee950678ac32531e44 | Native verification wrappers and scoped project contracts across languages |
| can1357/oh-my-pi | 88a69582c755bd000e8dc0290981fc787a4f400c | Externally observable contracts, suite-safe mocks and real lifecycle/installation surfaces |
| BerriAI/litellm | 79e63d3e06f3af3cbe20216f7d3462f521acee41 | Stable owned invariants, opt-in live checks and regression cases at real callback owners |

Read actual `SKILL.md`/agent instructions plus focused supporting code/tests:
Cloudflare's attack companions, validation/reporting and validator tests; Eve's `.agents/skills/test-audit`
and campaign/retention rules; Kestra's `BaseArchitectureTest` and `AbstractSQLInjectionTest`; DataHub's
`AuthUsageRequestContextTest` and ingestion secret-registry tests; oh-my-pi's real port-conflict listener
and model-color behavior tests; LiteLLM's unit instructions, budget-limiter regression and live-test helper.
These are selective inspections, not full audits or endorsements of every observed test.

Adapt the reasoning, not stack policies. Keep real unique security/lifecycle tests even if slow;
make expensive proof cheaper when possible instead of deleting guarantees. Do not import absolute mock bans,
metric quotas, automatic live API calls, review agents, style rules or publication permissions.
Cloudflare's multi-agent hunt and independent model verification become sequential source falsification
plus deterministic evidence; we explicitly do not claim same-agent review is independent.

The revised brief replaces arbitrary code-length gates with justified engineering quality.
Instruction word budgets remain disclosure-cost controls; line/function/abstraction/test quotas are absent.
The package preserves existing paths while giving required reads concrete workflow owners.
