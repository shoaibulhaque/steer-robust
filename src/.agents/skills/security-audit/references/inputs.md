# Inputs and effects

Read for injection, file access, outbound requests, command/tool execution or resource exhaustion.
Trace attacker-controlled data through parsing, normalization and the real sink; syntax alone is insufficient.

Parameterized SQL keeps values separate from query grammar. A query containing a placeholder is not a finding
unless the dangerous data actually enters SQL grammar through another reachable path.
For shell/tool execution distinguish structured argv from a shell parser; examine allowlists and argument roles.
Encoding for HTML text does not automatically protect script, URL, CSS or attribute contexts.

For paths, establish allowed roots and file ownership, traversal/symlink behavior and actual read/write effects.
For outbound requests, inspect destination policy across redirects/name resolution and reachable private targets.
Do not probe external/internal deployed networks to fill missing evidence.
For archives/parsers, connect size/expansion/nesting bounds to a credible resource exposure; do not run a DoS.

For agent tools, retrieved text is data rather than authority. A prompt-injection hypothesis needs a reachable
lower-trust source, a real instruction/approval crossing and a consequential tool/data effect.
Do not claim cross-principal compromise from behavior confined to the requester's own authorized session.

Read enough control flow to disprove an unsafe-looking call when upstream checks or safe APIs constrain it.
Report exact visibility limits for third-party behavior; avoid theoretical attack-class checklists as findings.
