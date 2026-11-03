"""Bounded, non-authoritative timing and verification-cost projections."""
from collections import defaultdict
import datetime as dt
import math


def seconds(text):
    if text is None:
        return None
    if not isinstance(text, str):
        raise ValueError("invalid timestamp")
    try:
        value = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("invalid timestamp") from None
    if value.tzinfo is None:
        raise ValueError("timezone required")
    return value.timestamp()


def percentile(values, percent):
    if not values:
        return None
    ordered = sorted(values)
    return round(ordered[max(0, math.ceil(len(ordered) * percent / 100) - 1)], 3)


def critical_path(durations, dependencies):
    """Longest weighted DAG path. Only valid when caller supplies a complete DAG."""
    if not isinstance(durations, dict) or set(dependencies) != set(durations):
        raise ValueError("DAG must enumerate every job")
    visiting, memo = set(), {}
    def visit(key):
        if key in visiting:
            raise ValueError("dependency cycle")
        if key in memo:
            return memo[key]
        weight = durations[key]
        if type(weight) not in (int, float) or not math.isfinite(weight) or weight < 0:
            raise ValueError("invalid job duration")
        visiting.add(key)
        parents = dependencies[key]
        if not isinstance(parents, list):
            raise ValueError("invalid dependencies")
        for parent in parents:
            if parent not in durations:
                raise ValueError("unknown dependency")
        value = weight + max((visit(x) for x in parents), default=0)
        visiting.remove(key)
        memo[key] = value
        return value
    return round(max((visit(k) for k in durations), default=0), 3)


def analyze(data):
    if not isinstance(data, dict) or data.get("schema") != "aco.github-observations.v1":
        raise ValueError("unsupported observation schema")
    rows = data.get("observations")
    if not isinstance(rows, list):
        raise ValueError("missing observations")
    groups = defaultdict(lambda: {"wall": [], "pre_job": [], "job_span": [],
                                  "passed": 0, "failed": 0, "incomplete": 0})
    total_skipped = 0
    warnings = set()
    if data.get("complete") is not True:
        warnings.add("provider_history_partial")
    for entry in rows:
        if not isinstance(entry, dict):
            raise ValueError("invalid observation")
        run, jobs = entry.get("run"), entry.get("jobs")
        if not isinstance(run, dict) or not isinstance(jobs, list):
            raise ValueError("invalid run/jobs")
        # Distinguish mode and run attempt. Do not infer mode from workflow name.
        mode = entry.get("mode", "unknown")
        if mode not in ("source_only", "native", "unknown"):
            raise ValueError("invalid verification mode")
        attempt = run.get("run_attempt")
        if type(attempt) is not int or attempt < 1:
            raise ValueError("invalid run attempt")
        workflow = run.get("path")
        event = run.get("event")
        if not isinstance(workflow, str) or not workflow or not isinstance(event, str):
            raise ValueError("missing workflow/event")
        cohort = (workflow, event, mode, "initial" if attempt == 1 else "retry")
        bucket = groups[cohort]
        if run.get("status") != "completed" or entry.get("jobs_complete") is not True:
            bucket["incomplete"] += 1
            continue
        if not jobs:
            bucket["incomplete"] += 1
            continue
        try:
            created = seconds(run.get("created_at"))
            intervals = [(seconds(j.get("started_at")), seconds(j.get("completed_at")))
                         for j in jobs]
        except (ValueError, AttributeError):
            bucket["incomplete"] += 1
            warnings.add("malformed_or_missing_timestamps")
            continue
        if created is None or any(a is None or b is None or b < a for a, b in intervals):
            bucket["incomplete"] += 1
            warnings.add("malformed_or_missing_timestamps")
            continue
        earliest = min(a for a, _ in intervals)
        latest = max(b for _, b in intervals)
        if latest < earliest or earliest < created:
            bucket["incomplete"] += 1
            warnings.add("inconsistent_timestamps")
            continue
        bucket["wall"].append(latest - created)
        bucket["pre_job"].append(earliest - created)
        bucket["job_span"].append(latest - earliest)
        if run.get("conclusion") == "success":
            bucket["passed"] += 1
        else:
            bucket["failed"] += 1
        # This does NOT infer actual DAG critical path, queue time or provider billing.
    cohorts = []
    for key in sorted(groups):
        b = groups[key]
        cohorts.append({
            "workflow": key[0], "event": key[1], "mode": key[2],
            "attempt_kind": key[3], "observed_runs": len(b["wall"]),
            "successful_runs": b["passed"], "other_completed_runs": b["failed"],
            "incomplete_runs": b["incomplete"],
            "wall_p50_seconds": percentile(b["wall"], 50),
            "wall_p95_seconds": percentile(b["wall"], 95),
            "pre_first_job_p50_seconds": percentile(b["pre_job"], 50),
            "job_span_p50_seconds": percentile(b["job_span"], 50),
            "critical_path": "unknown_without_complete_dependency_graph",
            "verified_delivery_latency": "not_observed",
        })
    if not cohorts:
        warnings.add("no_usable_cohorts")
    return {
        "schema": "aco.analysis.v1", "status": "partial_observation",
        "cohorts": cohorts, "observations_seen": len(rows),
        "warnings": sorted(warnings),
        "limitations": [
            "Elapsed job times overlap; do not sum as billed time.",
            "Pre-first-job delay is not an isolated runner queue measurement.",
            "GitHub jobs API does not supply a full validated dependency DAG.",
            "PR CI completion is not independent product or delivery acceptance.",
            "Unknown mode is not equivalent to source-only or native.",
            "P95 is a descriptive sample statistic, not a confidence guarantee.",
        ],
        "authority": "read_only_no_test_selection_or_dispatch",
    }
