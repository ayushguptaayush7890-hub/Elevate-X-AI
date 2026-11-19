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
        offsets: Optional[List[Tuple[int, int]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Decodes word-level BIO tags into verbatim character spans [start_offset:end_offset].
        Guarantees: text[start_offset:end_offset] == extracted_skill.
        """
        if offsets is None:
            # If offsets not provided, locate each word in text sequentially
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

        spans = []
        span_start = -1
        span_end = -1
        span_id = 1

        for idx, (tag, (t_st, t_en)) in enumerate(zip(bio_tags, offsets)):
            if tag == "B-SKILL":
                if span_start != -1 and span_end != -1:
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
            elif tag == "I-SKILL":
                if span_start != -1:
                    span_end = t_en
                else:
                    span_start = t_st
                    span_end = t_en
            else:
                if span_start != -1 and span_end != -1:
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

        if span_start != -1 and span_end != -1:
            extracted = text[span_start:span_end].strip()
            if extracted:
                spans.append({
                    "span_id": f"SP-{span_id:02d}",
                    "extracted_skill": extracted,
                    "start_offset": span_start,
                    "end_offset": span_end,
                    "skill_category": "tool_operation"
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
        Handles Devanagari script, Latin script, punctuation, and numerals.
        """
        tokens = []
        for match in re.finditer(r"[\w]+|[^\w\s]", text, re.UNICODE):
            tokens.append((match.group(), match.start(), match.end()))
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
