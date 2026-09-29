# V15 seven priority workstreams

| Workstream | Result | Status |
|---|---|---|
| Protocol sensitivity | Same engineered-HI RF compared under random-cycle, fixed battery holdout and LOBO; random-cycle appears optimistic and LOBO exposes unseen-cell error. | Evidence added; fixed holdout is descriptive (one cell). |
| Multi-domain validation | NASA development and HUST external holdout are preserved; CALCE features are available but no locked RUL/EOL protocol is claimed. | HUST complete; CALCE future extension. |
| Nested/repeated validation | Nested-LOBO pilot with inner leaf-size selection is recorded in `V15_NESTED_LOBO.csv`. | Pilot only because NASA has three observed-EOL cells. |
| Fair model-family comparison | RF/XGBoost/classical direct comparison; deep models have five-seed artefacts. | Deep convergence/tuning gate remains open. |
| History significance | State/history ablations and paired statistical artefacts are included. | History effect remains checkpoint-dependent, not universal. |
| Decision-oriented uncertainty | 80/90/95% coverage-width and normalized-width tables are included. | Coverage–sharpness trade-off is quantified; early intervals remain wide. |
| Sequential/online evidence | RF chronological replay with intervals is included. | Supporting software evidence; no electrical HIL or physical BMS. |

## Overall claim

The strengthened evidence supports an auditable, leakage-controlled evaluation-and-estimation framework. It does not support claims of a new learning algorithm, numerical SOTA, universal RF superiority, universal history sufficiency or production readiness.
