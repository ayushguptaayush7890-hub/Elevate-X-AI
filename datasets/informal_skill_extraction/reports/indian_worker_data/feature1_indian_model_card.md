# ELEVATE X AI — FEATURE 1: MODEL CARD
## Multilingual Informal Experience Skill Extractor (Phase 2 Development)

### Model Details
- **Model Identifier:** `elevate-x-ai-skill-extractor-indian-mock-v1`
- **Base Backbone:** `xlm-roberta-base` (Facebook AI / HuggingFace)
- **Architecture:** Multilingual Transformer with Token Classification Head (BIO Tagging: O, B-SKILL, I-SKILL)
- **Training Strategy:** Parameter-Efficient Transfer Learning (Top 2 Encoder Layers + Classification Head unfrozen, 14.18M trainable parameters)
- **Hardware Target:** Apple Silicon M2 MPS with automated CPU fallback
- **Model Provenance:** `synthetic_mock_development` (Trained on 4,150 synthetic records; validated on 500; benchmarked on 550)
- **Safety Constraint:** Genuine Indian worker records currently: `0`. Real worker fine-tuning threshold: `500 verified records`.

### Intended Use
- Extracting technical, practical, tactile skills from informal oral transcripts of blue-collar workers across 10 occupations in Devanagari Hindi, Roman Hindi, Hinglish, and Indian English.

### Evaluation Benchmark
- **Exact Span F1:** `0.8334`
- **Partial Overlap F1:** `0.9978`
- **Binary Token F1:** `0.9995`
- **Inference Speed:** `0.46 ms / record`
- **Deterministic Splitting:** Seed 42, 80/10/10 split without record overlap.
