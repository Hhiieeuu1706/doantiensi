# V19 figure and table display audit

Audit target: `BATTERY_RUL_PHD_THESIS_V20_FIGURE_CLEAN_FINAL.docx` and all PNG figures in the submission package.

## Result
- All 30 PNG figures were opened structurally and checked for pixel dimensions.
- The four legacy rasters below 1500 px on the long edge remain valid supplementary artifacts, but are not used for the principal discharge-cycle figure.
- The former dense all-cell discharge-cycle plot was replaced in the Word file by a 350 dpi four-cell small-multiples detail figure; the all-cell overview remains in the package as a supplementary figure.
- No scientific values, labels, split assignments, or frozen metrics were changed.
- The earlier mixed-scale V15.2 feature plot was removed from the final Word document; its robust-scaled and native-unit replacements remain in V18.1/V18.2.

## Figure inventory

| Figure | Pixels | Size | Status |
|---|---:|---:|---|
| `04_results/figures/01_canonical_capacity.png` | 1800 x 1080 | 169 KB | PASS |
| `04_results/figures/02_all_soh.png` | 2160 x 1260 | 363 KB | PASS |
| `04_results/figures/03_protocol_coverage.png` | 1980 x 1080 | 74 KB | PASS |
| `04_results/figures/04_feature_correlation.png` | 1440 x 1260 | 85 KB | LOW |
| `04_results/figures/05_baseline_capacity_mae.png` | 1980 x 1080 | 50 KB | PASS |
| `04_results/figures/06_early_rul_mae.png` | 1800 x 1080 | 118 KB | PASS |
| `04_results/figures/07_hi_screening_ranking.png` | 1800 x 1080 | 70 KB | PASS |
| `04_results/figures/08_ablation_10seed_capacity.png` | 1620 x 900 | 52 KB | PASS |
| `04_results/figures/09_partial_curve_mae.png` | 1440 x 900 | 64 KB | LOW |
| `04_results/figures/10_minimal_hi_subset.png` | 1440 x 900 | 61 KB | LOW |
| `04_results/figures/11_alignment_comparison.png` | 1620 x 900 | 82 KB | PASS |
| `04_results/figures/12_protocol_feature_shift.png` | 1800 x 900 | 65 KB | PASS |
| `04_results/figures/13_model_v2_capacity_mae.png` | 1800 x 900 | 122 KB | PASS |
| `04_results/figures/14_trajectory_rul_mae.png` | 1260 x 720 | 56 KB | LOW |
| `04_results/figures/15_trajectory_v3_ladder.png` | 1620 x 900 | 160 KB | PASS |
| `04_results/figures/16_deep_vs_champion.png` | 1440 x 720 | 85 KB | LOW |
| `04_results/figures/17_b0007_online_replay.png` | 1620 x 720 | 74 KB | PASS |
| `04_results/figures/fig_coverage_width.png` | 2100 x 1260 | 122 KB | PASS |
| `04_results/figures/fig_final_mae_ci.png` | 2100 x 1260 | 81 KB | PASS |
| `04_results/figures/fig_final_scatter.png` | 2100 x 1200 | 122 KB | PASS |
| `04_results/figures/fig_model_ladder_lobo.png` | 2100 x 1200 | 73 KB | PASS |
| `04_results/figures/v15_data_insights/v15_capacity_trajectories.png` | 2200 x 1320 | 492 KB | PASS |
| `04_results/figures/v15_data_insights/v15_protocol_capacity.png` | 2200 x 1100 | 133 KB | PASS |
| `04_results/figures/v15_data_insights/v15_protocol_sensitivity.png` | 1980 x 1100 | 151 KB | PASS |
| `04_results/figures/v15_data_insights/v15_rul_correlation_heatmap.png` | 1980 x 1540 | 208 KB | PASS |
| `04_results/figures/v15_data_insights/v15_state_history_distributions.png` | 2420 x 1320 | 124 KB | PASS |
| `04_results/figures/v18_data_quality/v18_capacity_trajectories_quality_flags.png` | 2640 x 1440 | 406 KB | PASS |
| `04_results/figures/v18_data_quality/v18_duration_capacity_audit.png` | 1920 x 1440 | 309 KB | PASS |
| `04_results/figures/v18_data_quality/v18_features_native_units_6panel.png` | 3278 x 1940 | 255 KB | PASS |
| `04_results/figures/v18_data_quality/v18_features_robust_scaled.png` | 2640 x 1440 | 145 KB | PASS |
| `04_results/figures/v19_publication_quality/v19_discharge_cycle_capacity_overview.png` | 3640 x 2135 | 730 KB | PASS |
| `04_results/figures/v19_publication_quality/v19_discharge_cycle_capacity_small_multiples.png` | 3637 x 2594 | 348 KB | PASS |

## Table audit

The V19 source document contains 11 Word tables. Every table has a consistent number of cells per row (no malformed row widths):

| Table | Rows x columns |
|---|---:|
| T1 | 6 x 3 |
| T2 | 4 x 3 |
| T3 | 5 x 5 |
| T4 | 5 x 5 |
| T5 | 7 x 4 |
| T6 | 5 x 6 |
| T7 | 5 x 4 |
| T8 | 5 x 4 |
| T9 | 4 x 5 |
| T10 | 7 x 5 |
| T11 | 5 x 3 |

The remaining required check is visual rendering in Word/LibreOffice at 100% zoom; if the local renderer is unavailable, the PNG inventory and OOXML/table checks above are the reproducible structural audit.
