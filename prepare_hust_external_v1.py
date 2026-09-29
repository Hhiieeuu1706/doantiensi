"""Prepare the HUST final-external dataset without exposing final labels.

Phase 1 (``ingest``) verifies and extracts the raw archive, hashes every raw
file, discovers battery identifiers, and locks the deterministic 60/20/20
split.  It deliberately does not compute capacity-derived EOL/RUL labels.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "external_data" / "raw" / "HUST"
ARCHIVE = RAW_DIR / "our_data.zip"
EXTRACT_DIR = RAW_DIR / "extracted"
TABLES = ROOT / "outputs" / "tables"
PROTOCOL_ID = "final-external-hust-v1.0"
BATTERY_RE = re.compile(r"(?:cell|battery|batt|b)[_-]?(\d{1,3})(?:\D|$)", re.I)
HUST_FILE_RE = re.compile(r"^(\d{1,2})-(\d{1,2})\.pkl$", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_extract() -> None:
    """Extract only paths contained by EXTRACT_DIR; retain archive unchanged."""
    if not ARCHIVE.is_file():
        raise FileNotFoundError(f"Missing raw HUST archive: {ARCHIVE}")
    with zipfile.ZipFile(ARCHIVE) as zf:
        corrupt = zf.testzip()
        if corrupt:
            raise RuntimeError(f"Archive integrity check failed at {corrupt}")
        root = EXTRACT_DIR.resolve()
        invalid = []
        for info in zf.infolist():
            target = (EXTRACT_DIR / info.filename).resolve()
            if root not in target.parents and target != root:
                invalid.append(info.filename)
        if invalid:
            raise RuntimeError(f"Unsafe archive paths detected: {invalid[:3]}")
        EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
        zf.extractall(EXTRACT_DIR)


def normalized_battery_id(path: Path) -> str | None:
    """Use the first explicit cell/battery token in a relative raw path."""
    # HUST names its 77 cells as e.g. ``1-1.pkl`` through ``10-8.pkl``.
    hust_match = HUST_FILE_RE.match(path.name)
    if hust_match:
        return f"HUST_{int(hust_match.group(1)):02d}_{int(hust_match.group(2)):02d}"
    for part in path.parts[::-1]:
        hit = BATTERY_RE.search(part)
        if hit:
            return f"HUST_{int(hit.group(1)):03d}"
    return None


def write_csv(frame: pd.DataFrame, destination: Path) -> None:
    """Write a protocol artifact after its explicit destination has been created."""
    # The desktop workspace may deny creation of sidecar ``.tmp`` files under a
    # folder watched by spreadsheet software.  The destination is precreated
    # and the complete DataFrame is emitted in one operation.
    frame.to_csv(destination, index=False)


def raw_manifest() -> pd.DataFrame:
    records = []
    for path in sorted(EXTRACT_DIR.rglob("*")):
        if path.is_file():
            relative = path.relative_to(ROOT)
            records.append({
                "relative_path": str(relative),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "extension": path.suffix.lower(),
                "battery_id_candidate": normalized_battery_id(path.relative_to(EXTRACT_DIR)),
            })
    return pd.DataFrame(records)


def lock_split(manifest: pd.DataFrame) -> pd.DataFrame:
    batteries = sorted(x for x in manifest.battery_id_candidate.dropna().unique())
    if len(batteries) < 10:
        raise RuntimeError(
            "Could not discover at least 10 HUST battery IDs from raw paths; "
            "inspect HUST_RAW_MANIFEST_V1.csv and update only the ID extractor."
        )
    ranked = sorted(
        batteries,
        key=lambda bid: hashlib.sha256(f"{PROTOCOL_ID}:{bid}".encode()).hexdigest(),
    )
    n = len(ranked)
    n_dev = int(n * 0.60)
    n_cal = int(n * 0.20)
    rows = []
    for rank, bid in enumerate(ranked):
        split = "development" if rank < n_dev else "calibration" if rank < n_dev + n_cal else "final_untouched"
        rows.append({
            "protocol_id": PROTOCOL_ID,
            "battery_id": bid,
            "sort_sha256": hashlib.sha256(f"{PROTOCOL_ID}:{bid}".encode()).hexdigest(),
            "rank": rank + 1,
            "split": split,
            "label_access": "forbidden_until_model_freeze" if split == "final_untouched" else "permitted",
        })
    return pd.DataFrame(rows)


def ingest() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    safe_extract()
    archive = pd.DataFrame([{
        "relative_path": str(ARCHIVE.relative_to(ROOT)),
        "bytes": ARCHIVE.stat().st_size,
        "sha256": sha256(ARCHIVE),
        "source_url": "https://data.mendeley.com/public-files/datasets/nsc7hnsg4s/files/5ca0ac3e-d598-4d07-8dcb-879aa047e98b/file_downloaded",
        "dataset_doi": "10.17632/nsc7hnsg4s.2",
    }])
    manifest = raw_manifest()
    write_csv(archive, TABLES / "HUST_ARCHIVE_MANIFEST_V1.csv")
    write_csv(manifest, TABLES / "HUST_RAW_MANIFEST_V1.csv")
    split = lock_split(manifest)
    write_csv(split, TABLES / "HUST_SPLIT_LOCK_V1.csv")
    report = {
        "protocol_id": PROTOCOL_ID,
        "archive": archive.iloc[0].to_dict(),
        "raw_files": int(len(manifest)),
        "extensions": manifest.extension.value_counts().to_dict(),
        "battery_candidates": int(manifest.battery_id_candidate.nunique()),
        "split_counts": split.split.value_counts().to_dict(),
        "next_step": "Parse signals and audit units/cycles without materializing final EOL/RUL labels.",
    }
    (TABLES / "HUST_INGEST_AUDIT_V1.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["ingest"], default="ingest")
    args = parser.parse_args()
    if args.phase == "ingest":
        ingest()


if __name__ == "__main__":
    main()
