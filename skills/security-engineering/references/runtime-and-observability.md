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
