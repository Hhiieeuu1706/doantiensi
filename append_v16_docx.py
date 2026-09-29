from docx import Document
from pathlib import Path
src=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V15_FINAL_AUDITED.docx'); out=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V16_FINAL_AUDITED.docx')
d=Document(src); ref=next((p for p in d.paragraphs if p.text.strip()=='References'),d.paragraphs[-1])
ref.insert_paragraph_before('V16 absolute-cycle and transfer validation').style='Heading 1'
for s in [
'To avoid treating the true EOL as an online input, absolute-cycle evaluation was added at cycles 25, 50, 75 and 100. NASA LOBO results are reported at these fixed cycle horizons in the supplementary CSV. Lifetime-normalized 20/40/60/80% results are retained as retrospective benchmark checkpoints and are labeled accordingly.',
'A NASA-only zero-shot model was evaluated on the 16-cell HUST final holdout and compared with the development-adapted estimator. Zero-shot MAE was 1618.4, 1213.9, 809.4 and 404.9 cycles at 20/40/60/80%; adapted MAE was 116.5, 116.1, 85.2 and 20.3 cycles. This quantifies adaptation benefit, but it does not constitute universal cross-domain generalization.',
'The primary uncertainty table is the target-coverage sensitivity table (80%, 90%, 95%) with coverage, interval width and normalized width. Earlier V8/V11 interval values are historical/sensitivity artefacts and are not mixed with the primary result.'
]: ref.insert_paragraph_before(s).style='Normal'
def table(headers,rows):
 t=d.add_table(rows=1,cols=len(headers)); t.style='Table Grid'
 for i,h in enumerate(headers): t.rows[0].cells[i].text=str(h)
 for row in rows:
  c=t.add_row().cells
  for i,v in enumerate(row): c[i].text=str(v)
table(['Checkpoint','NASA→HUST zero-shot MAE','Adapted HUST holdout MAE'],[['20%','1618.4','116.5'],['40%','1213.9','116.1'],['60%','809.4','85.2'],['80%','404.9','20.3']])
d.save(out); print(out)
