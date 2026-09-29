from docx import Document
from docx.shared import Inches
from pathlib import Path
src=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V17_FINAL.docx'); out=Path('06_manuscript/BATTERY_RUL_PHD_THESIS_V18_DATA_QUALITY_FINAL.docx'); d=Document(src)
ref=next((p for p in d.paragraphs if p.text.strip()=='References'),d.paragraphs[-1])
ref.insert_paragraph_before('Data quality audit and scale-aware visualization').style='Heading 1'
for s in ['The original combined boxplot was replaced because the six variables have incompatible physical units. The thesis now uses both native-unit panels and robust-scaled distributions. Duration is strongly associated with sample count and short-duration cycles are inspected separately rather than interpreted as ordinary degradation.', 'The audit flagged 38 incomplete cycles using duration below 500 s or fewer than 50 samples, plus 44 missing/non-positive capacity records. None of the incomplete cycles carried an observed-EOL label in the current NASA table, so the registered EOL labels are unchanged. Cumulative energy reaches 1158.15 Wh while per-cycle energy reaches 10.07 Wh, supporting the interpretation that the cumulative-energy feature is a lifetime sum rather than a per-cycle quantity.']:
 ref.insert_paragraph_before(s).style='Normal'
figdir=Path('SUBMISSION_PACKAGE_V10/04_results/figures/v18_data_quality')
for name,cap in [('v18_features_robust_scaled.png','Figure V18.1. Robust-scaled state and history feature distributions.'),('v18_features_native_units_6panel.png','Figure V18.2. Native-unit feature distributions in six panels.'),('v18_duration_capacity_audit.png','Figure V18.3. Duration–capacity quality audit.'),('v18_capacity_trajectories_quality_flags.png','Figure V18.4. Capacity trajectories with flagged incomplete/anomalous cycles.')]:
 img=figdir/name
 if img.exists():
  p=ref.insert_paragraph_before(); p.alignment=1; p.add_run().add_picture(str(img),width=Inches(5.8)); c=ref.insert_paragraph_before(cap); c.alignment=1
d.save(out); print(out)
