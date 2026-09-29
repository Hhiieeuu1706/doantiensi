from pathlib import Path
import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
R=Path(__file__).resolve().parent; T=R/'outputs/tables'
rows=list(csv.DictReader((T/'HUST_cycle_features_v1.csv').open(encoding='utf-8-sig')))
features=['capacity_ah','soh','duration_s','temperature_c_mean','temperature_c_max','temperature_rise_c','voltage_v_mean','current_a_mean','current_a_std','cycle_index']
def val(r,f):
    k={'soh':'soh','cycle_index':'cycle_index'}.get(f,f)
    try: return float(r.get(k,0) or 0)
    except: return 0.0
dev=[r for r in rows if r.get('split')=='development' and r.get('rul_cycles','') not in ('','nan')]
X=np.array([[val(r,f) for f in features] for r in dev]); y=np.array([float(r['rul_cycles']) for r in dev])
model=RandomForestRegressor(n_estimators=100,random_state=2026,min_samples_leaf=2,n_jobs=-1).fit(X,y)
out=[]
for bid in sorted(set(r['battery_id'] for r in rows if r.get('split')=='final_untouched')):
    seq=sorted([r for r in rows if r['battery_id']==bid],key=lambda z:int(z['cycle_index']))
    preds=model.predict(np.array([[val(r,f) for f in features] for r in seq]))
    for r,pred0 in zip(seq,preds):
        pred=max(0.0,float(pred0)); out.append([bid,int(r['cycle_index']),pred,r.get('rul_cycles',''),float(r.get('soh',0) or 0),float(r['cycle_index'])/max(1,len(seq))])
with (T/'V9_RF_SEQUENTIAL_REPLAY.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['battery_id','cycle','rul_pred','rul_true','soh_estimate','observation_fraction']); w.writerows(out)
print('RF sequential replay',len(out))
