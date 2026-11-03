# Research sources: historical claims vs technical authority

Method catalogue only. Team speedups are their claims, not reproducible
evidence for another repository. Avoid copying third-party source code,
entire protected articles or license text into Apache-2.0 project output.

**Integrating case, not counted among the 11 citations:**
[Owen Gretzinger / Boardy — How I made our CI 20x faster, Oct 2026](https://x.com/owengretzinger/article/2116291924219060319).
Reported 40m to 2m and greater monthly compute cost. No ACO benchmark yet.

## Eleven cited sources and the portable methods

1. [Arpit Bhayani — Amdahl](https://x.com/arpit_bhayani):
   writing speedup does not equal delivery speedup; add queueing/capacity.
2. [Vercel CI introduction, Oct 2026](https://vercel.com/blog/introducing-vercel-ci):
   affected tasks, remote cache and a dependency graph. Vendor 2-6x
   is not a portable speed claim.
3. [Matt Pocock — Black Hole of Success](https://x.com/mattpocockuk):
   enforceable quality guardrails vs prompt-only instructions.
4. [Jarred Sumner / Bun 1.4.4](https://bun.com/blog/bun-v1.4.4):
   typecheck tool parity, cold start, diagnostic and memory benchmark.
5. [Linear CI Bottleneck Reworked](https://linear.app/now/ci-bottleneck-reworked):
   setup, cache opposite case, critical-path work, selective isolation.
6. [Andreas Kling — Profiling](https://x.com/awesomekling):
   one large hotspot vs many cumulative small costs; inspect traces.
7. [Peter Steinberger / OpenClaw Test Audit](https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md):
   independent behavior value, faults, consolidation and mutation.
8. [Kun Chen — CI/CD verification split](https://x.com/kunchenguid):
   release gate may inherit checks only with deployment blocking;
   test skipped via affected graph needs counterexample.
9. [Rory Graman — local hook](https://x.com/rorygraman):
   local feedback is fast but remote required checks remain independent.
10. [Flo Crivello — CI cost and agent throughput](https://x.com/Altimor):
    cost of blocked work, real agent/runner capacity.
11. [David Ondrej — Actions spend](https://x.com/DavidOndrej1):
    compare actual provider cost, not just elapsed job times.

## Original technical references

- [GitHub Actions workflow runs](https://docs.github.com/en/rest/actions/workflow-runs)
- [GitHub Actions jobs](https://docs.github.com/en/rest/actions/workflow-jobs)
- [GitHub Actions cache](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Vitest performance / isolation](https://vitest.dev/guide/improving-performance.html)
- [Nx affected](https://nx.dev/docs/features/ci-features/affected)
- [Bun benchmarks](https://bun.com/blog/bun-v1.4.4)
- [Linear report](https://linear.app/now/ci-bottleneck-reworked)
- [Vercel CI](https://vercel.com/blog/introducing-vercel-ci)

URLs are evidence pointers. Their applicability, license, performance
and limitations must be checked at the source revision used by a target.
