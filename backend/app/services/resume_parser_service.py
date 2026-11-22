"""
Feature 3: Resume Parser Service
Supports PDF and DOCX documents with deterministic text extraction,
native Apple Vision Neural OCR fallback for scanned documents on macOS,
and Neural Section Classification using the trained ResumeSectionNeuralClassifier.
Extracts entities, skills, education, experience, projects, and certifications
with strict source text evidence tracking.
"""

import os
import re
import io
import json
import torch
import torch.nn as nn
from typing import Dict, Any, List, Optional, Tuple
from pypdf import PdfReader
import docx
from sklearn.feature_extraction.text import TfidfVectorizer

from app.schemas.resume_generator import (
    ResumeFullData, PersonalInfo, EducationEntry, SkillCategories,
    ExperienceEntry, InternshipEntry, ProjectEntry, CertificationEntry, AdditionalSections
)

CHECKPOINT_PATH = "backend/app/ml/checkpoints/resume_section_classifier_best.pt"
VOCAB_PATH = "backend/app/ml/models/section_classifier_vocab.json"

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

LABEL_NAMES = ["personal_info", "experience", "education", "skills", "projects", "certifications"]

class ResumeSectionNeuralClassifier(nn.Module):
    def __init__(self, input_dim=10000, hidden_dim=256, num_classes=6, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes)
        )
    def forward(self, x):
        return self.net(x)

_CLASSIFIER_MODEL = None
_VECTORIZER = None

def _get_classifier_and_vectorizer():
    global _CLASSIFIER_MODEL, _VECTORIZER
    if _CLASSIFIER_MODEL is None and os.path.exists(CHECKPOINT_PATH) and os.path.exists(VOCAB_PATH):
        try:
            with open(VOCAB_PATH, "r", encoding="utf-8") as f:
                vocab_data = json.load(f)
            
            vec = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), sublinear_tf=True)
            vec.vocabulary_ = vocab_data["vocab"]
            import numpy as np
            vec.idf_ = np.array(vocab_data["idf"], dtype=np.float64)
            _VECTORIZER = vec

            model = ResumeSectionNeuralClassifier(input_dim=10000, hidden_dim=256, num_classes=6).to(DEVICE)
            model.load_state_dict(torch.load(CHECKPOINT_PATH, map_location=DEVICE))
            model.eval()
            _CLASSIFIER_MODEL = model
        except Exception as e:
            print(f"[ResumeParser] Error loading section classifier: {e}")
    return _CLASSIFIER_MODEL, _VECTORIZER

class ResumeParserService:
    @classmethod
    def _run_apple_vision_ocr(cls, image_bytes: bytes) -> Tuple[List[str], List[float]]:
        """Runs native macOS Apple Vision text recognition on raw image bytes."""
        try:
            import objc
            objc.loadBundle('Vision', globals(), bundle_path='/System/Library/Frameworks/Vision.framework')
            VNRecognizeTextRequest = objc.lookUpClass('VNRecognizeTextRequest')
            VNImageRequestHandler = objc.lookUpClass('VNImageRequestHandler')
            NSData = objc.lookUpClass('NSData')
            
            ns_data = NSData.dataWithBytes_length_(image_bytes, len(image_bytes))
            handler = VNImageRequestHandler.alloc().initWithData_options_(ns_data, None)
            
            request = VNRecognizeTextRequest.alloc().init()
            request.setRecognitionLevel_(0)  # 0: Accurate, 1: Fast
            
            success = handler.performRequests_error_([request], None)
            results = request.results()
            
            lines = []
            confidences = []
            if results:
                for obs in results:
                    candidates = obs.topCandidates_(1)
                    if candidates:
                        cand = candidates[0]
                        text = cand.string().strip()
                        if text:
                            lines.append(text)
                            confidences.append(float(cand.confidence()))
            return lines, confidences
        except Exception as e:
            print(f"[ResumeParser] Apple Vision OCR unavailable: {e}")
            return [], []

    @classmethod
    def extract_text_from_pdf(cls, file_bytes: bytes) -> Tuple[str, List[str], Dict[str, Any]]:
        """Extracts text lines from PDF using pypdf, falling back to Apple Vision OCR if scanned."""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
        except Exception as e:
            raise ValueError(f"Corrupted or invalid PDF document: {str(e)}")

        if reader.is_encrypted:
            raise ValueError("Password-protected PDF document. Please remove encryption before uploading.")

        lines = []
        page_count = len(reader.pages)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                for line in page_text.split("\n"):
                    clean_line = line.strip()
                    if clean_line:
                        lines.append(clean_line)

        full_text = "\n".join(lines)
        ocr_used = False
        ocr_confidence = 1.0

        # If text is empty or negligible (<30 chars) across all pages, attempt Apple Vision OCR on embedded images
        if len(full_text.strip()) < 30:
            ocr_lines = []
            ocr_confs = []
            for page in reader.pages:
                for img_file in page.images:
                    img_lines, img_confs = cls._run_apple_vision_ocr(img_file.data)
                    ocr_lines.extend(img_lines)
                    ocr_confs.extend(img_confs)

            if ocr_lines:
                lines = ocr_lines
                full_text = "\n".join(lines)
                ocr_used = True
                ocr_confidence = sum(ocr_confs) / len(ocr_confs) if ocr_confs else 0.85

        meta = {
            "pageCount": page_count,
            "ocrUsed": ocr_used,
            "ocrConfidence": round(ocr_confidence, 3),
            "isScanned": ocr_used,
            "isLowConfidence": ocr_confidence < 0.60
        }
        return full_text, lines, meta

    @classmethod
    def extract_text_from_docx(cls, file_bytes: bytes) -> Tuple[str, List[str], Dict[str, Any]]:
        """Extracts text lines from DOCX using python-docx with table and paragraph structure."""
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
        except Exception as e:
            raise ValueError(f"Corrupted or invalid DOCX document: {str(e)}")

        lines = []
        for p in doc.paragraphs:
            text = p.text.strip()
            if text:
                lines.append(text)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    c_text = cell.text.strip()
                    if c_text and c_text not in lines:
                        lines.append(c_text)

        full_text = "\n".join(lines)
        meta = {
            "paragraphCount": len(doc.paragraphs),
            "tableCount": len(doc.tables),
            "ocrUsed": False,
            "ocrConfidence": 1.0,
            "isScanned": False,
            "isLowConfidence": False
        }
        return full_text, lines, meta

    @classmethod
    def validate_file_signature(cls, filename: str, file_bytes: bytes) -> str:
        """Validates magic bytes to prevent renamed malicious payloads."""
        if len(file_bytes) == 0:
            raise ValueError("Uploaded document is empty (0 bytes).")
        if len(file_bytes) > 15 * 1024 * 1024:
            raise ValueError("File size exceeds 15MB upload limit.")

        ext = filename.lower().split(".")[-1] if "." in filename else ""
        if ext == "pdf":
            # PDF signature: %PDF (hex 25 50 44 46)
            if not file_bytes.startswith(b"%PDF"):
                raise ValueError("Invalid file signature: Content is not a valid PDF document.")
            return "pdf"
        elif ext == "docx":
            # DOCX signature: PK\x03\x04 (hex 50 4B 03 04, zip container)
            if not file_bytes.startswith(b"PK\x03\x04"):
                raise ValueError("Invalid file signature: Content is not a valid DOCX document.")
            return "docx"
        else:
            raise ValueError(f"Unsupported file format '.{ext}'. Supported formats: .pdf, .docx")

    @classmethod
    def parse_document(cls, filename: str, file_bytes: bytes) -> Dict[str, Any]:
        """
        Ingests PDF or DOCX file with magic byte validation, deterministic extraction,
        OCR fallback on scanned PDFs, neural section classification, and line evidence tracking.
        """
        # 1. Security & Signature Validation
        safe_filename = re.sub(r"[^a-zA-Z0-9_\.-]", "_", os.path.basename(filename))
        doc_type = cls.validate_file_signature(safe_filename, file_bytes)

        # 2. Text Extraction & OCR
        if doc_type == "pdf":
            full_text, raw_lines, doc_meta = cls.extract_text_from_pdf(file_bytes)
        else:
            full_text, raw_lines, doc_meta = cls.extract_text_from_docx(file_bytes)

        if not raw_lines or len(full_text.strip()) < 20:
            raise ValueError("Unable to extract sufficient text: document appears to be empty or unreadable.")

        # 3. Neural Section Classifier + Heading Rules
        classifier, vec = _get_classifier_and_vectorizer()

        sections = {
            "personal_info": [],
            "experience": [],
            "education": [],
            "skills": [],
            "projects": [],
            "certifications": [],
            "additional": [],
        }

        current_section = "personal_info"

        heading_patterns = {
            "experience": r"^(?:#+\s*)?(work\s+experience|professional\s+experience|employment\s+history|employment|work\s+history|experience)[\s:]*$",
            "education": r"^(?:#+\s*)?(education|academic\s+background|academics|qualifications|academic\s+credentials|degrees)[\s:]*$",
            "skills": r"^(?:#+\s*)?(technical\s+skills|skills\s+(&|and)\s+abilities|skills|technologies|core\s+competencies|technical\s+stack|technical\s+capabilities)[\s:]*$",
            "projects": r"^(?:#+\s*)?(projects|notable\s+projects|academic\s+projects|key\s+projects|personal\s+projects)[\s:]*$",
            "certifications": r"^(?:#+\s*)?(certifications|certificates|licenses\s+(&|and)\s+certifications|licenses|credentials)[\s:]*$",
            "additional": r"^(?:#+\s*)?(honors\s+(&|and)\s+awards|awards|achievements|publications|extracurricular\s+activities|volunteer\s+experience)[\s:]*$",
        }

        evidence_lines = []

        for line_num, line in enumerate(raw_lines):
            clean = line.strip()
            lower = clean.lower()

            # Heading match: only short lines (< 45 chars) without long colon values
            matched_header = None
            if len(clean) < 45 and not (":" in clean and len(clean.split(":", 1)[1].strip()) > 8):
                clean_h = re.sub(r"^[#\*\-•\s]+", "", clean).strip()
                lower_h = clean_h.lower()
                for sec_name, pattern in heading_patterns.items():
                    if re.search(pattern, lower_h):
                        matched_header = sec_name
                        break

            if matched_header:
                current_section = matched_header
                continue

            # Neural model classification refinement
            if classifier and vec and len(clean) > 30 and current_section == "personal_info" and line_num > 5:
                try:
                    feat = vec.transform([clean]).toarray()
                    with torch.no_grad():
                        logits = classifier(torch.tensor(feat, dtype=torch.float32).to(DEVICE))
                        pred_idx = torch.argmax(logits, dim=1).item()
                        predicted_sec = LABEL_NAMES[pred_idx]
                        if predicted_sec in sections and predicted_sec != "personal_info":
                            current_section = predicted_sec
                except Exception:
                    pass

            sections[current_section].append({"line_num": line_num + 1, "text": clean})
            evidence_lines.append({"line_num": line_num + 1, "text": clean, "section": current_section})

        # 4. Structured Entity Extraction
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", full_text)
        email = email_match.group(0) if email_match else ""

        phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,5}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}", full_text)
        phone = phone_match.group(0) if phone_match else ""

        linkedin_match = re.search(r"(https?://(?:www\.)?linkedin\.com/in/[\w\-_]+)", full_text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else ""

        github_match = re.search(r"(https?://(?:www\.)?github\.com/[\w\-_]+)", full_text, re.IGNORECASE)
        github = github_match.group(0) if github_match else ""

        portfolio_match = re.search(r"(https?://(?:www\.)?(?!linkedin|github)[\w\-\.]+\.[a-z]{2,}(?:/[\w\-_]*)*)", full_text, re.IGNORECASE)
        portfolio = portfolio_match.group(0) if portfolio_match else ""

        # Extract name & professional title from top personal_info lines
        full_name = ""
        professional_title = ""
        location = ""

        SECTION_HEADER_WORDS = {"PROFESSIONAL SUMMARY", "SUMMARY", "ABOUT ME", "OBJECTIVE", "PROFILE", "CAREER OBJECTIVE", "EXPERIENCE", "EDUCATION", "SKILLS"}

        pi_lines = [item["text"] for item in sections["personal_info"] if item["text"]]
        for idx, t in enumerate(pi_lines[:8]):
            # If line is a section header keyword, skip it
            if t.strip().upper() in SECTION_HEADER_WORDS:
                continue

            # Check if this line has a title prefix before '|' even if it also has contact info
            if "|" in t and not professional_title:
                parts = [p.strip() for p in t.split("|")]
                first_part = parts[0]
                if not re.search(r"@|linkedin|github|phone|resume|portfolio|http|\+?\d{3}", first_part, re.IGNORECASE) and len(first_part.split()) in [2, 3, 4, 5, 6]:
                    professional_title = first_part

            # Skip contact/metadata lines for name detection
            if re.search(r"@|linkedin|github|phone|resume|curriculum|portfolio|http|\+?\d{3}", t, re.IGNORECASE):
                # Check for location in contact line
                loc_match = re.search(r"(?:\|\s*|\b)([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]+(?:\s*,\s*[A-Z][a-zA-Z\s]+)?)", t)
                if loc_match and not location:
                    location = loc_match.group(1).strip()
                continue

            if not full_name and len(t.split()) in [2, 3, 4] and not re.search(r"[:\d]", t):
                full_name = t.strip()
                # Check if next line is a professional title
                if idx + 1 < len(pi_lines):
                    next_l = pi_lines[idx + 1]
                    if next_l.strip().upper() not in SECTION_HEADER_WORDS and not re.search(r"@|linkedin|github|phone|http|\+?\d{3}", next_l, re.IGNORECASE) and len(next_l) < 70:
                        professional_title = next_l.strip()
            elif full_name and not professional_title and len(t) < 70 and t.strip().upper() not in SECTION_HEADER_WORDS and not re.search(r"@|linkedin|github|phone|http|\+?\d{3}", t, re.IGNORECASE):
                professional_title = t.strip()

        # Summary lines
        summary_sentences = [item["text"] for item in sections["personal_info"] if len(item["text"]) > 35 and not re.search(r"@|linkedin|github|phone|http|\+?\d{3}", item["text"], re.IGNORECASE)]
        summary = " ".join(summary_sentences[:3]) if summary_sentences else ""

        # 5. Structured Skills & Coursework Categorization with Exact Provenance
        # Recognized taxonomies and vocabularies
        LANGUAGES = {
            "python", "javascript", "typescript", "c++", "cpp", "c", "c#", "java", "go", "golang",
            "rust", "ruby", "php", "swift", "kotlin", "r", "scala", "sql", "sql (mysql)", "bash",
            "shell", "dart", "html", "css"
        }
        FRAMEWORKS = {
            "flask", "fastapi", "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch",
            "opencv", "react", "react.js", "reactjs", "node", "node.js", "nodejs", "express", "django",
            "next.js", "nextjs", "vue", "angular", "spring boot", "keras", "tailwind css", "tailwind",
            "graphql"
        }
        DATABASES = {
            "mysql", "mongodb", "postgresql", "postgres", "redis", "sqlite", "sql", "sql (mysql)",
            "nosql", "dynamodb", "cassandra", "elasticsearch", "oracle", "mariadb", "firebase", "supabase"
        }
        TOOLS = {
            "git", "github", "docker", "google colab", "google cloud", "gcp", "jupyter notebook",
            "jupyter", "vs code", "vscode", "postman", "kubernetes", "aws", "azure", "linux", "jenkins",
            "ci/cd", "terraform", "jira", "gitlab"
        }
        AIML = {
            "machine learning", "deep learning", "cnn", "yolov8", "yolo", "llm", "llms", "large language models",
            "rag", "model training", "evaluation", "computer vision", "cv", "nlp", "natural language processing",
            "transformers", "hugging face", "scikit-learn", "sklearn", "lora", "fine-tuning", "mlx", "onnx",
            "langchain", "artificial intelligence", "ai", "resnet"
        }
        OTHER_SKILLS = {
            "problem solving", "debugging", "oop", "object-oriented programming", "api development",
            "rest apis", "rest api", "restful", "data structures and algorithms", "dsa", "web development"
        }

        # Ignored heading keywords that must NEVER be treated as candidate skills
        HEADING_KEYWORDS = {
            "technical skills", "skills", "technologies", "programming languages", "machine learning / al",
            "machine learning / ai", "frameworks/libraries", "frameworks", "libraries", "web development",
            "databases", "tools & platforms", "tools", "platforms", "other skills", "relevant coursework",
            "coursework", "core competencies", "technical capabilities"
        }

        categorized_skills = {
            "programmingLanguages": [],
            "frameworks": [],
            "databases": [],
            "developerTools": [],
            "aiMlSkills": [],
            "otherSkills": []
        }
        all_skill_tokens = []
        candidate_skills_inventory = []
        extracted_coursework = []

        # Step 5A: Separate Technical Skills vs. Relevant Coursework
        raw_skills_items = sections.get("skills", [])
        coursework_items = []
        tech_skill_items = []
        in_coursework_block = False

        for itm in raw_skills_items:
            txt = itm["text"].strip()
            if not txt or txt in ("• •", "•", "-", "–", "*"):
                continue
            if re.search(r"^(?:#+\s*)?(?:relevant\s+coursework|coursework)[\s:]*$", txt, re.I):
                in_coursework_block = True
                continue
            if in_coursework_block:
                coursework_items.append(itm)
            else:
                tech_skill_items.append(itm)

        # Step 5B: Extract Coursework Items with provenance
        for itm in coursework_items:
            cw_tokens = [p.strip() for p in re.split(r"[,•|;]", itm["text"]) if len(p.strip()) > 1]
            for tok in cw_tokens:
                clean_tok = tok.strip(" •-*–")
                if clean_tok and clean_tok.lower() not in HEADING_KEYWORDS and clean_tok not in extracted_coursework:
                    extracted_coursework.append(clean_tok)
                    candidate_skills_inventory.append({
                        "skill": clean_tok,
                        "category": "coursework",
                        "categoryLabel": "Relevant Coursework",
                        "sourceSection": "Relevant Coursework",
                        "sourcePhrase": itm["text"],
                        "lineNum": itm["line_num"],
                        "extractionMethod": "academic_coursework_extraction",
                        "confidence": 0.99
                    })

        # Step 5C: Check for Tabular / Column-wise Category Layout
        CATEGORY_HEADER_PATTERNS = [
            ("programmingLanguages", "Programming Languages", r"^programming\s+languages"),
            ("aiMlSkills", "Machine Learning / AI", r"^(machine\s+learning|ai\b)"),
            ("frameworks", "Frameworks/Libraries", r"^(frameworks|libraries)"),
            ("frameworks", "Web Development", r"^web\s+development"),
            ("databases", "Databases", r"^databases?"),
            ("developerTools", "Tools & Platforms", r"^(tools|platforms)"),
            ("otherSkills", "Other Skills", r"^other\s+skills")
        ]

        found_headers = []
        found_values = []

        for itm in tech_skill_items:
            txt = itm["text"].strip()
            is_hdr = False
            for cat_key, cat_lbl, pat in CATEGORY_HEADER_PATTERNS:
                if re.search(pat, txt, re.I) and "," not in txt and len(txt) < 35:
                    found_headers.append((cat_key, cat_lbl, itm))
                    is_hdr = True
                    break
            if not is_hdr:
                found_values.append(itm)

        # If detected perfect 1-to-1 columnar alignment (e.g. 7 headers followed by 7 comma-separated lines)
        if len(found_headers) > 0 and len(found_headers) == len(found_values):
            for (cat_key, cat_lbl, h_itm), v_itm in zip(found_headers, found_values):
                tokens = [t.strip() for t in re.split(r"[,•|;]", v_itm["text"]) if len(t.strip()) > 1]
                for tok in tokens:
                    tok_clean = tok.strip(" •-*–")
                    if not tok_clean or tok_clean.lower() in HEADING_KEYWORDS:
                        continue

                    # Refine category for composite sections (e.g. Web Development)
                    final_cat = cat_key
                    if cat_lbl == "Web Development":
                        if tok_clean.lower() in ("html", "css", "javascript"):
                            final_cat = "programmingLanguages"
                        elif tok_clean.lower() in ("react.js", "react", "node.js", "node"):
                            final_cat = "frameworks"
                        else:
                            final_cat = "otherSkills"
                    elif tok_clean.lower() in ("computer vision", "cv"):
                        final_cat = "aiMlSkills"

                    categorized_skills[final_cat].append(tok_clean)
                    all_skill_tokens.append(tok_clean)
                    candidate_skills_inventory.append({
                        "skill": tok_clean,
                        "category": final_cat,
                        "categoryLabel": cat_lbl,
                        "sourceSection": "Technical Skills",
                        "sourcePhrase": v_itm["text"],
                        "lineNum": v_itm["line_num"],
                        "extractionMethod": "tabular_column_mapping",
                        "confidence": 0.99
                    })
        else:
            # Fallback: process lines sequentially (colon prefixes or lexical keyword matching)
            for itm in tech_skill_items:
                line_text = itm["text"].strip()
                if not line_text or line_text.lower() in HEADING_KEYWORDS:
                    continue

                if ":" in line_text:
                    parts = line_text.split(":", 1)
                    prefix = parts[0].strip().lower()
                    tokens = [s.strip() for s in re.split(r"[,•|;]", parts[1]) if len(s.strip()) > 1]
                    for tok in tokens:
                        tok_clean = tok.strip(" •-*–")
                        norm = tok_clean.lower()
                        if not tok_clean or norm in HEADING_KEYWORDS:
                            continue
                        all_skill_tokens.append(tok_clean)

                        if "language" in prefix or norm in LANGUAGES:
                            cat = "programmingLanguages"
                        elif any(k in prefix for k in ["framework", "library", "libraries"]) or norm in FRAMEWORKS:
                            cat = "frameworks"
                        elif any(k in prefix for k in ["database", "storage", "db"]) or norm in DATABASES:
                            cat = "databases"
                        elif any(k in prefix for k in ["tool", "cloud", "devops", "platform"]) or norm in TOOLS:
                            cat = "developerTools"
                        elif any(k in prefix for k in ["ai", "ml", "machine learning", "deep learning"]) or norm in AIML:
                            cat = "aiMlSkills"
                        else:
                            cat = "otherSkills"

                        categorized_skills[cat].append(tok_clean)
                        candidate_skills_inventory.append({
                            "skill": tok_clean,
                            "category": cat,
                            "categoryLabel": prefix.title(),
                            "sourceSection": "Technical Skills",
                            "sourcePhrase": line_text,
                            "lineNum": itm["line_num"],
                            "extractionMethod": "prefix_token_mapping",
                            "confidence": 0.98
                        })
                else:
                    tokens = [s.strip() for s in re.split(r"[,•|;]", line_text) if len(s.strip()) > 1]
                    for tok in tokens:
                        tok_clean = tok.strip(" •-*–")
                        norm = tok_clean.lower()
                        if not tok_clean or norm in HEADING_KEYWORDS:
                            continue
                        all_skill_tokens.append(tok_clean)

                        if norm in LANGUAGES:
                            cat = "programmingLanguages"
                        elif norm in FRAMEWORKS:
                            cat = "frameworks"
                        elif norm in DATABASES:
                            cat = "databases"
                        elif norm in TOOLS:
                            cat = "developerTools"
                        elif norm in AIML:
                            cat = "aiMlSkills"
                        else:
                            cat = "otherSkills"

                        categorized_skills[cat].append(tok_clean)
                        candidate_skills_inventory.append({
                            "skill": tok_clean,
                            "category": cat,
                            "categoryLabel": cat,
                            "sourceSection": "Technical Skills",
                            "sourcePhrase": line_text,
                            "lineNum": itm["line_num"],
                            "extractionMethod": "ontology_lexical_mapping",
                            "confidence": 0.95
                        })

        # Deduplicate within each category while preserving order and casing
        for cat in categorized_skills:
            seen_in_cat = set()
            deduped = []
            for item in categorized_skills[cat]:
                k = item.lower().strip()
                if k and k not in seen_in_cat and k not in HEADING_KEYWORDS:
                    seen_in_cat.add(k)
                    deduped.append(item)
            categorized_skills[cat] = deduped

        # 6. Structured Education Extraction
        education_entries: List[EducationEntry] = []
        current_edu: Optional[Dict[str, Any]] = None

        for item in sections["education"]:
            txt = item["text"]
            deg_match = re.search(r"\b(b\.?tech|b\.?e\.?|b\.?s\.?|b\.?a\.?|m\.?tech|m\.?s\.?|m\.?b\.?a\.?|ph\.?d|bachelor|master|diploma|associate|secondary)\b", txt, re.IGNORECASE)
            inst_match = re.search(r"\b(university|college|institute|school|academy|iit|nit|bits|dtu|iiit)\b", txt, re.IGNORECASE)
            date_match = re.search(r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20\d\d|19\d\d)\s*(?:–|-|to)\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20\d\d|19\d\d|present)", txt, re.IGNORECASE)
            grade_match = re.search(r"(?:cgpa|gpa|grade|score)[:\s]*([0-9\.]+(?:\s*\/\s*[0-9\.]+)?%?)", txt, re.IGNORECASE)

            # If current_edu exists and line provides dates or grades for it
            if current_edu and (date_match or grade_match) and not (deg_match and inst_match):
                if date_match and not current_edu["startDate"]:
                    parts = re.split(r"\s*(?:–|-|to)\s*", date_match.group(0), flags=re.IGNORECASE)
                    current_edu["startDate"] = parts[0].strip() if len(parts) > 0 else ""
                    current_edu["endDate"] = parts[1].strip() if len(parts) > 1 else ""
                if grade_match and not current_edu["grade"]:
                    current_edu["grade"] = grade_match.group(0).strip()
                continue

            # If current_edu exists and is missing degree or institution, merge complementary line
            if current_edu:
                if inst_match and not current_edu["institution"] and current_edu["degree"]:
                    current_edu["institution"] = txt
                    continue
                elif deg_match and not current_edu["degree"] and current_edu["institution"]:
                    current_edu["degree"] = txt
                    continue

            if deg_match or inst_match:
                if current_edu and (current_edu["institution"] or current_edu["degree"]):
                    education_entries.append(EducationEntry(**current_edu))
                current_edu = {
                    "id": f"edu-{len(education_entries) + 1}",
                    "institution": txt if inst_match else "",
                    "degree": txt if deg_match and not inst_match else "",
                    "fieldOfStudy": "",
                    "startDate": "",
                    "endDate": "",
                    "grade": None,
                    "coursework": []
                }
                if date_match:
                    parts = re.split(r"\s*(?:–|-|to)\s*", date_match.group(0), flags=re.IGNORECASE)
                    current_edu["startDate"] = parts[0].strip() if len(parts) > 0 else ""
                    current_edu["endDate"] = parts[1].strip() if len(parts) > 1 else ""
                if grade_match:
                    current_edu["grade"] = grade_match.group(0).strip()
            elif current_edu:
                if re.search(r"coursework|courses", txt, re.IGNORECASE):
                    cw_tokens = [c.strip() for c in re.split(r"[,•|;:]", re.sub(r"^(?:relevant\s+)?coursework[:\s]*", "", txt, flags=re.IGNORECASE)) if len(c.strip()) > 2]
                    current_edu["coursework"].extend(cw_tokens[:8])
                elif not current_edu["degree"] and len(txt) < 80:
                    current_edu["degree"] = txt
                elif not current_edu["fieldOfStudy"] and len(txt) < 80:
                    current_edu["fieldOfStudy"] = txt

        if current_edu and (current_edu["institution"] or current_edu["degree"]):
            education_entries.append(EducationEntry(**current_edu))

        # Attach extracted coursework to degree/university education entry
        if extracted_coursework and education_entries:
            target_edu = None
            for edu in education_entries:
                combined_txt = (edu.degree + " " + edu.institution).lower()
                if re.search(r"b\.?tech|bachelor|master|m\.?tech|degree|university", combined_txt):
                    target_edu = edu
                    break
            if not target_edu:
                target_edu = education_entries[0]
            target_edu.coursework = list(extracted_coursework)

        # 7. Structured Experience & Internships Extraction
        experience_entries: List[ExperienceEntry] = []
        internship_entries: List[InternshipEntry] = []
        current_exp: Optional[Dict[str, Any]] = None
        is_intern_role = False

        for item in sections["experience"]:
            txt = item["text"]
            date_match = re.search(r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20\d\d|19\d\d)\s*(?:–|-|to)\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20\d\d|19\d\d|present)", txt, re.IGNORECASE)
            is_bullet = txt.startswith(("-", "•", "*", "–"))

            # If current_exp exists and this is a secondary line with date or location
            if current_exp and not current_exp.get("startDate") and date_match and not is_bullet:
                dp = re.split(r"\s*(?:–|-|to)\s*", date_match.group(0), flags=re.IGNORECASE)
                current_exp["startDate"] = dp[0].strip() if len(dp) > 0 else ""
                current_exp["endDate"] = dp[1].strip() if len(dp) > 1 else "Present"
                loc_part = re.sub(r"((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20\d\d|19\d\d)\s*(?:–|-|to)\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(?:20\d\d|19\d\d|present)", "", txt, flags=re.IGNORECASE).strip(" |–-")
                if loc_part and len(loc_part) < 40:
                    current_exp["location"] = loc_part
                continue

            # Determine if this line is a new job header
            is_new_header = (not is_bullet) and (
                "|" in txt or
                re.search(r"\b(engineer|developer|lead|architect|manager|intern|specialist|analyst|consultant|director)\b", txt, re.IGNORECASE)
            )

            if is_new_header:
                # Save previous entry
                if current_exp and (current_exp.get("company") or current_exp.get("role")):
                    if is_intern_role:
                        internship_entries.append(InternshipEntry(
                            id=f"intern-{len(internship_entries) + 1}",
                            organization=current_exp.get("company", ""),
                            role=current_exp.get("role", "Intern"),
                            duration=f"{current_exp.get('startDate', '')} – {current_exp.get('endDate', '')}",
                            workPerformed=current_exp.get("responsibilities", []),
                            achievements=current_exp.get("achievements", [])
                        ))
                    else:
                        experience_entries.append(ExperienceEntry(
                            id=f"exp-{len(experience_entries) + 1}",
                            company=current_exp.get("company", ""),
                            role=current_exp.get("role", ""),
                            employmentType="Full-time",
                            location=current_exp.get("location", None),
                            startDate=current_exp.get("startDate", ""),
                            endDate=current_exp.get("endDate", "Present"),
                            current="present" in current_exp.get("endDate", "").lower(),
                            responsibilities=current_exp.get("responsibilities", [])
                        ))

                is_intern_role = "intern" in txt.lower()
                parts = [p.strip() for p in re.split(r"[|–-]", txt) if p.strip()]
                comp = parts[0] if len(parts) > 0 else ""
                role = parts[1] if len(parts) > 1 else ("Software Engineer" if not is_intern_role else "Engineering Intern")

                s_date = ""
                e_date = "Present"
                if date_match:
                    dp = re.split(r"\s*(?:–|-|to)\s*", date_match.group(0), flags=re.IGNORECASE)
                    s_date = dp[0].strip() if len(dp) > 0 else ""
                    e_date = dp[1].strip() if len(dp) > 1 else "Present"

                current_exp = {
                    "company": comp,
                    "role": role,
                    "location": None,
                    "startDate": s_date,
                    "endDate": e_date,
                    "responsibilities": [],
                    "achievements": []
                }
            elif current_exp:
                clean_bullet = re.sub(r"^[-•\*–\d\.\s]+", "", txt).strip()
                if len(clean_bullet) > 10:
                    current_exp["responsibilities"].append(clean_bullet)
                    if re.search(r"(\d+%|\$\d+|\d+\+|\b\d+\b)", clean_bullet):
                        current_exp["achievements"].append(clean_bullet)

        if current_exp and (current_exp.get("company") or current_exp.get("role")):
            if is_intern_role:
                internship_entries.append(InternshipEntry(
                    id=f"intern-{len(internship_entries) + 1}",
                    organization=current_exp.get("company", ""),
                    role=current_exp.get("role", "Intern"),
                    duration=f"{current_exp.get('startDate', '')} – {current_exp.get('endDate', '')}",
                    workPerformed=current_exp.get("responsibilities", []),
                    achievements=current_exp.get("achievements", [])
                ))
            else:
                experience_entries.append(ExperienceEntry(
                    id=f"exp-{len(experience_entries) + 1}",
                    company=current_exp.get("company", ""),
                    role=current_exp.get("role", ""),
                    employmentType="Full-time",
                    location=current_exp.get("location", None),
                    startDate=current_exp.get("startDate", ""),
                    endDate=current_exp.get("endDate", "Present"),
                    current="present" in current_exp.get("endDate", "").lower(),
                    responsibilities=current_exp.get("responsibilities", [])
                ))

        # 8. Structured Projects Extraction
        project_entries: List[ProjectEntry] = []
        current_proj: Optional[Dict[str, Any]] = None
        DATE_PAT = re.compile(r"^(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*\d{4}|\d{4})\s*[-–—to\s]*(?:present|current|\d{4}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*\d{4})?$", re.I)
        TECH_PAT = re.compile(r"^(?:tech\s*stack|technologies|tools\s*used)[:\s]*(.+)", re.I)
        is_bullet_pending = False

        for item in sections["projects"]:
            txt = item["text"].strip()
            if not txt:
                continue

            if txt in ("•", "-", "*", "–"):
                is_bullet_pending = True
                continue

            is_bullet = txt.startswith(("-", "•", "*", "–")) or is_bullet_pending
            is_bullet_pending = False
            clean_txt = re.sub(r"^[-•\*–\d\.\s]+", "", txt).strip()

            # Check if tech stack line
            tm = TECH_PAT.search(clean_txt)
            if tm and current_proj:
                raw_techs = tm.group(1)
                techs = [t.strip() for t in re.split(r"[,|•]", raw_techs) if t.strip()]
                current_proj["technologies"].extend(techs)
                continue

            # Check if date line
            if DATE_PAT.match(clean_txt) and current_proj:
                continue

            # Check if new project title candidate
            is_title_candidate = (
                not is_bullet
                and bool(clean_txt)
                and not DATE_PAT.match(clean_txt)
                and len(clean_txt) < 95
                and not clean_txt[0].islower()
                and not re.search(r"^https?://", clean_txt)
                and (" - " in clean_txt or len(clean_txt.split()) <= 8)
                and not re.search(r"^(?:innovative|eager|passionate|motivated|seeking|responsible)\b", clean_txt, re.I)
            )

            if is_title_candidate:
                if current_proj and current_proj["title"]:
                    project_entries.append(ProjectEntry(**current_proj))

                title = clean_txt
                desc = ""
                techs = []
                if " - " in clean_txt:
                    parts = clean_txt.split(" - ", 1)
                    title = parts[0].strip()
                    desc = parts[1].strip()

                tech_match = re.search(r"\(([^)]+)\)", title)
                if tech_match:
                    techs = [t.strip() for t in tech_match.group(1).split(",") if t.strip()]
                    title = re.sub(r"\([^)]+\)", "", title).strip()

                current_proj = {
                    "id": f"proj-{len(project_entries) + 1}",
                    "title": title or clean_txt,
                    "description": desc,
                    "technologies": techs,
                    "contributions": [],
                    "projectUrl": None,
                    "githubUrl": None
                }
            elif current_proj:
                if re.search(r"github\.com", txt):
                    gh_m = re.search(r"https?://github\.com/[\w\-_/]+", txt)
                    current_proj["githubUrl"] = gh_m.group(0) if gh_m else txt
                elif is_bullet:
                    if clean_txt:
                        current_proj["contributions"].append(clean_txt)
                else:
                    # Bullet continuation or appended description
                    if current_proj["contributions"]:
                        current_proj["contributions"][-1] += " " + clean_txt
                    elif not current_proj["description"]:
                        current_proj["description"] = clean_txt

        if current_proj and current_proj["title"]:
            project_entries.append(ProjectEntry(**current_proj))

        # 9. Structured Certifications Extraction
        certification_entries: List[CertificationEntry] = []
        for item in sections["certifications"]:
            txt = item["text"]
            clean_cert = re.sub(r"^[-•\*–\d\.\s]+", "", txt).strip()
            if len(clean_cert) > 5:
                # Check for Organization / Year
                parts = [p.strip() for p in re.split(r"[|–-]", clean_cert) if p.strip()]
                cert_name = parts[0]
                issuer = parts[1] if len(parts) > 1 else "Certified Authority"
                year_match = re.search(r"\b(20\d\d|19\d\d)\b", clean_cert)
                issue_date = year_match.group(0) if year_match else "Verified"

                certification_entries.append(CertificationEntry(
                    id=f"cert-{len(certification_entries) + 1}",
                    name=cert_name,
                    issuingOrganization=issuer,
                    issueDate=issue_date,
                    credentialUrl=None
                ))

        # 10. Additional Sections Extraction
        achievements_list = []
        for item in sections["additional"]:
            clean_add = re.sub(r"^[-•\*–\d\.\s]+", "", item["text"]).strip()
            if len(clean_add) > 5:
                achievements_list.append(clean_add)

        # Assemble full ResumeFullData structured model
        structured_resume = ResumeFullData(
            personalInfo=PersonalInfo(
                fullName=full_name or (raw_lines[0] if raw_lines else "Candidate"),
                professionalTitle=professional_title,
                email=email,
                phone=phone,
                location=location,
                linkedIn=linkedin or None,
                gitHub=github or None,
                portfolio=portfolio or None,
                summary=summary
            ),
            skills=SkillCategories(**categorized_skills),
            education=education_entries,
            experience=experience_entries,
            internships=internship_entries,
            projects=project_entries,
            certifications=certification_entries,
            additional=AdditionalSections(
                achievements=achievements_list[:5],
                awards=[],
                publications=[],
                volunteerExperience=[],
                extracurricular=[],
                languages=[],
                interests=[]
            ),
            templateId="ats_friendly",
            accentColor="#17233F",
            typography="sans",
            spacing="normal"
        )

        # Build parsed result payload
        parsed_resume = {
            "documentMetadata": {
                "filename": safe_filename,
                "documentType": doc_type,
                "totalLines": len(raw_lines),
                "totalWords": len(full_text.split()),
                "parsedVia": "Apple Vision Neural OCR (Metal)" if doc_meta["ocrUsed"] else "Deterministic Stream Parser + Neural Section Classifier (MPS)",
                "ocrUsed": doc_meta["ocrUsed"],
                "ocrConfidence": doc_meta["ocrConfidence"],
                "isLowConfidence": doc_meta["isLowConfidence"],
            },
            "structuredResume": structured_resume.model_dump(),
            "personalInfo": structured_resume.personalInfo.model_dump(),
            "skills": all_skill_tokens,
            "categorizedSkills": structured_resume.skills.model_dump(),
            "candidateSkillsInventory": candidate_skills_inventory,
            "skillsInventory": candidate_skills_inventory,
            "relevantCoursework": extracted_coursework,
            "education": [e.model_dump() for e in education_entries],
            "experience": [e.model_dump() for e in experience_entries],
            "internships": [e.model_dump() for e in internship_entries],
            "projects": [p.model_dump() for p in project_entries],
            "certifications": [c.model_dump() for c in certification_entries],
            "sectionBreakdown": {
                "personalInfoCount": len(sections["personal_info"]),
                "experienceCount": len(sections["experience"]),
                "educationCount": len(sections["education"]),
                "skillsCount": len(sections["skills"]),
                "projectsCount": len(sections["projects"]),
                "certificationsCount": len(sections["certifications"]),
            },
            "rawSections": {
                sec: [item["text"] for item in items] for sec, items in sections.items()
            },
            "evidenceLines": evidence_lines[:150],
            "rawText": full_text[:4000]
        }

        return parsed_resume
