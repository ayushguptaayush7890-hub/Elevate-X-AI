"""
ELEVATE X AI — FEATURE 1: CANONICAL SKILL RETRIEVER
Maps extracted skill phrases to the 32-skill Canonical Competency Catalogue
using semantic character n-gram cosine embeddings with confidence thresholding.

Guarantees:
1. Normalizes only a separate retrieval copy of text; preserves original phrase.
2. Returns top candidate matches with similarity confidence scores (0.0 to 1.0).
3. If confidence < 0.65, marks status as 'unmapped' and flags for human review.
4. Links official crosswalks: ESCO URI, O*NET SOC, and NSQF QP/NOS.
"""

import re
from typing import List, Dict, Optional, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

try:
    from .model_config import default_config, ModelConfig
    from .dataset_loader import load_canonical_skill_catalogue
except (ImportError, ValueError):
    from model_config import default_config, ModelConfig
    from dataset_loader import load_canonical_skill_catalogue

# Generic action words that should not trigger domain matches on their own
GENERIC_ACTION_WORDS = {
    "installation", "install", "installing",
    "operation", "operate", "operating",
    "checking", "check",
    "testing", "test",
    "inspection", "inspect", "inspecting",
    "fitting", "fit",
    "repair", "repairing",
    "service", "servicing",
    "apply", "application", "applying",
    "maintenance", "maintain",
    "cleaning", "clean",
    "work", "kaam", "karna"
}

# Semantic Competency Constraints & Signature Concepts for the 32 Canonical Skills
SKILL_SIGNATURES = {
    # TRD-01 Tailor and Garment Worker
    "SKL-TLR-001": {
        "occupation_id": "TRD-01",
        "required_any": ["lockstitch", "single needle", "silai machine", "sewing machine", "sewing", "industrial sewing", "garment assembly", "suit silta", "kurta silna", "stitching", "silai", "garment joining"],
        "forbidden_if_only": ["cutting", "naap", "overlock", "bakram", "collar", "tension", "service", "silai ka kaam", "tailor work"]
    },
    "SKL-TLR-002": {
        "occupation_id": "TRD-01",
        "required_any": ["overlock", "interlock", "serging", "kinari", "edge finishing", "edge serging"],
        "forbidden_if_only": ["lockstitch", "naap", "bakram"]
    },
    "SKL-TLR-003": {
        "occupation_id": "TRD-01",
        "required_any": ["bakram", "interlining", "collar", "fusible", "canvas"],
        "forbidden_if_only": ["naap", "overlock"]
    },
    "SKL-TLR-004": {
        "occupation_id": "TRD-01",
        "required_any": ["measurement", "naap", "fabric cutting", "kapde ki cutting", "pattern drafting", "cutting fabric", "cloth cutting", "garment pattern"],
        "forbidden_if_only": ["pipe", "conduit", "plywood", "metal", "wire", "cable"]
    },
    "SKL-TLR-005": {
        "occupation_id": "TRD-01",
        "required_any": ["katori", "katora", "blouse drafting", "dart stitching", "choli"],
        "forbidden_if_only": []
    },
    "SKL-TLR-006": {
        "occupation_id": "TRD-01",
        "required_any": ["machine tension", "bobbin tuning", "feed dog", "machine service", "tension calibration", "bobbin case"],
        "forbidden_if_only": []
    },

    # TRD-02 Electrician
    "SKL-ELE-001": {
        "occupation_id": "TRD-02",
        "required_any": ["conduit", "jhirri", "chasing", "wall chasing", "channel cutting", "pipe daalna", "conduit fitting", "pvc conduit"],
        "forbidden_if_only": ["mcb", "multimeter", "earthing", "wire pulling", "fish tape", "pulling"]
    },
    "SKL-ELE-002": {
        "occupation_id": "TRD-02",
        "required_any": ["mcb", "distribution board", "db box", "breaker", "panel termination", "db dressing", "fuse panel", "mcb fitting"],
        "forbidden_if_only": ["jhirri", "chasing", "multimeter"]
    },
    "SKL-ELE-003": {
        "occupation_id": "TRD-02",
        "required_any": ["multimeter", "voltage", "phase", "continuity", "neutral", "fault diagnosis", "faults check", "electrical fault", "phase tester"],
        "forbidden_if_only": ["conduit", "earthing pit", "fault repair", "meter reading", "bulb"]
    },
    "SKL-ELE-004": {
        "occupation_id": "TRD-02",
        "required_any": ["earthing", "earth pit", "grounding", "megger", "earth resistance"],
        "forbidden_if_only": []
    },

    # TRD-03 Plumber
    "SKL-PLM-001": {
        "occupation_id": "TRD-03",
        "required_any": ["solvent", "cement joint", "solvent cement", "solvent lagana", "solvent fitting", "pipe jointing"],
        "forbidden_if_only": ["cutting", "chudi", "threading", "diverter", "cistern", "tank", "unblocking", "cleaning"]
    },
    "SKL-PLM-002": {
        "occupation_id": "TRD-03",
        "required_any": ["die", "threading", "chudi", "gi pipe", "thread cutting", "pipe die"],
        "forbidden_if_only": ["solvent", "diverter"]
    },
    "SKL-PLM-003": {
        "occupation_id": "TRD-03",
        "required_any": ["diverter", "shower mixer", "wall mixer", "concealed mixer"],
        "forbidden_if_only": ["solvent", "die"]
    },
    "SKL-PLM-004": {
        "occupation_id": "TRD-03",
        "required_any": ["cistern", "flush tank", "float valve", "flush repair", "flush cistern", "siphon washer"],
        "forbidden_if_only": ["cpvc", "gi pipe", "chudi", "die"]
    },

    # TRD-04 Motor Mechanic
    "SKL-MEC-001": {
        "occupation_id": "TRD-04",
        "required_any": ["engine oil", "oil change", "oil drain", "mobil oil", "engine oil drain", "oil filter", "lubricant"],
        "forbidden_if_only": ["engine repair", "engine overhaul", "tappet", "brake", "valve", "spark plug", "cable lubrication"]
    },
    "SKL-MEC-002": {
        "occupation_id": "TRD-04",
        "required_any": ["tappet", "valve clearance", "feeler gauge", "tappet setting", "tappet calibration"],
        "forbidden_if_only": ["oil", "brake"]
    },
    "SKL-MEC-003": {
        "occupation_id": "TRD-04",
        "required_any": ["brake bleeding", "disc brake", "brake caliper", "brake fluid", "disc brake oil", "hydraulic air bleeding", "brake service"],
        "forbidden_if_only": ["engine oil", "tappet"]
    },

    # TRD-05 Carpenter
    "SKL-CRP-001": {
        "occupation_id": "TRD-05",
        "required_any": ["circular saw", "plywood", "ply kaatna", "panel sizing", "ply cutting", "sheet sizing"],
        "forbidden_if_only": ["sunmica", "laminate", "randa", "planer", "unloading", "truck", "hand saw"]
    },
    "SKL-CRP-002": {
        "occupation_id": "TRD-05",
        "required_any": ["sunmica", "laminate", "fevicol", "adhesive application", "sheet pressing", "lamination"],
        "forbidden_if_only": ["randa", "circular saw", "cutter blade", "trimming"]
    },
    "SKL-CRP-003": {
        "occupation_id": "TRD-05",
        "required_any": ["randa", "planer", "planing", "wood smoothing", "wood surface planing", "wood leveling"],
        "forbidden_if_only": ["circular saw", "sunmica", "varnish", "sharpening", "whetstone"]
    },

    # TRD-06 Welder
    "SKL-WLD-001": {
        "occupation_id": "TRD-06",
        "required_any": ["arc welding", "6013", "electrode", "stick welding", "manual metal arc", "mmaw"],
        "forbidden_if_only": ["slag", "chipping", "bevel", "grinder"]
    },
    "SKL-WLD-002": {
        "occupation_id": "TRD-06",
        "required_any": ["slag", "chipping hammer", "weld cleaning", "slag removal", "slag jhaadna"],
        "forbidden_if_only": []
    },
    "SKL-WLD-003": {
        "occupation_id": "TRD-06",
        "required_any": ["bevel", "v-groove", "edge grinding", "beveling", "grinder se bevel"],
        "forbidden_if_only": ["welding rod", "electrode"]
    },

    # TRD-07 Mason
    "SKL-MSN-001": {
        "occupation_id": "TRD-07",
        "required_any": ["sahul", "plumb bob", "vertical alignment", "vertical leveling"],
        "forbidden_if_only": ["chunai", "ghoontai"]
    },
    "SKL-MSN-002": {
        "occupation_id": "TRD-07",
        "required_any": ["chunai", "bricklaying", "brick masonry", "mortar bed", "1:4 masala"],
        "forbidden_if_only": ["sahul", "ghoontai"]
    },
    "SKL-MSN-003": {
        "occupation_id": "TRD-07",
        "required_any": ["ghoontai", "neat cement", "cement punning", "cement slurry float", "cement ghol"],
        "forbidden_if_only": ["chunai", "sahul"]
    },

    # TRD-08 Painter
    "SKL-PNT-001": {
        "occupation_id": "TRD-08",
        "required_any": ["putty", "patti", "wall skimming", "putty application", "putty lagana"],
        "forbidden_if_only": ["regmar", "sandpaper", "primer"]
    },
    "SKL-PNT-002": {
        "occupation_id": "TRD-08",
        "required_any": ["regmar", "sandpaper", "sanding", "primer", "primer sealing", "abrasive sanding", "ghisai"],
        "forbidden_if_only": ["putty blade", "putty patti"]
    },

    # TRD-09 Agriculture
    "SKL-AGR-001": {
        "occupation_id": "TRD-09",
        "required_any": ["drip", "lateral", "dripper", "drip line", "drip irrigation", "micro irrigation"],
        "forbidden_if_only": ["venturi", "fertigation"]
    },
    "SKL-AGR-002": {
        "occupation_id": "TRD-09",
        "required_any": ["venturi", "fertigation", "fertilizer dosing", "khad chalana", "venturi dosing"],
        "forbidden_if_only": ["drip lateral"]
    },

    # TRD-10 Mobile Repair
    "SKL-MOB-001": {
        "occupation_id": "TRD-10",
        "required_any": ["smd", "cc pin", "charging jack", "usb port", "desoldering", "charging port"],
        "forbidden_if_only": ["jumper", "track repair"]
    },
    "SKL-MOB-002": {
        "occupation_id": "TRD-10",
        "required_any": ["jumper", "track repair", "pcb track", "micro wire", "copper trace"],
        "forbidden_if_only": ["charging jack", "cc pin"]
    }
}

class CanonicalSkillRetriever:
    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or default_config
        self.threshold = self.config.canonical_match_threshold
        self.skills_catalogue = load_canonical_skill_catalogue()
        
        # Build index
        self.skill_index = []
        self.corpus = []
        
        for sk in self.skills_catalogue:
            # Build search document containing canonical name, aliases, hindi/hinglish vernacular terms, description
            sk_id = sk.get("canonical_skill_id")
            sk_name = sk.get("canonical_skill_name")
            aliases = sk.get("alternative_names", []) or []
            hi_names = sk.get("hindi_names", []) or []
            hng_names = sk.get("hinglish_names", []) or []
            en_names = sk.get("english_names", []) or []
            tools = sk.get("required_tools", []) or []
            desc = sk.get("skill_description", "")
            
            combined_search_text = " ".join([
                sk_name,
                " ".join(aliases),
                " ".join(hi_names),
                " ".join(hng_names),
                " ".join(en_names),
                " ".join(tools),
                desc
            ])
            
            clean_search_text = self.normalize_for_retrieval(combined_search_text)
            self.corpus.append(clean_search_text)
            self.skill_index.append(sk)
            
        # Character-level n-gram TF-IDF vectorizer captures subword roots across Hindi/Hinglish/English
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1,
            sublinear_tf=True
        )
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        else:
            self.tfidf_matrix = None

    @staticmethod
    def normalize_for_retrieval(text: str) -> str:
        """
        Normalizes a separate text copy for search indexing.
        Does NOT alter the original surface text.
        """
        # Lowercase, strip punctuation and extra spaces
        t = text.lower()
        t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    @staticmethod
    def validate_semantic_compatibility(
        query: str,
        canonical_id: str,
        occupation_id: Optional[str] = None
    ) -> bool:
        """
        Validates semantic, action, tool, material, and occupation compatibility.
        Guarantees that a high surface/lexical overlap score cannot override an action
        contradiction or missing core object.
        """
        sig = SKILL_SIGNATURES.get(canonical_id)
        if not sig:
            return True
            
        # 1. Occupation compatibility check
        expected_occ = sig.get("occupation_id")
        if occupation_id and expected_occ and occupation_id != expected_occ:
            return False
            
        q_lower = query.lower()
        
        # 2. Must contain at least one required signature concept / action / tool
        has_req = any(req in q_lower for req in sig["required_any"])
        if not has_req:
            return False
            
        # 3. Check forbidden-if-only contradictions
        for forb in sig.get("forbidden_if_only", []):
            if forb in q_lower:
                return False
                
        return True

    def match_phrase(
        self,
        extracted_phrase: str,
        top_k: int = 3,
        occupation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Matches an extracted skill phrase against the canonical catalogue.
        Combines character n-gram cosine retrieval with direct alias overlap, occupation domain weighting,
        and strict semantic action/object compatibility validation.
        Returns top candidates, best match, confidence score, and review flag.
        """
        clean_query = self.normalize_for_retrieval(extracted_phrase)
        
        if not clean_query or self.tfidf_matrix is None or len(self.skill_index) == 0:
            return {
                "original_phrase": extracted_phrase,
                "mapping_status": "unmapped",
                "is_unmapped_skill": True,
                "confidence_score": 0.0,
                "canonical_skill": None,
                "canonical_skill_id": None,
                "esco_uri": None,
                "onet_soc_code": None,
                "nsqf_reference": None,
                "human_review_required": True,
                "candidates": []
            }
            
        q_vec = self.vectorizer.transform([clean_query])
        sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        
        q_words = set(clean_query.split())
        
        candidates = []
        for idx, sk in enumerate(self.skill_index):
            tfidf_score = float(sims[idx])
            
            sig = SKILL_SIGNATURES.get(sk.get("canonical_skill_id"), {})
            # Direct title and alias overlap evaluation
            targets = (
                [sk.get("canonical_skill_name", "")] +
                (sk.get("alternative_names") or []) +
                (sk.get("hinglish_names") or []) +
                (sk.get("english_names") or []) +
                sig.get("required_any", [])
            )
            
            alias_score = 0.0
            for tgt in targets:
                ctgt = self.normalize_for_retrieval(tgt)
                t_words = set(ctgt.split())
                if not t_words:
                    continue
                
                matched_q = set()
                for qw in q_words:
                    for tw in t_words:
                        if (
                            qw == tw
                            or qw.rstrip("s") == tw.rstrip("s")
                            or (len(qw) >= 4 and len(tw) >= 4 and (qw.startswith(tw) or tw.startswith(qw) or qw[:4] == tw[:4]))
                        ):
                            matched_q.add(qw)
                            break
                
                if matched_q:
                    domain_matches = {w for w in matched_q if w not in GENERIC_ACTION_WORDS}
                    if domain_matches:
                        prec = len(matched_q) / len(q_words)
                        sim = 0.60 + 0.35 * prec
                    else:
                        sim = 0.35
                    if sim > alias_score:
                        alias_score = sim
            
            # Occupation domain coherence weighting
            sk_occ = sk.get("occupation_id")
            if occupation_id and sk_occ == occupation_id and alias_score >= 0.5:
                alias_score = min(1.0, alias_score + 0.05)
                
            combined_score = max(tfidf_score, alias_score)
            
            # Semantic compatibility evaluation
            is_compatible = self.validate_semantic_compatibility(
                extracted_phrase,
                sk.get("canonical_skill_id"),
                occupation_id
            )
            
            effective_score = combined_score if is_compatible else min(combined_score, 0.35)
            
            candidates.append({
                "skill_id": sk.get("canonical_skill_id"),
                "skill_name": sk.get("canonical_skill_name"),
                "occupation_id": sk.get("occupation_id"),
                "similarity_score": round(effective_score, 4),
                "raw_similarity_score": round(combined_score, 4),
                "is_semantically_compatible": is_compatible,
                "esco_uri": sk.get("esco_uri"),
                "onet_soc_code": sk.get("onet_code"),
                "nsqf_reference": sk.get("nsqf_reference"),
                "is_indigenous": sk.get("is_indigenous_skill", False)
            })
            
        candidates.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_candidates = candidates[:top_k]
        
        # Selection Gate: Best match must meet threshold AND be semantically compatible
        compatible_matches = [
            c for c in top_candidates
            if c.get("is_semantically_compatible") and c["similarity_score"] >= self.threshold
        ]
        
        if compatible_matches:
            best = compatible_matches[0]
            return {
                "original_phrase": extracted_phrase,
                "mapping_status": "mapped",
                "is_unmapped_skill": False,
                "confidence_score": best["similarity_score"],
                "canonical_skill": best["skill_name"],
                "canonical_skill_id": best["skill_id"],
                "esco_uri": best["esco_uri"],
                "onet_soc_code": best["onet_soc_code"],
                "nsqf_reference": best["nsqf_reference"],
                "human_review_required": False,
                "candidates": top_candidates
            }
        else:
            top_score = top_candidates[0]["similarity_score"] if top_candidates else 0.0
            return {
                "original_phrase": extracted_phrase,
                "mapping_status": "unmapped",
                "is_unmapped_skill": True,
                "confidence_score": top_score,
                "canonical_skill": None,
                "canonical_skill_id": None,
                "esco_uri": None,
                "onet_soc_code": None,
                "nsqf_reference": None,
                "human_review_required": True,
                "candidates": top_candidates
            }

