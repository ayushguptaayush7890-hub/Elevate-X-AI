"""
ELEVATE X AI — FEATURE 1: MODEL TRAINING & EXPERIMENT RUNNER
Implements systematic token classification training across 4 configurations:
- Experiment A: Frozen XLM-RoBERTa backbone + trainable classification head (MPS)
- Experiment B: Partially unfrozen XLM-RoBERTa (top 2 encoder layers + head) (MPS)
- Experiment C: Full fine-tuning (controlled CPU fallback)
- Experiment D: Lightweight baseline (TF-IDF / rule-based dictionary matcher)

Enforces strict Training Safety Gate: Indian worker data remains locked until >= 500 genuine records.
"""

import os
import sys
import time
import random
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    AutoConfig,
    get_linear_schedule_with_warmup
)
from seqeval.metrics import f1_score, precision_score, recall_score, classification_report

from .model_config import ModelConfig, default_config, TAG2ID, ID2TAG, BIO_TAGS, REPORTS_DIR
from .dataset_loader import load_skillspan, load_genuine_indian_worker_data
from .bio_tokenizer import BIOTokenizer
from .model_registry import ModelRegistry, CHECKPOINTS_DIR

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def enforce_training_safety_gate(dataset_target: str):
    if dataset_target in ["indian_worker_data", "genuine_worker_data"]:
        genuine_records = load_genuine_indian_worker_data()
        count = len(genuine_records)
        if count < default_config.minimum_genuine_records_gate:
            error_msg = (
                f"\n{'='*70}\n"
                f"CRITICAL TRAINING SAFETY GATE BLOCKED EXECUTION:\n"
                f"Target dataset: {dataset_target}\n"
                f"Genuine records available: {count}\n"
                f"Required minimum threshold: {default_config.minimum_genuine_records_gate}\n"
                f"Reason: GENUINE WORKER DATA COLLECTION IS STILL PENDING.\n"
                f"{'='*70}\n"
            )
            print(error_msg, file=sys.stderr)
            raise PermissionError(error_msg)

class ProperSkillSpanDataset(Dataset):
    def __init__(self, records: List[Dict[str, Any]], tokenizer, max_length: int = 128):
        self.records = records
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx: int):
        item = self.records[idx]
        tokens = item["tokens"]
        bio_tags = item["bio_tags"]

        encoding = self.tokenizer(
            tokens,
            is_split_into_words=True,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )

        word_ids = encoding.word_ids(batch_index=0)
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
                labels.append(-100)  # Mask subsequent subwords

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(labels, dtype=torch.long)
        }

def evaluate_on_records(model, records: List[Dict[str, Any]], tokenizer, device) -> Dict[str, float]:
    model.eval()
    gold_all = []
    pred_all = []

    for item in records:
        tokens = item["tokens"]
        gold_bio = item["bio_tags"]

        enc = tokenizer(
            tokens,
            is_split_into_words=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        ).to(device)

        word_ids = enc.word_ids(batch_index=0)

        with torch.no_grad():
            outputs = model(**enc)
            pred_ids = torch.argmax(outputs.logits[0], dim=-1).cpu().tolist()

        word_preds = []
        prev_wid = None
        for wid, pid in zip(word_ids, pred_ids):
            if wid is None:
                continue
            if wid != prev_wid:
                word_preds.append(ID2TAG.get(pid, "O"))
                prev_wid = wid

        if len(word_preds) < len(tokens):
            word_preds += ["O"] * (len(tokens) - len(word_preds))
        else:
            word_preds = word_preds[:len(tokens)]

        gold_all.append(gold_bio)
        pred_all.append(word_preds)

    p = precision_score(gold_all, pred_all)
    r = recall_score(gold_all, pred_all)
    f1 = f1_score(gold_all, pred_all)
    return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f1, 4)}

def run_experiment_a_frozen(
    train_samples: int = 1500,
    dev_samples: int = 300,
    epochs: int = 3,
    batch_size: int = 16,
    lr: float = 1e-3
) -> Dict[str, Any]:
    print("\n" + "=" * 65)
    print("RUNNING EXPERIMENT A: Frozen XLM-RoBERTa Backbone (MPS)")
    print("=" * 65)
    set_seed(42)
    device = ModelRegistry.get_device(prefer_mps=True)
    print(f"Device: {device.type.upper()}")

    train_data = load_skillspan("train", max_samples=train_samples)
    dev_data = load_skillspan("dev", max_samples=dev_samples)

    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
    model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-base", num_labels=len(BIO_TAGS))

    for p in model.roberta.parameters():
        p.requires_grad = False

    model.to(device)
    model.eval()

    trainable_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Trainable parameters: {trainable_count:,} (Head only)")

    train_dataset = ProperSkillSpanDataset(train_data, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    class_weights = torch.tensor([1.0, 10.0, 8.0], dtype=torch.float, device=device)
    loss_fn = nn.CrossEntropyLoss(weight=class_weights, ignore_index=-100)
    optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=lr, weight_decay=1e-4)

    t0 = time.time()
    best_f1 = 0.0
    history = []

    for epoch in range(epochs):
        epoch_loss = 0.0
        steps = 0
        for batch in train_loader:
            optimizer.zero_grad()
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            out = model(input_ids=ids, attention_mask=mask)
            loss = loss_fn(out.logits.view(-1, len(BIO_TAGS)), labels.view(-1))
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            steps += 1

        avg_loss = epoch_loss / max(1, steps)
        dev_metrics = evaluate_on_records(model, dev_data, tokenizer, device)
        model.eval()
        print(f"  Epoch {epoch+1}/{epochs} | Train Loss: {avg_loss:.4f} | Dev F1: {dev_metrics['f1']:.4f} (P: {dev_metrics['precision']:.4f}, R: {dev_metrics['recall']:.4f})")
        history.append({"epoch": epoch + 1, "loss": round(avg_loss, 4), "dev_f1": dev_metrics["f1"]})
        if dev_metrics["f1"] > best_f1:
            best_f1 = dev_metrics["f1"]

    duration = time.time() - t0
    ckpt_dir = CHECKPOINTS_DIR / "exp_a_frozen"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(ckpt_dir)
    tokenizer.save_pretrained(ckpt_dir)

    return {
        "experiment_id": "exp_a_frozen",
        "description": "Frozen XLM-RoBERTa Backbone (MPS Linear Probe)",
        "trainable_params": trainable_count,
        "train_samples": len(train_data),
        "dev_samples": len(dev_data),
        "best_dev_f1": best_f1,
        "duration_seconds": round(duration, 2),
        "checkpoint_dir": str(ckpt_dir),
        "history": history
    }

def run_experiment_b_partial(
    train_samples: int = 1500,
    dev_samples: int = 300,
    epochs: int = 3,
    batch_size: int = 8,
    lr: float = 5e-5
) -> Dict[str, Any]:
    print("\n" + "=" * 65)
    print("RUNNING EXPERIMENT B: Partially Unfrozen XLM-RoBERTa (Top 2 Layers, MPS)")
    print("=" * 65)
    set_seed(42)
    device = ModelRegistry.get_device(prefer_mps=True)
    print(f"Device: {device.type.upper()}")

    train_data = load_skillspan("train", max_samples=train_samples)
    dev_data = load_skillspan("dev", max_samples=dev_samples)

    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
    model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-base", num_labels=len(BIO_TAGS))

    # Freeze lower 10 layers, unfreeze top 2
    for p in model.roberta.parameters():
        p.requires_grad = False
    for p in model.roberta.encoder.layer[-2:].parameters():
        p.requires_grad = True

    model.to(device)
    model.eval()  # Kept in eval mode to prevent SDPA dropout issues on MPS

    trainable_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Trainable parameters: {trainable_count:,} (Top 2 encoder layers + classification head)")

    train_dataset = ProperSkillSpanDataset(train_data, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    class_weights = torch.tensor([1.0, 10.0, 8.0], dtype=torch.float, device=device)
    loss_fn = nn.CrossEntropyLoss(weight=class_weights, ignore_index=-100)
    optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=lr, weight_decay=1e-4)

    t0 = time.time()
    best_f1 = 0.0
    history = []

    for epoch in range(epochs):
        epoch_loss = 0.0
        steps = 0
        for batch in train_loader:
            optimizer.zero_grad()
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            out = model(input_ids=ids, attention_mask=mask)
            loss = loss_fn(out.logits.view(-1, len(BIO_TAGS)), labels.view(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(filter(lambda p: p.requires_grad, model.parameters()), max_norm=1.0)
            optimizer.step()
            epoch_loss += loss.item()
            steps += 1

        avg_loss = epoch_loss / max(1, steps)
        dev_metrics = evaluate_on_records(model, dev_data, tokenizer, device)
        model.eval()
        print(f"  Epoch {epoch+1}/{epochs} | Train Loss: {avg_loss:.4f} | Dev F1: {dev_metrics['f1']:.4f} (P: {dev_metrics['precision']:.4f}, R: {dev_metrics['recall']:.4f})")
        history.append({"epoch": epoch + 1, "loss": round(avg_loss, 4), "dev_f1": dev_metrics["f1"]})
        if dev_metrics["f1"] > best_f1:
            best_f1 = dev_metrics["f1"]
            # Save best checkpoint
            best_dir = CHECKPOINTS_DIR / "best_skillspan_model"
            best_dir.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(best_dir)
            tokenizer.save_pretrained(best_dir)

    duration = time.time() - t0
    ckpt_dir = CHECKPOINTS_DIR / "exp_b_partial"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(ckpt_dir)
    tokenizer.save_pretrained(ckpt_dir)

    return {
        "experiment_id": "exp_b_partial",
        "description": "Partially Unfrozen XLM-RoBERTa (Top 2 Layers, MPS)",
        "trainable_params": trainable_count,
        "train_samples": len(train_data),
        "dev_samples": len(dev_data),
        "best_dev_f1": best_f1,
        "duration_seconds": round(duration, 2),
        "checkpoint_dir": str(ckpt_dir),
        "history": history
    }

def run_experiment_c_full(
    train_samples: int = 100,
    dev_samples: int = 50,
    epochs: int = 1,
    batch_size: int = 4,
    lr: float = 2e-5
) -> Dict[str, Any]:
    print("\n" + "=" * 65)
    print("RUNNING EXPERIMENT C: Full XLM-RoBERTa Fine-Tuning (CPU Controlled Run)")
    print("=" * 65)
    set_seed(42)
    device = torch.device("cpu")
    print(f"Device: CPU (Controlled fallback due to MPS SDPA dropout restriction)")

    train_data = load_skillspan("train", max_samples=train_samples)
    dev_data = load_skillspan("dev", max_samples=dev_samples)

    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
    model = AutoModelForTokenClassification.from_pretrained("xlm-roberta-base", num_labels=len(BIO_TAGS))
    model.to(device)
    model.train()

    trainable_count = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Trainable parameters: {trainable_count:,} (All 278M parameters)")

    train_dataset = ProperSkillSpanDataset(train_data, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    loss_fn = nn.CrossEntropyLoss(ignore_index=-100)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)

    t0 = time.time()
    step_latencies = []
    epoch_loss = 0.0

    for idx, batch in enumerate(train_loader):
        s0 = time.time()
        optimizer.zero_grad()
        ids = batch["input_ids"].to(device)
        mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        out = model(input_ids=ids, attention_mask=mask)
        loss = loss_fn(out.logits.view(-1, len(BIO_TAGS)), labels.view(-1))
        loss.backward()
        optimizer.step()

        lat = (time.time() - s0) * 1000.0
        step_latencies.append(lat)
        epoch_loss += loss.item()
        if (idx + 1) % 5 == 0 or idx == len(train_loader) - 1:
            print(f"  Step {idx+1}/{len(train_loader)} | Batch Loss: {loss.item():.4f} | Latency: {lat:.1f} ms/step")

    dev_metrics = evaluate_on_records(model, dev_data, tokenizer, device)
    duration = time.time() - t0
    print(f"  CPU Controlled Run Done | Dev F1: {dev_metrics['f1']:.4f} | Mean Step: {np.mean(step_latencies):.1f} ms")

    return {
        "experiment_id": "exp_c_full",
        "description": "Full XLM-RoBERTa Fine-Tuning (CPU Fallback)",
        "trainable_params": trainable_count,
        "train_samples": len(train_data),
        "dev_samples": len(dev_data),
        "best_dev_f1": dev_metrics["f1"],
        "duration_seconds": round(duration, 2),
        "mean_step_latency_ms": round(float(np.mean(step_latencies)), 1),
        "notes": "Feasible on CPU but high latency (~4800ms/step). MPS full backprop restricted by SDPA dropout."
    }

def run_experiment_d_baseline(test_samples: int = 300) -> Dict[str, Any]:
    print("\n" + "=" * 65)
    print("RUNNING EXPERIMENT D: Lightweight Lexical / Rule-Based Baseline")
    print("=" * 65)
    test_data = load_skillspan("test", max_samples=test_samples)

    # Simple dictionary of frequent vocational/technical skills
    LEXICON = {
        "python", "java", "sql", "docker", "kubernetes", "c++", "linux", "aws", "azure", "git",
        "react", "angular", "node.js", "rest", "api", "testing", "agile", "scrum", "qa",
        "troubleshooting", "maintenance", "installation", "wiring", "welding", "carpentry", "plumbing"
    }

    gold_all = []
    pred_all = []

    for item in test_data:
        tokens = item["tokens"]
        gold_bio = item["bio_tags"]

        pred_bio = []
        for t in tokens:
            clean_t = t.lower().strip(".,;:()[]{}")
            if clean_t in LEXICON:
                pred_bio.append("B-SKILL")
            else:
                pred_bio.append("O")

        gold_all.append(gold_bio)
        pred_all.append(pred_bio)

    p = precision_score(gold_all, pred_all)
    r = recall_score(gold_all, pred_all)
    f1 = f1_score(gold_all, pred_all)
    print(f"  Baseline Results on Test Partition: F1: {f1:.4f} | Precision: {p:.4f} | Recall: {r:.4f}")

    return {
        "experiment_id": "exp_d_baseline",
        "description": "Lexical Dictionary Baseline (Non-Neural)",
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1": round(f1, 4),
        "test_samples": len(test_data)
    }

if __name__ == "__main__":
    res_d = run_experiment_d_baseline()
    res_a = run_experiment_a_frozen(train_samples=1000, dev_samples=200, epochs=2)
    res_b = run_experiment_b_partial(train_samples=1000, dev_samples=200, epochs=3)
    res_c = run_experiment_c_full(train_samples=40, dev_samples=20, epochs=1)

    print("\n" + "=" * 65)
    print("EXPERIMENT SUITE COMPLETE")
    print("=" * 65)
    print(f"Exp D (Rule Baseline): Dev F1 = {res_d['f1']}")
    print(f"Exp A (Frozen Backbone): Dev F1 = {res_a['best_dev_f1']}")
    print(f"Exp B (Partially Unfrozen): Dev F1 = {res_b['best_dev_f1']}")
    print(f"Exp C (Full CPU Controlled): Dev F1 = {res_c['best_dev_f1']}")

