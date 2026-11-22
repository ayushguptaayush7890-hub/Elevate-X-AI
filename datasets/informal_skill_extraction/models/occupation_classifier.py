"""
ELEVATE X AI — FEATURE 1: OCCUPATION CLASSIFIER
Categorizes verbatim descriptions into one of the 10 target vocational trades:
TRD-01: Tailor and Garment Worker
TRD-02: Electrician
TRD-03: Plumber
TRD-04: Motor Mechanic
TRD-05: Carpenter
TRD-06: Welder
TRD-07: Mason / Raj Mistri
TRD-08: Painter
TRD-09: Agriculture and Irrigation Worker
TRD-10: Mobile Repair Technician
"""

import re
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np

TRADE_VOCABULARY = {
    "TRD-01": ["tailor", "silai", "kapda", "fabric", "overlock", "needle", "suit", "shirt", "pant", "bakram", "collar", "dart", "cutting", "blouse", "measuring tape", "inch tape"],
    "TRD-02": ["electrician", "wiring", "mcb", "conduit", "switch", "socket", "earthing", "multimeter", "voltage", "phase", "neutral", "short circuit", "jhirri", "inverter", "wire"],
    "TRD-03": ["plumber", "pipe", "cpvc", "upvc", "gi pipe", "solvent", "threading", "die", "leakage", "diverter", "tap", "flush", "cistern", "valve", "drainage", "nal", "water tank"],
    "TRD-04": ["mechanic", "engine", "bike", "car", "brake", "disc", "caliper", "clutch", "oil change", "spark plug", "feeler gauge", "filter", "fork", "sprocket", "carburetor"],
    "TRD-05": ["carpenter", "wood", "plywood", "sunmica", "fevicol", "saw", "randa", "plane", "chaurasi", "chisel", "furniture", "mortise", "tenon", "table", "door"],
    "TRD-06": ["welder", "welding", "arc", "mig", "tig", "electrode", "flux", "grinder", "joint", "iron", "ms pipe", "goggles", "slag", "fabrication"],
    "TRD-07": ["mason", "mistri", "chunai", "brick", "cement", "masala", "plaster", "gurmala", "trowel", "sahul", "plumb bob", "water level", "foundation", "tiles"],
    "TRD-08": ["painter", "paint", "putty", "roller", "brush", "primer", "regmar", "sanding", "distemper", "emulsion", "waterproofing", "deewar", "wall"],
    "TRD-09": ["agriculture", "kisan", "khet", "drip irrigation", "lateral", "venturi", "fertilizer", "rotavator", "tractor", "pump", "sprayer", "crop"],
    "TRD-10": ["mobile", "smartphone", "folder", "display", "charging", "cc pin", "smd", "blower", "jumper", "shorting", "motherboard", "touch", "connector"]
}

TRADE_NAMES = {
    "TRD-01": "Tailor and Garment Worker",
    "TRD-02": "Electrician",
    "TRD-03": "Plumber",
    "TRD-04": "Motor Mechanic",
    "TRD-05": "Carpenter",
    "TRD-06": "Welder",
    "TRD-07": "Mason / Raj Mistri",
    "TRD-08": "Painter",
    "TRD-09": "Agriculture and Irrigation Worker",
    "TRD-10": "Mobile Repair Technician"
}

class OccupationClassifier:
    def __init__(self):
        self._train_classifier()

    def _train_classifier(self):
        corpus = []
        labels = []
        
        # 1. Base vocabulary
        for tid, terms in TRADE_VOCABULARY.items():
            for term in terms:
                corpus.append(term)
                labels.append(tid)
                corpus.append(f"main {term} ka kaam karta hu")
                labels.append(tid)
                corpus.append(f"expert in {term}")
                labels.append(tid)

        # 2. Devanagari & Vernacular terms from Language Registry
        from pathlib import Path
        import json
        vocab_path = Path(__file__).resolve().parents[1] / "processed" / "indian_worker_data" / "language_vocabulary" / "trade_terms_hindi_hinglish.json"
        if vocab_path.exists():
            try:
                with open(vocab_path, "r", encoding="utf-8") as f:
                    terms_list = json.load(f)
                    for item in terms_list:
                        tid = item.get("trade_id")
                        if tid in TRADE_NAMES:
                            if item.get("devanagari"):
                                corpus.append(item["devanagari"])
                                labels.append(tid)
                            if item.get("roman_hinglish"):
                                corpus.append(item["roman_hinglish"])
                                labels.append(tid)
            except Exception:
                pass

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=500, C=5.0))
        ])
        self.pipeline.fit(corpus, labels)

    def classify(self, text: str) -> Dict[str, Any]:
        """Predicts trade identifier from verbatim text."""
        clean_text = text.lower().strip()
        if not clean_text:
            return {"occupation_id": "TRD-01", "occupation_title": TRADE_NAMES["TRD-01"], "confidence": 0.1}

        pred_id = str(self.pipeline.predict([clean_text])[0])
        prob_vec = self.pipeline.predict_proba([clean_text])[0]
        conf = float(np.max(prob_vec))

        # Check if trade vocabulary keyword actually matched in text
        has_direct_keyword = False
        for tid, kws in TRADE_VOCABULARY.items():
            for kw in kws:
                if re.search(rf"\b{re.escape(kw)}\b", clean_text, re.IGNORECASE):
                    has_direct_keyword = True
                    break
            if has_direct_keyword:
                break

        # If confidence is low and no direct vocational trade keyword is present, abstain
        if conf < 0.35 and not has_direct_keyword:
            return {
                "occupation_id": "UNCLASSIFIED",
                "occupation_title": "General / Technical Professional",
                "confidence": round(conf, 4)
            }

        return {
            "occupation_id": pred_id,
            "occupation_title": TRADE_NAMES.get(pred_id, "Unknown Trade"),
            "confidence": round(conf, 4)
        }
