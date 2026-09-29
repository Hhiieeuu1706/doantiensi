from pathlib import Path
import csv, math
import numpy as np
ROOT=Path(__file__).resolve().parent
T=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'; O=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'tables'/'supplementary'; O.mkdir(parents=True,exist_ok=True)
cal=list(csv.DictReader((T/'HUST_RF_CALIBRATION_V1.csv').open(encoding='utf-8-sig')))
fin=list(csv.DictReader((T/'HUST_FINAL_UNTOUCHED_RESULTS_V1.csv').open(encoding='utf-8-sig')))
rows=[]
for cov in (.80,.90,.95):
  for frac in (.2,.4,.6,.8):
    ce=[float(r['abs_error']) for r in cal if abs(float(r['checkpoint_fraction'])-frac)<1e-9]
    fe=[float(r['abs_error']) for r in fin if abs(float(r['checkpoint_fraction'])-frac)<1e-9]
    q=float(np.quantile(ce, cov, method='higher')) if ce else float('nan')
    covered=[e<=q for e in fe]
    true=[float(r['rul_true']) for r in fin if abs(float(r['checkpoint_fraction'])-frac)<1e-9]
    width=2*q
    rows.append([cov,frac,len(fe),float(np.mean(covered)),q,width,width/(float(np.mean(true)) if true else float('nan')),float(np.median(true))])
with (O/'V14_E8_COVERAGE_WIDTH.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['target_coverage','checkpoint_fraction','n_final','actual_coverage','half_width','interval_width','normalized_width_mean_rul','median_true_rul']); w.writerows(rows)
print('wrote',O/'V14_E8_COVERAGE_WIDTH.csv')
