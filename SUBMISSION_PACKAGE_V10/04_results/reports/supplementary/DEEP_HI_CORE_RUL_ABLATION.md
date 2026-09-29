# Deep HI-core RUL ablation

TCN, 10 seeds, locked LOBO. RUL-specific core v3.1 adds current-cycle SOH, which is available only after cycle completion. Core MAE 9.741; extended 10.881; cycle-only 13.648. Core vs extended change -10.5%; improvement vs cycle-only 28.6%. Decision **PASS**. This is a post-ablation availability correction and requires confirmation on an untouched external family.

```csv
feature_set,feature_count,rul_mae,worst_case,core_acceptance
cycle_only,1,13.648349631081024,24.203250351548192,
hi_core_rul_v3p1,15,9.740825412298245,20.0533826649189,PASS
hi_extended_v2,13,10.880923858315995,18.27012058496475,
history_only,6,11.59525482474516,24.040776190161708,

```
