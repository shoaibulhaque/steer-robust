# Brownfield Evolution

**Read when:** extending a running or legacy codebase, or deciding whether existing boundaries and practices should be preserved or changed.

## Establish What Actually Exists

Inspect the relevant code, callers, tests, configuration, and deployment or operational evidence available. Trace one real request or job across its entry point, authoritative data, effects, and consumers. Find the closest working feature before proposing a new framework or parallel path.

Distinguish:
- **Supported contract:** observable behavior or stored/API shape relied upon by a consumer.
- **Incidental implementation:** structure or historical workaround that may be changed safely.
- **Suspected defect:** behavior that conflicts with an independently established requirement.
- **Unknown:** a behavior or dependency not yet verified.

Do not label every current behavior as intentional. Equally, do not "fix" an apparent oddity without understanding the consumer that depends on it.

## Choose the Smallest Coherent Change

Locate the current owner of each rule and the extension point that already serves similar requirements. Map affected producers, consumers, data models, and tests; include other repositories where a contract crosses repository boundaries.

Check whether the proposed change introduces hidden coordination or spreads knowledge across components. When that risk is material, examine whether a rule is duplicated, a caller knows too much, or a new abstraction protects no real contract.

Treat pre-existing tangles as separate candidates for refactoring. Do not expand a requested feature into global cleanup. If preparatory restructuring is necessary, establish behavior evidence and separate it from the feature's behavior change.

## Plan Compatibility and Verification

Identify where current data, public APIs, stored schemas, deployed configurations, or user workflows constrain the change. Name behavior that must remain stable and behavior intentionally changing.

- Verify relevant existing behavior before a risky structural step; characterize untested legacy behavior first if required.
- Use test-first evidence for intended new behavior, including relevant rejection and failure cases.
- For consumers outside the change's atomic deployment boundary, plan compatibility and version ordering rather than assuming simultaneous cutover.

Avoid adding indirection only to imitate a supposedly clean architecture. A locally cohesive module with a stable contract may be easier to maintain than several forwarding layers.

## Example: Existing Django Service

A new consent rule touches an API serializer, business decision, persistence, and a client response. Multiple edits can be legitimate: each layer has a different role. One authoritative consent policy should decide eligibility; serializers and clients should not independently reinterpret the rule.

If existing clients depend on a previous response shape, the migration plan must account for them instead of silently redefining the API.
