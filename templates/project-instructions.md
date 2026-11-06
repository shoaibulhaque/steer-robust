<!--
Project appendix template. Append everything below this comment to the end of the universal
AGENTS.md (or CLAUDE.md) in a repository, then fill it from repository evidence.

- Delete this comment, unused sections, and every <placeholder>.
- Do not repeat the universal defaults; add only what is specific to this repository.
- Write each rule as a checkable statement with its trigger, scope, and exception.
- Point to authoritative files instead of copying them, and say when to read each one.
- Put a rule that applies to one directory in that directory's own AGENTS.md instead.
-->

## Project-Specific Instructions

### Product and Architecture

- Purpose and domain vocabulary: <one or two sentences; key terms and their meaning>.
- Important invariants: <rules that must always hold, and where they are enforced>.
- Module ownership and extension points: <paths and what each owns>.
- External contracts and supported clients: <APIs, data formats, and their source of truth>.

### Commands

- Setup: `<command>`.
- Focused test for one file or test: `<command>`.
- Full required checks before completion: `<build, lint, type, and test commands>`.
- Expensive or external checks: `<command>`; run only when <condition>.

### Conventions

- Established patterns to follow: <pattern and an example path>.
- Dependency policy: <how to add or upgrade dependencies>.
- Generated files: <paths; regenerate with `<command>`; never edit by hand>.
- Compatibility obligations: <supported versions, platforms, and migration rules>.

### Further Guidance

- <path>: read when <task or area>.
- Nested instructions: <directories with their own AGENTS.md>.

### Delivery

- Branch, commit, and PR conventions: <format or template path>.
- Definition of done: <required evidence>.
- Release or deployment steps and who may run them: <process>.
