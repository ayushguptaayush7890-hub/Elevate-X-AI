"""
Generates the formal Extended Model Training Report for Feature 1 Phase 2.
"""

import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_ROOT = SCRIPT_DIR.parent
REPORTS_DIR = DATASET_ROOT / "reports" / "indian_worker_data"
EXP_DIR = SCRIPT_DIR / "checkpoints" / "indian_mock" / "exp_indian_xlm_roberta"

def generate_report():
    hist_path = EXP_DIR / "training_history.json"
    if not hist_path.exists():
        print(f"Waiting for {hist_path} to be generated...")
        return False

    with open(hist_path, "r", encoding="utf-8") as f:
        history = json.load(f)

    report_path = REPORTS_DIR / "feature1_indian_model_training_report.md"
    
    best_entry = max(history, key=lambda x: x["exact_f1"])
    total_time = sum(h["duration_sec"] for h in history)

    content = f"""# ELEVATE X AI — FEATURE 1: MODEL TRAINING & CONVERGENCE REPORT
## Extended Multilingual Training on Indian Mock Dataset (Phase 2)

> **PROVENANCE NOTICE:** All training and validation metrics below are computed on the **Synthetic Indian Mock Development Dataset** (Train: 4,150 records, Val: 500 records). Genuine Indian worker records stand at 0. Real-world Indian worker fine-tuning remains locked until 500 verified records are collected.

---

### 1. Training Configuration & Architecture
- **Experiment Identifier:** `exp_indian_xlm_roberta`
- **Base Architecture:** `xlm-roberta-base` (277.4M total parameters)
- **Trainable Parameters:** `14,178,051` (5.11%) — Top 2 transformer encoder layers + 3-class token classification head
- **Target Epochs:** 20 (Min: 8, Max: 30, Early Stopping Patience: 5 on Validation Exact Span F1)
- **Batch Size:** 32
- **Optimizer:** AdamW (`lr_backbone = 3e-5`, `lr_head = 1e-4`, `weight_decay = 0.01`)
- **Learning Rate Schedule:** Linear warmup for 10% of total steps followed by linear decay
- **Loss Function:** Class-Weighted Cross-Entropy (`[O: 1.0, B-SKILL: 10.0, I-SKILL: 8.0]`, `ignore_index = -100`)
- **Hardware Acceleration:** Apple Silicon M2 MPS (Metal Performance Shaders) with CPU fallback
- **Dataset Partitioning:** 80% Train (4,150), 10% Validation (500), 10% Test (550 untouched)

---

### 2. Epoch-by-Epoch Convergence History

| Epoch | Train Loss | Val Loss | Token Precision | Token Recall | Token F1 | Exact Span P | Exact Span R | Exact Span F1 | Partial Overlap F1 | Duration (s) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
"""

    for h in history:
        is_best = " **(Best)**" if h["epoch"] == best_entry["epoch"] else ""
        content += f"| {h['epoch']:02d}{is_best} | {h['train_loss']:.4f} | {h['val_loss']:.4f} | {h['tok_p']:.4f} | {h['tok_r']:.4f} | {h['tok_f1']:.4f} | {h['exact_p']:.4f} | {h['exact_r']:.4f} | **{h['exact_f1']:.4f}** | {h['partial_f1']:.4f} | {h['duration_sec']:.1f}s |\n"

    content += f"""
---

### 3. Training Milestone Summary
- **Best Validation Epoch:** Epoch `{best_entry['epoch']}`
- **Peak Validation Exact Span F1:** `{best_entry['exact_f1']:.4f}`
- **Peak Validation Partial Overlap F1:** `{best_entry['partial_f1']:.4f}`
- **Peak Validation Token F1 (seqeval):** `{best_entry['tok_f1']:.4f}`
- **Total Training Duration:** `{total_time:.1f} seconds` ({total_time / 60:.2f} minutes)
- **Early Stopping Trigger:** Completed minimum required epochs with early stopping patience tracking on validation Exact Span F1.
- **Checkpoint Serialization:** Best weights saved to `datasets/informal_skill_extraction/models/checkpoints/indian_mock/exp_indian_xlm_roberta/best_checkpoint/` with offline Hugging Face safetensors format.
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Training report successfully generated at {report_path}")
    return True

if __name__ == "__main__":
    generate_report()

