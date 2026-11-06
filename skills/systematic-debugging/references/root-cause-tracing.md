# Root-Cause Tracing

**Read when:** an error appears far from its origin, a stack trace shows a long call chain, it is
unclear where invalid data came from, or a test passes alone but fails in the suite.

## Contents

- Overview
- The Tracing Process
- Example: Empty Project Directory
- Adding Stack Traces
- Finding Which Test Causes Pollution
- Completion

## Overview

Bugs often show up deep in the call stack: `git init` in the wrong directory, a file created in the
wrong place, a database opened with the wrong path. The instinct is to fix where the error appears, but
that treats a symptom.

**Core principle:** trace backward through the call chain to the original trigger, then fix at the source.

## The Tracing Process

1. **Observe the symptom.** Record the operation, input, state, and stack, separating fact from
   interpretation.
2. **Find the immediate cause.** What code directly performs the failing operation, with which arguments?
3. **Ask what called it.** Follow callers and transformations, including deferred work and callbacks.
4. **Keep tracing up.** Find where a valid value became invalid, or where the wrong assumption entered.
5. **Fix at the source.** Protect the violated invariant there, then verify the consumer path.

If you cannot trace one level further, you have found a dead end, not a root cause. Report what is
known and add the instrumentation below.

## Example: Empty Project Directory

**Symptom:** a `.git` directory appears in the package's source tree during tests.

```text
Error: git init failed in ~/project/packages/core
```

**Immediate cause:**

```typescript
await execFileAsync('git', ['init'], { cwd: projectDir });
```

**What called it:**

```text
WorktreeManager.createSessionWorktree(projectDir, sessionId)
  → called by Session.initializeWorkspace()
  → called by Session.create()
  → called by test at Project.create()
```

**What value was passed:** `projectDir = ''`. An empty `cwd` resolves to `process.cwd()`, which is the
source directory.

**Original trigger:**

```typescript
const context = setupCoreTest(); // returns { tempDir: '' } until beforeEach runs
Project.create('name', context.tempDir); // read before beforeEach
```

**Root cause:** a top-level variable read the fixture value before setup assigned it.
**Fix at the source:** make `tempDir` a getter that throws if read before `beforeEach`.
**Then:** add defenses only where they protect a distinct boundary; see the defense-in-depth reference
linked from the skill.

## Adding Stack Traces

When you cannot trace by reading, instrument the operation just before it runs:

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error('DEBUG git init:', { directory, cwd: process.cwd(), stack });
  await execFileAsync('git', ['init'], { cwd: directory });
}
```

```bash
npm test 2>&1 | grep 'DEBUG git init'
```

- **In tests, write to stderr** (`console.error`); the logger may be suppressed.
- **Log before the operation,** not after it fails.
- **Include the deciding context:** arguments, working directory, relevant state, timestamps. Never log
  secrets, tokens, the full environment, or whole request bodies.
- **Capture the stack:** `new Error().stack` (or the language's equivalent) shows the full call chain.
- **Analyze the traces:** look for the test file, the triggering line, and the repeating pattern.

Use the project's logger, debugger, or tracing where it reaches the boundary. Confirm instrumentation is
enabled, so a missing log line is not mistaken for a missing event. Remove temporary diagnostics when done.

## Finding Which Test Causes Pollution

When a side effect appears during the suite but you do not know which test causes it:

1. Start from a clean, disposable fixture and confirm the artifact is absent.
2. Run the suspect tests one at a time in the suite's normal order, checking for the artifact after each:

   ```bash
   for test in $(list-test-files); do
     run-one-test "$test" || echo "FAILED to run: $test"
     [ -e .git ] && { echo "Polluter: $test"; break; }
   done
   ```

3. Confirm the suspect by running it alone, then with its consumer.

Use the runner's native selection, ordering, seed, and shuffle options instead of a custom script where
they exist. Limits: some pollution needs several tests or a shared process, so a one-test-at-a-time scan
can miss it; bisect a reliably reproducing subset instead. Preserve exit codes, so a failed invocation is
not read as a clean run. Never delete a real repository or existing state to manufacture a clean baseline.

## Completion

The causal chain explains every observation, and the fix rejects the failure without removing
legitimate behavior. If a link in the chain was never observed, say so: reading source shows a possible
path, not proof of the path that ran.
