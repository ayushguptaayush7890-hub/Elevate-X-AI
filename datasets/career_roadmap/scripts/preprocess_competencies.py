"""
Preprocessing script for Career Roadmap Competencies & Prerequisite Tiers.
Builds tiered learning stages for occupations based on pedagogical progressions:
Tier 1: Foundations & Core Tooling
Tier 2: Applied Competencies & Architecture
Tier 3: Advanced Production, Testing & MLOps/Compliance
Tier 4: Capstone Portfolio, System Integration & Industry Readiness
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parents[3]
PROCESSED_DIR = BASE_DIR / "datasets" / "career_roadmap" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def build_competency_tiers():
    tiers_catalog: Dict[str, List[Dict[str, Any]]] = {
        "ai engineer": [
            {
                "stage_number": 1,
                "title": "Mathematical Foundations & Core Pythonic Engineering",
                "time_estimate": "3-4 Weeks",
                "description": "Establish deep fluency in vectorized scientific computing, automatic differentiation, clean code architecture, and foundational probability/linear algebra.",
                "skills_to_acquire": ["Python", "NumPy", "Pandas", "Git", "GitHub"],
                "practical_tasks": [
                    "Implement a fully vectorized multilayer perceptron from scratch in NumPy with backpropagation and mini-batch SGD.",
                    "Build automated unit tests verifying matrix gradient computation and numerical stability against edge cases."
                ],
                "resource_search_keys": ["Python", "NumPy", "Pandas", "Git"]
            },
            {
                "stage_number": 2,
                "title": "Deep Learning Architecture & Neural Frameworks",
                "time_estimate": "4-5 Weeks",
                "description": "Master neural network construction, training loop optimization, GPU tensor operations, and convolutional/transformer model architectures in PyTorch.",
                "skills_to_acquire": ["Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Computer Vision"],
                "practical_tasks": [
                    "Train a custom vision transformer / ResNet on custom image data with augmentations, learning rate warmup, and mixed precision.",
                    "Benchmark inference latency and VRAM footprint comparing PyTorch eager mode versus TorchScript / ONNX export."
                ],
                "resource_search_keys": ["PyTorch", "Deep Learning", "Machine Learning", "Computer Vision"]
            },
            {
                "stage_number": 3,
                "title": "Generative AI, Large Language Models & RAG Systems",
                "time_estimate": "4-5 Weeks",
                "description": "Engineer robust RAG (Retrieval-Augmented Generation) pipelines, chunking strategies, dense vector search, and instruction fine-tuning on domain corpora.",
                "skills_to_acquire": ["Large Language Models", "RAG", "Natural Language Processing", "NLP"],
                "practical_tasks": [
                    "Build an end-to-end multi-document RAG system with hybrid semantic retrieval, reranking, and citation verification.",
                    "Fine-tune a quantized instruction model using LoRA / QLoRA with structured evaluation on held-out benchmarks."
                ],
                "resource_search_keys": ["Generative AI", "Large Language Models", "RAG", "Natural Language Processing"]
            },
            {
                "stage_number": 4,
                "title": "Production Deployment, API Serving & Containerized MLOps",
                "time_estimate": "3-4 Weeks",
                "description": "Containerize model pipelines, build high-throughput async REST endpoints with FastAPI, and configure automated health and drift monitoring.",
                "skills_to_acquire": ["FastAPI", "Docker", "Postman", "C++", "SQL"],
                "practical_tasks": [
                    "Deploy an async FastAPI inference microservice wrapped in multi-stage Docker container with health probes and batching.",
                    "Execute load tests with Postman/k6 to verify latency SLAs under concurrent traffic."
                ],
                "resource_search_keys": ["FastAPI", "Docker", "Postman", "SQL"]
            }
        ],

        "data scientist": [
            {
                "stage_number": 1,
                "title": "Statistical Data Analysis & Python Data Stack",
                "time_estimate": "3-4 Weeks",
                "description": "Master data wrangling, exploratory data analysis, hypothesis testing, and statistical distributions using standard Python data science libraries.",
                "skills_to_acquire": ["Python", "Pandas", "NumPy", "Data Analysis", "Statistics"],
                "practical_tasks": [
                    "Conduct an in-depth exploratory data analysis on a multi-table relational dataset with missing value imputation and outlier detection.",
                    "Formulate and test statistical hypotheses using parametric and non-parametric statistical tests."
                ],
                "resource_search_keys": ["Python", "Pandas", "NumPy", "Data Analysis"]
            },
            {
                "stage_number": 2,
                "title": "Relational Querying & Database Analytics",
                "time_estimate": "3-4 Weeks",
                "description": "Write advanced SQL queries, window functions, CTEs, and schema aggregations to extract and transform enterprise analytics datasets.",
                "skills_to_acquire": ["SQL", "Data Visualization", "Git", "GitHub"],
                "practical_tasks": [
                    "Design and execute complex multi-join SQL queries with rolling window aggregates and partitioned analytical functions.",
                    "Build an automated data pipeline script to load raw transactional records into an analytical schema."
                ],
                "resource_search_keys": ["SQL", "PostgreSQL", "Git"]
            },
            {
                "stage_number": 3,
                "title": "Supervised & Unsupervised Machine Learning",
                "time_estimate": "4-5 Weeks",
                "description": "Train predictive classification, regression, and clustering pipelines using Scikit-Learn with rigorous cross-validation and hyperparameter tuning.",
                "skills_to_acquire": ["Machine Learning", "Scikit-Learn", "Feature Engineering"],
                "practical_tasks": [
                    "Build a reproducible Scikit-Learn pipeline with custom transformers, feature encoders, and ensemble tree models.",
                    "Evaluate model calibration, ROC-AUC, PR-AUC, and feature importance using SHAP values."
                ],
                "resource_search_keys": ["Machine Learning", "Scikit-learn", "Classification"]
            },
            {
                "stage_number": 4,
                "title": "Model Interpretation, Productionization & Business Storytelling",
                "time_estimate": "3-4 Weeks",
                "description": "Translate complex statistical findings into actionable business insights and deploy model prediction services.",
                "skills_to_acquire": ["PyTorch", "Docker", "FastAPI"],
                "practical_tasks": [
                    "Package trained predictive pipelines into containerized microservices with automated prediction verification.",
                    "Develop an interactive executive dashboard communicating key driver metrics and risk indicators."
                ],
                "resource_search_keys": ["Docker", "FastAPI", "Cloud Computing"]
            }
        ],

        "backend developer": [
            {
                "stage_number": 1,
                "title": "Core Server Languages & Relational Database Engineering",
                "time_estimate": "3-4 Weeks",
                "description": "Develop high-performance backend foundations, object-oriented/functional design, schema migrations, and indexing strategies.",
                "skills_to_acquire": ["Python", "SQL", "PostgreSQL", "Git", "GitHub"],
                "practical_tasks": [
                    "Design a normalized relational schema with foreign key constraints, indexes, and write migration scripts using Alembic.",
                    "Benchmark query execution plans using EXPLAIN ANALYZE to eliminate sequential table scans."
                ],
                "resource_search_keys": ["Python", "SQL", "PostgreSQL", "Git"]
            },
            {
                "stage_number": 2,
                "title": "RESTful API Architecture & Authentication",
                "time_estimate": "4-5 Weeks",
                "description": "Architect scalable REST APIs using FastAPI/Flask with Pydantic schemas, dependency injection, JWT auth, and role-based permissions.",
                "skills_to_acquire": ["FastAPI", "Flask", "Node.js", "Postman", "REST APIs"],
                "practical_tasks": [
                    "Build a complete CRUD REST service in FastAPI with async database sessions and OAuth2/JWT security.",
                    "Author an automated Postman test suite validating status codes, payload contracts, and error responses."
                ],
                "resource_search_keys": ["FastAPI", "REST APIs", "Postman", "Node.js"]
            },
            {
                "stage_number": 3,
                "title": "Containerization, Caching & Background Task Workers",
                "time_estimate": "3-4 Weeks",
                "description": "Implement distributed caching, asynchronous task queues, and containerize backend microservices.",
                "skills_to_acquire": ["Docker", "Microservices", "Linux", "PyTest"],
                "practical_tasks": [
                    "Dockerize multi-container application with Redis cache and Celery/async background workers via Docker Compose.",
                    "Implement comprehensive unit and integration test suite using pytest with mock database fixtures."
                ],
                "resource_search_keys": ["Docker", "Containerization", "DevOps"]
            },
            {
                "stage_number": 4,
                "title": "High Availability, CI/CD & Production Hardening",
                "time_estimate": "3-4 Weeks",
                "description": "Configure automated CI/CD deployment pipelines, structured logging, rate limiting, and security compliance.",
                "skills_to_acquire": ["CI/CD", "Cloud Computing", "REST APIs"],
                "practical_tasks": [
                    "Create a GitHub Actions CI pipeline executing linting, security scans, and test suites on pull requests.",
                    "Implement distributed tracing, structured JSON logging, and token bucket rate limiting on public endpoints."
                ],
                "resource_search_keys": ["AWS", "Cloud Computing", "DevOps"]
            }
        ],

        "software developer": [
            {
                "stage_number": 1,
                "title": "Web Foundations & Client-Side Programming",
                "time_estimate": "3-4 Weeks",
                "description": "Master semantic HTML5, modern CSS3 layouts, responsive design, and core ECMAScript / TypeScript fundamentals.",
                "skills_to_acquire": ["HTML", "CSS", "JavaScript", "Git", "GitHub"],
                "practical_tasks": [
                    "Build a responsive web application layout from scratch with accessible semantic markup and flexbox/grid.",
                    "Implement asynchronous DOM data fetching with error handling, debouncing, and local storage persistence."
                ],
                "resource_search_keys": ["JavaScript", "Frontend Development", "Git"]
            },
            {
                "stage_number": 2,
                "title": "Component Architecture & Modern React Development",
                "time_estimate": "4-5 Weeks",
                "description": "Build single-page web applications using React.js with functional components, custom hooks, and state management.",
                "skills_to_acquire": ["React.js", "Node.js", "REST APIs"],
                "practical_tasks": [
                    "Create a full-featured React application featuring routing, controlled forms, custom hook abstractions, and state management.",
                    "Optimize rendering performance using memoization and virtualized lists for large datasets."
                ],
                "resource_search_keys": ["React.js", "JavaScript", "Frontend Development"]
            },
            {
                "stage_number": 3,
                "title": "Full Stack Backend Integration & Persistent Storage",
                "time_estimate": "4-5 Weeks",
                "description": "Connect frontend single-page apps to backend REST APIs, authentication flows, and relational databases.",
                "skills_to_acquire": ["Python", "FastAPI", "SQL", "Postman"],
                "practical_tasks": [
                    "Construct a full-stack web application connecting React client to FastAPI backend with SQL persistence.",
                    "Validate API contracts and implement user login, session management, and protected client routes."
                ],
                "resource_search_keys": ["FastAPI", "Python", "SQL", "Postman"]
            },
            {
                "stage_number": 4,
                "title": "Containerized Deployment & Production Engineering",
                "time_estimate": "3-4 Weeks",
                "description": "Package full-stack applications with Docker, deploy to cloud infrastructure, and set up continuous integration.",
                "skills_to_acquire": ["Docker", "Git", "Cloud Computing"],
                "practical_tasks": [
                    "Build multi-stage Docker build files for both frontend and backend and orchestrate with Docker Compose.",
                    "Deploy the application to cloud hosting with SSL termination and automated GitHub Actions verification."
                ],
                "resource_search_keys": ["Docker", "Cloud Computing", "AWS"]
            }
        ],

        "apparel quality assurance specialist (export standard)": [
            {
                "stage_number": 1,
                "title": "Textile Fundamentals, Fabric Inspection & 4-Point Defect Grading",
                "time_estimate": "3-4 Weeks",
                "description": "Master woven and knit fabric structure identification, yarn defects, and standard ASTM D5430 4-point fabric inspection systems for export consignments.",
                "skills_to_acquire": [
                    "Fabric Grading & 4-Point System", "Garment Inspection",
                    "Textile Lab Testing (Shrinkage & Colorfastness)"
                ],
                "practical_tasks": [
                    "Perform 100-meter fabric roll inspection applying ASTM D5430 4-point penalty criteria and calculate defect points per 100 square yards.",
                    "Execute standard shrinkage wash tests and colorfastness crocking evaluations adhering to ISO/AATCC standards."
                ],
                "resource_search_keys": ["Textile Quality Control", "Fabric Inspection", "Apparel Standards"]
            },
            {
                "stage_number": 2,
                "title": "In-Line & End-Line Garment Construction Quality Control",
                "time_estimate": "3-4 Weeks",
                "description": "Implement rigorous traffic light quality systems in sewing lines, analyzing stitch types (ASTM D6193), seam strength, tension, and puckering.",
                "skills_to_acquire": [
                    "Stitch & Seam Quality Analysis", "Garment Inspection",
                    "Pattern Making & Tech Pack Review"
                ],
                "practical_tasks": [
                    "Audit sewing line work-in-progress (WIP) using Traffic Light System to identify high-defect workstations.",
                    "Measure critical garment dimensions against buyer Tech Pack tolerance sheets (±0.5 cm specifications)."
                ],
                "resource_search_keys": ["Garment Manufacturing", "Sewing Quality", "Apparel Tech Pack"]
            },
            {
                "stage_number": 3,
                "title": "Statistical Quality Sampling (ANSI/ASQ Z1.4 & ISO 2859-1 AQL 2.5)",
                "time_estimate": "3-4 Weeks",
                "description": "Execute international export final random inspection (FRI) protocols using AQL 2.5 Normal Single Sampling plans for critical, major, and minor defects.",
                "skills_to_acquire": [
                    "AQL 2.5 Sampling Standards", "Garment Inspection",
                    "Buyer Compliance & Audit Protocols"
                ],
                "practical_tasks": [
                    "Calculate sample size and accept/reject numbers for a 5,000-piece export order using ANSI/ASQ Z1.4 Normal General Inspection Level II.",
                    "Conduct complete final random inspection (FRI) and compile formal export pass/fail inspection certificate."
                ],
                "resource_search_keys": ["AQL 2.5", "Export Quality Inspection", "ISO 2859"]
            },
            {
                "stage_number": 4,
                "title": "Export Quality Management Systems (QMS) & Buyer Compliance Audits",
                "time_estimate": "2-3 Weeks",
                "description": "Establish ISO 9001 quality assurance workflows, root cause analysis (CAPA), needle detection calibration, and Sedex/WRAP social compliance readiness.",
                "skills_to_acquire": [
                    "Quality Management Systems (QMS)", "Apparel Export Documentation",
                    "Buyer Compliance & Audit Protocols"
                ],
                "practical_tasks": [
                    "Formulate a Corrective and Preventive Action (CAPA) report using 5-Why analysis for recurring shade variation defects.",
                    "Conduct a 9-point calibration audit of factory conveyor metal detectors with certified test cards (1.0 mm Fe / 1.2 mm Non-Fe)."
                ],
                "resource_search_keys": ["Apparel Export QMS", "Textile Compliance", "CAPA Quality"]
            }
        ]
    }

    out_file = PROCESSED_DIR / "occupation_competency_tiers.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(tiers_catalog, f, indent=2)

    print(f"[SUCCESS] Processed competency tiers for {len(tiers_catalog)} core occupations into {out_file}")


if __name__ == "__main__":
    build_competency_tiers()
