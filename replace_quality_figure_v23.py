from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V22_TABLES_PLACED_FINAL.docx'; dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V23_FIGURE_READABLE_FINAL.docx'
img=pkg/'04_results/figures/v23_quality_trajectory/v23_capacity_trajectories_quality_flags.png'
with ZipFile(src,'r') as zin, ZipFile(dst,'w',ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data=img.read_bytes() if item.filename=='word/media/image9.png' else zin.read(item.filename)
        zout.writestr(item,data)
print(dst)
