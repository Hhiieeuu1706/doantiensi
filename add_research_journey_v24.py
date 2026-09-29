from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_BREAK

ROOT=Path(__file__).resolve().parent
pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V23_FIGURE_READABLE_FINAL.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V24_RESEARCH_JOURNEY_FINAL.docx'

doc=Document(src)
anchor=doc.paragraphs[8]  # end of the opening introduction paragraph
els=[]

def para(text='', style='Normal'):
    p=doc.add_paragraph(style=style)
    p.add_run(text)
    els.append(p._p)
    return p

para('Research origin and decision path', 'Heading 2')
para('This study did not begin with a decision to apply a particular neural architecture. It began with a practical and scientific concern: a battery RUL model can obtain a small numerical error while still failing on an unseen battery, an unseen operating protocol, or a battery whose end of life is not observed. The initial project direction therefore combined two goals that are often separated in the literature: understand what the measurements reveal about degradation, and build an estimator that remains auditable when it is exposed to new cells and new protocols.')
para('The starting hypothesis was deliberately modest. Cycle count alone should not be treated as battery age, because two cells at the same cycle index can have different capacity, voltage, temperature, duration and accumulated operating history. The first task was consequently not model selection. It was to determine whether the data were sufficiently well defined to support a defensible RUL target, and whether state and history variables contained information beyond cycle count.')

para('Research questions and intended direction', 'Heading 3')
para('The work was organized around four questions. (1) What is a valid, reproducible unit of observation: charge, discharge, EIS, cycle, or partial cycle? (2) Which health indicators carry information about degradation, and does history add information beyond current state? (3) Which estimator is reliable when the held-out battery has never appeared in training? (4) Can the estimator produce sequential predictions with uncertainty without using future cycles? These questions led to an eight-step research route: data audit; aging insight; health-indicator screening; EOL/RUL definition; model ladder; battery-level generalization; online adaptive replay; and prototype packaging.')
para('The route was intentionally evidence-first. A model was allowed to become the selected estimator only after the information schema, label rule, split protocol and evaluation checkpoints had been locked. This is why the final work is positioned as an integrated evaluation-and-estimation framework rather than as a claim that a new architecture has been invented.')

para('What was done and why each decision was made', 'Heading 3')
para('The execution followed the research route in stages. First, NASA records were normalized into cycle-level discharge observations with voltage, current, temperature, time, duration, capacity and derived history indicators. Duplicate records, anomalies, incomplete cycles and the censored B0007 cell were audited rather than silently converted into artificial RUL labels. Second, degradation trajectories and feature distributions were inspected to identify voltage/current/temperature summaries, duration, energy throughput, capacity state and rolling history as candidate indicators. Third, SOH and RUL ablations were used to test whether cycle-only, current-state-only, history-only and state-plus-history inputs behaved differently at 20%, 40%, 60% and 80% observation.')
para('The ground truth was then fixed before model comparison. Primary EOL is the first of two consecutive cycles below 75% of the median capacity in the first five cycles, and RUL(k) = N_EOL - k. Censored batteries are excluded from point-RUL accuracy rather than assigned a fabricated EOL. The model ladder compared linear and robust trajectories, Gaussian-process/trajectory alternatives, Random Forest, XGBoost and an ensemble under battery-level LOBO. This ordering matters: it lets the data determine whether a complex model is justified instead of assuming that a larger model is scientifically superior.')
para('The NASA results were followed by external HUST validation. HUST was separated into development, calibration and final untouched cells; the final set was not used for feature selection or tuning. Both zero-shot transfer and development-only adaptation were reported, because the very large zero-shot error is itself evidence of domain shift rather than a result that should be hidden. Sequential RF replay was then added so that each prediction uses only data available up to the current cycle. Finally, E1-E11 audits were added to test protocol sensitivity, ranking stability, model-family fairness, history generalization, uncertainty, EOL sensitivity, external validation, leakage, sequential replay and literature comparability.')

para('Decision log: limitations encountered and resulting choices', 'Heading 3')
table=doc.add_table(rows=1, cols=4)
table.style='Table Grid'
hdr=table.rows[0].cells
for c,t in zip(hdr,['Observed limitation','Why it matters','Decision taken','Claim boundary']): c.text=t
rows=[
('NASA is heterogeneous and B0007 is censored','A false EOL would contaminate every RUL metric','Audit operations, preserve censoring, exclude B0007 from point-RUL metrics','No claim that every NASA cell has observed EOL'),
('Only three NASA cells have observed EOL','Bootstrap intervals and history conclusions have high sampling uncertainty','Report per-cell results and bootstrap intervals','History is checkpoint-dependent, not universal'),
('Random cycle splits can leak battery identity','They can make RUL look easier than unseen-cell prediction','Use battery holdout and LOBO as primary evidence; retain random split only as sensitivity','No random-split SOTA claim'),
('NASA to HUST protocol/chemistry shift is large','A shared feature schema is not automatically domain invariant','Report zero-shot separately from development-only adaptation','No universal zero-shot generalization claim'),
('Conformal coverage is high but intervals are wide','Coverage alone does not establish operational usefulness','Report 80/90/95% coverage together with width and normalized width','Uncertainty is coverage-valid but not yet sharp'),
('Deep-model convergence/tuning records are incomplete','Different optimization budgets would make the comparison unfair','Keep deep-family results conditional and separate from the RF leaderboard','No claim that RF beats all deep learning'),
('Partial-cycle API, electrical HIL and BMS hardware are incomplete','Offline replay is not the same as field deployment','Describe software replay as validated and hardware integration as future work','Prototype, not production-ready BMS'),
('Published studies use incompatible splits and horizons','Raw metric ranking would be misleading','Use a protocol-comparison matrix instead of numerical SOTA ranking','Methodological advantage, not numerical SOTA')]
for row in rows:
    cells=table.add_row().cells
    for c,t in zip(cells,row): c.text=t
els.append(table._tbl)

para('How to read the rest of the thesis', 'Heading 3')
para('The remainder of the document should be read as a chain of controlled decisions. Sections 2-4 establish the literature, data contract and integrated framework. Sections 5-8 show how the protocol, state/history inputs and model ladder were tested. Sections 9-11 test external-domain behavior, uncertainty and sequential replay. The discussion and limitations then separate what is demonstrated from what remains a future experiment. In particular, the selected Random Forest is the best estimator among the evaluated models under the locked protocol; it is not presented as a universally superior algorithm. The central contribution is the evidence-producing workflow that makes this statement, and its uncertainty, reproducible.')

# insert in desired order after the introduction paragraph
for el in reversed(els):
    anchor._p.addnext(el)

doc.save(dst)
print(dst)
