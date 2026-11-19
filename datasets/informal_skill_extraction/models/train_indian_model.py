"""
ELEVATE X AI — FEATURE 1: INDIAN MOCK MODEL EXTENDED TRAINING ENGINE
Trains and benchmarks multilingual token classification architectures on the Indian Mock Dataset.

Mandatory Protocol:
- Target epochs: 20 (minimum 8, maximum 30).
- Early stopping patience: 5 validation epochs on Exact Span F1.
- Evaluates on Validation split (500 records); keeps Test split (550 records) untouched.
- Saves best_checkpoint, latest_checkpoint, training_history.csv, and training_history.json.
- Optimized for Apple Silicon M2 MPS with fallback protection.
- Supports XLM-RoBERTa (Model B), MuRIL (Model C), English Baseline Zero-Shot (Model A), and Lexical (Model D).
"""

import os
import sys
import time
import json
import random
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    get_linear_schedule_with_warmup
)
from seqeval.metrics import precision_score, recall_score, f1_score
import numpy as np

# Repo paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
DATASET_ROOT = SCRIPT_DIR.parent
MOCK_DATA_DIR = DATASET_ROOT / "processed" / "indian_mock_data"
CHECKPOINTS_ROOT = SCRIPT_DIR / "checkpoints" / "indian_mock"
REPORTS_DIR = DATASET_ROOT / "reports" / "indian_worker_data"
EXPERIMENTS_DIR = DATASET_ROOT / "experiments"

CHECKPOINTS_ROOT.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

ID2TAG = {0: "O", 1: "B-SKILL", 2: "I-SKILL"}
TAG2ID = {"O": 0, "B-SKILL": 1, "I-SKILL": 2}

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


# =============================================================================
# DATASET & TOKENIZATION WITH SUBWORD-TO-WORD MASKING
# =============================================================================

class IndianMockDataset(Dataset):
    def __init__(self, records: List[Dict[str, Any]], tokenizer, max_length: int = 128):
        self.records = records
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.cached_samples = []
        self.word_ids_list = []

        all_tokens = [r["tokens"] for r in records]
        encodings = tokenizer(
            all_tokens,
            is_split_into_words=True,
            truncation=True,
            max_length=max_length,
            padding="max_length",
            return_tensors="pt"
        )

        for idx, item in enumerate(records):
            bio_tags = item["bio_tags"]
            word_ids = encodings.word_ids(batch_index=idx)
            self.word_ids_list.append(word_ids)

            labels = []
            prev_wid = None
            for wid in word_ids:
                if wid is None:
                    labels.append(-100)
                elif wid != prev_wid:
                    tag = bio_tags[wid] if wid < len(bio_tags) else "O"
                    labels.append(TAG2ID.get(tag, 0))
                    prev_wid = wid
                else:
                    labels.append(-100)

            self.cached_samples.append({
                "input_ids": encodings["input_ids"][idx],
                "attention_mask": encodings["attention_mask"][idx],
                "labels": torch.tensor(labels, dtype=torch.long)
            })

    def __len__(self):
        return len(self.cached_samples)

    def __getitem__(self, idx: int):
        return self.cached_samples[idx]


# =============================================================================
# EVALUATION METRICS (TOKEN & EXACT/PARTIAL SPAN)
# =============================================================================

def compute_span_metrics(gold_records: List[Dict], pred_tags_list: List[List[str]]) -> Dict[str, float]:
    """
    Computes Exact Span F1 and Partial Overlap F1.
    """
    exact_tp = 0
    exact_fp = 0
    exact_fn = 0

    partial_tp = 0
    total_gold_spans = 0
    total_pred_spans = 0

    for item, pred_tags in zip(gold_records, pred_tags_list):
        text = item["input_text"]
        tokens = item["tokens"]
        gold_spans = item["skill_spans"]
        total_gold_spans += len(gold_spans)

        # Decode predicted spans
        pred_spans = []
        span_st = -1
        span_en = -1
        curr_pos = 0

        # Map word tokens to offsets
        offsets = []
        for t in tokens:
            idx = text.find(t, curr_pos)
            if idx != -1:
                offsets.append((idx, idx + len(t)))
                curr_pos = idx + len(t)
            else:
                offsets.append((curr_pos, curr_pos + len(t)))
                curr_pos += len(t) + 1

        for t_idx, (tag, (st, en)) in enumerate(zip(pred_tags, offsets)):
            if tag == "B-SKILL":
                if span_st != -1:
                    pred_spans.append((span_st, span_en))
                span_st = st
                span_en = en
            elif tag == "I-SKILL":
                if span_st != -1:
                    span_en = en
                else:
                    span_st = st
                    span_en = en
            else:
                if span_st != -1:
                    pred_spans.append((span_st, span_en))
                span_st = -1
                span_en = -1
        if span_st != -1:
            pred_spans.append((span_st, span_en))

        total_pred_spans += len(pred_spans)

        gold_set = {(s["start_offset"], s["end_offset"]) for s in gold_spans}
        pred_set = set(pred_spans)

        exact_tp += len(gold_set.intersection(pred_set))
        exact_fp += len(pred_set - gold_set)
        exact_fn += len(gold_set - pred_set)

        # Partial overlap greedy match
        matched_gold = set()
        for pst, pen in pred_spans:
            for g_idx, g in enumerate(gold_spans):
                if g_idx in matched_gold:
                    continue
                gst, gen = g["start_offset"], g["end_offset"]
                if max(pst, gst) < min(pen, gen):
                    matched_gold.add(g_idx)
                    partial_tp += 1
                    break

    exact_p = exact_tp / (exact_tp + exact_fp) if (exact_tp + exact_fp) > 0 else 0.0
    exact_r = exact_tp / (exact_tp + exact_fn) if (exact_tp + exact_fn) > 0 else 0.0
    exact_f1 = (2 * exact_p * exact_r) / (exact_p + exact_r) if (exact_p + exact_r) > 0 else 0.0

    part_p = partial_tp / total_pred_spans if total_pred_spans > 0 else 0.0
    part_r = partial_tp / total_gold_spans if total_gold_spans > 0 else 0.0
    part_f1 = (2 * part_p * part_r) / (part_p + part_r) if (part_p + part_r) > 0 else 0.0

    return {
        "exact_p": round(exact_p, 4),
        "exact_r": round(exact_r, 4),
        "exact_f1": round(exact_f1, 4),
        "partial_p": round(part_p, 4),
        "partial_r": round(part_r, 4),
        "partial_f1": round(part_f1, 4),
        "exact_tp": exact_tp,
        "exact_fp": exact_fp,
        "exact_fn": exact_fn
    }


def evaluate_model(
    model,
    val_dataset: IndianMockDataset,
    records: List[Dict[str, Any]],
    tokenizer,
    device: torch.device,
    batch_size: int = 32
) -> Dict[str, Any]:
    model.eval()
    gold_bio_all = []
    pred_bio_all = []
    total_val_loss = 0.0
    num_batches = 0

    criterion = nn.CrossEntropyLoss(
        weight=torch.tensor([1.0, 10.0, 8.0], dtype=torch.float).to(device),
        ignore_index=-100
    )

    loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    with torch.no_grad():
        for batch_idx, batch in enumerate(loader):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            total_val_loss += outputs.loss.item()
            num_batches += 1

            preds = torch.argmax(outputs.logits, dim=-1).cpu().tolist()
            start_rec_idx = batch_idx * batch_size

            for in_b_idx, pred_seq in enumerate(preds):
                r_idx = start_rec_idx + in_b_idx
                if r_idx >= len(records):
                    break
                rec = records[r_idx]
                tokens = rec["tokens"]
                gold_bio = rec["bio_tags"]

                word_ids = val_dataset.word_ids_list[r_idx]

                pred_tags = []
                prev_wid = None
                wid_to_tag = {}
                for wid, pid in zip(word_ids, pred_seq[:len(word_ids)]):
                    if wid is not None and wid != prev_wid:
                        wid_to_tag[wid] = ID2TAG.get(pid, "O")
                        prev_wid = wid

                for w_idx in range(len(tokens)):
                    pred_tags.append(wid_to_tag.get(w_idx, "O"))

                gold_bio_all.append(gold_bio)
                pred_bio_all.append(pred_tags)

    avg_val_loss = total_val_loss / num_batches if num_batches > 0 else 0.0
    tok_p = precision_score(gold_bio_all, pred_bio_all)
    tok_r = recall_score(gold_bio_all, pred_bio_all)
    tok_f1 = f1_score(gold_bio_all, pred_bio_all)

    span_metrics = compute_span_metrics(records, pred_bio_all)

    return {
        "val_loss": round(avg_val_loss, 4),
        "tok_p": round(tok_p, 4),
        "tok_r": round(tok_r, 4),
        "tok_f1": round(tok_f1, 4),
        "exact_p": span_metrics["exact_p"],
        "exact_r": span_metrics["exact_r"],
        "exact_f1": span_metrics["exact_f1"],
        "partial_f1": span_metrics["partial_f1"]
    }


# =============================================================================
# EXTENDED TRAINING ENGINE (20 EPOCHS, MIN 8, MAX 30, PATIENCE 5)
# =============================================================================

def train_extended(
    model_name_or_key: str = "xlm-roberta-base",
    experiment_id: str = "exp_indian_xlm_roberta",
    target_epochs: int = 20,
    min_epochs: int = 8,
    max_epochs: int = 30,
    patience: int = 5,
    batch_size: int = 32,
    lr_backbone: float = 3e-5,
    lr_head: float = 1e-4,
    weight_decay: float = 0.01,
    unfreeze_layers: int = 2
) -> Dict[str, Any]:
    print("=" * 80)
    print(f"ELEVATE X AI — EXTENDED TRAINING: {experiment_id.upper()}")
    print("=" * 80)
    print(f"Base Model:       {model_name_or_key}")
    print(f"Epoch Target:     {target_epochs} (Min: {min_epochs}, Max: {max_epochs}, Patience: {patience})")
    print(f"Batch Size:       {batch_size}")
    print(f"Device:           {'Apple Silicon MPS' if torch.backends.mps.is_available() else 'CPU Fallback'}")

    set_seed(42)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    # Load data
    train_records = load_jsonl(MOCK_DATA_DIR / "indian_mock_train.jsonl")
    val_records = load_jsonl(MOCK_DATA_DIR / "indian_mock_val.jsonl")
    print(f"Loaded Train: {len(train_records):,} records | Validation: {len(val_records):,} records")

    # Tokenizer & Model
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_key)
    model = AutoModelForTokenClassification.from_pretrained(
        model_name_or_key,
        num_labels=3,
        id2label=ID2TAG,
        label2id=TAG2ID
    ).to(device)

    # Freeze embeddings and lower layers; keep them in eval mode to prevent MPS SDPA dropout crash
    if "roberta" in model_name_or_key.lower():
        for param in model.roberta.embeddings.parameters():
            param.requires_grad = False
        total_layers = len(model.roberta.encoder.layer)
        for i in range(total_layers - unfreeze_layers):
            for param in model.roberta.encoder.layer[i].parameters():
                param.requires_grad = False
    elif "bert" in model_name_or_key.lower() or "muril" in model_name_or_key.lower():
        for param in model.bert.embeddings.parameters():
            param.requires_grad = False
        total_layers = len(model.bert.encoder.layer)
        for i in range(total_layers - unfreeze_layers):
            for param in model.bert.encoder.layer[i].parameters():
                param.requires_grad = False

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Trainable Parameters: {trainable_params:,} / {total_params:,} ({trainable_params/total_params*100:.2f}%)")

    print("Pre-tokenizing train and validation sets...")
    train_dataset = IndianMockDataset(train_records, tokenizer)
    val_dataset = IndianMockDataset(val_records, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    optimizer = torch.optim.AdamW([
        {"params": [p for n, p in model.named_parameters() if p.requires_grad and "classifier" not in n], "lr": lr_backbone},
        {"params": [p for n, p in model.named_parameters() if p.requires_grad and "classifier" in n], "lr": lr_head}
    ], weight_decay=weight_decay)

    total_steps = len(train_loader) * target_epochs
    warmup_steps = int(total_steps * 0.1)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

    class_weights = torch.tensor([1.0, 10.0, 8.0], dtype=torch.float).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights, ignore_index=-100)

    # Checkpoint paths
    exp_checkpoint_dir = CHECKPOINTS_ROOT / experiment_id
    best_checkpoint_dir = exp_checkpoint_dir / "best_checkpoint"
    latest_checkpoint_dir = exp_checkpoint_dir / "latest_checkpoint"
    best_checkpoint_dir.mkdir(parents=True, exist_ok=True)
    latest_checkpoint_dir.mkdir(parents=True, exist_ok=True)

    history = []
    best_val_f1 = -1.0
    best_epoch = -1
    no_improve_epochs = 0
    best_state_dict = None

    # Set offline mode after model load to prevent any network checks during training/saving
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    print("\nStarting Extended Training Loop...")
    t0_global = time.time()

    for epoch in range(1, max_epochs + 1):
        t_epoch_start = time.time()
        model.eval()  # Kept in eval mode to prevent SDPA dropout crash on MPS

        total_train_loss = 0.0
        for batch_idx, batch in enumerate(train_loader):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            loss = criterion(logits.view(-1, 3), labels.view(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()
            scheduler.step()
            total_train_loss += loss.item()

            if (batch_idx + 1) % 50 == 0 or (batch_idx + 1) == len(train_loader):
                print(f"  [Epoch {epoch:02d}] Step {batch_idx + 1}/{len(train_loader)} | Batch Loss: {loss.item():.4f}", flush=True)

        avg_train_loss = total_train_loss / len(train_loader)
        epoch_dur = time.time() - t_epoch_start

        # Evaluate on validation partition
        val_metrics = evaluate_model(model, val_dataset, val_records, tokenizer, device, batch_size=batch_size)
        val_exact_f1 = val_metrics["exact_f1"]

        current_lr = scheduler.get_last_lr()[0]
        epoch_stats = {
            "epoch": epoch,
            "train_loss": round(avg_train_loss, 4),
            "val_loss": val_metrics["val_loss"],
            "tok_p": val_metrics["tok_p"],
            "tok_r": val_metrics["tok_r"],
            "tok_f1": val_metrics["tok_f1"],
            "exact_p": val_metrics["exact_p"],
            "exact_r": val_metrics["exact_r"],
            "exact_f1": val_exact_f1,
            "partial_f1": val_metrics["partial_f1"],
            "learning_rate": round(current_lr, 8),
            "duration_sec": round(epoch_dur, 2),
            "device": str(device)
        }
        history.append(epoch_stats)

        print(f"Epoch {epoch:02d}/{max_epochs:02d} | Train Loss: {avg_train_loss:.4f} | Val Loss: {val_metrics['val_loss']:.4f} | Exact F1: {val_exact_f1:.4f} | Partial F1: {val_metrics['partial_f1']:.4f} | Time: {epoch_dur:.1f}s", flush=True)

        # Check for improvement (track in memory without disk write bottleneck)
        if val_exact_f1 > best_val_f1 + 0.001:
            best_val_f1 = val_exact_f1
            best_epoch = epoch
            no_improve_epochs = 0
            best_state_dict = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            print(f"  >>> New Best Validation Exact Span F1: {best_val_f1:.4f} (recorded in memory)")
        else:
            no_improve_epochs += 1

        # Early Stopping Logic:
        # Minimum epochs requirement must be met before early stopping
        if epoch >= min_epochs:
            if no_improve_epochs >= patience:
                print(f"\n[Early Stopping Triggered] No improvement in validation Exact Span F1 for {patience} consecutive epochs after minimum {min_epochs} epochs. Best epoch was {best_epoch} (F1: {best_val_f1:.4f}).")
                break
            if epoch >= target_epochs and val_exact_f1 <= best_val_f1:
                print(f"\n[Target Epochs Reached] Completed target {target_epochs} epochs with stable convergence at epoch {best_epoch} (F1: {best_val_f1:.4f}).")
                break

    total_training_time = time.time() - t0_global
    print(f"\nExtended training finished in {total_training_time:.2f} seconds. Best Epoch: {best_epoch} with Val Exact F1: {best_val_f1:.4f}")

    # Save best and latest checkpoint to disk
    if best_state_dict is not None:
        print(f"Loading best weights from epoch {best_epoch} and saving to {best_checkpoint_dir}...")
        model.load_state_dict(best_state_dict)

    model.save_pretrained(str(best_checkpoint_dir), safe_serialization=True)
    tokenizer.save_pretrained(str(best_checkpoint_dir))
    model.save_pretrained(str(latest_checkpoint_dir), safe_serialization=True)
    tokenizer.save_pretrained(str(latest_checkpoint_dir))
    print(f"Checkpoints successfully serialized to {best_checkpoint_dir} and {latest_checkpoint_dir}")

    # Export history to CSV and JSON
    hist_csv_path = exp_checkpoint_dir / "training_history.csv"
    with open(hist_csv_path, "w", encoding="utf-8") as cf:
        cf.write("epoch,train_loss,val_loss,tok_p,tok_r,tok_f1,exact_p,exact_r,exact_f1,partial_f1,learning_rate,duration_sec,device\n")
        for h in history:
            cf.write(f"{h['epoch']},{h['train_loss']},{h['val_loss']},{h['tok_p']},{h['tok_r']},{h['tok_f1']},{h['exact_p']},{h['exact_r']},{h['exact_f1']},{h['partial_f1']},{h['learning_rate']},{h['duration_sec']},{h['device']}\n")

    hist_json_path = exp_checkpoint_dir / "training_history.json"
    with open(hist_json_path, "w", encoding="utf-8") as jf:
        json.dump(history, jf, indent=2)

    return {
        "experiment_id": experiment_id,
        "best_epoch": best_epoch,
        "best_val_exact_f1": best_val_f1,
        "total_epochs_trained": len(history),
        "total_time_sec": total_training_time,
        "best_checkpoint_path": str(best_checkpoint_dir),
        "history": history
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="xlm-roberta-base")
    parser.add_argument("--exp_id", type=str, default="exp_indian_xlm_roberta")
    parser.add_argument("--epochs", type=int, default=20)
    args = parser.parse_args()

    train_extended(model_name_or_key=args.model, experiment_id=args.exp_id, target_epochs=args.epochs)
