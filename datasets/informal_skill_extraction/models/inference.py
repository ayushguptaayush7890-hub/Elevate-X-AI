"""
ELEVATE X AI — FEATURE 1: HIGH-LEVEL INFERENCE INTERFACE
Provides a clean, unified Python API for extracting skills from natural descriptions
in Hindi (Devanagari), Roman Hindi, Hinglish, and English.
"""

from typing import Dict, Any, Optional, List
from .skill_extractor import ModularSkillExtractor
from .model_config import default_config

_extractor_instance = None

def get_skill_extractor(config=None) -> ModularSkillExtractor:
    global _extractor_instance
    if _extractor_instance is None:
        _extractor_instance = ModularSkillExtractor(config or default_config)
    return _extractor_instance

def extract_skills(text: str, occupation_hint: Optional[str] = None) -> Dict[str, Any]:
    """
    Main inference entrypoint for Feature 1.
    
    Args:
        text: Raw natural language description from informal worker or resume.
        occupation_hint: Optional occupation code (e.g. 'TRD-01', 'TRD-02').
        
    Returns:
        Structured dictionary with extracted spans, categories, canonical mappings,
        confidence scores, and human review flags.
    """
    extractor = get_skill_extractor()
    return extractor.predict(text=text, occupation_hint=occupation_hint)

