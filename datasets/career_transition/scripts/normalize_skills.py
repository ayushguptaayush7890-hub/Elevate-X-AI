"""
Normalize and consolidate skills from ESCO v1.2.1 and O*NET 28.1.
Produces:
  datasets/career_transition/processed/skills/master_skills.parquet
  datasets/career_transition/processed/skills/master_skills.json
"""

import os
import json
import pandas as pd

def normalize_skills():
    print("=" * 80)
    print("NORMALIZE MASTER SKILLS")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = os.path.join(base_dir, "processed", "skills")

    esco_file = os.path.join(skills_dir, "esco_skills.parquet")
    onet_file = os.path.join(skills_dir, "onet_competencies.parquet")

    records = []

    # 1. ESCO skills
    if os.path.exists(esco_file):
        df_esco = pd.read_parquet(esco_file)
        for _, row in df_esco.iterrows():
            alt = row.get("alternative_labels")
            if isinstance(alt, str):
                try:
                    alt_list = json.loads(alt)
                except Exception:
                    alt_list = [a.strip() for a in alt.split("\n") if a.strip()]
            elif isinstance(alt, list):
                alt_list = alt
            else:
                alt_list = []

            records.append({
                "skill_id": row["esco_skill_uri"],
                "name": str(row["skill_name"]).strip(),
                "type": str(row.get("skill_type", "skill")),
                "alternative_labels": alt_list,
                "description": str(row.get("description", "")),
                "source": "ESCO v1.2.1"
            })
        print(f"Loaded {len(df_esco)} ESCO skills.")

    # 2. O*NET competencies
    if os.path.exists(onet_file):
        df_onet = pd.read_parquet(onet_file)
        for _, row in df_onet.iterrows():
            records.append({
                "skill_id": f"onet:{row['competency_id']}",
                "name": str(row["name"]).strip(),
                "type": str(row.get("type", "work_activity")),
                "alternative_labels": [],
                "description": f"O*NET Generalized Work Activity / Skill element {row['competency_id']}: {row['name']}",
                "source": "O*NET 28.1"
            })
        print(f"Loaded {len(df_onet)} O*NET competencies.")

    df_master = pd.DataFrame(records)
    out_parquet = os.path.join(skills_dir, "master_skills.parquet")
    out_json = os.path.join(skills_dir, "master_skills.json")

    # Serialize alternative_labels as json string for parquet compatibility
    df_parquet = df_master.copy()
    df_parquet["alternative_labels"] = df_parquet["alternative_labels"].apply(json.dumps)
    df_parquet.to_parquet(out_parquet, index=False)

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    print(f"Total unified master skills: {len(records)}")
    print(f"[SUCCESS] Saved master skills:\n  Parquet: {out_parquet}\n  JSON:    {out_json}")

if __name__ == "__main__":
    normalize_skills()
