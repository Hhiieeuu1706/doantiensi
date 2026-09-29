import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTOCOL_PATH = ROOT / "research_protocol_v3.yaml"

with PROTOCOL_PATH.open("r", encoding="utf-8") as handle:
    PROTOCOL = json.load(handle)

PROTOCOL_ID = PROTOCOL["protocol_id"]
NASA = PROTOCOL["primary_nasa"]
EVALUATION = PROTOCOL["evaluation"]
ACCEPTANCE = PROTOCOL["acceptance"]

CANONICAL_BATTERIES = NASA["battery_ids"]
OBSERVED_EOL_BATTERIES = NASA["observed_eol_metric_batteries"]
CENSORED_BATTERIES = NASA["censored_batteries"]
NASA_EOL_AH = float(NASA["eol_threshold_ah"])
CHECKPOINTS = tuple(float(x) for x in EVALUATION["checkpoint_fractions"])
SEEDS = tuple(int(x) for x in EVALUATION["seed_registry"])


def protocol_metadata():
    return {
        "protocol_id": PROTOCOL_ID,
        "protocol_path": str(PROTOCOL_PATH),
        "nasa_eol_threshold_ah": NASA_EOL_AH,
        "checkpoint_fractions": list(CHECKPOINTS),
        "outer_split": EVALUATION["outer_split"],
        "random_cycle_split_allowed": EVALUATION["random_cycle_split_allowed"],
    }
