# Performance and complexity

Read when scale affects a design, changing expensive paths or claiming an optimization.
Match effort to realistic sizes and the dominant resource; a complexity label is not itself a defect.

## Understand the cost

- Name actual dimensions: rows, tenants, requests, files, references, bytes or concurrent operations.
- Estimate time and additional space before and after when they affect the choice.
- Identify realistic ranges, worst supported cases and hot-path frequency from evidence.
- A quadratic scan over a tiny bounded set may be clearer than an elaborate index.
- Investigate hidden multiplication: nested scans, repeated parsing, serialization, sorting and allocation.
- Count database queries, filesystem operations and network round trips; I/O often dominates CPU.
- Account for query plans and index behavior using the project's tools when those determine the result.
- Include retained data, closures, buffers, queues and caches; a small reference may keep a large allocation alive.

## Improve at the stable scope

- Move invariant work to the scope where its inputs are stable before adding a cache.
- Choose a data structure that matches actual lookups and updates without hiding invalidation costs.
- Batch equivalent I/O where contracts allow it; preserve ordering, failure isolation and resource limits.
- Cache only with an explicit key, lifetime, capacity, invalidation rule and failure policy.
- Do not reuse data across authorization or tenant boundaries merely to improve hit rate.
- Bound background work at the same scarce resource used by interactive requests.
- For UI work, consider payload, bundle, request waterfalls and unnecessary render work where relevant.

## Measure a credible comparison

- State the question and metric before running a benchmark.
- Compare equivalent work, correctness and supported cases on identified revisions/artifacts.
- Hold relevant workload and environment conditions constant; account for warmup, caching and noise.
- Use repetitions sufficient for the variability and decision; do not impose a universal run count.
- Measure the limiting resource and end-to-end effect when local improvements may shift the bottleneck.
- Report counter-costs: memory, allocation, disk/network traffic, startup time and operational complexity.
- Explain why a surprising result represents the intended work rather than a shortcut or measurement artifact.
- Treat a query count or microbenchmark as evidence for that metric, not automatic production speedup.

## Maintainability cost

- Use project complexity and lint thresholds where present; lower numbers do not prove better design.
- Consider control-flow depth, hidden state, coupling and the number of places a change must touch.
- Prefer a clear algorithm for realistic input sizes over clever code with a negligible measured benefit.
- Reassess an optimization if it introduces more failure modes than the demonstrated benefit justifies.

## Report the result

Name the workload, before/after metric, method and important limits.
Label measured, estimated and inferred costs separately; do not turn character counts into measured tokens.
An unmeasured hypothesis may guide the next experiment, but must not be reported as a verified speedup.
