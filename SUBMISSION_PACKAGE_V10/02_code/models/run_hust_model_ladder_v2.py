from pathlib import Path
import json, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF,WhiteKernel
from sklearn.linear_model import LinearRegression,HuberRegressor
from sklearn.metrics import mean_absolute_error
ROOT=Path(__file__).resolve().parent; T=ROOT/'outputs/tables'; CPS=[.2,.4,.6,.8]
def main():
 d=pd.read_csv(T/'HUST_cycle_features_v1.csv'); d=d[d.split=='development'].copy(); d['soh_initial']=d.groupby('battery_id').capacity_ah.transform('first'); d['soh']=d.capacity_ah/d.soh_initial; rows=[]
 for bid,g in d.groupby('battery_id'):
  eol=float(g.eol_cycle.dropna().iloc[0]) if g.eol_cycle.notna().any() else float((g.cycle_index+g.rul_source).median()); ref=float(g.soh_initial.iloc[0])
  for f in CPS:
   k=max(5,int(eol*f)); o=g[g.cycle_index<=k].tail(max(10,int(.65*k))); feat=[k, float(o.capacity_ah.iloc[-1]/ref),float(o.duration_s.iloc[-1]),float(o.voltage_v_mean.iloc[-1]),float(abs(o.current_a_mean.iloc[-1]))]; rows.append({'battery_id':bid,'checkpoint_fraction':f,'eol':eol,'rul_true':eol-k,'cycle':k,'soh':feat[1],'duration':feat[2],'vmean':feat[3],'imean':feat[4]})
 s=pd.DataFrame(rows); X=['cycle','soh','duration','vmean','imean']; preds=[]
 for test in s.battery_id.unique():
  tr=s[s.battery_id!=test]; te=s[s.battery_id==test].copy();
  models={'linear':LinearRegression(),'huber':HuberRegressor(),'rf':RandomForestRegressor(n_estimators=150,min_samples_leaf=3,random_state=7)}
  for name,m in models.items(): m.fit(tr[X],tr.rul_true); te['pred_'+name]=m.predict(te[X])
  gp=GaussianProcessRegressor(kernel=RBF(1.0)+WhiteKernel(.1),normalize_y=True,random_state=7).fit(tr[X].iloc[::3],tr.rul_true.iloc[::3]); te['pred_gp']=gp.predict(te[X])
  te['pred_monotone']=np.maximum(0,te.pred_linear); te['pred_ensemble']=te[['pred_linear','pred_huber','pred_rf','pred_gp','pred_monotone']].median(axis=1); preds.append(te)
 out=pd.concat(preds); out.to_csv(T/'HUST_MODEL_LADDER_LOBO_V2.csv',index=False); summ=[]
 for name in ['linear','huber','rf','gp','monotone','ensemble']:
  err=(out['pred_'+name]-out.rul_true).abs(); summ.append({'model':name,'n':len(out),'rul_mae':float(err.mean()),'rul_rmse':float(np.sqrt(((out['pred_'+name]-out.rul_true)**2).mean())),'median_ae':float(err.median()),'negative_rate':float((out['pred_'+name]<0).mean())})
 pd.DataFrame(summ).to_csv(T/'HUST_MODEL_LADDER_SUMMARY_V2.csv',index=False); print(pd.DataFrame(summ).to_string(index=False)); (T/'HUST_MODEL_LADDER_REPORT_V2.json').write_text(json.dumps({'protocol':'LOBO-development','models':[x['model'] for x in summ],'ensemble':'median of all models','calibration_touched':False,'final_touched':False},indent=2),encoding='utf-8')
if __name__=='__main__': main()
