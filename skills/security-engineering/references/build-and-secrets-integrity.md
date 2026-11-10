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
