# Architecture Evaluation

**Read when:** the design involves material performance, reliability, security, cost, modifiability, or migration tradeoffs, or an important feasibility claim has weak evidence.

## Turn Qualities into Concrete Scenarios

For each consequential quality attribute, name the stimulus, operating condition, affected component, and observable response. A claim such as "highly available" or "secure" has little value until the scenario says what failures, actors, or guarantees are in scope.

Use few high-impact scenarios rather than a checklist of every conceivable quality.

A useful scenario names **stimulus, operating condition, response, and measure**. For example:
"While old and new API instances coexist, an old reader must accept records created by the new writer
without losing the existing required fields." This is more decisive than "support compatibility."
A latency scenario needs a representative request mix and environment; a reliability scenario needs
a failure point, observable state, and recovery behavior.

Do not invent numerical SLOs to complete a table. When the user has not supplied a target, identify
the missing measurement or offer a clearly labeled assumption that can later be validated.

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

A useful challenge pass asks:
1. **Correctness:** which invariant can fail under an actual concurrent, partial, or reordered schedule?
2. **Scale:** what resource saturates first under the expected work and how would we observe it?
3. **Changeability:** what future change already implied by the requirements would force unrelated modules to co-change?
4. **Operations:** who notices and resolves a stuck state, malformed deployment, or failed migration?
5. **Reversibility:** which decision is costly to undo, and what is the contingency if its assumption fails?

Select the questions that threaten the proposed design; avoid reporting harmless hypothetical risks as blockers.

## Reduce Uncertainty Before Committing

Identify claims that would change the design if disproven: storage performance, an external API contract, consistency assumptions, library support, or migration downtime. Define a bounded experiment with a representative workload or input, a success criterion, and what decision each outcome changes.

An experiment can establish feasibility only under its tested conditions. A local benchmark does not prove internet-scale traffic; mocks do not prove end-to-end durability; a load test without failure injection cannot establish recovery.

**Decision experiment:** "At the expected peak input size and concurrency, measure job completion
time and memory for one worker. If the result meets the agreed objective with acceptable headroom,
keep one worker; otherwise compare bounded parallel workers before introducing a broker cluster."
The plan describes how to gather evidence, not an invented performance outcome.

## Preserve the Decision

Record the selected approach, consequential rejected alternatives, assumptions, tradeoffs, and **reconsideration triggers** when future maintainers would otherwise lose the rationale. An ADR, compact decision paragraph, or diagram may be appropriate; neither a formal review meeting nor a long report is mandatory.

If a design is difficult to reverse, state both the evidence that justified it and a failure signal
that warrants re-evaluation. A plan should not silently commit to an irreversible schema or vendor
choice while treating the rationale as an unchangeable truth.

When the selected architecture has a meaningful long-lived guarantee, consider a small repeatable
fitness check (dependency-boundary test, API compatibility check, workload regression, or failure
schedule) that would detect erosion. Do not invent a new framework merely to call it a fitness test.

## Example

A small product requests asynchronous certificate generation. A single durable worker may meet the present concurrency and recovery requirements. A broker cluster would add independent failure and operations surfaces. If measured queueing time or worker isolation eventually violates the stated service objective, that becomes a reason to reconsider, not a reason to deploy the cluster today.
