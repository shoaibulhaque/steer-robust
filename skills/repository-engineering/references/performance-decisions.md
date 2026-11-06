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
