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
