# API, Parser and Outbound-Request Boundaries

**Read when:** an explicit API security review, hardening request, or threat model involves authorization, content-type handling, uploads, URL importers, XML, webhooks, SSRF, or other parser and egress boundaries.

## Follow the Actual Operation

Map the in-scope route, handler or consumer, its authentication context, object/tenant authority, parser, validation, and sensitive effects. Confirm supported framework versions, middleware ordering and deployment restrictions before assuming a route is reachable.

For an API operation, distinguish:
- **Identity:** who has authenticated?
- **Authorization:** can this principal perform this action on this specific object in this tenant and state?
- **Shape:** is this request syntactically valid and within resource limits?
- **Business invariant:** is the operation legal, in sequence, and consistent under concurrency?
- **Effect:** which persisted record, remote call, notification or resource access occurs?

An opaque identifier, schema validator, API gateway, or client-side filter alone is not an authorization guarantee. Permission checks may belong in a service, query, policy or other enforced boundary; do not mandate a particular controller line or SQL predicate.

## Check Parser Consistency

When a route supports more than one representation or parser, verify that *equivalent operations* enforce equivalent authorization, validation and resource limits. Do not assume that a changed Content-Type makes an otherwise unreachable parser active.

| Candidate issue | Evidence that matters | Insufficient shortcut |
| --- | --- | --- |
| JSON and form paths interpret a protected field differently | Reachable handler, accepted formats, parsed values and downstream authorization decision | Merely sending a different header |
| XML supports external entities | Actual parser configuration, reachable XML path, effective entity policy and safe controlled observation if needed | Presence of an XML dependency |
| Upload allows unintended effects | Real content sniffing, size/path limits, extraction and storage/serving behavior | Checking only the filename extension |
| Mass assignment | Client-controlled field reaches an unauthorized state-changing operation | Unexpected field accepted but ignored |

Use the relevant framework's current parsing and validation guarantees. Declared schemas can be permissive for compatibility; rejecting *all* unknown fields is not automatically safe or required.

## Review Server-Side URL Retrieval

For an actual URL-fetching capability, trace user control through URL parsing, redirects, DNS resolution, connection establishment, proxy and outbound credentials. Apply the application's permitted-destination policy to the *connected* endpoint and to subsequent redirects and retries. Account for internal, loopback, link-local and IPv6 destinations when they are not authorized.

DNS checks disconnected from the eventual socket are not enough. Conversely, allowlisting a known internal service may be a legitimate requirement; the control must reflect the application contract rather than a blanket ban.

**Safe verification:** prefer code/config analysis and isolated tests with owned endpoints and controlled DNS. Do not probe real cloud metadata endpoints or internal services merely to complete an audit. Confirming external entity resolution or a URL fetch does **not** by itself prove access to credentials, privileged roles or full infrastructure compromise. State additional prerequisites and effective controls.

## Report the Boundary, Not an Attack Narrative

For each supported finding, identify attacker control, reachable source, enforcement gap, sensitive effect, consequence and the exact verification limit. If a proposed chain depends on an unobserved step, mark that dependency as conditional. Do not force small observations into a high-severity chain or assign impact from a scanner label.

**Primary references:** [OWASP ASVS](https://asvs.owasp.org/), [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

## Worked Review: Endpoint Authorization Through the Real Data Path

An endpoint accepts a report identifier. Authentication runs in middleware, but the handler retrieves the report by identifier and then returns its bytes. The reviewer should trace the actual principal-to-object binding, not infer that middleware authentication implies authorization.

```python
# Illustrative domain boundary, NOT a framework-agnostic prescription.
def get_report(principal, report_id):
    report = reports.find_visible_to(principal, report_id)
    if report is None:
        raise NotFound()  # Or a contractually appropriate denial.
    return report
```

`find_visible_to` must itself enforce current object and tenant permissions; a function name does not establish that. Where resource ownership or permissions can change, check whether an earlier authorization decision can become stale before the effect. Multi-step writes may need an atomic policy+mutation operation, database row lock or another suitable concurrency control.

**Rejecting evidence:** user A's authorized request succeeds; user B's request for A's report fails through the real route, and the body/metadata and side effects remain inaccessible. Test a role downgrade or tenant reassignment only if that is a supported real-world transition.

**Counterexample:** the same record may be intentionally shared across organizations under explicit access grants. A strict `tenant_id == current_tenant` predicate could wrongly reject valid access; enforce actual policy rather than a simplistic ownership equality.

## Worked Review: Webhook Authenticity and Replay

For a payment/status webhook, distinguish:
- **Origin authentication:** signed payload or provider-specific verification based on the *raw representation* required by the provider.
- **Freshness and replay:** timestamp windows or stable event identifiers, as supported.
- **Idempotent business effect:** duplicates, reordering and retries must not create new payments, certificates or access grants.
- **Resource limits:** parsed body size, processing time and external calls.

A verified signature does **not** mean that the event refers to a legitimate order in the local domain, nor that a duplicate event should be processed twice. Test invalid signature rejection, a valid duplicate, a late/out-of-order event, and an event for a missing object through the actual intake path.

## Case Selection by Boundary

Choose an appropriate subset rather than checking every parser for every route:

| Real capability | Additional questions |
| --- | --- |
| File upload or archive extraction | Byte size and decompression amplification, object ownership, symlink/path containment, media serving policy, cleanup on partial failure |
| XML ingestion | Actual parser defaults, entity/DTD policy, supported features and safe handling of entity expansion |
| URL import or webhooks with outbound calls | DNS and redirect handling, connected destination, credential propagation, deadlines and response-size limits |
| GraphQL or flexible filtering | Object authorization beneath resolvers, query complexity, resource budgets and field exposure |
| Bulk operation | Per-object authorization, partial-success contract, bounded resource consumption and concurrency semantics |
| Query/form/body parsing | Which representations are actually supported and whether alternate parsing paths bypass protections |

A broad scanner pass can propose candidates, but the finding requires the real route, supported representation, reachable sensitive operation and effective controls. Do not exploit external parties or use uncontrolled callbacks to prove reachability.
