# Optional code-quality tools

Read when an actual complexity, duplication or assertion-quality question needs measurement.
Use the project's configured tools first. No tool here is a prerequisite for ordinary work.

| Question | Existing option | Interpretation |
|---|---|---|
| Python branch complexity | Ruff C901 or Radon | Locate decisions; a score is a signal, not a forced split |
| Python nesting/reader effort | Complexipy cognitive complexity | Review nesting and context; metric definitions differ |
| JS/TS branching | ESLint complexity | Honor configured variant and threshold |
| Complexity plus coverage | Crapper | Confirm successful coverage collection; N/A or failed collection is not coverage proof |
| Similar structural code | Dryer | Candidate duplicates can encode different domain responsibilities |
| Assertion sensitivity | Existing Stryker, mutmut, PIT, cargo-mutants, or Mutator | Survivors need investigation; equivalent/uncovered/invalid mutants differ |
| Architectural dependencies | Existing boundary lint or UML viewer | Explain ownership and allowed direction; no new AST index or viewer service |

Check installed versions, supported languages, command behavior and scope before running.
Crapper/Mutator can install coverage tools and write metrics; their launchers can create environments.
Do not run them blindly or import those installation defaults. Prefer an explicit project-owned command.
Mutation runs need a passing baseline, bounded files/time/workers and isolated source copies.
Separate test failure, compile-invalid mutation, timeout, uncovered site and surviving meaningful mutation.
A broken runner that kills every mutant proves nothing. Reconcile interrupted edits and preserve originals.
Do not rerun full mutation suites for a trivial fix or turn arbitrary CRAP/duplication thresholds into policy.

A useful test detects a meaningful fault in the changed contract. Prefer one controlled negative case
before an expensive mutation campaign. Keep an existing justified boundary even with one caller.
Split code when it lowers reader load or separates real responsibilities, not merely to lower a number.
Dependencies point toward domain policy when the project's architecture calls for it; do not impose
one layered architecture on every framework. Data shape, vocabulary and invariants come before class diagrams.
