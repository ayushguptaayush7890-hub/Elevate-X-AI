"""
Script 10: normalize_occupations.py
Consolidates occupations across ESCO, O*NET, and India NCO-2015.
Generates:
- processed/occupations/master_occupations.parquet
- processed/occupations/master_occupations.json
"""

import sys
import json
import re
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
PROC_DIR = BASE_DIR / "datasets" / "career_transition" / "processed" / "occupations"


def clean_text(s):
    if not s or pd.isna(s):
        return ""
    return re.sub(r'\s+', ' ', str(s)).strip()


def main():
    print("=" * 80)
    print("NORMALIZE MASTER OCCUPATIONS")
    print("=" * 80)

    master = []

    # 1. ESCO Occupations
    esco_file = PROC_DIR / "esco_occupations.parquet"
    if esco_file.exists():
        df_esco = pd.read_parquet(esco_file)
        print(f"Loaded {len(df_esco)} ESCO occupations.")
        for _, r in df_esco.iterrows():
            title = clean_text(r["occupation_title"])
            aliases = [clean_text(a) for a in str(r.get("alternative_titles", "")).split("\n") if clean_text(a)]
            master.append({
                "canonical_id": f"ESCO:{r['esco_code'] or r['esco_occupation_uri'].split('/')[-1]}",
                "uri": r["esco_occupation_uri"],
                "occupation_title": title,
                "clean_title": title.lower(),
                "aliases": aliases,
                "description": clean_text(r["description"]),
                "classification_system": "ESCO",
                "source": "ESCO v1.2.1",
                "isco_group": str(r.get("isco_group", "")),
                "national_system": "European Union / International"
            })

    # 2. O*NET Occupations
    onet_file = PROC_DIR / "onet_occupations.parquet"
    if onet_file.exists():
        df_onet = pd.read_parquet(onet_file)
        print(f"Loaded {len(df_onet)} O*NET occupations.")
        for _, r in df_onet.iterrows():
            title = clean_text(r["occupation_title"])
            master.append({
                "canonical_id": f"ONET:{r['onet_soc_code']}",
                "uri": f"https://www.onetonline.org/link/summary/{r['onet_soc_code']}",
                "occupation_title": title,
                "clean_title": title.lower(),
                "aliases": [],
                "description": clean_text(r["description"]),
                "classification_system": "O*NET",
                "source": "O*NET 28.1",
                "isco_group": str(r.get("job_zone", "")),
                "national_system": "United States"
            })

    # 3. India NCO-2015 Occupations
    nco_file = PROC_DIR / "nco_occupations.parquet"
    if nco_file.exists():
        df_nco = pd.read_parquet(nco_file)
        print(f"Loaded {len(df_nco)} India NCO occupations.")
        for _, r in df_nco.iterrows():
            title = clean_text(r["occupation_title"])
            master.append({
                "canonical_id": f"NCO:{r['nco_2015_code']}",
                "uri": f"https://www.dge.gov.in/nco-2015#{r['nco_2015_code']}",
                "occupation_title": title,
                "clean_title": title.lower(),
                "aliases": [],
                "description": clean_text(r["description"]),
                "classification_system": "NCO-2015",
                "source": "DGE Ministry of Labour & Employment India",
                "isco_group": str(r.get("division_code", "")),
                "national_system": "India"
            })

    df_master = pd.DataFrame(master)
    print(f"Total unified master occupations: {len(df_master)}")

    out_parquet = PROC_DIR / "master_occupations.parquet"
    out_json = PROC_DIR / "master_occupations.json"

    df_master.to_parquet(out_parquet, index=False)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(master, f, indent=2)

    print(f"[SUCCESS] Saved master occupations:")
    print(f"  Parquet: {out_parquet.relative_to(BASE_DIR)}")
    print(f"  JSON:    {out_json.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
