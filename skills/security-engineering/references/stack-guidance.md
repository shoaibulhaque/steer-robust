# Stack Guidance

**Read when:** choosing a stack-specific control for the requested security work. Establish the actual
framework/version, runtime, deployment and relevant surface first. Search repository security guidance
and existing middleware before selecting a new mechanism.

## Operating Modes

For secure coding, use the relevant existing protection. For review, verify its actual configuration
and bypass paths. For threat modeling, identify what the framework guarantees and what application
code must still enforce. None of these requires loading every stack's documentation.

## Definitions and Review Guidance

A default described in current documentation may differ from the version installed in the project.
Consult documentation for that supported version and inspect overrides. Absence of a control from the
repository does not prove its absence from the deployment; mark that assumption rather than inventing it.

## Secure Baseline and Focused Rules

| Stack or surface | Investigate only the affected controls | Primary starting point |
| --- | --- | --- |
| Django | Middleware, object/tenant authorization, CSRF, template escaping, deployment settings | [Django security](https://docs.djangoproject.com/en/stable/topics/security/) |
| Flask | Actual extension/configuration guarantees, escaping, sessions, CSRF and trusted proxy configuration | [Flask web security](https://flask.palletsprojects.com/en/stable/web-security/) |
| FastAPI | Authentication dependencies, per-object access, response schemas and frontend cookie/CSRF assumptions | [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/) |
| Express/Node | Middleware ordering, body limits, proxy trust, session/cookie behavior and dangerous sinks | [Express security](https://expressjs.com/en/advanced/best-practice-security.html) |
| Next.js | Server/client data exposure and authorization in every callable server boundary | [Next.js data security](https://nextjs.org/docs/app/guides/data-security) |
| React, Vue and browser JS, including legacy jQuery | HTML/URL sinks, direct DOM APIs, untrusted templates, browser credentials and real server-side enforcement | [React DOM](https://react.dev/reference/react-dom/components/common), [Vue security](https://vuejs.org/guide/best-practices/security.html), [browser security](https://developer.mozilla.org/en-US/docs/Web/Security) |
| Go HTTP services | Server/client timeouts, request limits, path and template handling, authorization and cancellation | [net/http](https://pkg.go.dev/net/http) |
| Other stacks/native code | Locate maintained official security/API guidance for the actual runtime; inspect parsing, privilege, memory/resource ownership and integration assumptions | Project's supported-version documentation |

## Practical Scanning Heuristics

Search for the actual entry points and sensitive operations: routes, consumers, file/archive handlers,
subprocesses, HTTP clients, rendering sinks and permission enforcement. A search match is a lead, not a
finding. Trace the data and controls before claiming exploitability. Prefer safe focused checks using
existing project tooling; no scanner or third-party analyzer is mandatory.

## Sources and Maintenance

This table replaces the supplied ten large stack manuals with conditional routes to authoritative
guidance. It does not claim equivalent exhaustive coverage or currency for an uninspected version.
Verify specific defaults and APIs when applying a rule; do not import a dated version pin into a new stack.
