# Threat Modeling

**Read when:** explicitly asked for a threat model or an abuse-path analysis of a repository, service,
or design. A threat model is a design assessment: a threat hypothesis is not a confirmed vulnerability
because it appears in a table.

## Contents

- Quick start
- Workflow: eight stages
- Risk calibration
- Output contract

## Quick Start

Collect or infer: the in-scope paths, intended usage, deployment model, internet exposure, expected
authentication, and any existing architecture notes. Infer what the repository shows; label everything
else as an assumption. Do not invent components, endpoints, stores, flows, or controls to fill a
template. Anchor every architectural claim to one or two repository paths, symbols, or config keys.
Never output secret values; describe only their presence and location.

## Workflow

### 1. Scope and Extract the System Model

Identify the repository shape: languages, frameworks, how it runs (server, CLI, library, worker),
entry points, and build artifacts. Then search for security-relevant surfaces:

- Network listeners, routes, RPC handlers, and message consumers.
- Authentication, sessions and tokens, authorization checks, roles and ACLs.
- Parsing and deserialization (JSON, YAML, XML, protobuf), template rendering, dynamic code execution.
- File uploads and reads, archive extraction, image and document parsing.
- Database, queue, and cache clients, and how queries are built.
- Secrets and configuration loading, key management.
- Outbound HTTP clients, webhooks, and URL fetchers (SSRF surfaces).
- Sandboxing, privilege boundaries, and subprocess execution.
- Logging, auditing, and error-handling paths.
- CI, build, and release: pipelines, dependency management, artifact publishing.

Separate runtime behavior from CI, build, dev tooling, tests, and examples. Include tooling only when it
controls a relevant trust or release boundary. List out-of-scope items explicitly.

### 2. Derive Boundaries, Assets, and Entry Points

Record each trust boundary as a concrete edge between components:

- Source and destination.
- Data crossing it: credentials, personal data, files, tokens, prompts.
- Channel or protocol: HTTP, gRPC, IPC, file, database.
- Guarantees: authentication, encryption, origin checks, schema validation, rate limits.

Enumerate entry points: endpoints, upload surfaces, parsers and decoders, job triggers, admin tooling,
and logging or error sinks. Include tool entry points for agent products.

### 3. Calibrate Assets and Attacker Capabilities

For each asset, state why it matters in confidentiality, integrity, or availability terms, including
compliance or user harm. Describe realistic attacker capabilities from the exposure and intended use.
State non-capabilities explicitly, such as no network access to internal services or no admin
credentials, to prevent inflated severity.

### 4. Enumerate Threats as Abuse Paths

Write each threat as an attacker story: **goal → controlled input → crossed boundary → sensitive effect
→ impact**. Tie it to entry points, boundaries, and privileged components. Prefer multi-step abuse paths
over one-line generic threats. Consider repeated, out-of-order, and concurrent actions when they can
violate an invariant. STRIDE or another method can prompt questions; never generate a quota of threats
from categories. Keep the number of threats small and each one high quality.

### 5. Prioritize with Likelihood and Impact

For each threat:

- **Likelihood:** low, medium, or high, with a one- or two-sentence justification.
- **Impact:** low, medium, or high, with a one- or two-sentence justification.
- **Priority:** critical, high, medium, or low, from likelihood × impact, adjusted for existing controls.

State which assumptions most affect the ranking. Mark conditional paths and evidence gaps. Distinguish
missing hardening from a reachable exploit. Do not dismiss a credible serious impact because it is
unusual, and do not assign severity from an API name alone.

### 6. Validate Service Context and Assumptions

Compare the assumptions with repository configuration and known deployment facts; resolve
contradictions. Summarize the three to six assumptions that most affect scope or ranking. When an
answer would materially change the result, ask one to three targeted questions: service owner and
environment, scale and users, deployment model, authentication and authorization, internet exposure,
data sensitivity, multi-tenancy. If the context is already available, or the user cannot answer,
proceed and mark the affected conclusions as conditional.

### 7. Recommend Mitigations and Focus Paths

For each high or critical threat, give:

- Existing mitigations, with evidence anchors.
- Gaps and weaknesses.
- Recommended mitigations in code, configuration, or process, placed at the owning component.
- Detection and monitoring ideas, where they change the outcome.

Prefer specific implementation hints over generic advice: "enforce the upload schema at the gateway"
rather than "validate inputs". Include recovery or monitoring only where it matters; logs never replace
prevention. Mark recommendations conditional when their assumptions remain unresolved.

List 2 to 30 focus paths for manual review, each with a one-sentence reason tied to a threat.

### 8. Quality Check Before Finalizing

- [ ] Every discovered entry point is covered.
- [ ] Every trust boundary appears in at least one threat.
- [ ] Runtime and CI or dev risks are kept separate.
- [ ] User clarifications, or their absence, are reflected.
- [ ] Assumptions and open questions are explicit.
- [ ] Major claims have evidence anchors; no exhaustive coverage is claimed for unread components.

## Risk Calibration

Tailor the levels to the repository's assets and exposure, with two or three examples per level.
Illustrative defaults:

| Priority | Typical examples |
| --- | --- |
| Critical or high | Pre-auth remote code execution, authentication bypass, cross-tenant access, sensitive data exfiltration, key or token theft, sandbox escape, integrity compromise of models, configuration, or build artifacts |
| Medium | Targeted denial of service of a critical component, partial data exposure, rate-limit bypass with measurable impact, log or metric poisoning that weakens detection |
| Low | Low-sensitivity information leaks, noisy denial of service with easy mitigation, issues that need unlikely preconditions |

## Output Contract

Match the requested artifact; a focused question may need only a short answer. For a full threat model,
use these sections in order. Write it to a file only when asked or when the repository requires one.

1. **Executive summary:** one paragraph on the top risk themes and highest-risk areas.
2. **Scope and assumptions:** in-scope and out-of-scope paths, assumptions, and open questions that
   would change the ranking.
3. **System model:** primary components; data flows and trust boundaries as arrow bullets
   (`Internet → API server`) with data, channel, guarantees, and validation for each; optionally one
   compact Mermaid `flowchart` with trust zones as subgraphs.
4. **Assets and security objectives:** table of asset, why it matters, and objective (C, I, or A).
5. **Attacker model:** capabilities and non-capabilities.
6. **Entry points and attack surfaces:** table of surface, how reached, trust boundary, notes, evidence.
7. **Top abuse paths:** five to ten numbered sequences of goal, steps, and impact.
8. **Threat table:** threat ID (`TM-001`…), source, prerequisites, action, impact, impacted assets,
   existing controls with evidence, gaps, recommended mitigations, detection ideas, likelihood, impact
   severity, priority.
9. **Criticality calibration:** what each priority level means for this system, with examples.
10. **Focus paths for security review:** table of path, why it matters, related threat IDs.

Keep threat IDs stable across revisions. Never require a fixed number of threats or include credentials.
