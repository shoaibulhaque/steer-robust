# Opt-in behavioral evaluations

This suite runs real Codex CLI sessions in fresh local fixture repositories. It consumes account usage.
All evaluation checks are opt-in and outside ordinary CI, including the inexpensive grader controls.
Python 3.9+, Git, existing Linux bubblewrap, Codex CLI with JSON/debug prompt-input, and file auth are required.
No API key or auth token is committed. The default auth path is linked locally, never copied into a fixture.

## Run

From the source repository:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evals/run.py --out /tmp/steer-trial
python3 evals/regrade.py /tmp/steer-trial
```

The default ten-task suite includes `bug abstraction verification lever multi stateful robustness security testvalue honesty`.
`--arm enabled`/`disabled` runs an affected arm separately; `--model` pins an explicitly selected model
for both arms. Without it the CLI chooses its default; do not claim a named model from that alone.
`--timeout` bounds each worker. An existing output directory is rejected; retain separate failed attempts.
For live model checks, provide existing tools through `STEER_TLC_JAR` and `STEER_JAVA` before running.
No dependencies are downloaded or installed by the suite. Without them, model-checking proof stays blocked.

Each worker gets a fresh HOME/CODEX_HOME, identical task, workspace-write sandbox and no user config.
An outer read-only mount namespace hides this entire repository (including graders) and other temporary
runs/scripts; only the current trial and explicitly supplied optional toolchain are rebound.
A deterministic preflight checks that answer files are inaccessible and the fixture is visible.
Standard `/dev` and `/proc` mounts preserve nested Codex execution. Failure to enforce isolation blocks the run.
The same native system dev/skills may remain in both arms; only this bundle is absent from disabled fixtures.
No caching configuration is changed; arm order alternates. This is not a controlled cache benchmark.
Multi-repo fixtures have independent nested Git repositories and separate contracts.
The task forbids subagents, installs, networking and publication; only local fixture mutations are requested.
Raw traces and prompt snapshots can contain client context; keep them outside the repository.
Remove temporary auth symlinks after a run if retaining artifacts for review. Never archive them publicly.

## Four distinct evidence layers

1. **Advertised:** `codex debug prompt-input` lists the exact native skill path, resolving root aliases.
   This is a same-workspace preflight snapshot, not a claim about the model's private attention.
2. **Loaded:** completed successful reader commands returned the actual required source text.
   Agent prose, echoed filenames, failed readers and partial content do not count as full guide loading.
3. **Actions:** completed tool traces, changed files, independently executed migrations and regression tests.
   Read-adherence is reported separately; merely opening a guide is not semantic compliance.
4. **Correct:** outside-worker outcome checks exercise owned interfaces and preservation cases.
   Worker-written unittest tests must pass repaired code and fail independently restored broken code.
   Test discovery supports the fixture's standard-library contract; other harnesses need explicit adapters.

`traces.py`, `outcomes.py` and `regression.py` are independent of worker responses and normal package tests.
Qualitative design judgments use explicit review criteria and are labeled same-agent assessments,
not independent verification. No evaluator agents or additional model calls are required.

## Negative controls and fairness

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py'
```

Controls reject the broken/unfinished fixtures, vacuous passing tests, unconditional callback rejection,
blanket JSON replacement, unrelated policy changes, self-reported reads and failed/echoed reads.
The grader does not reject abstractions merely because they add a class or file. Qualitative design is reviewed
against domain ownership, reader load, actual variation and preserved guarantees, not a size threshold.
A known repair plus meaningful regression is accepted. Native aliased discovery has a positive control.
These are controlled faults in evaluation fixtures, not a new production mutation-testing framework.
Fixture-specific constraints must not be generalized to every real project or architecture.

## Results and cost

Per-trial `result.json` records correctness, discriminating tests, read evidence, changed files, elapsed time,
command counts, failures and usage events. `regrade.py` writes a separate `regraded.json`, preserving originals.
Use this after fixing a grader; rerun workers only when a src/task change invalidates their evidence.
Input/cached/output tokens are native reported counts; cost in money is unavailable and must not be invented.
Changed files/tool calls are effort proxies, not automatic penalties for necessary verification.
Report outcomes per arm and individual task, not only a combined score. Include failures and reruns.
One paired trial per task cannot establish statistical reliability, universal alignment or zero regression.
Claude adoption is structurally tested; these Codex trials do not establish live Claude behavior.

## Stateful proof and interrupted runs

Implementation correctness and completed model checking are separate fields.
`model_evidence.py` requires actual model-checker receipts for a counterexample and explicit successful
completion, plus retained specs/configs/Mermaid. A zero-exit depth-limited run without completion is rejected.
Receipts are tool evidence, not a semantic proof that a hand-authored model matches every implementation path.
An interrupted trial with no completed result must be retained as interrupted, never counted as a pass.
Updated cases/graders require regrading retained outputs; changes to relevant guidance require affected reruns.

The stateful fixture's local callback regression can prove its code contract without the runtime-QA skill.
Only engineering-change, verification and statechart are required there; forcing an extra runtime workflow
would contradict conditional activation. Grader corrections are recorded separately from worker runs.

## Qualitative engineering review rubric

Keep functional correctness separate from these same-agent assessments:
- Does each boundary own a real invariant, adaptation or integration responsibility?
- Does an abstraction reduce necessary reader knowledge or support real variation without scattering policy?
- Are error, security, state and operational guarantees preserved under the task's credible conditions?
- Does each test add a distinct failure signal at justified maintenance/runtime cost?
- Is configuration/tooling supported by the actual task rather than an imagined future use?

Record the concrete source/effect supporting a judgment. Mark ambiguous judgments unresolved;
never claim independent design verification or infer quality from line/test/class counts.
These fixtures are small and public; they cannot establish broad robustness or prevent prior model exposure.

The runner stops on native account-limit errors or a wholly unavailable command executor.
Those trials remain blocked/incomplete records, not model-quality failures or passes; resolve the blocker
before starting a fresh output directory. A mid-task quota interruption can leave a partially changed fixture.
