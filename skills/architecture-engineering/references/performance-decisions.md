# Performance Decisions

**Read when:** performance is a requirement, a reported defect, or a consequential design tradeoff.
This guide does not require benchmarking ordinary edits.

## Overview

**Core principle:** choose naturally efficient simple designs, and require evidence before paying
substantial complexity for an optimization.

## Describe the Workload

Identify input size, skew, read/write mix, concurrency, fan-out and important latency/resource limits.
Separate CPU, allocation/memory, I/O, network round trips and queueing. A favorable asymptotic label
does not describe remote-call count or the tail latency of a heavily contended operation.

For example, scanning a collection once may be simpler than maintaining an index for a small local
list. Repeating a remote lookup per item can dominate a superficially linear function; a supported
batch operation may remove that cost without creating a cache consistency problem.

## Establish a Comparison

Use representative inputs and a baseline with the same semantics, environment and relevant state.
Distinguish warm-up, cold/warm caches, setup and actual operation time. Repeat enough to detect useful
differences rather than trusting one noisy number; preserve raw observations when needed for review.
A microbenchmark answers its modeled question, not automatically the end-to-end workload.

## Prefer Removing Work

Remove invariant repeated work, unnecessary conversions, round trips or inappropriate representations
before adding concurrency, caching or custom algorithms. Reuse supported project/library capabilities.
If an optimization introduces retained state, include memory growth, invalidation, correctness and
operational costs in the choice. Faster incorrect answers are not an acceptable optimization.

Do not trade away ordering, authorization, freshness or precision silently. Surface material UX,
maintainer and agent-navigability costs. A useful performance boundary can hide implementation cost
without forcing every caller to understand the optimization.

## Verify and Stop

Recheck the affected behavioral contract and compare the relevant workload. State measured benefit,
conditions and uncertainty. Keep the simpler implementation when the gain does not justify its costs;
stop when the actual requirement is met instead of expanding into a tuning project.

## Worked Case: List Endpoint Becomes Slow

A production API serves a list of orders. Latency increases with number of results. Before introducing Redis or rewriting the entire query layer, establish the actual shape of work.

Map the request as **request validation → authorization and tenant scope → query → serialization → remote enrichment → response**. Record number of database queries, rows read, remote calls, query plans where available, and percentile latency under representative load. An apparently efficient O(n) loop can make n remote requests and become network-bound; a single large query can be index or lock-bound.

Choose the remedy from the observation:

| Evidence | Candidate direction | New risk to assess |
| --- | --- | --- |
| Repeated query per row | Batching, eager-loading or targeted query changes | Authorization scope and excessive fetched rows |
| Excessive response size | Pagination or bounded fields | Client contract, ordering and stable cursor semantics |
| Expensive repeated invariant conversion | Compute once at appropriate ownership boundary | Stale derived state if persisted |
| Slow external per-row calls | Provider batch, bounded concurrency or async composition | Rate limits, failure amplification, partial results |
| Contended state or large table scan | Index or query strategy, database-specific analysis | Write overhead, correctness and maintenance |
| Stable hot reads with validated freshness requirements | Cache at a justified boundary | Invalidation, tenant mixups, stale permission and eviction |

Do not benchmark merely to justify a preselected cache. A measured improvement should include the query mix, dataset size, hardware/environment, and what was excluded. If the optimization changes ordering, precision, caching semantics or tenant access, it is a contract change with its own tests.

## Capacity Reasoning Without Fabricated Numbers

Average daily work is not peak demand. For a queued service, estimate arrival bursts, service time, concurrency and backlog tolerance separately. For a storage design, distinguish raw data growth from indexes, replication, backups and retention. When figures are unknown, label them as assumptions and choose a measurement or sensitivity analysis that would change the decision.

A useful design question is: **which resource saturates first at the expected demand, how is that observable, and what reversible step follows?** It need not be answered with a distributed architecture. Conversely, isolation, durability or team ownership may justify a dedicated service without a high request rate.

## Tail Latency and Failure

The 95th percentile of an end-to-end request is not the sum of component p95s. Correlated fan-out, retries and contention can amplify tails; test representative concurrency and dependency failure where they materially affect user experience.

Retries can worsen saturation. If a performance remedy adds retries, a queue or parallelism, bound work and understand cancellation, deadline and overload behavior. Improvement is not sound if it creates duplicate payments or removes authorization.

## Decision Record

For a consequential optimization, state baseline, candidate, changed assumptions, observed benefit, correctness checks and rollback implications. If no representative measurement is available, call the choice provisional; do not present a guessed speedup as fact.
