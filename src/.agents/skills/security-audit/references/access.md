# Identity, access and lifecycle

Read for authentication, authorization, tenant/object access or revocation questions.
Shared trust rules remain in the security guide; these are focused investigation questions.

Trace caller identity separately from requested object identity. A valid session does not prove tenant membership
or permission for every referenced object. Inspect list, detail, mutation, bulk, export and background owners
only when the requested scope or real consumers involve them.
For delegated actions, identify both the delegator's scope and the deputy's effective authority.
Do not flag intended owner-level operations solely because the caller can affect their own resources.

At asynchronous boundaries, distinguish admission from current authority at effect time.
Model a concrete capture, retirement/replacement and callback sequence when relevant;
use [statechart](../../statechart/SKILL.md) for ordering-sensitive ambiguity, then replay against code.
A cached token or matching identifier is not necessarily current authorization; a complete ownership protocol may be.

For tokens and HTTP identity, inspect actual signature/secret checks and required issuer, audience, origin,
expiry and principal/resource binding. Follow the installed framework rather than inventing custom auth rules.
A missing cookie flag, header or rate limit alone does not establish an attack.
Framing/cache findings need two actual components interpreting the same bytes/key differently.
If the decisive proxy/IdP/browser policy is outside source, retain needs_validation with that missing fact.
