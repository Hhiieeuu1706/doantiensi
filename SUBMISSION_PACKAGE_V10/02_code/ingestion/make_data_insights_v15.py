from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT=Path(__file__).resolve().parent
src=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'/'discharge_cycles_features_labels.csv'
out=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'figures'/'v15_data_insights'
out.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(src)
df=df[df['operation_type'].eq('discharge')].copy()
sns.set_theme(style='whitegrid',context='talk')

fig,ax=plt.subplots(figsize=(10,6))
for bid,g in df.groupby('battery_id'):
    g=g.sort_values('discharge_cycle_index')
    ax.plot(g['discharge_cycle_index'],g['capacity_ah'],alpha=.8,label=bid)
ax.set(xlabel='Discharge cycle',ylabel='Capacity (Ah)',title='Battery capacity degradation trajectories')
ax.legend(ncol=2,fontsize=8); fig.tight_layout(); fig.savefig(out/'v15_capacity_trajectories.png',dpi=220); plt.close(fig)

cols=['capacity_ah','duration_s','voltage_drop_v','temperature_rise_c','capacity_rolling_slope_5','cumulative_energy_wh']
avail=[c for c in cols if c in df.columns]
long=df[avail].melt(var_name='feature',value_name='value').replace([float('inf'),-float('inf')],pd.NA).dropna()
fig,ax=plt.subplots(figsize=(11,6)); sns.boxplot(data=long,x='feature',y='value',ax=ax,color='#9ecae1'); ax.tick_params(axis='x',rotation=30); ax.set_title('State and history feature distributions'); fig.tight_layout(); fig.savefig(out/'v15_state_history_distributions.png',dpi=220); plt.close(fig)

num=df.select_dtypes('number').copy(); corr=num.corr(numeric_only=True)
target='rul_cycles'
if target in corr:
    top=corr[target].abs().sort_values(ascending=False).head(12).index
    fig,ax=plt.subplots(figsize=(9,7)); sns.heatmap(corr.loc[top,top],cmap='vlag',center=0,ax=ax); ax.set_title('Feature correlation screen including RUL'); fig.tight_layout(); fig.savefig(out/'v15_rul_correlation_heatmap.png',dpi=220); plt.close(fig)

if 'protocol_id' in df.columns:
    tab=df.groupby('protocol_id').agg(cells=('battery_id','nunique'),cycles=('discharge_cycle_index','count'),mean_capacity=('capacity_ah','mean'),mean_temp=('temperature_c_mean','mean')).reset_index()
    tab.to_csv(out/'v15_protocol_summary.csv',index=False)
    fig,ax=plt.subplots(figsize=(10,5)); sns.barplot(data=tab,x='protocol_id',y='mean_capacity',ax=ax,color='#74c476'); ax.tick_params(axis='x',rotation=35); ax.set_title('Mean capacity by discharge protocol'); fig.tight_layout(); fig.savefig(out/'v15_protocol_capacity.png',dpi=220); plt.close(fig)

e1=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'tables'/'supplementary'/'V14_E1_PROTOCOL_SENSITIVITY.csv'
if e1.exists():
    t=pd.read_csv(e1); fig,ax=plt.subplots(figsize=(9,5)); sns.lineplot(data=t,x='checkpoint_fraction',y='mae',hue='protocol',marker='o',ax=ax); ax.set(title='RUL MAE changes with split protocol',xlabel='Observed-life fraction',ylabel='MAE (cycles)'); fig.tight_layout(); fig.savefig(out/'v15_protocol_sensitivity.png',dpi=220); plt.close(fig)

insights=[]
if 'rul_cycles' in df: insights.append(f"rows={len(df)}; batteries={df['battery_id'].nunique()}; mean_rul={df['rul_cycles'].mean():.2f} cycles")
if 'capacity_ah' in df: insights.append(f"capacity range={df['capacity_ah'].min():.3f}–{df['capacity_ah'].max():.3f} Ah")
(out/'v15_data_insights.txt').write_text('\n'.join(insights),encoding='utf-8')
print(f'generated figures in {out}')
