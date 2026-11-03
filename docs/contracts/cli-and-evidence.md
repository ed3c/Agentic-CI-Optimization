# Versioned CLI and private evidence

CLI v1:
- aco collect --repo OWNER/REPO --max-runs N --output PRIVATE:
  GitHub Actions GET-only existing PR runs, latest listed attempts and
  jobs. Read token from GITHUB_TOKEN or GH_TOKEN, N in 1..150.
- aco analyze --input PRIVATE --output PRIVATE:
  descriptive P50/P95 grouped by cohort; critical path stays UNKNOWN
  until a complete independent graph is supplied.
- aco review-controls --input REVIEW_DOC --output PRIVATE:
  missing provenance, protected value and consolidation proposals only.
  All may_delete flags stay false.
- aco frontier --input EXPERIMENT_DOC --output PRIVATE:
  non-dominated observed candidates where all owner/quality constraints
  are true and >=30 real observations are supplied.

Input/output use named aco.*.v1 JSON schemas in implementation.
Input error, missing capability, unsafe output directory or existing
target returns exit code 3 and a redacted error, never source secrets.
Successful analysis exits 0 but does NOT certify test/CI/product PASS.
Output is 0600, outside git, refuses overwrites. stdout has metadata only.

Collector does NOT fetch all historical retry attempts; cannot infer
native/source-only mode, a complete DAG, provider billing or verified
delivery from a GitHub runs listing. It performs no POST/PUT, dispatch,
test modification, merging or deployment. Private Soodles receipts
remain in the authorized private environment, not this public repo.
