from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
src=ROOT/'archive'/'root_cleanup'/'outputs'/'tables'/'discharge_cycles_features_labels.csv'
out=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'/'figures'/'v23_quality_trajectory'
out.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(src); df=df[df.operation_type.eq('discharge')].copy()
df['quality_flag']=(df['duration_s']<500)|(df['n_samples']<50)|df['capacity_ah'].isna()|(df['capacity_ah']<=0)
fig,ax=plt.subplots(figsize=(11.2,6.0),dpi=350)
for bid,g in df.sort_values('discharge_cycle_index').groupby('battery_id'):
    ax.plot(g.discharge_cycle_index,g.capacity_ah,color='#7f8c8d',alpha=.42,lw=.85,zorder=1)
    bad=g[g.quality_flag]
    if not bad.empty: ax.scatter(bad.discharge_cycle_index,bad.capacity_ah,color='#d62728',s=15,zorder=4)
colors={'B0005':'#1f77b4','B0006':'#ff7f0e','B0007':'#2ca02c','B0018':'#9467bd'}
for bid,col in colors.items():
    g=df[df.battery_id.eq(bid)]
    if not g.empty: ax.plot(g.discharge_cycle_index,g.capacity_ah,color=col,lw=2.2,label=bid,zorder=3)
ax.set_title('Capacity trajectories and quality flags',pad=10)
ax.set_xlabel('Discharge cycle'); ax.set_ylabel('Capacity (Ah)')
ax.grid(alpha=.28); ax.legend(title='Reference cells',ncol=4,loc='upper right',frameon=True)
ax.text(.01,.02,'Gray: all cells | colored: NASA reference cells | red: incomplete/anomalous cycles',transform=ax.transAxes,fontsize=8.5,color='#333')
fig.tight_layout(); fig.savefig(out/'v23_capacity_trajectories_quality_flags.png',dpi=350,bbox_inches='tight'); plt.close(fig)
print(out/'v23_capacity_trajectories_quality_flags.png')
