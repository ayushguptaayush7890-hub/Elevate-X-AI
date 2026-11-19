"""
ELEVATE X AI — FEATURE 1: CANONICAL SKILL MAPPING QUALITY EVALUATION DATASET GENERATOR & BENCHMARK
Generates 220 comprehensive evaluation cases covering all 10 occupations across:
- Correct Mappings (True Positives)
- Semantically Incompatible / Subtly Different Tasks (True Negatives)
- Ambiguous Phrases (True Negatives)
- Unsupported Genuine Trade Competencies (True Negatives)
- Out-of-Domain Non-Trade Terms (True Negatives)

Evaluates CanonicalSkillRetriever on all cases and reports:
- Precision, Recall, Specificity, Accuracy
- False Mappings (False Positives)
- False Unmapped (False Negatives)
- Breakdown by human-reviewed vs synthetic cases
- Breakdown by trade
"""

import sys
from pathlib import Path
import csv

# Ensure repo root is on sys.path
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from datasets.informal_skill_extraction.models.canonical_skill_retriever import CanonicalSkillRetriever

EVAL_CASES = [
    # =========================================================================
    # TRD-01: Tailor and Garment Worker (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-001", "occ": "TRD-01", "phrase": "single needle silai", "gt_id": "SKL-TLR-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Hinglish term for single needle lockstitch"},
    {"id": "EVAL-002", "occ": "TRD-01", "phrase": "suit silta", "gt_id": "SKL-TLR-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular lockstitch garment assembly"},
    {"id": "EVAL-003", "occ": "TRD-01", "phrase": "sewing machine", "gt_id": "SKL-TLR-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Industrial sewing machine operation"},
    {"id": "EVAL-004", "occ": "TRD-01", "phrase": "overlock maarna", "gt_id": "SKL-TLR-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Hinglish 3/5 thread overlock edging"},
    {"id": "EVAL-005", "occ": "TRD-01", "phrase": "interlock seaming", "gt_id": "SKL-TLR-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "English alias for edge serging"},
    {"id": "EVAL-006", "occ": "TRD-01", "phrase": "bakram press karna", "gt_id": "SKL-TLR-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Fusible interlining application to collar"},
    {"id": "EVAL-007", "occ": "TRD-01", "phrase": "collar making", "gt_id": "SKL-TLR-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Collar stitching and fusible bonding"},
    {"id": "EVAL-008", "occ": "TRD-01", "phrase": "kapde ki cutting", "gt_id": "SKL-TLR-004", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Pattern measurement and fabric cutting"},
    {"id": "EVAL-009", "occ": "TRD-01", "phrase": "customer ka naap lena", "gt_id": "SKL-TLR-004", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Body anatomical measurement taking"},
    {"id": "EVAL-010", "occ": "TRD-01", "phrase": "katora cutting karna", "gt_id": "SKL-TLR-005", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Traditional katori blouse drafting"},
    {"id": "EVAL-011", "occ": "TRD-01", "phrase": "machine tension set karna", "gt_id": "SKL-TLR-006", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Sewing machine tension calibration"},
    # Semantically Incompatible (4)
    {"id": "EVAL-012", "occ": "TRD-01", "phrase": "kapde ki iron pressing", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "General clothes ironing is not fusible canvas bonding"},
    {"id": "EVAL-013", "occ": "TRD-01", "phrase": "fabric dyeing in vat", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Dyeing fabric plies is not garment cutting or stitching"},
    {"id": "EVAL-014", "occ": "TRD-01", "phrase": "tailoring shears oiling", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Scissor oiling is not machine feed dog calibration"},
    {"id": "EVAL-015", "occ": "TRD-01", "phrase": "thread spool inventory check", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Stock counting is not seam sewing"},
    # Ambiguous Skills (3)
    {"id": "EVAL-016", "occ": "TRD-01", "phrase": "silai ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic tailoring statement lacks specific NOS task"},
    {"id": "EVAL-017", "occ": "TRD-01", "phrase": "general tailor work", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Vague trade description"},
    {"id": "EVAL-018", "occ": "TRD-01", "phrase": "alteration and fitting", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Unspecified garment modification"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-019", "occ": "TRD-01", "phrase": "fall pico border finishing", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Saree pico/fall is genuine trade skill but absent in 32 catalogue"},
    {"id": "EVAL-020", "occ": "TRD-01", "phrase": "kaj button lagana", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Manual button and buttonhole stitching is not in 32 catalogue"},
    {"id": "EVAL-021", "occ": "TRD-01", "phrase": "pant zipper replacement", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Zip attachment NOS is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-022", "occ": "TRD-01", "phrase": "tailoring shop billing ledger", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Clerical accounting task"},

    # =========================================================================
    # TRD-02: Electrician (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-023", "occ": "TRD-02", "phrase": "jhirri kaatna", "gt_id": "SKL-ELE-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular Hindi for wall conduit chasing"},
    {"id": "EVAL-024", "occ": "TRD-02", "phrase": "pvc conduit fitting", "gt_id": "SKL-ELE-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Rigid PVC pipe installation in wall channels"},
    {"id": "EVAL-025", "occ": "TRD-02", "phrase": "wall chasing", "gt_id": "SKL-ELE-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "English trade standard for masonry chasing"},
    {"id": "EVAL-026", "occ": "TRD-02", "phrase": "MCB box wiring", "gt_id": "SKL-ELE-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Distribution board dressing and MCB termination"},
    {"id": "EVAL-027", "occ": "TRD-02", "phrase": "MCB install", "gt_id": "SKL-ELE-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Miniature Circuit Breaker mounting and wiring"},
    {"id": "EVAL-028", "occ": "TRD-02", "phrase": "distribution board dressing", "gt_id": "SKL-ELE-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Panel wire bundling and busbar connection"},
    {"id": "EVAL-029", "occ": "TRD-02", "phrase": "multimeter se check karna", "gt_id": "SKL-ELE-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular multimeter diagnostics"},
    {"id": "EVAL-030", "occ": "TRD-02", "phrase": "voltage testing", "gt_id": "SKL-ELE-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "AC voltage measurement between phase and neutral"},
    {"id": "EVAL-031", "occ": "TRD-02", "phrase": "electrical faults check", "gt_id": "SKL-ELE-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Continuity and fault diagnosis using multimeter"},
    {"id": "EVAL-032", "occ": "TRD-02", "phrase": "earthing pit banana", "gt_id": "SKL-ELE-004", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Grounding installation and earth pit excavation"},
    {"id": "EVAL-033", "occ": "TRD-02", "phrase": "earth resistance testing", "gt_id": "SKL-ELE-004", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Megger verification of grounding ohms"},
    # Semantically Incompatible (4)
    {"id": "EVAL-034", "occ": "TRD-02", "phrase": "conduit wire pulling with fish tape", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Cable pulling is distinct from conduit chasing and masonry grooving"},
    {"id": "EVAL-035", "occ": "TRD-02", "phrase": "meter reading register entry", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Reading energy meter digits is not multimeter voltage diagnosis"},
    {"id": "EVAL-036", "occ": "TRD-02", "phrase": "switch board plastic cover wiping", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Cleaning faceplates is not MCB distribution termination"},
    {"id": "EVAL-037", "occ": "TRD-02", "phrase": "light bulb replacement in holder", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Screwing light bulbs is not DB panel wiring"},
    # Ambiguous Skills (3)
    {"id": "EVAL-038", "occ": "TRD-02", "phrase": "wiring", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic wiring without conduit or panel context is ambiguous"},
    {"id": "EVAL-039", "occ": "TRD-02", "phrase": "bijli ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "General electrical trade statement"},
    {"id": "EVAL-040", "occ": "TRD-02", "phrase": "electrical fault repair", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Vague fault repair without testing tool or equipment context"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-041", "occ": "TRD-02", "phrase": "submersible motor copper rewinding", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Motor stator rewinding is not in 32 catalogue"},
    {"id": "EVAL-042", "occ": "TRD-02", "phrase": "ceiling fan capacitor change", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Capacitor replacement is not in 32 catalogue"},
    {"id": "EVAL-043", "occ": "TRD-02", "phrase": "solar inverter battery hydrometer testing", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Battery specific gravity check is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-044", "occ": "TRD-02", "phrase": "delivery bike driving", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Transportation activity"},

    # =========================================================================
    # TRD-03: Plumber (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-045", "occ": "TRD-03", "phrase": "cpvc solvent fitting", "gt_id": "SKL-PLM-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "CPVC solvent cement jointing"},
    {"id": "EVAL-046", "occ": "TRD-03", "phrase": "solvent cement lagana", "gt_id": "SKL-PLM-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Chemical solvent weld application"},
    {"id": "EVAL-047", "occ": "TRD-03", "phrase": "pipe jointing with solvent", "gt_id": "SKL-PLM-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Solvent cement joint creation"},
    {"id": "EVAL-048", "occ": "TRD-03", "phrase": "GI chudi kaatna", "gt_id": "SKL-PLM-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular GI pipe manual die threading"},
    {"id": "EVAL-049", "occ": "TRD-03", "phrase": "pipe die threading", "gt_id": "SKL-PLM-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Manual pipe die stock threading"},
    {"id": "EVAL-050", "occ": "TRD-03", "phrase": "gi pipe par die se chudi kaatna", "gt_id": "SKL-PLM-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Thread cutting on galvanized iron pipe"},
    {"id": "EVAL-051", "occ": "TRD-03", "phrase": "diverter fitting", "gt_id": "SKL-PLM-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Concealed wall diverter installation"},
    {"id": "EVAL-052", "occ": "TRD-03", "phrase": "shower mixer mounting", "gt_id": "SKL-PLM-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Concealed wall diverter shower alignment"},
    {"id": "EVAL-053", "occ": "TRD-03", "phrase": "wall diverter lagana", "gt_id": "SKL-PLM-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Wall diverter assembly and pipe alignment"},
    {"id": "EVAL-054", "occ": "TRD-03", "phrase": "flush tank float valve fix", "gt_id": "SKL-PLM-004", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Flush cistern float valve repair"},
    {"id": "EVAL-055", "occ": "TRD-03", "phrase": "cistern repair", "gt_id": "SKL-PLM-004", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Toilet flush tank siphon and valve servicing"},
    # Semantically Incompatible (4) - Specifically testing the suspicious audit cases
    {"id": "EVAL-056", "occ": "TRD-03", "phrase": "CPVC pipe cutting", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "CRITICAL AUDIT CASE: Cutting pipe is prep work, not solvent cement jointing"},
    {"id": "EVAL-057", "occ": "TRD-03", "phrase": "leakage repair", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "CRITICAL AUDIT CASE: Generic leakage fix is not flush cistern valve inspection"},
    {"id": "EVAL-058", "occ": "TRD-03", "phrase": "pipe unblocking with steel wire", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Clearing pipe block is not die threading"},
    {"id": "EVAL-059", "occ": "TRD-03", "phrase": "drain line grease trap cleaning", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Sludge cleaning is not diverter installation"},
    # Ambiguous Skills (3)
    {"id": "EVAL-060", "occ": "TRD-03", "phrase": "plumbing work", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic trade title statement"},
    {"id": "EVAL-061", "occ": "TRD-03", "phrase": "paani ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Vernacular broad description"},
    {"id": "EVAL-062", "occ": "TRD-03", "phrase": "pipe fitting", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Missing material (CPVC/GI) and action (solvent/thread/diverter)"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-063", "occ": "TRD-03", "phrase": "water storage tank cleaning", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Overhead tank descaling is not in 32 catalogue"},
    {"id": "EVAL-064", "occ": "TRD-03", "phrase": "RO water purifier candle replacement", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "RO filter change is not in 32 catalogue"},
    {"id": "EVAL-065", "occ": "TRD-03", "phrase": "gas geyser water connection", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Water heater plumbing is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-066", "occ": "TRD-03", "phrase": "hardware shop counter sales", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Retail commerce activity"},

    # =========================================================================
    # TRD-04: Motor Mechanic (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-067", "occ": "TRD-04", "phrase": "engine oil change", "gt_id": "SKL-MEC-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Motorcycle engine oil drain and refill"},
    {"id": "EVAL-068", "occ": "TRD-04", "phrase": "mobil oil drain", "gt_id": "SKL-MEC-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Sump plug opening and used engine oil drain"},
    {"id": "EVAL-069", "occ": "TRD-04", "phrase": "oil filter replacement", "gt_id": "SKL-MEC-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Oil drain and filter element replacement"},
    {"id": "EVAL-070", "occ": "TRD-04", "phrase": "tappet setting", "gt_id": "SKL-MEC-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Feeler gauge valve tappet clearance calibration"},
    {"id": "EVAL-071", "occ": "TRD-04", "phrase": "valve clearance adjustment", "gt_id": "SKL-MEC-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Engine valve clearance tuning"},
    {"id": "EVAL-072", "occ": "TRD-04", "phrase": "tappet set karna", "gt_id": "SKL-MEC-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular tappet clearance setting"},
    {"id": "EVAL-073", "occ": "TRD-04", "phrase": "brake bleeding", "gt_id": "SKL-MEC-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Hydraulic disc brake air bleeding"},
    {"id": "EVAL-074", "occ": "TRD-04", "phrase": "disc brake oil badalna", "gt_id": "SKL-MEC-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Brake master cylinder fluid replacement and bleeding"},
    {"id": "EVAL-075", "occ": "TRD-04", "phrase": "hydraulic disc brake bleeding", "gt_id": "SKL-MEC-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Caliper hydraulic purge"},
    {"id": "EVAL-076", "occ": "TRD-04", "phrase": "brake service", "gt_id": "SKL-MEC-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Brake system service and bleeding"},
    {"id": "EVAL-077", "occ": "TRD-04", "phrase": "engine oil drain", "gt_id": "SKL-MEC-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Engine lubrication service"},
    # Semantically Incompatible (4) - Specifically testing the suspicious audit cases
    {"id": "EVAL-078", "occ": "TRD-04", "phrase": "engine repair", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "CRITICAL AUDIT CASE: Engine overhaul is not oil drain and replacement"},
    {"id": "EVAL-079", "occ": "TRD-04", "phrase": "engine overhaul and piston replacement", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Rebuilding cylinder head is not oil change"},
    {"id": "EVAL-080", "occ": "TRD-04", "phrase": "drum brake shoe sanding", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Mechanical drum shoe sanding is not hydraulic disc caliper bleeding"},
    {"id": "EVAL-081", "occ": "TRD-04", "phrase": "clutch cable lubrication", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Wire cable greasing is not engine oil drain"},
    # Ambiguous Skills (3)
    {"id": "EVAL-082", "occ": "TRD-04", "phrase": "bike servicing", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Vague general servicing without specified task"},
    {"id": "EVAL-083", "occ": "TRD-04", "phrase": "mechanic ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic trade identity statement"},
    {"id": "EVAL-084", "occ": "TRD-04", "phrase": "engine sound checking", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Auditory listening without feeler gauge calibration"},
    # Unsupported Genuine Trade Skills (3) - Specifically testing spark plug gap
    {"id": "EVAL-085", "occ": "TRD-04", "phrase": "spark plug gap check", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "CRITICAL AUDIT CASE: Genuine mechanic skill absent in 32 catalogue, correctly unmapped"},
    {"id": "EVAL-086", "occ": "TRD-04", "phrase": "carburetor jet tuning", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Fuel air ratio screw tuning is not in 32 catalogue"},
    {"id": "EVAL-087", "occ": "TRD-04", "phrase": "drive chain tension adjustment", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Chain slack adjustment is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-088", "occ": "TRD-04", "phrase": "motorbike washing with shampoo", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Cosmetic cleaning activity"},

    # =========================================================================
    # TRD-05: Carpenter (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-089", "occ": "TRD-05", "phrase": "circular saw se ply kaatna", "gt_id": "SKL-CRP-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Circular saw plywood panel sizing"},
    {"id": "EVAL-090", "occ": "TRD-05", "phrase": "plywood cutting", "gt_id": "SKL-CRP-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Power saw wood panel slicing"},
    {"id": "EVAL-091", "occ": "TRD-05", "phrase": "sheet sizing with circular saw", "gt_id": "SKL-CRP-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Straight guide panel cutting"},
    {"id": "EVAL-092", "occ": "TRD-05", "phrase": "sunmica press karna", "gt_id": "SKL-CRP-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Laminate sheet pressing with adhesive"},
    {"id": "EVAL-093", "occ": "TRD-05", "phrase": "fevicol lagakar laminate chipkana", "gt_id": "SKL-CRP-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular decorative laminate bonding"},
    {"id": "EVAL-094", "occ": "TRD-05", "phrase": "adhesive application on plywood", "gt_id": "SKL-CRP-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Contact adhesive spreading and pressing"},
    {"id": "EVAL-095", "occ": "TRD-05", "phrase": "randa chalana", "gt_id": "SKL-CRP-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular hand wood planer leveling"},
    {"id": "EVAL-096", "occ": "TRD-05", "phrase": "hand planing", "gt_id": "SKL-CRP-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Manual wood surface smoothing"},
    {"id": "EVAL-097", "occ": "TRD-05", "phrase": "wood surface leveling with randa", "gt_id": "SKL-CRP-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Timber edge planing"},
    {"id": "EVAL-098", "occ": "TRD-05", "phrase": "circular saw plywood panel sizing", "gt_id": "SKL-CRP-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Full canonical phrase match"},
    {"id": "EVAL-099", "occ": "TRD-05", "phrase": "laminate sheet pressing", "gt_id": "SKL-CRP-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Laminate roller pressing"},
    # Semantically Incompatible (4)
    {"id": "EVAL-100", "occ": "TRD-05", "phrase": "plywood sheet unloading from truck", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Manual material handling is not saw panel sizing"},
    {"id": "EVAL-101", "occ": "TRD-05", "phrase": "sunmica edge trimming with cutter blade", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Scoring laminate edge is not full sheet adhesive pressing"},
    {"id": "EVAL-102", "occ": "TRD-05", "phrase": "wood varnish brush coating", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Clear varnish painting is not mechanical wood planing"},
    {"id": "EVAL-103", "occ": "TRD-05", "phrase": "randa blade whetstone sharpening", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Honing planer iron is maintenance, not timber planing"},
    # Ambiguous Skills (3)
    {"id": "EVAL-104", "occ": "TRD-05", "phrase": "furniture banana", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic furniture making statement"},
    {"id": "EVAL-105", "occ": "TRD-05", "phrase": "lakdi ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Broad woodcraft trade reference"},
    {"id": "EVAL-106", "occ": "TRD-05", "phrase": "wood cutting with hand saw", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Handsaw timber crosscut is not circular saw plywood panel sizing"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-107", "occ": "TRD-05", "phrase": "mortise and tenon joint chiseled", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Traditional joinery carving is not in 32 catalogue"},
    {"id": "EVAL-108", "occ": "TRD-05", "phrase": "hydraulic hinge auto close alignment", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Modular kitchen fitting is not in 32 catalogue"},
    {"id": "EVAL-109", "occ": "TRD-05", "phrase": "wooden door godrej rim lock installation", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Lock fitting is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-110", "occ": "TRD-05", "phrase": "cement plaster wall troweling", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Masonry activity"},

    # =========================================================================
    # TRD-06: Welder (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-111", "occ": "TRD-06", "phrase": "arc welding", "gt_id": "SKL-WLD-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Shielded metal arc welding"},
    {"id": "EVAL-112", "occ": "TRD-06", "phrase": "6013 rod chalana", "gt_id": "SKL-WLD-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "E6013 electrode stick welding"},
    {"id": "EVAL-113", "occ": "TRD-06", "phrase": "manual stick welding", "gt_id": "SKL-WLD-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "MMAW arc fusion"},
    {"id": "EVAL-114", "occ": "TRD-06", "phrase": "chipping hammer se slag nikalna", "gt_id": "SKL-WLD-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Weld slag descaling with chipping hammer"},
    {"id": "EVAL-115", "occ": "TRD-06", "phrase": "weld cleaning", "gt_id": "SKL-WLD-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Weld bead wire brushing"},
    {"id": "EVAL-116", "occ": "TRD-06", "phrase": "slag jhaadna", "gt_id": "SKL-WLD-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular flux slag removal"},
    {"id": "EVAL-117", "occ": "TRD-06", "phrase": "grinder se bevel banana", "gt_id": "SKL-WLD-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "V-groove edge grinding with angle grinder"},
    {"id": "EVAL-118", "occ": "TRD-06", "phrase": "v-groove edge grinding", "gt_id": "SKL-WLD-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Bevel joint edge preparation"},
    {"id": "EVAL-119", "occ": "TRD-06", "phrase": "edge beveling", "gt_id": "SKL-WLD-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Plate chamfer grinding"},
    {"id": "EVAL-120", "occ": "TRD-06", "phrase": "stick welding", "gt_id": "SKL-WLD-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "SMAW manual arc joint"},
    {"id": "EVAL-121", "occ": "TRD-06", "phrase": "chipping hammer se slag hatana", "gt_id": "SKL-WLD-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Weld bead cleaning"},
    # Semantically Incompatible (4)
    {"id": "EVAL-122", "occ": "TRD-06", "phrase": "welding generator cable coiling", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Tidying wires is not striking electric arc"},
    {"id": "EVAL-123", "occ": "TRD-06", "phrase": "iron channel hacksaw cutting", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Manual hacksaw sawing is not grinder beveling"},
    {"id": "EVAL-124", "occ": "TRD-06", "phrase": "grinding disc spanner change", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Replacing tool disc is maintenance, not edge beveling"},
    {"id": "EVAL-125", "occ": "TRD-06", "phrase": "welding mask glass wiping", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Cleaning visor is not weld bead slag chipping"},
    # Ambiguous Skills (3)
    {"id": "EVAL-126", "occ": "TRD-06", "phrase": "welding ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic welding trade statement"},
    {"id": "EVAL-127", "occ": "TRD-06", "phrase": "lohe ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Vague metal trade reference"},
    {"id": "EVAL-128", "occ": "TRD-06", "phrase": "metal fabrication", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Broad trade category lacking specific NOS task"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-129", "occ": "TRD-06", "phrase": "TIG stainless steel argon welding", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "GTAW TIG welding is not in 32 catalogue"},
    {"id": "EVAL-130", "occ": "TRD-06", "phrase": "oxy acetylene gas torch cutting", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Thermal gas flame cutting is not in 32 catalogue"},
    {"id": "EVAL-131", "occ": "TRD-06", "phrase": "MIG CO2 wire feed welding", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "GMAW MIG welding is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-132", "occ": "TRD-06", "phrase": "mobile software flashing", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "IT / Electronics activity"},

    # =========================================================================
    # TRD-07: Mason (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-133", "occ": "TRD-07", "phrase": "sahul lagana", "gt_id": "SKL-MSN-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular plumb bob vertical alignment"},
    {"id": "EVAL-134", "occ": "TRD-07", "phrase": "plumb bob check", "gt_id": "SKL-MSN-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Vertical alignment measurement"},
    {"id": "EVAL-135", "occ": "TRD-07", "phrase": "sahul se seedh dekhna", "gt_id": "SKL-MSN-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Corner lead verticality check"},
    {"id": "EVAL-136", "occ": "TRD-07", "phrase": "chunai karna", "gt_id": "SKL-MSN-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Bricklaying in cement sand mortar"},
    {"id": "EVAL-137", "occ": "TRD-07", "phrase": "1:4 masala chunai", "gt_id": "SKL-MSN-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "1:4 mix brick masonry laying"},
    {"id": "EVAL-138", "occ": "TRD-07", "phrase": "brick masonry", "gt_id": "SKL-MSN-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Trowel mortar bed spreading and brick alignment"},
    {"id": "EVAL-139", "occ": "TRD-07", "phrase": "ghoontai karna", "gt_id": "SKL-MSN-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Neat cement trowel floating"},
    {"id": "EVAL-140", "occ": "TRD-07", "phrase": "neat cement finish", "gt_id": "SKL-MSN-003", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Pure cement slurry punning surface finish"},
    {"id": "EVAL-141", "occ": "TRD-07", "phrase": "cement punning", "gt_id": "SKL-MSN-003", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Waterproof slick cement troweling"},
    {"id": "EVAL-142", "occ": "TRD-07", "phrase": "vertical leveling with sahul", "gt_id": "SKL-MSN-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Masonry plumb inspection"},
    {"id": "EVAL-143", "occ": "TRD-07", "phrase": "masala banakar chunai karna", "gt_id": "SKL-MSN-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Brickwork course laying"},
    # Semantically Incompatible (4)
    {"id": "EVAL-144", "occ": "TRD-07", "phrase": "sand sieving with wire mesh screen", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Screening river sand is prep, not brick course laying"},
    {"id": "EVAL-145", "occ": "TRD-07", "phrase": "brick watering with hose pipe", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Wetting red clay bricks is prep, not trowel chunai"},
    {"id": "EVAL-146", "occ": "TRD-07", "phrase": "curing newly plastered wall with water", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Spraying curing water is not neat cement ghoontai floating"},
    {"id": "EVAL-147", "occ": "TRD-07", "phrase": "carrying cement bag on shoulder", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Labour transport is not skilled alignment"},
    # Ambiguous Skills (3)
    {"id": "EVAL-148", "occ": "TRD-07", "phrase": "raj mistri work", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic mason title statement"},
    {"id": "EVAL-149", "occ": "TRD-07", "phrase": "makaan ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Broad construction statement"},
    {"id": "EVAL-150", "occ": "TRD-07", "phrase": "cement ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Vague material reference without specific task"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-151", "occ": "TRD-07", "phrase": "concrete slab plywood shuttering", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Centering shuttering carpentry is not in 32 catalogue"},
    {"id": "EVAL-152", "occ": "TRD-07", "phrase": "vitrified floor tile fixing with adhesive", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Tile laying is not in 32 catalogue"},
    {"id": "EVAL-153", "occ": "TRD-07", "phrase": "granite kitchen slab molding polishing", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Stone counter molding is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-154", "occ": "TRD-07", "phrase": "tractor trolley driving", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Agricultural transit activity"},

    # =========================================================================
    # TRD-08: Painter (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-155", "occ": "TRD-08", "phrase": "putty patti kheenchna", "gt_id": "SKL-PNT-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular steel blade putty application"},
    {"id": "EVAL-156", "occ": "TRD-08", "phrase": "putty lagana", "gt_id": "SKL-PNT-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Wall putty skimming"},
    {"id": "EVAL-157", "occ": "TRD-08", "phrase": "wall skimming with putty blade", "gt_id": "SKL-PNT-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Acrylic wall putty smoothing"},
    {"id": "EVAL-158", "occ": "TRD-08", "phrase": "regmar maarna", "gt_id": "SKL-PNT-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular abrasive sandpapering"},
    {"id": "EVAL-159", "occ": "TRD-08", "phrase": "sandpapering putty", "gt_id": "SKL-PNT-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Silicon carbide wall surface sanding"},
    {"id": "EVAL-160", "occ": "TRD-08", "phrase": "primer lagana", "gt_id": "SKL-PNT-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Wall sealer primer application"},
    {"id": "EVAL-161", "occ": "TRD-08", "phrase": "double coat wall putty", "gt_id": "SKL-PNT-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Two coat putty blade skimming"},
    {"id": "EVAL-162", "occ": "TRD-08", "phrase": "regmar maarkar primer lagana", "gt_id": "SKL-PNT-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Progressive sanding and primer sealing"},
    {"id": "EVAL-163", "occ": "TRD-08", "phrase": "abrasive sanding", "gt_id": "SKL-PNT-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Sanding drywall with abrasive paper"},
    {"id": "EVAL-164", "occ": "TRD-08", "phrase": "putty application", "gt_id": "SKL-PNT-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Drywall skimming with blade"},
    {"id": "EVAL-165", "occ": "TRD-08", "phrase": "ghisai karna", "gt_id": "SKL-PNT-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular wall sanding for smooth surface"},
    # Semantically Incompatible (4)
    {"id": "EVAL-166", "occ": "TRD-08", "phrase": "paint bucket stirring with wooden stick", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Stirring paint dilution is not putty skimming"},
    {"id": "EVAL-167", "occ": "TRD-08", "phrase": "masking tape sticking on door frames", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Edge masking prep is not abrasive sanding"},
    {"id": "EVAL-168", "occ": "TRD-08", "phrase": "washing roller brush in mineral thinner", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Tool cleanup is not primer application"},
    {"id": "EVAL-169", "occ": "TRD-08", "phrase": "empty paint tin disposing", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Refuse handling is not putty application"},
    # Ambiguous Skills (3)
    {"id": "EVAL-170", "occ": "TRD-08", "phrase": "painting ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic painter trade statement"},
    {"id": "EVAL-171", "occ": "TRD-08", "phrase": "rangai putai", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Vague colloquial term for house painting"},
    {"id": "EVAL-172", "occ": "TRD-08", "phrase": "wall painting", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Broad category without tool/coat specification"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-173", "occ": "TRD-08", "phrase": "wood polyurethane PU lacquer spray", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Compressor wood polish spray is not in 32 catalogue"},
    {"id": "EVAL-174", "occ": "TRD-08", "phrase": "stencil wall decorative texture rolling", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Patterned texture roller design is not in 32 catalogue"},
    {"id": "EVAL-175", "occ": "TRD-08", "phrase": "terrace elastomeric waterproof coat application", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Roof waterproofing membrane is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-176", "occ": "TRD-08", "phrase": "welding safety helmet wearing", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Welding safety protocol"},

    # =========================================================================
    # TRD-09: Agriculture Worker (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-177", "occ": "TRD-09", "phrase": "drip line bichhana", "gt_id": "SKL-AGR-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular lateral drip tubing layout"},
    {"id": "EVAL-178", "occ": "TRD-09", "phrase": "lateral tubing layout", "gt_id": "SKL-AGR-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Micro-irrigation 16mm lateral unrolling"},
    {"id": "EVAL-179", "occ": "TRD-09", "phrase": "dripper punching in pipe", "gt_id": "SKL-AGR-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Emitter puncture tool installation"},
    {"id": "EVAL-180", "occ": "TRD-09", "phrase": "venturi se khad chalana", "gt_id": "SKL-AGR-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular venturi fertilizer injection"},
    {"id": "EVAL-181", "occ": "TRD-09", "phrase": "fertigation dosing", "gt_id": "SKL-AGR-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Venturi vacuum differential nutrient calibration"},
    {"id": "EVAL-182", "occ": "TRD-09", "phrase": "venturi calibration", "gt_id": "SKL-AGR-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Manometer pressure differential adjustment for suction"},
    {"id": "EVAL-183", "occ": "TRD-09", "phrase": "drip lateral pipe layout", "gt_id": "SKL-AGR-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Crop bed line layout"},
    {"id": "EVAL-184", "occ": "TRD-09", "phrase": "venturi chalana", "gt_id": "SKL-AGR-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Irrigation mainline fertilizer dosing"},
    {"id": "EVAL-185", "occ": "TRD-09", "phrase": "micro irrigation drip layout", "gt_id": "SKL-AGR-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Field tubing installation"},
    {"id": "EVAL-186", "occ": "TRD-09", "phrase": "fertilizer dosing with venturi", "gt_id": "SKL-AGR-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Venturi injector operation"},
    {"id": "EVAL-187", "occ": "TRD-09", "phrase": "dripper punching", "gt_id": "SKL-AGR-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Installing drip emitters along pipe"},
    # Semantically Incompatible (4)
    {"id": "EVAL-188", "occ": "TRD-09", "phrase": "open field mud channel clearing with spade", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Ditch flood irrigation is not micro-drip lateral layout"},
    {"id": "EVAL-189", "occ": "TRD-09", "phrase": "broadcasting urea fertilizer by hand", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Hand throwing urea pellets is not venturi hydraulic fertigation"},
    {"id": "EVAL-190", "occ": "TRD-09", "phrase": "diesel pump engine oil top up", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Pump motor servicing is not drip pipe or venturi calibration"},
    {"id": "EVAL-191", "occ": "TRD-09", "phrase": "loading wheat grain bags on cart", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Harvest hauling is not pressurized irrigation"},
    # Ambiguous Skills (3)
    {"id": "EVAL-192", "occ": "TRD-09", "phrase": "kheti ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic farmer statement"},
    {"id": "EVAL-193", "occ": "TRD-09", "phrase": "irrigation work", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Vague watering term without drip/venturi specifics"},
    {"id": "EVAL-194", "occ": "TRD-09", "phrase": "kisan farming", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Broad agricultural occupation statement"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-195", "occ": "TRD-09", "phrase": "knapsack sprayer pesticide spraying", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Manual chemical spraying is not in 32 catalogue"},
    {"id": "EVAL-196", "occ": "TRD-09", "phrase": "tractor rotavator soil tilling", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Mechanized soil tillage is not in 32 catalogue"},
    {"id": "EVAL-197", "occ": "TRD-09", "phrase": "paddy rice seedling manual transplanting", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "Wetland nursery planting is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-198", "occ": "TRD-09", "phrase": "cloth cutting shears handling", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Tailoring activity"},

    # =========================================================================
    # TRD-10: Mobile Repair Technician (22 cases)
    # =========================================================================
    # Correct Mappings (11)
    {"id": "EVAL-199", "occ": "TRD-10", "phrase": "cc pin badalna", "gt_id": "SKL-MOB-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular Hindi for micro USB / Type C port soldering"},
    {"id": "EVAL-200", "occ": "TRD-10", "phrase": "charging jack soldering", "gt_id": "SKL-MOB-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "SMD micro-soldering of charging connector"},
    {"id": "EVAL-201", "occ": "TRD-10", "phrase": "smd rework station chalana", "gt_id": "SKL-MOB-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Hot air nozzle temperature regulation for desoldering"},
    {"id": "EVAL-202", "occ": "TRD-10", "phrase": "jumper maarna", "gt_id": "SKL-MOB-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Vernacular micro wire PCB track jumper bypass"},
    {"id": "EVAL-203", "occ": "TRD-10", "phrase": "pcb track repair", "gt_id": "SKL-MOB-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Copper trace scraping and jumper wire bonding"},
    {"id": "EVAL-204", "occ": "TRD-10", "phrase": "micro wire jumper soldering", "gt_id": "SKL-MOB-002", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "0.02mm enameled jumper wire micro-soldering"},
    {"id": "EVAL-205", "occ": "TRD-10", "phrase": "smd hot air desoldering", "gt_id": "SKL-MOB-001", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Rework station component removal"},
    {"id": "EVAL-206", "occ": "TRD-10", "phrase": "usb port desoldering", "gt_id": "SKL-MOB-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "Heat gun connector removal with flux"},
    {"id": "EVAL-207", "occ": "TRD-10", "phrase": "track bypass jumper soldering", "gt_id": "SKL-MOB-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "UV solder mask cure over jumper"},
    {"id": "EVAL-208", "occ": "TRD-10", "phrase": "charging port replacement", "gt_id": "SKL-MOB-001", "gt_status": "mapped", "type": "correct_mapping", "human": True, "note": "USB charging socket resoldering"},
    {"id": "EVAL-209", "occ": "TRD-10", "phrase": "broken pcb track jumper wire bypass", "gt_id": "SKL-MOB-002", "gt_status": "mapped", "type": "correct_mapping", "human": False, "note": "Motherboard broken line repair"},
    # Semantically Incompatible (4)
    {"id": "EVAL-210", "occ": "TRD-10", "phrase": "smartphone plastic back cover prying", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Removing phone casing is disassembly, not micro-soldering"},
    {"id": "EVAL-211", "occ": "TRD-10", "phrase": "wiping tempered glass with alcohol swab", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Screen wiping is not motherboard copper jumpering"},
    {"id": "EVAL-212", "occ": "TRD-10", "phrase": "sim card tray ejecting with pin", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": True, "note": "Inserting SIM pin is not SMD rework station hot air soldering"},
    {"id": "EVAL-213", "occ": "TRD-10", "phrase": "packing phone in plastic bubble wrap", "gt_id": None, "gt_status": "unmapped", "type": "semantically_incompatible", "human": False, "note": "Shipping parcel wrap is not PCB track repair"},
    # Ambiguous Skills (3)
    {"id": "EVAL-214", "occ": "TRD-10", "phrase": "mobile repairing", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Generic trade identity statement"},
    {"id": "EVAL-215", "occ": "TRD-10", "phrase": "phone hardware repair", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": False, "note": "Vague hardware reference without component specifics"},
    {"id": "EVAL-216", "occ": "TRD-10", "phrase": "mobile ka kaam", "gt_id": None, "gt_status": "unmapped", "type": "ambiguous_skill", "human": True, "note": "Colloquial broad description"},
    # Unsupported Genuine Trade Skills (3)
    {"id": "EVAL-217", "occ": "TRD-10", "phrase": "OCA vacuum laminating display glass", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Screen separator / autoclave lamination is not in 32 catalogue"},
    {"id": "EVAL-218", "occ": "TRD-10", "phrase": "iPhone Face ID infrared dot projector repair", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": True, "note": "Biometric sensor soldering is not in 32 catalogue"},
    {"id": "EVAL-219", "occ": "TRD-10", "phrase": "EMMC BGA IC reballing with solder paste", "gt_id": None, "gt_status": "unmapped", "type": "unsupported_trade_skill", "human": False, "note": "BGA stencil reballing is not in 32 catalogue"},
    # Out of Domain (1)
    {"id": "EVAL-220", "occ": "TRD-10", "phrase": "plumber cpvc pipe cutting", "gt_id": None, "gt_status": "unmapped", "type": "out_of_domain", "human": False, "note": "Plumbing activity"}
]

def main():
    print("=" * 80)
    print("ELEVATE X AI — FEATURE 1: CANONICAL SKILL MAPPING QUALITY AUDIT")
    print(f"Total Evaluation Cases: {len(EVAL_CASES)}")
    print("=" * 80)
    
    retriever = CanonicalSkillRetriever()
    
    results = []
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    trade_metrics = {}
    human_metrics = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    synth_metrics = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    
    csv_rows = []
    
    for case in EVAL_CASES:
        c_id = case["id"]
        occ = case["occ"]
        phrase = case["phrase"]
        gt_id = case["gt_id"]
        gt_status = case["gt_status"]
        case_type = case["type"]
        is_human = case["human"]
        note = case["note"]
        
        # Initialize trade metrics container
        if occ not in trade_metrics:
            trade_metrics[occ] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0, "total": 0}
        trade_metrics[occ]["total"] += 1
        
        # Execute Canonical Matching
        res = retriever.match_phrase(phrase, occupation_id=occ)
        pred_id = res["canonical_skill_id"]
        pred_name = res["canonical_skill"]
        pred_status = res["mapping_status"]
        conf = res["confidence_score"]
        
        # Classification Evaluation Logic
        # Case 1: Ground Truth is Mapped
        if gt_status == "mapped":
            if pred_status == "mapped" and pred_id == gt_id:
                eval_outcome = "TRUE_POSITIVE"
                tp += 1
                trade_metrics[occ]["TP"] += 1
                bucket = human_metrics if is_human else synth_metrics
                bucket["TP"] += 1
            elif pred_status == "mapped" and pred_id != gt_id:
                eval_outcome = "FALSE_POSITIVE_MISMATCH"
                fp += 1
                trade_metrics[occ]["FP"] += 1
                bucket = human_metrics if is_human else synth_metrics
                bucket["FP"] += 1
            else: # pred_status == "unmapped"
                eval_outcome = "FALSE_NEGATIVE_UNMAPPED"
                fn += 1
                trade_metrics[occ]["FN"] += 1
                bucket = human_metrics if is_human else synth_metrics
                bucket["FN"] += 1
        # Case 2: Ground Truth is Unmapped
        else:
            if pred_status == "unmapped":
                eval_outcome = "TRUE_NEGATIVE"
                tn += 1
                trade_metrics[occ]["TN"] += 1
                bucket = human_metrics if is_human else synth_metrics
                bucket["TN"] += 1
            else: # pred_status == "mapped"
                eval_outcome = "FALSE_POSITIVE_OVER_MAPPED"
                fp += 1
                trade_metrics[occ]["FP"] += 1
                bucket = human_metrics if is_human else synth_metrics
                bucket["FP"] += 1
                
        csv_rows.append({
            "case_id": c_id,
            "occupation_id": occ,
            "input_phrase": phrase,
            "case_type": case_type,
            "is_human_reviewed": is_human,
            "ground_truth_status": gt_status,
            "ground_truth_canonical_id": gt_id or "UNMAPPED",
            "predicted_status": pred_status,
            "predicted_canonical_id": pred_id or "UNMAPPED",
            "predicted_canonical_name": pred_name or "None",
            "confidence_score": conf,
            "evaluation_outcome": eval_outcome,
            "notes": note
        })
        
    # Write CSV output
    out_csv = Path("reports/feature1_mapping_evaluation.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "case_id", "occupation_id", "input_phrase", "case_type", "is_human_reviewed",
        "ground_truth_status", "ground_truth_canonical_id", "predicted_status",
        "predicted_canonical_id", "predicted_canonical_name", "confidence_score",
        "evaluation_outcome", "notes"
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
        
    total = len(EVAL_CASES)
    acc = (tp + tn) / total
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    
    print("\nOVERALL BENCHMARK RESULTS:")
    print(f"Total Cases:             {total}")
    print(f"True Positives (TP):     {tp}  (Mapped accurately)")
    print(f"True Negatives (TN):     {tn}  (Safely left unmapped)")
    print(f"False Positives (FP):    {fp}  (False mappings / over-attributions)")
    print(f"False Negatives (FN):    {fn}  (Missed canonical mappings)")
    print(f"Overall Accuracy:        {acc * 100:.2f}%")
    print(f"Mapping Precision:       {prec * 100:.2f}%")
    print(f"Mapping Recall:          {rec * 100:.2f}%")
    print(f"Specificity (Unmapped):  {spec * 100:.2f}%")
    print(f"F1 Score:                {f1 * 100:.2f}%")
    
    # Human-reviewed vs Synthetic
    h_tot = human_metrics["TP"] + human_metrics["FP"] + human_metrics["TN"] + human_metrics["FN"]
    h_acc = (human_metrics["TP"] + human_metrics["TN"]) / h_tot if h_tot > 0 else 0.0
    h_prec = human_metrics["TP"] / (human_metrics["TP"] + human_metrics["FP"]) if (human_metrics["TP"] + human_metrics["FP"]) > 0 else 0.0
    h_rec = human_metrics["TP"] / (human_metrics["TP"] + human_metrics["FN"]) if (human_metrics["TP"] + human_metrics["FN"]) > 0 else 0.0
    
    s_tot = synth_metrics["TP"] + synth_metrics["FP"] + synth_metrics["TN"] + synth_metrics["FN"]
    s_acc = (synth_metrics["TP"] + synth_metrics["TN"]) / s_tot if s_tot > 0 else 0.0
    
    print("\nSUBSET BREAKDOWN:")
    print(f"Independently Human-Reviewed Subset (N={h_tot}):")
    print(f"  Accuracy:  {h_acc * 100:.2f}% | Precision: {h_prec * 100:.2f}% | Recall: {h_rec * 100:.2f}%")
    print(f"Synthetic Expansion Subset (N={s_tot}):")
    print(f"  Accuracy:  {s_acc * 100:.2f}%")
    
    print("\nPER-TRADE ACCURACY BREAKDOWN:")
    for occ, m in sorted(trade_metrics.items()):
        t_acc = (m["TP"] + m["TN"]) / m["total"] * 100
        print(f"  {occ}: Accuracy {t_acc:.1f}% (TP={m['TP']}, TN={m['TN']}, FP={m['FP']}, FN={m['FN']})")
        
    print(f"\nSaved detailed evaluation dataset to: {out_csv.resolve()}")

if __name__ == "__main__":
    main()

