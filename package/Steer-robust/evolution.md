# Compatibility and evolution

Read when changing public behavior, stored formats, dependency versions or deployments with mixed versions.

## Find the real contract

- Inspect callers, tests, documentation and downstream tools before declaring an interface internal.
- Contracts can include ordering, exceptions, hooks, timing guarantees, configuration and command output.
- Stored data, wire formats, plugin APIs and operational scripts can outlive the implementation that created them.
- Distinguish deliberate guarantees from incidental behavior, using the project's compatibility policy.
- When intent is unclear and the consequence material, gather evidence or ask instead of guessing it away.

## Coordinated internal changes

- Migrate owned callers and remove obsolete paths together when there is no required transition period.
- Preserve external or independently deployed consumers with a deliberate compatibility mechanism where needed.
- Give any bridge a concrete consumer, owner and removal condition; avoid indefinite speculative shims.
- Update affected tests and docs to the final contract rather than retaining two accidental ways to operate.

## Persistent data and rollout

- Check existing data, old readers/writers, queued work, replicas and restart/recovery behavior.
- Plan additive, transitional or coordinated changes according to actual deployment constraints.
- Separate irreversible data transformation from code rollback; identify what old code can still read safely.
- Bound migration batches and operational impact; support safe resume or detect partial progress.
- Reconcile duplicates and conflicts without overwriting valid state under the guise of normalization.
- Verify the migration with representative old data and important recovery or mixed-version cases.
- Make deployment order and rollback limits explicit when correctness depends on them.
- Shared CI/workflow changes may run against older PR branches before companion files arrive; gate transitions accordingly.

## Dependency and tool upgrades

- Honor the requested target, supported runtime and repository update policy; latest is not automatically correct.
- Check official migration guidance and changed APIs for the versions actually involved.
- Keep manifests and lockfiles consistent using the repository's package manager.
- Check dependency need, maintenance and relevant advisories with the project's available tools.
- Avoid unrelated major upgrades or a new package manager as a side effect of a narrow repair.
- Verify affected behavior and integration boundaries; compilation alone does not establish compatibility.

## Delivery evidence

- Connect checks to the exact code and artifact being delivered, including generated output when applicable.
- Recheck validation invalidated by a rebase, regeneration or material edit.
- Update required documentation, migration notes, templates and release metadata in the project's own format.
- Verify the authorized remote or installed result when the task includes publishing or installation.
- A pushed tag, built artifact or local test is not automatically proof that the requested release is available.
