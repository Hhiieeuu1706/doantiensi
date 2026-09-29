from pathlib import Path
from docx import Document
ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V26_CLEAN_MASTER_AUDITED.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V27_FINAL_AUDITED.docx'
doc=Document(src)

# Group supplementary evidence before References under one top-level heading.
paras=doc.paragraphs
refs=next(i for i,p in enumerate(paras) if p.text.strip()=='References')
first=None
for p in paras[:refs]:
    if p.style.name.startswith('Heading 1') and ('E1' in p.text or 'robustness audit' in p.text): first=p; break
if first:
    first.text='Supplementary robustness and data-quality evidence'
    for p in paras[paras.index(first)+1:refs]:
        if p.style.name.startswith('Heading 1'): p.style=doc.styles['Heading 2']

# Preserve Appendix A, then explicitly begin the extended research-history appendix.
app=next((p for p in doc.paragraphs if p.text.strip()=='Appendix B. Extended audit and research history'),None)
if app: app.text='Appendix A. Reproducibility artefacts'
q=next((p for p in doc.paragraphs if p.text.strip()=='Thesis research questions'),None)
if q:
    p=doc.add_paragraph('Appendix B. Extended audit and research history',style='Heading 1')
    q._p.addprevious(p._p)

doc.save(dst); print(dst)
