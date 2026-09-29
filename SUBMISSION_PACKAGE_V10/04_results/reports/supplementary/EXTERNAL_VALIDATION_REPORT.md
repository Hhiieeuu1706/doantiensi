# External validation report — CALCE CS2

## Decision

**External validation is scientifically complete, but the model is not accepted for cross-domain deployment.** The locked NASA model does not generalize zero-shot to CALCE. Checkpoint-wise LOBO calibration substantially reduces error, especially at 60–80% life, but uncertainty coverage remains below the 80% acceptance floor. Fine-tuning is unstable and also fails coverage.

## Dataset and leakage control

- Source: official CALCE Battery Research Group dataset page: https://web.calce.umd.edu/batteries/data/
- Batteries: CS2_35, CS2_36, CS2_37, CS2_38; 4 cells, 3921 parsed discharge cycles.
- Chemistry/rating: LiCoO2, nominal 1.1 Ah as documented by CALCE.
- EOL: first of two consecutive cycles below 75% of the median capacity of the first five valid cycles.
- Observed EOL cycles: CS2_35=649, CS2_36=545, CS2_37=645, CS2_38=692.
- All calibration and fine-tuning are leave-one-battery-out. The held-out battery never contributes to its own scaling, fitting, or interval estimate.

## Aggregate results

| Stage | Mean RUL MAE (cycles) | Mean coverage |
|---|---:|---:|
| checkpoint_calibration | 43.26 | 68.8% |
| calibration_only | 66.01 | 50.0% |
| zero_shot | 169.07 | 25.0% |
| fine_tuned_lobo | 199.43 | 18.8% |
| external_classical | 236.77 | 0.0% |


## Checkpoint-wise calibration result

| Observed life | RUL MAE | Coverage | Mean 90% interval width |
|---:|---:|---:|---:|
| 20% | 85.13 | 75.0% | 299.51 |
| 40% | 50.25 | 75.0% | 127.91 |
| 60% | 22.34 | 75.0% | 72.65 |
| 80% | 15.32 | 50.0% | 34.85 |


## Acceptance gates

- Checkpoint calibration improves mean MAE versus zero-shot by 74.4%: **PASS**.
- Checkpoint calibration mean coverage is 68.8% versus required 80%: **FAIL**.
- Fine-tuning improves mean MAE versus the external classical baseline by 15.8% and beats it at 3/4 checkpoints, but coverage is 18.8%: **FAIL**.
- Overall release decision: **REJECT for deployment; retain as external-validation evidence and domain-adaptation baseline.**

## Interpretation

The primary domain shift is structural: NASA cells are approximately 2 Ah and reach EOL much earlier, while CALCE CS2 cells are approximately 1.1 Ah and reach the chosen 75% threshold around 545–692 cycles. Normalizing capacity and current removes unit scale but not the different degradation-time distribution. The zero-shot model therefore learns the wrong remaining-life scale. Calibration can recover much of the point accuracy using three external cells, but four cells are insufficient to estimate reliable predictive tails.

## Next required experiment

1. Add at least one independent CALCE family or another public dataset with compatible raw V/I/time signals.
2. Fit a hierarchical/domain-adaptive trajectory model with battery-family effects and monotonic capacity constraints.
3. Calibrate uncertainty out-of-fold using conformal residuals; target 85–95% empirical coverage for a nominal 90% interval.
4. Freeze all hyperparameters before testing the final untouched battery family.
5. Only accept GRU/TCN if it beats the same transfer baseline at at least 3/4 checkpoints and passes the uncertainty gate.
