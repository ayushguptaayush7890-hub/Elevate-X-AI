"""
Build crosswalk mapping between ESCO v1.2.1, O*NET 28.1, and India NCO-2015.
Produces:
  datasets/career_transition/processed/crosswalks/occupation_crosswalk.parquet
  datasets/career_transition/processed/crosswalks/occupation_crosswalk.json
"""

import os
import json
import pandas as pd

def build_crosswalks():
    print("=" * 80)
    print("BUILD OCCUPATION TAXONOMY CROSSWALK (ESCO <-> O*NET <-> NCO-2015)")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    crosswalk_dir = os.path.join(base_dir, "processed", "crosswalks")
    occ_dir = os.path.join(base_dir, "processed", "occupations")
    os.makedirs(crosswalk_dir, exist_ok=True)

    master_occ_file = os.path.join(occ_dir, "master_occupations.parquet")
    df = pd.read_parquet(master_occ_file)

    esco_df = df[df["source"] == "ESCO v1.2.1"]
    onet_df = df[df["source"] == "O*NET 28.1"]
    nco_df = df[df["source"].str.contains("India", case=False, na=False)]

    # Index by isco_group
    esco_by_isco = {}
    for _, row in esco_df.iterrows():
        isco = str(row.get("isco_group", "")).strip()
        if isco:
            esco_by_isco.setdefault(isco, []).append({
                "canonical_id": row["canonical_id"],
                "uri": row.get("uri", ""),
                "title": row["occupation_title"]
            })

    # Index NCO by first 4 digits (ISCO unit group)
    nco_by_isco = {}
    for _, row in nco_df.iterrows():
        code_part = str(row["canonical_id"]).replace("NCO:", "").strip()
        isco = code_part.split(".")[0] if "." in code_part else str(row.get("isco_group", "")).strip()
        if isco:
            nco_by_isco.setdefault(isco, []).append({
                "canonical_id": row["canonical_id"],
                "title": row["occupation_title"]
            })

    # Title normalization helper for exact/near matching
    def clean_title(t):
        return "".join(c.lower() for c in str(t) if c.isalnum() or c.isspace()).strip()

    esco_title_map = {clean_title(r["occupation_title"]): r["canonical_id"] for _, r in esco_df.iterrows()}

    # Crosswalk entries
    crosswalk_records = []

    # 1. Map NCO to ESCO via ISCO unit group and direct title similarity
    for _, nco_row in nco_df.iterrows():
        nco_id = nco_row["canonical_id"]
        nco_title = nco_row["occupation_title"]
        code_part = str(nco_id).replace("NCO:", "").strip()
        nco_isco = code_part.split(".")[0] if "." in code_part else str(nco_row.get("isco_group", ""))
        nco_clean = clean_title(nco_title)

        matched_esco = None
        match_type = "none"

        # Check title match
        if nco_clean in esco_title_map:
            matched_esco = esco_title_map[nco_clean]
            match_type = "exact_title"
        elif nco_isco and nco_isco in esco_by_isco:
            # Pick first or best title match in same ISCO
            group_esco = esco_by_isco[nco_isco]
            matched_esco = group_esco[0]["canonical_id"]
            match_type = "isco_group"

        crosswalk_records.append({
            "source_taxonomy": "India NCO-2015",
            "source_id": nco_id,
            "source_title": nco_title,
            "target_taxonomy": "ESCO v1.2.1",
            "target_id": matched_esco or "",
            "match_type": match_type,
            "isco_unit_group": nco_isco
        })

    # 2. Map O*NET to ESCO via title and SOC/ISCO alignment
    for _, onet_row in onet_df.iterrows():
        onet_id = onet_row["canonical_id"]
        onet_title = onet_row["occupation_title"]
        onet_clean = clean_title(onet_title)

        matched_esco = None
        match_type = "none"

        if onet_clean in esco_title_map:
            matched_esco = esco_title_map[onet_clean]
            match_type = "exact_title"
        else:
            # Substring match
            for esc_clean, esc_id in esco_title_map.items():
                if onet_clean and (onet_clean in esc_clean or esc_clean in onet_clean):
                    matched_esco = esc_id
                    match_type = "title_subsumption"
                    break

        crosswalk_records.append({
            "source_taxonomy": "O*NET 28.1",
            "source_id": onet_id,
            "source_title": onet_title,
            "target_taxonomy": "ESCO v1.2.1",
            "target_id": matched_esco or "",
            "match_type": match_type,
            "isco_unit_group": ""
        })

    df_cw = pd.DataFrame(crosswalk_records)
    out_parquet = os.path.join(crosswalk_dir, "occupation_crosswalk.parquet")
    out_json = os.path.join(crosswalk_dir, "occupation_crosswalk.json")

    df_cw.to_parquet(out_parquet, index=False)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(crosswalk_records[:500], f, indent=2)  # sample in json

    print(f"Total crosswalk links established: {len(df_cw)}")
    print(f"Matched entries: {len(df_cw[df_cw['match_type'] != 'none'])} / {len(df_cw)}")
    print(f"[SUCCESS] Saved Crosswalk:\n  Parquet: {out_parquet}\n  JSON:    {out_json}")

if __name__ == "__main__":
    build_crosswalks()
