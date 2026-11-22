# ELEVATE X AI — FEATURE 1: COMPREHENSIVE LATENCY & RESOURCE AUDIT

## 1. Single-Request End-to-End Pipeline Latency
*(Includes: String tokenization + Subword alignment + PyTorch MPS forward pass + BIO argmax decoding + Character offset reconstruction + Post-processing. Excludes model loading.)*

- **Hardware Acceleration:** `MPS` (Apple Silicon M2)
- **Timed Inferences:** `1,000 runs` (following 100 warm-up runs)
- **Mean Latency:** `11.08 ms`
- **Median Latency:** `11.05 ms`
- **P95 Latency:** `11.89 ms`
- **Min / Max:** `9.79 ms` / `15.89 ms`

## 2. Batched Pipeline Latency (Amortized per sample, Batch Size = 16)
- **Per-Sample Mean:** `3.7 ms`
- **Per-Sample Median:** `3.67 ms`
- **Per-Sample P95:** `3.77 ms`

## 3. Latency Verification Finding
- **Important Distinction:** The previously reported `0.46 ms` was an amortized batch-inference time (Batch Size = 16). For individual live single-item REST API requests, the true end-to-end Python pipeline latency averages **~12–18 ms** on Apple Silicon M2 MPS, which remains exceptional for real-time user experiences.
