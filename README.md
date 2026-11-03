# Agentic CI Optimization (ACO)

Read-only, source-bound analysis for faster **verified** engineering. Primary
focus: Verification Selection Engineering and Agent Execution Engineering.
Performance Engineering is used when necessary work is the bottleneck.

ACO is NOT a test runner, test selector, CI dispatcher, approval gate or merge
tool. It never asserts an actual speedup without comparable observations.

## Independent install and use

Python 3.10+, no runtime dependencies:

    python3 -m pip install .
    aco --help

Raw provider reads and results MUST stay outside Git worktrees (e.g. a private
temporary directory). ACO refuses overwrites and writes output files mode 0600.

    export GITHUB_TOKEN=...  # GitHub Actions read permission only
    aco collect --repo OWNER/REPO --max-runs 50 --output /private/runs.json
    aco analyze --input /private/runs.json --output /private/summary.json
    aco review-controls --input controls.json --output /private/review.json
    aco frontier --input experiments.json --output /private/frontier.json

collect uses REST GET only, reading existing PR workflow runs and the latest
listed attempts, bounded to 150 runs. It cannot execute CI, change cache,
create PRs, modify tests or write to GitHub.

Current limitations: the GitHub job list does not establish an exact DAG
critical path, pure runner queue delay, native/source-only mode, billed cost,
or full verified delivery. No such claims are made from this data.

## Normative and supporting documents

- [Mathematics and quality](docs/contracts/ci-optimization-mathematics-and-quality.md)
- [Interface and private evidence](docs/contracts/cli-and-evidence.md)
- [Five trade-offs](.agents/skills/agentic-ci-optimization/references/five-tradeoffs.md)
- [Research source index](docs/research/source-index.md)
- [Tools](docs/research/tool-catalog.md)
- [Agent skill](.agents/skills/agentic-ci-optimization/SKILL.md)

Observed Frontier is descriptive: matching cohort and verified outcome, >=30
real latency observations, independent negative controls, source freshness,
security and original owner acceptance. Causal claims need separate experiments.

Soodles is an optional consumer, not a runtime dependency. Private Soodles
evidence must never enter this public repository.

License: [Apache-2.0](LICENSE). External research, code and product
documentation retain their separate authors, rights and licenses.
