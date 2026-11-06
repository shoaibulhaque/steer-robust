# Defense-in-Depth Validation

**Read when:** the root cause is known and you are deciding which layers should validate or enforce
the violated rule.

## Overview

**Core principle:** each defense protects a distinct failure or bypass path. Repeating the same check
at every layer is not automatically safer and can scatter ownership.

## The Four Layers

### 1. Entry Point Validation

Validate untrusted syntax, ranges and shape at the owning input boundary. Carry validated values
inward while their guarantees remain stable. Internal assertions do not replace external validation.

### 2. Business Invariants

Enforce domain rules at their owner, including transaction/isolation requirements for shared state.
Shape-valid input can still violate authorization, balance or lifecycle constraints.

### 3. Environment and Effect Boundaries

Check meaningful independent constraints where effects occur: current object/tenant authorization,
resource containment, or an execution environment's actual permissions. Recheck when trust, mutable
state or time invalidates an earlier guarantee. Do not rely on string path prefixes for containment
or assume the name of an environment variable establishes a safe execution environment.

### 4. Diagnostic Evidence

Use safe observability to explain failures and verify coverage of bypass paths. Logging is not an
enforcement control. Keep diagnostics proportional; sensitive context can create a second exposure.

## Applying the Pattern

Trace the bad value, identify independent entry/bypass paths, and assign each invariant to an owner.
Add a second defense when it protects a real distinct boundary. Test the protected operation through
that path, including denied cases. Remove redundant task-created guards that add no guarantee.

No finite list makes a bug impossible. Report what the exercised paths establish and what remains
outside the model, supported environment or verification scope.
