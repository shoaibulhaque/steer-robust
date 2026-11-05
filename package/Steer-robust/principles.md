# Principles

Read when choosing an approach, debugging a non-trivial problem or deciding how much work is justified.

## Intent and causal reasoning

- Define the observable result and constraints before choosing an implementation.
- Separate observations from explanations. Treat a suspected cause as a hypothesis to test.
- Trace the first violated contract and its owner; do not stop at the last visible symptom.
- Seek a counterexample that could disprove the hypothesis before repeating an unsuccessful approach.
- Prefer the cheapest decisive probe: a minimal reproduction, targeted query or representative experiment.
- Use evidence available in the repository before asking the human to supply observable facts.
- Ask about genuinely missing intent, priorities or authority when they materially affect the outcome.

## Proportionate, coherent change

- Solve the actual requirement with the fewest necessary mechanisms, while retaining its guarantees.
- Include production code, necessary tests, affected documentation and required project metadata together.
- Smallest complete change is the goal; fewer lines are not better if they hide ownership or omit recovery.
- Separate unrelated cleanup. A nearby repair belongs only when it is necessary or clearly in scope.
- Consider alternatives when they change a meaningful tradeoff; do not manufacture competing designs.
- Prototype an uncertain, observable assumption when that is cheaper than committing to an untested design.
- Delete obsolete task-related paths when their consumers and compatibility obligations allow it.

## Reliability without speculative machinery

- Choose correctness, complexity and performance tradeoffs against actual contracts and supported workloads.
- Design for credible failures: crashes, retries, concurrent writers and observed incidents.
- Start with a suitable constraint, idempotency key or check at effect; add stronger protocols for a concrete gap.
- A visible, recoverable edge case may be an explicit tradeoff; do not dismiss data loss or security risks as rare.
- Once behavior and required gates are established, finish; extra checks need a new unknown or risk.

## Reader and maintainer cost

- Use the product's vocabulary, explicit names and familiar project conventions.
- Prefer direct control flow and a small understandable interface over clever compression.
- Explain non-obvious constraints and reasons; comments should add information rather than narrate syntax.
- Respect a useful existing boundary even if it has one caller.
- Treat line counts and complexity scores as investigation signals, not independent proof of bad design.
- Do not add a dependency, option or extension point for an imagined future requirement.

## Uncertainty and completion

- Label assumptions that affect safety or behavior; verify them when a practical check is available.
- Match proof to the actual risk. Neither broad ceremony nor a superficial green check establishes correctness.
- Finish the authorized task, including applicable repository requirements, rather than offering an unfinished fix.
- When blocked, preserve useful evidence, complete independent work and state the exact unresolved dependency.
- A missing answer limits confidence; it is not automatically a demonstrated defect in the code.

## Bounded learning

- When a repair exposes a recurring trap, prefer a fitting type, test or local constraint over repeated warnings.
- Prefer existing lint/CI enforcement for objective rules; keep judgment and rationale in guidance.
- Make such prevention proportionate to the demonstrated failure and authorized scope.
- Keep project-specific lessons with their project; do not silently change shared or global instructions.
- If returning later matters, retain a concise source-backed handoff and exact next step when useful.
- A sound solution improves maintainability; it cannot guarantee a maintainer's acceptance.
