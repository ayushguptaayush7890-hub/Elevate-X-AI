"""
Prepare graph training pairs and random walk sequences from authentic occupation-skill graph.
Produces:
  datasets/career_transition/interim/graph_train_pairs.parquet
  datasets/career_transition/interim/node_vocab.json
"""

import os
import json
import random
import pandas as pd
import numpy as np

def prepare_graph_data():
    print("=" * 80)
    print("PREPARE GRAPH EMBEDDING TRAINING DATA")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graph_dir = os.path.join(base_dir, "processed", "occupation_skill_graph")
    interim_dir = os.path.join(base_dir, "interim")
    os.makedirs(interim_dir, exist_ok=True)

    edges_file = os.path.join(graph_dir, "edges.parquet")
    df_edges = pd.read_parquet(edges_file)
    print(f"Loaded {len(df_edges)} edges.")

    # Unique nodes
    unique_sources = set(df_edges["source"].astype(str))
    unique_targets = set(df_edges["target"].astype(str))
    all_nodes = sorted(list(unique_sources.union(unique_targets)))
    
    node_to_idx = {node: idx for idx, node in enumerate(all_nodes)}
    idx_to_node = {idx: node for node, idx in node_to_idx.items()}

    print(f"Total vocabulary size: {len(all_nodes)} nodes.")

    vocab_file = os.path.join(interim_dir, "node_vocab.json")
    with open(vocab_file, "w", encoding="utf-8") as f:
        json.dump({"node_to_idx": node_to_idx, "total_nodes": len(all_nodes)}, f)

    # Encode positive pairs
    src_indices = [node_to_idx[s] for s in df_edges["source"].astype(str)]
    tgt_indices = [node_to_idx[t] for t in df_edges["target"].astype(str)]
    weights = df_edges["weight"].astype(float).values

    num_samples = len(src_indices)
    
    # Generate negative pairs via random sampling
    neg_targets = np.random.randint(0, len(all_nodes), size=num_samples)

    train_df = pd.DataFrame({
        "source_idx": src_indices,
        "target_idx": tgt_indices,
        "weight": weights,
        "neg_target_idx": neg_targets
    })

    out_file = os.path.join(interim_dir, "graph_train_pairs.parquet")
    train_df.to_parquet(out_file, index=False)
    print(f"[SUCCESS] Prepared {len(train_df)} training pairs.\n  Saved: {out_file}\n  Vocab: {vocab_file}")

if __name__ == "__main__":
    prepare_graph_data()
