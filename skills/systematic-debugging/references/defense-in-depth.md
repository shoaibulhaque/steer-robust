# Defense-in-Depth Validation

**Read when:** the root cause is known and you are deciding which layers should validate or enforce
the violated rule.

## Contents

- Overview
- The Four Layers
- Applying the Pattern
- Example
- Limits

## Overview

After fixing a bug caused by invalid data, one check can feel sufficient. But a single check can be
bypassed by another code path, a later refactor, or a mock.

**Core principle:** give each layer the check it owns, so the bug becomes structurally hard to repeat.
Each defense must protect a distinct failure or bypass path; copying the same check into every layer
scatters ownership without adding protection.

## The Four Layers

### Layer 1: Entry-Point Validation

**Purpose:** reject invalid input at the boundary where it enters.

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
  // ... proceed
}
```

Carry the validated value inward while its guarantee still holds. Internal assertions do not replace
validation of untrusted input.

### Layer 2: Business-Logic Validation

**Purpose:** ensure the data makes sense for this operation. Shape-valid input can still violate an
authorization, balance, or lifecycle rule.

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
  // ... proceed
}
```

Enforce domain rules at their owner, including any transaction or isolation needed for shared state.

### Layer 3: Environment and Effect Guards

**Purpose:** refuse a dangerous effect in a context where it must never happen.

```typescript
async function gitInit(directory: string) {
  // In tests, refuse git init outside the temp directory.
  if (process.env.NODE_ENV === 'test') {
    const target = realpathSync(resolve(directory));
    const tmp = realpathSync(tmpdir());
    const rel = relative(tmp, target);
    if (rel === '' || rel.startsWith('..') || isAbsolute(rel)) {
      throw new Error(`Refusing git init outside temp dir during tests: ${directory}`);
    }
  }
  // ... proceed
}
```

Compare resolved paths, not string prefixes: `/tmpfoo` starts with `/tmp`. An environment variable's
value does not prove a safe execution environment; such a guard is a backstop, not containment. Recheck where trust, mutable
state, or time can invalidate an earlier guarantee, such as current object and tenant authorization.

### Layer 4: Diagnostic Instrumentation

**Purpose:** capture context for forensics when the other layers fail.

```typescript
async function gitInit(directory: string) {
  logger.debug('About to git init', { directory, cwd: process.cwd(), stack: new Error().stack });
  // ... proceed
}
```

Logging is not enforcement. Keep diagnostics proportional and free of secrets; sensitive context in logs
creates a second exposure.

## Applying the Pattern

1. **Trace the data flow:** where does the bad value originate, and where is it used?
2. **Map the checkpoints:** list every boundary the data passes, and every path that can bypass one.
3. **Assign each check to its owner:** entry, business rule, effect guard, diagnostics.
4. **Test each layer:** bypass layer 1 and verify layer 2 catches it; include denied cases.

Remove redundant task-created guards that add no guarantee.

## Example

**Bug:** an empty `projectDir` caused `git init` in the source tree.

**Data flow:** test setup produced `''` → `Project.create(name, '')` →
`WorkspaceManager.createWorkspace('')` → `git init` ran in `process.cwd()`.

**Layers added:**

- Layer 1: `Project.create()` validates that the directory is non-empty, exists, and is writable.
- Layer 2: `WorkspaceManager` validates that `projectDir` is non-empty.
- Layer 3: `WorktreeManager` refuses `git init` outside the temp directory in tests.
- Layer 4: a stack trace is logged before `git init`.

Each layer caught cases the others missed: other code paths bypassed entry validation, mocks bypassed the
business check, and platform differences needed the environment guard.

## Limits

No finite set of layers makes a bug impossible. Report which paths the tests exercised and what remains
outside the model, the supported environments, or the verification scope.
