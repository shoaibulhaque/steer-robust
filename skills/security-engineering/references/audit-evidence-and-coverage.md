# Audit Evidence, Coverage and Finding Verification

**Read when:** a deep security audit, formal evidence record, independently checked finding, or repeatable multi-area review is explicitly requested. Routine code changes and focused questions do not require an audit ledger.

## Scope and Coverage

Establish the in-scope revisions, deployed context, actors, trust boundaries, sensitive effects and known exclusions. For a broad review, optionally track small meaningful units of coverage (API operation, privileged job, parser, asset-access path, CI boundary, configuration area).

A ledger records what was reviewed and what evidence is missing, not proof that the whole system is safe. No fixed JSON schema, subagent count or report artifact is mandatory without an actual reporting requirement.

## Candidate → Counterevidence → Disposition

1. Trace who controls the input and which entry point actually receives it.
2. Follow transformations, authorization, parsing and configuration to the sensitive operation.
3. Seek counterevidence: effective upstream controls, unreachable paths, disabled parsers, version-specific defaults, deployment policy or an independent ownership check.
4. Choose the least risky evidence that resolves uncertainty: source analysis, isolated test, or authorized controlled reproduction. Another reviewer can reduce anchoring but is not required; two agreeing models do not prove a finding.
5. Record the supported scope, confidence, preconditions, observed result and remaining unknowns.

| Result | Meaning |
| --- | --- |
| **Confirmed** | The stated defect and feasible effect are established to the extent claimed through decisive code/config evidence or controlled observation |
| **Conditional** | A meaningful prerequisite such as deployed exposure, parser configuration or role authority remains unverified |
| **Hardening** | Additional defensive control recommended without a proven reachable exploit |
| **Rejected** | Evidence defeats the candidate in the assessed scope |
| **Not reviewed** | Outside the actual review |

Do not attach high severity to a chain of conditional observations or inflate "possible impact" into observed compromise. Some code/config violations can be established statically; not every finding requires an exploit. Runtime testing must be authorized, bounded and use owned or isolated resources. Avoid risky live probes or access to other tenants' data.

## Report Decisions, Not a Scanner Dump

For each material result, identify the affected location/revision, attacker capability, boundary, source-to-effect path, existing checks, decisive evidence, possible impact, mitigation at the owner, and the verification limit. Group duplicate manifestations of the same root cause where that genuinely improves remediation; keep distinct ownership and exploit paths visible.

Separate uncertainty from confirmation. Record limits on paths, deployment or versions not examined. If an output schema or machine-readable ledger is required by the user's actual workflow, implement it then—do not manufacture one for an ordinary review.

**References:** [OWASP ASVS](https://asvs.owasp.org/), [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final).
