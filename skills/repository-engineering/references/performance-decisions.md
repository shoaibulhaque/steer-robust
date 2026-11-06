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

Know which operations are fundamentally expensive, in rough orders of magnitude:

| Operation | Typical cost |
| --- | --- |
| Network round trip within a datacenter | Tens of microseconds |
| Wide-area network round trip | Tens to hundreds of milliseconds |
| Disk I/O | Milliseconds; flash storage tens to hundreds of microseconds |
| Dynamic memory allocation | Significant, including freeing and garbage collection |
| Cache miss to main memory | Hundreds of instruction times |

Measure the ones that matter with small micro-benchmarks in the project's environment instead of
trusting the table.

## Prefer Naturally Efficient Choices

Often the efficient design is just as simple as the slow one. Choose it by default:

- For keyed lookup, a hash table is commonly several times faster than an ordered map; use the ordered
  map only when you need its ordering.
- Store small records inline in an array instead of allocating each one separately behind a pointer.

When the faster design adds only a little complexity and hides it behind an unchanged interface, it may
be worth doing now. When it adds substantial complexity or a more complicated interface, start simple
and optimize when measurements show the need, unless clear evidence already shows performance will matter.

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
