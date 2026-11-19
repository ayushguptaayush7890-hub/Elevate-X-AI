"""
ELEVATE X AI — FEATURE 1: SKILL EXTRACTION MODEL PACKAGE
"""

from .model_config import ModelConfig, default_config

__all__ = [
    "ModelConfig",
    "default_config",
    "ModularSkillExtractor",
    "extract_skills",
    "get_skill_extractor",
    "SkillExtractionService"
]


def __getattr__(name: str):
    if name == "ModularSkillExtractor":
        from .skill_extractor import ModularSkillExtractor
        return ModularSkillExtractor
    if name == "extract_skills":
        from .inference import extract_skills
        return extract_skills
    if name == "get_skill_extractor":
        from .inference import get_skill_extractor
        return get_skill_extractor
    if name == "SkillExtractionService":
        from .model_service import SkillExtractionService
        return SkillExtractionService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


