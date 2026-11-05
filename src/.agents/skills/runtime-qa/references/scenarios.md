# Select a useful scenario

Read the row that matches the changed contract. These are proof choices, not a mandatory cross-product matrix.
Use repository wrappers, fixtures and suites before writing a separate harness. Keep required CI coverage.

| Surface | Real boundary and observable result | Relevant counter-case |
|---|---|---|
| Web UI | Render the actual component/page with representative data; drive the changed interaction. Inspect focus, DOM, computed geometry and screenshots where relevant. | Neighboring viewport, keyboard route or an intentionally different layout; verify text/content remains usable. |
| API/framework | Use the application's router, middleware, validation and owning service; assert response and resulting state through the supported read path. | Invalid input or another object/tenant with the same authenticated user; failure leaves state unchanged. |
| CLI/library | Run the supported built/installed executable or public API with actual input; inspect exit, stdout/stderr, output bytes and relevant effects. | Valid input alongside invalid input, argument order or important compatibility behavior. |
| Compiler/generator | Capture a local fixture, emit with production code, build and render the output. Compare a frozen-input regeneration separately. | A nearby authored constraint must survive; deterministic wrong output is still wrong. |
| Plugin/lifecycle | Drive the actual coordinator and owner, including callback capture and retirement/replacement. | First prove a valid call works. Retain the callback, retire its owner while another participant stays live, then prove rejection and unchanged downstream counters. |
| Worker/persistence | Submit through the owning API/queue; observe acknowledged completion and committed/read-back state. | Failure between commit and acknowledgment, retry, cancellation or restart at the relevant transition. |
| Performance | Compare the same workload, outputs, environment and relevant resource costs before/after. | Representative larger input or cold/warm case when it can invalidate the claimed gain. |

## Build a falsifiable fixture

Write a short acceptance statement before choosing assertions:

> With [input/state], [entry point] must produce [observable result]. After [failure/transition],
> [forbidden effect] must not occur. [Preserved case] must still behave as specified.

Use the production owner of that decision. A fake provider can deliver a deterministic response, but
replacing the coordinator that selects authority cannot prove coordinator correctness. Counters should
observe the real effect boundary, not a mock expectation that implements the desired answer.

A local fake service can prove request/response handling. It does not prove live authentication,
third-party delivery or protocol interoperability. State those limits and run an authorized live lane
only when the claim or project policy requires it. Never borrow a personal session as a fixture.

## Compare the right observations

- Await a transaction/job/message completion boundary with a bounded deadline, rather than an arbitrary sleep.
- For absence, drain the applicable work or await its terminal result before comparing effect counters.
  No event during a short idle window is insufficient proof that later work cannot run.
- Retain pre/post values for state, writes, outbound requests or resource count when that is the guarantee.
- For UI, inspect the actual saved image. Measure what failed: line boxes for wrapping, visible text for
  collapsed content, focus/keyboard state for interaction. A good total score can hide one broken element.
- For an alleged inherited failure, run the relevant base under equivalent conditions when practical.
  Unchanged dependencies alone do not prove every failure predates a patch.

## Handle the first failure

Check readiness, version, fixture identity and harness completion before changing product code.
A missing browser is setup failure; an inaccessible evidence link is a delivery gap; an untested live
integration is a proof limit. Preserve the original observation and repair the responsible owner.
Use a bounded retry for an explained transient fault. Repeated green hunting is not diagnosis.
