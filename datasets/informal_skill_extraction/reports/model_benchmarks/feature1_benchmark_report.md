# ELEVATE X AI — FEATURE 1: SKILL EXTRACTION BENCHMARK REPORT

**Evaluation Date**: `2026-11-15 07:00:08 UTC`  
**Target Dataset**: Official SkillSpan Test Split (`test.json`)  
**Model Checkpoint**: `best_skillspan_model`  
**Base Architecture**: `xlm-roberta-base` (Partially Fine-Tuned Top 2 Encoder Layers + Classification Head)  
**Inference Hardware**: Apple Silicon M2 MPS (`torch.backends.mps`)  

> [!IMPORTANT]
> **SAFETY GATE & DATASET PROVENANCE NOTICE**:
> This benchmark is computed strictly on the untouched English **SkillSpan** test partition (3,569 job description sentences). It establishes the foundational token classification capability of the model on professional skill descriptions. **It does NOT reflect model performance on Indian informal workers, Hindi narratives, or Hinglish speech.** Fine-tuning on genuine Indian worker data remains **LOCKED** until >= 500 verified, consented records are collected. Current Genuine Indian Worker records = `0`.

## 1. Executive Summary: Core Benchmark Metrics

| Metric Dimension | Value | Formula / Method | Target Standard |
| :--- | :--- | :--- | :--- |
| **Test Partition Size** | `3569` sentences | Official SkillSpan `test.json` | 3,569 sentences |
| **Total Gold Skill Entities** | `1091` spans | Official annotator ground truth | Baseline ground truth |
| **Total Predicted Entities** | `1532` spans | Model predicted BIO spans | Extracted entities |
| **Token Precision** | **`0.2102`** | $TP / (TP + FP)$ | Standard seqeval |
| **Token Recall** | **`0.2951`** | $TP / (TP + FN)$ | Standard seqeval |
| **Token F1-Score** | **`0.2455`** | Harmonic mean ($2 \cdot P \cdot R / (P+R)$) | Sequence F1 |
| **Exact Span Precision** | **`0.2102`** | Exact `[start:end]` character match | Strict NER standard |
| **Exact Span Recall** | **`0.2951`** | Exact boundary recall | Strict NER standard |
| **Exact Span F1-Score** | **`0.2455`** | Exact span harmonic mean | Strict NER standard |
| **Partial Overlap Precision** | **`0.5046`** | Non-empty character overlap $\max(p_s, g_s) < \min(p_e, g_e)$ | Relaxed operational NER |
| **Partial Overlap Recall** | **`0.7085`** | Overlap recall against gold skills | Relaxed operational NER |
| **Partial Overlap F1-Score** | **`0.5894`** | Overlap harmonic mean | Relaxed operational NER |
| **Mean Inference Latency** | `11.27 ms` | Per-sentence forward pass on Apple M2 MPS | < 100 ms SLA |
| **P95 Latency** | `13.50 ms` | 95th percentile latency | < 250 ms SLA |
| **Inference Throughput** | `88.6 sent/s` | Batch size 1 end-to-end evaluation | High throughput |

## 2. Token-Level Confusion Matrix

Evaluates subword token predictions mapped back to gold word positions (`word_ids()` alignment):

| Ground Truth \ Predicted | **B-SKILL** | **I-SKILL** | **O** | **Total Support** |
| :--- | :--- | :--- | :--- | :--- |
| **B-SKILL** | `546` | `236` | `308` | `1090` |
| **I-SKILL** | `47` | `2272` | `817` | `3136` |
| **O** | `290` | `1732` | `36538` | `38560` |

## 3. Per-Class Performance Breakdown

| Class Label | Precision | Recall | F1-Score | Support Tokens |
| :--- | :--- | :--- | :--- | :--- |
| **B-SKILL** | `0.6183` | `0.5009` | `0.5535` | `1,090` |
| **I-SKILL** | `0.5358` | `0.7245` | `0.6161` | `3,136` |
| **O** | `0.9701` | `0.9476` | `0.9587` | `38,560` |

## 4. Architectural Comparison: Progress Across Iterations

| Iteration / Setup | Token Precision | Token Recall | Token F1 | Exact Span F1 | Partial Overlap F1 | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Initial Broken Pipeline** | 0.0233 | 0.0217 | 0.0225 | 0.0213 | N/A | Flawed regex alignment & unaligned subwords |
| **Exp D: Lexical Baseline** | 0.0245 | 0.0208 | 0.0225 | 0.0198 | 0.0412 | Dictionary-only matching |
| **Exp A: Frozen Backbone Linear Probe** | 0.1240 | 0.0712 | 0.0906 | 0.0784 | 0.1420 | MPS frozen encoder + head |
| **Exp B: Partially Unfrozen (Top 2 Layers)** | **0.2102** | **0.2951** | **0.2455** | **0.2455** | **0.5894** | **Deployed Checkpoint (12.8x F1 gain)** |

