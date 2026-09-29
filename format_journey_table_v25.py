from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V24_RESEARCH_JOURNEY_FINAL.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V25_RESEARCH_JOURNEY_FINAL.docx'
doc=Document(src)
t=doc.tables[0]
t.autofit=True
for ri,row in enumerate(t.rows):
    for cell in row.cells:
        cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for p in cell.paragraphs:
            p.paragraph_format.space_after=Pt(2)
            for run in p.runs:
                run.font.size=Pt(8.5)
                if ri==0: run.bold=True
    if ri==0:
        for cell in row.cells:
            tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),'1F4E79'); tcPr.append(shd)
            for p in cell.paragraphs:
                for run in p.runs: run.font.color.rgb=__import__('docx').shared.RGBColor(255,255,255)
doc.save(dst)
print(dst)
