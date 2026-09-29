from pathlib import Path
import json,numpy as np,pandas as pd
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parent;T=ROOT/'outputs/tables';X=['cycle','soh','duration','vmean','imean']
def main():
 dev=pd.read_csv(T/'HUST_MODEL_LADDER_LOBO_V2.csv'); raw=pd.read_csv(T/'HUST_cycle_features_v1.csv'); ids=pd.read_csv(T/'HUST_SPLIT_LOCK_V1.csv').query("split=='calibration'").battery_id.tolist(); rows=[]
 for bid,g in raw[raw.battery_id.isin(ids)].groupby('battery_id'):
  e=float((g.cycle_index+g.rul_source).median()); ref=g.capacity_ah.head(5).median(); g=g.copy(); g['soh']=g.capacity_ah/ref
  for f in [.2,.4,.6,.8]:
   k=int(e*f); o=g[g.cycle_index<=k].iloc[-1]; rows.append({'battery_id':bid,'checkpoint_fraction':f,'rul_true':e-k,'cycle':k,'soh':o.soh,'duration':o.duration_s,'vmean':o.voltage_v_mean,'imean':abs(o.current_a_mean)})
 cal=pd.DataFrame(rows); rf=RandomForestRegressor(n_estimators=400,min_samples_leaf=3,random_state=11).fit(dev[X],dev.rul_true); cal['pred_rf']=rf.predict(cal[X]); cal['abs_error']=(cal.pred_rf-cal.rul_true).abs(); cal.to_csv(T/'HUST_RF_CALIBRATION_V1.csv',index=False); alpha=.1; q={}
 for k,g in cal.groupby('checkpoint_fraction'):
  n=len(g); rank=min(n,max(1,int(np.ceil((n+1)*(1-alpha))))); q[k]=float(np.sort(g.abs_error.to_numpy())[rank-1])
 cov={str(k):float((g.abs_error<=q[k]).mean()) for k,g in cal.groupby('checkpoint_fraction')}; out={'model':'RF-champion-v1','train_cells':int(dev.battery_id.nunique()),'calibration_cells':int(cal.battery_id.nunique()),'mae':float(cal.abs_error.mean()),'quantiles_90':q,'coverage_by_checkpoint':cov,'target_coverage':.9,'finite_sample_conformal':True,'final_touched':False}; (T/'HUST_RF_CALIBRATION_REPORT_V1.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
