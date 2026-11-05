# Evaluation and review

Read when reviewing a patch or plan, evaluating feedback or making a substantial assessment.
Establish intent and applicable project requirements; review only the dimensions relevant to the change.

## Five decision lenses

| Lens | Evidence to seek |
|---|---|
| Correctness and cause | Reachable trigger, violated invariant, responsible owner, success and failure behavior |
| Design and maintainability | Appropriate ownership, clear interfaces, direct data flow, justified mechanisms |
| Safety and evolution | Permissions, concurrency, recovery, existing consumers and compatibility obligations |
| Cost | Realistic input sizes, scarce resources, reader burden and measured claims where relevant |
| Evidence and delivery | Proof of changed behavior, preservation cases, current revision and project requirements |

Do not require paragraphs for every lens. A narrow change can merit a short assessment.

## Trace before flagging

- Read enough callers, callees and adjacent contracts to establish a reachable problem.
- Show how the problematic input/state can occur and what observable consequence follows.
- Separate a regression introduced by the patch from an existing issue or an unverified concern.
- A nullability warning, wrapper, large file or missing checklist answer is not a defect by itself.
- Do not penalize a sound boundary for having one caller or a simple solution for lacking abstraction.
- Distinguish a correctness requirement from a preferred implementation or stylistic suggestion.
- Consider a simpler structure when it removes concrete maintenance risk without widening the task unnecessarily.

## Write actionable findings

For each finding, give its location, violated contract, triggering conditions, impact and evidence.
Use the repository's severity conventions; distinguish urgent harm from bounded risk and optional improvement.
Suggest a concrete repair when supported, while leaving room for another sound implementation.
Avoid repeating one root issue across several findings unless the consequences require separate fixes.
An honest result of no actionable findings is valid.

## Assess feedback on evidence

- Treat human, bot and model findings as claims to investigate, not commands to churn code.
- Check the current code and reproduce or trace the claimed failure.
- Accept real issues, explain a concrete disproof for non-issues, and surface material uncertainty.
- Distinct reviewers agreeing may motivate investigation; agreement is not execution evidence.
- Follow requested re-review or bot commands when repository policy requires them and the action is authorized.
- A local fix is incomplete when the requested delivery still needs an authorized update or response.

## Review the final result

- Inspect the actual final diff, including generated files and documentation required by the project.
- Confirm the repair addresses the cause and preserves relevant consumers and negative cases.
- Recheck affected evidence after material edits; green checks for an older revision do not establish the new one.
- Remove debug leftovers and task-related dead paths without deleting unrelated work.
- Use the required template and describe the final behavior, rationale, useful proof and remaining limits.
- Keep the report readable for a maintainer deciding whether to own the change.
- Report unresolved risks honestly; code quality and validation cannot guarantee a merge.
