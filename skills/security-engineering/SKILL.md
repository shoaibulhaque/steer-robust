---
name: security-engineering
description: "Use when explicitly asked for a security review or audit, a threat model or abuse-path analysis, secure-coding guidance, or hardening of authentication, authorization, tenant isolation, secrets, input handling, SSRF, file handling, or agent tool permissions. Grounds findings in reachable code paths. Not for ordinary feature work, general code review, or non-security design."
---

# Security Engineering

## Overview

Produce security decisions grounded in the repository, for the scope the user requested: secure-coding
guidance or hardening, a security review, or a threat model.

**Core principle:** a finding connects an attacker capability, a reachable path, and a concrete impact,
each backed by source evidence. A plausible threat is not a verified vulnerability.

## Choose the Mode

| Request | Mode | Output |
| --- | --- | --- |
| "Make this secure", "harden X", "how should I handle tokens here?" | Secure coding | A bounded correction or advice at the affected boundary |
| "Review this for security", "audit this service" | Security review | Validated, prioritized findings |
| "Threat model this", "what could an attacker do?" | Threat model | The eight-stage [Threat Modeling](references/threat-modeling.md) workflow |

## Stack Guidance

Establish the actual languages, frameworks, versions, and deployment from repository evidence: lock
files, build metadata, and configuration. Then read the manual for each stack in scope, covering both
backend and frontend when the system has both. Read only the matching manuals.

| Read when the repository uses | Manual |
| --- | --- |
| Django | [python-django-web-server-security.md](references/python-django-web-server-security.md) |
| Flask | [python-flask-web-server-security.md](references/python-flask-web-server-security.md) |
| FastAPI | [python-fastapi-web-server-security.md](references/python-fastapi-web-server-security.md) |
| Express or a Node.js HTTP server | [javascript-express-web-server-security.md](references/javascript-express-web-server-security.md) |
| Next.js | [javascript-typescript-nextjs-web-server-security.md](references/javascript-typescript-nextjs-web-server-security.md) |
| React | [javascript-typescript-react-web-frontend-security.md](references/javascript-typescript-react-web-frontend-security.md) |
| Vue | [javascript-typescript-vue-web-frontend-security.md](references/javascript-typescript-vue-web-frontend-security.md) |
| jQuery | [javascript-jquery-web-frontend-security.md](references/javascript-jquery-web-frontend-security.md) |
| Browser JavaScript or TypeScript without one of the frameworks above, or an unspecified frontend | [javascript-general-web-frontend-security.md](references/javascript-general-web-frontend-security.md) |
| Go services | [golang-general-backend-security.md](references/golang-general-backend-security.md) |

Before choosing a new mechanism, search the repository's security guidance and existing middleware;
prefer the protection the project already uses.

How to apply a manual:

- **Its rules are a review checklist, not findings.** Each rule still needs a traced, reachable path
  before it is reported as a vulnerability.
- **Verify versions.** Each manual names the versions it was written for. Check defaults and APIs
  against the project's installed version and that version's official documentation. Do not carry a
  manual's version pin into a project that uses another version.
- **Use it per mode.** For secure coding, apply the relevant existing protection. For review, verify its
  actual configuration and bypass paths. For a threat model, separate what the framework guarantees
  from what application code must still enforce.
- **Scope follows this skill.** The manuals describe generation, passive review, and audit modes; apply
  only the mode the user requested. Their passive mode applies while this skill is active, not to
  unrelated work.
- **Deployment controls may be invisible.** A protection absent from the repository may exist in a
  proxy, gateway, or platform. Report it as "not visible in application code; verify in deployment".

No language is excluded. For a stack without a manual, use the project's security guidance and the
framework's official security documentation for the supported version, and inspect parsing, privilege,
memory and resource ownership, and integration assumptions. A missing manual is a coverage limit, not
permission to invent secure defaults. In a review, do not report a generic checklist as demonstrated
defects.

To find candidates, search for entry points and sensitive operations: routes, message consumers, file
and archive handlers, subprocess calls, outbound HTTP clients, template and HTML sinks, deserializers,
and permission checks. A search match is a lead, not a finding.

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

## Example: Applying One Manual Rule

The FastAPI manual's rule `FASTAPI-AUTHZ-001` names an insecure pattern: `GET /users/{id}` returns a
user record without verifying that the caller can access that `id`. Applying it in a review:

1. **Lead:** list endpoints that take an identifier from the path, query, or body, as the rule's
   detection hint says.
2. **Trace:** for each one, follow the handler from authentication to the data access. Is the record
   compared with the caller's identity, role, or tenant before it is returned?
3. **Falsify:** look for an owner filter in the query, a shared dependency or middleware, or a
   database row-level policy that already enforces access.
4. **Classify:** no check anywhere on the path means a confirmed finding. A check that depends on
   deployment configuration you cannot see means a conditional one.
5. **Report** with the fields from the Report step: location, the trigger (an authenticated caller
   requests another user's `id`), the impact (another user's data is returned), the counterevidence
   checked, and the rule's fix: an object-level ownership, ACL, or tenant check, plus a response model
   that returns only allowed fields.
6. **Verify a fix** with two tests through the real endpoint: another user's `id` is rejected, and the
   owner's own request still succeeds.

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
- Severity assigned from an API name or scanner rule alone.
- "Validated somewhere upstream" assumed without locating the check.
- A fix tested only on the allowed case, never on the denied one.

## Verification Checklist

- [ ] Scope, mode, and stack versions are stated.
- [ ] Each finding is classified as confirmed, conditional, or hardening, with evidence.
- [ ] Counterevidence was sought for each finding.
- [ ] Mitigations name the owning component and a rejecting test.
- [ ] Coverage gaps and assumptions are listed; no secret values appear in the output.
