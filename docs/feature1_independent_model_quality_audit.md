# Feature 1 — Independent Model Quality Audit

**Project:** Elevate X AI — Vocational & Technical Skill Extraction Engine  
**Feature:** Feature 1 (AI Skill Extraction)  
**Audit Type:** Strict Evaluation-Only (No Code or Weight Changes)  
**Audit Date:** November 21, 2026  
**Execution Environment:** macOS (Darwin 24.5.0), Apple Silicon MPS (`mps:0`), Python 3.13  

---

## 1. Verification of Model-Only Inference

An independent audit was conducted on the running API and inference pipeline to verify that skill extraction is 100% driven by the neural token classification model without manual intervention.

### 1.1 Loaded Checkpoint & File Integrity
The inference pipeline lazily loads the verified fine-tuned model checkpoint from:
`datasets/informal_skill_extraction/models/checkpoints/best_indian_model`

The cryptographic SHA-256 hashes, file sizes, and architectures were verified:

| File Name | File Size | SHA-256 Hash | Role |
|---|---|---|---|
| `model.safetensors` | 1,109,845,500 bytes (1.11 GB) | `7c47b0a7db6d50d7430eb74b261c31f576e17099200b2bf7bf8434e2d30bb665` | Fine-tuned XLM-RoBERTa Token Classification weights |
| `config.json` | 901 bytes | `945f136273e37221da4125b78b3ee142ab228a8787f739a66cc31e0950c5630c` | Model configuration, label map, hidden dimensions |
| `tokenizer.json` | 17,098,351 bytes (17.1 MB) | `a04dec98c0804beeedde93263778442d924081d88090d4ac3db097205fa959bd` | SentencePiece vocabulary & subword merges |
| `tokenizer_config.json` | 343 bytes | `5d84c938d902dbd684af806ccc920e4c99812d897b0f271eebf856361a4337f6` | Tokenizer special tokens and normalization rules |

### 1.2 Model & Tokenizer Configuration
- **Model Class:** `XLMRobertaForTokenClassification`
- **Tokenizer Class:** `XLMRobertaTokenizer`
- **Number of Labels:** `3`
- **Label Mapping:**
  - `0`: `O` (Outside of any skill)
  - `1`: `B-SKILL` (Beginning of a skill entity)
  - `2`: `I-SKILL` (Inside / continuation of a skill entity)
- **Token Alignment:** Subword-to-word alignment using `encoding.word_ids(batch_index=0)` preserving word boundary indexing.

### 1.3 Strict Absence of Heuristics and Fallbacks
The inference flow was inspected to confirm that:
1. **No Keyword Injections:** Calls to `technical_skill_lexicon.py` and `extract_skills_heuristic()` are completely absent from the inference execution graph in `skill_extractor.py`.
2. **No Regex Compound Matchers:** `find_compound_matches()` has been removed from `semantic_normalizer.py`.
3. **No UI Mock Data:** The frontend `experience/page.tsx` contains no demo buttons, demo data state, or hardcoded sample cards.
4. **Failure Behavior:** If the neural model fails or checkpoint files are missing, the pipeline raises a `RuntimeError` and returns an explicit `HTTP 503 Service Unavailable`, rather than silently falling back to a mock or dictionary response.

### 1.4 Actual Hardware Execution Device
Device verification was performed on live tensor parameters during inference:
- **Configured Device:** `mps`
- **Parameter Tensor Device:** `mps:0` (Apple Silicon Metal Performance Shaders)
- **Logits Tensor Device:** `mps:0`
- **Parameter Dtype:** `torch.float32`

---

## 2. Evaluation on Existing Untouched Test Data

Evaluation was conducted exclusively on the held-out test partition:
`datasets/informal_skill_extraction/processed/indian_mock_data/indian_mock_test.jsonl` (550 records, untouched since generation). No synthetic training or validation records were mixed into the test set.

### 2.1 Overall Performance Metrics

| Evaluation Metric | Score | Sample Count / Breakdown |
|---|---|---|
| **Exact Span Precision** | **0.7817** | 1,010 True Positives / 1,292 Predicted Spans |
| **Exact Span Recall** | **0.8714** | 1,010 True Positives / 1,159 Gold Spans |
| **Exact Span F1-Score** | **0.8242** | Harmonic mean of exact boundary matches |
| **Partial Span F1-Score** | **0.9457** | Overlap matches at token level |
| **Entity Chunk Precision (Seqeval equiv.)** | **0.5927** | Strict token chunk boundary precision |
| **Entity Chunk Recall (Seqeval equiv.)** | **0.7420** | Strict token chunk boundary recall |
| **Entity Chunk F1-Score** | **0.6590** | Strict chunk-level F1 |
| **Character Slicing Invariant Errors** | **0 Errors** | `text[start:end] == span_text` holds for 100% of spans |

### 2.2 Per-Class BIO Token Metrics

Classification report computed over all 12,684 evaluation tokens:

| BIO Class | Precision | Recall | F1-Score | Support (Tokens) |
|---|---|---|---|---|
| **`O`** | 0.9587 | 0.9713 | 0.9650 | 6,695 |
| **`B-SKILL`** | 0.8885 | 0.9905 | 0.9368 | 1,159 |
| **`I-SKILL`** | 0.9579 | 0.9141 | 0.9355 | 4,830 |
| **Macro Average** | **0.9350** | **0.9587** | **0.9458** | 12,684 |
| **Weighted Average** | **0.9520** | **0.9489** | **0.9512** | 12,684 |

### 2.3 Token Confusion Matrix
Rows represent Gold ground-truth labels; columns represent Model predictions:

$$\begin{pmatrix} & \text{Pred O} & \text{Pred B-SKILL} & \text{Pred I-SKILL} \\ \text{Gold O} & 6,503 & 8 & 184 \\ \text{Gold B-SKILL} & 1 & 1,148 & 10 \\ \text{Gold I-SKILL} & 279 & 136 & 4,415 \end{pmatrix}$$

**Observations:**
- Out of 1,159 gold `B-SKILL` tokens, the model correctly identified 1,148 as `B-SKILL` (99.05% recall). Only 1 was missed as `O`.
- Gold `I-SKILL` tokens had 279 instances classified as `O`, mostly corresponding to auxiliary conjunctions and prepositions omitted by boundary tightening.

---

### 2.4 Per-Domain (Trade) Performance Breakdown

Performance across all 10 target vocational trades:

| Trade Code | Trade Name | Gold Spans | Pred Spans | Exact F1 | Chunk F1 |
|---|---|---|---|---|---|
| **TRD-01** | Tailor & Garment Worker | 115 | 132 | **0.7611** | 0.6434 |
| **TRD-02** | Electrician | 114 | 133 | **0.7287** | 0.6226 |
| **TRD-03** | Plumber | 114 | 119 | **0.9099** | 0.7339 |
| **TRD-04** | Motor Mechanic | 123 | 137 | **0.8154** | 0.6099 |
| **TRD-05** | Carpenter | 120 | 122 | **0.9587** | 0.7968 |
| **TRD-06** | Welder | 111 | 128 | **0.7950** | 0.6087 |
| **TRD-07** | Mason / Raj Mistri | 118 | 121 | **0.9289** | 0.7452 |
| **TRD-08** | Painter | 115 | 128 | **0.8560** | 0.6183 |
| **TRD-09** | Agriculture & Irrigation | 118 | 146 | **0.7045** | 0.5775 |
| **TRD-10** | Mobile Repair Technician | 111 | 126 | **0.8017** | 0.6508 |

**Analysis:**
- **Top Performing Trades:** Carpenter (`0.9587` Exact F1), Mason (`0.9289`), and Plumber (`0.9099`). These trades feature distinct, unambiguous physical tool and material terms (e.g., *chaurasi, plumb bob, solvent cement*).
- **Lower Scoring Trades:** Agriculture (`0.7045`) and Electrician (`0.7287`). Lower scores stem from compound coordination (e.g., *drip lateral line installation and venturi filter cleaning* being split into two sub-spans).

---

### 2.5 Per-Language & Script Performance Breakdown

| Linguistic Mode | Script | Gold Spans | Pred Spans | Exact F1 | Chunk F1 |
|---|---|---|---|---|---|
| **Mixed Script** | Mixed (Devanagari + Latin) | 240 | 242 | **0.9876** | 0.8920 |
| **Hindi** | Devanagari | 231 | 237 | **0.9744** | 0.6618 |
| **Roman Hindi** | Latin | 227 | 241 | **0.9145** | 0.7555 |
| **Hinglish** | Latin (Code-switched) | 232 | 282 | **0.7043** | 0.6731 |
| **English** | Latin | 229 | 290 | **0.5742** | 0.3389 |

**Analysis:**
- The multilingual XLM-RoBERTa model shows superior accuracy on **Devanagari and Mixed-Script** inputs (`> 0.97` Exact F1).
- Performance drops on pure conversational English (`0.5742`), where the model exhibits higher sensitivity and splits multi-word phrases.

---

### 2.6 Cross-Domain Evaluation on English SkillSpan Dataset (Job Postings)
Evaluated on 500 held-out sentences from the SkillSpan job posting dataset (`datasets/informal_skill_extraction/raw/skillspan/test.json`):

| Annotation Schema | Precision | Recall | F1-Score |
|---|---|---|---|
| **SkillSpan (`tags_skill` only)** | 0.0030 | 0.0290 | **0.0055** |
| **SkillSpan Combined (`skills` + `knowledge`)** | 0.0348 | 0.0868 | **0.0497** |

**Cross-Domain Finding:**
The Indian vocational fine-tuned checkpoint exhibits a significant domain transfer gap when applied zero-shot to formal corporate English job postings. In job postings, technical skills (e.g., *Java, React, SQL*) are expressed as nouns in bulleted requirements rather than first-person experiential sentences (*"Main 5 saal se bike repair karta hu"*).

---

## 3. In-Depth Error Analysis

An inspection of model prediction errors across the test set revealed specific failure modes:

### 3.1 Compound Skill Splitting (Granularity Mismatch)
The single largest source of strict exact-match false positives/negatives is compound entity conjoining. In the ground-truth annotations, coordinate clauses are frequently grouped as single compound spans, whereas the neural model predicts individual atomic skills:

- **Example 1 (Record `MOCK-TRD-01-00163`):**
  - *Input:* `"Hamari workshop me daily bakram chipkana aur collar banana... hota hai."`
  - *Gold Annotation:* `['bakram chipkana aur collar banana']` (1 span)
  - *Model Prediction:* `['bakram chipkana', 'collar banana']` (2 distinct spans)
  - *Metric Impact:* Counted as 1 False Negative and 2 False Positives for Exact Match, even though the semantic extraction is more precise.
- **Example 2 (Record `MOCK-TRD-01-00279`):**
  - *Input:* `"Site par daily routine me fabric cutting and pattern marking execute karta hu."`
  - *Gold Annotation:* `['fabric cutting and pattern marking']`
  - *Model Prediction:* `['fabric cutting', 'pattern marking']`

### 3.2 Boundary Extension & Trailing Verbs
In some instances, the model includes procedural verbs or trailing inspections within the skill entity:
- **Example 3 (Record `MOCK-TRD-01-00284`):**
  - *Input:* `"...handover se pehle overlock seam edging inspect karte hain."`
  - *Gold:* `['overlock seam edging']`
  - *Pred:* `['overlock seam edging inspect']` (trailing verb `inspect` tagged as `I-SKILL`).
- **Example 4 (Record `MOCK-TRD-01-00029`):**
  - *Input:* `"...kapde ki cutting ki jaanch karte hain."`
  - *Gold:* `['कपड़े की कटिंग']`
  - *Pred:* `['कपड़े की कटिंग', 'जांच']` (standalone verb `जांच` tagged as isolated `B-SKILL`).

### 3.3 Leading Preposition Truncation
In colloquial Hindi/Hinglish phrasing, leading prepositions occasionally confuse token boundary transitions:
- **Example 5 (Record `MOCK-TRD-01-00036`):**
  - *Input:* `"Yadi koi dikkat aaye to grahak se design baat-chit karte hain."`
  - *Gold:* `['ग्राहक से डिजाइन बातचीत']`
  - *Pred:* `['से डिजाइन बातचीत']` (missed `ग्राहक`, started chunk on preposition `से`).

### 3.4 Symbol & Technical Entity Probing
Probing tests were performed across modern technical entities containing punctuation symbols:

| Probe ID | Input Phrase | Extracted Skills | Behavior & Analysis |
|---|---|---|---|
| **SYM-01** | `"I develop backends using C++ and C#."` | `['backends using', 'C++', 'C#']` | `C++` and `C#` cleanly extracted without dropping `+` or `#`. Partial false positive on `backends using`. |
| **SYM-02** | `"Expert in Node.js and React.js development."` | `['Node.js', 'React.js development']` | Extracted dot-notated technologies accurately. |
| **SYM-03** | `"Building microservices with Python 3, FastAPI, and Docker."` | `['Building microservices with Python 3', 'FastAPI', 'Docker.']` | Multi-word phrase grouping and trailing period attached to `Docker.`. |
| **SYM-04** | `"Proficient in .NET core, ASP.NET, and SQL Server."` | `['.NET core', 'ASP.NET', 'SQL Server.']` | Dot-prefixed `.NET` successfully captured. |
| **OUT-01** | `"The quick brown fox jumps over the lazy dog."` | `['quick brown fox jumps over', 'dog.']` | Out-of-domain false positive due to absence of negative training samples in synthetic mock data. |
| **OUT-02** | `"Tomorrow is a holiday and the weather is sunny today."` | `[]` (Empty) | Correctly returned 0 skills on standard conversational non-skill text. |

---

## 4. Occupation Classification Audit

A separate audit was conducted on `OccupationClassifier` (`datasets/informal_skill_extraction/models/occupation_classifier.py`).

### 4.1 Architecture & Limitations
Unlike the skill extraction module, **occupation classification is NOT a deep neural model**:
- **Algorithm:** Scikit-learn `TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5))` combined with `LogisticRegression(max_iter=500, C=5.0)`.
- **Training Data:** Synthesized keyword vocabulary dictionary (`TRADE_VOCABULARY`) with templated synthetic carrier phrases (*"main {term} ka kaam karta hu"*).
- **Abstention Logic:** If classification probability is $< 0.35$ and no predefined trade keywords match in the text, it abstains with:
  `{"occupation_id": "UNCLASSIFIED", "occupation_title": "General / Technical Professional", "confidence": 0.0}`

### 4.2 Audit Finding on `UNCLASSIFIED`
- When technical descriptions such as `"I know c++ java"` or non-vocational sentences are processed, returning `UNCLASSIFIED` with `0.0` confidence is **correct and intended behavior**.
- It is a significant improvement over the previous bug where non-vocational descriptions were erroneously tagged as `"Carpenter (TRD-05) 20% Conf"`.
- However, the fact that occupation classification relies on a lightweight linear model and keyword heuristics is an architectural limitation and must not be conflated with the neural token classifier.

---

## 5. Performance & Hardware Resource Audit

Resource utilization and inference latencies were benchmarked directly on the test host:

### 5.1 Cold Model Loading Time
- **Initialization to Ready:** **11.4744 seconds**
- **Breakdown:** Checkpoint weight deserialization from disk (1.11 GB safetensors), configuration loading, transfer of 199 parameter tensors to Apple Silicon MPS memory.

### 5.2 Process & Hardware Memory
- **Initial Python Process RSS Memory:** `21.12 MB`
- **Loaded Process RSS Memory:** `46.05 MB`
- **Net Process Host Memory Increase:** `24.92 MB`
- **PyTorch MPS Unified GPU Memory Allocated:** **1,058.42 MB (~1.03 GB)**

### 5.3 Warm Inference Latency Benchmarks
Benchmarked over 50 consecutive invocations across Hindi, Hinglish, and English inputs:

| Metric | Measured Latency |
|---|---|
| **Minimum Latency** | **13.64 ms** |
| **Median Latency** | **20.30 ms** |
| **Mean Latency** | **21.54 ms** |
| **95th Percentile (P95)** | **25.48 ms** |
| **Maximum Latency** | **84.11 ms** |

---

## 6. Training Safety Gate & Governance Status

- **Safety Policy:** Fine-tuning or retraining weights is strictly gated by verified field data volume.
  $$\text{Gate Condition: Real Indian Worker Records} \ge 500$$
- **Current Real Records Count:** `0` (Located at `datasets/informal_skill_extraction/raw/indian_worker_data/real/pilot_tailor_batch1.jsonl`).
- **Safety Gate Status:** **LOCKED**.
- **Compliance Confirmation:**
  - Zero synthetic worker records were fabricated.
  - Zero code modifications were introduced during this audit.
  - All metrics recorded in this report represent authentic, observed executions on existing held-out test partitions.

---

## 7. Audit Conclusions & Technical Recommendations

1. **Model-Only Verification Confirmed:** Feature 1 skill extraction is 100% neural, executing token classification on Apple Silicon MPS with zero keyword or regex fallbacks.
2. **High Multilingual Precision:** The fine-tuned XLM-RoBERTa model achieves strong accuracy on vocational Hindi/Hinglish domains (`0.8242` Exact F1, `0.9457` Partial F1), with zero character-slicing invariant errors.
3. **Identified Bottlenecks:**
   - Coordinate clauses (*"X aur Y"*) are split into atomic skills by the model, causing superficial exact-match penalties against compound gold annotations.
   - Punctuation attachment on tokens (e.g., `Docker.`) should be addressed via post-inference trailing punctuation stripping.
   - Occupation classification should eventually be upgraded from TF-IDF/Logistic Regression to a joint multi-task neural sequence classification head on the transformer.
