"""
ELEVATE X AI — FEATURE 1: SKILL CATEGORY CLASSIFIER
Categorizes extracted skill phrases into the 8 functional categories:
1. technical_tactile
2. tool_operation
3. quality_inspection
4. troubleshooting_repair
5. safety_compliance
6. measurement_planning
7. client_communication
8. material_handling
"""

import re
from typing import Dict, List, Tuple, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np

try:
    from .model_config import SKILL_CATEGORIES, default_config
except (ImportError, ValueError):
    from model_config import SKILL_CATEGORIES, default_config

# Lexical priors for Indian informal vocational terminology
CATEGORY_KEYWORDS = {
    "tool_operation": [
        "machine", "blower", "solder", "cutter", "chaurasi", "randa", "welding",
        "drill", "grinder", "roller", "iron", "die", "auzaar", "patti", "trowel",
        "hacksaw", "chisel", "wrench", "screwdriver", "spanner", "hammer", "multimeter"
    ],
    "technical_tactile": [
        "silai", "jointing", "wiring", "plaster", "chunai", "fitting", "conduit",
        "soldering", "stitching", "cutting", "assembly", "winding", "threading",
        "gluing", "solvent", "jhirri", "chudi", "leveling", "screed", "mortar"
    ],
    "quality_inspection": [
        "check", "test", "sahul", "level", "feeler gauge", "inspection", "measurement",
        "alignment", "gauge", "finishing", "dekhna", "jaanch", "continuity", "leak test"
    ],
    "troubleshooting_repair": [
        "repair", "fault", "short circuit", "leakage", "tighten", "replace",
        "troubleshoot", "dismantle", "cleaning", "fix", "drain", "bleed", "tripping",
        "dhoondhna", "badalna", "theek karna", "jumper"
    ],
    "safety_compliance": [
        "safety", "earthing", "isolation", "insulated", "fuse", "mcb", "trip",
        "protective", "resistance", "danger", "hazard", "glove", "mask", "rccb"
    ],
    "measurement_planning": [
        "inch tape", "naap", "measurement", "water level", "drawing", "marking",
        "pattern", "layout", "dimension", "estimate", "calibration", "scale"
    ],
    "client_communication": [
        "customer", "grahak", "order", "requirement", "cost", "bill", "delivery",
        "complaint", "deal", "sample", "feedback", "conversation"
    ],
    "material_handling": [
        "fabric", "plywood", "cement", "pipe", "sand", "brick", "copper", "wire",
        "cable", "solvent", "oil", "coolant", "paint", "putty", "bakram", "kapda"
    ]
}

class SkillCategoryClassifier:
    def __init__(self):
        self.categories = SKILL_CATEGORIES
        self._init_classifier()

    def _init_classifier(self):
        # Build training corpus from domain keywords and knowledge base
        corpus = []
        labels = []
        for cat, kws in CATEGORY_KEYWORDS.items():
            for kw in kws:
                corpus.append(kw)
                labels.append(cat)
                # Augmented synthetic phrases for robust training
                corpus.append(f"{kw} se kaam karna")
                labels.append(cat)
                corpus.append(f"using {kw} for work")
                labels.append(cat)

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=500, C=5.0))
        ])
        self.pipeline.fit(corpus, labels)

    def classify_phrase(self, phrase: str) -> Dict[str, Any]:
        """Classifies a skill phrase into one of the 8 categories with confidence."""
        if not phrase.strip():
            return {"category": "technical_tactile", "confidence": 0.5, "probabilities": {}}

        clean_text = phrase.lower().strip()
        
        # Rule-based priority for explicit matches
        for cat, kws in CATEGORY_KEYWORDS.items():
            for kw in kws:
                if re.search(rf"\b{re.escape(kw)}\b", clean_text):
                    # Found strong keyword indicator
                    probs = {c: 0.05 for c in self.categories}
                    probs[cat] = 0.85
                    return {
                        "category": cat,
                        "confidence": 0.85,
                        "probabilities": probs,
                        "method": "lexical_heuristic"
                    }

        # Model inference
        pred_cat = self.pipeline.predict([clean_text])[0]
        prob_vec = self.pipeline.predict_proba([clean_text])[0]
        classes = self.pipeline.classes_
        
        probs = {cls: float(prob_vec[i]) for i, cls in enumerate(classes)}
        conf = float(np.max(prob_vec))

        return {
            "category": pred_cat,
            "confidence": round(conf, 4),
            "probabilities": probs,
            "method": "statistical_classifier"
        }

