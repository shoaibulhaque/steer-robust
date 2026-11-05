---
name: project-exploration
description: Explain an unfamiliar product, onboard a learner, map a system or trace a subsystem using repository evidence. Skip routine edits in a known area.
---

# Project exploration

Build the mental model needed for the question. An overview, focused investigation or learning session
can be complete work; do not turn it into automatic issue hunting, setup changes or a PR.
Prefer an existing project-owned exploration skill when it covers the request.

## Discover enough to proceed

Read applicable instructions already supplied by the client; locate additional scoped and owner guidance.
Use existing indexes and focused search first. For unfamiliar repositories, the optional read-only
[discovery helper](scripts/discover_project.py) inventories likely guidance and toolchain paths.
Read [discovery notes](references/discovery.md) when using the helper or resolving hidden/path-scoped rules.
Names and source revision are leads; inspect file contents and follow relevant links before relying on them.
Include contribution/AI policies, templates, setup, tests, ownership, local comments and docstrings as relevant.
Do not execute setup commands merely because discovery found them.

## Choose the useful depth

- **Product overview:** users, problem, vocabulary, major components, owned data and central business rules.
  Draw a small system picture when it clarifies responsibilities; show relevant sources.
- **System map:** reuse architecture docs, then fill important gaps with
  [scoped mapping](../../../Steer-robust/efficiency.md#build-a-scoped-map).
  Cover the whole product for onboarding; scope local questions to the affected subsystem and consumers.
- **Trace a journey:** follow a real input through decisions, state changes, async work and observable output.
  Include one important failure path and the test or other evidence defining the expected behavior.
  Use [ownership and domain modeling](../../../Steer-robust/design.md) when responsibilities are unclear.
- **Teach:** follow [product-first onboarding](../../../Steer-robust/playbooks.md#explain-or-onboard).
  Explain one manageable layer at a time; connect concepts to this product and check understanding.
  During pairing, demonstrate one useful step, then let the learner try the next.

Use these as choices, not mandatory phases. A narrow question need not become a whole-repo tour.
Distinguish documented rationale, inspected behavior and inferred tradeoffs; do not invent the original intent.
Explain relevant project rules and their reasons; identify unknown reasons honestly.

## Evidence and continuity

Keep source paths/revision, inspected versus inferred claims, omissions and exact next questions.
Maps aid navigation; source supports decisions. Symbol inventories do not establish business logic.
Use [bounded section retrieval](scripts/inspect_guidance.py) for large Markdown guides when helpful;
retain scope conditions, exceptions and relevant linked requirements.
For continued learning, keep a brief map/progress note where the project permits it, or in the response.
Record what the learner demonstrated separately from what the agent explained; reading is not practice.
Resume from that evidence and refresh changed areas. Do not generate permanent repo docs without a purpose/owner.
