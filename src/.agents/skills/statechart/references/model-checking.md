# Bounded TLC checking

Read when running statechart. This small workflow is inspired by pstack's statechart capability;
its implementation is original and deliberately omits automatic installs, whole-graph projection and rendering services.
See the source repository's research notes for attribution and scope differences.

## Model and run

Use a scratch directory for spec/config and a fresh output directory per attempt.
Write `Init`, a disjunction of named actions in `Next`, and the actual safety rule as `INVARIANT`.
Bound constants/state space to the question. Record constraints, symmetry and omitted behaviors explicitly.
Constraints can exclude behavior; passing a bounded model is not a global correctness claim.
For deadlock checking retain TLC's default; legitimate terminal states may explicitly stutter.

With an existing Java runtime and locally supplied official `tla2tools.jar`:

```sh
python3 .agents/skills/statechart/scripts/check.py model.tla --config model.cfg   --jar /path/to/tla2tools.jar --java /path/to/java --out /tmp/model-attempt
```

The wrapper uses one worker and TLC's breadth-first default, a wall-clock limit and a bounded Java heap.
If BFS fails because the sandbox forbids TLC's RMI listener, retain that failed attempt and rerun with
`--search iterative` in a new output folder. This uses TLC's iterative deepening without relaxing the sandbox.
TLC 1.7.4 actually treats `-dfid` as a maximum despite its help text; the wrapper caps depth at 1024
and still requires explicit completed checking. A depth-bound exit of zero without completion is not a pass.
It records spec/config hashes, exact invocation, exit status, raw output and parsed state sequence in JSON.
Exit 0 requires TLC's explicit successful completion. Exit 1 includes a counterexample or tool failure;
exit 2 is invalid invocation. `report.json` distinguishes these outcomes.
`trace.mmd` exists only for a parsed counterexample. Do not reuse artifacts from an earlier output folder.
Unrecognized output fails closed. Timeout does not establish absence of a bug.
For shortest safety traces avoid simulation, fixed-depth truncation and alternate worker settings.
Iterative deepening explores successively increasing depths; report its search mode explicitly.
Liveness cycles have different semantics; the wrapper does not visualize them or claim minimality.

## Interpret and replay

TLC's counterexample is shortest by transition count for the checked safety model, not necessarily time.
Preserve state identity: label values faithfully and escape Mermaid metacharacters.
A simplified business-level diagram can be authored separately, but label omitted detail and never
merge a failing state with a passing one in a way that hides the failure.
Tie the path to an implementation test exercising the real owner and an allowed positive control.
A model can be wrong; a TLC pass plus failing implementation test remains a real unresolved issue.

## Dependency policy

Use project-supplied tools first. Java/TLC are not bundled, downloaded or installed by this wrapper.
Use an official release and verify its checksum before independently obtaining dependencies.
The ordinary package tests use controlled subprocess fixtures; optional live TLC tests require explicit paths.
No dependency is needed for reading the skill or applying normal code/testing principles.
