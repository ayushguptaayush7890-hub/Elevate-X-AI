"""
ELEVATE X AI — FEATURE 1: MODULAR SKILL EXTRACTOR
End-to-end multi-task inference pipeline:
A. Multilingual text encoder & token-level BIO sequence tagging
B. Verbatim character span offset reconstruction (text[start:end] == extracted_skill)
C. Skill category classification (8 functional classes)
D. Occupation domain categorization (10 target trades)
E. Canonical skill matching & similarity retrieval (32 competencies)
F. Confidence calibration & human-review gating
"""

import re
import torch
from typing import Dict, List, Any, Optional

try:
    from .model_config import ModelConfig, default_config, ID2TAG, TAG2ID, SKILL_CATEGORIES
    from .bio_tokenizer import BIOTokenizer
    from .skill_classifier import SkillCategoryClassifier, CATEGORY_KEYWORDS
    from .occupation_classifier import OccupationClassifier, TRADE_VOCABULARY
    from .canonical_skill_retriever import CanonicalSkillRetriever
    from .model_registry import ModelRegistry
    from .semantic_normalizer import SemanticSkillNormalizer
except (ImportError, ValueError):
    from model_config import ModelConfig, default_config, ID2TAG, TAG2ID, SKILL_CATEGORIES
    from bio_tokenizer import BIOTokenizer
    from skill_classifier import SkillCategoryClassifier, CATEGORY_KEYWORDS
    from occupation_classifier import OccupationClassifier, TRADE_VOCABULARY
    from canonical_skill_retriever import CanonicalSkillRetriever
    from model_registry import ModelRegistry
    from semantic_normalizer import SemanticSkillNormalizer

class ModularSkillExtractor:
    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or default_config
        self.device = ModelRegistry.get_device(prefer_mps=self.config.use_mps)
        
        # Core modules
        self.bio_tokenizer = BIOTokenizer()
        self.skill_classifier = SkillCategoryClassifier()
        self.occupation_classifier = OccupationClassifier()
        self.canonical_retriever = CanonicalSkillRetriever(self.config)
        
        self.model = None
        self.hf_tokenizer = None

    def _ensure_neural_model_loaded(self):
        if self.model is None:
            try:
                self.hf_tokenizer = ModelRegistry.load_tokenizer(self.config.model_key)
                self.model = ModelRegistry.load_token_classification_model(
                    model_key=self.config.model_key,
                    num_labels=self.config.num_bio_labels
                )
                self.model.eval()
            except Exception as e:
                # If network is unavailable or loading fails, fallback cleanly to rule-augmented extractor
                self.model = None

    def extract_skills_neural(self, text: str) -> List[Dict[str, Any]]:
        """
        Token-level BIO neural inference using fine-tuned multilingual transformer.
        Uses exact is_split_into_words subword-to-word alignment with word_ids.
        """
        self._ensure_neural_model_loaded()
        if self.model is None or self.hf_tokenizer is None:
            return []

        word_data = self.bio_tokenizer.word_tokenize_with_offsets(text)
        if not word_data:
            return []

        words = [w[0] for w in word_data]
        offsets = [(w[1], w[2]) for w in word_data]

        try:
            encoding = self.hf_tokenizer(
                words,
                is_split_into_words=True,
                truncation=True,
                max_length=256,
                return_tensors="pt"
            ).to(self.device)

            word_ids = encoding.word_ids(batch_index=0)

            with torch.no_grad():
                outputs = self.model(**encoding)
                logits = outputs.logits[0]
                preds = torch.argmax(logits, dim=-1).cpu().tolist()

            word_preds_dict = {}
            prev_wid = None
            for wid, pid in zip(word_ids, preds):
                if wid is not None and wid != prev_wid:
                    word_preds_dict[wid] = ID2TAG.get(pid, "O")
                    prev_wid = wid

            predicted_bio = []
            for w_idx in range(len(words)):
                predicted_bio.append(word_preds_dict.get(w_idx, "O"))

            return self.bio_tokenizer.decode_bio_to_spans(text, words, predicted_bio, offsets)
        except Exception:
            return []

    def extract_skills_heuristic(self, text: str) -> List[Dict[str, Any]]:
        """
        High-precision rule & domain vocabulary extractor.
        Guarantees exact character slices and prunes conversational filler words.
        """
        spans = []
        clean_text = text
        word_data = self.bio_tokenizer.word_tokenize_with_offsets(clean_text)
        
        # Compile all skill trigger terms
        all_triggers = set()
        for kws in CATEGORY_KEYWORDS.values():
            all_triggers.update(kws)
        for kws in TRADE_VOCABULARY.values():
            all_triggers.update(kws)

        # Load Devanagari & Hinglish terms from Language Registry
        from pathlib import Path
        import json
        vocab_dir = Path(__file__).resolve().parents[1] / "processed" / "indian_worker_data" / "language_vocabulary"
        t_file = vocab_dir / "trade_terms_hindi_hinglish.json"
        if t_file.exists():
            try:
                with open(t_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        if item.get("devanagari"):
                            all_triggers.add(item["devanagari"])
                        if item.get("roman_hinglish"):
                            all_triggers.add(item["roman_hinglish"])
            except Exception:
                pass
        v_file = vocab_dir / "action_verbs_vocabulary.json"
        if v_file.exists():
            try:
                with open(v_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        if item.get("devanagari"):
                            all_triggers.add(item["devanagari"])
                        if item.get("roman_hinglish"):
                            all_triggers.add(item["roman_hinglish"])
            except Exception:
                pass
            
        phrases_seen = set()
        
        # Exact non-greedy match on verified trade terms sorted longest first
        for kw in sorted(all_triggers, key=lambda x: -len(x)):
            if len(kw) < 3:
                continue
            for m in re.finditer(rf"\b({re.escape(kw)})\b", clean_text, re.IGNORECASE):
                sub_text = m.group(1).strip()
                st = m.start(1)
                en = st + len(sub_text)
                
                raw_span = {
                    "span_id": f"SP-{len(spans) + 1:02d}",
                    "extracted_skill": clean_text[st:en],
                    "start_offset": st,
                    "end_offset": en,
                    "confidence_score": 0.88
                }
                
                # Prune conversational filler or auxiliary boundary words
                pruned = BIOTokenizer.clean_and_trim_skill_span(clean_text, raw_span)
                if not pruned:
                    continue

                pst = pruned["start_offset"]
                pen = pruned["end_offset"]
                pskill = pruned["extracted_skill"].lower()

                # Check for overlap
                overlap = any(s["start_offset"] <= pst < s["end_offset"] or s["start_offset"] < pen <= s["end_offset"] for s in spans)
                if not overlap and pskill not in phrases_seen:
                    phrases_seen.add(pskill)
                    spans.append(pruned)
                    
        # Sort spans by start_offset
        spans.sort(key=lambda x: x["start_offset"])
        return spans

    def predict(self, text: str, occupation_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes end-to-end skill extraction on verbatim text.
        """
        if not text or not text.strip():
            return {
                "input_text": text,
                "detected_occupation": {"occupation_id": "TRD-01", "occupation_title": "Tailor and Garment Worker", "confidence": 0.0},
                "extracted_skills_count": 0,
                "extracted_skills": []
            }

        # 1. Occupation Classification
        occ_result = self.occupation_classifier.classify(text)
        if occupation_hint:
            occ_result["occupation_id"] = occupation_hint
            
        # 2. Extract Candidate Skill Spans (Heuristic + Fine-tuned Neural)
        heuristic_spans = self.extract_skills_heuristic(text)
        neural_spans = []
        try:
            raw_neural = self.extract_skills_neural(text)
            for n_sp in raw_neural:
                p = BIOTokenizer.clean_and_trim_skill_span(text, n_sp)
                if p:
                    neural_spans.append(p)
        except Exception:
            neural_spans = []

        candidate_spans = list(heuristic_spans)
        for n_sp in neural_spans:
            st = n_sp["start_offset"]
            en = n_sp["end_offset"]
            overlap = any(h["start_offset"] <= st < h["end_offset"] or h["start_offset"] < en <= h["end_offset"] for h in candidate_spans)
            if not overlap:
                candidate_spans.append(n_sp)

        candidate_spans.sort(key=lambda x: x["start_offset"])
        
        # 3. Consolidate Spans, Group Compounds, & Filter Generic Isolated Words
        consolidated_spans = SemanticSkillNormalizer.consolidate_and_normalize(
            text=text,
            raw_spans=candidate_spans,
            occupation_id=occ_result.get("occupation_id")
        )
        
        # 4. Enrich Spans with Category, Normalized Title, and Canonical Mapping
        enriched_spans = []
        for idx, sp in enumerate(consolidated_spans):
            phrase = sp["extracted_skill"]
            norm_name = sp.get("normalized_skill", phrase)
            evidence_str = sp.get("evidence_text", phrase)
            st = sp["start_offset"]
            en = sp["end_offset"]
            
            # Guarantee character offset invariant (Verbatim source substring)
            assert text[st:en] == phrase, f"Character slice mismatch: '{text[st:en]}' != '{phrase}'"
            assert evidence_str == phrase, f"Evidence text mismatch: '{evidence_str}' != '{phrase}'"
            
            # A. Category Classification
            cat_res = self.skill_classifier.classify_phrase(norm_name or phrase)
            
            # B. Canonical Skill Retrieval & Ontological Mapping
            # Match both raw phrase and normalized competency title against canonical catalogue
            canon_raw = self.canonical_retriever.match_phrase(
                phrase,
                occupation_id=occ_result.get("occupation_id")
            )
            canon_norm = self.canonical_retriever.match_phrase(
                norm_name,
                occupation_id=occ_result.get("occupation_id")
            )
            canon_res = canon_norm if canon_norm["confidence_score"] >= canon_raw["confidence_score"] else canon_raw
            
            enriched_spans.append({
                "span_id": f"SP-{idx + 1:02d}",
                "extracted_skill": phrase,
                "normalized_skill": norm_name,
                "evidence_text": evidence_str,
                "start_offset": st,
                "end_offset": en,
                "skill_category": cat_res["category"],
                "category_confidence": cat_res["confidence"],
                "canonical_skill": canon_res["canonical_skill"],
                "canonical_skill_id": canon_res["canonical_skill_id"],
                "mapping_status": canon_res["mapping_status"],
                "is_unmapped_skill": canon_res["is_unmapped_skill"],
                "mapping_confidence": canon_res["confidence_score"],
                "human_review_required": canon_res["human_review_required"],
                "crosswalks": {
                    "esco_uri": canon_res["esco_uri"],
                    "onet_soc_code": canon_res["onet_soc_code"],
                    "nsqf_reference": canon_res["nsqf_reference"]
                },
                "candidates": canon_res["candidates"]
            })
            
        return {
            "input_text": text,
            "detected_occupation": occ_result,
            "extracted_skills_count": len(enriched_spans),
            "extracted_skills": enriched_spans
        }
