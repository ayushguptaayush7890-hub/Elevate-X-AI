"""
Identify duplicate and near-duplicate occupation and skill records across sources.
Produces:
  datasets/career_transition/audit/duplicate_report.json
"""

import os
import json
import pandas as pd
from collections import Counter

def deduplicate_records():
    print("=" * 80)
    print("DEDUPLICATE & CROSS-TAXONOMY EQUIVALENCE AUDIT")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audit_dir = os.path.join(base_dir, "audit")
    occ_dir = os.path.join(base_dir, "processed", "occupations")
    skills_dir = os.path.join(base_dir, "processed", "skills")
    os.makedirs(audit_dir, exist_ok=True)

    # 1. Occupations
    occ_file = os.path.join(occ_dir, "master_occupations.parquet")
    df_occ = pd.read_parquet(occ_file)

    def norm_text(t):
        return "".join(c.lower() for c in str(t) if c.isalnum() or c.isspace()).strip()

    title_counts = Counter()
    title_to_ids = {}
    for _, row in df_occ.iterrows():
        clean = norm_text(row["occupation_title"])
        title_counts[clean] += 1
        if clean not in title_to_ids:
            title_to_ids[clean] = []
        title_to_ids[clean].append({
            "canonical_id": row["canonical_id"],
            "title": row["occupation_title"],
            "source": row["source"],
            "isco_group": row.get("isco_group", "")
        })

    cross_duplicates = []
    intra_duplicates = []
    for clean, cnt in title_counts.items():
        if cnt > 1:
            records = title_to_ids[clean]
            sources = set(r["source"] for r in records)
            if len(sources) > 1:
                cross_duplicates.append({
                    "normalized_title": clean,
                    "count": cnt,
                    "records": records
                })
            else:
                intra_duplicates.append({
                    "normalized_title": clean,
                    "count": cnt,
                    "records": records
                })

    # 2. Skills
    skills_file = os.path.join(skills_dir, "master_skills.parquet")
    df_skills = pd.read_parquet(skills_file)
    skill_counts = Counter(norm_text(s) for s in df_skills["name"])
    skill_duplicates = sum(1 for c in skill_counts.values() if c > 1)

    report = {
        "total_occupations_analyzed": len(df_occ),
        "total_skills_analyzed": len(df_skills),
        "exact_intra_taxonomy_occupation_duplicates": len(intra_duplicates),
        "cross_taxonomy_occupation_equivalences": len(cross_duplicates),
        "duplicate_skill_names_count": skill_duplicates,
        "sample_cross_taxonomy_equivalences": cross_duplicates[:20],
        "sample_intra_taxonomy_duplicates": intra_duplicates[:10],
        "deduplication_policy": "Preserve distinct taxonomy primary keys while linking via unified crosswalk to maintain exact government taxonomy fidelity."
    }

    out_file = os.path.join(audit_dir, "duplicate_report.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[SUCCESS] Deduplication Audit Complete:\n  Cross-taxonomy Equivalences: {len(cross_duplicates)}\n  Intra-taxonomy duplicates: {len(intra_duplicates)}\n  Saved: {out_file}")

if __name__ == "__main__":
    deduplicate_records()
