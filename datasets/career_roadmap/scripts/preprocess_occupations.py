"""
Preprocessing script for Career Roadmap Occupations.
Unifies ESCO, O*NET, and NQR standards into a multi-domain occupation registry.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parents[3]
RAW_DIR = BASE_DIR / "datasets" / "career_roadmap" / "raw"
PROCESSED_DIR = BASE_DIR / "datasets" / "career_roadmap" / "processed"
METADATA_DIR = BASE_DIR / "datasets" / "career_roadmap" / "metadata"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def build_unified_occupations():
    unified: Dict[str, Dict[str, Any]] = {}

    # 1. Load ESCO profiles if available
    esco_profiles_path = BASE_DIR / "datasets" / "skill_gap" / "processed" / "esco" / "occupation_skill_profiles.json"
    if esco_profiles_path.exists():
        with open(esco_profiles_path, "r", encoding="utf-8") as f:
            esco_data = json.load(f)
            for title, info in esco_data.items():
                norm_key = title.strip().lower()
                unified[norm_key] = {
                    "canonical_title": title,
                    "domain": "ESCO v1.1.1",
                    "source_id": info.get("concept_uri", ""),
                    "description": info.get("description", ""),
                    "essential_skills": info.get("essential_skills", []),
                    "optional_skills": info.get("optional_skills", []),
                    "category": "Standard International Occupation"
                }

    # 2. Enrich/Override with Target Core Benchmark Occupations
    core_benchmarks = [
        {
            "canonical_title": "AI Engineer",
            "aliases": ["machine learning engineer", "ml engineer", "ai/ml engineer", "artificial intelligence engineer"],
            "domain": "Information Technology / AI",
            "source_id": "ESCO:2512.1.18 / ONET:15-1252.00",
            "description": "Architects, implements, fine-tunes, and deploys deep learning models, LLMs, and intelligent automation systems into scalable production environments.",
            "essential_skills": [
                "Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow",
                "Large Language Models", "RAG", "Natural Language Processing",
                "Computer Vision", "FastAPI", "Docker", "Git"
            ],
            "optional_skills": ["Kubernetes", "MLOps", "CUDA", "C++", "Vector Databases", "LangChain"]
        },
        {
            "canonical_title": "Data Scientist",
            "aliases": ["data science specialist", "applied scientist", "statistical data analyst"],
            "domain": "Information Technology / Data Science",
            "source_id": "ESCO:2511.1.4 / ONET:15-2051.00",
            "description": "Applies statistical modeling, machine learning, data mining, and predictive analytics to solve complex business and engineering problems.",
            "essential_skills": [
                "Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Machine Learning",
                "Data Analysis", "Statistics", "Data Visualization", "Git"
            ],
            "optional_skills": ["PyTorch", "Tableau", "BigQuery", "A/B Testing", "Feature Engineering"]
        },
        {
            "canonical_title": "Backend Developer",
            "aliases": ["backend engineer", "server-side developer", "api engineer", "python backend engineer"],
            "domain": "Software Engineering",
            "source_id": "ESCO:2512.1.3 / ONET:15-1252.00",
            "description": "Builds robust server-side applications, REST/GraphQL APIs, microservices architectures, and database persistence layers.",
            "essential_skills": [
                "Python", "FastAPI", "Flask", "Node.js", "SQL", "PostgreSQL",
                "REST APIs", "Docker", "Git", "GitHub", "Postman"
            ],
            "optional_skills": ["Redis", "Celery", "Kafka", "Microservices", "CI/CD", "Linux", "PyTest"]
        },
        {
            "canonical_title": "Software Developer",
            "aliases": ["software engineer", "full stack developer", "full stack engineer", "application developer"],
            "domain": "Software Engineering",
            "source_id": "ESCO:2512.1.1 / ONET:15-1252.00",
            "description": "Designs, develops, tests, and deploys scalable web applications, integrating responsive frontend interfaces with high-performance backend systems.",
            "essential_skills": [
                "Python", "JavaScript", "React.js", "Node.js", "HTML", "CSS",
                "SQL", "Git", "GitHub", "REST APIs", "Docker"
            ],
            "optional_skills": ["TypeScript", "Next.js", "Tailwind CSS", "Redux", "PostgreSQL", "C++"]
        },
        {
            "canonical_title": "Apparel Quality Assurance Specialist (Export Standard)",
            "aliases": [
                "apparel quality assurance specialist", "apparel qa specialist",
                "garment quality controller", "textile quality assurance manager",
                "apparel export quality inspector", "apparel quality controller"
            ],
            "domain": "Apparel & Textile Manufacturing / Export",
            "source_id": "NQR:AMH/Q0101 / ESCO:7531.1.4 / ONET:51-6092.00",
            "description": "Oversees comprehensive quality control and assurance in apparel manufacturing and export operations, enforcing AQL 2.5 statistical sampling, fabric defect grading (4-point system), garment construction standards, lab testing, and international compliance.",
            "essential_skills": [
                "Garment Inspection", "Fabric Grading & 4-Point System", "AQL 2.5 Sampling Standards",
                "Apparel Export Documentation", "Stitch & Seam Quality Analysis",
                "Textile Lab Testing (Shrinkage & Colorfastness)", "Quality Management Systems (QMS)",
                "Buyer Compliance & Audit Protocols"
            ],
            "optional_skills": [
                "Pattern Making & Tech Pack Review", "Industrial Engineering (SAM/SMV)",
                "Lean Manufacturing (5S & Kaizen)", "ERP for Apparel", "Environmental Safety & Sedex"
            ]
        }
    ]

    for bench in core_benchmarks:
        title = bench["canonical_title"]
        norm_key = title.strip().lower()
        unified[norm_key] = {
            "canonical_title": title,
            "domain": bench["domain"],
            "source_id": bench["source_id"],
            "description": bench["description"],
            "essential_skills": bench["essential_skills"],
            "optional_skills": bench["optional_skills"],
            "aliases": bench.get("aliases", []),
            "category": "Core Benchmark Occupation"
        }
        for alias in bench.get("aliases", []):
            alias_key = alias.strip().lower()
            if alias_key not in unified:
                unified[alias_key] = {
                    "canonical_title": title,
                    "is_alias": True,
                    "target_canonical_key": norm_key
                }

    out_file = PROCESSED_DIR / "unified_occupations.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(unified, f, indent=2)

    print(f"[SUCCESS] Processed {len(unified)} occupation entries into {out_file}")


if __name__ == "__main__":
    build_unified_occupations()
