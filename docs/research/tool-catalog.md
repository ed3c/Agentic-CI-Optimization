# Candidate CI technology (not required by ACO)

| Domain | Tools | What must be compared |
| --- | --- | --- |
| Runner | GitHub-hosted, Blacksmith, Vercel CI | queue, startup, CPU/RSS, security and total cost |
| Typechecking | tsc, tsgo, bun check | diagnostics, reference projects, memory, emitted files |
| Lint | ESLint, Oxlint | rule/plugin parity, missing diagnostics, elapsed time |
| Tests | unittest, Vitest, native integration | oracle, isolation, order-dependent faults, actual setup |
| Task graph | Nx affected, Turborepo | dependencies and hidden input counterexamples |
| Cache | actions/cache, remote task cache | hit/miss, trusted writer, poisoning, restore/save |
| Agent | hooks and required server checks | local bypass, exact-head remote acceptance |

Vendor tools are conditional experiments, not hard-coded optimization rules.
