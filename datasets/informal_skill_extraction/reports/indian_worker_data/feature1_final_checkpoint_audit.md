# ELEVATE X AI — FEATURE 1: FINAL CHECKPOINT & ARTIFACT AUDIT REPORT

## 1. Checkpoint Verification Summary

- **Total Training Epochs:** `18` (18 epochs completed)
- **Best Epoch:** `Epoch 13`
- **Best Validation Exact Span F1:** `0.8277`
- **Best Checkpoint SHA256:** `7c47b0a7db6d50d7430eb74b261c31f576e17099200b2bf7bf8434e2d30bb665`
- **Deployed Production Checkpoint SHA256:** `7c47b0a7db6d50d7430eb74b261c31f576e17099200b2bf7bf8434e2d30bb665`
- **Bit-for-Bit Identity:** `100% IDENTICAL`

## 2. Architecture & Parameter Count Audit

- **Backbone:** `xlm-roberta-base`
- **Total Parameter Count:** `277,455,363`
- **Trainable Parameter Count:** `14,178,051` (5.11%)
- **Exact Match with 14,178,051:** `True`
- **Unfrozen Layers:** `roberta.encoder.layer.10.*` (7,087,872), `roberta.encoder.layer.11.*` (7,087,872), `classifier.*` (2,307). Lower layers 0-9 and embeddings strictly frozen.

## 3. Latest vs Best Checkpoint Analysis

- **Finding:** In `train_indian_model.py`, after early stopping at Epoch 18, `model.load_state_dict(best_state_dict)` was called to reload Epoch 13 weights into memory before writing both `best_checkpoint` and `latest_checkpoint`. Consequently, both directories contain the optimal Epoch 13 weights (`7c47b0a7...`). The deployed production model in `best_indian_model` is genuinely and strictly the Epoch 13 best model.
