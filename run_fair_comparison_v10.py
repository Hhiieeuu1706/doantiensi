from pathlib import Path
import csv, math
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
R=Path(__file__).resolve().parent; T=R/'outputs/tables'
rows=list(csv.DictReader((T/'discharge_cycles_features_labels.csv').open(encoding='utf-8-sig')))
rows=[r for r in rows if r.get('operation_type')=='discharge' and r.get('rul_cycles','') not in ('','nan') and r.get('observed_eol','')=='True']
features=['capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c','capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','discharge_cycle_index']
def v(r,k):
 try:return float(r.get(k,0) or 0)
 except:return 0.0
bats=sorted(set(r['battery_id'] for r in rows)); out=[]
for held in bats:
 tr=[r for r in rows if r['battery_id']!=held]; te=[r for r in rows if r['battery_id']==held]
 for frac in (.2,.4,.6,.8):
  eol=max(v(r,'eol_cycle') for r in te); z=min(te,key=lambda r:abs(v(r,'discharge_cycle_index')-frac*eol)); X=np.array([[v(r,k) for k in features] for r in tr]); y=np.array([v(r,'rul_cycles') for r in tr]); xt=np.array([[v(z,k) for k in features]])
  models={'RF':RandomForestRegressor(n_estimators=200,random_state=2026,min_samples_leaf=2,n_jobs=-1),'XGBoost':XGBRegressor(n_estimators=200,max_depth=4,learning_rate=.05,subsample=.8,colsample_bytree=.8,random_state=2026,n_jobs=4,objective='reg:squarederror')}
  for name,m in models.items():
   m.fit(X,y); pred=float(m.predict(xt)[0]); true=v(z,'rul_cycles'); out.append([held,frac,name,true,pred,abs(pred-true),(pred-true)**2])
with (T/'V10_FAIR_ENGINEERED_HI_RF_XGBOOST.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['held_out_battery','checkpoint_fraction','model','rul_true','rul_pred','absolute_error','squared_error']); w.writerows(out)
with (T/'V10_FAIR_ENGINEERED_HI_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['model','mean_mae','rmse','median_abs_error','n_predictions'])
 for name in ('RF','XGBoost'):
  a=np.array([r[5] for r in out if r[2]==name]); w.writerow([name,float(a.mean()),math.sqrt(float(np.mean(a*a))),float(np.median(a)),len(a)])
print('fair comparison complete',len(out))
