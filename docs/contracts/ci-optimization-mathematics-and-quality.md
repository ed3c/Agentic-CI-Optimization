# CI optimization mathematics and verification-quality contract

Normative v1. Applies to proposals to modify, retire, consolidate,
reschedule or replace any CI job or test in a repository adopting ACO.
It is NOT a new execution gate, test selector or second state ledger.

## Variables and objective

For a change/task d: O(d) is the independently required verification
obligations; S(d) is the ORIGINAL OWNER's selected controls; x configures
runner, cache, DAG scheduling, isolation, sharding and toolchain.

Minimize (P95(T_verified(d,S,x)), E(C_verified(d,S,x))) subject to:
- Every independent protected contract and original acceptance preserved;
- Fault and legal-neighbor discriminators and chosen negative controls pass;
- Actual HEAD/oracle/environment/provider evidence fresh and applicable;
- Runner/cache/workflow trust boundaries and security controls pass;
- Explicit project budget B respected, if one is defined.

ACO may model candidates for S but never replaces the owner's actual
Selection. No observed false green is NOT a zero-risk guarantee. A Pareto
optimum is workload-dependent, not a universal best CI configuration.

## Three time domains — never conflate

1. Provider CI Wall Time: explicit clock origin (e.g. created_at) through
   last required job completion. Includes orchestration delay, not Agent time.
2. Actual DAG Critical Path: only when exact dependencies and weights
   form a complete independently validated graph. Otherwise UNKNOWN.
   Overlapping job durations cannot be added to compute wall/billing.
   Pre-first-job delay cannot be labeled runner queue without evidence.
3. Verified Delivery: task start through all independently required original
   acceptance receipts, exact session/HEAD/consumer. A PR green status
   cannot supply that measure. Merge and deployment are separate effects.

Cohorts must preserve workflow/event, verification mode, initial vs retry,
origin of base/HEAD, runtime/image, requested outcome and time period.
Unknown mode is NOT source-only. Report failures, cancellations and partial
readback, not just green timings. Runs on one HEAD are correlated.
Nearest-rank sample P95 is descriptive, not a confidence interval.
Claim causal improvement only from controlled paired/randomized experiments
with explicit uncertainty and sufficient comparable samples.

## Test value distinct from demand and cost

Retained can be on-demand; fast can be a bad Oracle. Audit the independent
requirement, actual planted fault, legal neighbor, original consumer,
unique protection or proved equivalent survivor, source/version and demand.
Candidate actions: Keep, Rewrite, Consolidate, Select On Demand,
Reschedule or Delete. Historical keep/rewrite/merge/remove is evidence,
not license to delete on a different HEAD. Slow runtime, coverage,
Mutation Score, test LOC or budget alone never authorizes deletion.
ACO reviews are recommendations, not accepted test retirement.

## Cost and Pareto

Distinguish inclusive per-method, per-module, per-job, run wall, runner
billing and Agent cost. They overlap and cannot be summed.
Cost per Verified Task requires an accepted original-task denominator.
Without that evidence, CI-only costs must remain separately labeled.

Observed Frontier requires the SAME cohort and verified outcome, >=30
real latency observations per candidate (exploratory minimum, not a proof
of statistical power), comparable measured cost, all source/negative/
security requirements, and original-owner acceptance. Estimated/
partial/synthetic candidates must be separate. The CLI returns a
descriptive non-dominated set, not significance, causality or SLO.

## Authority and escalation

Source check != Test PASS. Catalog != execution. Model PASS != runtime
conformance. CI Green != Provider effect or Parent Goal. Oracles derive
from independent requirements, not candidate output.

For Soodles, the original Test Manager owns canonical Selection and
exact-head acceptance. For other repositories, THEIR own original
test owner does. Original Provider owns run, attempt and effects.
Outer and Poteto are optional execution adapters, not prerequisites.
When original scope is unknown, preserve needs_scope/refusal; do not
fallback to full suite or skip. Unknown writes require Owner readback.
No test deletion, CI job dispatch, merge, deployment or state mutation
is authorized by this read-only analyzer.

## Independent falsifiers

- Hidden affected dependency wrongly skips a required test.
- Removed control loses its fault or legal-neighbor distinction.
- Oracle is rewritten from current implementation just to turn green.
- Stale cache/HEAD/attempt is promoted to fresh evidence.
- Overlapping job durations are summed as CI wall or billed minutes.
- Native/source-only/unknown modes are mixed.
- Bypassed hooks remove remote required checks.
- Timeout, missing provenance, partial provider or absent Native
  carrier becomes PASS.
- Public artifact leaks raw private CI evidence.

Use only the original Owner's necessary selected tests, not mandatory
full suites on each routine iteration. Synthetic fixtures test
parsing/negative controls, not verified speedup.
