# E1–E11 evidence completion audit

## Scope and freeze rule

V8 frozen NASA and HUST final results are unchanged. The 16-cell HUST final-untouched set is not used for tuning. New analyses use NASA development batteries or the 46-cell HUST development subset; the 15-cell calibration subset is used only for interval calibration.

| ID | Check | Evidence artifact | Status | Defensible conclusion |
|---|---|---|---|---|
| E1 | Protocol sensitivity | `baseline_fold_metrics.csv`, `hi_core_ablation_v3_*`, `research_quality_gate_v3.csv` | Partial | The locked battery-level protocol is audited; a paired leaky random-cycle versus locked experiment is still required before claiming that protocol choice quantitatively changes performance. |
| E2 | Model-ranking stability | `trajectory_v3_model_ranking.csv`, `feature_rank_stability.csv`, `HUST_MODEL_LADDER_LOBO_V2.csv` | Complete | Ranking is protocol-dependent; RF is best among evaluated non-sequence models under the locked protocol, not universally. |
| E3 | Fair model-family benchmark | `V10_FAIR_ENGINEERED_HI_RF_XGBOOST.csv`, `V10_FAIR_DEEP_ENGINEERED_HI.csv`, `V11_DEEP_PER_BATTERY_BOOTSTRAP.csv` | Conditional | RF/XGBoost/classical comparison is direct. Deep results remain a separate representation experiment until equal convergence/tuning records are accepted. |
| E4 | NASA + HUST-development state/history ablation | `V9_RUL_STATE_HISTORY_ABLATION*.csv`, `hi_core_ablation_v3_*`, `deep_hi_core_rul_ablation_*` | Complete with scope limit | State dominates cycle-only. History is checkpoint-dependent; NASA RUL sample is only three observed-EOL cells, so generality is not established. |
| E5 | Statistical uncertainty | `champion_uncertainty_500bootstrap*`, `ablation_statistical_tests.csv`, `statistical_reporting_v2_summary.csv` | Complete | Bootstrap intervals and per-cell distributions are reported; small NASA n remains a limitation. |
| E6 | EOL sensitivity | `eol_threshold_sensitivity.csv` | Complete | 70/75/80% thresholds alter censoring and EOL timing; 75% remains the registered primary threshold. |
| E7 | External HUST validation | `HUST_FINAL_UNTOUCHED_RESULTS_V1.csv`, `HUST_FINAL_STATISTICS_BOOTSTRAP_V1.csv` | Complete | Trend improves with observation horizon after development-only adaptation. |
| E8 | Uncertainty usefulness | `external_checkpoint_calibrated_summary.csv`, `HUST_FINAL_NORMALIZED_CONFORMAL_V2.csv` | Partial | Coverage is reported with width; intervals remain conservative/wide, so practical usefulness is not yet demonstrated. |
| E9 | Leakage audit | `research_integrity_tests.csv`, `research_quality_gate_v3.csv`, `HUST_FINAL_FREEZE_MANIFEST_V1.csv` | Complete | Battery-level split, final freeze and future-data restrictions are auditable. |
| E10 | Sequential replay | `V9_RF_SEQUENTIAL_REPLAY.csv`, `V10_RF_SEQUENTIAL_REPLAY_WITH_INTERVALS.csv` | Supporting | RF chronological replay is available; electrical HIL and physical BMS validation remain future work. |
| E11 | Protocol comparison matrix | `V9_PUBLISHED_BENCHMARK_HUST.csv`, `V10_FRAMEWORK_ABLATION_MATRIX.csv` | Complete | Published raw metrics are not ranked when split/target/horizon differ; methodological comparison is explicit. |

## Evidence boundary

The strongest supported claim is an auditable, leakage-controlled evaluation-and-estimation framework. The work does not claim a new learning algorithm, universal history sufficiency, numerical SOTA, production BMS readiness, or RF superiority over all deep-learning families.
