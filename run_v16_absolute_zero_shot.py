from pathlib import Path
import csv, math
import numpy as np
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'
OUT=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'tables'/'supplementary'; OUT.mkdir(parents=True,exist_ok=True)
NASA=list(csv.DictReader((SRC/'discharge_cycles_features_labels.csv').open(encoding='utf-8-sig')))
NASA=[r for r in NASA if r.get('operation_type')=='discharge' and r.get('observed_eol')=='True' and r.get('rul_cycles','') not in ('','nan')]
H=list(csv.DictReader((SRC/'HUST_cycle_features_v1.csv').open(encoding='utf-8-sig')))
H=[r for r in H if r.get('operation_type')=='discharge']
HF=list(csv.DictReader((SRC/'HUST_FINAL_UNTOUCHED_RESULTS_V1.csv').open(encoding='utf-8-sig')))
def n(r,k):
    try:return float(r.get(k,0) or 0)
    except:return 0.0
def xn(r): return [n(r,'capacity_ah'),n(r,'duration_s'),n(r,'voltage_v_mean'),n(r,'current_a_mean'),n(r,'temperature_c_mean'),n(r,'temperature_rise_c'),n(r,'discharge_cycle_index')]
def xh(r): return [n(r,'capacity_ah'),n(r,'duration_s'),n(r,'voltage_v_mean'),n(r,'current_a_mean'),n(r,'temperature_c_mean'),n(r,'temperature_rise_c'),n(r,'cycle_index')]
m0=RandomForestRegressor(n_estimators=200,min_samples_leaf=2,random_state=2026,n_jobs=-1).fit(np.array([xn(r) for r in NASA]),np.array([n(r,'rul_cycles') for r in NASA]))
final=[r for r in HF]
dev=[r for r in H if r.get('split')=='development' and r.get('rul_cycles','') not in ('','nan')]
rows=[]
for b in sorted({r['battery_id'] for r in final}):
    br=sorted([r for r in final if r['battery_id']==b],key=lambda r:n(r,'cycle')); eol=max(n(r,'cycle')+n(r,'rul_true') for r in br)
    for frac in (.2,.4,.6,.8):
        t=min(br,key=lambda r:abs(n(r,'cycle')-frac*eol)); q={'capacity_ah':t.get('soh',0),'cycle_index':t.get('cycle',0),'duration_s':t.get('duration',0),'voltage_v_mean':t.get('vmean',0),'current_a_mean':t.get('imean',0),'temperature_c_mean':0,'temperature_rise_c':0}; p=float(m0.predict([xh(q)])[0]); y=n(t,'rul_true'); rows.append(['NASA_to_HUST_zero_shot',b,frac,n(t,'cycle'),y,p,abs(p-y)])
with (OUT/'V16_NASA_HUST_ZERO_SHOT.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['stage','battery_id','checkpoint_fraction','cycle','rul_true','rul_pred','absolute_error']);w.writerows(rows)
with (OUT/'V16_NASA_HUST_ZERO_SHOT_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['stage','checkpoint_fraction','n','mae','rmse'])
    for frac in (.2,.4,.6,.8):
        a=[r for r in rows if r[2]==frac]; e=[float(r[6]) for r in a]; w.writerow(['NASA_to_HUST_zero_shot',frac,len(e),float(np.mean(e)),math.sqrt(float(np.mean(np.array(e)**2)))])
absrows=[]
for b in sorted({r['battery_id'] for r in NASA}):
    tr=[r for r in NASA if r['battery_id']!=b]; te=[r for r in NASA if r['battery_id']==b]
    m1=RandomForestRegressor(n_estimators=100,min_samples_leaf=2,random_state=2026,n_jobs=-1).fit(np.array([xn(r) for r in tr]),np.array([n(r,'rul_cycles') for r in tr]))
    for cyc in (25,50,75,100):
        eligible=[r for r in te if n(r,'discharge_cycle_index')>=cyc]
        if not eligible: continue
        t=min(eligible,key=lambda r:abs(n(r,'discharge_cycle_index')-cyc)); p=float(m1.predict([xn(t)])[0]); y=n(t,'rul_cycles'); absrows.append(['NASA_LOBO_absolute_cycle',b,cyc,n(t,'discharge_cycle_index'),y,p,abs(p-y)])
with (OUT/'V16_ABSOLUTE_CYCLE_EVALUATION.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f);w.writerow(['stage','battery_id','requested_cycle','used_cycle','rul_true','rul_pred','absolute_error']);w.writerows(absrows)
print('wrote V16 tables')
