from pathlib import Path
import csv, random, math
import numpy as np
import torch
from torch import nn
R=Path(__file__).resolve().parent; T=R/'outputs/tables'
rows=list(csv.DictReader((T/'discharge_cycles_features_labels.csv').open(encoding='utf-8-sig')))
rows=[r for r in rows if r.get('operation_type')=='discharge' and r.get('rul_cycles','') not in ('','nan') and r.get('observed_eol','')=='True']
feat=['capacity_ah','soh_initial','duration_s','voltage_v_mean','current_a_mean','temperature_c_mean','temperature_rise_c','capacity_lag1_ah','capacity_rolling_mean_5','capacity_rolling_slope_5','cumulative_energy_wh','discharge_cycle_index']
def v(r,k):
 try:return float(r.get(k,0) or 0)
 except:return 0.0
class Net(nn.Module):
 def __init__(self,kind):
  super().__init__(); self.kind=kind; self.proj=nn.Linear(len(feat),32)
  if kind=='LSTM': self.seq=nn.LSTM(32,32,batch_first=True)
  elif kind=='GRU': self.seq=nn.GRU(32,32,batch_first=True)
  elif kind=='TCN': self.seq=nn.Conv1d(32,32,3,padding=2)
  else: self.att=nn.MultiheadAttention(32,4,batch_first=True); self.ff=nn.Sequential(nn.Linear(32,32),nn.ReLU())
  self.out=nn.Linear(32,1)
 def forward(self,x):
  z=torch.relu(self.proj(x))
  if self.kind in ('LSTM','GRU'): z=self.seq(z)[0][:,-1]
  elif self.kind=='TCN': z=torch.relu(self.seq(z.transpose(1,2)))[:,:,:x.shape[1]].mean(2)
  else: z=self.ff(self.att(z,z,z)[0]).mean(1)
  return self.out(z).squeeze(-1)
def make_seq(rs,i,L=20):
 s=rs[max(0,i-L+1):i+1]; a=np.array([[v(r,k) for k in feat] for r in s],float); a=np.vstack([np.zeros((L-len(a),len(feat))),a]); return a
out=[]; bats=sorted(set(r['battery_id'] for r in rows))
for held in bats:
 tr=sorted([r for r in rows if r['battery_id']!=held],key=lambda r:int(r['discharge_cycle_index'])); te=sorted([r for r in rows if r['battery_id']==held],key=lambda r:int(r['discharge_cycle_index']))
 trainX=np.stack([make_seq([r for r in tr if r['battery_id']==b],i) for b in sorted(set(r['battery_id'] for r in tr)) for i,r in enumerate([q for q in tr if q['battery_id']==b])]); trainy=np.array([v(r,'rul_cycles') for r in tr],float)
 mu=trainX.reshape(-1,len(feat)).mean(0); sd=trainX.reshape(-1,len(feat)).std(0)+1e-6; trainX=(trainX-mu)/sd
 for frac in (.2,.4,.6,.8):
  eol=max(v(r,'eol_cycle') for r in te); target=min(te,key=lambda r:abs(v(r,'discharge_cycle_index')-frac*eol)); ti=te.index(target); tx=(make_seq(te,ti)-mu)/sd
  for kind in ('LSTM','GRU','TCN','Transformer'):
   preds=[]
   for seed in (11,22,33,44,55):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed); m=Net(kind); opt=torch.optim.Adam(m.parameters(),lr=0.003); X=torch.tensor(trainX,dtype=torch.float32); y=torch.tensor(trainy,dtype=torch.float32)
    for _ in range(10): opt.zero_grad(); loss=((m(X)-y)**2).mean(); loss.backward(); opt.step()
    with torch.no_grad(): preds.append(float(m(torch.tensor(tx[None],dtype=torch.float32))[0]))
   true=v(target,'rul_cycles'); pred=float(np.mean(preds)); out.append([held,frac,kind,true,pred,abs(pred-true),float(np.std(preds,ddof=1))])
with (T/'V10_FAIR_DEEP_ENGINEERED_HI.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['held_out_battery','checkpoint_fraction','model','rul_true','rul_pred','absolute_error','seed_std']); w.writerows(out)
with (T/'V10_FAIR_DEEP_ENGINEERED_HI_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['model','mean_mae','rmse','median_abs_error','n_predictions'])
 for kind in ('LSTM','GRU','TCN','Transformer'):
  a=np.array([r[5] for r in out if r[2]==kind]); w.writerow([kind,float(a.mean()),math.sqrt(float(np.mean(a*a))),float(np.median(a)),len(a)])
print('deep fair comparison complete',len(out))
