# Incomplete-cycle quality rule

For the NASA discharge feature table, a cycle is flagged as incomplete when `duration_s < 500 s` or `n_samples < 50`. Capacity values that are missing or non-positive are separately flagged as capacity anomalies. Flagged cycles remain in the raw audit and quality report, but are excluded from EOL/RUL label construction and model fitting in the cleaned analysis table.

Audit result: 38 incomplete cycles and 44 non-positive/missing-capacity rows were flagged. None of the incomplete cycles carried an observed-EOL label in the current NASA table, so the registered EOL labels are unchanged. The rule is conservative and must be revalidated for other datasets/protocols.
