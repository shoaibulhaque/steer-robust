# Architecture Evaluation

**Read when:** the design involves material performance, reliability, security, cost, modifiability, or migration tradeoffs, or an important feasibility claim has weak evidence.

## Turn Qualities into Concrete Scenarios

For each consequential quality attribute, name the stimulus, operating condition, affected component, and observable response. A claim such as "highly available" or "secure" has little value until the scenario says what failures, actors, or guarantees are in scope.

Use few high-impact scenarios rather than a checklist of every conceivable quality.

| Attribute | Illustrative scenario to refine from real requirements |
| --- | --- |
| Throughput | Under the agreed peak request mix, which component saturates first and at what operational cost? |
| Resilience | If a worker fails after an external effect but before acknowledgement, what state and duplicate outcome remain? |
| Compatibility | Can an old client work during a rolling deployment with the new API writer? |
| Security | Can a user with one tenant's credentials operate on another tenant's records? |
| Changeability | Can one pricing policy change without editing unrelated provider implementations? |

These are example prompts, **not default acceptance thresholds**. Identify known measurements, assumptions, and the evidence needed to validate them.

## Challenge Consequential Decisions

Compare the candidate with a credible simpler alternative, or two genuinely different options if no simple baseline exists. Evaluate:

- Functional coverage and correctness invariants.
- Change surface and knowledge required of callers.
- Capacity or failure behavior under realistic workload and deployment assumptions.
- Operational ownership, cost, observability, and rollback.
- Reversibility and the price of a wrong decision.

Do not give every option a pseudo-precise score or treat complexity as inherently good or bad. Explain why the selected tradeoff fits the constraints.

## Reduce Uncertainty Before Committing

Identify claims that would change the design if disproven: storage performance, an external API contract, consistency assumptions, library support, or migration downtime. Define a bounded experiment with a representative workload or input, a success criterion, and what decision each outcome changes.

An experiment can establish feasibility only under its tested conditions. A local benchmark does not prove internet-scale traffic; mocks do not prove end-to-end durability; a load test without failure injection cannot establish recovery.

## Preserve the Decision

Record the selected approach, consequential rejected alternatives, assumptions, tradeoffs, and **reconsideration triggers** when future maintainers would otherwise lose the rationale. An ADR, compact decision paragraph, or diagram may be appropriate; neither a formal review meeting nor a long report is mandatory.

## Example

A small product requests asynchronous certificate generation. A single durable worker may meet the present concurrency and recovery requirements. A broker cluster would add independent failure and operations surfaces. If measured queueing time or worker isolation eventually violates the stated service objective, that becomes a reason to reconsider, not a reason to deploy the cluster today.
