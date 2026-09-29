from docx import Document
from pathlib import Path
src=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V16_FINAL_AUDITED.docx'); out=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V17_CONSISTENT.docx')
d=Document(src)
repls={
'Cycle-only is consistently weaker than state-only. History-only is informative but unstable. State plus history is slightly worse than state-only at 20–40% and better at 60–80%; therefore the evidence supports conditional, checkpoint-dependent history information, not an “history is essential” claim.':'Cycle-only is generally weaker than state-only, but not at every checkpoint: at 60% cycle-only MAE is 14.47 versus 15.19 for state-only. History-only is informative but unstable. State plus history is slightly worse than state-only at 20–40% and better at 60–80%; therefore the evidence supports conditional, checkpoint-dependent information value, not an “history is essential” claim.',
'Finite-sample conformal calibration achieved 100% empirical coverage on the frozen final predictions. This coverage is conservative: interval widths were approximately 831, 684, 787 and 363 cycles at 20%, 40%, 60% and 80% checkpoints. Accordingly, uncertainty is coverage-valid but not sharp enough for production decisions; early-life uncertainty remains the principal bottleneck.':'The primary uncertainty result is the target-coverage sensitivity table reporting 80%, 90% and 95% target coverage together with actual coverage, interval width and normalized width. On the 16-cell frozen set, nominal-or-higher empirical coverage is obtained at several targets, but widths remain large, especially at early checkpoints. The result is coverage evidence on this finite holdout, not population-level calibration or production-ready sharpness.',
'Conformal coverage is 100%, but widths are approximately 831, 684, 787 and 363 cycles across checkpoints. Coverage alone is not excellent uncertainty; early-life sharpness is the main bottleneck.':'The primary uncertainty table reports target coverage at 80%, 90% and 95%, actual coverage, interval width and normalized width. Coverage is interpreted jointly with sharpness; early-life intervals remain wide and therefore operational utility is not claimed.',
'RF cycle-level intervals were calibrated from the independent HUST calibration subset using checkpoint-conditioned absolute residual quantiles. The resulting widths are approximately 1043, 648, 349 and 220 cycles for 20%, 40%, 60% and 80% observation fractions. These intervals do not alter frozen V8 point metrics.':'Earlier V8/V11 cycle-level interval widths are retained as historical sensitivity artefacts. The primary uncertainty result is the 80/90/95% target-coverage table, which does not alter frozen V8 point metrics.',
'Threshold sensitivity at 70% and 80% remains required.':'Threshold sensitivity at 70%, 75% and 80% has been audited; 75% remains the registered primary operational threshold.',
'Future work must prioritize fair model-family comparison, EOL sensitivity, RF online replay, sharper uncertainty and publisher-verified benchmarks before defense or submission.':'Future work must prioritize final fair model-family convergence, sharper uncertainty, CALCE RUL harmonization and hardware validation; RF sequential replay has already been executed as software evidence.'}
for p in d.paragraphs:
    old=p.text
    if old in repls:
        for r in p.runs: r.text=''
        p.add_run(repls[old])
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            if 'Cycle-only RUL MAE is higher than state-only at all four checkpoints' in cell.text: cell.text='Cycle-only is weaker overall, but not at every checkpoint; at 60% it is slightly better than state-only.'
            if cell.text.strip()=='Coverage-valid but not sharp enough for production': cell.text='Empirical coverage is reported with wide intervals; sharpness remains limited.'
ref=next((p for p in d.paragraphs if p.text.strip()=='References'),d.paragraphs[-1])
cap=ref.insert_paragraph_before('Table V17.1. Absolute-cycle NASA LOBO evaluation.'); cap.style='Caption'
t=d.add_table(rows=1,cols=4); t.style='Table Grid'
for i,h in enumerate(['Absolute cycle','MAE (cycles)','RMSE (cycles)','Eligible batteries']): t.rows[0].cells[i].text=h
for row in [('25','9.98','9.99','3'),('50','10.36','11.01','3'),('75','9.46','11.09','3'),('100','5.59','7.21','3')]:
    c=t.add_row().cells
    for i,v in enumerate(row): c[i].text=v
ref._p.addprevious(t._tbl)
disc=ref.insert_paragraph_before('The zero-shot transfer result is substantively important. A NASA-only model produced HUST final-holdout MAE of 1618.4, 1213.9, 809.4 and 404.9 cycles at 20–80% retrospective checkpoints, whereas development-adapted performance was 116.5, 116.1, 85.2 and 20.3 cycles. This indicates severe domain shift under the current shared feature, chemistry and protocol mismatch, and shows that most usable performance in this setup comes from target-domain development adaptation. It is evidence against naive zero-shot transfer, not evidence of universal adaptation success.')
disc.style='Normal'
d.save(out); print(out)
