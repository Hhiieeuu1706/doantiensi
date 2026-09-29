# Submission package plan

## Keep

### Manuscript
- `06_manuscript/BATTERY_RUL_PHD_THESIS_V11_QUALITY_AUDITED.docx`
- `06_manuscript/Battery_RUL_Research_Q1_Enhanced_FIXED.docx`

### Protocol and reproducibility
- `02_protocol/V10_PROTOCOL_LOCK.yaml`
- `research_protocol_v3.yaml`
- `final_external_protocol_v1.yaml`
- `requirements-deep.txt`
- `outputs/tables/HUST_RAW_MANIFEST_V1.csv`
- `outputs/tables/HUST_SPLIT_LOCK_V1.csv`
- `outputs/tables/V10_CANONICAL_SCHEMA.csv`
- `outputs/reports/V10_PROCESS_QUALITY_GATE.json`
- `outputs/reports/V10_PROCESS_REPORT.md`

### Core code
- `prepare_hust_external_v1.py`
- `parse_hust_v1.py`
- `audit_hust_compatibility_v1.py`
- `run_hust_model_ladder_v2.py`
- `calibrate_hust_rf_v1.py`
- `freeze_and_test_hust_final_v1.py`
- `run_fair_comparison_v10.py`
- `run_fair_deep_engineered_v10.py`
- `run_rul_ablation_v9.py`
- `run_rf_sequential_replay_v9.py`
- `calibrate_rf_cycle_intervals_v10.py`
- `online_service.py`
- `bms_adapter.py`
- `test_online_hil.py`

### Main evidence tables
- `HUST_FINAL_UNTOUCHED_RESULTS_V1.csv`
- `HUST_FINAL_STATISTICS_BOOTSTRAP_V1.csv`
- `HUST_MODEL_LADDER_LOBO_V2.csv`
- `HUST_RF_CALIBRATION_V1.csv`
- `V9_RUL_STATE_HISTORY_ABLATION_SUMMARY.csv`
- `V10_FAIR_MODEL_FAMILY_FINAL.csv`
- `V10_FAIR_DEEP_ENGINEERED_HI_SUMMARY.csv`
- `V11_DEEP_PER_BATTERY_BOOTSTRAP.csv`
- `V10_RF_CALIBRATED_CYCLE_INTERVALS.csv`
- `V10_RF_CALIBRATED_CYCLE_INTERVALS_SUMMARY.csv`
- `V9_NORMALIZED_FINAL_METRICS.csv`
- `V9_PUBLISHED_BENCHMARK_HUST.csv`
- `V10_FRAMEWORK_ABLATION_MATRIX.csv`

### Figures
- all publication figures in `outputs/figures` referenced by the manuscript

## Exclude from ZIP

- `.venv-deep`, `.venv-v9`, `.deps`, `node_modules`
- `.mplcache`, `.mplconfig`, `__pycache__`
- `delete_me`, `render_final`, `render_v9`
- `archive` and obsolete manuscript versions
- intermediate exploratory CSVs not listed above
- deep training logs and raw per-cycle predictions unless specifically requested by reviewers
- workbook builders and one-off analysis scripts

## Important

Do not delete excluded files from the working archive until submission is accepted. Exclusion from the ZIP is sufficient. Raw HUST data may be too large for email; provide its SHA-256 manifest and the official Mendeley DOI when required.
