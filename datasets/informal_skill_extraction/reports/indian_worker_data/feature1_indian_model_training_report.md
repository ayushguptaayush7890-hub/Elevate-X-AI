# ELEVATE X AI — FEATURE 1: MODEL TRAINING & CONVERGENCE REPORT
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
| 01 | 0.8016 | 0.4679 | 0.3350 | 0.5350 | 0.4120 | 0.2585 | 0.4128 | **0.3179** | 0.7663 | 126.1s |
| 02 | 0.1250 | 0.0671 | 0.7988 | 0.8956 | 0.8444 | 0.6573 | 0.7369 | **0.6948** | 0.9429 | 145.4s |
| 03 | 0.0253 | 0.0432 | 0.8927 | 0.9340 | 0.9129 | 0.7392 | 0.7734 | **0.7559** | 0.9774 | 139.4s |
| 04 | 0.0097 | 0.0240 | 0.9432 | 0.9655 | 0.9542 | 0.7854 | 0.8039 | **0.7945** | 0.9883 | 86.1s |
| 05 | 0.0042 | 0.0125 | 0.9737 | 0.9862 | 0.9799 | 0.8142 | 0.8246 | **0.8194** | 0.9936 | 75.3s |
| 06 | 0.0016 | 0.0100 | 0.9727 | 0.9842 | 0.9785 | 0.8130 | 0.8227 | **0.8178** | 0.9941 | 73.9s |
| 07 | 0.0012 | 0.0121 | 0.9756 | 0.9852 | 0.9804 | 0.8156 | 0.8236 | **0.8196** | 0.9951 | 78.2s |
| 08 | 0.0005 | 0.0088 | 0.9785 | 0.9882 | 0.9833 | 0.8185 | 0.8266 | **0.8225** | 0.9951 | 76.5s |
| 09 | 0.0003 | 0.0090 | 0.9785 | 0.9882 | 0.9833 | 0.8185 | 0.8266 | **0.8225** | 0.9951 | 79.2s |
| 10 | 0.0002 | 0.0087 | 0.9805 | 0.9892 | 0.9848 | 0.8203 | 0.8276 | **0.8239** | 0.9956 | 79.0s |
| 11 | 0.0002 | 0.0089 | 0.9834 | 0.9901 | 0.9867 | 0.8229 | 0.8286 | **0.8257** | 0.9966 | 91.3s |
| 12 | 0.0001 | 0.0092 | 0.9834 | 0.9901 | 0.9867 | 0.8229 | 0.8286 | **0.8257** | 0.9966 | 141.6s |
| 13 **(Best)** | 0.0001 | 0.0087 | 0.9853 | 0.9921 | 0.9887 | 0.8249 | 0.8305 | **0.8277** | 0.9966 | 183.0s |
| 14 | 0.0001 | 0.0089 | 0.9834 | 0.9901 | 0.9867 | 0.8229 | 0.8286 | **0.8257** | 0.9966 | 88.3s |
| 15 | 0.0001 | 0.0088 | 0.9843 | 0.9911 | 0.9877 | 0.8239 | 0.8296 | **0.8267** | 0.9966 | 84.8s |
| 16 | 0.0001 | 0.0088 | 0.9853 | 0.9921 | 0.9887 | 0.8249 | 0.8305 | **0.8277** | 0.9966 | 90.6s |
| 17 | 0.0001 | 0.0089 | 0.9853 | 0.9921 | 0.9887 | 0.8249 | 0.8305 | **0.8277** | 0.9966 | 84.1s |
| 18 | 0.0001 | 0.0089 | 0.9853 | 0.9921 | 0.9887 | 0.8249 | 0.8305 | **0.8277** | 0.9966 | 87.5s |

---

### 3. Training Milestone Summary
- **Best Validation Epoch:** Epoch `13`
- **Peak Validation Exact Span F1:** `0.8277`
- **Peak Validation Partial Overlap F1:** `0.9966`
- **Peak Validation Token F1 (seqeval):** `0.9887`
- **Total Training Duration:** `1810.3 seconds` (30.17 minutes)
- **Early Stopping Trigger:** Completed minimum required epochs with early stopping patience tracking on validation Exact Span F1.
- **Checkpoint Serialization:** Best weights saved to `datasets/informal_skill_extraction/models/checkpoints/indian_mock/exp_indian_xlm_roberta/best_checkpoint/` with offline Hugging Face safetensors format.
