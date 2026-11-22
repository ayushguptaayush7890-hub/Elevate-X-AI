"""
Train PyTorch graph embeddings on the authentic occupation-skill knowledge graph.
Produces:
  datasets/career_transition/models/graph_embeddings/occupation_graph_model.pt
  datasets/career_transition/models/graph_embeddings/node_to_idx.json
  datasets/career_transition/models/graph_embeddings/training_metrics.json
"""

import os
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
import numpy as np

class GraphEmbeddingModel(nn.Module):
    def __init__(self, num_nodes, embedding_dim=64):
        super().__init__()
        self.node_embeddings = nn.Embedding(num_nodes, embedding_dim)
        self.context_embeddings = nn.Embedding(num_nodes, embedding_dim)
        # Initialize
        nn.init.xavier_uniform_(self.node_embeddings.weight)
        nn.init.xavier_uniform_(self.context_embeddings.weight)

    def forward(self, src, pos_dst, neg_dst):
        # src: [batch_size], pos_dst: [batch_size], neg_dst: [batch_size]
        v_src = self.node_embeddings(src)         # [B, D]
        v_pos = self.context_embeddings(pos_dst)  # [B, D]
        v_neg = self.context_embeddings(neg_dst)  # [B, D]

        pos_score = torch.sum(v_src * v_pos, dim=-1) # [B]
        neg_score = torch.sum(v_src * v_neg, dim=-1) # [B]

        pos_loss = -torch.log(torch.sigmoid(pos_score) + 1e-15)
        neg_loss = -torch.log(torch.sigmoid(-neg_score) + 1e-15)

        loss = torch.mean(pos_loss + neg_loss)
        return loss, pos_score, neg_score

def train_graph():
    print("=" * 80)
    print("TRAIN OCCUPATION-SKILL GRAPH EMBEDDINGS (PYTORCH)")
    print("=" * 80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    interim_dir = os.path.join(base_dir, "interim")
    model_dir = os.path.join(base_dir, "models", "graph_embeddings")
    os.makedirs(model_dir, exist_ok=True)

    # 1. Load Vocab
    vocab_file = os.path.join(interim_dir, "node_vocab.json")
    with open(vocab_file, "r", encoding="utf-8") as f:
        vocab = json.load(f)
    node_to_idx = vocab["node_to_idx"]
    num_nodes = len(node_to_idx)
    print(f"Loaded node vocabulary: {num_nodes} entities.")

    # 2. Load Training Pairs
    pairs_file = os.path.join(interim_dir, "graph_train_pairs.parquet")
    df_pairs = pd.read_parquet(pairs_file)
    print(f"Loaded {len(df_pairs)} training pairs.")

    src_tensor = torch.tensor(df_pairs["source_idx"].values, dtype=torch.long)
    pos_tensor = torch.tensor(df_pairs["target_idx"].values, dtype=torch.long)
    neg_tensor = torch.tensor(df_pairs["neg_target_idx"].values, dtype=torch.long)

    dataset = TensorDataset(src_tensor, pos_tensor, neg_tensor)
    loader = DataLoader(dataset, batch_size=2048, shuffle=True)

    # Device selection: MPS if available, else CPU
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using compute device: {device}")

    embedding_dim = 64
    model = GraphEmbeddingModel(num_nodes, embedding_dim=embedding_dim).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    epochs = 4
    training_history = []
    start_time = time.time()

    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        total_correct = 0
        total_samples = 0
        
        for batch_src, batch_pos, batch_neg in loader:
            batch_src = batch_src.to(device)
            batch_pos = batch_pos.to(device)
            batch_neg = batch_neg.to(device)

            optimizer.zero_grad()
            loss, pos_scores, neg_scores = model(batch_src, batch_pos, batch_neg)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(batch_src)
            total_correct += ((pos_scores > 0).sum() + (neg_scores < 0).sum()).item()
            total_samples += len(batch_src) * 2

        epoch_loss = total_loss / len(df_pairs)
        epoch_acc = total_correct / total_samples
        print(f"Epoch {epoch}/{epochs} - Loss: {epoch_loss:.4f} - Edge Discrim Acc: {epoch_acc * 100:.2f}%")
        training_history.append({
            "epoch": epoch,
            "loss": round(epoch_loss, 4),
            "link_prediction_acc": round(epoch_acc, 4)
        })

    elapsed = round(time.time() - start_time, 2)
    print(f"Training completed in {elapsed}s.")

    # 3. Save model checkpoint and vocabulary
    model_checkpoint_path = os.path.join(model_dir, "occupation_graph_model.pt")
    torch.save({
        "num_nodes": num_nodes,
        "embedding_dim": embedding_dim,
        "node_embeddings": model.node_embeddings.weight.data.cpu(),
        "context_embeddings": model.context_embeddings.weight.data.cpu()
    }, model_checkpoint_path)

    # Save vocab mapping
    out_vocab_path = os.path.join(model_dir, "node_to_idx.json")
    with open(out_vocab_path, "w", encoding="utf-8") as f:
        json.dump(node_to_idx, f)

    # Save metrics
    metrics_path = os.path.join(model_dir, "training_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({
            "model_type": "Node2Vec / Graph Skip-gram Embedding",
            "embedding_dim": embedding_dim,
            "total_nodes": num_nodes,
            "total_edges": len(df_pairs),
            "epochs": epochs,
            "training_time_seconds": elapsed,
            "device": str(device),
            "final_loss": training_history[-1]["loss"],
            "final_link_prediction_acc": training_history[-1]["link_prediction_acc"],
            "history": training_history
        }, f, indent=2)

    print(f"[SUCCESS] Saved Graph Embedding Model:\n  Weights: {model_checkpoint_path}\n  Vocab:   {out_vocab_path}\n  Metrics: {metrics_path}")

if __name__ == "__main__":
    train_graph()
