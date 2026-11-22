"""
Build unified NetworkX bipartite graph connecting occupations to skills/competencies.
Produces:
  datasets/career_transition/processed/occupation_skill_graph/master_graph.graphml
  datasets/career_transition/processed/occupation_skill_graph/edges.parquet
  datasets/career_transition/processed/occupation_skill_graph/graph_summary.json
"""

import os
import json
import pandas as pd
import networkx as nx

def build_graph():
    print("=" * 80)
    print("BUILD UNIFIED OCCUPATION-SKILL KNOWLEDGE GRAPH")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graph_dir = os.path.join(base_dir, "processed", "occupation_skill_graph")
    occ_dir = os.path.join(base_dir, "processed", "occupations")
    skills_dir = os.path.join(base_dir, "processed", "skills")
    os.makedirs(graph_dir, exist_ok=True)

    G = nx.Graph()

    # 1. Load Master Occupations
    occ_parquet = os.path.join(occ_dir, "master_occupations.parquet")
    df_occ = pd.read_parquet(occ_parquet)
    print(f"Loaded {len(df_occ)} master occupations.")
    
    # Track isco to skills mapping for NCO bridging
    isco_to_skills = {}

    for _, row in df_occ.iterrows():
        occ_id = str(row["uri"] if row.get("uri") else row["canonical_id"])
        G.add_node(
            occ_id,
            node_type="occupation",
            title=str(row["occupation_title"]),
            source=str(row["source"]),
            canonical_id=str(row["canonical_id"]),
            isco_code=str(row.get("isco_group", ""))
        )

    # 2. Load Master Skills
    skills_parquet = os.path.join(skills_dir, "master_skills.parquet")
    df_skills = pd.read_parquet(skills_parquet)
    print(f"Loaded {len(df_skills)} master skills.")
    for _, row in df_skills.iterrows():
        skill_id = str(row["skill_id"])
        G.add_node(
            skill_id,
            node_type="skill",
            name=str(row["name"]),
            source=str(row["source"]),
            type=str(row.get("type", "skill"))
        )

    edge_records = []

    # 3. Add ESCO Relations
    esco_rel_file = os.path.join(graph_dir, "esco_relations.parquet")
    if os.path.exists(esco_rel_file):
        df_esco_rel = pd.read_parquet(esco_rel_file)
        # Create map of esco uri to isco code
        esco_occ_map = df_occ[df_occ["source"] == "ESCO v1.2.1"].set_index("uri")["isco_group"].to_dict()

        for _, row in df_esco_rel.iterrows():
            src = str(row["esco_occupation_uri"])
            dst = str(row["esco_skill_uri"])
            rel_type = str(row.get("relation_type", "essential"))
            weight = 1.0 if rel_type == "essential" else 0.6
            
            G.add_edge(src, dst, weight=weight, relation_type=rel_type, source="ESCO v1.2.1")
            edge_records.append({
                "source": src,
                "target": dst,
                "weight": weight,
                "relation_type": rel_type,
                "provenance": "ESCO v1.2.1"
            })

            # Record ISCO to skills
            isco = esco_occ_map.get(src, "")
            if isco:
                if isco not in isco_to_skills:
                    isco_to_skills[isco] = set()
                isco_to_skills[isco].add(dst)

        print(f"Added {len(df_esco_rel)} ESCO edges.")

    # 4. Add O*NET Relations
    onet_rel_file = os.path.join(graph_dir, "onet_relations.parquet")
    if os.path.exists(onet_rel_file):
        df_onet_rel = pd.read_parquet(onet_rel_file)
        for _, row in df_onet_rel.iterrows():
            src = f"onet:{row['onet_soc_code']}"
            dst = f"onet:{row['competency_id']}"
            score = float(row.get("importance_score", 3.0))
            weight = min(1.0, max(0.1, score / 5.0))
            rel_type = str(row.get("relation_type", "work_activity"))

            G.add_edge(src, dst, weight=weight, relation_type=rel_type, source="O*NET 28.1")
            edge_records.append({
                "source": src,
                "target": dst,
                "weight": weight,
                "relation_type": rel_type,
                "provenance": "O*NET 28.1"
            })
        print(f"Added {len(df_onet_rel)} O*NET edges.")

    # 5. Connect India NCO occupations to skills using ISCO unit group mapping
    df_nco = df_occ[df_occ["source"].str.contains("India", case=False, na=False)]
    nco_edge_count = 0
    for _, row in df_nco.iterrows():
        occ_id = str(row["canonical_id"])
        # Extract 4-digit ISCO unit group from code like NCO:7411.0100 -> 7411
        code_part = occ_id.replace("NCO:", "").strip()
        isco = code_part.split(".")[0] if "." in code_part else str(row.get("isco_group", ""))
        skills = isco_to_skills.get(isco, set())
        # Pick top associated skills (limit to 15 per NCO occupation to keep graph balanced)
        for s in list(skills)[:15]:
            G.add_edge(occ_id, s, weight=0.75, relation_type="nco_isco_aligned", source="India NCO Crosswalk")
            edge_records.append({
                "source": occ_id,
                "target": s,
                "weight": 0.75,
                "relation_type": "nco_isco_aligned",
                "provenance": "India NCO Crosswalk"
            })
            nco_edge_count += 1
    print(f"Connected India NCO occupations with {nco_edge_count} cross-taxonomy edges.")

    # 6. Save Edges Parquet
    df_edges = pd.DataFrame(edge_records)
    edges_parquet = os.path.join(graph_dir, "edges.parquet")
    df_edges.to_parquet(edges_parquet, index=False)

    # 7. Save GraphML
    out_graphml = os.path.join(graph_dir, "master_graph.graphml")
    nx.write_graphml(G, out_graphml)

    # 8. Summary stats
    summary = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "num_occupations": sum(1 for _, d in G.nodes(data=True) if d.get("node_type") == "occupation"),
        "num_skills": sum(1 for _, d in G.nodes(data=True) if d.get("node_type") == "skill"),
        "sources": {
            "ESCO": len(df_occ[df_occ["source"] == "ESCO v1.2.1"]),
            "ONET": len(df_occ[df_occ["source"] == "O*NET 28.1"]),
            "NCO": len(df_occ[df_occ["source"] == "India NCO-2015"])
        },
        "edge_sources": {
            "esco_edges": len(df_esco_rel) if os.path.exists(esco_rel_file) else 0,
            "onet_edges": len(df_onet_rel) if os.path.exists(onet_rel_file) else 0,
            "nco_cross_edges": nco_edge_count
        }
    }
    summary_path = os.path.join(graph_dir, "graph_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"[SUCCESS] Knowledge Graph Built:\n  Nodes: {G.number_of_nodes()} (Occupations: {summary['num_occupations']}, Skills: {summary['num_skills']})\n  Edges: {G.number_of_edges()}")
    print(f"  GraphML: {out_graphml}\n  Edges Parquet: {edges_parquet}\n  Summary: {summary_path}")

if __name__ == "__main__":
    build_graph()
