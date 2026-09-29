from pathlib import Path
import csv, random, math
import numpy as np
from sklearn.ensemble import RandomForestRegressor

ROOT=Path(__file__).resolve().parent
src=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'/'discharge_cycles_features_labels.csv'
outdir=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'tables'/'supplementary'
outdir.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(src.open(encoding='utf-8-sig')))
rows=[r for r in rows if r.get('operation_type')=='discharge' and r.get('observed_eol')=='True' and r.get('rul_cycles','') not in ('','nan')]
features=['capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c','capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','charge_throughput_ah']
for r in rows:
    for f in features: r[f]=r.get(f) or '0'
bats=sorted({r['battery_id'] for r in rows}); records=[]
for frac in (.2,.4,.6,.8):
    targets=[]
    for b in bats:
        br=[r for r in rows if r['battery_id']==b]
        eol=max(float(r['eol_cycle']) for r in br)
        targets.append(min(br,key=lambda r:abs(float(r['discharge_cycle_index'])-frac*eol)))
    test_ids={(t['battery_id'],t['discharge_cycle_index']) for t in targets}
    pool=[r for r in rows if (r['battery_id'],r['discharge_cycle_index']) not in test_ids]
    rng=random.Random(2026+int(frac*100)); rng.shuffle(pool); cut=max(1,int(.8*len(pool)))
    fixed_holdout=targets[0]['battery_id']
    for protocol, testset, trainset in [('random_cycle',targets,pool[:cut]),('battery_holdout',[t for t in targets if t['battery_id']==fixed_holdout],[r for r in rows if r['battery_id']!=fixed_holdout]),('LOBO',targets,rows)]:
        if protocol=='LOBO':
            pred=[]
            for t in testset:
                tr=[r for r in rows if r['battery_id']!=t['battery_id']]
                m=RandomForestRegressor(n_estimators=200,min_samples_leaf=2,random_state=2026,n_jobs=-1).fit(np.array([[float(r[f]) for f in features] for r in tr]),np.array([float(r['rul_cycles']) for r in tr]))
                pred.append((float(m.predict([[float(t[f]) for f in features]])[0]),float(t['rul_cycles'])))
        else:
            m=RandomForestRegressor(n_estimators=200,min_samples_leaf=2,random_state=2026,n_jobs=-1).fit(np.array([[float(r[f]) for f in features] for r in trainset]),np.array([float(r['rul_cycles']) for r in trainset]))
            pred=[(float(m.predict([[float(t[f]) for f in features]])[0]),float(t['rul_cycles'])) for t in testset]
        errs=[abs(p-y) for p,y in pred]; sq=[(p-y)**2 for p,y in pred]
        records.append([protocol,frac,len(errs),float(np.mean(errs)),math.sqrt(float(np.mean(sq))),float(np.median(errs))])
with (outdir/'V14_E1_PROTOCOL_SENSITIVITY.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['protocol','checkpoint_fraction','n_batteries','mae','rmse','median_abs_error']); w.writerows(records)
print('wrote',outdir/'V14_E1_PROTOCOL_SENSITIVITY.csv')
