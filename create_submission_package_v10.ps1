$root=(Get-Location).Path
$pkg=Join-Path $root 'SUBMISSION_PACKAGE_V10'
if(Test-Path $pkg){Remove-Item -LiteralPath $pkg -Recurse -Force}
$dirs=@('01_protocol','02_code\ingestion','02_code\models','02_code\online','03_data_manifests','04_results\tables','04_results\figures','04_results\reports','05_manuscript','06_reproducibility','07_external_data_pointer')
foreach($d in $dirs){New-Item -ItemType Directory -Path (Join-Path $pkg $d) -Force | Out-Null}
function CopyToPackage($src,$dst){$s=Join-Path $root $src; if(Test-Path $s){Copy-Item -LiteralPath $s -Destination (Join-Path $pkg $dst) -Force}}
CopyToPackage '02_protocol\V10_PROTOCOL_LOCK.yaml' '01_protocol\V10_PROTOCOL_LOCK.yaml'; CopyToPackage 'research_protocol_v3.yaml' '01_protocol\research_protocol_v3.yaml'; CopyToPackage 'final_external_protocol_v1.yaml' '01_protocol\final_external_protocol_v1.yaml'; CopyToPackage 'external_data_contract.yaml' '01_protocol\external_data_contract.yaml'
foreach($f in @('prepare_hust_external_v1.py','parse_hust_v1.py','audit_hust_compatibility_v1.py')){CopyToPackage $f ('02_code\ingestion\'+$f)}
foreach($f in @('run_hust_model_ladder_v2.py','calibrate_hust_rf_v1.py','freeze_and_test_hust_final_v1.py','run_rul_ablation_v9.py','run_fair_comparison_v10.py','run_fair_deep_engineered_v10.py','calibrate_rf_cycle_intervals_v10.py')){CopyToPackage $f ('02_code\models\'+$f)}
foreach($f in @('online_service.py','run_rf_sequential_replay_v9.py','test_online_hil.py','bms_adapter.py')){CopyToPackage $f ('02_code\online\'+$f)}
foreach($f in @('HUST_RAW_MANIFEST_V1.csv','HUST_SPLIT_LOCK_V1.csv','V10_CANONICAL_SCHEMA.csv')){CopyToPackage ('outputs\tables\'+$f) ('03_data_manifests\'+$f)}
foreach($f in @('HUST_FINAL_UNTOUCHED_RESULTS_V1.csv','HUST_FINAL_STATISTICS_BOOTSTRAP_V1.csv','HUST_MODEL_LADDER_LOBO_V2.csv','HUST_RF_CALIBRATION_V1.csv','V9_RUL_STATE_HISTORY_ABLATION_SUMMARY.csv','V10_FAIR_MODEL_FAMILY_FINAL.csv','V10_FAIR_DEEP_ENGINEERED_HI_SUMMARY.csv','V11_DEEP_PER_BATTERY_BOOTSTRAP.csv','V10_RF_CALIBRATED_CYCLE_INTERVALS.csv','V10_RF_CALIBRATED_CYCLE_INTERVALS_SUMMARY.csv','V9_NORMALIZED_FINAL_METRICS.csv','V9_PUBLISHED_BENCHMARK_HUST.csv','V10_FRAMEWORK_ABLATION_MATRIX.csv')){CopyToPackage ('outputs\tables\'+$f) ('04_results\tables\'+$f)}
Get-ChildItem outputs\figures -File | Where-Object {$_.Name -match "^(fig_|0[1-9]_).*" -and $_.Extension -in '.png','.pdf','.svg'} | ForEach-Object {CopyToPackage ('outputs\figures\'+$_.Name) ('04_results\figures\'+$_.Name)}
foreach($f in @('V10_PROCESS_QUALITY_GATE.json','V10_PROCESS_REPORT.md','V9_COMPLETION_STATUS.md','V11_DEEP_QUALITY_GATE.md')){CopyToPackage ('outputs\reports\'+$f) ('04_results\reports\'+$f)}
foreach($f in @('quality_gate_environment.json','RESEARCH_QUALITY_GATE_V3.md')){CopyToPackage ('outputs\reports\'+$f) ('04_results\reports\'+$f)}
CopyToPackage 'outputs\tables\V10_MODEL_FAMILY_COMPARISON_STATUS.csv' '04_results\tables\V10_MODEL_FAMILY_COMPARISON_STATUS.csv'
CopyToPackage '06_manuscript\BATTERY_RUL_PHD_THESIS_V11_QUALITY_AUDITED.docx' '05_manuscript\BATTERY_RUL_PHD_THESIS_V11_QUALITY_AUDITED.docx'; CopyToPackage '06_manuscript\Battery_RUL_Research_Q1_Enhanced_FIXED.docx' '05_manuscript\Battery_RUL_Research_Q1_Enhanced_FIXED.docx'
CopyToPackage 'requirements-deep.txt' '06_reproducibility\requirements-deep.txt'; CopyToPackage '07_reproducibility\SUBMISSION_PACKAGE_MANIFEST_V1.csv' '06_reproducibility\SUBMISSION_PACKAGE_MANIFEST_V1.csv'; CopyToPackage '07_reproducibility\PROCESS_STATUS_V10.md' '06_reproducibility\PROCESS_STATUS_V10.md'
CopyToPackage '07_reproducibility\README.md' '06_reproducibility\README.md'; CopyToPackage 'PROJECT_MAP.md' '06_reproducibility\PROJECT_MAP.md'; CopyToPackage 'RELEASE_README_V1.md' '06_reproducibility\RELEASE_README_V1.md'; CopyToPackage 'V9_COMPLETION_STATUS.md' '06_reproducibility\V9_COMPLETION_STATUS.md'
@'
# External data pointer

Raw HUST data are intentionally not duplicated into this package because the archive is approximately 1.2 GB. Download the official dataset from Mendeley Data DOI 10.17632/nsc7hnsg4s.2 and verify it against `03_data_manifests/HUST_RAW_MANIFEST_V1.csv`.
'@ | Set-Content (Join-Path $pkg '07_external_data_pointer\README.md')
@'
# Battery RUL submission package V10

This package is organized by function. Start with `06_reproducibility/README.md`, then read `01_protocol`, run code under `02_code` from the original project root, inspect `04_results`, and open the thesis in `05_manuscript`.

V8 frozen results are preserved. V9/V10 additions are labeled. The package does not claim production BMS readiness or universal RF superiority over deep learning.
'@ | Set-Content (Join-Path $pkg 'README.md')
@'
The scripts in this submission package are copied for archival clarity. For exact execution, run them from the original `battery_rul_pipeline` root because they resolve paths relative to their source location.
'@ | Set-Content (Join-Path $pkg '02_code\README.md')
Write-Output $pkg
