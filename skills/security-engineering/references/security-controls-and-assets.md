# Security Controls and Assets

**Read when:** choosing which assets and controls apply to the scoped system, tracing enforcement, or
checking review coverage. Pick only what applies; this is not an unconditional implementation checklist.

## Asset Categories

- User data: personal data, content, uploads.
- Authentication artifacts: passwords, tokens, sessions, cookies.
- Authorization state: roles, policies, ACLs, tenant membership.
- Secrets and keys: API keys, signing keys, encryption keys.
- Configuration and feature flags.
- Models and weights, for ML systems.
- Source code and build artifacts.
- Audit logs and telemetry.
- Availability-critical resources: queues, caches, rate limits, compute budgets.
- Tenant isolation boundaries and metadata.
- For agent products: tool access, retrieved content, and privileged actions.

For each relevant asset, name its owner and the protection it is promised.

## Control Categories and Evidence

| Category | Controls | Evidence to inspect |
| --- | --- | --- |
| Identity and access | Authentication, authorization, session handling, mTLS, key rotation | Authentication establishes identity; authorization checks the current action, object, and tenant. Opaque IDs do not replace permission checks. |
| Input and output | Schema validation, parser hardening, output encoding | Validation happens at the owner; encoding or parameterization matches the destination. Type safety alone does not establish authorization. |
| Network | TLS, network policies, WAF, rate limiting, DoS controls | Actual TLS and proxy trust, redirect and DNS behavior, allowed destinations, deadlines, credential propagation. |
| Files, archives, native memory | Path containment, size limits, sandboxed parsers | Containment across symlinks and traversal, size and resource limits, ownership, integer conversions, cleanup on failure. |
| Data protection | Encryption at rest and in transit, tokenization, redaction | Key management, which fields are encrypted, where plaintext appears in logs or caches. |
| Persistence and concurrency | Transactions, constraints, idempotency | Atomicity and isolation, operation identity, replay safety, effects outside transactions. |
| Isolation | Process sandboxing, containers, tenant isolation, seccomp | The boundary actually enforced at runtime, not the one in a diagram. |
| Observability | Audit logs, alerting, anomaly detection, tamper resistance | What security-relevant events are recorded, without logging secrets or personal data. |
| Supply chain | Dependency pinning, SBOMs, provenance, signing | Build inputs, supported dependencies, artifact provenance, actual production configuration. |
| Change control | CI checks, deployment approvals, configuration guardrails | Who can change production behavior and how changes are reviewed. |
| Agent and tool execution | Per-action permission, argument validation, effect controls | Untrusted text stays data; enforcement lives outside the model. |

## Personal Data Across Its Lifetime

When the change touches personal data, trace what is collected, inferred, exposed, retained, replayed,
and deleted. Logs, caches, search indexes, analytics events, backups, and derived records can keep
sensitive data after the primary record changes or is deleted. Use synthetic data in tests and fixtures.

## Mitigation Phrasing

Name the boundary, the protected asset, the enforcing component, and a rejecting test. "Improve
security" is not a plan. Patterns:

- "Enforce schema at `<boundary>` for `<payload>` before `<component>`."
- "Require an authorization check for `<action>` on `<resource>` in `<service>`."
- "Isolate `<parser>` in a sandbox with `<resource limits>`."
- "Rate-limit `<endpoint>` by `<key>`, with burst caps."
- "Encrypt `<data>` at rest with `<key management>`, and rotate `<keys>`."

Example: enforce current object-and-tenant authorization before returning a stored record, and test a
different tenant through the real endpoint. Prefer the project's existing protection over a new framework.

## Evidence Limits

A static candidate needs reachability and impact analysis. A simulated exploit verifies only its modeled
assumptions. A passing authorization test for one route does not prove coverage of all routes. Use
maintained project and official framework guidance for version-specific details.
