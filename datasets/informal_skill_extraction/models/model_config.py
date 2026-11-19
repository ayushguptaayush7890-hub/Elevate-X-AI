"""
ELEVATE X AI — FEATURE 1: MODEL CONFIGURATION & HARDWARE DETECTOR
Informal Experience -> Skill Extraction System
Supports Apple Silicon MPS (M1/M2/M3) and CPU fallback.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parents[3]
MODELS_DIR = BASE_DIR / "datasets" / "informal_skill_extraction" / "models"
REPORTS_DIR = BASE_DIR / "datasets" / "informal_skill_extraction" / "reports" / "model_benchmarks"
DATASETS_DIR = BASE_DIR / "datasets" / "informal_skill_extraction"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# BIO Tags
BIO_TAGS = ["O", "B-SKILL", "I-SKILL"]
TAG2ID = {tag: i for i, tag in enumerate(BIO_TAGS)}
ID2TAG = {i: tag for i, tag in enumerate(BIO_TAGS)}

# 8 Functional Skill Categories
SKILL_CATEGORIES = [
    "technical_tactile",
    "tool_operation",
    "quality_inspection",
    "troubleshooting_repair",
    "safety_compliance",
    "measurement_planning",
    "client_communication",
    "material_handling"
]
CATEGORY2ID = {cat: i for i, cat in enumerate(SKILL_CATEGORIES)}
ID2CATEGORY = {i: cat for i, cat in enumerate(SKILL_CATEGORIES)}

# 10 Vocational Occupations
OCCUPATIONS = [
    "TRD-01: Tailor and Garment Worker",
    "TRD-02: Electrician",
    "TRD-03: Plumber",
    "TRD-04: Motor Mechanic",
    "TRD-05: Carpenter",
    "TRD-06: Welder",
    "TRD-07: Mason / Raj Mistri",
    "TRD-08: Painter",
    "TRD-09: Agriculture and Irrigation Worker",
    "TRD-10: Mobile Repair Technician"
]
OCCUPATION_CODES = [
    "TRD-01", "TRD-02", "TRD-03", "TRD-04", "TRD-05",
    "TRD-06", "TRD-07", "TRD-08", "TRD-09", "TRD-10"
]
OCC2ID = {code: i for i, code in enumerate(OCCUPATION_CODES)}
ID2OCC = {i: code for i, code in enumerate(OCCUPATION_CODES)}

# Candidate Model Hub Identifiers
CANDIDATE_MODELS = {
    "xlm_roberta": {
        "name": "XLM-RoBERTa Base",
        "hf_model_id": "xlm-roberta-base",
        "description": "Multilingual RoBERTa (100 languages, 250k vocab, 278M params)",
        "role": "primary_candidate",
        "license": "MIT"
    },
    "muril": {
        "name": "MuRIL Base Cased",
        "hf_model_id": "google/muril-base-cased",
        "description": "Multilingual Representation for Indian Languages (Devanagari, Roman Hindi, English, 236M params)",
        "role": "primary_indic_alternative",
        "license": "Apache-2.0"
    },
    "indicbert": {
        "name": "IndicBERT v1",
        "hf_model_id": "ai4bharat/indic-bert",
        "description": "Indic-specific ALBERT (12 Indic languages, 33M params)",
        "role": "lightweight_indic_alternative",
        "license": "MIT"
    },
    "mbert": {
        "name": "mBERT Base Cased",
        "hf_model_id": "bert-base-multilingual-cased",
        "description": "Multilingual BERT (104 languages, 178M params)",
        "role": "multilingual_baseline",
        "license": "Apache-2.0"
    },
    "distil_mbert": {
        "name": "DistilBERT Multilingual",
        "hf_model_id": "distilbert-base-multilingual-cased",
        "description": "6-layer distilled multilingual BERT (134M params, fast inference)",
        "role": "edge_fast_alternative",
        "license": "Apache-2.0"
    }
}

@dataclass
class ModelConfig:
    # Model Selection
    model_key: str = "xlm_roberta"
    pretrained_model_name_or_path: str = "xlm-roberta-base"
    
    # Architecture
    max_seq_length: int = 128
    num_bio_labels: int = len(BIO_TAGS)
    num_categories: int = len(SKILL_CATEGORIES)
    num_occupations: int = len(OCCUPATION_CODES)
    dropout_rate: float = 0.2
    
    # Training / Benchmark Hyperparameters
    batch_size: int = 16
    learning_rate: float = 3e-5
    weight_decay: float = 0.01
    num_train_epochs: int = 3
    warmup_ratio: float = 0.1
    eval_batch_size: int = 32
    seed: int = 42
    
    # Hardware & Performance
    use_mps: bool = True
    cpu_fallback: bool = True
    gradient_accumulation_steps: int = 1
    fp16: bool = False
    
    # Canonical Matching
    canonical_match_threshold: float = 0.65
    embedding_dim: int = 768
    
    # Safety Gate
    minimum_genuine_records_gate: int = 500
    
    def get_device(self) -> str:
        """Determines optimal PyTorch device on Mac M2 (MPS vs CPU)."""
        if hasattr(self, "_cached_device"):
            return self._cached_device
        try:
            import sys
            if "torch" in sys.modules:
                import torch
                if self.use_mps and torch.backends.mps.is_available() and torch.backends.mps.is_built():
                    self._cached_device = "mps"
                    return "mps"
            import platform
            if self.use_mps and platform.system() == "Darwin" and platform.machine() == "arm64":
                self._cached_device = "mps"
                return "mps"
        except Exception:
            pass
        self._cached_device = "cpu"
        return self._cached_device

default_config = ModelConfig()

