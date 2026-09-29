from docx import Document
from pathlib import Path
paths=[Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V12_NOVELTY_AUDITED.docx'),Path('SUBMISSION_PACKAGE_V10/05_manuscript/BATTERY_RUL_PHD_THESIS_V12_NOVELTY_AUDITED.docx')]
for path in paths:
 d=Document(path)
 if any('V14 protocol sensitivity and uncertainty audit' in p.text for p in d.paragraphs): continue
 ref=next((p for p in d.paragraphs if p.text.strip()=='References'),d.paragraphs[-1])
 h=ref.insert_paragraph_before('V14 protocol sensitivity and uncertainty audit'); h.style='Heading 1'
 for s in [
 'A same-feature Random Forest comparison across random-cycle, fixed battery-holdout and LOBO splits shows lower apparent error under random-cycle splitting and higher error when the battery is unseen. The fixed holdout uses one battery and is descriptive; LOBO remains the primary generalization estimate. This result supports leakage control without claiming a universal effect size.',
 'Coverage–width analysis at 80%, 90% and 95% target coverage confirms the expected trade-off: higher coverage requires wider intervals, with particularly large normalized widths at early checkpoints. The uncertainty is therefore coverage-valid but not yet practically sharp.',
 'Five-seed deep-family artifacts are retained, but their convergence log uses a fixed epoch schedule rather than validation-loss plateau and patience. They remain provisional representation evidence; the manuscript does not claim universal Random Forest superiority over deep learning.'
 ]:
  p=ref.insert_paragraph_before(s); p.style='Normal'
 d.save(path)
print('updated')
