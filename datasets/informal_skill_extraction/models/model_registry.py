"""
ELEVATE X AI — FEATURE 1: MODEL REGISTRY & HUB ADAPTER
Manages model instances, tokenizers, pretrained checkpoints, and device placement
across XLM-RoBERTa, MuRIL, IndicBERT, mBERT, and Distil-mBERT.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    AutoConfig
)

try:
    from .model_config import CANDIDATE_MODELS, ModelConfig, default_config, BIO_TAGS, TAG2ID, ID2TAG
except (ImportError, ValueError):
    from model_config import CANDIDATE_MODELS, ModelConfig, default_config, BIO_TAGS, TAG2ID, ID2TAG

CHECKPOINTS_DIR = Path(__file__).resolve().parent / "checkpoints"
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)

class ModelRegistry:
    _loaded_models: Dict[str, Any] = {}
    _loaded_tokenizers: Dict[str, Any] = {}

    @classmethod
    def get_device(cls, prefer_mps: bool = True) -> torch.device:
        if prefer_mps and torch.backends.mps.is_available() and torch.backends.mps.is_built():
            return torch.device("mps")
        return torch.device("cpu")

    @classmethod
    def load_tokenizer(cls, model_key: str = "xlm_roberta"):
        if model_key in cls._loaded_tokenizers:
            return cls._loaded_tokenizers[model_key]

        model_info = CANDIDATE_MODELS.get(model_key, CANDIDATE_MODELS["xlm_roberta"])
        hf_id = model_info["hf_model_id"]

        try:
            tokenizer = AutoTokenizer.from_pretrained(hf_id)
        except Exception:
            # Fallback to local or fast alternative if offline
            tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

        cls._loaded_tokenizers[model_key] = tokenizer
        return tokenizer

    @classmethod
    def load_token_classification_model(
        cls,
        model_key: str = "xlm_roberta",
        checkpoint_path: Optional[str] = None,
        num_labels: int = len(BIO_TAGS)
    ):
        device = cls.get_device()
        cache_key = f"{model_key}_{num_labels}_{checkpoint_path}"
        if cache_key in cls._loaded_models:
            return cls._loaded_models[cache_key].to(device)

        model_info = CANDIDATE_MODELS.get(model_key, CANDIDATE_MODELS["xlm_roberta"])
        hf_id = model_info["hf_model_id"]

        ckpt = checkpoint_path
        if ckpt is None:
            # 1. Best Indian Mock fine-tuned checkpoint
            mock_best = CHECKPOINTS_DIR / "indian_mock" / "exp_indian_xlm_roberta" / "best_checkpoint"
            best_prod = CHECKPOINTS_DIR / "best_indian_model"
            eng_base = CHECKPOINTS_DIR / "english_baseline" / "exp_b_partial" / "best_checkpoint"

            if best_prod.exists() and (best_prod / "model.safetensors").exists():
                ckpt = str(best_prod)
            elif mock_best.exists() and (mock_best / "model.safetensors").exists():
                ckpt = str(mock_best)
            elif eng_base.exists() and (eng_base / "model.safetensors").exists():
                ckpt = str(eng_base)
            else:
                default_cp = CHECKPOINTS_DIR / f"{model_key}_skillspan"
                if default_cp.exists() and (default_cp / "model.safetensors").exists():
                    ckpt = str(default_cp)

        if ckpt and Path(ckpt).exists() and (Path(ckpt) / "model.safetensors").exists():
            print(f"[ModelRegistry] Loading fine-tuned token classification checkpoint from: {ckpt}")
            model = AutoModelForTokenClassification.from_pretrained(ckpt)
        else:
            raise FileNotFoundError(
                f"[ModelRegistry] Critical: No trained fine-tuned token classification checkpoint found at '{ckpt}'. "
                f"Automatic random initialization or silent fallback is strictly prohibited."
            )

        model = model.to(device)
        model.eval()
        cls._loaded_models[cache_key] = model
        return model

