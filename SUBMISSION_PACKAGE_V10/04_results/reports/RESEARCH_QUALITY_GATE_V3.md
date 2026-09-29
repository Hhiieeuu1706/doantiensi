# Research Quality Gate v3

## Decision: **CONDITIONAL_LIMITATION**

Protocol: `battery-rul-protocol-v3.0`. Passed 38/42 automated checks. Open blockers: 0; open major findings: 4. Registered research limitations covering current major findings: True.

This gate evaluates whether the current evidence is ready to be frozen before the next modeling stage. `CONDITIONAL_LIMITATION` permits freezing the current work as a research baseline, but explicitly forbids claims of calibrated cross-domain deployment.

## Category scorecard

| Category | Passed | Total |
|---|---:|---:|
| data | 7 | 7 |
| hi | 7 | 7 |
| labels | 5 | 5 |
| leakage | 7 | 7 |
| online | 2 | 2 |
| protocol | 4 | 4 |
| reproducibility | 1 | 1 |
| uncertainty | 5 | 9 |

## Open blocker/major findings

- **MAJOR — gru_mean_coverage_85_to_95pct:** coverage=0.833
- **MAJOR — gru_minimum_checkpoint_coverage:** minimum checkpoint coverage=0.667
- **MAJOR — tcn_minimum_checkpoint_coverage:** minimum checkpoint coverage=0.667
- **MAJOR — external_interval_efficiency:** mean interval width / mean true RUL=1.059


## Required actions before next research stage

1. Keep protocol v3 and HI core v3 frozen; changes require a new protocol version.
2. Treat TCN/GRU intervals as developmental because checkpoint-aware normalized conformal v4 did not remove the 2/3 checkpoint outcome.
3. Do not tune uncertainty further on the same NASA/CALCE cases; add independent batteries or an untouched family.
4. Use a hierarchical/domain-adaptive trajectory model in the next experiment and pre-register interval-efficiency criteria.
5. Preserve the completed manual cycle sign-off and rerun it whenever raw parsing changes.
6. Close limitations only when their explicit sample-size, coverage and interval-width criteria are met.
