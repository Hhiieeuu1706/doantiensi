from pathlib import Path
import csv, numpy as np
R=Path('SUBMISSION_PACKAGE_V10/04_results/tables/supplementary'); SRC=Path('archive/root_cleanup/outputs/tables')
z=list(csv.DictReader((R/'V16_NASA_HUST_ZERO_SHOT.csv').open(encoding='utf-8-sig')))
a=list(csv.DictReader((SRC/'HUST_FINAL_UNTOUCHED_RESULTS_V1.csv').open(encoding='utf-8-sig')))
rows=[]
for frac in (.2,.4,.6,.8):
 e=[float(r['absolute_error']) for r in z if float(r['checkpoint_fraction'])==frac]
 p=[float(r['abs_error']) for r in a if float(r['checkpoint_fraction'])==frac]
 rows.append([frac,len(e),float(np.mean(e)),float(np.sqrt(np.mean(np.array(e)**2))),len(p),float(np.mean(p)),float(np.sqrt(np.mean(np.array(p)**2)))])
with (R/'V16_ZERO_SHOT_VS_ADAPTED_HUST.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['checkpoint_fraction','zero_shot_n','zero_shot_mae','zero_shot_rmse','adapted_n','adapted_mae','adapted_rmse']);w.writerows(rows)
