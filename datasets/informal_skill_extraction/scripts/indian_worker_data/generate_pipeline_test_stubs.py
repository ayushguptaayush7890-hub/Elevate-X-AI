"""
Generate Multi-Span Synthetic Pipeline Test Stubs for Dataset 4
Strictly for testing validation scripts, offset computation, and schema conformance.
ALL records are explicitly tagged source_type: "synthetic_test_stub" and consent_status: "confirmed_dpdp_exempt_synthetic".
NEVER to be used as real-world training data.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_SYNTHETIC_DIR = BASE_DIR / "raw" / "indian_worker_data" / "synthetic_test_only"
INTERIM_DIR = BASE_DIR / "interim" / "indian_worker_data"

RAW_SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

# 20 realistic test stubs covering all 10 trades, Hindi, Hinglish, and English
STUBS_DATA = [
    # 1. Tailor - Hinglish
    {
        "record_id": "IND-TLR-0001",
        "worker_id": "STUB-TLR-01",
        "occupation_id": "TRD-01",
        "occupation": "Tailor and Garment Worker",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 8.0,
        "work_context": "independent_repair_shop",
        "worker_description": "Main single needle machine par pant shirt ki silai karta hu aur overlock se kinari band karta hu.",
        "spans": [
            {
                "extracted_skill": "single needle machine par pant shirt ki silai karta hu",
                "skill_category": "tool_operation",
                "canonical_skill": "Single-Needle Lockstitch Garment Assembly",
                "alternative_skill_names": ["silai machine operation", "pant shirt stitching"],
                "esco_uri": "http://data.europa.eu/esco/skill/08d51185-df0e-4360-aee8-2a210f968be8",
                "onet_soc_code": "51-6052.00",
                "nsqf_reference": "AMH/Q1947:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "overlock se kinari band karta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Overlock Seam Edging and Finishing",
                "alternative_skill_names": ["overlock stitching", "edge overcasting"],
                "esco_uri": "http://data.europa.eu/esco/skill/901726a8-bf64-469d-8c4d-a9914c62bca8",
                "onet_soc_code": "51-6052.00",
                "nsqf_reference": "AMH/Q1947:NOS-102",
                "confidence_score": 0.95,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Pilot tailoring test stub in colloquial Hinglish",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 2. Tailor - Hindi (Devanagari)
    {
        "record_id": "IND-TLR-0002",
        "worker_id": "STUB-TLR-02",
        "occupation_id": "TRD-01",
        "occupation": "Tailor and Garment Worker",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 14.0,
        "work_context": "micro_workshop",
        "worker_description": "मैं ग्राहक का नाप लेकर कपड़े की कटिंग करता हूँ और कॉलर में बकरम चिपका कर सिलाई करता हूँ।",
        "spans": [
            {
                "extracted_skill": "ग्राहक का नाप लेकर कपड़े की कटिंग करता हूँ",
                "skill_category": "measurement_planning",
                "canonical_skill": "Garment Pattern Measurement and Fabric Cutting",
                "alternative_skill_names": ["कपड़ा नापना", "कटिंग करना"],
                "esco_uri": "http://data.europa.eu/esco/skill/56c702b8-9ee2-402f-b4ec-86f3ea833a69",
                "onet_soc_code": "51-6052.00",
                "nsqf_reference": "AMH/Q1947:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "कॉलर में बकरम चिपका कर सिलाई करता हूँ",
                "skill_category": "technical_tactile",
                "canonical_skill": "Fusible Interlining Application and Collar Stitching",
                "alternative_skill_names": ["बकरम चिपकाना", "कॉलर सिलाई"],
                "esco_uri": "http://data.europa.eu/esco/skill/08d51185-df0e-4360-aee8-2a210f968be8",
                "onet_soc_code": "51-6052.00",
                "nsqf_reference": "AMH/Q1947:NOS-102",
                "confidence_score": 0.96,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Devanagari tailoring test stub with fusible canvas interlining",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 3. Electrician - Hinglish
    {
        "record_id": "IND-ELE-0001",
        "worker_id": "STUB-ELE-01",
        "occupation_id": "TRD-02",
        "occupation": "Electrician",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 6.0,
        "work_context": "customer_site",
        "worker_description": "Main deewar mein jhirri kaat kar PVC conduit daalta hu aur multimeter se neutral-phase check karta hu.",
        "spans": [
            {
                "extracted_skill": "deewar mein jhirri kaat kar PVC conduit daalta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Concealed Wall Conduit Chasing and Installation",
                "alternative_skill_names": ["jhirri kaatna", "PVC pipe conduit installation"],
                "esco_uri": "http://data.europa.eu/esco/skill/3d3d82d9-e932-430b-9df0-e3ebc707db9e",
                "onet_soc_code": "47-2111.00",
                "nsqf_reference": "ELE/Q3104:NOS-201",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "multimeter se neutral-phase check karta hu",
                "skill_category": "troubleshooting_repair",
                "canonical_skill": "Multimeter Phase and Neutral Voltage Diagnostics",
                "alternative_skill_names": ["phase check karna", "voltage testing"],
                "esco_uri": "http://data.europa.eu/esco/skill/a638bfe4-7d5b-4fa8-9585-e7f09700eb87",
                "onet_soc_code": "47-2111.00",
                "nsqf_reference": "ELE/Q3104:NOS-202",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Concealed conduit and multimeter diagnostic",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 4. Electrician - Hindi
    {
        "record_id": "IND-ELE-0002",
        "worker_id": "STUB-ELE-02",
        "occupation_id": "TRD-02",
        "occupation": "Electrician",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 10.0,
        "work_context": "independent_repair_shop",
        "worker_description": "हम मेन एमसीबी बॉक्स की वायरिंग करते हैं और इन्वर्टर बैटरी का कनेक्शन जोड़ते हैं।",
        "spans": [
            {
                "extracted_skill": "मेन एमसीबी बॉक्स की वायरिंग करते हैं",
                "skill_category": "technical_tactile",
                "canonical_skill": "Miniature Circuit Breaker (MCB) Distribution Board Wiring",
                "alternative_skill_names": ["MCB wiring", "distribution panel setup"],
                "esco_uri": "http://data.europa.eu/esco/skill/3d3d82d9-e932-430b-9df0-e3ebc707db9e",
                "onet_soc_code": "47-2111.00",
                "nsqf_reference": "ELE/Q3104:NOS-201",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "इन्वर्टर बैटरी का कनेक्शन जोड़ते हैं",
                "skill_category": "tool_operation",
                "canonical_skill": "Power Inverter and Backup Battery Installation",
                "alternative_skill_names": ["inverter fitting", "battery connection"],
                "esco_uri": "http://data.europa.eu/esco/skill/a638bfe4-7d5b-4fa8-9585-e7f09700eb87",
                "onet_soc_code": "47-2111.00",
                "nsqf_reference": "ELE/Q3104:NOS-203",
                "confidence_score": 0.96,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "MCB box and inverter connection in Devanagari",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 5. Plumber - Hinglish
    {
        "record_id": "IND-PLM-0001",
        "worker_id": "STUB-PLM-01",
        "occupation_id": "TRD-03",
        "occupation": "Plumber",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 9.0,
        "work_context": "customer_site",
        "worker_description": "Main CPVC pipe mein solvent lagakar fitting karta hu aur GI pipe par die se chudi kaatta hu.",
        "spans": [
            {
                "extracted_skill": "CPVC pipe mein solvent lagakar fitting karta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "CPVC Pipe Solvent Cement Jointing",
                "alternative_skill_names": ["CPVC jointing", "solvent fitting"],
                "esco_uri": "http://data.europa.eu/esco/skill/b5e28a52-c80f-48d6-9430-c3dcfdcfda98",
                "onet_soc_code": "47-2152.00",
                "nsqf_reference": "PSC/Q0104:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "GI pipe par die se chudi kaatta hu",
                "skill_category": "tool_operation",
                "canonical_skill": "Galvanized Iron Pipe Manual Die Threading",
                "alternative_skill_names": ["GI chudi kaatna", "pipe threading"],
                "esco_uri": "http://data.europa.eu/esco/skill/e3223ca8-7fba-4f2d-b108-e71e72f9fafe",
                "onet_soc_code": "47-2152.00",
                "nsqf_reference": "PSC/Q0104:NOS-102",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Plumbing CPVC solvent and GI threading",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 6. Plumber - English
    {
        "record_id": "IND-PLM-0002",
        "worker_id": "STUB-PLM-02",
        "occupation_id": "TRD-03",
        "occupation": "Plumber",
        "secondary_occupations": [],
        "original_language": "english",
        "script_type": "latin",
        "experience_years": 5.0,
        "work_context": "customer_site",
        "worker_description": "I install concealed wall diverters and test flush cistern float valves for water leaks.",
        "spans": [
            {
                "extracted_skill": "install concealed wall diverters",
                "skill_category": "technical_tactile",
                "canonical_skill": "Concealed Wall Diverter Installation",
                "alternative_skill_names": ["diverter fitting", "wall mixer mounting"],
                "esco_uri": "http://data.europa.eu/esco/skill/b5e28a52-c80f-48d6-9430-c3dcfdcfda98",
                "onet_soc_code": "47-2152.00",
                "nsqf_reference": "PSC/Q0104:NOS-101",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "test flush cistern float valves for water leaks",
                "skill_category": "troubleshooting_repair",
                "canonical_skill": "Flush Cistern Float Valve Inspection and Leak Testing",
                "alternative_skill_names": ["float valve repair", "leak detection"],
                "esco_uri": "http://data.europa.eu/esco/skill/e3223ca8-7fba-4f2d-b108-e71e72f9fafe",
                "onet_soc_code": "47-2152.00",
                "nsqf_reference": "PSC/Q0104:NOS-103",
                "confidence_score": 0.95,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "English trade description for sanitary fixture",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 7. Motor Mechanic - Hinglish
    {
        "record_id": "IND-MEC-0001",
        "worker_id": "STUB-MEC-01",
        "occupation_id": "TRD-04",
        "occupation": "Motor Mechanic",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 11.0,
        "work_context": "independent_repair_shop",
        "worker_description": "Main bike ka engine oil change karta hu aur feeler gauge se tappet setting karta hu.",
        "spans": [
            {
                "extracted_skill": "bike ka engine oil change karta hu",
                "skill_category": "tool_operation",
                "canonical_skill": "Motorcycle Engine Oil Drain and Replacement",
                "alternative_skill_names": ["oil change", "engine service"],
                "esco_uri": "http://data.europa.eu/esco/skill/ea444455-beee-4367-9aa8-f58473e6ab18",
                "onet_soc_code": "49-3023.00",
                "nsqf_reference": "ASC/Q1411:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "feeler gauge se tappet setting karta hu",
                "skill_category": "quality_inspection",
                "canonical_skill": "Engine Valve Tappet Clearance Calibration",
                "alternative_skill_names": ["tappet setting", "valve clearance adjust"],
                "esco_uri": "http://data.europa.eu/esco/skill/96253c55-6b83-4a12-87f5-201ea1815e45",
                "onet_soc_code": "49-3023.00",
                "nsqf_reference": "ASC/Q1411:NOS-102",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Two-wheeler engine service and valve clearance",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 8. Motor Mechanic - Hindi
    {
        "record_id": "IND-MEC-0002",
        "worker_id": "STUB-MEC-02",
        "occupation_id": "TRD-04",
        "occupation": "Motor Mechanic",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 7.0,
        "work_context": "service_center",
        "worker_description": "हम डिस्क ब्रेक की कैलीपर से पुराना ब्रेक ऑयल ब्लीड करते हैं और क्लच प्लेट रिप्लेस करते हैं।",
        "spans": [
            {
                "extracted_skill": "डिस्क ब्रेक की कैलीपर से पुराना ब्रेक ऑयल ब्लीड करते हैं",
                "skill_category": "troubleshooting_repair",
                "canonical_skill": "Hydraulic Disc Brake Caliper Fluid Bleeding",
                "alternative_skill_names": ["brake bleeding", "brake oil replace"],
                "esco_uri": "http://data.europa.eu/esco/skill/ea444455-beee-4367-9aa8-f58473e6ab18",
                "onet_soc_code": "49-3023.00",
                "nsqf_reference": "ASC/Q1402:NOS-101",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "क्लच प्लेट रिप्लेस करते हैं",
                "skill_category": "technical_tactile",
                "canonical_skill": "Clutch Friction Plate Disassembly and Replacement",
                "alternative_skill_names": ["clutch plate badalna", "clutch overhaul"],
                "esco_uri": "http://data.europa.eu/esco/skill/96253c55-6b83-4a12-87f5-201ea1815e45",
                "onet_soc_code": "49-3023.00",
                "nsqf_reference": "ASC/Q1402:NOS-102",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Automotive brake fluid bleed and clutch plate",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 9. Carpenter - Hinglish
    {
        "record_id": "IND-CRP-0001",
        "worker_id": "STUB-CRP-01",
        "occupation_id": "TRD-05",
        "occupation": "Carpenter",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 12.0,
        "work_context": "micro_workshop",
        "worker_description": "Main circular saw se plywood kaatta hu aur fevicol lagakar sunmica press karta hu.",
        "spans": [
            {
                "extracted_skill": "circular saw se plywood kaatta hu",
                "skill_category": "tool_operation",
                "canonical_skill": "Circular Saw Plywood Panel Sizing",
                "alternative_skill_names": ["circular saw cutting", "plywood sizing"],
                "esco_uri": "http://data.europa.eu/esco/skill/a83fa741-9c60-4416-86f1-a1d2931db26e",
                "onet_soc_code": "47-2031.00",
                "nsqf_reference": "FFS/Q0103:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "fevicol lagakar sunmica press karta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Adhesive Application and Laminate Sheet Pressing",
                "alternative_skill_names": ["sunmica pasting", "laminate bonding"],
                "esco_uri": "http://data.europa.eu/esco/skill/474c10a4-e7fa-42f0-a29d-439ea8ba0784",
                "onet_soc_code": "47-2031.00",
                "nsqf_reference": "FFS/Q0103:NOS-102",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Woodwork circular saw and laminate bonding",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 10. Carpenter - Hindi
    {
        "record_id": "IND-CRP-0002",
        "worker_id": "STUB-CRP-02",
        "occupation_id": "TRD-05",
        "occupation": "Carpenter",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 16.0,
        "work_context": "independent_repair_shop",
        "worker_description": "हम हाथ का रंदा चलाकर लकड़ी को समतल करते हैं और चौरसी से साल-कब्जा जोड़ बनाते हैं।",
        "spans": [
            {
                "extracted_skill": "हाथ का रंदा चलाकर लकड़ी को समतल करते हैं",
                "skill_category": "tool_operation",
                "canonical_skill": "Manual Wood Surface Planing and Smoothing",
                "alternative_skill_names": ["रंदा चलाना", "लकड़ी समतल करना"],
                "esco_uri": "http://data.europa.eu/esco/skill/a83fa741-9c60-4416-86f1-a1d2931db26e",
                "onet_soc_code": "47-2031.00",
                "nsqf_reference": "FFS/Q0103:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "चौरसी से साल-कब्जा जोड़ बनाते हैं",
                "skill_category": "technical_tactile",
                "canonical_skill": "Wood Chisel Mortise and Tenon Joinery",
                "alternative_skill_names": ["साल कब्जा बनाना", "chisel joinery"],
                "esco_uri": "http://data.europa.eu/esco/skill/474c10a4-e7fa-42f0-a29d-439ea8ba0784",
                "onet_soc_code": "47-2031.00",
                "nsqf_reference": "FFS/Q0103:NOS-103",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Hand planer and mortise-tenon joinery",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 11. Welder - Hinglish
    {
        "record_id": "IND-WLD-0001",
        "worker_id": "STUB-WLD-01",
        "occupation_id": "TRD-06",
        "occupation": "Welder",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 8.0,
        "work_context": "industrial_cluster",
        "worker_description": "Main 6013 rod se arc welding karta hu aur chipping hammer se weld slag nikalta hu.",
        "spans": [
            {
                "extracted_skill": "6013 rod se arc welding karta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Shielded Metal Arc Welding with E6013 Electrodes",
                "alternative_skill_names": ["arc welding", "rod welding"],
                "esco_uri": "http://data.europa.eu/esco/skill/85aa0e37-f4e3-4710-91fc-1b776c5f7881",
                "onet_soc_code": "51-4121.00",
                "nsqf_reference": "CSC/Q0204:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "chipping hammer se weld slag nikalta hu",
                "skill_category": "quality_inspection",
                "canonical_skill": "Weld Slag Removal and Bead Cleaning",
                "alternative_skill_names": ["slag chipping", "weld cleaning"],
                "esco_uri": "http://data.europa.eu/esco/skill/901726a8-bf64-469d-8c4d-a9914c62bca8",
                "onet_soc_code": "51-4121.00",
                "nsqf_reference": "CSC/Q0204:NOS-102",
                "confidence_score": 0.96,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Arc welding and slag removal in fabrication shed",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 12. Welder - English
    {
        "record_id": "IND-WLD-0002",
        "worker_id": "STUB-WLD-02",
        "occupation_id": "TRD-06",
        "occupation": "Welder",
        "secondary_occupations": [],
        "original_language": "english",
        "script_type": "latin",
        "experience_years": 10.0,
        "work_context": "industrial_cluster",
        "worker_description": "I prepare V-groove edge beveling using angle grinder and cut steel plates with oxy-acetylene torch.",
        "spans": [
            {
                "extracted_skill": "prepare V-groove edge beveling using angle grinder",
                "skill_category": "tool_operation",
                "canonical_skill": "Angle Grinder V-Groove Edge Beveling",
                "alternative_skill_names": ["edge grinding", "weld beveling"],
                "esco_uri": "http://data.europa.eu/esco/skill/85aa0e37-f4e3-4710-91fc-1b776c5f7881",
                "onet_soc_code": "51-4121.00",
                "nsqf_reference": "CSC/Q0204:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "cut steel plates with oxy-acetylene torch",
                "skill_category": "tool_operation",
                "canonical_skill": "Oxy-Acetylene Thermal Gas Cutting",
                "alternative_skill_names": ["gas cutting", "flame cutting"],
                "esco_uri": "http://data.europa.eu/esco/skill/503d5272-944d-44a6-9ae2-cb729b1beee4",
                "onet_soc_code": "51-4121.00",
                "nsqf_reference": "CSC/Q0204:NOS-103",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Edge preparation and oxy-fuel gas cutting",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 13. Mason - Hinglish
    {
        "record_id": "IND-MSN-0001",
        "worker_id": "STUB-MSN-01",
        "occupation_id": "TRD-07",
        "occupation": "Mason / Raj Mistri",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 15.0,
        "work_context": "construction_site",
        "worker_description": "Main sahul lagakar deewar ki seedh dekhta hu aur 1:4 cement masala banakar chunai karta hu.",
        "spans": [
            {
                "extracted_skill": "sahul lagakar deewar ki seedh dekhta hu",
                "skill_category": "quality_inspection",
                "canonical_skill": "Plumb Bob Vertical Alignment Verification",
                "alternative_skill_names": ["sahul lagana", "plumbing a wall"],
                "esco_uri": "http://data.europa.eu/esco/skill/3035f299-4458-45ec-9f5b-6f0a67cf4798",
                "onet_soc_code": "47-2061.00",
                "nsqf_reference": "CON/Q0103:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "1:4 cement masala banakar chunai karta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Bricklaying in 1:4 Cement Sand Mortar",
                "alternative_skill_names": ["masala banana", "chunai karna"],
                "esco_uri": "http://data.europa.eu/esco/skill/065b2169-d419-4e78-98f5-30ad8a5fa689",
                "onet_soc_code": "47-2061.00",
                "nsqf_reference": "CON/Q0103:NOS-102",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Plumb bob leveling and bricklaying in construction",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 14. Mason - Hindi
    {
        "record_id": "IND-MSN-0002",
        "worker_id": "STUB-MSN-02",
        "occupation_id": "TRD-07",
        "occupation": "Mason / Raj Mistri",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 20.0,
        "work_context": "construction_site",
        "worker_description": "हम वाटर लेवल पाइप से चारों कोनों का लेवल मिलाते हैं और गुरमाले से दीवार पर प्लास्टर चढ़ाते हैं।",
        "spans": [
            {
                "extracted_skill": "वाटर लेवल पाइप से चारों कोनों का लेवल मिलाते हैं",
                "skill_category": "measurement_planning",
                "canonical_skill": "Clear Water Tube Horizontal Leveling",
                "alternative_skill_names": ["water level nikalna", "horizontal alignment"],
                "esco_uri": "http://data.europa.eu/esco/skill/3035f299-4458-45ec-9f5b-6f0a67cf4798",
                "onet_soc_code": "47-2061.00",
                "nsqf_reference": "CON/Q0103:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "गुरमाले से दीवार पर प्लास्टर चढ़ाते हैं",
                "skill_category": "technical_tactile",
                "canonical_skill": "Wooden Float Cement Plaster Application",
                "alternative_skill_names": ["gurmala chalana", "plaster karna"],
                "esco_uri": "http://data.europa.eu/esco/skill/065b2169-d419-4e78-98f5-30ad8a5fa689",
                "onet_soc_code": "47-2061.00",
                "nsqf_reference": "CON/Q0103:NOS-103",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Water tube leveling and plaster float",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 15. Painter - Hinglish
    {
        "record_id": "IND-PNT-0001",
        "worker_id": "STUB-PNT-01",
        "occupation_id": "TRD-08",
        "occupation": "Painter",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 6.0,
        "work_context": "customer_site",
        "worker_description": "Main patti se double coat putty kheenchtahu aur regmar maarkar primer lagata hu.",
        "spans": [
            {
                "extracted_skill": "patti se double coat putty kheenchtahu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Blade Application of Double Coat Wall Putty",
                "alternative_skill_names": ["putty kheenchna", "putty application"],
                "esco_uri": "http://data.europa.eu/esco/skill/107a637f-eb6a-4ee1-b755-f7169fef89e2",
                "onet_soc_code": "47-2141.00",
                "nsqf_reference": "CON/Q0501:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "regmar maarkar primer lagata hu",
                "skill_category": "tool_operation",
                "canonical_skill": "Abrasive Sanding and Wall Primer Sealing",
                "alternative_skill_names": ["regmar maarna", "primer coating"],
                "esco_uri": "http://data.europa.eu/esco/skill/6ffea371-678a-4d33-bcbe-8e01bb285ec5",
                "onet_soc_code": "47-2141.00",
                "nsqf_reference": "CON/Q0501:NOS-102",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Putty blade and sandpaper primer application",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 16. Painter - English
    {
        "record_id": "IND-PNT-0002",
        "worker_id": "STUB-PNT-02",
        "occupation_id": "TRD-08",
        "occupation": "Painter",
        "secondary_occupations": [],
        "original_language": "english",
        "script_type": "latin",
        "experience_years": 8.0,
        "work_context": "customer_site",
        "worker_description": "I apply acrylic exterior emulsion with roller and coat damp surfaces with waterproofing solution.",
        "spans": [
            {
                "extracted_skill": "apply acrylic exterior emulsion with roller",
                "skill_category": "tool_operation",
                "canonical_skill": "Roller Application of Exterior Acrylic Emulsion",
                "alternative_skill_names": ["roller painting", "emulsion rolling"],
                "esco_uri": "http://data.europa.eu/esco/skill/107a637f-eb6a-4ee1-b755-f7169fef89e2",
                "onet_soc_code": "47-2141.00",
                "nsqf_reference": "CON/Q0501:NOS-102",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "coat damp surfaces with waterproofing solution",
                "skill_category": "technical_tactile",
                "canonical_skill": "Damp-Proof Waterproof Barrier Coating",
                "alternative_skill_names": ["waterproofing coat", "dampproofing"],
                "esco_uri": "http://data.europa.eu/esco/skill/6ffea371-678a-4d33-bcbe-8e01bb285ec5",
                "onet_soc_code": "47-2141.00",
                "nsqf_reference": "CON/Q0501:NOS-103",
                "confidence_score": 0.96,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Exterior emulsion roller and waterproofing",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 17. Agriculture - Hinglish
    {
        "record_id": "IND-AGR-0001",
        "worker_id": "STUB-AGR-01",
        "occupation_id": "TRD-09",
        "occupation": "Agriculture and Irrigation Worker",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 10.0,
        "work_context": "agricultural_field",
        "worker_description": "Main drip irrigation ki lateral pipe bichhata hu aur venturi se khad paani chalata hu.",
        "spans": [
            {
                "extracted_skill": "drip irrigation ki lateral pipe bichhata hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Micro-Irrigation Drip Lateral Pipe Layout",
                "alternative_skill_names": ["drip line laying", "pipe installation"],
                "esco_uri": "http://data.europa.eu/esco/skill/42435b86-fb12-4217-b6f1-a1d2931db26e",
                "onet_soc_code": "45-2092.00",
                "nsqf_reference": "AGR/Q1002:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "venturi se khad paani chalata hu",
                "skill_category": "tool_operation",
                "canonical_skill": "Venturi Fertigation Fertilizer Dosing Calibration",
                "alternative_skill_names": ["venturi operation", "fertigation dosing"],
                "esco_uri": "http://data.europa.eu/esco/skill/14109407-7d63-455b-80a5-f865ee1dfcb1",
                "onet_soc_code": "45-2092.00",
                "nsqf_reference": "AGR/Q1002:NOS-102",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Drip irrigation pipe layout and venturi dosing",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 18. Agriculture - Hindi
    {
        "record_id": "IND-AGR-0002",
        "worker_id": "STUB-AGR-02",
        "occupation_id": "TRD-09",
        "occupation": "Agriculture and Irrigation Worker",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 14.0,
        "work_context": "agricultural_field",
        "worker_description": "हम बोरवेल मोटर चालू करके डिस्क फिल्टर को धोकर साफ करते हैं और ट्रैक्टर पर रोटावेटर जोड़ते हैं।",
        "spans": [
            {
                "extracted_skill": "डिस्क फिल्टर को धोकर साफ करते हैं",
                "skill_category": "troubleshooting_repair",
                "canonical_skill": "Irrigation Disc Filter Flushing and Cleaning",
                "alternative_skill_names": ["filter dhona", "filter backwash"],
                "esco_uri": "http://data.europa.eu/esco/skill/42435b86-fb12-4217-b6f1-a1d2931db26e",
                "onet_soc_code": "45-2092.00",
                "nsqf_reference": "AGR/Q1002:NOS-102",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "ट्रैक्टर पर रोटावेटर जोड़ते हैं",
                "skill_category": "tool_operation",
                "canonical_skill": "Tractor Three-Point Hitch Rotavator Coupling",
                "alternative_skill_names": ["rotavator jorna", "tractor implement hitching"],
                "esco_uri": "http://data.europa.eu/esco/skill/14109407-7d63-455b-80a5-f865ee1dfcb1",
                "onet_soc_code": "45-2092.00",
                "nsqf_reference": "AGR/Q1101:NOS-201",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Disc filter maintenance and tractor implement hitching",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 19. Mobile Repair - Hinglish
    {
        "record_id": "IND-MOB-0001",
        "worker_id": "STUB-MOB-01",
        "occupation_id": "TRD-10",
        "occupation": "Mobile Repair Technician",
        "secondary_occupations": [],
        "original_language": "hinglish",
        "script_type": "latin",
        "experience_years": 5.0,
        "work_context": "service_center",
        "worker_description": "Main SMD blower se charging port nikal kar naya CC pin solder karta hu aur jumper maarta hu.",
        "spans": [
            {
                "extracted_skill": "SMD blower se charging port nikal kar naya CC pin solder karta hu",
                "skill_category": "tool_operation",
                "canonical_skill": "SMD Hot Air Desoldering and USB Port Micro-Soldering",
                "alternative_skill_names": ["CC pin badalna", "charging jack soldering"],
                "esco_uri": "http://data.europa.eu/esco/skill/8f220311-bf12-4217-b6f1-a1d2931db26e",
                "onet_soc_code": "49-2022.00",
                "nsqf_reference": "ELE/Q8104:NOS-101",
                "confidence_score": 0.99,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "jumper maarta hu",
                "skill_category": "technical_tactile",
                "canonical_skill": "Micro-Wire PCB Track Jumper Bypass",
                "alternative_skill_names": ["jumper wire soldering", "track bypass"],
                "esco_uri": "http://data.europa.eu/esco/skill/96253c55-6b83-4a12-87f5-201ea1815e45",
                "onet_soc_code": "49-2022.00",
                "nsqf_reference": "ELE/Q8104:NOS-102",
                "confidence_score": 0.96,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Mobile hardware charging jack and PCB jumper bypass",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    },
    # 20. Mobile Repair - Hindi
    {
        "record_id": "IND-MOB-0002",
        "worker_id": "STUB-MOB-02",
        "occupation_id": "TRD-10",
        "occupation": "Mobile Repair Technician",
        "secondary_occupations": [],
        "original_language": "hindi",
        "script_type": "devanagari",
        "experience_years": 7.0,
        "work_context": "independent_repair_shop",
        "worker_description": "हम हीटिंग पैड पर फोल्डर अलग करते हैं और डीसी सप्लाई से मदरबोर्ड की शॉर्टिंग निकालते हैं।",
        "spans": [
            {
                "extracted_skill": "हीटिंग पैड पर फोल्डर अलग करते हैं",
                "skill_category": "tool_operation",
                "canonical_skill": "Touchscreen Display Folder Thermal Separation",
                "alternative_skill_names": ["folder alag karna", "display disassembly"],
                "esco_uri": "http://data.europa.eu/esco/skill/8f220311-bf12-4217-b6f1-a1d2931db26e",
                "onet_soc_code": "49-2022.00",
                "nsqf_reference": "ELE/Q8104:NOS-101",
                "confidence_score": 0.98,
                "is_unmapped_skill": False
            },
            {
                "extracted_skill": "डीसी सप्लाई से मदरबोर्ड की शॉर्टिंग निकालते हैं",
                "skill_category": "troubleshooting_repair",
                "canonical_skill": "DC Benchtop Power Supply Motherboard Short Circuit Diagnostics",
                "alternative_skill_names": ["shorting nikalna", "PCB leakage testing"],
                "esco_uri": "http://data.europa.eu/esco/skill/96253c55-6b83-4a12-87f5-201ea1815e45",
                "onet_soc_code": "49-2022.00",
                "nsqf_reference": "ELE/Q8104:NOS-103",
                "confidence_score": 0.97,
                "is_unmapped_skill": False
            }
        ],
        "ambiguity_flag": False,
        "notes": "Touch folder thermal separation and motherboard short diagnostics",
        "annotation_source": "synthetic_generator",
        "annotation_status": "reviewed",
        "source_type": "synthetic_test_stub",
        "source_reference": "elevate_x_synthetic_development_stub_v2",
        "annotator_id": "ANN-STUB-01",
        "reviewer_id": "REV-STUB-01",
        "reviewer_status": "approved",
        "consent_status": "confirmed_dpdp_exempt_synthetic"
    }
]

def generate_stubs():
    records = []
    print(f"Generating {len(STUBS_DATA)} multi-span synthetic test stubs...")
    
    for idx, item in enumerate(STUBS_DATA):
        text = item["worker_description"]
        skill_spans = []
        
        for s_idx, span_def in enumerate(item["spans"]):
            sub = span_def["extracted_skill"]
            start = text.find(sub)
            if start == -1:
                raise ValueError(f"Substring '{sub}' not found in record {item['record_id']}: '{text}'")
            end = start + len(sub)
            
            # Verify exact slice
            assert text[start:end] == sub, f"Slice mismatch in {item['record_id']}: '{text[start:end]}' != '{sub}'"
            
            span_obj = {
                "span_id": f"SP-{s_idx + 1:02d}",
                "extracted_skill": sub,
                "start_offset": start,
                "end_offset": end,
                "skill_category": span_def["skill_category"],
                "canonical_skill": span_def["canonical_skill"],
                "alternative_skill_names": span_def.get("alternative_skill_names", []),
                "esco_uri": span_def.get("esco_uri"),
                "onet_soc_code": span_def.get("onet_soc_code"),
                "nsqf_reference": span_def.get("nsqf_reference"),
                "confidence_score": span_def.get("confidence_score", 1.0),
                "mapping_status": "mapped" if (span_def.get("esco_uri") or span_def.get("nsqf_reference")) else "unmapped",
                "is_unmapped_skill": span_def.get("is_unmapped_skill", False)
            }
            skill_spans.append(span_obj)
            
        record = {
            "record_id": item["record_id"],
            "worker_id": item["worker_id"],
            "worker_description": text,
            "original_language": item["original_language"],
            "script_type": item["script_type"],
            "region": item.get("region", "Delhi NCR"),
            "occupation_id": item["occupation_id"],
            "occupation": item["occupation"],
            "secondary_occupations": item.get("secondary_occupations", []),
            "experience_years": item.get("experience_years"),
            "work_context": item.get("work_context", "independent_repair_shop"),
            "collection_date": item.get("collection_date", "2026-11-14"),
            "skill_spans": skill_spans,
            "ambiguity_flag": item.get("ambiguity_flag", False),
            "notes": item.get("notes"),
            "annotation_source": item["annotation_source"],
            "annotation_status": item["annotation_status"],
            "source_type": item["source_type"],
            "source_reference": item["source_reference"],
            "annotator_id": item.get("annotator_id"),
            "reviewer_id": item.get("reviewer_id"),
            "reviewer_status": item["reviewer_status"],
            "consent_status": item["consent_status"]
        }
        records.append(record)
        
    out_paths = [
        RAW_SYNTHETIC_DIR / "synthetic_pipeline_test.jsonl",
        INTERIM_DIR / "synthetic_pipeline_test.jsonl"
    ]
    
    for p in out_paths:
        with open(p, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"Saved {len(records)} verified records to {p}")

if __name__ == "__main__":
    generate_stubs()
