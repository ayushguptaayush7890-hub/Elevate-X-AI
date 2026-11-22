"""
Script 7: preprocess_nco.py
Normalizes extracted India NCO-2015 occupational records into production parquet format.
Generates:
- processed/occupations/nco_occupations.parquet
"""

import sys
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
INTERIM_FILE = BASE_DIR / "datasets" / "career_transition" / "interim" / "extracted_occupations" / "nco_occupations.json"
PROC_DIR = BASE_DIR / "datasets" / "career_transition" / "processed" / "occupations"


def main():
    print("=" * 80)
    print("PREPROCESS INDIA NCO-2015")
    print("=" * 80)

    if not INTERIM_FILE.exists():
        print("Missing nco_occupations.json! Run extract_india_nco.py first.")
        sys.exit(1)

    with open(INTERIM_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} extracted NCO records.")

    df["source"] = "NCO 2015 (DGE India)"
    df["occupation_title"] = df["occupation_title"].astype(str).str.strip()
    df["clean_title"] = df["occupation_title"].str.lower().str.replace(r'[^a-z0-9 ]', ' ', regex=True).str.strip()

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PROC_DIR / "nco_occupations.parquet"
    df.to_parquet(out_file, index=False)

    print(f"[SUCCESS] Saved {len(df)} NCO occupations to {out_file.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
