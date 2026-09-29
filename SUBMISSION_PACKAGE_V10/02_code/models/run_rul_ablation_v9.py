from pathlib import Path
import csv, math, random
from collections import defaultdict
import numpy as np
from sklearn.ensemble import RandomForestRegressor

R=Path(__file__).resolve().parent; T=R/'outputs'/'tables'
rows=list(csv.DictReader((T/'discharge_cycles_features_labels.csv').open(encoding='utf-8-sig')))
rows=[r for r in rows if r.get('operation_type')=='discharge' and r.get('rul_cycles','') not in ('','nan') and r.get('observed_eol','')=='True']
groups={
 'cycle_only':['discharge_cycle_index'],
 'state_only':['capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c'],
 'history_only':['capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','charge_throughput_ah'],
 'state_plus_history':['capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c','capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','charge_throughput_ah']}
for r in rows:
 for k in set(sum(groups.values(),[])): 
  if r.get(k,'') in ('','nan'): r[k]='0'
bats=sorted(set(r['battery_id'] for r in rows)); out=[]
for held in bats:
 train=[r for r in rows if r['battery_id']!=held]; test=[r for r in rows if r['battery_id']==held]
 if not test: continue
 for frac in (.2,.4,.6,.8):
  eol=max(float(r['eol_cycle']) for r in test); target=min(test,key=lambda r:abs(float(r['discharge_cycle_index'])-frac*eol))
  for name,fs in groups.items():
   X=np.array([[float(r[f]) for f in fs] for r in train]); y=np.array([float(r['rul_cycles']) for r in train]); model=RandomForestRegressor(n_estimators=200,random_state=2026,min_samples_leaf=2,n_jobs=-1).fit(X,y)
   pred=float(model.predict(np.array([[float(target[f]) for f in fs]]))[0]); true=float(target['rul_cycles']); out.append([held,frac,name,true,pred,abs(pred-true),(pred-true)**2])
with (T/'V9_RUL_STATE_HISTORY_ABLATION.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['held_out_battery','checkpoint_fraction','input_set','rul_true','rul_pred','absolute_error','squared_error']); w.writerows(out)
with (T/'V9_RUL_STATE_HISTORY_ABLATION_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['input_set','checkpoint_fraction','n_batteries','mae','rmse','median_abs_error','bootstrap_ci_low','bootstrap_ci_high'])
 for name in groups:
  for frac in (.2,.4,.6,.8):
   a=np.array([x[5] for x in out if x[2]==name and x[1]==frac]); ids=sorted(set(x[0] for x in out if x[2]==name and x[1]==frac)); vals=[]
   for seed in range(1000):
    rng=random.Random(seed); vals.append(float(np.mean([a[rng.randrange(len(a))] for _ in range(len(a))])))
   w.writerow([name,frac,len(ids),float(np.mean(a)),math.sqrt(float(np.mean(np.array([x[6] for x in out if x[2]==name and x[1]==frac])))),float(np.median(a)),float(np.quantile(vals,.025)),float(np.quantile(vals,.975))])
print('RUL ablation complete',len(out))
