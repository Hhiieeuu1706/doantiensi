from pathlib import Path
import csv, numpy as np
R=Path(__file__).resolve().parent; T=R/'outputs/tables'
replay=list(csv.DictReader((T/'V9_RF_SEQUENTIAL_REPLAY.csv').open(encoding='utf-8-sig')))
cal=list(csv.DictReader((T/'HUST_CALIBRATION_PREDICTIONS_V1.csv').open(encoding='utf-8-sig')))
qs={}
for frac in (.2,.4,.6,.8):
 vals=[]
 for r in cal:
  if abs(float(r.get('checkpoint_fraction',0))-frac)<1e-6 and r.get('rul_true','') not in ('','nan'):
   vals.append(abs(float(r['rul_pred_adapted'])-float(r['rul_true'])))
 qs[frac]=float(np.quantile(vals,.9)) if vals else 0.0
out=[]
for r in replay:
 frac=float(r['observation_fraction']); key=min(qs,key=lambda x:abs(x-frac)); q=qs[key]; pred=float(r['rul_pred']); true=r.get('rul_true','')
 out.append([r['battery_id'],r['cycle'],pred,max(0,pred-q),pred+q,true,frac,key,q])
with (T/'V10_RF_CALIBRATED_CYCLE_INTERVALS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['battery_id','cycle','rul_pred','rul_low','rul_high','rul_true','observation_fraction','calibration_checkpoint','quantile_width']); w.writerows(out)
with (T/'V10_RF_CALIBRATED_CYCLE_INTERVALS_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['calibration_checkpoint','quantile_width']); [w.writerow([k,v]) for k,v in qs.items()]
print('calibrated RF intervals',len(out),qs)
