"""Observed, source-bound cost/latency candidates; no implicit quality trade."""
from .analysis import percentile


REQUIRED = (
    "required_contracts_preserved",
    "negative_controls_passed",
    "source_fresh",
    "security_valid",
    "original_owner_acceptance",
)


def compare(doc):
    if not isinstance(doc, dict) or doc.get("schema") != "aco.experiments.v1":
        raise ValueError("unsupported experiment schema")
    rows = doc.get("candidates")
    if not isinstance(rows, list) or not rows:
        raise ValueError("missing candidates")
    processed = []
    ids = set()
    for c in rows:
        if not isinstance(c, dict) or not isinstance(c.get("id"), str) or not c["id"]:
            raise ValueError("invalid candidate")
        if c["id"] in ids:
            raise ValueError("duplicate candidate")
        ids.add(c["id"])
        samples = c.get("verified_latencies_seconds")
        evidence = c.get("evidence")
        cost = c.get("cost_per_verified_task")
        cohort = c.get("cohort")
        if not isinstance(cohort, str) or not cohort:
            raise ValueError("cohort required")
        if not isinstance(samples, list) or any(
            type(v) not in (int, float) or not 0 <= v < float("inf") for v in samples
        ):
            raise ValueError("invalid latency samples")
        if type(cost) not in (int, float) or not 0 <= cost < float("inf"):
            raise ValueError("invalid comparable cost")
        if not isinstance(evidence, dict):
            raise ValueError("independent evidence required")
        valid = all(evidence.get(k) is True for k in REQUIRED)
        valid &= (evidence.get("observed") is True and
                  len(samples) >= 30 and
                  evidence.get("same_verification_outcome") is True)
        processed.append({"id": c["id"], "cohort": cohort,
                          "p95_seconds": percentile(samples, 95) if samples else None,
                          "cost_per_verified_task": cost, "observations": len(samples),
                          "eligible": valid,
                          "missing_conditions": [k for k in REQUIRED
                                                 if evidence.get(k) is not True]})
    for c in processed:
        c["pareto"] = False
        if not c["eligible"]:
            continue
        comparable = [other for other in processed if
                      other["eligible"] and other["cohort"] == c["cohort"] and
                      other is not c]
        c["pareto"] = not any(
            (other["p95_seconds"] <= c["p95_seconds"] and
             other["cost_per_verified_task"] <= c["cost_per_verified_task"] and
             (other["p95_seconds"] < c["p95_seconds"] or
              other["cost_per_verified_task"] < c["cost_per_verified_task"]))
            for other in comparable
        )
    return {"schema": "aco.frontier.v1", "candidates": processed,
            "meaning": "descriptive_observed_non_dominated_only",
            "warning": "No causal speedup or statistical confidence claim without controlled paired comparison."}
