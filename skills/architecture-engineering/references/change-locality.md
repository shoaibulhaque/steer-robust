# Change Locality: Prevent Tangled Design

**Read when:** a planned or implemented multi-consumer change risks hidden coordination, unnecessary coupling, copied domain decisions, or surplus abstraction.

**Core test:** should these pieces change for the same reason? If yes, make the relationship and authority clear. If not, do not force them to move together.

## Three Architectural Tangles

| Type | Symptoms | Design response |
| --- | --- | --- |
| **Hidden links** | Copied rules or values, scattered feature-specific logic, a global or file secretly set elsewhere, undocumented call order, manually synchronized state | Make ownership discoverable; represent needed coordination through explicit contracts, state transitions, or one authority |
| **Needless links** | Consumers depend on internals, stable modules import volatile policy, a generic helper takes one caller's concepts, interface changes propagate without behavioral reason | Move volatile decisions to their owner; hide meaningful implementation detail; keep independent policies independent |
| **Surplus** | Pass-through wrappers, speculative extension points, unused configuration, dead code, redundant stored derivations | Do not add the concept without a real owner, requirement, or protective guarantee; remove task-created surplus, not unrelated legacy code |

These are **diagnostic categories**, not instructions to deduplicate or eliminate every wrapper. The same domain decision may be represented through a schema, API, editor, and renderer without being duplicated. Each layer can have a legitimate responsibility.

## Distinguish Knowledge from Repetition

A useful extraction centralizes **one decision**, not necessarily identical syntax. Two implementations may look alike but represent policies owned by different departments, vendors, or regulations; a shared helper with new flags for each variation would increase coupling.

Conversely, repeated authorization or eligibility rules are one piece of knowledge even when expressed with different syntax. Changing them separately creates hidden links and inconsistent behavior.

The cost of an interface is not its file count. Ask what a caller needs to know to use it correctly, what it hides, and which independent changes it forces the caller to absorb. A single caller can warrant an adapter when it isolates volatile I/O, enforces a contract, or creates a necessary test seam.

## Apply Two Change Probes

1. **Same rule changes:** can the maintainer find one authoritative decision and its consumers, or must they guess which copies, flags, and manual steps to update?
2. **One consumer changes independently:** does that force changes to stable, unrelated consumers or to a shared abstraction that knows too much?

Use a concrete change the system actually needs. Git co-change history can reveal hidden coordination, but correlation alone does not prove the modules belong together: formatting, release, or bulk migration commits also co-change.

When the change is consequential, trace a hypothetical next edit **within the known domain**:
- The eligibility policy changes: how many independently defined decisions must the maintainer locate?
- The mobile client changes presentation: must the billing rule or another consumer change without a behavior reason?
- A failed operation is retried: does the caller need to know an internal ordering or global state to avoid damage?

This is a design probe, not a forecast of requirements. If it does not identify a credible synchronization cost, stop instead of manufacturing a new abstraction.

## Special Cases Are Architectural Evidence

An `if` for one value, a caller-specific option, a swallowed exception, a hardcoded wait, a retry, or a disabled test may indicate an unrepresented requirement or an ownership mistake. Ask:

- Which real behavior, failure mode, or contract makes this exception necessary?
- Is the exception placed at the component that knows why it exists?
- Would changing the underlying policy require finding more exceptions elsewhere?

Preserve legitimate distinctions, compatibility requirements, and safeguards. A remote timeout does not mean the effect failed; removing retries or deduplication solely to make code appear simpler can break correctness.

A special case merits a brief explanation when its reason is otherwise invisible. Do not document every conditional; capture the non-obvious contractual constraint, preferably near the owning code or a focused test. An exception handler that silently swallows a failure may be a real defect; an exception handler that reconciles an ambiguous remote outcome may be essential.

## Examples

**Hidden link — duplicated policy:** a toolbar, shortcut handler, and command palette each implement their own enablement rule. Their UI components differ, but the *decision* belongs with the command contract. Keeping one authoritative rule prevents a later feature from updating only two of three interfaces.

**Needless link — caller vocabulary:** a generic payments helper accumulates `is_refund`, `provider`, and `special_checkout` flags that only one flow understands. Consider separate domain operations or a boundary owned by the policy, not another flag.

**Surplus — shallow wrapper:** `Service.fetch(x)` forwards the same argument and result to `Client.fetch(x)` without an invariant, semantics, or protected variability. The extra layer can increase reader load without hiding complexity. However, even a single caller can justify an adapter that isolates volatile external I/O.

**Legitimate fan-out:** introducing a CMS field requires a schema, editor, preview, and renderer change. The file count is not the problem; inconsistent fallback semantics would be.

## Scope and Stop

Do not convert this diagnostic reference into the upstream skill's whole-codebase "untangle in one pass" workflow. The goal here is to **prevent new tangles in the requested change** and identify a better boundary when the change demands one. For a dedicated restructuring request, use the behavior-preserving refactoring workflow.

During planning, identify likely coordination traps and ownership decisions; do not edit. During implementation, inspect the diff for tangles **introduced by this change**, remove unjustified additions, and preserve behavioral and compatibility requirements.

A typical change need not fit in one file. Stop when owners and necessary dependencies are explicit and no avoidable new coordination remains. Do not repeatedly refactor the whole repository until every special case disappears.
