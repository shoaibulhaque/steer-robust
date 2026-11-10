# Greenfield Design

**Read when:** defining an initial application or service architecture without an existing implementation that dictates ownership or integration conventions.

## Derive the Design from Real Work

Begin with a representative end-to-end user or operational scenario: who initiates it, what must happen, where an irreversible effect occurs, and what constitutes success. Separate essential functionality, nonnegotiable constraints, expected growth, and open assumptions. Do not turn a desired technology into an unstated business requirement.

Convert consequential quality attributes into scenarios. For example, "fast" needs a particular workload and latency objective, and "reliable jobs" needs a specified failure outcome. If numbers are unknown, identify the uncertainty and a future measurement rather than inventing capacity.

## Draw the First Boundaries

1. Identify the authoritative source for each important decision and data item: identities, authorization, content, payments, or other domain-specific concepts.
2. Group rules by reason to change. Keep distinct meanings separate even when their names or data shapes match.
3. Define public contracts at boundaries that actually matter: input, output, errors, side effects, ownership and version expectations.
4. Choose the simplest deployment structure that meets today's constraints. A modular application can have strong internal boundaries without separately deployed services.
5. Trace a thin vertical slice through UI or API, domain behavior, persistence, and one external effect where relevant. Prefer a working path over building every layer as an independent framework.

A new abstraction earns its existence by hiding meaningful volatility, protecting an invariant, or clarifying domain intent. Do not add a service, broker, cache, or plugin system solely because it may be needed later.

## Capacity and Operations as Design Inputs

Estimate only quantities that could change the architecture: peak arrival rate rather than only daily averages, concurrent in-flight work, per-request CPU and memory, payload size, storage growth, and remote provider limits. Use explicit units and ranges; distinguish assumed inputs from measured values.

Consider the smallest sustainable operational model: how configuration and secrets enter, how migrations run, how failures surface, how an operator can restart or recover work, and who owns backups if stored data is critical. An unneeded cluster adds operational risk; a "single server" still requires a recovery decision when losing that server would violate a stated guarantee.

Do not make "cloud-native" synonymous with distributed. Prefer known, well-supported dependencies and contracts over novelty. If an unusual technology is proposed, name the requirement that needs it and the cost of replacing it.

## Challenge the Initial Architecture

Compare the candidate with a credible simpler option when the consequences justify it. Evaluate likely bottlenecks, uncertain integration behavior, data loss or duplication, security boundaries, and cost of operating the design.

An uncertainty can justify a narrow spike or benchmark with a predefined success criterion. The spike is evidence about feasibility, not a substitute for a behavior specification.

Examples:

- A static site with a CMS may need content validation, draft access control, and reliable builds; it does not thereby need a general event-driven backend.
- A scheduled report may need one durable worker. Add a distributed work system only if actual workload, recovery, or isolation needs warrant it.

## Plan the First Delivery

Order work by dependencies and risk: representative contract and data model, one end-to-end path, relevant failure cases, supporting features, then operational hardening and deployment. State acceptance evidence for each important outcome. Record reversible technology choices as such, and name observable conditions that would trigger reconsideration.

For a substantial greenfield system, the first end-to-end slice should prove the boundaries most likely to invalidate the design—such as persistent job acceptance, tenant-scoped reads, or a vendor API—rather than a collection of isolated interfaces that cannot yet communicate.

**Avoid these failures:**
- Choosing microservices because the domain has several modules.
- Treating expected business growth as measured production load.
- Proposing a cache without explaining freshness, invalidation, and a baseline bottleneck.
- Modeling success paths while leaving ownership of failed or cancelled operations undefined.
- Creating every abstraction before any user-visible workflow is demonstrable.

A plan is adequate when another engineer can implement the first valuable slice without guessing which component owns the essential rules. Do not imply that pre-launch capacity estimates were production measurements.
