# Threat Modeling

**Read when:** explicitly asked for a threat model or abuse-path analysis. This is a design assessment;
a threat hypothesis does not become a confirmed code vulnerability merely by appearing in a table.

## Quick Start

Identify requested scope, intended usage, deployment, important assets and authoritative repository
evidence. Infer what is observable; label assumptions and ask only for missing context that materially
changes the model. Do not invent endpoints, stores or controls to fill a template.

## Workflow

### 1. Scope and Extract the System Model

Identify runtime components, services, stores and external integrations. Separate development/tooling
paths unless they control relevant assets. Follow the concrete in-scope data flows and evidence anchors.

### 2. Derive Boundaries, Assets and Entry Points

For each relevant edge, record source/destination, data, privilege transition, protocol and existing
validation/authorization. Include job, upload, administrative and tool entry points where applicable.

### 3. Calibrate Assets and Attacker Capabilities

State what an attacker controls, what access is required, and what is outside their capabilities.
Distinguish confidentiality, integrity and availability objectives for actual assets, including tenant
isolation, build artifacts or agent-tool permissions when those matter.

### 4. Enumerate Threats as Abuse Paths

Trace goal → controlled input → crossed boundary → sensitive effect → impact. Consider out-of-order,
repeated and concurrent actions when they can violate an invariant. STRIDE or another established
method can prompt questions; do not generate a quota of threats from categories.

### 5. Prioritize with Likelihood and Impact

Explain prerequisites, exposure, severity and effective controls. Mark conditional paths and evidence
gaps. Distinguish missing hardening from a reachable exploit; do not dismiss credible serious impact
because it is unusual or award severity from an API name alone.

### 6. Validate Service Context and Assumptions

Compare assumptions with repository configuration and known deployment facts. Resolve contradictions.
Ask a targeted question when the answer would materially change scope or a conclusion; otherwise
proceed with explicit limits. A report need not pause when the required context is already available.

### 7. Recommend Mitigations and Focus Paths

Separate existing controls from proposals. Place each proposal at an actual owner, explain the
protected guarantee and verification, and identify residual risk. Include recovery/monitoring where
it changes the outcome, without replacing prevention with logs or demanding unrelated infrastructure.

### 8. Quality Check Before Finalizing

Check that major claims have evidence, relevant entry points/boundaries have been considered, missing
coverage is stated, and findings reflect assumptions and counterevidence. Keep runtime and build risks
distinct. Do not claim an exhaustive review of uninspected components.

## Report Format

Adapt to the requested artifact; a focused question may need only a short answer. For a full model:

1. Scope, assumptions and evidence anchors.
2. Components, data flows, trust boundaries and assets.
3. Attacker capabilities/non-capabilities and entry points.
4. Prioritized abuse paths, prerequisites, existing controls, mitigations and residual risk.
5. Focus paths, missing evidence and verification plan.

A compact diagram is useful when it clarifies boundaries; it is optional. Stable IDs help track threats
across revisions. Never include credentials or require a fixed number of threats, paths or severity examples.
