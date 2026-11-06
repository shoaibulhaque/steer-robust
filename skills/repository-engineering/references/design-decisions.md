# Design Decisions at Real Boundaries

**Read when:** choosing a consequential interface, abstraction, owner, domain boundary, or design
pattern. Skip it when an established repository pattern already meets the requirement.

## Contents

- Overview
- Establish the model and owner
- Test whether an abstraction pays
- Keep policy, infrastructure, and deployment distinct
- Compare a real alternative
- Change safely

## Overview

**Core principle:** reduce the knowledge needed to use and change the system while preserving the
semantics its users depend on. A short implementation is not necessarily a simple interface.

## 1. Establish the Model and Owner

Start from a concrete scenario: who acts, on what entity, under which rules, and what must stay true?
Trace the current owner, callers, stored representation, and external contract.

**The same word can name different models.** Example: a cargo-booking team and a voyage-scheduling
team intend one unified system and casually share objects without agreeing what they share. Their
models diverge unnoticed until the system behaves unpredictably. Each model needs an explicit boundary,
its bounded context, kept consistent inside. Translation to an outside model, such as a legacy tracking
system, sits at the boundary. A shared name or schema does not establish shared meaning.

For substantial business rules, name the vocabulary, identity rules, and invariants, and choose
transaction and consistency boundaries around the rules that must hold together. Use a lighter design
for simple workflows where rich modeling adds little.

## 2. Test Whether an Abstraction Pays

| Question | Evidence of a useful boundary | Warning sign |
| --- | --- | --- |
| What does it hide? | Volatile details or an invariant callers need not reconstruct | The same arguments and methods forwarded through another layer |
| What changes together? | One design decision has one local owner | Context flags reconcile unrelated meanings |
| What must callers know? | A compact contract with clear effects, errors, and ownership | Hidden initialization order, shared mutable context, implicit cleanup |
| What invalid states disappear? | The representation or API prevents a credible misuse | A new type only renames a primitive |
| Why now? | Current behavior or justified variation needs it | A hypothetical future consumer is its only purpose |

Examples:

- **Deep:** Unix file I/O offers five calls, while the implementation behind them has changed radically
  over decades without changing that interface. A balanced-tree module offers insert, remove, and fetch,
  and hides rebalancing.
- **Shallow:** a one-line method that only stores a null for an attribute hides nothing; its interface
  is as complex as its body. Reading a serialized object from a file in Java needs three stacked stream
  objects, and forgetting the buffering one silently makes I/O slow. Make the common case simple.
- **Information leakage:** when one class reads a file format and another writes it, both depend on the
  format even if neither exposes it. Reorganize so that knowledge affects one module.
- **False abstraction:** a file system can hide block allocation, but not when data reaches durable
  storage. Databases depend on that, so flush rules belong in the interface.

A one-caller helper can still isolate a difficult effect or name an independent concept. Several callers
do not prove a shared helper is right. Judge caller knowledge, change surface, hidden state, and
dependencies to trace, not caller counts or line limits.

**Design patterns:** check a pattern's applicability and its consequences, including the liabilities,
against the actual variation before introducing it. Read a pattern's intent, applicability, and
consequences, not only its structure. A pattern name does not justify its indirection.

## 3. Keep Policy, Infrastructure, and Deployment Distinct

- **Policy vs infrastructure:** keep business decisions independent of volatile UI, storage, and vendor
  mechanics where that separation has value. This never licenses ignoring the storage's real transaction,
  encoding, query, or durability semantics.
- **Dependency direction:** check what imports what. Cycles and dependencies from stable policy onto
  volatile details make change expensive. A folder named `domain` or a diagram with inward arrows
  enforces nothing; check imports, visibility, and who can mutate what.
- **Module, process, service:** each gives different isolation and failure properties. Choose the
  smallest topology that meets the actual availability, scale, and team requirements. A network
  boundary adds partial failure, latency, and versioning to every call.

## 4. Compare a Real Alternative

For a material decision, contrast the proposal with a plausible simpler solution. Consider public
surface, coupling, domain ownership, failure behavior, reversibility, time and space growth, and
operational burden. Name the uncertainty that would change the choice. Use a small experiment when it
settles that uncertainty cheaply; do not build two complete systems as a ritual.

Record a short rationale when future maintainers cannot infer the important constraint.

## 5. Change Safely

Keep behavior-preserving structure changes distinct from new behavior. Example: users want an existing
plain-text statement printed in HTML. Copying the function would duplicate the charging rules, so first
restructure it to separate calculation from rendering, then add the HTML output. For legacy paths,
characterize the relevant behavior and introduce only a necessary seam. A seam that makes a unit test
pass still needs proof that production wiring invokes the right implementation.

Do not import another project's architecture, deployment topology, or language conventions. Finish when
the contract has an understandable owner and adequate feedback, not when every abstraction or pattern
has been considered.
