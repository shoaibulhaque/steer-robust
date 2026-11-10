---
name: security-engineering
description: "Use for explicit security reviews, threat models, secure-coding or hardening work involving APIs, auth, tenant isolation, AI tools, secrets, dependencies, CI/CD or infrastructure. Investigate real trust boundaries and verify candidate findings. Not an automatic deep audit for ordinary coding, refactoring or general PR review."
---

# Security Engineering

## Overview

Produce security decisions grounded in the repository, for the scope the user requested: secure-coding
guidance or hardening, a security review, or a threat model.

**Core principle:** a finding connects an attacker capability, a reachable path, and a concrete impact,
each backed by source evidence. A plausible threat is not a verified vulnerability.

**Two layers of responsibility:** `AGENTS.md` already requires secure-by-default engineering in
every relevant change. This skill is for focused security design, hardening, investigation and reporting
when those are the requested task. Do not make an ordinary feature or PR review invoke a full audit
solely because it touches authenticated code. Conversely, do not defer fixing a known security
regression merely because this specialized skill was not invoked.

## Plan-Only Requests

A security plan distinguishes hypotheses from confirmed vulnerabilities. Identify relevant assets, trust boundaries, attacker capabilities, controls and their owners, and rejecting tests. Label deployment assumptions. Do not edit code, infrastructure, or credentials or claim the proposed controls are implemented or tested.

## Choose the Mode

| Request | Mode | Output |
| --- | --- | --- |
| "Make this secure", "harden X", "how should I handle tokens here?" | Secure coding | A bounded correction or advice at the affected boundary |
| "Review this for security", "audit this service" | Security review | Validated, prioritized findings |
| "Threat model this", "what could an attacker do?" | Threat model | The scoped [Threat Modeling](references/threat-modeling.md) workflow |
| "Deep audit", "validate these findings", "check coverage" | Assurance | Trace candidates, seek counterevidence, record findings and limits |

Establish the actual languages, frameworks, and versions from repository evidence. For stack-specific
controls, read only the matching rows of [Stack Guidance](references/stack-guidance.md), then the
project's and framework's documentation for that version. No language is excluded: a stack without
listed guidance is a coverage limit, not permission to invent secure defaults. In a review, do not
report a generic checklist as demonstrated defects.

## Workflow

### 1. Scope the System

Identify the in-scope paths, assets, deployment assumptions, and the user's question. Separate runtime
code from build, CI, and test tooling; include tooling when it controls a trust or release boundary.
Trace real entry points through validation, authorization, and effects. A dependency, file name, or
scanner hit does not prove code is present or reachable.

### 2. Map Boundaries and Attacker Capabilities

For each relevant entry point, answer:

- Who controls the input, and are they authenticated?
- Which object, tenant, or action is targeted?
- Where does privilege change, which component enforces the check, and is there a credible bypass?
- What can the attacker not do? Non-capabilities prevent inflated severity.

Read [Security Controls and Assets](references/security-controls-and-assets.md) when choosing which
assets and control categories apply, or when checking review coverage.

### 3. Investigate and Falsify

For each candidate, trace **source → transformation → enforcement → sensitive operation**. Look for
counterevidence: an unreachable path, effective validation, an upstream check, or a deployment restriction.
Use a harmless, isolated reproduction when feasible. Never exploit live systems, disclose secrets, or
expand permissions.

Classify each result:

- **Confirmed:** a reachable path with a feasible trigger and concrete impact.
- **Conditional:** exploitable only if an unverified assumption holds; name the assumption.
- **Hardening:** a missing defense-in-depth control with no demonstrated path.
- **Open question:** context needed before the candidate can be classified.

### 4. Prioritize by Actual Impact

Rate each finding from its prerequisites, exposure, affected assets, and harm, after accounting for
effective controls. A dangerous API name or a missing optional header is not high severity by itself.
Rarity does not make data loss, cross-tenant access, or a credible privilege bypass acceptable.

### 5. Report

Follow the requested format. A full review report contains:

1. Scope, coverage, and assumptions.
2. Findings, most severe first. For each: ID, location, classification, trigger, impact, counterevidence
   considered, and a concrete mitigation at the owning component.
3. What was not covered and how each finding can be verified.

Keep threat-model hypotheses separate from confirmed vulnerabilities. Write a report file only when
asked or when the repository requires one. Never include secret values.

## Conditional References

Use only references that help resolve the in-scope question; do not turn them into a mandatory
checklist. Consult current official guidance for the deployed platform and versions.

- [API and Parser Boundaries](references/api-and-parser-boundaries.md): API authorization,
  parser differences, XML, uploads, URL fetchers, SSRF and outbound trust.
- [AI Application Boundaries](references/ai-application-boundaries.md): LLM/RAG context, tenant
  retrieval, model/tool execution, high-impact actions and resource use.
- [Build and Secrets Integrity](references/build-and-secrets-integrity.md): package resolution,
  CI permissions, artifacts, provenance, credentials and rotation decisions.
- [Runtime and Observability](references/runtime-and-observability.md): servers, containers,
  reverse proxies, platform identity, audit logs and actionable detection.
- [Audit Evidence and Coverage](references/audit-evidence-and-coverage.md): broad or deep audit
  coverage, falsification, independence when useful, and evidence-backed reporting.
- [Threat-Informed Defense](references/threat-informed-defense.md): prioritize concrete protections
  against AI-accelerated or automated intrusions, exposed services, credential theft, exploited
  vulnerabilities and compromised coding-agent workflows. Do not infer compromise from a threat report.
- [Threat Modeling](references/threat-modeling.md): scoped abuse-path modeling.
- [Security Controls and Assets](references/security-controls-and-assets.md): relevant assets,
  controls and review coverage.
- [Stack Guidance](references/stack-guidance.md): supported-framework control discovery.

## Assumptions and Project Overrides

Project contracts and the supported deployment govern implementation choices. When a local exception
weakens a protection, state the tradeoff and the residual risk; do not declare it safe. Ask only when
missing context would change the scope or a conclusion. Otherwise proceed with labeled assumptions;
do not require a ceremonial confirmation before every report.

## Fixes

A review-only request does not authorize edits. When fixes are authorized:

- Fix coherent findings; preserve legitimate behavior.
- Use the applicable testing workflow, including rejected, unauthorized, and cross-tenant cases.
- Verify both the protection and its connection: the real entry point must reach the check.
- Recheck the affected evidence after the fix.
- Do not add dependencies, rotate credentials, publish findings, or change infrastructure without scope.

## Durable Security Rules

- An unpredictable identifier does not replace object- and tenant-level authorization.
- Check current authority at the protected operation. A check made earlier can be stale after permissions,
  ownership, or time change.
- Validate input where it enters and encode output for its destination: SQL, HTML, shell, URL, or path.
- Establish real TLS, proxy, and cookie behavior before recommending a change. Avoid breaking local
  development. Do not assume an unseen deployment is insecure, and do not dismiss a missing production
  control.
- In native code, check size arithmetic, signedness, conversions, and buffer ownership.
- In agent products, treat retrieved content and model output as untrusted data. Enforce permissions and
  validate effects at the tool boundary; a prompt instruction is not an isolation mechanism.

## Red Flags — Recheck Before Reporting

- A finding with no traced path from attacker input to sensitive operation.
- A scanner, uploaded skill, or role-played persona treated as a substitute for authorization,
  observed configuration, or evidence.
- Mandatory exploitation, artificial vulnerability chains, or blanket hardening unrelated to scope.
- Severity assigned from an API name or scanner rule alone.
- "Validated somewhere upstream" assumed without locating the check.
- A fix tested only on the allowed case, never on the denied one.

## Verification Checklist

- [ ] Scope, mode, and stack versions are stated.
- [ ] Each finding is classified as confirmed, conditional, or hardening, with evidence.
- [ ] Counterevidence was sought for each finding.
- [ ] Mitigations name the owning component and a rejecting test.
- [ ] Coverage gaps and assumptions are listed; no secret values appear in the output.
