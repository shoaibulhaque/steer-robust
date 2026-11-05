# Design and architectural warning signs

Read when changing responsibilities, state, interfaces or control flow.

## Find the owner

- Trace callers, data and tests; inspect history when ownership is unclear.
- Minimize layers to trace and mutable state to hold; measure reader load, not only line count.
- Give invariants and mutable resources a responsible owner; other components use its contract.
- Repair invalid shared input at its producer while preserving other consumers' contracts.
- A legitimate consumer boundary guard must not conceal an upstream invariant failure.
- Keep policy and representation together when they change together.

## Model the domain

- Name business rules, valid states and transitions before adding branches or fields.
- Use types/data structures expressing identity, ownership and allowed operations.
- Encode constraints in types when useful; enforce runtime and mutable constraints at the relevant transition.
- Deduplicate by the actual resource: object identity, path, content and logical identity are not interchangeable.
- Prefer authoritative data over a separately synchronized mirror.
- Retain a snapshot when historical meaning, editable drafts, isolation or recovery requires its own state.
- Derive mechanical lists or representations from one owner; validate agreement when independent forms are needed.

## Design from the caller

- Sketch usage: inputs, result, errors and coordination.
- Keep entrypoints focused on boundary adaptation; use the existing domain owner for decisions.
- Hide substantial policy or complexity behind a small interface; do not expose internal stages without a need.
- Hide transport, storage and framework details unless they are intentional contracts.
- Prefer complete operations over methods requiring callers to reconstruct invariants.
- Constrain internal imports using the project's module tools when accidental bypass is a real risk.
- Separate decisions from mechanics without unnecessary forwarding chains.

## Abstraction and alternatives

- Reuse an existing owner when its responsibility fits; do not create a competing way to do the same job.
- Put optional integrations at suitable edges; extend core contracts only for a demonstrated shared need.
- Extract shared behavior for demonstrated common responsibility or variation, not repeated text alone.
- One caller can justify adaptation, policy or isolation; a wrapper without such a role may be removable.
- Compare alternatives affecting real constraints, interface cost or maintenance.
- Record non-obvious tradeoffs; an essay is optional.
- For measured complexity, duplication or weak assertions, read [optional analyzers](analyzers.md).
- Migrate coordinated internal callers when removing an old path; preserve required external transitions.

## Warning signs to investigate

Trace actual costs or violated contracts before flagging defects.

| Signal | Question |
|---|---|
| Large interface with little hidden policy | Does learning this API save the caller from learning its implementation? |
| Representation details repeated across modules | Can one owner hide the decision and prevent coordinated changes? |
| Modules split only into load/validate/save stages | Does the split scatter the same knowledge and invariant? |
| Repeated pass-through methods | Does each boundary add policy, adaptation or isolation? |
| Several writers or synchronized copies | Who owns consistency, invalidation and recovery? |
| Two equivalent supported paths | Is the variation required, or is migration incomplete? |
| Publicly importable implementation details | Can a caller bypass the invariant or create accidental compatibility? |
| Hand-synchronized registries | Can one source derive them, or a check detect drift? |
| Growing flags, casts or unrelated conditionals | Is the underlying state model missing a real distinction? |

## Framework and UI state

- Follow the actual framework's lifecycle and supported version; do not universalize one framework's rules.
- Where rendering must be repeatable, keep externally visible effects in the appropriate lifecycle owner.
- Local mutation that cannot escape may be compatible with repeatable computation.
- Derive display data where possible; effects may legitimately synchronize external systems.
- Editable drafts need their own update and reset semantics; they are not automatically redundant state.
