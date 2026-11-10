# Build, Dependency and Secret Integrity

**Read when:** reviewing or hardening dependency manifests, release pipelines, CI/CD authority, artifacts, credentials or secret handling. This reference is not a mandatory setup checklist.

## Trace What Is Trusted

Identify the actual dependency resolver, lockfile semantics, build inputs, release artifact, deployment environment, and who can alter each. Inspect the permissions available to CI jobs, third-party actions and build scripts. A vulnerable package name or mutable tag is a review lead, not by itself a demonstrated exploitable deployment.

### Dependencies and Artifacts

- Use supported lockfiles or checksums for the chosen language and package manager where reproducible installation matters. Verify their *actual* semantics; not all files represent a fully locked dependency tree.
- Assess known vulnerabilities by affected version, reachability, triggering conditions, deployed use, and remediation availability. A scanner warning is evidence to investigate, not proof of practical impact.
- Compare pinned container digests or CI action revisions with update strategy. Immutability prevents surprise changes but also requires deliberate patching.
- Consider an SBOM for inventory and incident response, or signing/provenance for high-consequence release chains. These can improve traceability; they do not replace verification of the artifact that actually runs.

### CI/CD Permissions

Inspect whether untrusted PR code can run with privileged credentials, whether package installation executes scripts, who approves production changes, and whether an artifact can be replaced after validation. Prefer least privilege and ephemeral credentials such as workload identity or OIDC when supported and appropriate; never assume CI permission settings are safe without checking the workflow and provider.

Choose release gates around credible impact and fixability. Avoid both "ignore every scanner failure" and "block on every advisory regardless of reachability." Record approved exceptions with owners and review conditions when the project uses them.

### Secrets Across Their Lifetime

Trace creation, storage, injection, runtime access, logs/traces, rotation, revocation and accidental exposure. Do not commit real credentials or put them in images, public examples or diagnostic output.

A production secret manager may be appropriate, but secure platform injection can also fit. An ignored local `.env` file is not automatically protected against local access, backup or telemetry. Avoid fixed rotation intervals without an applicable organizational policy or an operable rotation mechanism. Prioritize least privilege, short-lived access when available, and quick revocation after exposure.

## Verification and Scope

Prefer evidence that a low-trust actor cannot obtain a production credential, the deployment runs the intended reviewed artifact, and exposed credentials can be revoked safely. Report which claims are proved and which depend on uninspected hosting configuration.

Do not rotate secrets, change CI permissions, publish artifacts or modify production infrastructure without authorization.

**References:** [OpenSSF Scorecard](https://openssf.org/projects/scorecard/), [SLSA](https://slsa.dev/), [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final).

## Worked Case: A CI Job with External Contributions

A repository accepts untrusted pull requests and deploys using GitHub Actions. A new workflow checks out submitted code, installs dependencies, runs tests and may access cloud credentials.

Trace the workflow with a small trust map:

| Step | Who controls its inputs? | Privilege to investigate |
| --- | --- | --- |
| Checkout and package installation | Pull-request author, commit metadata, package scripts, lockfile | Shell execution and workspace filesystem |
| CI token and repository APIs | Runner permissions, workflow event type and settings | Contents writes, actions or package publishing |
| Cloud authentication | Workload identity claims or static credentials | Target account/project, role scope and duration |
| Artifact creation | Build steps and dependencies | Which revision produces bytes and who can replace them |
| Deployment | Job/environment rules and operator approval | Whether the reviewed artifact is the deployed artifact |

A workflow with a valid OIDC token can still be too powerful if its cloud trust policy accepts untrusted contexts. A build with pinned actions can still execute malicious scripts from third-party packages. The aim is not to ban builds but to prevent untrusted work from inheriting production authority.

**Proportionate correction:** separate low-trust test execution from privileged publishing/deployment; minimize token and cloud role scope; bind protected environments to intended branches or approvals where available; verify artifact identity where the threat warrants it.

**Test/evidence:** a pull-request run should not obtain a production token or deploy artifact. A main-branch, approved release should still publish the intended revision. A permission field in YAML is evidence of intended configuration; provider-side policies and event semantics may still need inspection.

## Dependency Changes: Reachability Before Severity

A newly disclosed library issue can require immediate action if the deployed application invokes the affected function with attacker-controlled input. Another advisory for the same package may be irrelevant to this program's configuration.

Record package version and dependency graph, vulnerability range, affected capability, source of input, exposed call path, fixed version and patch compatibility. If reachability cannot be established with available evidence, label it unknown—not automatically safe or definitively exploitable.

A lockfile can reduce surprise updates, but does not guarantee trusted package authors. Package provenance, maintainer compromise, install scripts and release process matter when the threat model calls for them.

## Secret Exposure and Revocation Procedure

For a discovered credential in a repository or log:
1. Determine exposure scope without reproducing or printing the secret.
2. Identify its actual authority and affected systems.
3. Contain or revoke using an authorized operational path; do not blindly rotate production keys in a plan-only or review-only task.
4. Confirm replacement, dependent service behavior and revocation propagation.
5. Address recurrence at the **source** (logging, CI injection, configuration or access policy) rather than only deleting the visible occurrence.

Deleting a commit does not guarantee the credential is unrecoverable from clones, artifacts or caches. Document the operational implications without encouraging destructive history rewrites.

## Provenance Limits

SLSA provenance and signing are useful when an actual consumer verifies identity, build parameters and the artifact being deployed. A generated statement without enforcement or a protected key may be only inventory metadata. Evaluate the assurance chain end to end; do not install signing infrastructure solely to make a scan green.
