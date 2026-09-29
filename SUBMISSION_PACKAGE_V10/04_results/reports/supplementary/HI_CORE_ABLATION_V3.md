# HI core v3 ablation

Fixed Random Forest, 10 seeds, battery-level LOBO and locked 20/40/60/80% prefixes. All imputers are fitted inside each training fold.

Core acceptance requires capacity MAE no worse than 5% versus extended v2 and at least 10% better than cycle-only.

- Core MAE: 0.02142 Ah
- Extended MAE: 0.02099 Ah
- Cycle-only MAE: 0.06989 Ah
- Core degradation versus extended: 2.0%
- Core improvement versus cycle-only: 69.3%
- Decision: **PASS**

```csv
feature_set,feature_count,capacity_mae,soh_mae,worst_case_mae,core_acceptance
core_minus_current,13,0.02011324872231875,0.010349451965745538,0.07999087657956211,
core_minus_history,8,0.02194502659866899,0.011304987593675538,0.08333731111437458,
core_minus_temperature,12,0.02131585749955341,0.010992224208880089,0.07907794137312132,
cycle_only,1,0.069885419596281,0.036786514834013614,0.12101815186398193,
hi_core_v3,14,0.021420149214727142,0.01104224539081297,0.0804321591721578,PASS
hi_extended_v2,17,0.02099254315145676,0.010815664830975213,0.08109977248591423,
history_only,6,0.029101510516364653,0.015132440328343474,0.08621593385839348,

```
