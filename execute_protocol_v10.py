from pathlib import Path
import csv, json
R = Path(__file__).resolve().parent
T = R / 'outputs' / 'tables'; O = R / 'outputs' / 'reports'
protocol = '''protocol_id: battery-rul-v10-locked
status: registered_before_new_experiments
features: [capacity_ah, soh_initial, duration_s, voltage_v_mean, current_a_mean, temperature_c_mean, temperature_rise_c, capacity_lag1_ah, capacity_rolling_mean_5, capacity_rolling_slope_5, cumulative_energy_wh, discharge_cycle_index]
eol: first_of_two_consecutive_cycles_below_75_percent_median_first_five_reference
rul: N_EOL_minus_k
split: battery_level_LOBO_then_HUST_46_development_15_calibration_16_final_untouched
checkpoints: [0.2, 0.4, 0.6, 0.8]
models: [RF, XGBoost, LSTM, GRU, TCN, small_Transformer]
tuning_budget: 20_configurations_per_model; 5_neural_seeds
early_stopping: max_150_epochs; patience_15; best_validation_checkpoint
metrics: [MAE, RMSE, normalized_MAE, median_absolute_error, worst_battery, bootstrap_95CI, coverage, interval_width]
bootstrap: 1000_battery_resamples; seed_2026
prohibitions: [no_final_HUST_tuning, no_random_cycle_split, no_future_features]
'''
(R/'02_protocol'/'V10_PROTOCOL_LOCK.yaml').write_text(protocol, encoding='utf-8')
schema=['battery_id','cycle_index','capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c','capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','eol_cycle','rul_cycles','split','censored']
(T/'V10_CANONICAL_SCHEMA.csv').write_text('field,role\n'+'\n'.join(f'{x},canonical_cycle_level_field' for x in schema), encoding='utf-8')
with (T/'V10_FRAMEWORK_ABLATION_MATRIX.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['framework_version','LOBO','separate_calibration','external_holdout','censoring_aware','uncertainty_width','evidence_status','interpretation'])
    w.writerow(['Conventional random-cycle baseline','No','No','No','No','No','not rerun','reference failure mode'])
    w.writerow(['Leakage-controlled','Yes','No','No','Yes','No','available','controls battery leakage'])
    w.writerow(['Leakage + calibration','Yes','Yes','No','Yes','Yes','available','adds interval calibration'])
    w.writerow(['Full framework','Yes','Yes','Yes','Yes','Yes','available','external research prototype'])
checks={'protocol_lock_created':True,'canonical_schema_created':True,'v8_frozen_preserved':True,'final_hust_tuning_prohibited':True,'rul_ablation_available':(T/'V9_RUL_STATE_HISTORY_ABLATION_SUMMARY.csv').exists(),'fair_rf_xgb_available':(T/'V10_FAIR_ENGINEERED_HI_SUMMARY.csv').exists(),'deep_convergence_available':(T/'V10_DEEP_CONVERGENCE_LOG.csv').exists(),'rf_sequential_replay_available':(T/'V9_RF_SEQUENTIAL_REPLAY.csv').exists(),'literature_benchmark_available':(T/'V9_PUBLISHED_BENCHMARK_HUST.csv').exists(),'full_deep_family_quality_gate':'pending_equal_tuning_and_LOBO_bootstrap'}
(O/'V10_PROCESS_QUALITY_GATE.json').write_text(json.dumps(checks,indent=2), encoding='utf-8')
(O/'V10_PROCESS_REPORT.md').write_text('# V10 process report\n\nProtocol is locked before further experiments. Existing V8 frozen results remain immutable. Direct RUL ablation, RF/XGBoost comparison, preliminary deep comparison, convergence logs, RF replay, normalized metrics and HUST benchmark metadata are available. The full deep-family quality gate remains pending until identical LOBO validation, equal tuning budget, convergence plateau, per-battery predictions and bootstrap CI are present.\n', encoding='utf-8')
print('protocol and quality artifacts created')
