from docx import Document
from pathlib import Path
path=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V15_FINAL_AUDITED.docx')
d=Document(path)
if any('Detailed V15 robustness audit' in p.text for p in d.paragraphs): raise SystemExit('already updated')
ref=next((p for p in d.paragraphs if p.text.strip()=='References'),d.paragraphs[-1])
h=ref.insert_paragraph_before('Detailed V15 robustness audit'); h.style='Heading 1'
paras=[
'LOBO remains the primary unseen-battery protocol. Nested-LOBO is an additional pilot in which hyperparameters are selected on the inner battery folds and the outer battery remains untouched. Because NASA has only three observed-EOL batteries, nested estimates are reported descriptively with no claim of stable population-level uncertainty.',
'Protocol sensitivity was evaluated with the same Random Forest, engineered health indicators, EOL definition and checkpoints. Random-cycle splitting produced lower apparent error than battery-holdout and LOBO, demonstrating why cycle-level random splitting is not used for the primary generalization claim.',
'The fair deep-family gate remains explicit. RF/XGBoost/classical models have direct engineered-HI comparison. LSTM, GRU, TCN and Transformer have five-seed artifacts, but a final claim requires validation-loss plateau, patience and equal tuning budget on every outer fold. Until that gate is met, no universal RF-versus-deep claim is made.',
'History generalization is bounded: NASA and HUST-development analyses support checkpoint-dependent information value, not history sufficiency across all chemistries and protocols. CALCE is retained as an external feature audit; a fully harmonized CALCE RUL/EOL protocol is future work.',
'Uncertainty usefulness is evaluated through 80%, 90% and 95% coverage targets, interval width and normalized width. The result is a coverage–sharpness trade-off: early-life intervals remain wide, so operational utility is not claimed.',
'The online component is software replay/HIL only. Electrical HIL, physical BMS integration and field validation require hardware and are not represented as completed experiments.'
]
for s in paras: ref.insert_paragraph_before(s).style='Normal'
def add_table(headers,rows):
 t=d.add_table(rows=1,cols=len(headers)); t.style='Table Grid'
 for i,hdr in enumerate(headers): t.rows[0].cells[i].text=str(hdr)
 for row in rows:
  c=t.add_row().cells
  for i,v in enumerate(row): c[i].text=str(v)
 return t
ref.insert_paragraph_before('Table V15.1. Protocol sensitivity results.').style='Caption'
add_table(['Protocol','20% MAE','40% MAE','60% MAE','80% MAE'],[['Random-cycle','1.55','4.15','4.07','2.13'],['Fixed battery holdout','8.00','7.78','14.92','7.77'],['LOBO','6.27','5.97','12.29','6.78']])
ref.insert_paragraph_before('Table V15.2. Uncertainty coverage–width summary.').style='Caption'
add_table(['Target coverage','Checkpoint','Actual coverage','Interval width','Normalized width'],[['80%','20%','75.0%','294.4','0.182'],['80%','60%','93.8%','1091.8','1.349'],['90%','20%','81.3%','354.0','0.219'],['90%','60%','100%','1499.6','1.853'],['95%','20%','100%','1662.5','1.027'],['95%','60%','100%','1574.4','1.945']])
d.save(path)
print('updated',path)
