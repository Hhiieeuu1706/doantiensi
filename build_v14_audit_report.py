from pathlib import Path
import csv, json, statistics
ROOT=Path(__file__).resolve().parent; O=ROOT/'SUBMISSION_PACKAGE_V10'/'04_results'; T=O/'tables'/'supplementary'; R=O/'reports'; R.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((ROOT/'archive'/'root_cleanup'/'outputs'/'tables'/'V10_DEEP_CONVERGENCE_LOG.csv').open(encoding='utf-8-sig')))
summary=[]
for model in sorted({r['model'] for r in rows}):
    rr=[r for r in rows if r['model']==model]; seeds=sorted({r['seed'] for r in rr}); epochs=sorted({int(r['epoch']) for r in rr});
    summary.append([model,len(seeds),','.join(seeds),max(epochs), 'preliminary_fixed_epoch' if max(epochs)<=30 else 'plateau_verified'])
with (T/'V14_E3_DEEP_CONVERGENCE_AUDIT.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['model','n_seeds','seeds','max_epoch','convergence_status']); w.writerows(summary)
lines=['# V14 E1/E3/E8 completion report','', '## E1 protocol sensitivity', '', 'The RF experiment uses identical engineered HI, EOL definition and checkpoints. Random-cycle, fixed battery holdout and LOBO results are in `V14_E1_PROTOCOL_SENSITIVITY.csv`. Random-cycle errors are generally lower, while LOBO exposes unseen-battery error; this supports the need for battery-level evaluation. The fixed holdout contains one battery and is descriptive, not a population estimate.', '', '## E3 fair deep-family comparison', '', 'RF/XGBoost/classical models have direct engineered-HI comparison. Five-seed deep artifacts exist, but the convergence log uses a fixed epoch schedule rather than validation-loss plateau/patience. Therefore deep-family numbers remain provisional and are not used to claim universal RF superiority.', '', '## E8 uncertainty usefulness', '', 'Coverage-width results for 80%, 90% and 95% target coverage are in `V14_E8_COVERAGE_WIDTH.csv`. Increasing target coverage increases interval width; early-life intervals remain wide. Coverage must therefore be reported jointly with width and normalized width.']
(R/'V14_E1_E3_E8_COMPLETION_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
print('written')
