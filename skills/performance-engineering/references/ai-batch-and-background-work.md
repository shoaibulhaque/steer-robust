# AI, Batch Pipelines and Asynchronous Work

**Read when:** optimizing RAG, inference, embeddings, ingestion, ETL, reports, media pipelines, or
long-running background jobs where work duplication, queueing, model calls or resource cost matter.

## Identify the Actual Pipeline

For AI: **request → retrieval/filtering → context assembly → model execution → tool calls →
postprocessing → user result**. For batch: **input/version detection → transform → durable output →
commit/checkpoint → downstream consumption**. Distinguish useful output latency, full completion,
backlog, throughput, energy/compute cost and quality/correctness.

A faster model call is not automatically a better AI application: token cost, retrieval errors,
lost citations, incorrect tool effects or reduced answer quality may dominate the outcome.

## Eliminate Unnecessary Work Safely

- Reuse unchanged parsing, chunking or embedding work when input version, model/version,
  segmentation, tenant visibility and invalidation are known.
- Deduplicate work by a meaningful stable identity; avoid merging distinct requests that share
  superficial text but require different permissions or freshness.
- Process changed data incrementally, with a clear deletion/reindex strategy when source content
  changes or is revoked. Stale vectors can leak old or unauthorized content.
- Batch work where supported and beneficial. Batching can improve throughput at the cost of
  first-result latency and error isolation; streaming can improve perceived latency without
  reducing total tokens or compute.
- Cache deterministic outputs or provider responses only with appropriate identity, expiration,
  model/prompt version, privacy and correctness contracts. Not every model output is safely
  reusable.
- Avoid unnecessary tool loops, repeated context construction, oversized payloads and
  reprocessing of completed stages. Limit agent recursion, token budgets, tool calls and
  concurrent work based on actual goals.

## Concurrency and State

A worker system needs distinct treatment of **acceptance, claim, attempt, durable effect,
acknowledgment and recovery** when failures can occur between them. An asynchronous function is not
a durable job queue; a background request that survives navigation is different from a server-side
operation guaranteed to survive process failure.

Bound workers and external provider concurrency. Under provider quota pressure, increasing
parallelism can increase retries, cost and latency. Use scheduling and backpressure compatible with
user-facing priority and fairness. Define what may be cancelled or superseded and what must complete.

An uncertain remote effect requires reconciliation or idempotent identity where business consequences
matter. Retrying a timed-out charge or write without knowing its outcome can create duplicate effects.

## Worked Case: Re-Embedding Every Document on Each Deploy

A multi-tenant knowledge app rebuilds vectors for all documents whenever code is deployed. It is
slow and costly, and stale records may remain after a user deletes content.

A better **candidate** flow checks document revision/hash, model and chunking version, tenant scope
and deletion state before recomputing only required items. Persist checkpoints and reconciliation
signals; updates and deletes invalidate derived embeddings and retrieval index records. The index is
not authoritative over its source records.

**Security check:** a query from tenant B must never retrieve vectors derived from tenant A, even if
cache keys or vector metadata are malformed. The actual retrieval enforcement is more important
than the model's instruction to "ignore other tenants."

**Verification:** compare full and incremental rebuild outputs over controlled create/update/delete
fixtures, record staged latency/cost and verify permission/deletion outcomes. A faster rebuild
without deletion correctness is not an improvement.

## Worked Case: Streaming an AI Response

Streaming can improve time to first visible token, but may worsen rendering work if the client
re-renders the entire transcript for every token. If the UI is the bottleneck, coalesce safe
presentation updates while retaining logical output order and cancellation behavior. Do not
confuse displaying partial text with completing a durable server operation.

Evaluate first-useful-output latency, end-to-end completion, total tokens, server resources,
client responsiveness and quality. A fast-looking spinner or immediate streaming cursor does not
prove the content is delivered efficiently.

## Decision Evidence

For high-cost pipelines, select meaningful stage timings, cache hit/miss reasons, per-tenant resource
use, retry counts, error/quality rates, and output correctness checks. A fake model, mock vector
store or single short prompt can confirm local logic but not production serving throughput.

Do not mandate a vector database, queue product, inference server, streaming protocol or caching
framework. Choose components from the real product and operating constraints.

## Sources

- [Google SRE: Non-Abstract Large System Design](https://sre.google/workbook/non-abstract-design/)
- [Microsoft: Retry Storm Antipattern](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/)
- [AWS: Performance Efficiency](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/design-principles.html)
- [OWASP: LLM Security](https://genai.owasp.org/llm-top-10/)
