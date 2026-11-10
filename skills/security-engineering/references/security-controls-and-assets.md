# Security Controls and Assets

**Read when:** selecting relevant assets, tracing enforcement or checking review coverage. These are
questions for the scoped system, not an unconditional implementation checklist.

## Asset Categories

Consider user data, identity/session artifacts, authorization state, secrets, configuration, executable
artifacts, audit evidence and availability-critical resources. For agent products, include tool access,
retrieved content and privileged actions. Identify the owner and promised protection for each relevant asset.

## Security Control Categories

| Boundary | Evidence to inspect |
| --- | --- |
| Identity and access | Authentication establishes identity; authorization checks the current action, object and tenant. Opaque IDs do not replace permission checks. |
| Input and output | Validation occurs at the owner; encoding/parameterization matches the destination. Parsing or type safety alone does not establish authorization. |
| Network and remote access | Actual TLS/proxy trust, redirect/DNS behavior, destinations, deadlines and credential propagation. |
| Files, archives and native memory | Containment across symlinks/traversal, size/resource limits, ownership, integer conversions and failure cleanup. |
| Persistence and concurrency | Atomicity/isolation, operation identity, replay safety and effects outside transactions. |
| Data lifetime | Collection, redaction, retention, caches, backups, replay and deletion of derived records. |
| Supply chain and deployment | Build inputs, supported dependencies, artifact provenance and actual production configuration. |
| Agent/tool execution | Untrusted text remains data; executable argument validation, per-action permission and effect controls exist outside the model. |

## Mitigation Phrasing

Name the boundary, protected asset, exact enforcing component and a rejecting test. "Improve security"
is not an implementation plan. For example: enforce current object-and-tenant authorization before
returning a stored record; test a different tenant through the real endpoint. Prefer the project's
existing protection over a parallel framework.

## Evidence Limits

A static candidate needs reachability and impact analysis. A simulated exploit verifies only its
modeled assumptions. A passing authorization test for one route does not prove coverage of all routes.
Use maintained project and official framework guidance for version-specific implementation details.


## Worked Case: Tenant-Scoped Object Access

**Claim under review:** "Report URLs are unguessable, so other tenants cannot access reports."

An opaque ID can reduce guessing, but does not establish authorization. Inspect the real report-download entry point: identity resolution, current tenant membership, object lookup, permission enforcement and the eventual read or signed download. Check whether another route, queue consumer, or pre-signed link bypasses the intended decision where in scope.

A focused controlled test uses two tenants and a report owned by tenant A:
- A permitted A user can retrieve the report.
- A valid B user who is given A's ID is rejected through the **real entry point**.
- The rejection occurs before protected bytes or sensitive metadata are returned. If the operation can create side effects, verify those do not occur.

The expected denial must come from the declared contract. A model-generated route name or a scanner string is not evidence that the route is reachable. A test on a mocked permission helper is not proof that the production endpoint actually invokes it.

**Report with calibrated certainty:** if a reachable alternate path bypasses the check, identify the path, required attacker capability, affected asset and demonstrated impact. If the route's deployment exposure or upstream access policy is unknown, classify the scenario as conditional until that fact is established. Propose enforcement at the owning object/tenant boundary and a rejecting regression test. Do not exercise someone else's live records to prove the point.
