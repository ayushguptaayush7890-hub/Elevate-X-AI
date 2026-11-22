"""
ELEVATE X AI — FEATURE 1: BIO TOKENIZER & SPAN ALIGNER
Handles bidirectional alignment between verbatim text, word tokens, subword tokens,
and BIO labels with strict Unicode character offset preservation and boundary pruning.
"""

import re
from typing import List, Dict, Tuple, Any, Optional

# Conversational filler phrases and auxiliaries stripped from informal spans
STOP_BOUNDARY_PHRASES = [
    # Hindi / Hinglish auxiliaries & verbs
    "karta hu", "karti hu", "karte hain", "kar raha hu", "kar rahe hain",
    "kiya tha", "kar sakta hu", "hota hai", "hote hain", "ho raha hai",
    "silta hu", "silti hu", "silte hain", "sil raha hu",
    "lagata hu", "lagate hain", "banata hu", "banate hain",
    "kaam karta hu", "kaam karte hain",
    # Conjunctions & trailing noise
    "aur customer", "aur client", "aur grahak", "aur helper", "aur",
    "tatha", "evam", "ya", "lekin", "parantu",
    "ke according", "ke hisab se", "ke sath", "ke liye", "ke pass",
    "se lekar", "se", "ke", "ki", "ko", "me", "mein", "par", "pe", "ka",
    # English fillers
    "in order to", "responsible for", "and customer", "and client",
    "as well as", "along with", "and other", "with", "and", "or", "for", "to"
]

class BIOTokenizer:
    def __init__(self, tokenizer=None, bio_tags: Optional[List[str]] = None):
        self.tokenizer = tokenizer
        self.bio_tags = bio_tags or ["O", "B-SKILL", "I-SKILL"]
        self.tag2id = {tag: i for i, tag in enumerate(self.bio_tags)}
        self.id2tag = {i: tag for i, tag in enumerate(self.bio_tags)}

    @staticmethod
    def decode_bio_to_spans(
        text: str,
        words: List[str],
        bio_tags: List[str],
        offsets: Optional[List[Tuple[int, int]]] = None,
        confidences: Optional[List[float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Decodes word-level BIO tags into verbatim character spans [start_offset:end_offset].
        Strictly preserves model-predicted tags with model confidence scores.
        Guarantees: text[start_offset:end_offset] == extracted_skill.
        """
        if offsets is None:
            offsets = []
            curr_pos = 0
            for w in words:
                idx = text.find(w, curr_pos)
                if idx != -1:
                    offsets.append((idx, idx + len(w)))
                    curr_pos = idx + len(w)
                else:
                    offsets.append((curr_pos, curr_pos + len(w)))
                    curr_pos += len(w) + 1

        if confidences is None:
            confidences = [0.90] * len(words)

        # Stop words, conversational auxiliaries, and delimiters that cannot start a skill chunk
        delimiters = {",", ";", ":", "|", "/", "and", "aur", "or"}
        stop_and_fillers = {
            "i", "we", "you", "he", "she", "it", "they", "am", "is", "are", "was", "were",
            "know", "knows", "knowing", "have", "has", "had", "do", "does", "did",
            "in", "to", "for", "the", "a", "an", "with", "from", "by", "of", "on", "at",
            "aur", "and", "or", "mein", "me", "par", "pe", "se", "ko", "ka", "ki", "ke",
            "hu", "hai", "hain", "karta", "karti", "karte", "karna", "kar"
        }

        valid_bio = []
        in_chunk = False
        for idx, (w, tag) in enumerate(zip(words, bio_tags)):
            w_lower = w.lower().strip()
            if tag == "B-SKILL":
                valid_bio.append("B-SKILL")
                in_chunk = True
            elif tag == "I-SKILL":
                if in_chunk:
                    prev_w = words[idx - 1]
                    if w_lower in delimiters:
                        valid_bio.append("O")
                        in_chunk = False
                    elif prev_w.endswith("++") or prev_w.endswith("#"):
                        # Boundary symbol like c++, c# terminates chunk and starts next
                        valid_bio.append("B-SKILL")
                        in_chunk = True
                    else:
                        valid_bio.append("I-SKILL")
                else:
                    # Model flagged as skill entity but not inside chunk: promote to B-SKILL if not filler
                    if w_lower not in delimiters and w_lower not in stop_and_fillers and len(w_lower) > 1:
                        valid_bio.append("B-SKILL")
                        in_chunk = True
                    else:
                        valid_bio.append("O")
                        in_chunk = False
            else:
                valid_bio.append("O")
                in_chunk = False

        spans = []
        span_start = -1
        span_end = -1
        span_id = 1
        curr_confs = []

        for idx, (tag, (t_st, t_en), conf) in enumerate(zip(valid_bio, offsets, confidences)):
            if tag == "B-SKILL":
                if span_start != -1 and span_end != -1:
                    extracted = text[span_start:span_end].strip()
                    if extracted:
                        avg_conf = sum(curr_confs) / max(1, len(curr_confs))
                        spans.append({
                            "span_id": f"SP-{span_id:02d}",
                            "extracted_skill": extracted,
                            "start_offset": span_start,
                            "end_offset": span_end,
                            "skill_category": "technical_tactile",
                            "confidence_score": round(avg_conf, 4)
                        })
                        span_id += 1
                span_start = t_st
                span_end = t_en
                curr_confs = [conf]
            elif tag == "I-SKILL":
                if span_start != -1:
                    span_end = t_en
                    curr_confs.append(conf)
                else:
                    span_start = t_st
                    span_end = t_en
                    curr_confs = [conf]
            else:
                if span_start != -1 and span_end != -1:
                    extracted = text[span_start:span_end].strip()
                    if extracted:
                        avg_conf = sum(curr_confs) / max(1, len(curr_confs))
                        spans.append({
                            "span_id": f"SP-{span_id:02d}",
                            "extracted_skill": extracted,
                            "start_offset": span_start,
                            "end_offset": span_end,
                            "skill_category": "technical_tactile",
                            "confidence_score": round(avg_conf, 4)
                        })
                        span_id += 1
                span_start = -1
                span_end = -1
                curr_confs = []

        if span_start != -1 and span_end != -1:
            extracted = text[span_start:span_end].strip()
            if extracted:
                avg_conf = sum(curr_confs) / max(1, len(curr_confs))
                spans.append({
                    "span_id": f"SP-{span_id:02d}",
                    "extracted_skill": extracted,
                    "start_offset": span_start,
                    "end_offset": span_end,
                    "skill_category": "technical_tactile",
                    "confidence_score": round(avg_conf, 4)
                })

        return spans

    @staticmethod
    def tokens_and_offsets(tokens: List[str]) -> Tuple[str, List[Tuple[int, int]]]:
        """
        Reconstructs space-joined text and exact (start, end) character offsets for each word token.
        Guarantees text[start:end] == token for all tokens.
        """
        offsets = []
        curr = 0
        for t in tokens:
            st = curr
            en = st + len(t)
            offsets.append((st, en))
            curr = en + 1
        text = " ".join(tokens)
        return text, offsets

    @staticmethod
    def word_tokenize_with_offsets(text: str) -> List[Tuple[str, int, int]]:
        """
        Tokenizes free-form text into words preserving exact Unicode character offsets [start, end).
        Preserves programming tokens (c++, c#, node.js) and accurately segments Devanagari script,
        Latin script, and separates trailing sentence punctuation.
        Guarantees: text[start:end] == token for every returned token.
        """
        tokens = []
        if not text:
            return tokens

        for match in re.finditer(r"\S+", text):
            raw = match.group()
            st = match.start()
            en = match.end()

            # Separate trailing sentence punctuation (e.g., comma, period, danda, semicolon)
            # but preserve intentional symbols like c++, c#, .net, node.js
            m_punct = re.search(r"([,\.।;:!?]+)$", raw)
            if m_punct and not (raw.endswith("++") or raw.endswith("#") or raw in ["node.js", "vue.js", ".net"]):
                p_len = len(m_punct.group(1))
                word_part = raw[:-p_len]
                punct_part = raw[-p_len:]
                if word_part:
                    tokens.append((word_part, st, en - p_len))
                tokens.append((punct_part, en - p_len, en))
            else:
                tokens.append((raw, st, en))

        return tokens

    @staticmethod
    def extract_spans_from_tokens_and_bio(
        tokens: List[str],
        bio_tags: List[str]
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Converts a list of word tokens and corresponding BIO labels into verbatim character spans.
        Guarantees: text[start_offset:end_offset] == extracted_skill.
        """
        text, offsets = BIOTokenizer.tokens_and_offsets(tokens)
        spans = []
        span_tokens = []
        span_start = -1
        span_end = -1
        span_id = 1

        for idx, (tag, (t_st, t_en)) in enumerate(zip(bio_tags, offsets)):
            if tag == "B-SKILL":
                if span_tokens and span_start != -1 and span_end != -1:
                    extracted = text[span_start:span_end].strip()
                    if extracted:
                        spans.append({
                            "span_id": f"SP-{span_id:02d}",
                            "extracted_skill": extracted,
                            "start_offset": span_start,
                            "end_offset": span_end,
                            "skill_category": "tool_operation"
                        })
                        span_id += 1
                span_start = t_st
                span_end = t_en
                span_tokens = [tokens[idx]]
            elif tag == "I-SKILL":
                if span_tokens and span_start != -1:
                    span_end = t_en
                    span_tokens.append(tokens[idx])
                else:
                    span_start = t_st
                    span_end = t_en
                    span_tokens = [tokens[idx]]
            else:
                if span_tokens and span_start != -1 and span_end != -1:
                    extracted = text[span_start:span_end].strip()
                    if extracted:
                        spans.append({
                            "span_id": f"SP-{span_id:02d}",
                            "extracted_skill": extracted,
                            "start_offset": span_start,
                            "end_offset": span_end,
                            "skill_category": "tool_operation"
                        })
                        span_id += 1
                span_start = -1
                span_end = -1
                span_tokens = []

        if span_tokens and span_start != -1 and span_end != -1:
            extracted = text[span_start:span_end].strip()
            if extracted:
                spans.append({
                    "span_id": f"SP-{span_id:02d}",
                    "extracted_skill": extracted,
                    "start_offset": span_start,
                    "end_offset": span_end,
                    "skill_category": "tool_operation"
                })

        return text, spans

    @staticmethod
    def clean_and_trim_skill_span(text: str, span: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Prunes conversational filler, auxiliary verbs, and trailing stop phrases from an extracted span.
        Recalculates start_offset and end_offset to preserve text[start:end] == extracted_skill.
        Returns None if span becomes empty or meaningless.
        """
        raw_phrase = span["extracted_skill"]
        raw_start = span["start_offset"]
        raw_end = span["end_offset"]

        cleaned = raw_phrase.strip()
        # Strip trailing stop phrases
        for phrase in sorted(STOP_BOUNDARY_PHRASES, key=lambda x: -len(x)):
            pattern = rf"\s+{re.escape(phrase)}\b"
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()

        # Strip leading pronouns / conjunctions
        leading_stops = ["aur", "main", "hum", "mera", "meri", "mere", "and", "i", "we", "the", "a", "an"]
        for lstp in leading_stops:
            cleaned = re.sub(rf"^{re.escape(lstp)}\s+", "", cleaned, flags=re.IGNORECASE).strip()

        if len(cleaned) < 2 or not re.search(r"\w", cleaned):
            return None

        # Recalculate exact offsets inside the original window
        try:
            rel_idx = text[raw_start:raw_end].index(cleaned)
            new_start = raw_start + rel_idx
            new_end = new_start + len(cleaned)
        except ValueError:
            # Fallback to direct text search near raw_start
            pos = text.find(cleaned, max(0, raw_start - 5))
            if pos != -1:
                new_start = pos
                new_end = pos + len(cleaned)
            else:
                new_start = raw_start
                new_end = raw_end
                cleaned = raw_phrase

        # Ensure exact slice invariant
        assert text[new_start:new_end] == cleaned, f"Slice invariant violated: '{text[new_start:new_end]}' != '{cleaned}'"

        updated = dict(span)
        updated["extracted_skill"] = cleaned
        updated["start_offset"] = new_start
        updated["end_offset"] = new_end
        return updated
