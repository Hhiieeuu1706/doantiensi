from pathlib import Path
import csv, math, random
import numpy as np
from sklearn.ensemble import RandomForestRegressor

ROOT=Path(__file__).resolve().parent; SRC=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'; OUT=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'tables'/'supplementary'; OUT.mkdir(parents=True,exist_ok=True)

# Nested-LOBO on NASA observed-EOL cells: inner battery holdout selects leaf size, outer battery is untouched.
rows=list(csv.DictReader((SRC/'discharge_cycles_features_labels.csv').open(encoding='utf-8-sig')))
rows=[r for r in rows if r.get('operation_type')=='discharge' and r.get('observed_eol')=='True' and r.get('rul_cycles','') not in ('','nan')]
rows=[r for r in rows if int(float(r.get('discharge_cycle_index',0))) % 5 == 0 or int(float(r.get('discharge_cycle_index',0))) <= 2]
fs=['capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c','capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','charge_throughput_ah']
for r in rows:
    for f in fs:r[f]=r.get(f) or '0'
bats=sorted({r['battery_id'] for r in rows}); nested=[]
for frac in (.2,.4,.6,.8):
  targets=[]
  for b in bats:
    br=[r for r in rows if r['battery_id']==b]; eol=max(float(r['eol_cycle']) for r in br); targets.append(min(br,key=lambda r:abs(float(r['discharge_cycle_index'])-frac*eol)))
  for t in targets:
    tr=[r for r in rows if r['battery_id']!=t['battery_id']]
    best=None
    for leaf in (1,2,4):
      vals=[]
      for valb in sorted({r['battery_id'] for r in tr}):
        it=[r for r in tr if r['battery_id']!=valb]; va=[r for r in tr if r['battery_id']==valb]
        m=RandomForestRegressor(n_estimators=10,min_samples_leaf=leaf,random_state=2026,n_jobs=-1).fit(np.array([[float(r[f]) for f in fs] for r in it]),np.array([float(r['rul_cycles']) for r in it]))
        vals.extend([abs(float(m.predict([[float(v[f]) for f in fs]])[0])-float(v['rul_cycles'])) for v in va])
      score=float(np.mean(vals))
      if best is None or score<best[0]:best=(score,leaf)
    m=RandomForestRegressor(n_estimators=10,min_samples_leaf=best[1],random_state=2026,n_jobs=-1).fit(np.array([[float(r[f]) for f in fs] for r in tr]),np.array([float(r['rul_cycles']) for r in tr]))
    pred=float(m.predict([[float(t[f]) for f in fs]])[0]); nested.append([t['battery_id'],frac,best[1],best[0],float(t['rul_cycles']),pred,abs(pred-float(t['rul_cycles']))])
with (OUT/'V15_NESTED_LOBO.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['held_out_battery','checkpoint_fraction','selected_min_samples_leaf','inner_cv_mae','rul_true','rul_pred','absolute_error']);w.writerows(nested)

# Decision-oriented interval summary from final HUST predictions (threshold: lower bound below zero is a conservative alert).
fin=list(csv.DictReader((SRC/'HUST_FINAL_NORMALIZED_CONFORMAL_V2.csv').open(encoding='utf-8-sig'))); dec=[]
for frac in (.2,.4,.6,.8):
 rr=[r for r in fin if abs(float(r['checkpoint_fraction'])-frac)<1e-9]
 dec.append([frac,len(rr),float(np.mean([float(r['rul_pred'])-float(r['rul_true']) for r in rr])),float(np.mean([float(r['norm_width']) for r in rr])) if rr and 'norm_width' in rr[0] else float('nan'),int(sum(str(r.get('norm_covered','')).lower()=='true' for r in rr))])
with (OUT/'V15_DECISION_UNCERTAINTY_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['checkpoint_fraction','n_final','mean_signed_error','mean_normalized_width','covered_count']);w.writerows(dec)

with (OUT/'V15_MULTI_DOMAIN_EVIDENCE.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['domain','role','cells_or_records','status','claim_boundary']);w.writerows([
 ['NASA PCoE','development / LOBO','4 cells; 3 observed EOL','nested LOBO completed','primary within-domain evidence'],
 ['HUST','external holdout','77 cells; 46 dev / 15 cal / 16 final','final evaluation frozen','external-domain after development-only adaptation'],
 ['CALCE','external feature audit','cycle-feature records available','no final RUL label protocol locked','cannot claim external RUL generalization yet']])
print('V15 workstreams written')
