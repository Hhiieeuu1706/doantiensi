from docx import Document
from pathlib import Path
src=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V17_CONSISTENT.docx'); out=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V17_FINAL.docx')
d=Document(src)
for p in d.paragraphs:
    if 'Threshold sensitivity at 70% and 80% remains required' in p.text:
        p.text=p.text.replace('Threshold sensitivity at 70% and 80% remains required.','Threshold sensitivity at 70%, 75% and 80% has been audited; 75% remains the registered primary operational threshold.')
    if 'Future work must prioritize fair model-family comparison, EOL sensitivity, RF online replay' in p.text:
        p.text='Future work must prioritize final fair model-family convergence, sharper uncertainty, CALCE RUL harmonization and hardware validation; RF sequential replay has already been executed as software evidence.'
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            if c.text.strip()=='Cycle count is weaker under this NASA LOBO ablation': c.text='Cycle-only is generally weaker, but not uniformly at every checkpoint.'
d.save(out); print(out)
