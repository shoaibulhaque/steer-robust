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
