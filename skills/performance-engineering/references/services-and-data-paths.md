# Backend, API, Storage and Distributed Data-Path Performance

**Read when:** slow services, high tail latency, costly or chatty data access, contention, queue
backlogs, throughput limits or excessive memory/compute appear in a server or data API workload.

## Follow One Real Request and Its Dependencies

Trace **ingress → auth and validation → domain work → database/storage → remote calls → serialization
→ response**, including queue wait, connection pool wait, cache and retries. Establish representative
request mix, dataset shape, cardinality, concurrency and the service's actual limits before naming a
bottleneck.

A 200 ms API can be CPU-bound, waiting for a pool, acquiring a lock, performing many DB queries,
blocking on a remote dependency, or spending most of its time serializing a huge response. These
mechanisms require different solutions. A profiler, query plan, span tree or targeted timing probe
should distinguish them before an architectural rewrite.

## Find Work That Scales with the Wrong Quantity

| Signal | Investigate | Common tradeoff of a fix |
| --- | --- | --- |
| Query count grows with returned rows | ORM lazy relation loads, per-item permission or metadata lookup | Eager fetching may retrieve excessive data or bypass per-object visibility if misapplied |
| Many small round trips | Chatty RPC, repeated Redis access, per-row remote enrichment | Batching can increase memory, first-item latency or partial-failure complexity |
| Response size explodes | Unbounded list, overfetch, repeated serialization or large nested objects | Pagination changes client ordering/cursor contract |
| CPU high with high allocation | Parsing, serialization, redundant transforms, inefficient representation | Retained caches or native code add memory and safety costs |
| Throughput collapses at concurrency | Connection pools, locks, saturated downstream service or noisy neighbor | Higher concurrency can worsen contention or overload another tier |
| Tail latency spikes | Queueing, GC, retries, fan-out, cold instances or dependency timeouts | Retry/parallelism changes may amplify load |
| Slow writes with integrity errors | Lock contention, constraints, transaction scope, hot-row conflicts | Relaxing isolation or splitting transactions may violate invariants |

A datastore's performance cannot be inferred from its type alone. Use actual query/EXPLAIN plans,
index statistics, row counts, realistic lock behavior and representation before introducing another
database or cache. Do not replace a correct data model solely to achieve a lab microbenchmark.

## Data and Cache Correctness

Caches are state with identity, validity, freshness, eviction and failure semantics. Specify:
- what exact computation or remote result the entry represents;
- key dimensions (including user, tenant, permissions, locale and input version where relevant);
- whether stale results can be served, and for how long;
- invalidation triggers and ownership;
- memory bounds, isolation and fallback on a miss or failure.

A public-content cache has different requirements from a tenant-sensitive entitlement cache.
A cached result computed under a previous permission does not become safe because it is fast.

Incremental processing helps when a small input change should not recompute unaffected results,
but only if dependencies and change detection are trustworthy. Recompute safely when those
assumptions do not hold.

## Scheduling, Backpressure and Overload

A system that admits more work than it can complete can accumulate queues, consume memory and
eventually worsen latency for everyone. Identify **where admission and capacity are enforced**.
Possible controls include bounded parallelism, pooling, queue limits, load shedding,
deadlines, fair scheduling, cancellation of obsolete work and user-visible progress.

Choose these according to product guarantees:
- A disposable search suggestion may be cancelled when a newer input arrives.
- A paid order accepted durably must not disappear because a client closes its tab.
- A retry after ambiguous remote outcome needs stable identity/deduplication; random backoff alone
  cannot prevent duplicate business effects.
- A per-tenant quota may protect shared resources better than global IP limits.

Retries under overload can form a retry storm. Bound attempts, deadlines, and concurrency and
account for downstream pressure. A circuit breaker is useful only if it meaningfully protects a
real dependency and has a correct recovery path.

## Worked Case: API Latency Climbs with Result Count

An endpoint serves 200 records. A trace shows repeated calls to a pricing provider from inside
each serializer invocation. The number of remote calls grows with output size.

**First question:** does the provider support a compatible batch API? If so, batching may remove
network overhead while preserving order, partial errors, authentication and per-tenant data policy.
If not, bounded concurrency, partial results, a domain-owned snapshot or a different data contract
may be appropriate. Do not automatically cache mutable prices or silently send an entire tenant's
data to a third party.

**Proof:** for representative result sizes and concurrency, record number of remote requests,
p50/p95 latency and error outcomes before and after. Check returned prices and permission scope.
A fast mocked provider in unit tests cannot establish the real network benefit.

## Cost and Capacity

Estimate per-request CPU time, DB/IO work, bytes transferred and external request counts; relate
them to peak arrival and concurrency rather than monthly averages alone. Consider billing for
idle resources, storage reads, data transfer, third-party APIs and observability. Spending more
resources can be rational to meet a hard reliability requirement; reducing cost while violating
latency or data integrity is not a valid optimization.

## Sources

- [Microsoft Azure: Performance Antipatterns](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/)
- [Microsoft Azure: Chatty I/O](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/chatty-io/)
- [Google SRE: Non-Abstract Large System Design](https://sre.google/workbook/non-abstract-design/)
- [AWS: Performance Efficiency](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- [Django: Database Access Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
