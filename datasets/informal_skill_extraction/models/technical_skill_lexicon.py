"""Curated technical competency names and aliases used alongside neural spans.

These entries are a transparent coverage layer for technical terms that are
outside the vocationally weighted training corpus. They do not imply an
official ESCO, O*NET, or NSQF mapping; unsupported mappings remain for review.
"""

import re
from typing import Any, Dict, List


TECHNICAL_COMPETENCIES = [
    {
        "id": "TECH-PROG-CPP", "name": "C++ Programming",
        "aliases": [r"C\+\+", r"सी\s*\+\+", r"C\s+plus\s+plus", r"CPP", "सी प्लस प्लस"],
    },
    {"id": "TECH-PROG-PYTHON", "name": "Python Programming", "aliases": ["Python", "पायथन", "पाइथन"]},
    {"id": "TECH-PROG-JAVA", "name": "Java Programming", "aliases": ["Java", "जावा"]},
    {"id": "TECH-PROG-JS", "name": "JavaScript Programming", "aliases": ["JavaScript", "JS", "जावास्क्रिप्ट"]},
    {"id": "TECH-PROG-SQL", "name": "SQL", "aliases": ["SQL", "एसक्यूएल"]},
    {"id": "TECH-WEB-HTML", "name": "HTML", "aliases": ["HTML"]},
    {"id": "TECH-WEB-CSS", "name": "CSS", "aliases": ["CSS"]},
    {"id": "TECH-WEB-REACT", "name": "React", "aliases": ["React"]},
    {"id": "TECH-WEB-NODE", "name": "Node.js", "aliases": ["Node.js", "Node JS"]},
    {
        "id": "TECH-AI-ML", "name": "Artificial Intelligence and Machine Learning",
        "aliases": [
            "artificial intelligence and machine learning",
            "artificial intelligence & machine learning",
            "artificial intelligence / machine learning",
            "AI/ML", "AI ML", "AI and ML", "AI & ML",
            "AI and machine learning", "AI & machine learning",
            "कृत्रिम बुद्धिमत्ता और मशीन लर्निंग",
        ],
    },
    {"id": "TECH-AI", "name": "Artificial Intelligence", "aliases": ["artificial intelligence", "AI", "कृत्रिम बुद्धिमत्ता"]},
    {"id": "TECH-ML", "name": "Machine Learning", "aliases": ["machine learning", "ML", "मशीन लर्निंग"]},
    {"id": "TECH-DL", "name": "Deep Learning", "aliases": ["deep learning", "डीप लर्निंग"]},
    {"id": "TECH-DATA", "name": "Data Analysis", "aliases": ["data analysis", "data analytics"]},
    {"id": "TECH-CLOUD", "name": "Cloud Computing", "aliases": ["cloud computing", "cloud", "क्लाउड कंप्यूटिंग"]},
    {"id": "TECH-NLP", "name": "Natural Language Processing", "aliases": ["natural language processing", "NLP", "एनएलपी"]},
]


def _compile_alias(alias: str) -> re.Pattern[str]:
    # Entries may use regex syntax for spellings such as C++ and AI/ML.
    is_regex = "\\" in alias
    body = alias if is_regex else re.escape(alias)
    starts_word = bool(re.match(r"[A-Za-z0-9]", alias))
    ends_word = bool(re.search(r"[A-Za-z0-9]$", alias))
    return re.compile(
        (r"(?<![\w])" if starts_word else "") + body +
        (r"(?![\w])" if ends_word else ""),
        re.IGNORECASE,
    )


_MATCHERS = sorted(
    ((spec, _compile_alias(alias)) for spec in TECHNICAL_COMPETENCIES for alias in spec["aliases"]),
    key=lambda entry: len(entry[1].pattern),
    reverse=True,
)


def extract_technical_spans(text: str) -> List[Dict[str, Any]]:
    """Find supported competency mentions with exact source offsets."""
    spans: List[Dict[str, Any]] = []
    for spec, matcher in _MATCHERS:
        for match in matcher.finditer(text):
            start, end = match.span()
            if any(max(start, s["start_offset"]) < min(end, s["end_offset"]) for s in spans):
                continue
            spans.append({
                "extracted_skill": text[start:end],
                "normalized_skill": spec["name"],
                "evidence_text": text[start:end],
                "start_offset": start,
                "end_offset": end,
                "skill_category": "technical",
                "category_confidence": 0.99,
                "confidence_score": 0.99,
                "extraction_source": "curated_technical_alias",
                "technical_competency_id": spec["id"],
            })
    spans.sort(key=lambda span: span["start_offset"])
    for idx, span in enumerate(spans, start=1):
        span["span_id"] = f"TECH-{idx:02d}"
    return spans
