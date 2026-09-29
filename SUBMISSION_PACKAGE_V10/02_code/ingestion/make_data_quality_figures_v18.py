from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
ROOT=Path(__file__).resolve().parent
src=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'/'discharge_cycles_features_labels.csv'
out=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'figures'/'v18_data_quality'; out.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(src); df=df[df.operation_type.eq('discharge')].copy()
df['incomplete_cycle_flag']=(df['duration_s']<500)|(df['n_samples']<50)
df['capacity_anomaly_flag']=df['capacity_ah'].isna()|(df['capacity_ah']<=0)
df['label_excluded_by_quality']=df['incomplete_cycle_flag']|df['capacity_anomaly_flag']
cols=['capacity_ah','duration_s','voltage_drop_v','temperature_rise_c','capacity_rolling_slope_5','cumulative_energy_wh']; cols=[c for c in cols if c in df.columns]
summary=[]
for c in cols:
 q1,q3=df[c].quantile([.25,.75]); summary.append([c,len(df),float(df[c].median()),float(q3-q1),float(df[c].min()),float(df[c].max()),int(df[c].isna().sum())])
pd.DataFrame(summary,columns=['feature','n','median','iqr','min','max','missing']).to_csv(out/'v18_feature_scale_summary.csv',index=False)
df[df.incomplete_cycle_flag|df.capacity_anomaly_flag].to_csv(out/'v18_quality_flagged_cycles.csv',index=False)
long=[]
for c in cols:
 med=df[c].median(); iqr=df[c].quantile(.75)-df[c].quantile(.25); long.extend([(c,float(v)) for v in ((df[c]-med)/(iqr if iqr else 1)).dropna()])
long=pd.DataFrame(long,columns=['feature','robust_z']); sns.set_theme(style='whitegrid',context='talk')
fig,ax=plt.subplots(figsize=(11,6)); sns.boxplot(data=long,x='feature',y='robust_z',color='#9ecae1',showfliers=False,ax=ax); ax.axhline(0,color='black',lw=.8); ax.set(xlabel='',ylabel='Robust scaled value (x − median) / IQR',title='State and history features on a comparable robust scale'); ax.tick_params(axis='x',rotation=25); fig.tight_layout(); fig.savefig(out/'v18_features_robust_scaled.png',dpi=240); plt.close(fig)
fig,axs=plt.subplots(2,3,figsize=(14,8)); axs=axs.ravel()
for ax,c in zip(axs,cols): sns.boxplot(y=df[c],color='#74c476',showfliers=True,ax=ax); ax.set_title(c); ax.set_xlabel(''); ax.grid(axis='y',alpha=.25)
fig.suptitle('State and history features in native physical units',y=1.02); fig.tight_layout(); fig.savefig(out/'v18_features_native_units_6panel.png',dpi=240,bbox_inches='tight'); plt.close(fig)
fig,ax=plt.subplots(figsize=(8,6)); sns.scatterplot(data=df,x='duration_s',y='capacity_ah',hue='incomplete_cycle_flag',style='capacity_anomaly_flag',palette={False:'#4c78a8',True:'#e45756'},ax=ax); ax.set(title='Short-duration cycles and capacity anomalies',xlabel='Discharge duration (s)',ylabel='Capacity (Ah)'); fig.tight_layout(); fig.savefig(out/'v18_duration_capacity_audit.png',dpi=240); plt.close(fig)
fig,ax=plt.subplots(figsize=(11,6))
for bid,g in df.groupby('battery_id'):
 g=g.sort_values('discharge_cycle_index'); ax.plot(g.discharge_cycle_index,g.capacity_ah,color='#9aa0a6',alpha=.35,lw=.8); bad=g[g.incomplete_cycle_flag|g.capacity_anomaly_flag]
 if len(bad): ax.scatter(bad.discharge_cycle_index,bad.capacity_ah,color='#d62728',s=12,zorder=3)
ax.set(xlabel='Discharge cycle',ylabel='Capacity (Ah)',title='Capacity trajectories with incomplete/anomalous cycles marked red'); fig.tight_layout(); fig.savefig(out/'v18_capacity_trajectories_quality_flags.png',dpi=240); plt.close(fig)
(out/'v18_quality_summary.txt').write_text(f"rows={len(df)}\nincomplete_cycle_flag={int(df.incomplete_cycle_flag.sum())}\ncapacity_anomaly_flag={int(df.capacity_anomaly_flag.sum())}\nobserved_eol_among_incomplete={int(df.loc[df.incomplete_cycle_flag,'observed_eol'].eq(True).sum())}\nenergy_cumulative_max_Wh={df.cumulative_energy_wh.max():.3f}\nenergy_per_cycle_max_Wh={df.energy_throughput_wh.max():.3f}\nduration_capacity_correlation={df[['duration_s','capacity_ah']].corr().iloc[0,1]:.4f}\n")
print(out)
