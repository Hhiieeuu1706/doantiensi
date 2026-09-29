from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
src = ROOT / 'archive' / 'root_cleanup' / 'outputs' / 'tables' / 'discharge_cycles_features_labels.csv'
out = ROOT / 'SUBMISSION_PACKAGE_V10' / '04_results' / 'figures' / 'v19_publication_quality'
out.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(src)
df = df[df['operation_type'].eq('discharge')].copy()
df['incomplete_cycle_flag'] = (df['duration_s'] < 500) | (df['n_samples'] < 50)
df['capacity_anomaly_flag'] = df['capacity_ah'].isna() | (df['capacity_ah'] <= 0)
df['quality_flag'] = df['incomplete_cycle_flag'] | df['capacity_anomaly_flag']
df = df.sort_values(['battery_id', 'discharge_cycle_index'])

sns.set_theme(style='whitegrid', context='paper')
plt.rcParams.update({'font.size': 10, 'axes.titlesize': 13, 'axes.labelsize': 11,
                     'legend.fontsize': 8, 'xtick.labelsize': 9, 'ytick.labelsize': 9})

# Overview: preserve all cells but remove the unreadable 50-item legend.
fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=350)
for bid, g in df.groupby('battery_id'):
    ax.plot(g['discharge_cycle_index'], g['capacity_ah'], color='#9aa0a6', alpha=0.27, lw=0.75, zorder=1)
    bad = g[g['quality_flag']]
    if not bad.empty:
        ax.scatter(bad['discharge_cycle_index'], bad['capacity_ah'], color='#d62728', s=10, alpha=.8, zorder=3)
for bid, color in [('B0005', '#1f77b4'), ('B0006', '#ff7f0e'), ('B0007', '#2ca02c'), ('B0018', '#9467bd')]:
    g = df[df['battery_id'].eq(bid)]
    if not g.empty:
        ax.plot(g['discharge_cycle_index'], g['capacity_ah'], lw=1.9, color=color, label=bid, zorder=4)
ax.set_title('Discharge-cycle capacity trajectories')
ax.set_xlabel('Discharge cycle')
ax.set_ylabel('Capacity (Ah)')
ax.legend(title='Observed NASA cells', ncol=4, loc='upper right', frameon=True)
ax.text(0.01, 0.02, 'Gray: all cells; colored: B0005/B0006/B0007/B0018; red: quality flags',
        transform=ax.transAxes, fontsize=8.5, color='#444444')
fig.tight_layout()
fig.savefig(out / 'v19_discharge_cycle_capacity_overview.png', dpi=350, bbox_inches='tight')
plt.close(fig)

# Detail: small multiples make the observed-EOL trajectories legible without a dense legend.
ids = ['B0005', 'B0006', 'B0007', 'B0018']
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4), dpi=350, sharey=True)
for ax, bid in zip(axes.flat, ids):
    g = df[df['battery_id'].eq(bid)]
    if g.empty:
        ax.set_visible(False); continue
    ax.plot(g['discharge_cycle_index'], g['capacity_ah'], color='#1f77b4', lw=1.5)
    bad = g[g['quality_flag']]
    if not bad.empty:
        ax.scatter(bad['discharge_cycle_index'], bad['capacity_ah'], color='#d62728', s=18, zorder=3, label='quality flag')
    ax.set_title(bid)
    ax.set_xlabel('Discharge cycle')
    ax.set_ylabel('Capacity (Ah)')
    ax.grid(alpha=.25)
fig.suptitle('Discharge-cycle capacity trajectories for the NASA reference cells', y=0.995, fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(out / 'v19_discharge_cycle_capacity_small_multiples.png', dpi=350, bbox_inches='tight')
plt.close(fig)

(out / 'v19_figure_note.txt').write_text(
    'The dense all-battery plot was replaced by an overview without a 50-item legend and a four-cell small-multiple detail figure. '
    'All values and quality flags are computed from the same audited discharge table; no labels or frozen metrics were changed.\n',
    encoding='utf-8')
print(out)
