from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V27_FINAL_AUDITED.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V28_READER_GUIDE_FINAL.docx'
doc=Document(src)

def add_after(anchor, elements):
    for el in reversed(elements): anchor._p.addnext(el)

def p(text='',style='Normal'):
    q=doc.add_paragraph(style=style); q.add_run(text); return q

anchor=next(x for x in doc.paragraphs if x.text.startswith('Keywords:'))
els=[]
q=p('Reader guide: what this thesis does','Heading 1'); els.append(q._p)
q=p('In one paragraph: this thesis asks whether battery RUL prediction remains credible when the test battery is unseen, the operating protocol changes, future cycles are hidden, and uncertainty is reported honestly. The answer is established through a locked data contract, state/history health indicators, battery-level LOBO model selection, development-only external adaptation, calibration-only uncertainty and chronological replay. The selected Random Forest is the best model among those evaluated under this protocol; the contribution is the auditable evidence-producing framework, not a new learning algorithm.'); els.append(q._p)
q=p('How to read the workflow','Heading 2'); els.append(q._p)
q=p('The complete workflow is: raw V/I/T/time audit -> cycle-level health indicators -> EOL and censoring labels -> battery-level split -> LOBO model ladder -> HUST development-only adaptation -> calibration on a separate subset -> untouched external evaluation -> chronological online replay. Each arrow is a decision gate: later results are not allowed to revise an earlier locked definition.'); els.append(q._p)
q=p('Key terms for first-time readers','Heading 2'); els.append(q._p)
t=doc.add_table(rows=1,cols=2); t.style='Table Grid'; t.rows[0].cells[0].text='Term'; t.rows[0].cells[1].text='Plain-language meaning'
terms=[
('SOH','State of health: the current condition of a battery, usually capacity relative to its initial reference.'),
('RUL','Remaining useful life: the number of cycles left until the defined end-of-life threshold.'),
('HI','Health indicator: a measured or derived variable that carries information about degradation.'),
('EOL','End of life: the operational threshold used to define when a battery has failed for this study.'),
('LOBO','Leave-one-battery-out: train on batteries except one, then test on that unseen battery.'),
('Censored battery','A battery whose trajectory does not show the defined EOL crossing; it is not assigned a fake RUL label.'),
('Zero-shot / adaptation','Zero-shot applies the source model directly; adaptation allows development-domain data to recalibrate or refit it.'),
('Conformal interval','A prediction interval calibrated to achieve a target empirical coverage; width is also reported because coverage alone can be uninformative.')]
for a,b in terms:
 cells=t.add_row().cells; cells[0].text=a; cells[1].text=b
els.append(t._tbl)
q=p('Four questions and the answers supported by the experiments','Heading 2'); els.append(q._p)
t2=doc.add_table(rows=1,cols=2); t2.style='Table Grid'; t2.rows[0].cells[0].text='Question'; t2.rows[0].cells[1].text='Answer supported by this thesis'
qa=[
('Does cycle count alone describe battery age?','Not reliably. Current state is generally stronger, although cycle-only is slightly better at one checkpoint; the conclusion is not an absolute ranking at every horizon.'),
('Does operating history always improve RUL?','No. History is informative but checkpoint-dependent: it can hurt early prediction and help later prediction.'),
('Does the selected model generalize?','RF is best among evaluated models under the locked NASA LOBO protocol, and HUST performance improves with development-only adaptation and longer observation.'),
('Is the estimator ready for deployment?','It is a research prototype with chronological replay and calibrated coverage analysis. Intervals remain wide, and electrical HIL/BMS validation is still future work.')]
for a,b in qa:
 cells=t2.add_row().cells; cells[0].text=a; cells[1].text=b
els.append(t2._tbl)
q=p('A simple online example','Heading 2'); els.append(q._p)
q=p('At cycle 30, the estimator uses only data through cycle 30 and returns an RUL estimate with an interval. At cycle 31, the new measurement is appended and the estimate is recalculated; no future cycle is used. The online question is therefore not “what is the single best number?”, but “does the estimate become more accurate and more informative as the observed trajectory grows?”'); els.append(q._p)

def style_table(tbl):
 for ri,row in enumerate(tbl.rows):
  for cell in row.cells:
   cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for pp in cell.paragraphs:
    pp.paragraph_format.space_after=Pt(2)
    for run in pp.runs:
     run.font.size=Pt(8.5)
     if ri==0:
      run.bold=True; run.font.color.rgb=RGBColor(255,255,255)
  if ri==0:
   for cell in row.cells:
    shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),'1F4E79'); cell._tc.get_or_add_tcPr().append(shd)
style_table(t); style_table(t2)
add_after(anchor,els)
doc.save(dst); print(dst)
