# Findings and adversarial validation

Read before classifying security candidates. Scale the record to the task; no mandatory artifact system.

| Classification | Required evidence |
|---|---|
| `confirmed` | A reachable boundary violation established by a complete source argument or authorized bounded reproduction; explicitly name which evidence supports it |
| `needs_validation` | A specific source-grounded hypothesis with a decisive unresolved fact, exact blocker and safe validation plan |
| `rejected` | Concrete evidence refutes the path, control bypass or claimed impact; explain the failed premise |

Only confirmed records receive severity. Assess realistic prerequisites, affected principals and demonstrated
impact; do not infer code execution from parsing failure or broad compromise from a single bounded effect.
Unknown deployment, proxy, identity-provider or browser behavior is neither present nor absent by assumption.
Missing evidence is not a low-confidence confirmed bug. A refuted claim should not remain needs_validation.

## Sequential falsification

Reconstruct the strongest opposing case before accepting a finding:
- Can the claimed attacker actually choose this input and reach this entrypoint?
- Which principal owns the target resource? Is access intentionally delegated to that principal?
- Which upstream validation, typed query binding, framework escape, tenant filter or effect-time check applies?
- Does normalization happen before the relevant check? Can a later lookup change the resource or authority?
- Is the observed failure the alleged boundary violation, or an unrelated rejection/harness error?
- Does the reproduction exercise the real owner, with a positive control and a distinct denied principal/case?

Do not treat this same-agent pass as independent review. Deterministic reproduction can independently check
an objective property, but cannot supply missing deployment facts or exhaustive security assurance.

## Compact finding record

For each candidate retain:
- classification and stable root-cause identifier;
- affected principal/resource, violated boundary and reachable entrypoint-to-sink path;
- repository-relative source locations and reviewed revision/dirty state;
- observed/source-derived evidence, strongest falsification and remaining limits;
- severity only when confirmed, with conditions and bounded impact;
- narrow fix at the authoritative decision point, or a safe plan for a needs-validation blocker.

Use the requested report format. A focused response may be a short table; write files only when requested.
For a broad audit, include actual coverage, exclusions and incomplete work before findings.
Do not make JSON and prose disagree. Keep rejected candidates distinct from open risks.
Refresh conclusions invalidated by source, configuration or deployment changes.
Redact shareable diagnostics and do not publish secrets, private paths or exploit artifacts by default.
