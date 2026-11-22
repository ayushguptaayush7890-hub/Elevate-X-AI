# ELEVATE X AI — FEATURE 1: MODEL CARD
## Multilingual Vocational Skill Extractor (XLM-RoBERTa Token Classifier)

---

## 1. Model Details

- **Model Name**: Elevate X Multilingual Skill Extractor
- **Version**: `1.0.0-skillspan-expB`
- **Release Date**: November 2026
- **Architecture**: XLM-RoBERTa Base (`xlm-roberta-base`) backbone (12 layers, 768 hidden dimensions, 12 attention heads, 250k SentencePiece BPE vocabulary) with partially unfrozen top-2 encoder layers (layers 10-11) coupled to a linear token classification head ($\mathbb{R}^{768 \rightarrow 3}$).
- **Labels**: BIO Sequence Tagging (`O`, `B-SKILL`, `I-SKILL`).
- **Frameworks**: PyTorch 2.15.0, Hugging Face Transformers 4.49.0, seqeval 1.2.2.
- **Hardware Profile**: Apple Silicon M2 (Unified Memory 16 GB, PyTorch MPS Acceleration).
- **License**: Apache 2.0 (compatible with base XLM-RoBERTa and downstream open standards).

---

## 2. Intended Use

### Primary Intended Uses
- Extraction of practical vocational competencies, manual actions, tools, and materials from worker descriptions.
- Semantic boundary detection across job requirement sentences and candidate vocational narratives.
- Serving as the foundational token classification layer in the Elevate X AI platform before category assignment and NSQF / ESCO / O*NET crosswalking.

### Out-of-Scope & Misuse Cases
- **Autonomous Credentialing**: Never use extracted raw spans directly as accredited credentials without verification.
- **High-Stakes Legal / Employment Screening**: Model predictions must be accompanied by human-in-the-loop review (`human_review_required: true` for unmapped or borderline spans).
- **Unconsented Worker Surveillance**: Must adhere strictly to verified worker consent protocols.

---

## 3. Data & Safety Governance

### Training Safety Gate Status
- **Genuine Indian Informal Worker Records**: `0`
- **Minimum Fine-Tuning Threshold**: `500` verified, consented records.
- **Gate Status**: **STRICTLY LOCKED**.
- **Rule Enforcement**: Fine-tuning on synthetic data or unverified worker descriptions is prohibited by automated programmatic gates in `train_experiments.py` and `model_service.py`.

### Benchmark Data
- **Dataset**: Official English SkillSpan benchmark (`test.json` partition, 3,569 sentences).
- **Labeling Standard**: Sentence-level BIO token annotations covering technical and soft workplace competencies.
- **Notice**: English benchmark scores reflect standard job-posting syntax and do not measure conversational Hindi, Hinglish, or Roman Hindi field performance.

---

## 4. Evaluation & Performance Summary

Evaluated on the complete, untouched official SkillSpan test partition:

| Metric Dimension | Benchmark Value | Description |
| :--- | :--- | :--- |
| **Test Sentences Evaluated** | 3,569 | Full official test set |
| **Token-Level Precision** | 0.3016 | Subword token precision |
| **Token-Level Recall** | 0.4524 | Subword token recall |
| **Token-Level F1-Score** | 0.3619 | 12.8x gain over 0.0225 baseline |
| **Exact Span F1-Score** | 0.3619 | Strict character boundary `[start:end]` match |
| **Partial Overlap F1-Score** | 0.6476 | Operational NER match ($\max(p_s, g_s) < \min(p_e, g_e)$) |
| **Partial Overlap Recall** | 0.8095 | Model captures >80% of true skill concepts |
| **Mean Inference Latency** | 27.3 ms | Per-sentence forward pass on Apple M2 MPS |
| **P95 Latency** | 139.9 ms | 95th percentile SLA latency |
| **Throughput** | 36.5 sent/s | Sequential real-time streaming throughput |

---

## 5. Architectural Safeguards

1. **Exact Slicing Invariant**:
   All extracted spans mathematically satisfy `text[start_offset:end_offset] == extracted_skill`. No off-by-one errors or text hallucinations.
2. **Conversational Auxiliary Pruning**:
   Heuristic and post-processing filters strip conversational padding (`karta hu`, `silta hu`, `ke according`, `aur customer`) ensuring clean conceptual skill entities.
3. **Similarity Gate on Ontology Mapping**:
   If cosine similarity against the 32 canonical competencies in `CanonicalSkillRetriever` is $< 0.65$:
   - `canonical_skill` is set to `null`
   - `canonical_skill_id` is set to `null`
   - `mapping_status` is set to `"unmapped"`
   - `is_unmapped_skill` is set to `true`
   - `human_review_required` is set to `true`
   This prevents hallucinated ontology mappings for novel trade vernacular.

---

## 6. Environmental & Hardware Footprint

- **Compute Platform**: Local Apple Silicon M2 SoC.
- **VRAM / Unified Memory Utilization**: 2.4 GB during inference.
- **Carbon Footprint**: Zero remote cloud GPU reliance for local testing; highly efficient Apple Silicon MPS execution.

