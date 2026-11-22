"""
Script 3: inspect_dataset_schemas.py
Inspects raw dataset schemas across ESCO, O*NET, India NCO, Job Descriptions, and Learning Resources.
Writes audit/schema_audit.json.
"""

import os
import sys
import json
import csv
import pandas as pd
import pypdf
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[3]
CAREER_TRANS_DIR = BASE_DIR / "datasets" / "career_transition"
RAW_DIR = CAREER_TRANS_DIR / "raw"
AUDIT_DIR = CAREER_TRANS_DIR / "audit"


def inspect_csv_tsv(filepath: Path, sep=",") -> dict:
    df = pd.read_csv(filepath, sep=sep, nrows=5, low_memory=False)
    # count total lines
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        total_rows = sum(1 for _ in f) - 1
    return {
        "file": filepath.name,
        "format": "csv" if sep == "," else "tsv",
        "row_count": max(0, total_rows),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_record": df.iloc[0].to_dict() if len(df) > 0 else {}
    }


def inspect_parquet(filepath: Path) -> dict:
    df = pd.read_parquet(filepath)
    return {
        "file": filepath.name,
        "format": "parquet",
        "row_count": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "sample_record": {k: str(v)[:100] for k, v in df.iloc[0].to_dict().items()} if len(df) > 0 else {}
    }


def inspect_pdf(filepath: Path) -> dict:
    reader = pypdf.PdfReader(str(filepath))
    return {
        "file": filepath.name,
        "format": "pdf",
        "page_count": len(reader.pages),
        "is_encrypted": reader.is_encrypted,
        "sample_snippet": reader.pages[15].extract_text()[:250] if len(reader.pages) > 15 else ""
    }


def inspect_json(filepath: Path) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        count = len(data)
        sample = data[0] if count > 0 else {}
    elif isinstance(data, dict):
        count = len(data)
        sample = list(data.items())[0] if count > 0 else {}
    else:
        count = 1
        sample = {}
    return {
        "file": filepath.name,
        "format": "json",
        "record_count": count,
        "sample": str(sample)[:200]
    }


def main():
    print("=" * 80)
    print("INSPECT DATASET SCHEMAS")
    print("=" * 80)

    schema_report = {
        "timestamp": datetime.now().isoformat(),
        "datasets": {}
    }

    # 1. ESCO
    esco_schemas = {}
    for p in (RAW_DIR / "esco").glob("*.csv"):
        print(f"Inspecting ESCO: {p.name}...")
        esco_schemas[p.name] = inspect_csv_tsv(p, sep=",")
    schema_report["datasets"]["esco"] = esco_schemas

    # 2. O*NET
    onet_schemas = {}
    for p in (RAW_DIR / "onet").glob("*.txt"):
        print(f"Inspecting O*NET: {p.name}...")
        try:
            onet_schemas[p.name] = inspect_csv_tsv(p, sep="\t")
        except Exception as e:
            onet_schemas[p.name] = {"error": str(e)}
    schema_report["datasets"]["onet"] = onet_schemas

    # 3. India NCO
    nco_schemas = {}
    for p in (RAW_DIR / "india_nco").glob("*.pdf"):
        print(f"Inspecting India NCO PDF: {p.name}...")
        nco_schemas[p.name] = inspect_pdf(p)
    schema_report["datasets"]["india_nco"] = nco_schemas

    # 4. Job Descriptions
    jd_schemas = {}
    for p in (RAW_DIR / "job_descriptions").iterdir():
        if p.name.endswith(".parquet"):
            print(f"Inspecting Job Parquet: {p.name}...")
            jd_schemas[p.name] = inspect_parquet(p)
        elif p.name.endswith(".csv"):
            print(f"Inspecting Job CSV: {p.name}...")
            jd_schemas[p.name] = inspect_csv_tsv(p, sep=",")
    schema_report["datasets"]["job_descriptions"] = jd_schemas

    # 5. Learning Resources
    res_schemas = {}
    for p in (RAW_DIR / "learning_resources").glob("*.json"):
        print(f"Inspecting Learning Resources: {p.name}...")
        res_schemas[p.name] = inspect_json(p)
    schema_report["datasets"]["learning_resources"] = res_schemas

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = AUDIT_DIR / "schema_audit.json"
    with open(out_file, "w") as f:
        json.dump(schema_report, f, indent=2)

    print(f"\nSchema audit complete. Saved to {out_file.name}")


if __name__ == "__main__":
    main()
