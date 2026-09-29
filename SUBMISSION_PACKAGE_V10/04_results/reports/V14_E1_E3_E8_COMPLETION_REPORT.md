# V14 E1/E3/E8 completion report

## E1 protocol sensitivity

The RF experiment uses identical engineered HI, EOL definition and checkpoints. Random-cycle, fixed battery holdout and LOBO results are in `V14_E1_PROTOCOL_SENSITIVITY.csv`. Random-cycle errors are generally lower, while LOBO exposes unseen-battery error; this supports the need for battery-level evaluation. The fixed holdout contains one battery and is descriptive, not a population estimate.

## E3 fair deep-family comparison

RF/XGBoost/classical models have direct engineered-HI comparison. Five-seed deep artifacts exist, but the convergence log uses a fixed epoch schedule rather than validation-loss plateau/patience. Therefore deep-family numbers remain provisional and are not used to claim universal RF superiority.

## E8 uncertainty usefulness

Coverage-width results for 80%, 90% and 95% target coverage are in `V14_E8_COVERAGE_WIDTH.csv`. Increasing target coverage increases interval width; early-life intervals remain wide. Coverage must therefore be reported jointly with width and normalized width.