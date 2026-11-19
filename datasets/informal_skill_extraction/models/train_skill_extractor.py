"""
ELEVATE X AI — FEATURE 1: MODEL TRAINING RUNNER & SAFETY GATE
Trains token classification models on the permitted English SkillSpan dataset.
Enforces the strict Training Safety Gate blocking training on Indian worker data
until at least 500 verified, consented genuine field records are collected.
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, get_linear_schedule_with_warmup

from .model_config import ModelConfig, default_config, TAG2ID, ID2TAG, BIO_TAGS
from .dataset_loader import load_skillspan, load_genuine_indian_worker_data, DatasetProvenance
from .model_registry import ModelRegistry, CHECKPOINTS_DIR

class SkillSpanTorchDataset(Dataset):
    def __init__(self, records, tokenizer, max_length=128):
        self.records = records
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        item = self.records[idx]
        tokens = item["tokens"]
        bio_tags = item["bio_tags"]

        # Word-piece subword token alignment
        input_ids = []
        labels = []
        
        for word, tag in zip(tokens, bio_tags):
            subwords = self.tokenizer.tokenize(word)
            if not subwords:
                subwords = [self.tokenizer.unk_token or "[UNK]"]
                
            tag_id = TAG2ID.get(tag, 0)
            for i, sw in enumerate(subwords):
                input_ids.append(self.tokenizer.convert_tokens_to_ids(sw))
                # For subwords after the first, we can mask or use tag_id
                labels.append(tag_id if i == 0 else (TAG2ID["I-SKILL"] if tag == "B-SKILL" else tag_id))

        # Truncate
        if len(input_ids) > self.max_length - 2:
            input_ids = input_ids[:self.max_length - 2]
            labels = labels[:self.max_length - 2]

        # Add special tokens
        cls_id = self.tokenizer.cls_token_id or self.tokenizer.bos_token_id or 101
        sep_id = self.tokenizer.sep_token_id or self.tokenizer.eos_token_id or 102
        
        input_ids = [cls_id] + input_ids + [sep_id]
        labels = [-100] + labels + [-100]  # Mask special tokens in loss
        
        attention_mask = [1] * len(input_ids)
        
        # Padding
        pad_len = self.max_length - len(input_ids)
        if pad_len > 0:
            pad_id = self.tokenizer.pad_token_id or 0
            input_ids = input_ids + [pad_id] * pad_len
            attention_mask = attention_mask + [0] * pad_len
            labels = labels + [-100] * pad_len

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long)
        }

def enforce_training_safety_gate(dataset_target: str):
    """
    Blocks fine-tuning on Indian worker partition if genuine records < 500.
    """
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
                f"Policy: Fine-tuning ML models on synthetic stubs or unverified data is strictly prohibited.\n"
                f"{'='*70}\n"
            )
            print(error_msg, file=sys.stderr)
            raise PermissionError(error_msg)

def run_skillspan_training(
    model_key: str = "xlm_roberta",
    epochs: int = 2,
    batch_size: int = 16,
    max_samples: Optional[int] = 600,
    dataset_target: str = "skillspan"
):
    print("=" * 65)
    print("ELEVATE X AI — FEATURE 1 MODEL TRAINING ENGINE")
    print("=" * 65)
    
    # Check Safety Gate
    enforce_training_safety_gate(dataset_target)
    
    print(f"Dataset Target:      {dataset_target.upper()} (Permitted English Benchmark)")
    print(f"Candidate Model:     {model_key}")
    
    device = ModelRegistry.get_device(prefer_mps=default_config.use_mps)
    print(f"Compute Device:      {device.type.upper()} ({'Apple M2 MPS' if device.type == 'mps' else 'CPU Engine'})")
    
    # 1. Load Data
    print(f"\n[Step 1] Loading official SkillSpan train and dev partitions...")
    train_data = load_skillspan(split="train", max_samples=max_samples)
    dev_data = load_skillspan(split="dev", max_samples=max_samples // 4 if max_samples else None)
    print(f"  Loaded {len(train_data)} train samples, {len(dev_data)} dev samples.")
    
    # 2. Tokenizer & Model
    print(f"\n[Step 2] Loading tokenizer and initializing model architecture...")
    tokenizer = ModelRegistry.load_tokenizer(model_key)
    model = ModelRegistry.load_token_classification_model(
        model_key=model_key,
        num_labels=len(BIO_TAGS)
    )
    
    # Freeze backbone for linear probing on Apple Silicon MPS
    for param in model.roberta.parameters():
        param.requires_grad = False
        
    model.to(device)
    
    train_dataset = SkillSpanTorchDataset(train_data, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # 3. Class-weighted Cross-Entropy Loss to handle 'O' imbalance
    class_weights = torch.tensor([1.0, 14.0, 10.0], dtype=torch.float, device=device)
    loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights, ignore_index=-100)
    
    # Optimizer on classification head only
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable_params, lr=1e-3, weight_decay=1e-4)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(total_steps * 0.1),
        num_training_steps=total_steps
    )
    
    # 4. Training Loop (Model kept in eval mode to freeze backbone and enable MPS SDPA)
    print(f"\n[Step 3] Commencing training across {epochs} epoch(s)...")
    model.eval()
    start_time = time.time()
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        step_count = 0
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            logits = outputs.logits
            loss = loss_fn(logits.view(-1, len(BIO_TAGS)), labels.view(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(trainable_params, max_norm=1.0)
            optimizer.step()
            scheduler.step()
            
            epoch_loss += loss.item()
            step_count += 1
            if step_count % 10 == 0:
                print(f"  Epoch {epoch+1}/{epochs} | Step {step_count}/{len(train_loader)} | Batch Loss: {loss.item():.4f}")
                
        avg_loss = epoch_loss / max(1, step_count)
        print(f"  >> Epoch {epoch+1} Completed. Mean Training Loss: {avg_loss:.4f}")
        
    duration = time.time() - start_time
    print(f"\n[Step 4] Training finished in {duration:.2f} seconds.")
    
    # 5. Save Checkpoint
    checkpoint_dir = CHECKPOINTS_DIR / f"{model_key}_skillspan"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)
    print(f"Saved benchmark checkpoint to: {checkpoint_dir}")
    
    return {
        "status": "completed",
        "model_key": model_key,
        "epochs": epochs,
        "train_samples": len(train_data),
        "mean_loss": round(avg_loss, 4),
        "duration_seconds": round(duration, 2),
        "checkpoint_dir": str(checkpoint_dir)
    }

if __name__ == "__main__":
    run_skillspan_training(max_samples=600, epochs=2, batch_size=16)

