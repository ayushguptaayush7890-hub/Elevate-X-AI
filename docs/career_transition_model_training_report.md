# Elevate X AI — Career Transition Model Training Report

## 1. Model Objectives & Architecture

The career transition system utilizes a hybrid model architecture combining:
1. **PyTorch Knowledge Graph Embeddings:** A Node2Vec / Skip-gram graph representation model trained on 192,802 positive and sampled negative edge pairs to learn structural topological proximity between occupations and competencies.
2. **Semantic Competency Calibration:** Calibrated similarity thresholds for the `BAAI/bge-small-en-v1.5` encoder to prevent the high false-positive rates identified in earlier audits.
3. **Deterministic Compatibility Ranker:** An explainable linear programming score that weights skill overlap, structural graph cosine distance, and semantic similarity.

---

## 2. PyTorch Graph Embedding Training

### Model Specifications
- **Model Type:** PyTorch Node2Vec / Graph Skip-gram Embedding
- **Vocabulary Size:** 19,208 entities (occupations + competencies)
- **Embedding Dimension:** 64
- **Training Samples:** 192,802 pairs (edges + negative samples)
- **Hardware Acceleration:** Apple Silicon MPS (`torch.device("mps")`)
- **Optimizer:** Adam (lr = 0.01)
- **Batch Size:** 2,048
- **Saved Weights:** `datasets/career_transition/models/graph_embeddings/occupation_graph_model.pt`

### Training Progression & Convergence
| Epoch | Loss | Link Prediction Discrimination Accuracy | Elapsed Time |
|---|---|---|---|
| Epoch 1 | 1.1559 | 70.57% | 1.34s |
| Epoch 2 | 0.4509 | 94.86% | 1.32s |
| Epoch 3 | 0.1410 | 98.93% | 1.33s |
| **Epoch 4** | **0.0567** | **99.76%** | **1.35s** |

Total training time: **5.34 seconds** on Apple Silicon M2. The loss converged rapidly to 0.0567 with 99.76% accuracy in discriminating genuine occupational skill relationships from negative pairs.

---

## 3. Semantic Competency Matcher Calibration

### Calibration Thresholds (`calibration_config.json`)
- **Exact Match:** 1.00 (Canonical ESCO/O*NET/NCO ID or exact normalized string)
- **Synonym Similarity Threshold:** 0.85 (Official alternative labels and verified aliases)
- **Partial Match Threshold:** 0.75 (Adjacent competencies requiring related context validation)
- **False Positive Rejection Threshold:** < 0.65 (Rejects cross-domain semantic false alarms, e.g., Python vs Sewing)

### Benchmark Evaluation Metrics
- **Evaluated Pairs:** 1,001 authentic concept pairs
- **Synonym Recall @ 0.85:** 94.2%
- **Negative Rejection Rate @ 0.65:** 98.8%
- **F1 Score:** 0.964

---

## 4. Grounded Transition Bridge Generator

Instead of ungrounded generative hallucinations, the Transition Blueprint generator uses a structured four-stage curriculum where:
- **Missing and Bridgeable competencies** identified during the 5-tier evidence audit are partitioned across Stages 1 through 4.
- **Authentic Learning Resources** are bound directly from `verified_resources.json` (SWAYAM, NPTEL, Coursera, MIT OCW).
- **Execution tasks** are grounded in practical trade bridging, equipment calibration, and diagnostic assessments.
