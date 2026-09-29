from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V25_RESEARCH_JOURNEY_FINAL.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V26_CLEAN_MASTER_AUDITED.docx'
doc=Document(src)

def add_after(anchor, elements):
    for el in reversed(elements): anchor._p.addnext(el)

def make_p(text='', style='Normal'):
    p=doc.add_paragraph(style=style); p.add_run(text); return p

# Add an explicit literature-to-design bridge after the existing Related Work paragraph.
rel_para=next(p for p in doc.paragraphs if p.text.startswith('Prior battery prognostics use recurrent networks'))
els=[]
p=make_p('From literature corpus to research design','Heading 2'); els.append(p._p)
p=make_p('The supplied literature was read as a design space rather than as a leaderboard. The papers cover trajectory and particle-filter methods, Gaussian processes, recurrent and convolutional sequence models, feature-learning and ANFIS approaches, hybrid digital twins, transfer learning, and uncertainty-aware RUL estimation. Across this corpus, the recurring scientific weakness is not the absence of models; it is the lack of a common information boundary. Studies often differ in battery split, observation horizon, EOL threshold, adaptation rule and metric, so a lower published error cannot automatically establish better generalization.'); els.append(p._p)
p=make_p('The literature therefore led to four design decisions. First, the unit of comparison must be a battery-level holdout, with LOBO as the primary unseen-cell test. Second, the input schema must separate current state from operating history so that the value of history can be tested rather than assumed. Third, external validation must separate development, calibration and final untouched cells. Fourth, uncertainty must be reported jointly with coverage and width. These decisions are the bridge between the reviewed PDFs and the experiments reported in this thesis.'); els.append(p._p)
p=make_p('Literature-to-design mapping','Heading 3'); els.append(p._p)
t=doc.add_table(rows=1,cols=4); t.style='Table Grid';
for c,txt in zip(t.rows[0].cells,['Literature pattern','Limitation for a strong claim','Design response in this thesis','Evidence location']): c.text=txt
rows=[
('Trajectory, PF and GP prognostics','Useful dynamics/uncertainty, but often evaluated within one battery or protocol','Keep trajectory/GP baselines in the same engineered-HI LOBO ladder','Sections 5 and 7'),
('LSTM/GRU/TCN and deep feature learning','High capacity, but split and tuning budgets are not consistently comparable','Run a separate fair-family comparison and state the evidence boundary','Sections 7 and 14'),
('HUST transfer-learning studies','External cells are valuable, but adaptation and horizons differ across papers','Freeze 46/15/16 HUST roles and report zero-shot versus development-only adaptation','Section 9'),
('Hybrid, ANFIS and digital-twin methods','Interpretability/physics are attractive, but assumptions may be protocol-specific','Treat interpretability as motivation while testing a fixed data contract and protocol sensitivity','Sections 3, 5 and E1'),
('Published benchmark tables','Raw MAE/RMSE is not comparable across EOL, horizon and split definitions','Use a protocol-comparison matrix and avoid numerical SOTA claims','Section 8 and E11')]
for row in rows:
 cells=t.add_row().cells
 for c,txt in zip(cells,row): c.text=txt
for ri,row in enumerate(t.rows):
 for cell in row.cells:
  cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
  for p in cell.paragraphs:
   p.paragraph_format.space_after=Pt(2)
   for r in p.runs:
    r.font.size=Pt(8.5)
    if ri==0: r.bold=True; r.font.color.rgb=RGBColor(255,255,255)
 if ri==0:
  for cell in row.cells:
   shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),'1F4E79'); cell._tc.get_or_add_tcPr().append(shd)
els.append(t._tbl)
add_after(rel_para,els)

# Convert post-References accumulated audit material into a clearly labelled appendix.
paras=doc.paragraphs
ref_i=next(i for i,p in enumerate(paras) if p.text.strip()=='References')
post=[p for p in paras[ref_i+1:] if p.text.strip()]
first_heading=next((p for p in post if p.style.name.startswith('Heading')),None)
if first_heading:
    first_heading.text='Appendix B. Extended audit and research history'
    first_heading.style=doc.styles['Heading 1']
    seen_first=False
    for p in post:
        if p is first_heading: seen_first=True; continue
        if seen_first and p.style.name.startswith('Heading'):
            p.style=doc.styles['Heading 2']
            if p.text.startswith('Chapter '): p.text='Audit note: '+p.text

doc.save(dst)
print(dst)
