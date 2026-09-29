from pathlib import Path
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V28_VIETNAMESE_FINAL.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V28_VIETNAMESE_FINAL.docx'
doc=Document(src)
doc.add_heading('Hình minh họa chính',1)
items=[
 (pkg/'04_results/figures/fig_model_ladder_lobo.png','Hình 1. So sánh model ladder theo protocol LOBO.'),
 (pkg/'04_results/figures/fig_final_mae_ci.png','Hình 2. MAE RUL trên HUST final untouched với khoảng bootstrap.'),
 (pkg/'04_results/figures/v21_grouped_features/v21_grouped_state_history_robust.png','Hình 3. Phân phối feature state/history sau robust scaling.'),
 (pkg/'04_results/figures/v23_quality_trajectory/v23_capacity_trajectories_quality_flags.png','Hình 4. Trajectory capacity và các cycle bị gắn quality flag.')]
for path,cap in items:
 p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(path),width=Inches(6.0))
 q=doc.add_paragraph(cap); q.alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.save(dst)
print(dst)
