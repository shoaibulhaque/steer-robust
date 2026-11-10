# Runtime Boundaries and Security Observability

**Read when:** reviewing or hardening Linux services, containers, reverse proxies, network egress, infrastructure identity, security logs, detection or operational recovery.

## Inspect Deployment Reality

Identify deployed versions, exposure, service identity, authority, network paths, mounts, data stores, log destinations and the configuration actually used. Source templates alone do not prove runtime posture. Verify applicable operating-system and framework behavior before proposing settings.

### Isolation and Reachability

Evaluate least-privilege privileges, process/container isolation, write access, container runtime interfaces, network policy and credentials together.

- Default-deny network rules, non-root execution and read-only filesystems can strengthen an appropriate boundary. They are not always compatible with legitimate service requirements.
- Do not blindly disable host IP forwarding, block egress, rewrite Docker networking, or reload a reverse proxy on a live machine. Verify continued reachability and a recovery route before authorized changes.
- For reverse proxies, inspect trusted forwarders, TLS termination, session cookies, routing and relevant browser protections as deployed. Untrusted client-supplied forwarding headers must not be treated as identity evidence.
- Avoid pasting generic HSTS, CSP, sysctl or systemd templates into production without evaluating origin relationships, application behavior and rollback.

### Useful, Safe Telemetry

Select structured event fields for actual operational or security questions. Timestamps, event names and correlation IDs can be useful, but user IDs, IP addresses, request bodies, tokens and trace attributes carry privacy and retention concerns.

**Prefer collecting safe event schemas over logging sensitive bodies and trying to scrub them afterward.** Never deliberately log passwords, auth tokens, private keys, sensitive records, or other tenants' data for a diagnostic shortcut.

Audit trails for privilege changes or high-impact business effects may require durable, tamper-evident retention. An ordinary 401/403 response should not automatically generate a security alert; use application-appropriate baselines, context and thresholds.

### Detection That Leads to Action

Define which failure, abuse or policy drift matters, how it would be observed, and what a responsible operator would do. Dashboards and focused logs may be enough for a small team. A centralized SIEM, paid monitoring and external alerting are not default requirements.

A log proves only that an event was recorded; it is not itself a preventive authorization or integrity check. Verify that any important control is enforced at the owning boundary.

## Safe Verification

Choose non-disruptive checks and stage or validate configuration before any authorized deployment. Record remaining assumptions about actual network, identity or platform configuration. Do not claim a service is hardened because it conforms to a template or passes one scanner.

**References:** [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final).

## Worked Case: Small Public API on a Linux Server

For a server running a reverse proxy, API process, background worker and database, a **read-only** hardening review should first determine which components are actually exposed and where their authority comes from.

| Boundary | Investigation | High-value evidence |
| --- | --- | --- |
| Public ingress | DNS, external proxy, firewall/cloud ingress, exposed listen addresses | Public routes and effective origin policy |
| Administrative access | SSH/bastion/VPN, users, session handling, deployment identity | Who can log in, from where and with which capabilities |
| Application process | Service user, container privilege, writable mounts and secrets | Runtime uid, mounts, process command and effective grants |
| Database | Network exposure, service credentials, role grants, backup/restore | Accepted connections, grants, restoration evidence |
| Background jobs | Broker access, task identity, duplicate effects, worker leases | Ownership, retry and reconciliation behavior |
| Delivery chain | CI permissions, deploy token and artifact | Which actor can replace running code |

Do not assume a database in Docker is private merely because it has an internal-looking hostname. Verify published ports, host firewall and cloud ingress. Conversely, a process listening on all interfaces may still be protected by actual upstream network policy. Distinguish what is observed from what is inferred.

### Avoid a Self-Inflicted Outage

Hardening commands can disconnect the operator or silently break application traffic. A safe authorized plan stages one reversible change at a time, retains an administrative recovery path, validates health and logs, and distinguishes config validation from actually reachable service behavior.

Examples requiring deliberate analysis:
- HSTS affects browsers and subdomains; deploying it without validating certificate coverage can disrupt users.
- Strict CSP can break legitimate scripts; tailor it to the actual content model and test browser behavior.
- Non-root/read-only filesystem settings need explicit writable state and bind-port requirements.
- Default-deny firewall or egress policies must preserve DNS, updates, health checks and authorized external integrations.

The point is not to avoid hardening; it is to ensure the proposed control satisfies a specified guarantee without destroying the service it protects.

## Detection Design: From Failure to Operator Action

Start with an actual question, such as: "How will we know a privileged credential is being abused?" Then define the minimal event, threshold or anomaly, responder and recovery path.

| Event | Useful non-secret context | Operator action |
| --- | --- | --- |
| Privilege grant or role change | Actor identity reference, target role, time, request/trace ID | Verify authorization and revert unauthorized grant |
| Large sensitive export | Principal/tenant identifier under privacy policy, count/band, endpoint, outcome | Review legitimacy, revoke inappropriate token and assess access |
| Unusual admin authentication | Account, coarse source context, outcome and baseline | Check account integrity, enable containment if needed |
| Repeated failed background effect | Stable operation ID, state, failure category, retries | Recover or reconcile without duplicate effect |
| Unreviewed deployment | Artifact digest/commit, deploying actor, environment | Pause or revert deployment under change policy |

Not every error should page someone, and a log volume spike is not proof of an attack. Prefer actionable, bounded, privacy-conscious telemetry over copying full requests and responses. If the only response channel is an Admin dashboard, design useful dashboard states instead of adding an external messaging dependency by default.

## Recovery Is Part of Security

For systems that cannot tolerate significant data loss, a backup is not enough: define restore authority, isolation from compromised credentials and periodic proof that representative data can be restored. Security events may involve a malicious actor who has access to the application's normal deletion path; a backup under the same compromised privilege may be insufficient.

These considerations are risk-driven, not an unconditional requirement for every static or disposable development environment.
