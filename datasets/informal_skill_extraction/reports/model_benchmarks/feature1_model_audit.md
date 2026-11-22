# ELEVATE X AI — FEATURE 1: CODE & DATA AUDIT REPORT
**Feature**: Informal Experience → Skill Extraction  
**Date**: November 15, 2026  
**Auditor**: Elevate X AI Core Engineering Team  
**Scope**: Model Architecture, Preprocessing, Token Alignment, Training Pipeline, and Evaluation Benchmarks

---

## 1. Executive Summary

An exhaustive code and data audit was conducted on the Feature 1 skill extraction pipeline. The previous benchmark evaluation produced unacceptable scores on the official SkillSpan English test set:
- **Token Precision**: `0.0233`
- **Token Recall**: `0.0217`
- **Token F1-Score**: `0.0225`
- **Exact Span F1**: `0.0213`

The audit revealed that these poor scores were not indicative of inherent model capacity limits, but rather the result of **six structural defects** in token alignment, subword mapping, regex greediness, training dataset coverage, and evaluation metric comparison.

This document details the root causes identified, empirical evidence gathered, and the remediation plan required before executing the next training cycle.

---

## 2. Root Cause Analysis

### Root Cause 1: Severe Token Alignment Divergence in Evaluation
- **Defect**: In `evaluate_skill_extractor.py`, gold labels in SkillSpan are pre-tokenized at the word level (`tokens: ["Senior", "QA", "Engineer", "(", "m/f/d", ")", "<ORGANIZATION>"]`). However, during evaluation, the script called `BIOTokenizer.word_tokenize_with_offsets(text)` which tokenized via the regex `r"[\w]+|[^\w\s]"`.
- **Empirical Evidence**:
  - SkillSpan token list length: 5 tokens (`['<ORGANIZATION>', '<ORGANIZATION>', '<ORGANIZATION>', '<ORGANIZATION>', '.']`).
  - Regex token list length: 13 tokens (`['<', 'ORGANIZATION', '>', '<', 'ORGANIZATION', '>', ...']`).
  - When aligning predicted character spans back to BIO tags via `align_character_spans_to_bio`, tags were generated for the 13-token sequence.
  - The evaluation script then truncated or padded the sequence to match the 5-token gold sequence.
  - As a result, `seqeval` was comparing predicted BIO tags against completely misaligned token indices, guaranteeing an artificially suppressed near-zero F1 score.
- **Remediation**: Use the native `is_split_into_words=True` alignment from Hugging Face `FastTokenizer` with `word_ids()`, and compute character offsets directly from the token list via cumulative whitespace indexing: `tokens_and_offsets(tokens)`.

---

### Root Cause 2: Subword Token Alignment Flaws in `SkillSpanTorchDataset`
- **Defect**: In `train_skill_extractor.py`, `SkillSpanTorchDataset.__getitem__` iterated over words and called `self.tokenizer.tokenize(word)` for each word in isolation.
- **Empirical Evidence**:
  - XLM-RoBERTa uses SentencePiece BPE. In SentencePiece, a word preceded by a space has a different token representation than an isolated word (e.g. `tokenizer.tokenize(" QA")` produces `[' QA']` with ID `49952`, whereas isolated word tokenization misses whitespace boundary tokens).
  - Special tokens (`<s>`, `</s>`) were manually spliced with hardcoded fallback IDs instead of using the tokenizer's native encoding.
  - Subwords after the first token of a word were given `TAG2ID["I-SKILL"]` or duplicate labels rather than the standard PyTorch masking value of `-100`, corrupting the cross-entropy loss gradient during backpropagation.
- **Remediation**: Re-implement `SkillSpanTorchDataset` using `tokenizer(tokens, is_split_into_words=True, truncation=True, max_length=128)` and assign `-100` to all special tokens and subsequent subword pieces using `word_ids()`.

---

### Root Cause 3: Under-Training & Extreme Class Imbalance
- **Defect**:
  - The training run executed only **600 samples** out of 4,800 train samples for 2 epochs (only 76 total gradient steps).
  - The transformer backbone was completely frozen, meaning only the 2,307 parameters of the linear classification head were trained.
  - In SkillSpan, the token tag distribution is heavily imbalanced:
    - `"O"`: 83,382 tokens (89.6%)
    - `"I-SKILL"`: 7,850 tokens (8.4%)
    - `"B-SKILL"`: 2,221 tokens (2.4%)
  - Without sufficient training steps or balanced representation fine-tuning, the classifier struggled to establish optimal decision boundaries for the minority `B-SKILL` class.
- **Remediation**: Train across multiple architectures and configurations:
  1. Experiment A: Frozen backbone with calibrated learning rate and full training set.
  2. Experiment B: Partially unfrozen backbone (top 2 encoder layers).
  3. Experiment C: Full fine-tuning on CPU / MPS with gradient accumulation.
  4. Experiment D: Rule / TF-IDF hybrid baseline.

---

### Root Cause 4: Greedy Heuristic Regex Capturing Conversational Noise
- **Defect**: The heuristic extractor in `skill_extractor.py` used the regex pattern:
  ```python
  rf"\b({re.escape(kw)}(?:\s+[\w]+){{0,4}})\b"
  ```
- **Empirical Evidence**:
  - For the input: *"Main kapde ki cutting karta hu aur customer ke measurement ke according suit silta hu."*
  - Keyword `"cutting"` matched `"cutting karta hu aur customer"` (capturing 4 succeeding words: auxiliary verbs, conjunction, and unrelated noun).
  - Keyword `"measurement"` matched `"measurement ke according suit silta"` (capturing postposition and trailing words).
  - This resulted in ungrammatical, noisy skill spans being returned by the API and evaluated.
- **Remediation**: Remove greedy multi-word wildcard matching. Constrain heuristic and rule-based extraction to strict noun/verb compound phrases, and apply stop-word/auxiliary-verb stripping on Hindi, Roman Hindi, Hinglish, and English tokens.

---

### Root Cause 5: Evaluation Metric Granularity (Exact vs. Partial Span Match)
- **Defect**: The benchmark script only computed Exact Span F1, which requires 100% character boundary coincidence.
- **Empirical Evidence**:
  - In job postings and informal text, annotators often disagree on boundary determiners (e.g. `Python programming` vs `Python`, `cutting fabric` vs `fabric cutting`).
  - Standard NER literature (e.g., SemEval, CoNLL, SkillSpan benchmarks) reports both **Exact Span F1** and **Partial / Token Overlap F1** to distinguish complete misses from boundary variations.
- **Remediation**: Include Token F1, Exact Span F1, Partial Overlap F1, and per-class precision/recall in the evaluation pipeline.

---

### Root Cause 6: Checkpoint Loading & Device Constraints on Apple M2
- **Defect**:
  - Full fine-tuning on Apple M2 MPS triggered `torch.OutOfMemoryError` due to metal command buffer limits on backpropagation with AdamW optimizer states.
  - PyTorch MPS SDPA (Scaled Dot-Product Attention) does not support active dropout during `model.train()` backward passes (`NotImplementedError`).
- **Remediation**:
  - For training: Use controlled CPU engine for backward pass if MPS SDPA with dropout is invoked, or set `model.eval()` when training linear heads on MPS.
  - For inference: Leverage Apple M2 MPS natively (`torch.no_grad()`), which delivers sub-30ms latency.

---

## 3. Mandatory Safety Gate Verification

- **Genuine Indian Worker Records**: `0`
- **Synthetic Development Records**: `522` (strictly quarantined in `raw/indian_worker_data/synthetic_stubs/`)
- **Safety Gate**: **LOCKED** (Threshold: $\ge 500$ verified field records).
- **Compliance Confirmation**: No model will be fine-tuned or evaluated on synthetic worker data as if it were real training data. All benchmark experiments will be conducted strictly on the permitted official SkillSpan partitions (`train.json`, `dev.json`, `test.json`).

