from docx import Document
from docx.shared import Inches
from pathlib import Path
paths=[Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V12_NOVELTY_AUDITED.docx'),Path('SUBMISSION_PACKAGE_V10/05_manuscript/BATTERY_RUL_PHD_THESIS_V12_NOVELTY_AUDITED.docx')]
figdir=Path('SUBMISSION_PACKAGE_V10/04_results/figures/v15_data_insights')
for path in paths:
 d=Document(path)
 if any('Data-derived figures and reproducible insight generation' in p.text for p in d.paragraphs): continue
 ref=next((p for p in d.paragraphs if p.text.strip()=='References'),d.paragraphs[-1])
 h=ref.insert_paragraph_before('Data-derived figures and reproducible insight generation'); h.style='Heading 1'
 p=ref.insert_paragraph_before('The accompanying script make_data_insights_v15.py reads the canonical discharge-cycle feature table and generates capacity trajectories, state/history distributions, RUL correlation screening, protocol summaries and protocol-sensitivity plots. These figures are descriptive evidence for feature interpretation; they do not replace battery-level validation or causal analysis.')
 p.style='Normal'
 for name,caption in [('v15_capacity_trajectories.png','Figure V15.1. Capacity degradation trajectories.'),('v15_state_history_distributions.png','Figure V15.2. State and history feature distributions.'),('v15_protocol_sensitivity.png','Figure V15.3. RUL error under alternative split protocols.')]:
  img=figdir/name
  if img.exists():
   q=ref.insert_paragraph_before(); q.alignment=1; q.add_run().add_picture(str(img),width=Inches(5.8))
   c=ref.insert_paragraph_before(caption); c.alignment=1
 d.save(path)
print('updated')
