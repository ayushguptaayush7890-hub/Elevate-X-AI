"""
ELEVATE X AI — FEATURE 1: SEMANTIC SKILL NORMALIZER & SPAN CONSOLIDATOR
Controlled post-processing layer that:
1. Rejects isolated generic words (e.g., 'electrician', 'customer', 'check', 'machine', 'repair') unless in supported compound context.
2. Groups adjacent related skill tokens into meaningful vocational tasks.
3. Extends technical nouns with attached action verbs in the verbatim text.
4. Produces normalized vocational competency names while preserving exact character offsets (text[start:end] == extracted_skill).
5. Guarantees evidence_text matches the verbatim source substring.
"""

import re
from typing import List, Dict, Any, Tuple, Optional

# Generic words that cannot stand alone as distinct competencies
DISALLOWED_STANDALONE_WORDS = {
    # Occupation titles (should be detected as occupation, not skills)
    "electrician", "plumber", "tailor", "mechanic", "carpenter", "welder", 
    "painter", "mason", "raj mistri", "technician", "worker", "farmer", "kisan",
    
    # Generic isolated verbs without specific object
    "check", "checking", "repair", "repairing", "install", "installing", 
    "kaam", "work", "working", "service", "servicing", "chalata", "operate",
    "kar", "karta", "karti", "karte", "karna", "lagata", "lagana", "banata", "banana",
    "silta", "silna", "leta", "lena", "change", "testing",
    "know", "knows", "knowing", "have", "has", "had", "experience", "experienced",
    "janta", "aata", "seekha", "seekh", "kare",
    
    # Generic isolated nouns without task specification
    "customer", "client", "grahak", "machine", "machines", "tool", "tools",
    "saman", "cheez", "cheezein", "system", "part", "parts",
    "suit", "bike", "car", "wall", "diwar", "pipe", "pipes", "cement", "mortar", "bricks", "faults",
    
    # Connectives, conjunctions & pronouns
    "aur", "and", "or", "ka", "ki", "ke", "se", "ko", "mein", "me", "par", "pe",
    "main", "hum", "mera", "meri", "mere", "aap", "tum", "i", "we", "you", "they", "he", "she", "it"
}

# Controlled vocational compound patterns for Indian trade contexts
# Maps regex pattern over verbatim input text to (normalized_competency_name, functional_category)
COMPOUND_PATTERNS = [
    # 1. Electrician (TRD-02)
    (r"\b(mcb\s+install(?:ation)?)\b", "MCB Installation", "technical_tactile"),
    (r"\b(electrical\s+faults?\s+check(?:ing)?)\b", "Electrical Fault Diagnosis & Checking", "quality_inspection"),
    (r"\b(wiring)\b", "Electrical Wiring Installation", "technical_tactile"),
    (r"\b(conduit\s+wiring)\b", "Concealed Conduit Wiring", "technical_tactile"),
    (r"\b(multimeter)\b", "Multimeter Operation", "tool_operation"),
    (r"\b(distribution\s+board\s+install(?:ation)?)\b", "Distribution Board Installation", "technical_tactile"),
    (r"\b(earthing\s+pit\s+install(?:ation)?)\b", "Earthing Pit Installation", "technical_tactile"),
    
    # 2. Tailor and Garment Worker (TRD-01)
    (r"\b(kapde\s+ki\s+cutting)\b", "Garment Pattern & Fabric Cutting", "technical_tactile"),
    (r"\b(customer\s+ke\s+measurement(?:s)?)\b", "Customer Measurement & Sizing", "measurement_planning"),
    (r"\b(sewing\s+machine)\b", "Industrial Sewing Machine Operation", "tool_operation"),
    (r"\b(suit\s+silta)\b", "Suit Stitching & Garment Assembly", "technical_tactile"),
    (r"\b(katori\s+blouse\s+drafting)\b", "Traditional Katori Blouse Drafting", "technical_tactile"),
    (r"\b(overlock\s+machine)\b", "Overlock Machine Operation", "tool_operation"),
    (r"\b(dart\s+stitching)\b", "Dart Stitching & Garment Shaping", "technical_tactile"),
    
    # 3. Plumber (TRD-03)
    (r"\b(cpvc\s+pipe\s+cutting)\b", "CPVC Pipe Cutting & Sizing", "technical_tactile"),
    (r"\b(solvent\s+cement)\b", "Solvent Cement Application", "technical_tactile"),
    (r"\b(leakage\s+repair)\b", "Plumbing Leakage Repair", "troubleshooting_repair"),
    (r"\b(pipe\s+thread(?:ing)?)\b", "Pipe Threading & Fitting", "tool_operation"),
    (r"\b(drainage\s+pipe\s+laying)\b", "Drainage Pipe Laying", "technical_tactile"),
    (r"\b(submersible\s+pump\s+repair)\b", "Submersible Pump Repair", "troubleshooting_repair"),

    # 4. Motor Mechanic (TRD-04)
    (r"\b(engine\s+repair)\b", "Engine Repair & Overhaul", "troubleshooting_repair"),
    (r"\b(spark\s+plug\s+gap\s+check(?:ing)?)\b", "Spark Plug Gap Inspection", "quality_inspection"),
    (r"\b(brake\s+service)\b", "Brake System Service", "technical_tactile"),
    (r"\b(carburetor\s+tuning)\b", "Carburetor Tuning & Cleaning", "troubleshooting_repair"),
    (r"\b(oil\s+filter\s+change)\b", "Engine Oil & Filter Replacement", "technical_tactile"),
    
    # 5. Carpenter (TRD-05)
    (r"\b(lakdi\s+ki\s+cutting)\b", "Wood Cutting & Panel Sizing", "technical_tactile"),
    (r"\b(furniture\s+assemble)\b", "Furniture Assembly", "technical_tactile"),
    (r"\b(wooden\s+joints\s+banata)\b", "Wood Joinery & Joint Fabrication", "technical_tactile"),
    (r"\b(circular\s+saw\s+plywood)\b", "Circular Saw Plywood Panel Sizing", "tool_operation"),
    (r"\b(laminate\s+sheet\s+pressing)\b", "Laminate Sheet Pressing", "technical_tactile"),

    # 6. Welder (TRD-06)
    (r"\b(arc\s+welding)\b", "Manual Metal Arc Welding (MMAW)", "technical_tactile"),
    (r"\b(electrode\s+select)\b", "Electrode Selection & Preparation", "technical_tactile"),
    (r"\b(metal\s+joints\s+inspect)\b", "Weld Joint Quality Inspection", "quality_inspection"),
    (r"\b(root\s+pass\s+welding)\b", "Root Pass Joint Welding", "technical_tactile"),

    # 7. Painter (TRD-08)
    (r"\b(wall\s+surface\s+prepare)\b", "Wall Surface Preparation", "technical_tactile"),
    (r"\b(putty\s+lagata)\b", "Wall Putty Application & Leveling", "technical_tactile"),
    (r"\b(primer\s+aur\s+paint\s+apply)\b", "Primer & Paint Coating Application", "technical_tactile"),
    (r"\b(abrasive\s+sanding)\b", "Abrasive Sanding & Wall Sealing", "technical_tactile"),

    # 8. Mason (TRD-07)
    (r"\b(bricks\s+lagata)\b", "Brick Masonry & Alignment", "technical_tactile"),
    (r"\b(cement\s+mortar\s+prepare)\b", "Cement Mortar Preparation & Mixing", "technical_tactile"),
    (r"\b(wall\s+plastering)\b", "Wall Plastering & Surface Finishing", "technical_tactile"),

    # 9. Agriculture Worker (TRD-09)
    (r"\b(irrigation\s+pipes\s+install)\b", "Drip & Irrigation Pipe Installation", "technical_tactile"),
    (r"\b(soil\s+preparation)\b", "Agricultural Soil Preparation", "technical_tactile"),
    (r"\b(crops\s+ki\s+dekhbhal)\b", "Crop Monitoring & Field Health Care", "technical_tactile"),

    # 10. Mobile Repair Technician (TRD-10)
    (r"\b(mobile\s+phone\s+open)\b", "Mobile Phone Disassembly & Housing Opening", "technical_tactile"),
    (r"\b(charging\s+port\s+replace)\b", "Charging Port Soldering & Replacement", "troubleshooting_repair"),
    (r"\b(pcb\s+faults?\s+check)\b", "PCB Diagnostic Fault Checking", "quality_inspection"),
]

# Action verbs that attach to technical nouns to form compound tasks
ACTION_VERB_PATTERNS = [
    r"\binstall(?:ation)?\b",
    r"\brepair(?:ing)?\b",
    r"\bcheck(?:ing)?\b",
    r"\bcutting\b",
    r"\bmeasurement\b",
    r"\bservice\b",
    r"\boperation\b",
    r"\bjoining\b",
    r"\blagata\b",
    r"\bsilta\b",
    r"\bprepare\b",
    r"\bassemble\b",
    r"\binspect\b",
    r"\bapply\b"
]


class SemanticSkillNormalizer:
    @staticmethod
    def is_disallowed_standalone(phrase: str) -> bool:
        """Checks if a phrase is a standalone generic word."""
        clean = phrase.strip().lower()
        if clean in ("c++", "c#", "ai", "ml", "js", "ts", "sql", "r", "go", "git", "aws", "gcp"):
            return False
        clean_stripped = re.sub(r"[^\w\s]", "", clean)
        return clean_stripped in DISALLOWED_STANDALONE_WORDS or len(clean_stripped) < 3

    @staticmethod
    def find_compound_matches(text: str) -> List[Dict[str, Any]]:
        """
        Scans text for predefined high-precision compound vocational phrases.
        Guarantees text[start:end] == extracted_skill.
        """
        compound_spans = []
        for pattern, norm_name, cat in COMPOUND_PATTERNS:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                st, en = m.span(1)
                extracted = text[st:en]
                compound_spans.append({
                    "start_offset": st,
                    "end_offset": en,
                    "extracted_skill": extracted,
                    "normalized_skill": norm_name,
                    "evidence_text": extracted,
                    "skill_category": cat,
                    "confidence_score": 0.95
                })
        return compound_spans

    @staticmethod
    def consolidate_and_normalize(
        text: str,
        raw_spans: List[Dict[str, Any]],
        occupation_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Pure ML model post-processing pipeline:
        1. Takes ONLY model-predicted spans (strictly no synthetic or regex compound injection).
        2. Filters out disallowed standalone conversational tokens (e.g. 'aur', 'main').
        3. Assigns standardized normalized display labels while strictly preserving verbatim offsets.
        """
        all_candidates = []

        # Process model-predicted spans
        for r_sp in raw_spans:
            st = r_sp["start_offset"]
            en = r_sp["end_offset"]
            extracted = r_sp["extracted_skill"].strip()

            if not extracted:
                continue

            # Check disallowed standalone words
            if SemanticSkillNormalizer.is_disallowed_standalone(extracted):
                continue

            norm_label = SemanticSkillNormalizer.get_normalized_label(extracted, r_sp.get("skill_category"))

            all_candidates.append({
                "start_offset": st,
                "end_offset": en,
                "extracted_skill": extracted,
                "normalized_skill": norm_label,
                "evidence_text": extracted,
                "skill_category": r_sp.get("skill_category", "technical_tactile"),
                "confidence_score": r_sp.get("confidence_score", 0.90)
            })

        # Step 3: Sort by start offset and resolve any remaining overlaps
        all_candidates.sort(key=lambda x: (x["start_offset"], -x["end_offset"]))
        
        final_spans = []
        last_end = -1
        for sp in all_candidates:
            st = sp["start_offset"]
            en = sp["end_offset"]
            if st >= last_end:
                # Strictly verify slicing invariant
                assert text[st:en] == sp["extracted_skill"], f"Invariant failed: '{text[st:en]}' != '{sp['extracted_skill']}'"
                final_spans.append(sp)
                last_end = en

        return final_spans

    @staticmethod
    def get_normalized_label(phrase: str, category: Optional[str] = None) -> str:
        """
        Generates a standardized professional competency label for an extracted phrase.
        """
        p_lower = phrase.lower().strip()
        
        # Specific normalizations
        if "wiring" in p_lower:
            return "Electrical Wiring Installation"
        if "multimeter" in p_lower:
            return "Multimeter Operation"
        if "mcb" in p_lower:
            return "MCB Installation"
        if "fault" in p_lower and "check" in p_lower:
            return "Electrical Fault Diagnosis & Checking"
        if "cutting" in p_lower and ("pipe" in p_lower or "cpvc" in p_lower):
            return "CPVC Pipe Cutting & Sizing"
        if "solvent" in p_lower or "cement" in p_lower:
            return "Solvent Cement Application"
        if "leakage" in p_lower or "leak" in p_lower:
            return "Plumbing Leakage Repair"
        if "cutting" in p_lower and ("kapde" in p_lower or "fabric" in p_lower or "cloth" in p_lower):
            return "Garment Pattern & Fabric Cutting"
        if "measurement" in p_lower:
            return "Customer Measurement & Sizing"
        if "sewing" in p_lower or "machine" in p_lower:
            return "Industrial Sewing Machine Operation"
        if "suit" in p_lower or "silta" in p_lower or "stitching" in p_lower:
            return "Suit Stitching & Garment Assembly"
        if "engine" in p_lower:
            return "Engine Repair & Overhaul"
        if "spark plug" in p_lower:
            return "Spark Plug Gap Inspection"
        if "brake" in p_lower:
            return "Brake System Service"
            
        # Default: clean title case
        return phrase.strip().title()
