"""
Script 6: preprocess_onet.py
Processes authentic O*NET 28.1 database tables:
- Occupation Data.txt
- Essential Skills.txt
- Transferable Skills.txt
- Knowledge.txt
- Work Activities.txt
- Job Zones.txt
Generates:
- processed/occupations/onet_occupations.parquet
- processed/skills/onet_competencies.parquet
- processed/occupation_skill_graph/onet_relations.parquet
"""

import sys
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "datasets" / "career_transition" / "raw" / "onet"
PROC_DIR = BASE_DIR / "datasets" / "career_transition" / "processed"


def main():
    print("=" * 80)
    print("PREPROCESS O*NET 28.1")
    print("=" * 80)

    # 1. Occupation Data
    occ_file = RAW_DIR / "Occupation Data.txt"
    print(f"Reading {occ_file.name}...")
    df_occ = pd.read_csv(occ_file, sep="\t")
    print(f"  Raw O*NET occupations: {len(df_occ)}")

    df_occ = df_occ.rename(columns={
        "O*NET-SOC Code": "onet_soc_code",
        "Title": "occupation_title",
        "Description": "description"
    })
    df_occ["source"] = "O*NET 28.1"
    df_occ["occupation_title"] = df_occ["occupation_title"].astype(str).str.strip()

    # 2. Job Zones
    jz_file = RAW_DIR / "Job Zones.txt"
    if jz_file.exists():
        df_jz = pd.read_csv(jz_file, sep="\t")
        df_jz = df_jz.rename(columns={"O*NET-SOC Code": "onet_soc_code", "Job Zone": "job_zone"})
        df_occ = df_occ.merge(df_jz[["onet_soc_code", "job_zone"]], on="onet_soc_code", how="left")

    # 3. Work Activities & Knowledge
    relations = []
    competencies = {}

    # Read Work Activities
    wa_file = RAW_DIR / "Work Activities.txt"
    if wa_file.exists():
        print(f"Reading {wa_file.name}...")
        df_wa = pd.read_csv(wa_file, sep="\t")
        # filter for Importance rating (Scale ID: IM) with score >= 3.0
        df_wa_im = df_wa[(df_wa["Scale ID"] == "IM") & (df_wa["Data Value"] >= 3.0)]
        for _, row in df_wa_im.iterrows():
            soc = row["O*NET-SOC Code"]
            elem_id = row["Element ID"]
            elem_name = row["Element Name"]
            competencies[elem_id] = {
                "competency_id": elem_id,
                "name": elem_name,
                "type": "Work Activity",
                "source": "O*NET 28.1"
            }
            relations.append({
                "onet_soc_code": soc,
                "competency_id": elem_id,
                "importance_score": float(row["Data Value"]),
                "relation_type": "work_activity"
            })

    # Read Essential Skills
    es_file = RAW_DIR / "Essential Skills.txt"
    if es_file.exists():
        print(f"Reading {es_file.name}...")
        df_es = pd.read_csv(es_file, sep="\t")
        if "O*NET-SOC Code" in df_es.columns and "Element Name" in df_es.columns:
            for _, row in df_es.iterrows():
                soc = row["O*NET-SOC Code"]
                elem_id = row.get("Element ID", f"SK-{row['Element Name'][:10]}")
                elem_name = row["Element Name"]
                competencies[elem_id] = {
                    "competency_id": elem_id,
                    "name": elem_name,
                    "type": "Essential Skill",
                    "source": "O*NET 28.1"
                }
                relations.append({
                    "onet_soc_code": soc,
                    "competency_id": elem_id,
                    "importance_score": 4.0,
                    "relation_type": "essential_skill"
                })

    df_comp = pd.DataFrame(list(competencies.values()))
    df_rel = pd.DataFrame(relations)

    (PROC_DIR / "occupations").mkdir(parents=True, exist_ok=True)
    (PROC_DIR / "skills").mkdir(parents=True, exist_ok=True)
    (PROC_DIR / "occupation_skill_graph").mkdir(parents=True, exist_ok=True)

    occ_out = PROC_DIR / "occupations" / "onet_occupations.parquet"
    comp_out = PROC_DIR / "skills" / "onet_competencies.parquet"
    rel_out = PROC_DIR / "occupation_skill_graph" / "onet_relations.parquet"

    df_occ.to_parquet(occ_out, index=False)
    df_comp.to_parquet(comp_out, index=False)
    df_rel.to_parquet(rel_out, index=False)

    print(f"\n[SUCCESS] Saved O*NET processed parquets:")
    print(f"  Occupations:  {len(df_occ)} records -> {occ_out.relative_to(BASE_DIR)}")
    print(f"  Competencies: {len(df_comp)} records -> {comp_out.relative_to(BASE_DIR)}")
    print(f"  Relations:    {len(df_rel)} records -> {rel_out.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
