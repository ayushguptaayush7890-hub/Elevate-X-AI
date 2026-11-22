"""
Feature 3: ATS Matcher Service
Performs deterministic and 6-layer hybrid semantic job description analysis,
pretrained DistilBERT cosine semantic matching, and calculates an explainable
100-point ATS Compatibility Score:
- Part A: Job Requirement Alignment (0-60 points)
- Part B: Resume Document Quality (0-40 points)
Strict source evidence tracking for both resume and job description.
"""

import re
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from app.schemas.resume_generator import (
    ResumeFullData,
    ATSJobDescriptionAnalysisResponse,
    RequirementMatch,
    PartADetails,
    PartBDetails,
    ATSScoreBreakdown,
    ATSMatchResponse,
)

# Standard action verbs for Part B audit
ACTION_VERBS = {
    "accelerated", "achieved", "administered", "architected", "automated", "built", "championed",
    "collaborated", "conceived", "constructed", "created", "decreased", "delivered", "deployed",
    "designed", "developed", "devised", "directed", "engineered", "enhanced", "established",
    "executed", "expanded", "expedited", "formulated", "founded", "generated", "guided",
    "implemented", "improved", "increased", "initiated", "innovated", "installed", "instituted",
    "integrated", "introduced", "launched", "lead", "led", "managed", "maximized", "mentored",
    "minimized", "modernized", "monitored", "navigated", "negotiated", "optimized", "orchestrated",
    "organized", "overhauled", "oversaw", "pioneered", "planned", "programmed", "reduced",
    "refactored", "resolved", "restructured", "revamped", "scaled", "simplified", "spearheaded",
    "standardized", "streamlined", "strengthened", "supervised", "synthesized", "transformed",
    "upgraded", "validated", "yielded"
}

SENIORITY_KEYWORDS = {
    "Lead": ["lead", "principal", "staff", "director", "head of", "vp", "chief"],
    "Senior": ["senior", "sr.", "sr ", "advanced", "specialist"],
    "Mid": ["mid", "intermediate", "experienced"],
    "Junior / Entry": ["junior", "jr.", "entry", "associate", "intern", "graduate"]
}

# Technical alias dictionary for robust technical entity resolution (Layer 3)
TECHNICAL_ALIASES = {
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "sql (mysql)", "t-sql", "pl/sql", "nosql"],
    "react": ["react", "react.js", "reactjs", "react native"],
    "react.js": ["react", "react.js", "reactjs", "react native"],
    "node": ["node", "node.js", "nodejs"],
    "node.js": ["node", "node.js", "nodejs"],
    "llm": ["llm", "llms", "large language model", "large language models", "generative ai", "genai", "transformer", "transformers"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "nlp": ["nlp", "natural language processing", "text mining", "ner", "sentiment analysis", "spacy", "nltk", "transformers"],
    "computer vision": ["computer vision", "cv", "opencv", "yolo", "yolov8", "object detection", "image recognition", "image segmentation", "resnet", "cnn"],
    "machine learning": ["machine learning", "ml", "scikit-learn", "sklearn", "supervised learning", "unsupervised learning"],
    "deep learning": ["deep learning", "dl", "neural network", "neural networks", "cnn", "rnn", "lstm", "transformer", "transformers", "pytorch", "tensorflow"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow", "tf", "keras"],
    "docker": ["docker", "containerization", "containers"],
    "git": ["git"],
    "github": ["github", "git"],
    "postman": ["postman", "api testing"],
    "data structures and algorithms": ["data structures and algorithms", "dsa", "data structures & algorithms", "data structures", "algorithms"],
    "rest api": ["rest api", "rest apis", "restful", "restful api", "restful apis", "api development"],
    "c++": ["c++", "cpp"],
    "python": ["python", "python3"],
    "numpy": ["numpy"],
    "pandas": ["pandas"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "azure": ["azure", "microsoft azure"],
    "kubernetes": ["kubernetes", "k8s"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "linux": ["linux", "unix", "bash", "shell"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment", "github actions", "jenkins"],
    "typescript": ["typescript", "ts"],
    "javascript": ["javascript", "js", "es6"]
}

_EMBED_MODEL = None
_EMBED_TOKENIZER = None


def get_embed_model():
    """Lazily load cached DistilBERT semantic representation model."""
    global _EMBED_MODEL, _EMBED_TOKENIZER
    if not TRANSFORMERS_AVAILABLE:
        return None, None
    if _EMBED_MODEL is None:
        try:
            model_name = "typeform/distilbert-base-uncased-mnli"
            _EMBED_TOKENIZER = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
            _EMBED_MODEL = AutoModel.from_pretrained(model_name, local_files_only=True)
            _EMBED_MODEL.eval()
        except Exception:
            _EMBED_MODEL = None
            _EMBED_TOKENIZER = None
    return _EMBED_MODEL, _EMBED_TOKENIZER


def compute_distilbert_embeddings(texts: List[str]) -> Optional[np.ndarray]:
    """Computes mean-pooled L2-normalized 768-dim embeddings using DistilBERT."""
    model, tokenizer = get_embed_model()
    if model is None or tokenizer is None or not texts:
        return None
    try:
        inputs = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            mask = inputs["attention_mask"].unsqueeze(-1).expand(outputs.last_hidden_state.size()).float()
            sum_embeddings = torch.sum(outputs.last_hidden_state * mask, 1)
            sum_mask = torch.clamp(mask.sum(1), min=1e-9)
            mean_pooled = sum_embeddings / sum_mask
            normalized = torch.nn.functional.normalize(mean_pooled, p=2, dim=1)
        return normalized.cpu().numpy()
    except Exception:
        return None


class ATSMatcherService:
    @classmethod
    def analyze_job_description(cls, jd_text: str, job_title: Optional[str] = None) -> ATSJobDescriptionAnalysisResponse:
        t0 = time.time()
        lines = [line.strip() for line in jd_text.split("\n") if line.strip()]
        
        # Determine title
        inferred_title = job_title or ""
        if not inferred_title and lines:
            for l in lines[:5]:
                # Check for explicit title line
                title_match = re.search(r"^(?:job\s+title|role|position)[:\s]*(.+)", l, re.IGNORECASE)
                if title_match:
                    inferred_title = title_match.group(1).strip()
                    break
            if not inferred_title:
                first_clean = re.sub(r"^[#\*\-•\s]+", "", lines[0]).strip()
                if len(first_clean) < 80 and not re.search(r"about\s+us|company|overview|description", first_clean, re.IGNORECASE):
                    inferred_title = first_clean
                else:
                    inferred_title = "Target Professional Role"

        # Determine seniority
        lower_jd = jd_text.lower()
        seniority = "Mid-Level"
        for level, keywords in SENIORITY_KEYWORDS.items():
            if any(re.search(rf"\b{re.escape(k)}\b", lower_jd) for k in keywords):
                seniority = level
                break

        # Segment JD by headings
        required_skills: List[str] = []
        preferred_skills: List[str] = []
        qualifications: List[str] = []
        responsibilities: List[str] = []
        source_evidence: Dict[str, List[str]] = {
            "required": [],
            "preferred": [],
            "qualifications": [],
            "responsibilities": []
        }

        current_category = "overview"

        for line in lines:
            # Strip markdown and bullet decorators for classification
            clean_line = re.sub(r"^[#\*\-•\d\.\)\s]+", "", line).strip()
            clean_line = re.sub(r"[\*\:_]+$", "", clean_line).strip()
            line_lower = clean_line.lower()

            # Ignore title / metadata lines from polluting requirements
            if re.search(r"^(?:job\s+title|role|position|seniority|location|employment\s+type|department)[:\s]", line, re.IGNORECASE):
                continue
            if current_category == "overview" and inferred_title and (clean_line.lower() == inferred_title.lower() or re.search(r"^(?:#+\s*)?(?:senior|lead|staff|principal|junior)?\s*(?:ai|machine\s+learning|software|data|full\s+stack|backend|frontend)\s+(?:engineer|developer|scientist|architect)\b", line_lower)):
                continue

            # Header matchers (handling Markdown, colons, varied phrasing, strictly length < 55)
            if len(clean_line) < 55:
                if re.search(r"\b(preferred\s+qualifications?|preferred\s+skills?|nice\s+to\s+have|bonus|desired\s+qualifications?|additional\s+qualifications?)\b", line_lower):
                    current_category = "preferred"
                    continue
                elif re.search(r"\b(requirements?|must\s+have|minimum\s+qualifications?|basic\s+qualifications?|required\s+skills?|what\s+you('ll)?\s+need|what\s+we('re)?\s+looking\s+for|skills\s+(&|and)\s+experience|technical\s+requirements)\b", line_lower):
                    current_category = "required"
                    continue
                elif re.search(r"\b(responsibilities|duties|what\s+you('ll)?\s+do|the\s+role|day\s+to\s+day|key\s+deliverables|core\s+functions|what\s+you\s+will\s+be\s+doing)\b", line_lower):
                    current_category = "responsibilities"
                    continue
                elif re.search(r"\b(educational?\s+requirements?|academic\s+background|education|degrees?)\b", line_lower):
                    current_category = "qualifications"
                    continue
                elif re.search(r"^(about\s+(the\s+)?(us|company|team|role|our\s+mission)|company\s+overview|overview|who\s+we\s+are|benefits|perks)\b", line_lower):
                    current_category = "overview"
                    continue

            cleaned = re.sub(r"^[#\*\-•\s]+", "", line).strip()
            if not cleaned or len(cleaned) < 3:
                continue

            if current_category == "required":
                # Check for degree/education line inside requirements
                if re.search(r"\b(bachelor'?s|master'?s|degree|b\.?s|m\.?s|ph\.?d|diploma)\b", cleaned.lower()):
                    qualifications.append(cleaned)
                    source_evidence["qualifications"].append(line)
                # Only split if line is an isolated tag/token list, NOT a descriptive bullet requirement
                elif (
                    "," in cleaned 
                    and len(cleaned.split(",")) >= 3 
                    and all(len(s.strip().split()) <= 2 for s in cleaned.split(","))
                    and not re.search(r"\b(experience|proficien|knowledge|understanding|ability|degree|responsible|hands-on|strong|proven)\b", cleaned.lower())
                    and not ("(" in cleaned and ")" not in cleaned.split(",")[0])
                ):
                    sub_skills = [s.strip() for s in cleaned.split(",") if len(s.strip()) > 1]
                    required_skills.extend(sub_skills[:12])
                    source_evidence["required"].append(line)
                else:
                    required_skills.append(cleaned)
                    source_evidence["required"].append(line)
            elif current_category == "preferred":
                if (
                    "," in cleaned 
                    and len(cleaned.split(",")) >= 3 
                    and all(len(s.strip().split()) <= 2 for s in cleaned.split(","))
                    and not re.search(r"\b(experience|proficien|knowledge|understanding|ability|degree|responsible|hands-on|strong|proven)\b", cleaned.lower())
                    and not ("(" in cleaned and ")" not in cleaned.split(",")[0])
                ):
                    sub_skills = [s.strip() for s in cleaned.split(",") if len(s.strip()) > 1]
                    preferred_skills.extend(sub_skills[:10])
                else:
                    preferred_skills.append(cleaned)
                source_evidence["preferred"].append(line)
            elif current_category == "responsibilities":
                responsibilities.append(cleaned)
                source_evidence["responsibilities"].append(line)
            elif current_category == "qualifications":
                qualifications.append(cleaned)
                source_evidence["qualifications"].append(line)
            else:
                # Unstructured / Overview fallback classification based on linguistic cues
                if re.search(r"\b(bachelor'?s|master'?s|degree|b\.?s|m\.?s|ph\.?d|years\s+of\s+experience)\b", line_lower):
                    qualifications.append(cleaned)
                    source_evidence["qualifications"].append(line)
                elif re.search(r"^(build|develop|lead|design|manage|collaborate|implement|architect|maintain|deploy|spearhead|own|create|support)\b", line_lower):
                    responsibilities.append(cleaned)
                    source_evidence["responsibilities"].append(line)
                elif re.search(r"\b(experience\s+with|proficiency\s+in|knowledge\s+of|skilled\s+in|python|react|typescript|node|java|c\+\+|aws|docker|kubernetes|sql|machine\s+learning|fastapi|pytorch|transformers)\b", line_lower):
                    required_skills.append(cleaned)
                    source_evidence["required"].append(line)

        # Fallback deduplication and limits - expanded to 40 requirements to prevent artificial skill truncation
        def clean_list(items: List[str], max_len: int = 40) -> List[str]:
            seen = set()
            out = []
            for item in items:
                norm = item.strip().lower()
                if norm and norm not in seen and not re.search(r"^(requirements?|responsibilities|qualifications?)[:\s]*$", norm):
                    seen.add(norm)
                    out.append(item.strip())
            return out[:max_len]

        clean_req = clean_list(required_skills, 40)
        clean_pref = clean_list(preferred_skills, 20)
        clean_qual = clean_list(qualifications, 15)
        clean_resp = clean_list(responsibilities, 25)

        # Robust unstructured fallback: ensure requirements and responsibilities are never zero if text exists
        if not clean_req and not clean_resp and len(lines) > 2:
            for l in lines[1:]:
                cl = re.sub(r"^[#\*\-•\s]+", "", l).strip()
                if len(cl) > 15:
                    if any(verb in cl.lower() for verb in ["build", "develop", "maintain", "implement", "design", "manage", "lead"]):
                        clean_resp.append(cl)
                    else:
                        clean_req.append(cl)
            clean_req = clean_list(clean_req, 15)
            clean_resp = clean_list(clean_resp, 10)

        latency_ms = (time.time() - t0) * 1000.0

        return ATSJobDescriptionAnalysisResponse(
            jobTitle=inferred_title,
            seniorityLevel=seniority,
            requiredSkills=clean_req,
            preferredSkills=clean_pref,
            qualifications=clean_qual,
            keyResponsibilities=clean_resp,
            sourceEvidence=source_evidence,
            analysisLatencyMs=latency_ms
        )

    @classmethod
    def _match_requirement_against_pool(
        cls,
        req: str,
        category: str,
        candidate_pool: List[Dict[str, Any]],
        candidate_texts: List[str],
        cand_distilbert_vecs: Optional[np.ndarray],
        is_sparse_resume: bool
    ) -> RequirementMatch:
        """
        6-Layer Hybrid Matching System:
        Layer 1: Exact Phrase Matching (word boundaries)
        Layer 2: Normalized Lexical Matching (lowercase, stripped punctuation)
        Layer 3: Technical Entity Alias Expansion (canonical terms to variants)
        Layer 4: Pretrained DistilBERT 768-dim Semantic Cosine Embedding Matching
        Layer 5: Source Evidence Retrieval with explicit section tagging
        Layer 6: Deterministic 5-State Requirement Classification & Coursework Distinction
        """
        req_clean = req.strip()
        r_lower = req_clean.lower()
        
        # Step 1: Detect known technical entities from ontology present in requirement
        sorted_keys = sorted(TECHNICAL_ALIASES.keys(), key=lambda k: len(k), reverse=True)
        detected_entities = []
        seen_spans = []

        for k in sorted_keys:
            for al in TECHNICAL_ALIASES[k]:
                pat = rf"(?:^|[^\w\+#\.-]){re.escape(al)}(?:$|[^\w\+#\.-])"
                m = re.search(pat, r_lower)
                if m:
                    span = (m.start(), m.end())
                    if not any(s[0] <= span[0] < s[1] or s[0] < span[1] <= s[1] for s in seen_spans):
                        seen_spans.append(span)
                        detected_entities.append(k)
                        break

        if detected_entities:
            sub_terms = detected_entities
        else:
            # Fallback to delimiter splitting
            compound_delimiters = r"[,|/•]|\band\b|\bwith\b|\bor\b"
            raw_sub_terms = [t.strip() for t in re.split(compound_delimiters, req_clean, flags=re.I) if len(t.strip()) > 1]
            stopwords = {
                "experience", "with", "knowledge", "of", "proficient", "in", "strong",
                "understanding", "hands-on", "familiarity", "prior", "plus", "skills",
                "ability", "to", "demonstrated", "working", "deep", "solid", "practical"
            }
            sub_terms = []
            for st in raw_sub_terms:
                clean_st = " ".join(w for w in st.split() if w.lower() not in stopwords).strip()
                if clean_st and len(clean_st) > 1:
                    sub_terms.append(clean_st)
            if not sub_terms:
                sub_terms = [req_clean]

        matched_sub_terms: List[str] = []
        matched_evidences: List[Tuple[str, str, float, str]] = []  # (text, section, score, layer)

        # Layers 1, 2, 3: Exact, Normalized, and Alias Matching for constituent sub-terms
        for sub in sub_terms:
            sub_lower = sub.lower()
            sub_aliases = TECHNICAL_ALIASES.get(sub_lower, [sub_lower])
            sub_found = False

            for cand in candidate_pool:
                cand_text = cand["text"]
                cand_lower = cand_text.lower()
                section = cand["section"]

                for alias in sub_aliases:
                    pat = rf"(?:^|[^\w\+#\.-]){re.escape(alias)}(?:$|[^\w\+#\.-])"
                    if re.search(pat, cand_lower):
                        matched_sub_terms.append(sub)
                        matched_evidences.append((cand_text, section, 1.0, f"Layer 1/2/3: Exact/Alias '{alias}'"))
                        sub_found = True
                        break
                if sub_found:
                    break

        # Check if exact/alias sub-term matches succeeded
        if matched_sub_terms:
            ratio = len(matched_sub_terms) / len(sub_terms)
            top_ev = matched_evidences[0]
            ev_text, ev_sec, _, layer_info = top_ev

            # Section Tag mapping
            section_tag_map = {
                "skills": "[Technical Skill]",
                "projects": "[Project Evidence]",
                "experience": "[Work Experience]",
                "internships": "[Work Experience]",
                "education": "[Education Evidence]",
                "coursework": "[Coursework Evidence]",
                "certifications": "[Certification Evidence]",
                "summary": "[Summary Evidence]"
            }

            # Coursework vs. Work Experience distinction rule:
            # If the ONLY matches are from coursework, strictly map to partially_supported
            all_coursework = all(sec == "coursework" for _, sec, _, _ in matched_evidences)

            if all_coursework or ev_sec == "coursework":
                status = "partially_supported"
                status_label = "Partially Supported (Academic Coursework)"
                sim_score = 0.65
                audit_note = "Academic coursework knowledge identified in candidate resume (academic study vs commercial experience)."
            elif ratio >= 0.99 or len(sub_terms) == 1:
                status = "explicitly_matched"
                status_label = "Explicit Match"
                sim_score = 0.95
                audit_note = f"Direct technical match verified ({', '.join(matched_sub_terms)})."
            elif ratio >= 0.49:
                status = "partially_supported"
                status_label = f"Partially Supported ({len(matched_sub_terms)}/{len(sub_terms)} skills verified)"
                sim_score = float(round(0.50 + 0.35 * ratio, 3))
                missing_sub = [s for s in sub_terms if s not in matched_sub_terms]
                audit_note = f"Verified: {', '.join(matched_sub_terms)} | Not found in text: {', '.join(missing_sub)}."
            else:
                status = "partially_supported"
                status_label = f"Partially Supported ({len(matched_sub_terms)}/{len(sub_terms)} skills verified)"
                sim_score = float(round(0.50 + 0.20 * ratio, 3))
                missing_sub = [s for s in sub_terms if s not in matched_sub_terms]
                audit_note = f"Minor skill overlap ({', '.join(matched_sub_terms)}) | Not found: {', '.join(missing_sub)}."

            evidence_items = []
            for txt, sec, _, _ in matched_evidences[:4]:
                tag = section_tag_map.get(sec, f"[{sec.upper()}]")
                evidence_items.append(f"{tag} {txt}")

            return RequirementMatch(
                requirement=req_clean,
                category=category,
                status=status,
                statusLabel=status_label,
                similarityScore=sim_score,
                resumeEvidence=" | ".join(evidence_items),
                jdEvidence=req_clean,
                auditNote=audit_note
            )

        # Layer 4: Semantic Embedding Matching via Pretrained DistilBERT
        if cand_distilbert_vecs is not None and len(cand_distilbert_vecs) > 0:
            req_vec = compute_distilbert_embeddings([req_clean])
            if req_vec is not None:
                sims = np.dot(cand_distilbert_vecs, req_vec.T).squeeze()
                best_idx = int(np.argmax(sims))
                semantic_sim = float(sims[best_idx])
                best_cand = candidate_pool[best_idx]
                best_text = best_cand["text"]
                best_sec = best_cand["section"]

                section_tag_map = {
                    "skills": "[Technical Skill]",
                    "projects": "[Project Evidence]",
                    "experience": "[Work Experience]",
                    "internships": "[Work Experience]",
                    "education": "[Education Evidence]",
                    "coursework": "[Coursework Evidence]",
                    "certifications": "[Certification Evidence]",
                    "summary": "[Summary Evidence]"
                }
                tag = section_tag_map.get(best_sec, f"[{best_sec.upper()}]")

                if semantic_sim >= 0.72:
                    return RequirementMatch(
                        requirement=req_clean,
                        category=category,
                        status="explicitly_matched",
                        statusLabel="Explicit Match (Semantic)",
                        similarityScore=float(round(semantic_sim, 3)),
                        resumeEvidence=f"{tag} {best_text}",
                        jdEvidence=req_clean,
                        auditNote=f"High semantic alignment ({semantic_sim:.2f}) identified via DistilBERT representation."
                    )
                elif semantic_sim >= 0.50:
                    return RequirementMatch(
                        requirement=req_clean,
                        category=category,
                        status="partially_supported",
                        statusLabel="Partially Supported (Semantic)",
                        similarityScore=float(round(semantic_sim, 3)),
                        resumeEvidence=f"{tag} {best_text}",
                        jdEvidence=req_clean,
                        auditNote=f"Moderate semantic correlation ({semantic_sim:.2f}) identified in resume."
                    )

        # Fallback to TF-IDF Cosine Similarity if DistilBERT did not produce match or was unavailable
        if candidate_texts:
            try:
                corpus = [req_clean] + candidate_texts
                vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1)
                tfidf_mat = vectorizer.fit_transform(corpus)
                tfidf_sims = cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:])[0]
                best_idx = int(np.argmax(tfidf_sims))
                tfidf_score = float(tfidf_sims[best_idx])
                best_cand = candidate_pool[best_idx]
                tag = f"[{best_cand['section'].upper()}]"

                if tfidf_score >= 0.70:
                    return RequirementMatch(
                        requirement=req_clean,
                        category=category,
                        status="explicitly_matched",
                        statusLabel="Explicit Match (TF-IDF)",
                        similarityScore=float(round(tfidf_score, 3)),
                        resumeEvidence=f"{tag} {best_cand['text']}",
                        jdEvidence=req_clean,
                        auditNote=f"Lexical n-gram match ({tfidf_score:.2f}) verified in candidate resume."
                    )
                elif tfidf_score >= 0.45:
                    return RequirementMatch(
                        requirement=req_clean,
                        category=category,
                        status="partially_supported",
                        statusLabel="Partially Supported (TF-IDF)",
                        similarityScore=float(round(tfidf_score, 3)),
                        resumeEvidence=f"{tag} {best_cand['text']}",
                        jdEvidence=req_clean,
                        auditNote=f"Partial lexical overlap ({tfidf_score:.2f}) identified."
                    )
            except Exception:
                pass

        # Layer 6: Inconclusive / Not Found Handling
        if is_sparse_resume:
            return RequirementMatch(
                requirement=req_clean,
                category=category,
                status="uncertain_extraction",
                statusLabel="Uncertain Extraction",
                similarityScore=0.0,
                resumeEvidence=None,
                jdEvidence=req_clean,
                auditNote="Inconclusive extraction: candidate resume section contains minimal or unparsed text."
            )
        else:
            return RequirementMatch(
                requirement=req_clean,
                category=category,
                status="not_found_in_resume",
                statusLabel="Not Found in Text",
                similarityScore=0.0,
                resumeEvidence=None,
                jdEvidence=req_clean,
                auditNote="Requirement not located in provided resume text (Candidate verification recommended)."
            )

    @classmethod
    def match_resume(
        cls,
        jd_analysis: ATSJobDescriptionAnalysisResponse,
        resume_data: Optional[Any] = None,
        parsed_resume: Optional[Dict[str, Any]] = None,
        raw_jd_text: str = ""
    ) -> ATSMatchResponse:
        """
        Performs 6-layer hybrid semantic matching across all JD requirements against resume content,
        calculates Part A and Part B ATS scores, and catalogs strong/partial/missing matches.
        """
        # Collect candidate evidence pool with section tags
        candidate_pool: List[Dict[str, Any]] = []
        candidate_skills: List[str] = []
        candidate_action_lines: List[str] = []
        has_metrics_count = 0
        total_bullet_count = 0

        # Support both Pydantic model and dict
        if resume_data is not None:
            if isinstance(resume_data, dict):
                try:
                    resume_obj = ResumeFullData.model_validate(resume_data)
                except Exception:
                    resume_obj = None
            elif isinstance(resume_data, ResumeFullData):
                resume_obj = resume_data
            else:
                resume_obj = None

            if resume_obj:
                # 1. Skills
                skills_dict = resume_obj.skills.model_dump()
                for cat, skl_list in skills_dict.items():
                    for s in skl_list:
                        candidate_skills.append(s)
                        candidate_pool.append({"text": s, "section": "skills", "type": "technical_skill"})

                # 2. Experience
                for exp in resume_obj.experience:
                    candidate_pool.append({"text": f"{exp.role} at {exp.company}", "section": "experience", "type": "work_experience"})
                    for resp in exp.responsibilities:
                        candidate_pool.append({"text": resp, "section": "experience", "type": "work_experience"})
                        candidate_action_lines.append(resp)
                        total_bullet_count += 1
                        if re.search(r"(\d+%|\$\d+|\d+\+|\b\d+\b)", resp):
                            has_metrics_count += 1

                # 3. Internships
                for intern in resume_obj.internships:
                    candidate_pool.append({"text": f"{intern.role} at {intern.organization}", "section": "internships", "type": "work_experience"})
                    for wp in intern.workPerformed:
                        candidate_pool.append({"text": wp, "section": "internships", "type": "work_experience"})
                        candidate_action_lines.append(wp)
                        total_bullet_count += 1
                        if re.search(r"(\d+%|\$\d+|\d+\+|\b\d+\b)", wp):
                            has_metrics_count += 1

                # 4. Projects
                for proj in resume_obj.projects:
                    tech_desc = f", Tech: {', '.join(proj.technologies)}" if proj.technologies else ""
                    candidate_pool.append({
                        "text": f"Project {proj.title}{tech_desc}: {proj.description}",
                        "section": "projects",
                        "type": "project"
                    })
                    for tech in proj.technologies:
                        candidate_pool.append({"text": tech, "section": "projects", "type": "project_technology"})
                    for c in proj.contributions:
                        candidate_pool.append({
                            "text": f"Project {proj.title}: {c}",
                            "section": "projects",
                            "type": "project"
                        })
                        candidate_action_lines.append(c)
                        total_bullet_count += 1
                        if re.search(r"(\d+%|\$\d+|\d+\+|\b\d+\b)", c):
                            has_metrics_count += 1

                # 5. Education & Coursework
                for edu in resume_obj.education:
                    candidate_pool.append({
                        "text": f"{edu.degree} in {edu.fieldOfStudy} at {edu.institution} ({edu.grade or ''})",
                        "section": "education",
                        "type": "education"
                    })
                    for cw in edu.coursework:
                        candidate_pool.append({"text": cw, "section": "coursework", "type": "coursework"})

                # 6. Certifications
                for cert in resume_obj.certifications:
                    candidate_pool.append({
                        "text": f"Certification: {cert.name} by {cert.issuingOrganization}",
                        "section": "certifications",
                        "type": "certification"
                    })

                # 7. Summary
                if resume_obj.personalInfo and resume_obj.personalInfo.summary:
                    candidate_pool.append({"text": resume_obj.personalInfo.summary, "section": "summary", "type": "summary"})

        elif parsed_resume:
            raw_sections = parsed_resume.get("rawSections", {})
            for sec, lines in raw_sections.items():
                for l in lines:
                    candidate_pool.append({"text": l, "section": sec, "type": sec})
                    if sec in ["experience", "projects", "internships"]:
                        candidate_action_lines.append(l)
                        total_bullet_count += 1
                        if re.search(r"(\d+%|\$\d+|\d+\+|\b\d+\b)", l):
                            has_metrics_count += 1
            for s in parsed_resume.get("skills", []):
                candidate_skills.append(s)
                candidate_pool.append({"text": s, "section": "skills", "type": "technical_skill"})
            for cw in parsed_resume.get("relevantCoursework", []):
                candidate_pool.append({"text": cw, "section": "coursework", "type": "coursework"})
            for inv in parsed_resume.get("candidateSkillsInventory", []):
                sec = "coursework" if inv.get("category") == "coursework" else "skills"
                candidate_pool.append({"text": inv.get("skill", ""), "section": sec, "type": inv.get("category", "skill")})

        # Candidate texts and pre-computed DistilBERT embeddings
        candidate_texts = [c["text"] for c in candidate_pool]
        is_sparse_resume = len(candidate_pool) < 4 or len(candidate_skills) == 0

        # Precompute DistilBERT embeddings for candidate texts
        cand_distilbert_vecs = compute_distilbert_embeddings(candidate_texts)

        explicit_matches: List[RequirementMatch] = []
        partial_matches: List[RequirementMatch] = []
        not_found_requirements: List[RequirementMatch] = []
        uncertain_extractions: List[RequirementMatch] = []
        confirmed_missing: List[RequirementMatch] = []

        def route_match(m: RequirementMatch):
            if m.status == "explicitly_matched":
                explicit_matches.append(m)
            elif m.status == "partially_supported":
                partial_matches.append(m)
            elif m.status == "uncertain_extraction":
                uncertain_extractions.append(m)
            elif m.status == "confirmed_missing":
                confirmed_missing.append(m)
            else:
                not_found_requirements.append(m)

        # 1. Match Required Skills (Max 25 pts)
        req_skill_scores = []
        for req in jd_analysis.requiredSkills:
            m = cls._match_requirement_against_pool(
                req=req,
                category="required_skill",
                candidate_pool=candidate_pool,
                candidate_texts=candidate_texts,
                cand_distilbert_vecs=cand_distilbert_vecs,
                is_sparse_resume=is_sparse_resume
            )
            req_skill_scores.append(m.similarityScore)
            route_match(m)

        req_score_avg = np.mean(req_skill_scores) if req_skill_scores else 0.5
        part_a_req_skills = float(round(min(25.0, max(0.0, req_score_avg * 25.0)), 1))

        # 2. Match Preferred Skills (Max 10 pts)
        pref_skill_scores = []
        for pref in jd_analysis.preferredSkills:
            m = cls._match_requirement_against_pool(
                req=pref,
                category="preferred_skill",
                candidate_pool=candidate_pool,
                candidate_texts=candidate_texts,
                cand_distilbert_vecs=cand_distilbert_vecs,
                is_sparse_resume=is_sparse_resume
            )
            pref_skill_scores.append(m.similarityScore)
            route_match(m)

        pref_score_avg = np.mean(pref_skill_scores) if pref_skill_scores else 0.5
        part_a_pref_skills = float(round(min(10.0, max(0.0, pref_score_avg * 10.0)), 1))

        # 3. Match Responsibilities (Max 15 pts)
        resp_scores = []
        for resp in jd_analysis.keyResponsibilities:
            m = cls._match_requirement_against_pool(
                req=resp,
                category="responsibility",
                candidate_pool=candidate_pool,
                candidate_texts=candidate_texts,
                cand_distilbert_vecs=cand_distilbert_vecs,
                is_sparse_resume=is_sparse_resume
            )
            resp_scores.append(m.similarityScore)
            route_match(m)

        resp_score_avg = np.mean(resp_scores) if resp_scores else 0.5
        part_a_responsibilities = float(round(min(15.0, max(0.0, resp_score_avg * 15.0)), 1))

        # 4. Match Qualifications (Max 10 pts)
        qual_scores = []
        for qual in jd_analysis.qualifications:
            m = cls._match_requirement_against_pool(
                req=qual,
                category="qualification",
                candidate_pool=candidate_pool,
                candidate_texts=candidate_texts,
                cand_distilbert_vecs=cand_distilbert_vecs,
                is_sparse_resume=is_sparse_resume
            )
            qual_scores.append(m.similarityScore)
            route_match(m)

        qual_score_avg = np.mean(qual_scores) if qual_scores else 0.6
        part_a_qualifications = float(round(min(10.0, max(0.0, qual_score_avg * 10.0)), 1))

        total_part_a = float(round(part_a_req_skills + part_a_pref_skills + part_a_responsibilities + part_a_qualifications, 1))

        # =====================================================================
        # PART B: RESUME DOCUMENT QUALITY (Max 40 pts)
        # =====================================================================
        # 1. Action Verbs & Impact Metrics (Max 15 pts)
        action_verb_count = 0
        for line in candidate_action_lines:
            tokens = [t.lower() for t in re.findall(r"\b[a-zA-Z]{3,}\b", line)]
            if tokens and tokens[0] in ACTION_VERBS:
                action_verb_count += 1

        action_verb_ratio = (action_verb_count / max(1, total_bullet_count)) if total_bullet_count > 0 else 0.5
        metric_ratio = (has_metrics_count / max(1, total_bullet_count)) if total_bullet_count > 0 else 0.4
        
        part_b_action_impact = float(round(min(15.0, (action_verb_ratio * 8.0) + (metric_ratio * 7.0)), 1))

        # 2. Formatting & ATS Parseability (Max 10 pts)
        has_contact = False
        if resume_data:
            if isinstance(resume_data, ResumeFullData):
                has_contact = bool(resume_data.personalInfo.email and resume_data.personalInfo.phone)
            elif isinstance(resume_data, dict):
                has_contact = bool(resume_data.get("personalInfo", {}).get("email"))
        elif parsed_resume:
            has_contact = bool(parsed_resume.get("personalInfo", {}).get("email"))

        formatting_score = 7.0
        if has_contact:
            formatting_score += 2.0
        if total_bullet_count >= 4:
            formatting_score += 1.0
        part_b_formatting = float(round(min(10.0, formatting_score), 1))

        # 3. Section Completeness & Balance (Max 15 pts)
        completeness_pts = 0.0
        if resume_data:
            if isinstance(resume_data, ResumeFullData):
                if resume_data.education: completeness_pts += 3.0
                if candidate_skills: completeness_pts += 4.0
                if resume_data.experience or resume_data.internships: completeness_pts += 5.0
                if resume_data.projects: completeness_pts += 3.0
            elif isinstance(resume_data, dict):
                if resume_data.get("education"): completeness_pts += 3.0
                if candidate_skills: completeness_pts += 4.0
                if resume_data.get("experience") or resume_data.get("internships"): completeness_pts += 5.0
                if resume_data.get("projects"): completeness_pts += 3.0
        elif parsed_resume:
            sec_counts = parsed_resume.get("sectionBreakdown", {})
            if sec_counts.get("educationCount", 0) > 0: completeness_pts += 3.0
            if sec_counts.get("skillsCount", 0) > 0: completeness_pts += 4.0
            if sec_counts.get("experienceCount", 0) > 0: completeness_pts += 5.0
            if sec_counts.get("projectsCount", 0) > 0: completeness_pts += 3.0
        else:
            completeness_pts = 8.0

        part_b_completeness = float(round(min(15.0, completeness_pts), 1))

        total_part_b = float(round(part_b_action_impact + part_b_formatting + part_b_completeness, 1))

        overall_ats_score = float(round(total_part_a + total_part_b, 1))

        # Strengths & Critical Gaps
        strengths = []
        if part_a_req_skills >= 18.0:
            strengths.append(f"Strong coverage of core technical requirements ({part_a_req_skills}/25 pts).")
        if part_b_action_impact >= 10.0:
            strengths.append(f"Effective use of high-impact action verbs and quantified deliverables ({part_b_action_impact}/15 pts).")
        if explicit_matches:
            strengths.append(f"Direct semantic alignment found on {len(explicit_matches)} explicit target job requirements.")

        critical_gaps = []
        if not_found_requirements:
            sample_not_found = [m.requirement for m in not_found_requirements[:3]]
            critical_gaps.append(f"Not found in resume text: {', '.join(sample_not_found)} (Candidate verification recommended).")
        if uncertain_extractions:
            critical_gaps.append(f"{len(uncertain_extractions)} requirements could not be confirmed due to concise or ambiguous section extraction.")
        if part_b_action_impact < 9.0:
            critical_gaps.append("Low action verb density and limited quantified metrics in project/experience bullets.")
        if not candidate_skills or len(candidate_skills) < 5:
            critical_gaps.append("Skills inventory appears incomplete or lacks categorization.")

        explanation = (
            f"Evaluated via Elevate X Internal Compatibility Rubric: Part A Job Requirement Alignment achieved {total_part_a}/60 points "
            f"based on 6-layer hybrid matching across required skills ({part_a_req_skills}/25), preferred skills ({part_a_pref_skills}/10), "
            f"responsibilities ({part_a_responsibilities}/15), and qualifications ({part_a_qualifications}/10). "
            f"Part B Document Quality scored {total_part_b}/40 points based on action verbs/metrics ({part_b_action_impact}/15), "
            f"ATS parseability ({part_b_formatting}/10), and section completeness ({part_b_completeness}/15). "
            f"Total Internal Compatibility Score is {overall_ats_score}/100."
        )

        breakdown = ATSScoreBreakdown(
            rubricName="Elevate X Internal Compatibility Rubric (Deterministic 100-Point Audit)",
            partAScore=total_part_a,
            partBScore=total_part_b,
            totalScore=overall_ats_score,
            partADetails=PartADetails(
                requiredSkillsScore=part_a_req_skills,
                preferredSkillsScore=part_a_pref_skills,
                responsibilitiesScore=part_a_responsibilities,
                qualificationsScore=part_a_qualifications
            ),
            partBDetails=PartBDetails(
                actionVerbsAndImpactScore=part_b_action_impact,
                formattingAndParseabilityScore=part_b_formatting,
                sectionCompletenessScore=part_b_completeness
            ),
            explanation=explanation,
            methodologyDisclaimer=(
                "This score is an internal deterministic algorithmic audit based on text similarity and document structure. "
                "It is not an official or proprietary vendor ATS algorithm."
            )
        )

        all_missing_legacy = not_found_requirements + uncertain_extractions + confirmed_missing

        return ATSMatchResponse(
            overallScore=overall_ats_score,
            breakdown=breakdown,
            explicitMatches=explicit_matches,
            partialMatches=partial_matches,
            notFoundRequirements=not_found_requirements,
            uncertainExtractions=uncertain_extractions,
            confirmedMissing=confirmed_missing,
            # Backwards compatibility
            strongMatches=explicit_matches,
            missingRequirements=all_missing_legacy,
            strengthsSummary=strengths or ["Document exhibits good baseline structure."],
            criticalGapsSummary=critical_gaps or ["No critical structural gaps detected."],
            evaluatedAt=datetime.utcnow().isoformat()
        )
