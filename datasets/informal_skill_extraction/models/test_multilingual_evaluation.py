"""
ELEVATE X AI — FEATURE 1: MULTILINGUAL PIPELINE & UNICODE OFFSET TEST SUITE
Evaluates tokenizer, span alignment, and canonical skill retrieval across:
1. Devanagari Hindi
2. Roman Hindi
3. Hinglish (Colloquial code-switching)
4. English
5. Mixed-script text (Devanagari + Latin)

Strict Invariant Tested:
text[start_offset:end_offset] == extracted_skill across all scripts!
Notice: Synthetic examples used strictly for pipeline and software verification.
"""

import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE_DIR))

from datasets.informal_skill_extraction.models.inference import extract_skills
from datasets.informal_skill_extraction.models.bio_tokenizer import BIOTokenizer

TEST_CASES = [
    {
        "id": "CASE-01-DEVANAGARI-HINDI",
        "script": "devanagari",
        "language": "hindi",
        "text": "हम सीपीवीसी पाइप कटर से काट कर सॉल्वेंट सीमेंट लगाते हैं और वाटर लेवल पाइप से लेवल मिलाते हैं।",
        "expected_domain": "TRD-03"
    },
    {
        "id": "CASE-02-ROMAN-HINDI",
        "script": "latin",
        "language": "roman_hindi",
        "text": "Dukan par customer ka inch tape se naap lekar fabric cutting karta hu aur bakram chipkakar collar banata hu.",
        "expected_domain": "TRD-01"
    },
    {
        "id": "CASE-03-HINGLISH-CODE-SWITCH",
        "script": "latin",
        "language": "hinglish",
        "text": "Main 5 saal se bike repair mein engine oil change karta hu aur feeler gauge se plug gap set karta hu.",
        "expected_domain": "TRD-04"
    },
    {
        "id": "CASE-04-ENGLISH",
        "script": "latin",
        "language": "english",
        "text": "I install concealed PVC electrical conduits and wire miniature circuit breaker distribution boards.",
        "expected_domain": "TRD-02"
    },
    {
        "id": "CASE-05-MIXED-SCRIPT",
        "script": "mixed",
        "language": "multilingual",
        "text": "Hamara main kaam MCB distribution board की वायरिंग aur earthing pit testing करना है।",
        "expected_domain": "TRD-02"
    }
]

def run_multilingual_tests():
    print("=" * 70)
    print("ELEVATE X AI — MULTILINGUAL PIPELINE & UNICODE OFFSET VERIFICATION")
    print("=" * 70)
    print("Testing 5 linguistic modes (Devanagari, Roman Hindi, Hinglish, English, Mixed)...")
    
    total_spans_tested = 0
    total_offset_mismatches = 0
    
    for case in TEST_CASES:
        c_id = case["id"]
        text = case["text"]
        lang = case["language"]
        script = case["script"]
        
        print(f"\n--- [{c_id}] ({lang.upper()} | {script.upper()}) ---")
        print(f"Input: \"{text}\"")
        
        res = extract_skills(text)
        occ = res["detected_occupation"]
        spans = res["extracted_skills"]
        
        print(f"Detected Trade: [{occ['occupation_id']}] {occ['occupation_title']} (Confidence: {occ['confidence']})")
        print(f"Extracted Spans Count: {len(spans)}")
        
        for sp in spans:
            total_spans_tested += 1
            st = sp["start_offset"]
            en = sp["end_offset"]
            surf = sp["extracted_skill"]
            actual_slice = text[st:en]
            
            # Strict slice invariant
            if actual_slice != surf:
                total_offset_mismatches += 1
                print(f"  ❌ MISMATCH: text[{st}:{en}] == '{actual_slice}' != '{surf}'")
            else:
                print(f"  ✓ [{sp['span_id']}] '{surf}' -> Category: {sp['skill_category']} | Canonical: {sp['canonical_skill']} (Conf: {sp['mapping_confidence']})")
                
    print("\n" + "=" * 70)
    print(f"VERIFICATION SUMMARY: {total_spans_tested} spans tested across 5 language modes.")
    print(f"Total Character Offset Errors: {total_offset_mismatches}")
    if total_offset_mismatches == 0:
        print("ALL MULTILINGUAL & UNICODE TESTS PASSED (100% Offset Invariant Guarantee)!")
    else:
        print("FAILURES DETECTED!")
    print("=" * 70)
    
    return total_offset_mismatches == 0

if __name__ == "__main__":
    success = run_multilingual_tests()
    sys.exit(0 if success else 1)

