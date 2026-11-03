"""Bounded GitHub Actions GET-only collection, no retries or execution writes."""
import datetime as dt
import json
import os
import re
import urllib.error
import urllib.request


REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _get(url, token):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "agentic-ci-optimization-read-only",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError("GitHub read failed; observation remains unknown") from None


def _collect_pages(base, token, limit, *, collection):
    values = []
    total = None
    for page in range(1, (limit + 99) // 100 + 1):
        divider = "&" if "?" in base else "?"
        data = _get(base + divider + "per_page=100&page=" + str(page), token)
        if not isinstance(data, dict) or not isinstance(data.get(collection), list):
            raise ValueError("invalid provider collection")
        if type(data.get("total_count")) is not int:
            raise ValueError("missing provider total_count")
        total = data["total_count"]
        values.extend(data[collection][: max(0, limit - len(values))])
        if len(values) >= limit or len(data[collection]) < 100:
            break
    return values, (total is not None and total <= len(values))


def collect(repo, limit=50, token=None):
    if not REPO.fullmatch(repo) or ".." in repo:
        raise ValueError("expected owner/repo")
    if type(limit) is not int or not 1 <= limit <= 150:
        raise ValueError("max-runs must be 1..150")
    token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN or GH_TOKEN required for read-only collection")
    base = "https://api.github.com/repos/" + repo
    runs, complete = _collect_pages(
        base + "/actions/runs?event=pull_request", token, limit,
        collection="workflow_runs",
    )
    observed = []
    for run in runs:
        rid, attempt = run.get("id"), run.get("run_attempt")
        if type(rid) is not int or type(attempt) is not int or attempt < 1:
            raise ValueError("provider run identity invalid")
        jobs, full = _collect_pages(
            base + "/actions/runs/" + str(rid) + "/attempts/" +
            str(attempt) + "/jobs", token, 1000, collection="jobs",
        )
        complete &= full
        observed.append({
            "run": {key: run.get(key) for key in (
                "id", "run_attempt", "head_sha", "event", "path", "status",
                "conclusion", "created_at", "run_started_at", "updated_at")},
            "jobs": [{key: job.get(key) for key in (
                "id", "name", "status", "conclusion", "started_at",
                "completed_at", "steps")} for job in jobs],
            "jobs_complete": full,
            # GitHub API does not expose this job's original 'needs' DAG.
            "mode": "unknown",
        })
    return {
        "schema": "aco.github-observations.v1",
        "repository": repo,
        "collected_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "complete": complete,
        "limits": {"max_runs": limit, "max_jobs_per_attempt": 1000,
                   "retry_history": "only listed latest attempts",
                   "mode": "unverified", "job_dependencies": "unavailable"},
        "observations": observed,
    }
