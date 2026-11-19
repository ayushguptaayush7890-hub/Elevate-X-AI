"""
ELEVATE X AI — FEATURE 1: MODEL SERVICE FOR FASTAPI INTEGRATION
Singleton lifecycle service managing skill extraction model inference for the backend API.
"""

from typing import Dict, Any, Optional
from .model_config import default_config

class SkillExtractionService:
    @staticmethod
    def extract_from_narrative(text: str, occupation_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes worker narrative and returns structured skill entities.
        """
        from .inference import extract_skills
        return extract_skills(text=text, occupation_hint=occupation_hint)

    @staticmethod
    def get_service_status() -> Dict[str, Any]:
        """
        Returns model status, loaded architecture, and hardware information.
        """
        device = default_config.get_device()
        return {
            "service": "feature1_skill_extraction",
            "status": "operational",
            "primary_model": default_config.model_key,
            "pretrained_backbone": default_config.pretrained_model_name_or_path,
            "device": device.upper(),
            "hardware_acceleration": "Apple Silicon MPS" if device == "mps" else "CPU Fallback",
            "canonical_catalogue_size": 32,
            "training_safety_gate": "LOCKED (Genuine Indian worker records = 0, threshold = 500)"
        }

