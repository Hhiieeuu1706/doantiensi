from pathlib import Path
import hashlib,json,numpy as np,pandas as pd
from sklearn.ensemble import RandomForestRegressor
ROOT=Path(__file__).resolve().parent;T=ROOT/'outputs/tables';X=['cycle','soh','duration','vmean','imean']
def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 files=[T/'HUST_ADAPTER_FEATURES_V1.csv',T/'HUST_MODEL_LADDER_SUMMARY_V2.csv',T/'HUST_RF_CALIBRATION_REPORT_V1.json',ROOT/'run_hust_model_ladder_v2.py',ROOT/'calibrate_hust_rf_v1.py']; manifest=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in files]; (T/'HUST_FINAL_FREEZE_MANIFEST_V1.csv').write_text(pd.DataFrame(manifest).to_csv(index=False),encoding='utf-8')
 d=pd.read_csv(T/'HUST_MODEL_LADDER_LOBO_V2.csv'); raw=pd.read_csv(T/'HUST_cycle_features_v1.csv'); splits=pd.read_csv(T/'HUST_SPLIT_LOCK_V1.csv'); ids=splits.query("split=='final_untouched'").battery_id.tolist(); rows=[]; rf=RandomForestRegressor(n_estimators=400,min_samples_leaf=3,random_state=11).fit(d[X],d.rul_true)
 for bid,g in raw[raw.battery_id.isin(ids)].groupby('battery_id'):
  e=float((g.cycle_index+g.rul_source).median()); ref=g.capacity_ah.head(5).median(); g=g.copy(); g['soh']=g.capacity_ah/ref
  for f in [.2,.4,.6,.8]:
   k=int(e*f); o=g[g.cycle_index<=k].iloc[-1]; row={'battery_id':bid,'checkpoint_fraction':f,'rul_true':e-k,'cycle':k,'soh':o.soh,'duration':o.duration_s,'vmean':o.voltage_v_mean,'imean':abs(o.current_a_mean)}; row['rul_pred']=float(rf.predict(pd.DataFrame([row])[X])[0]); rows.append(row)
 out=pd.DataFrame(rows); out['abs_error']=(out.rul_pred-out.rul_true).abs(); cal=json.loads((T/'HUST_RF_CALIBRATION_REPORT_V1.json').read_text()); out['interval_q']=out.checkpoint_fraction.map({float(k):v for k,v in cal['quantiles_90'].items()}); out['covered']=out.abs_error<=out.interval_q; out.to_csv(T/'HUST_FINAL_UNTOUCHED_RESULTS_V1.csv',index=False); summary=out.groupby('checkpoint_fraction').agg(n=('rul_true','size'),rul_mae=('abs_error','mean'),coverage=('covered','mean'),interval_width=('interval_q','mean')).reset_index(); summary.to_csv(T/'HUST_FINAL_UNTOUCHED_SUMMARY_V1.csv',index=False); print(summary.to_string(index=False)); print(json.dumps({'final_cells':len(ids),'predictions':len(out),'manifest_files':len(manifest),'final_opened_once':True},indent=2))
if __name__=='__main__':main()
