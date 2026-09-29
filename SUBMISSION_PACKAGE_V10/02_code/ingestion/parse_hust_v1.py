from pathlib import Path
import pickle, re, json, hashlib
import numpy as np, pandas as pd

ROOT=Path(__file__).resolve().parent; RAW=ROOT/'external_data/raw/HUST/extracted/our_data'; T=ROOT/'outputs/tables'
def parse_one(p):
    outer=pickle.load(open(p,'rb')); key,nextv=next(iter(outer.items())); cycles=nextv['data']; rul=nextv.get('rul',{})
    a,b=key.split('-'); bid=f'HUST_{int(a):02d}_{int(b):02d}'
    rows=[]
    for cyc,g in cycles.items():
        cyc=int(cyc); g=g.copy(); g.columns=[str(c).strip() for c in g.columns]; status=g['Status'].astype(str)
        dis=g[status.str.contains('discharge',case=False,na=False)]
        if len(dis)==0: dis=g
        cap=pd.to_numeric(dis['Capacity (mAh)'],errors='coerce').dropna()
        t=pd.to_numeric(dis['Time (s)'],errors='coerce').dropna(); v=pd.to_numeric(dis['Voltage (V)'],errors='coerce').dropna(); i=pd.to_numeric(dis['Current (mA)'],errors='coerce').dropna()
        if len(cap)==0: continue
        rows.append({'battery_id':bid,'source_file':p.name,'cycle_index':cyc,'samples':len(dis),'capacity_ah':float(cap.max()/1000),'duration_s':float(t.max()-t.min()) if len(t)>1 else np.nan,'voltage_v_mean':float(v.mean()) if len(v) else np.nan,'voltage_v_min':float(v.min()) if len(v) else np.nan,'voltage_v_max':float(v.max()) if len(v) else np.nan,'current_a_mean':float(i.mean()/1000) if len(i) else np.nan,'current_a_std':float(i.std()/1000) if len(i)>1 else np.nan,'temperature_c_mean':30.0,'temperature_c_max':30.0,'temperature_rise_c':0.0,'rul_source':float(rul.get(cyc,np.nan)) if isinstance(rul,dict) else np.nan})
    return rows
def main():
    split=pd.read_csv(T/'HUST_SPLIT_LOCK_V1.csv'); allr=[]
    for p in sorted(RAW.glob('*.pkl')): allr.extend(parse_one(p))
    d=pd.DataFrame(allr).sort_values(['battery_id','cycle_index']); d['source_dataset']='HUST'; d['protocol_id']='final-external-hust-v1.0'; d['operation_type']='discharge'; d=d.merge(split[['battery_id','split','label_access']],on='battery_id',how='left')
    labels=[]
    for bid,g in d.groupby('battery_id'):
        ref=float(g.head(5).capacity_ah.median()); below=(g.capacity_ah<.75*ref).to_numpy(); idx=np.where(below[:-1]&below[1:])[0]; eol=int(g.iloc[idx[0]].cycle_index) if len(idx) else np.nan
        labels.append({'battery_id':bid,'reference_capacity_ah':ref,'eol_threshold_ah':.75*ref,'eol_cycle':eol,'observed_eol':bool(np.isfinite(eol)),'censored':not bool(np.isfinite(eol)),'observed_cycles':len(g)})
    lab=pd.DataFrame(labels); d=d.merge(lab,on='battery_id'); d['soh']=d.capacity_ah/d.reference_capacity_ah; d['rul_cycles']=np.where((d.split!='final_untouched')&d.observed_eol,d.eol_cycle-d.cycle_index,np.nan); d['quality_status']=np.where(d.capacity_ah.between(.2,1.5)&d.duration_s.gt(0),'usable','review')
    final_mask=d.split=='final_untouched'
    for col in ['observed_eol','censored']:
        d[col]=d[col].astype('object')
    d.loc[final_mask,['reference_capacity_ah','eol_threshold_ah','eol_cycle','observed_eol','censored','soh','rul_cycles']]=np.nan
    d.to_csv(T/'HUST_cycle_features_v1.csv',index=False); lab[lab.battery_id.isin(split.query("split!='final_untouched'").battery_id)].to_csv(T/'HUST_labels_devcal_v1.csv',index=False)
    audit={'rows':len(d),'batteries':d.battery_id.nunique(),'cycles_per_battery':d.groupby('battery_id').size().describe().to_dict(),'split_counts':split.split.value_counts().to_dict(),'final_labels_locked':True,'usable_rows':int((d.quality_status=='usable').sum())}
    (T/'HUST_PARSE_AUDIT_V1.json').write_text(json.dumps(audit,indent=2),encoding='utf-8'); print(json.dumps(audit,indent=2))
if __name__=='__main__': main()
