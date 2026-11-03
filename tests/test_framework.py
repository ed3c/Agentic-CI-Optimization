import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from agentic_ci_optimization.analysis import analyze, critical_path, percentile
from agentic_ci_optimization.frontier import compare
from agentic_ci_optimization.github_reader import collect
from agentic_ci_optimization.private_io import write_private_json
from agentic_ci_optimization.quality import review_controls


def run_one(rid=1, duration=80, mode="source_only"):
    return {
        "run": {
            "id": rid, "run_attempt": 1, "head_sha": "a" * 40,
            "path": ".github/workflows/runtime.yml",
            "event": "pull_request", "status": "completed",
            "conclusion": "success",
            "created_at": "2026-11-03T10:00:00Z",
        },
        "jobs": [{
            "id": rid, "name": "verification", "status": "completed",
            "conclusion": "success",
            "started_at": "2026-11-03T10:00:10Z",
            "completed_at": "2026-11-03T10:01:20Z",
        }],
        "jobs_complete": True, "mode": mode,
    }


class AnalysisTests(unittest.TestCase):
    def test_no_false_critical_path_or_delivered_claim(self):
        d = {"schema": "aco.github-observations.v1", "complete": True,
             "observations": [run_one()]}
        result = analyze(d)
        self.assertEqual(result["cohorts"][0]["wall_p95_seconds"], 80)
        self.assertEqual(result["cohorts"][0]["pre_first_job_p50_seconds"], 10)
        self.assertIn("unknown", result["cohorts"][0]["critical_path"])
        self.assertEqual(result["cohorts"][0]["verified_delivery_latency"], "not_observed")

    def test_mismatched_modes_not_mixed(self):
        d = {"schema": "aco.github-observations.v1", "complete": True,
             "observations": [run_one(), run_one(2, mode="native"),
                              run_one(3, mode="unknown")]}
        self.assertEqual(len(analyze(d)["cohorts"]), 3)

    def test_missing_job_is_incomplete_not_zero(self):
        d = {"schema": "aco.github-observations.v1", "complete": False,
             "observations": [dict(run_one(), jobs_complete=False)]}
        result = analyze(d)
        self.assertIsNone(result["cohorts"][0]["wall_p95_seconds"])
        self.assertEqual(result["cohorts"][0]["incomplete_runs"], 1)
        self.assertIn("provider_history_partial", result["warnings"])

    def test_unknown_timestamp_is_not_pass(self):
        entry = run_one()
        entry["jobs"][0]["completed_at"] = None
        d = {"schema": "aco.github-observations.v1", "complete": True,
             "observations": [entry]}
        self.assertEqual(analyze(d)["cohorts"][0]["incomplete_runs"], 1)

    def test_dag_cycle_missing_edge_and_correct_path(self):
        self.assertEqual(critical_path({"a": 2, "b": 3}, {"a": [], "b": ["a"]}), 5)
        with self.assertRaises(ValueError):
            critical_path({"a": 2, "b": 3}, {"a": ["b"], "b": ["a"]})
        with self.assertRaises(ValueError):
            critical_path({"a": 2}, {"a": ["missing"]})

    def test_nearest_rank(self):
        self.assertEqual(percentile(list(range(1, 101)), 95), 95)


class QualityTests(unittest.TestCase):
    def test_never_auto_delete_even_with_replacement_proposal(self):
        out = review_controls({"schema": "aco.control-review.v1", "controls": [
            {"id": "a", "replacement_proposal": "b"},
            {"id": "b", "contract_ref": "R1", "oracle_ref": "R1",
             "fault_ref": "F", "legal_neighbor_ref": "L", "demand_ref": "D",
             "source_ref": "S", "high_cost": True}
        ]})
        self.assertTrue(all(not x["may_delete"] for x in out["controls"]))
        self.assertEqual(out["controls"][0]["recommendation"], "evidence_gap")
        self.assertIn("performance_refactor", out["controls"][1]["recommendation"])

    def test_invalid_duplicate_control(self):
        with self.assertRaises(ValueError):
            review_controls({"schema": "aco.control-review.v1",
                             "controls": [{"id": "x"}, {"id": "x"}]})

    def test_frontier_quality_freshness_observation_and_dominance(self):
        evidence = dict.fromkeys((
            "required_contracts_preserved", "negative_controls_passed",
            "source_fresh", "security_valid", "original_owner_acceptance",
            "observed", "same_verification_outcome"), True)
        docs = {"schema": "aco.experiments.v1", "candidates": [
            {"id": "good", "cohort": "PR source-only", "verified_latencies_seconds": [10] * 30,
             "cost_per_verified_task": 1, "evidence": evidence},
            {"id": "slow", "cohort": "PR source-only", "verified_latencies_seconds": [20] * 30,
             "cost_per_verified_task": 2, "evidence": evidence},
            {"id": "unverified", "cohort": "PR source-only", "verified_latencies_seconds": [1] * 30,
             "cost_per_verified_task": 0,
             "evidence": {**evidence, "negative_controls_passed": False}},
        ]}
        res = compare(docs)["candidates"]
        self.assertTrue(res[0]["pareto"])
        self.assertFalse(res[1]["pareto"])
        self.assertFalse(res[2]["eligible"])
        self.assertFalse(res[2]["pareto"])


class PrivacyAndConsumerTests(unittest.TestCase):
    def test_private_file_and_git_leak_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "evidence.json"
            write_private_json(target, {"data": "synthetic"})
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(ValueError):
                write_private_json(target, {})
            checkout = Path(directory) / "checkout"
            checkout.mkdir()
            (checkout / ".git").mkdir()
            with self.assertRaises(ValueError):
                write_private_json(checkout / "leak.json", {})

    def test_read_only_collector_uses_mocked_get(self):
        runs = {"total_count": 1, "workflow_runs": [
            {"id": 7, "run_attempt": 1, "head_sha": "h" * 40,
             "event": "pull_request", "path": "runtime.yml",
             "status": "completed", "conclusion": "success",
             "created_at": "2026-11-03T00:00:00Z"}]}
        jobs = {"total_count": 1, "jobs": [
            {"id": 8, "name": "test", "status": "completed",
             "started_at": "2026-11-03T00:00:01Z",
             "completed_at": "2026-11-03T00:00:02Z"}]}
        with patch("agentic_ci_optimization.github_reader._get",
                   side_effect=[runs, jobs]) as fake:
            out = collect("sample/repository", 1, token="synthetic")
        self.assertEqual(fake.call_count, 2)
        self.assertEqual(out["schema"], "aco.github-observations.v1")
        self.assertEqual(out["observations"][0]["mode"], "unknown")

    def test_external_directory_cli_real_process(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            source = Path(directory) / "input.json"
            source.write_text(json.dumps({"schema": "aco.github-observations.v1",
                                          "complete": True,
                                          "observations": [run_one()]}))
            proc = subprocess.run(
                [sys.executable, "-m", "agentic_ci_optimization.cli",
                 "analyze", "--input", str(source), "--output", str(output)],
                cwd=directory, capture_output=True, text=True,
                env={**os.environ, "PYTHONPATH": ""},
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(output.read_text())["cohorts"][0]["wall_p50_seconds"], 80)
            self.assertNotIn("aaaaaaaa", proc.stdout)


if __name__ == "__main__":
    unittest.main()
