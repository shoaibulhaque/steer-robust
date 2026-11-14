# Mobile and Desktop Responsiveness, Memory and Energy

**Read when:** Android, iOS, macOS, Windows, Linux desktop or another interactive native runtime
exhibits slow startup, UI hangs, scrolling hitches, high memory, thermal throttling or battery drain.

## Separate the Experience Dimensions

- **Startup:** cold, warm and hot launches may have different causes. Record when controls are
  usable, not only when a splash screen disappears.
- **Response:** user input may wait behind expensive synchronous work even if all data eventually
  arrives. An event loop, UI dispatcher or main run loop must remain available.
- **Continuous frames:** dropped/hitching frames can occur with no long "hang" when layout,
  rendering, image decode or GPU work exceeds the available refresh interval.
- **Memory/energy:** caches, images, retained views, excessive polling or background loops can
  degrade later interaction and device battery/thermals even if startup looks good.
- **Reliability:** resource exhaustion may cause termination, app-not-responding events, or an
  abrupt loss of user state; performance fixes must preserve restoration and data integrity.

Measure actual devices and release-like builds. Debug instrumentation and emulators can distort
results; record their limits rather than claiming production device equivalence.

## Profile the Platform That Runs the Work

| Platform | Tools and diagnostic signals |
| --- | --- |
| Android | Android Studio profiler, Perfetto traces, JankStats, Macrobenchmark for startup/scroll, ANR traces, Android vitals when available |
| Apple native | Instruments Time Profiler, Hangs, Hitches, Allocations and Energy; representative devices and release configuration |
| Windows | Windows Performance Recorder/Analyzer, application UI dispatcher and CPU/GPU/IO event traces where relevant |
| Linux desktop | `perf`/sampling profiler, compositor and process metrics, application event-loop traces; actual graphics stack |
| Cross-platform | Framework-specific rendering profiler **plus** underlying OS/device signals to separate UI work from I/O, memory and GPU bottlenecks |

Use the official tool for the actual supported runtime version. Framework render counters alone do
not identify a kernel I/O wait or thermal issue.

## Avoid Blocking the Interactive Path

For a slow list screen, first inspect whether it loads and creates hundreds of expensive rows,
decodes images, allocates models and performs synchronous DB/network work before the first useful
frame. Lazy/virtualized containers can avoid initial work, but still cause hitches when items
become visible. Prewarm or prefetch **only when evidence shows it improves the interaction**
and memory limits permit it.

Choose background work for *independent* expensive operations, with a safe result handoff to the
UI thread. Moving work does not eliminate CPU, memory bandwidth, contention or battery cost.
Bound work and cancel obsolete UI requests without cancelling durable user transactions.

Minimize repeated state emissions/recomposition, uncontrolled timer loops, unnecessary bitmap
copies and retained subscriptions. Track view lifecycles, task cancellation, window/screen
navigation and process death. Ensure resource cleanup is correct after exceptions and pauses.

## Worked Case: Faster Startup, Worse Scrolling

A list screen changes from eager rendering to lazy rows. The startup trace improves, but scrolling
now produces visible hitches when users encounter complex rows.

**Do not mark the optimization complete based only on startup.** Compare startup-to-interactive,
frame duration distributions while scrolling, peak memory and later reuse of visible items. Profile
row creation, image decode, I/O, style/layout and downstream compositing.

Potential choices include simplifying row work, caching bounded decoded assets with real lifecycle
policy, prefetching a small amount, or using platform-supported precomputation. Each trades memory,
energy and latency. The correct choice depends on measured device classes and usage patterns, not a
rule that "lazy is always faster."

## Resource and Battery Boundaries

- Avoid periodic wakeups and continuous polling when event-driven or platform-scheduled work
  meets the requirement. But critical work may justify wakeups with an explicit battery budget.
- Cache only with eviction/invalidation. A large memory cache can trigger OS reclamation and hurt
  frame pacing or launch/resume.
- Account for foreground/background restrictions, thermal limits and low-memory process restarts.
- Protect user progress: cancellation of a display task is different from cancelling an authorized
  write or upload already committed remotely.

## Verification Contract

Check affected screen transitions, frame pacing, memory over repeated navigation, correct
restoration after backgrounding, and relevant offline/network failure. Use one or two representative
low/mid devices where possible, not only the developer's workstation.

Preserve accessibility: adaptive text sizing, reduced motion, keyboard/assistive interaction and
touch responsiveness may expose different layout work than a fixed screenshot.

## Sources

- [Android: App Performance](https://developer.android.com/topic/performance/overview)
- [Android: Macrobenchmark](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview)
- [Android: Address Common Performance Issues](https://developer.android.com/topic/performance/issues)
- [Apple: Understand UI Responsiveness](https://developer.apple.com/documentation/xcode/understanding-user-interface-responsiveness)
- [Apple: Reducing Main Thread Work](https://developer.apple.com/tutorials/instruments/reducing-main-thread-work-by-doing-less)
- [Apple: Executing Work Asynchronously](https://developer.apple.com/tutorials/instruments/executing-work-asynchronously)
