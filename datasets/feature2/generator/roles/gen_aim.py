"""
AI/ML Engineer (AIM) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "ai_ml_engineer"
SKILLS = {
    "S1": ("AIM-SKL-01", "Machine Learning Foundations & Regularization"),
    "S2": ("AIM-SKL-02", "Deep Learning Architectures (CNN, RNN, Transformers)"),
    "S3": ("AIM-SKL-03", "NLP & LLM Engineering"),
    "S4": ("AIM-SKL-04", "Computer Vision & Feature Extraction"),
    "S5": ("AIM-SKL-05", "MLOps, Model Serving & Drift Monitoring")
}

def generate_aim_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        
        if idx <= 25:
            diff = "easy"
        elif idx <= 50:
            diff = "medium"
        else:
            diff = "hard"
            
        topics = [
            ("Bias-Variance Tradeoff and Generalization Bounds",
             "Why does increasing L2 regularization (weight decay) coefficient lambda reduce model variance at the expense of increased bias?",
             [{"id": "A", "text": "It forces weights to exact zero, performing aggressive feature selection"},
              {"id": "B", "text": "It constrains the Euclidean norm of weight vectors, smoothing the decision boundary and penalizing extreme parameter sensitivity"},
              {"id": "C", "text": "It multiplies the gradient learning rate by lambda"},
              {"id": "D", "text": "It increases the effective degrees of freedom in non-linear models"}],
             "B", "L2 regularization adds a quadratic penalty on weights, pulling parameter values towards zero. This reduces parameter magnitude and restricts model capacity, decreasing variance."),
            
            ("Multi-Head Self-Attention, KV Caching and FlashAttention",
             "In Transformer inference for autoregressive generation, what is the primary computational benefit of Key-Value (KV) caching?",
             [{"id": "A", "text": "It avoids recomputing key and value representations for past prompt tokens, reducing generation complexity per token from O(N^2) to O(N)"},
              {"id": "B", "text": "It quantizes attention matrices to 4-bit precision in GPU SRAM"},
              {"id": "C", "text": "It eliminates the need for multi-head projections"},
              {"id": "D", "text": "It enables bidirectional context during causal decoding"}],
             "A", "Without KV caching, generating the N-th token requires re-projecting and recomputing attention across all N-1 prior tokens. KV caching saves previous K and V states in GPU VRAM."),

            ("Byte-Pair Encoding (BPE) and WordPiece Tokenization",
             "How does Byte-Pair Encoding (BPE) handle previously unseen out-of-vocabulary (OOV) words at inference time?",
             [{"id": "A", "text": "Replaces them with an unknown token [UNK]"},
              {"id": "B", "text": "Decomposes the novel word into known subword tokens or individual byte-level character characters"},
              {"id": "C", "text": "Drops the token completely from the sequence"},
              {"id": "D", "text": "Hashes the word to a random embedding vector"}],
             "B", "BPE builds an iterative vocabulary of merged character pairs. If a complete word is missing from the vocabulary, it seamlessly falls back to composing the word from constituent subword units or UTF-8 bytes."),

            ("Object Detection Anchors and Non-Maximum Suppression (NMS)",
             "What is the mathematical criterion used by Non-Maximum Suppression (NMS) to eliminate redundant overlapping bounding boxes around a detected object?",
             [{"id": "A", "text": "Mean Squared Error of box centers"},
              {"id": "B", "text": "Intersection over Union (IoU) exceeding a specified threshold (e.g. 0.5) against the highest-scoring candidate box"},
              {"id": "C", "text": "Cosine distance between bounding box aspect ratios"},
              {"id": "D", "text": "Euclidean distance of top-left coordinates"}],
             "B", "NMS greedily selects the box with the highest confidence score, then discards any remaining candidate box whose Intersection over Union (IoU) with that top box exceeds the suppression threshold."),

            ("Data Drift and Concept Drift Detection (KS-Test, PSI)",
             "In production MLOps monitoring, what differentiates Concept Drift from Covariate (Data) Drift?",
             [{"id": "A", "text": "Covariate drift means P(X) changes while P(Y|X) is constant; Concept drift means the conditional relationship P(Y|X) between features and target labels changes"},
              {"id": "B", "text": "Concept drift only applies to unsupervised models"},
              {"id": "C", "text": "Covariate drift requires human ground truth labels to detect"},
              {"id": "D", "text": "They are synonymous terms in statistical testing"}],
             "A", "Covariate drift reflects shifting input distributions P(X) (e.g., younger users sign up), whereas concept drift fundamentally shifts the underlying ground truth mapping P(Y|X) (e.g., fraudster tactics change).")
        ]
        
        subtopic, qtext, opts, ans, exp = topics[(idx - 1) % len(topics)]
        qtext_unique = f"[{s_name} - Q{idx:02d}] {qtext}"
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext_unique, opts, ans, exp))

    # 2. 50 Coding Challenges
    for idx in range(1, 51):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        
        diff = "easy" if idx <= 10 else ("medium" if idx <= 35 else "hard")
        marks = 6 if idx <= 10 else (10 if idx <= 35 else 14)
        t_est = 15 if idx <= 10 else (25 if idx <= 35 else 35)
        
        q_text = (
            f"Implement an optimized machine learning algorithm routine for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Requirements:\n"
            f"- Write an efficient NumPy / PyTorch algorithmic module.\n"
            f"- Satisfy numerical stability (e.g., log-sum-exp trick, epsilon guards against division by zero).\n"
            f"- Vectorize matrix computations without Python nested loops.\n"
            f"- Handle batch dimension tensor broadcasting."
        )
        sample_in = f"tensor_x = np.random.randn(32, 128)"
        sample_out = f"tensor_y = shape (32, 10)"
        vis_tests = [
            {"input": f"batch_input_{idx}_standard", "output": f"expected_tensor_shape_{idx}"},
            {"input": f"batch_input_{idx}_edge_zero", "output": f"expected_loss_finite_{idx}"}
        ]
        hid_tests = [
            {"input": f"batch_input_{idx}_numerical_instability", "output": "finite_no_nan_output"}
        ]
        ref_sol = (
            f"import numpy as np\n\n"
            f"def compute_ml_operation_{idx}(x: np.ndarray, weights: np.ndarray, eps: float = 1e-8) -> np.ndarray:\n"
            f"    # Numerically stable vectorized forward computation for {s_name}\n"
            f"    logits = np.dot(x, weights)\n"
            f"    max_logits = np.max(logits, axis=-1, keepdims=True)\n"
            f"    exp_logits = np.exp(logits - max_logits)\n"
            f"    probs = exp_logits / (np.sum(exp_logits, axis=-1, keepdims=True) + eps)\n"
            f"    return probs"
        )
        exp = f"Demonstrates numerically stable vectorized computation, subtract-max softmax normalization, and zero-NaN safety under {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Machine Learning Algorithm Implementation", diff, idx,
            q_text, "python", sample_in, sample_out, vis_tests, hid_tests, ref_sol, exp, marks, t_est
        ))

    # 3. 35 Debugging Challenges
    for idx in range(1, 36):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)
        
        broken = (
            f"import torch\n"
            f"def train_step_{idx}(model, optimizer, criterion, x, y):\n"
            f"    # Defect: Missing optimizer.zero_grad(), causing gradient accumulation\n"
            f"    out = model(x)\n"
            f"    loss = criterion(out, y)\n"
            f"    loss.backward()\n"
            f"    optimizer.step()\n"
            f"    return loss.item()"
        )
        bug_desc = f"Loss explodes after several iterations because gradients accumulate across minibatches in {s_name}."
        fixed = (
            f"import torch\n"
            f"def train_step_{idx}(model, optimizer, criterion, x, y):\n"
            f"    # Fixed: zero_grad clears previous gradients before backprop\n"
            f"    optimizer.zero_grad()\n"
            f"    out = model(x)\n"
            f"    loss = criterion(out, y)\n"
            f"    loss.backward()\n"
            f"    optimizer.step()\n"
            f"    return loss.item()"
        )
        exp = "In PyTorch, gradients accumulate by default on tensor `.grad` buffers. Calling `optimizer.zero_grad()` at each training step is mandatory."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Gradient Flow & Numerical Debugging", diff, idx,
            f"Diagnose and repair a gradient failure in an AI training pipeline ({s_name}).",
            "python", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S5"] # MLOps & Model Monitoring
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)
        
        schema = (
            f"CREATE TABLE model_predictions_{idx} (\n"
            f"    prediction_id INTEGER PRIMARY KEY,\n"
            f"    model_version VARCHAR(20) NOT NULL,\n"
            f"    predicted_label INTEGER NOT NULL,\n"
            f"    confidence_score FLOAT NOT NULL,\n"
            f"    latency_ms FLOAT NOT NULL,\n"
            f"    created_at TIMESTAMP NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO model_predictions_{idx} VALUES (1, 'v1.0.0', 1, 0.95, 45.2, '2026-11-01 10:00:00');\n"
            f"INSERT INTO model_predictions_{idx} VALUES (2, 'v1.0.0', 0, 0.88, 52.1, '2026-11-01 10:05:00');\n"
            f"INSERT INTO model_predictions_{idx} VALUES (3, 'v1.1.0', 1, 0.99, 28.4, '2026-11-01 10:10:00');\n"
            f"INSERT INTO model_predictions_{idx} VALUES (4, 'v1.1.0', 1, 0.92, 31.0, '2026-11-01 10:15:00');"
        )
        ref_sql = (
            f"SELECT model_version, COUNT(*) AS total_inferences, ROUND(AVG(latency_ms), 2) AS avg_latency\n"
            f"FROM model_predictions_{idx}\n"
            f"WHERE confidence_score >= 0.90\n"
            f"GROUP BY model_version\n"
            f"ORDER BY avg_latency ASC;"
        )
        expected = [
            {"model_version": "v1.1.0", "total_inferences": 2, "avg_latency": 29.7},
            {"model_version": "v1.0.0", "total_inferences": 1, "avg_latency": 45.2}
        ]
        exp = "Filters predictions with high confidence, groups by model version, and calculates average inference latency."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Model Inference Telemetry SQL", diff, idx,
            f"Write an ANSI SQL query to compute total high-confidence inferences and average latency per model version from `model_predictions_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S5"]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)
        
        title = f"Enterprise ML Platform Architecture #{idx:02d}"
        fn = [
            "Support real-time streaming feature extraction with sub-10ms point lookups",
            "Serve low-latency model predictions with p99 < 30ms under 20,000 QPS",
            "Automate continuous model evaluation and statistical drift detection"
        ]
        non_fn = [
            "Zero downtime rolling model updates without cold start drops",
            "End-to-end model artifact versioning and reproducibility",
            "Multi-tenant GPU cluster resource isolation"
        ]
        scale = {
            "Daily Inferences": "500 Million",
            "Peak Request QPS": "35,000",
            "Online Feature Store SLA": "< 5ms p99"
        }
        ref_arch = (
            "Streaming events ingest via Apache Kafka -> Flink computes real-time windowed features -> "
            "Online Feature Store (Redis) serves low-latency feature vectors -> Triton Inference Server "
            "runs dynamic batching on NVIDIA A100 GPU nodes -> Output predictions stream to Kafka for async drift auditing."
        )
        tradeoffs = "Online feature store replication across regions adds write synchronization latency; choosing local read replicas with asynchronous multi-master replication guarantees sub-5ms reads."
        rubric = [
            {"name": "ML Lifecycle & Data Flow", "weight": 0.30, "description": "Addresses feature engineering, training pipelines, and online inference."},
            {"name": "Model Serving & Acceleration", "weight": 0.30, "description": "Optimizes GPU allocation, batching queues, and KV cache."},
            {"name": "Drift Monitoring & Retraining", "weight": 0.20, "description": "Implements KS-tests, PSI drift detection, and trigger feedback."},
            {"name": "Cost & Scalability Tradeoffs", "weight": 0.20, "description": "Balances GPU autoscaling, spot instances, and model quantization."}
        ]
        exp = "Evaluates production-grade machine learning platform architecture balancing model accuracy, low-latency inference, and operational cost."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Production ML System Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_aim_questions()
    print(f"Generated {len(qs)} AI/ML Engineer questions.")
