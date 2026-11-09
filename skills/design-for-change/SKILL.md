---
name: design-for-change
description: "Use when planning or implementing a feature or fix that spans consumers, introduces shared state, or tempts duplicated rules, caller-specific flags, or extra layers. Prevent hidden coordination and coupling in the requested change. Not for isolated edits, pure refactoring, reviews, or major architecture decisions."
---

# Design for Change

## Overview

Keep a new change from making the next change harder. This skill evaluates the *change being planned or made*, not the codebase's overall architectural quality.

**Core principle:** decisions with the same reason to change should have one clear owner. Decisions that evolve independently should not be coupled just because their implementations look similar.

## When to Use

Use when a feature or fix crosses consumers or modules, introduces shared decisions or state, or invites copied rules, variant flags, or forwarding layers. Keep analysis proportional: an obvious local change needs no ceremony.

Consequential domain, interface, persistence, and architecture choices belong to `repository-engineering`; behavior-preserving restructuring belongs to `refactoring`, and an explicit patch review belongs to `change-verification`. This skill does not replace testing or invoke other skills automatically.

## Plan or Implement

- **Plan-only:** inspect the relevant path and propose the owner, consumer changes, boundaries, test-first steps where behavior changes, and completion evidence. Label assumptions. Do not edit files, implement, or claim tests passed.
- **Implementation:** apply the workflow to the actual change and review the resulting diff. Keep preparations and behavior changes separately checkable.

Do not generate a separate architectural report for routine work. State only decisions that help the user act on the plan or understand the patch.

## Workflow

### 1. Locate the Change's Reason and Owner

1. Trace a concrete scenario through its entry point, rule owner, consumers, effects, and nearby tests. Inspect close analogues, not the entire repository.
2. State the decision in domain terms and identify which component is authoritative.
3. Identify affected contracts and guarantees. Distinguish one rule represented across layers from independent rules that merely look alike.
4. Prefer an existing appropriate extension point over a parallel implementation.

If ownership is ambiguous or a new public contract is needed, address that consequential design choice rather than improvising.

### 2. Apply the Three Tangle Tests

| Pattern | Evidence | Better direction |
| --- | --- | --- |
| **Hidden links** | Copies of one rule, implicit call order, module globals set elsewhere, manually synchronized state | Make one owner authoritative; expose necessary coordination through a clear contract |
| **Needless links** | Stable code knows caller-specific policy, consumers reach into internals, generic interfaces accumulate context flags | Keep volatile decisions at their owner; expose only what callers genuinely need |
| **Surplus** | Pass-through layers, speculative extension points, unused configuration, or state that can be derived | Avoid new concepts unless they hide real volatility or enforce an invariant |

Check *reasons to change*, not syntactic similarity. Independent tax jurisdictions or providers may need distinct rules even when their code looks identical. Multiple consumers of the same eligibility rule must not independently invent its meaning.

### 3. Probe Change Locality

Use the present requirement as evidence; do not invent hypothetical product roadmaps.

- **Same rule evolves:** where does a maintainer change it? Could they miss another copy or required manual step?
- **One consumer evolves independently:** does an unrelated owner or consumer need changes?
- **A rule crosses layers:** do schema, API, editor, and renderer each perform their own legitimate job, or independently redefine the same meaning?

A legitimate change may touch many files. Optimize independent decisions and implicit coordination, **not** file counts, line counts, or number of interfaces.

For complex recurring coupling, Git co-change history and dependency paths may add evidence. Co-change alone does not justify combining modules: formatting, batch migrations, and releases also correlate edits.

### 4. Question New Special Cases

A value-specific branch, caller flag, retry, sleep, swallowed exception, or disabled test warrants investigating *why it exists*—not automatically deleting it.

- Preserve genuine business distinctions, compatibility paths, and defensive behavior.
- Put guards and retries with the boundary owning the invariant or failure policy. Respect ambiguous remote outcomes and non-idempotent effects.
- Avoid general infrastructure for hypothetical consumers.
- When a legitimate case does not fit the model, reconsider its owner or contract instead of hiding the conflict behind more flags.

### 5. Finish at the Requested Boundary

**For a plan:** give a concise change map: authoritative rule, affected consumers/contracts, work sequence, relevant risks, and evidence that would reject an incorrect implementation. Do not claim execution.

**For implementation:** inspect the diff for duplicated decisions, hidden ordering/state, unnecessary caller knowledge, and surplus concepts. Fix tangles this change introduces; report relevant pre-existing issues without expanding scope. Follow the existing test-first and verification workflows.

## Examples

**Legitimate fan-out:** a new content field affects schema, editor, preview, and renderer. Four files can be correct; independently defined defaulting rules that conflict are not.

**Wrong abstraction:** two payment providers expose similarly named statuses but follow different failure and business contracts. A generic mapper with provider flags can couple unrelated policies.

**Useful boundary:** even one consumer may justify an interface around volatile external I/O or an invariant. Do not delete it simply to reduce wrapper count.

## Red Flags

- Extracting every repeated line but leaving duplicated decisions.
- Adding caller flags rather than finding the owner of a distinction.
- Merging unrelated concepts to force a one-file change.
- Deleting a required workaround merely because it looks special.
- Turning a requested feature into an unsolicited codebase redesign.

**Stop when:** ownership is clear, necessary coordination is explicit, independent rules stay independent, and the plan or implementation has proportional verification.
