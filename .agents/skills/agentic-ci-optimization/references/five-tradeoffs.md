# Five contested CI trade-offs

| Trade-off | Discriminating experiment | Never conclude from |
| --- | --- | --- |
| Cache vs reinstall | same lockfile/image, cold/warm, restore/save/miss, trusted writer and transfer | Another team's cache results |
| Keep vs merge/delete | independently protected behavior, original fault/legal neighbor, effective survivor, marginal cost | LOC, coverage or runtime alone |
| Full suite vs affected | graph input closure, planted missed-edge negatives, justified shadow/full comparison, original owner | Green skip job or incomplete graph |
| Bigger runners vs shards | fixed workload, queue, startup, CPU/RSS, per-job and full makespan, bill | Sum of parallel jobs |
| Local hook vs server CI | bypass hook; independently verify required exact-HEAD server acceptance | AGENTS.md or hook presence |

This table does NOT authorize the analyzer to alter Selection. Apply
[the normative contract](../../../docs/contracts/ci-optimization-mathematics-and-quality.md)
with the target's original owner and independent negative controls.
Vendor techniques are candidates, not portable default requirements.
