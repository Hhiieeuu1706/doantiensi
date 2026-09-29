from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
src = ROOT / 'archive' / 'root_cleanup' / 'outputs' / 'tables' / 'discharge_cycles_features_labels.csv'
out = ROOT / 'SUBMISSION_PACKAGE_V10' / '04_results' / 'figures' / 'v21_grouped_features'
out.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(src)
df = df[df.operation_type.eq('discharge')].copy()
groups = {
    'State / physical': ['capacity_ah', 'duration_s', 'voltage_drop_v', 'temperature_rise_c'],
    'History': ['capacity_rolling_slope_5', 'cumulative_energy_wh'],
}
sns.set_theme(style='whitegrid', context='paper')
fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), dpi=350)
for ax, (title, cols) in zip(axes, groups.items()):
    vals=[]
    labels=[]
    for c in cols:
        if c not in df: continue
        x=df[c].dropna(); med=x.median(); iqr=x.quantile(.75)-x.quantile(.25)
        vals.append(((x-med)/(iqr if iqr else 1)).to_numpy()); labels.append(c)
    ax.boxplot(vals, tick_labels=labels, showfliers=True, patch_artist=True,
               boxprops={'facecolor':'#9ecae1','edgecolor':'#3182bd'},
               medianprops={'color':'#08519c','linewidth':1.3},
               whiskerprops={'color':'#636363'}, capprops={'color':'#636363'},
               flierprops={'marker':'o','markersize':2.5,'markerfacecolor':'#636363','alpha':.4})
    ax.axhline(0,color='black',lw=.7); ax.set_title(title); ax.set_ylabel('Robust scaled value')
    ax.tick_params(axis='x', rotation=30); ax.grid(axis='y',alpha=.25)
fig.suptitle('Grouped state and history feature distributions', y=1.01, fontsize=14)
fig.text(.5,-.02,'Each feature is centered by its median and scaled by its IQR; native-unit panels are reported in Figure V18.2.',ha='center',fontsize=8.5)
fig.tight_layout()
fig.savefig(out/'v21_grouped_state_history_robust.png',dpi=350,bbox_inches='tight')
plt.close(fig)
print(out/'v21_grouped_state_history_robust.png')
