from docx import Document
from pathlib import Path

paths=[Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V12_NOVELTY_AUDITED.docx'),Path('SUBMISSION_PACKAGE_V10/05_manuscript/BATTERY_RUL_PHD_THESIS_V12_NOVELTY_AUDITED.docx')]
heading='E1–E11 robustness audit and evidence boundary'
paras=[
'The complete robustness audit is supplied in V13_COMPLETE_E1_E11_AUDIT.md and the supplementary result tables. Protocol sensitivity, model-ranking stability, state/history ablation, bootstrap uncertainty, leakage audit, EOL sensitivity and protocol comparison are now documented as separate checks. RF/XGBoost and classical models share the engineered-HI protocol; deep sequence models remain a separate representation experiment until equal convergence and tuning records are accepted.',
'These additions strengthen the methodological contribution but do not change its scope. The evidence supports an auditable leakage-controlled framework, not a new learning algorithm, numerical SOTA claim, universal history sufficiency claim, production BMS readiness claim or universal RF superiority over deep learning. Uncertainty coverage is reported jointly with interval width and remains conservative, especially at early checkpoints.'
]
for path in paths:
    d=Document(path)
    # avoid duplicate insertion
    if any(heading in p.text for p in d.paragraphs): continue
    ref=next((p for p in d.paragraphs if p.text.strip()=='References'),None)
    if ref is None: ref=d.paragraphs[-1]
    hp=ref.insert_paragraph_before(heading); hp.style='Heading 1'
    for s in paras:
        p=ref.insert_paragraph_before(s); p.style='Normal'
    d.save(path)
print('updated')
