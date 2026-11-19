"""
ELEVATE X AI — FEATURE 1: DATASET LOADERS & PROVENANCE TRACKER
Provides strictly isolated loaders for:
1. English SkillSpan (train, dev, test) for official benchmark experiments
2. Genuine Indian Worker descriptions (quarantined, 0 records pending fieldwork)
3. Synthetic development examples (marked synthetic_test_stub)
4. Official reference catalogues (ESCO, O*NET, NSQF)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "datasets" / "informal_skill_extraction" / "raw"
PROCESSED_DIR = BASE_DIR / "datasets" / "informal_skill_extraction" / "processed"

SKILLSPAN_DIR = RAW_DIR / "skillspan"
SKILLSPAN_CLEANED_DIR = PROCESSED_DIR / "skillspan"
REAL_WORKER_DIR = RAW_DIR / "indian_worker_data" / "real"
SYNTH_CORPUS_PATH = PROCESSED_DIR / "indian_worker_data" / "synthetic_augmentation" / "synthetic_augmented_corpus.jsonl"
CANONICAL_CATALOGUE_PATH = PROCESSED_DIR / "indian_worker_data" / "canonical_skill_catalogue.json"

class DatasetProvenance:
    SKILLSPAN_BENCHMARK = "english_skillspan_benchmark"
    GENUINE_INDIAN_WORKER = "real_field_interview"
    SYNTHETIC_DEVELOPMENT = "synthetic_test_stub"
    OFFICIAL_STANDARD = "official_curriculum_standard"

def load_skillspan(split: str = "train", max_samples: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Loads official SkillSpan partition (train, dev, or test).
    Preserves exact tokens and tags_skill BIO labels.
    """
    valid_splits = {"train", "dev", "test"}
    if split not in valid_splits:
        raise ValueError(f"Invalid split '{split}'. Must be one of {valid_splits}")
        
    file_path = SKILLSPAN_DIR / f"{split}.json"
    if not file_path.exists():
        # Fallback to cleaned processed file
        file_path = SKILLSPAN_CLEANED_DIR / f"cleaned_{split}.json"
        
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if max_samples and idx >= max_samples:
                break
            if not line.strip():
                continue
            item = json.loads(line)
            tokens = item.get("tokens", [])
            tags_skill = item.get("tags_skill", [])
            
            # Map SkillSpan tags to standard BIO:
            # "O" -> "O", "B-Skill" -> "B-SKILL", "I-Skill" -> "I-SKILL"
            clean_tags = []
            for t in tags_skill:
                t_upper = str(t).upper().strip()
                if t_upper in ["B", "B-SKILL"]:
                    clean_tags.append("B-SKILL")
                elif t_upper in ["I", "I-SKILL"]:
                    clean_tags.append("I-SKILL")
                else:
                    clean_tags.append("O")
                    
            records.append({
                "id": f"SKILLSPAN-{split.upper()}-{idx:05d}",
                "tokens": tokens,
                "bio_tags": clean_tags,
                "text": " ".join(tokens),
                "source": item.get("source", "job_posting"),
                "provenance": DatasetProvenance.SKILLSPAN_BENCHMARK,
                "language": "english"
            })
            
    return records

def load_genuine_indian_worker_data(trade_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Loads authentic field interview records.
    Returns empty list if genuine collection is pending.
    """
    records = []
    if REAL_WORKER_DIR.exists():
        for f in REAL_WORKER_DIR.glob("*.jsonl"):
            with open(f, "r", encoding="utf-8") as fp:
                for line in fp:
                    if line.strip():
                        r = json.loads(line)
                        if r.get("source_type") == "real_field_interview":
                            if not trade_id or r.get("occupation_id") == trade_id:
                                r["provenance"] = DatasetProvenance.GENUINE_INDIAN_WORKER
                                records.append(r)
    return records

def load_synthetic_development_data(max_samples: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Loads quarantined synthetic augmented records for pipeline testing.
    Explicitly tags every record as synthetic_test_stub.
    """
    records = []
    if SYNTH_CORPUS_PATH.exists():
        with open(SYNTH_CORPUS_PATH, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                if max_samples and idx >= max_samples:
                    break
                if line.strip():
                    r = json.loads(line)
                    r["provenance"] = DatasetProvenance.SYNTHETIC_DEVELOPMENT
                    records.append(r)
    return records

def load_canonical_skill_catalogue() -> List[Dict[str, Any]]:
    """Loads 32 granular competencies with NSQF, ESCO, and O*NET crosswalks."""
    if not CANONICAL_CATALOGUE_PATH.exists():
        return []
    with open(CANONICAL_CATALOGUE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else data.get("skills", [])

