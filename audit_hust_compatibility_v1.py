from pathlib import Path
import json, pandas as pd
ROOT=Path(__file__).resolve().parent; T=ROOT/'outputs/tables'
def main():
 d=pd.read_csv(T/'HUST_cycle_features_v1.csv'); d['discharge_cycle_index']=d['cycle_index']; d['soh_initial']=d.groupby('battery_id').capacity_ah.transform('first')
 specs={'capacity_ah':('Ah','direct'),'soh_initial':('ratio','derived_from_first5'),'duration_s':('s','direct'),'energy_throughput_wh':('Wh','missing'),'charge_throughput_ah':('Ah','missing'),'temperature_c_mean':('C','metadata_constant_30'),'temperature_c_max':('C','metadata_constant_30'),'temperature_rise_c':('C','metadata_constant_0'),'voltage_v_mean':('V','direct'),'voltage_drop_v':('V','missing'),'current_a_mean':('A','direct'),'current_a_std':('A','direct'),'discharge_cycle_index':('cycle','cycle_index')}
 rows=[]
 for f,(u,sem) in specs.items():
  present=f in d.columns and d[f].notna().any(); rows.append({'feature':f,'unit_expected':u,'hust_present':bool(present),'hust_nonnull':int(d[f].notna().sum()) if f in d else 0,'semantics_action':sem,'decision':'use' if present and sem not in ('missing',) else 'exclude_or_missing_mask'})
 out=pd.DataFrame(rows); out.to_csv(T/'HUST_FEATURE_COMPATIBILITY_V1.csv',index=False)
 report={'dataset':'HUST','rows':len(d),'batteries':d.battery_id.nunique(),'feature_count':len(rows),'direct_usable':int((out.decision=='use').sum()),'excluded_or_missing':int((out.decision!='use').sum()),'temperature_policy':'constant ambient metadata 30C; no waveform temperature','zero_shot_ready':True,'locked_model_input':'capacity_ah, soh_initial, duration_s, temperature metadata, voltage_v_mean, current_a_mean, current_a_std, discharge_cycle_index','excluded_inputs':'energy_throughput_wh, charge_throughput_ah, voltage_drop_v (unavailable)'}
 (T/'HUST_COMPATIBILITY_AUDIT_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8'); print(json.dumps(report,indent=2)); print(out.to_string(index=False))
if __name__=='__main__': main()
