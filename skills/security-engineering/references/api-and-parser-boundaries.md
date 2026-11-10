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
