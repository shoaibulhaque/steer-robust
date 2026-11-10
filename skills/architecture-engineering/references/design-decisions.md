# Design Decisions at Real Boundaries

**Read when:** choosing a consequential interface, abstraction, owner or domain boundary. Do not
produce an alternatives report when an established repository pattern already meets the requirement.

## Overview

**Core principle:** reduce the knowledge needed to use and change the system while preserving the
semantics its users depend on. A short implementation is not necessarily a simple interface.

## 1. Establish the Model and Owner

Use a concrete user scenario: who acts, on what entity, under which rules, and what must remain true?
Trace its current owner, callers, stored representation and external contract. Terms can mean different
things in separate business contexts; a shared name or schema does not establish shared semantics.

For example, an account's billing status and access status may currently share two boolean values,
but differ in authority, lifecycle and audit requirements. A generic status manager would merge distinct
knowledge. Conversely, one centrally owned retry eligibility policy can remove real divergence when
several callers are governed by the same rule.

## 2. Test Whether an Abstraction Pays

| Question | Evidence of a useful boundary | Warning sign |
| --- | --- | --- |
| What does it hide? | Volatile details or a meaningful invariant callers need not reconstruct | The same arguments and methods forwarded through another layer |
| What changes together? | One domain decision has a local owner | Context flags reconcile unrelated meanings |
| What must callers know? | A compact contract with clear effects, errors and ownership | Hidden initialization order, shared mutable context or implicit cleanup |
| What invalid states disappear? | Representation or API prevents a credible misuse | A new type merely renames a primitive without clarifying a contract |
| Why now? | Current behavior or justified variation needs it | A hypothetical future consumer supplies its only purpose |

A one-caller helper can isolate a difficult effect or explain an independent concept. Multiple callers
do not prove that a shared helper is correct. Judge the change in caller knowledge, change surface,
state to hold and dependencies to trace; do not substitute caller counts or line limits for that judgment.

## 3. Compare a Real Alternative

For a material decision, contrast the proposed boundary with a plausible simpler solution. Consider
public surface, coupling, domain ownership, failure behavior, reversibility, time/space growth and
operational burden. Name the uncertainty that would change the choice. Use a small experiment when it
can settle that uncertainty cheaply; do not build two complete systems as a design ritual.

When a named design pattern seems to fit, check its applicability and its consequences, including
the liabilities, against the actual variation. A pattern name does not justify its indirection.

Preserve a short rationale when future maintainers cannot infer the important constraint. A diagram
or architecture label does not enforce a boundary: inspect dependencies, API access and actual mutation.

## 4. Change Safely

Keep behavior-preserving structure changes distinct from new behavior. For legacy paths, characterize
the relevant observation and introduce only a necessary seam. A seam that makes a unit test pass
still needs proof that production wiring invokes the right implementation.

Do not generalize another project's architecture, deployment topology or language conventions into
this repository. Finish when the contract has an understandable owner and adequate feedback, not when
every possible abstraction or pattern has been considered.

## Worked Boundary Decision: One Eligibility Rule, Several Consumers

A product's eligibility is displayed in a web UI, enforced through an API and checked by a background job. A proposed implementation repeats the full decision in each component.

Investigate whether the UI is merely presenting an authoritative result or making an independent business decision. If **the same policy** governs all three consumers, make the policy discoverable and enforceable at its owning domain boundary; the client may display eligibility but must not become a substitute for server authorization.

However, the UI may legitimately have a presentation-only rule, such as disabling a button while the server remains authoritative. Do not merge two policies solely because both use the word "eligible."

**Change-locality probe:** if the eligibility rule changes, where must maintainers edit? If one consumer changes presentation, must the domain policy or unrelated clients be revised? Prefer a design that answers those questions without hidden synchronization.

## Counterexample: Useful Separate Adapters

Two external providers return similarly named statuses, but one status reflects final settlement and another reflects pending authorization. A common enum with provider flags can hide a significant difference in business effects.

Consider keeping provider-specific translation at the provider boundary, mapping into an internally meaningful domain result only when semantics are truly equivalent. Adding an interface is worthwhile when it hides differing failure or authentication behavior; it is surplus when every method blindly forwards arguments.

## Interface Contract Notes

For consequential boundaries, a short contract may be more valuable than an elaborate diagram. Specify:
- Supported inputs and who validates them.
- Returned states, including absent, rejected and ambiguous results.
- Observable side effects and which owner can perform them.
- Authorization identity and any tenant or role conditions.
- Compatibility and version expectations if independently deployed consumers exist.
- Whether repeated or concurrent calls are safe, and which party owns recovery.

These are prompts for relevant decisions, not a demand that every helper receive six sections of documentation. Preserve important rationale near the owning code or as a concise ADR when future engineers would otherwise rediscover the same tradeoff.
