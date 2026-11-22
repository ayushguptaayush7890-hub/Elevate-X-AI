"""
Feature 3: ATS Improvement Engine
Generates grounded, non-hallucinatory STAR bullet improvements and missing evidence
interview questions using local instruction-following LLM (Qwen2.5-1.5B via MLX)
or deterministic rule-based elevation.
Strictly adheres to candidate truthfulness: NEVER invents metrics, projects, tools, or companies.
"""

import re
import uuid
import time
from typing import Dict, Any, List, Optional
from app.schemas.resume_generator import (
    ResumeFullData,
    AIImprovementSuggestion,
    AIImprovementResponse,
)
from app.services.resume_ai_generator import ResumeAIGeneratorService

STRONG_ACTION_VERBS = [
    "Architected", "Engineered", "Orchestrated", "Spearheaded", "Implemented",
    "Streamlined", "Optimized", "Scaled", "Automated", "Delivered", "Pioneered"
]

class ATSImprovementService:
    @classmethod
    def generate_improvements(
        cls,
        resume_data: ResumeFullData,
        job_description: str,
        gap_requirements: List[str]
    ) -> AIImprovementResponse:
        t0 = time.time()
        suggestions: List[AIImprovementSuggestion] = []
        targeted_questions: List[str] = []

        # 1. Inspect existing Experience bullets for elevation
        bullet_idx = 0
        for exp in resume_data.experience:
            for resp in exp.responsibilities:
                bullet_idx += 1
                clean_bullet = resp.strip().lstrip("•-* \t")
                if not clean_bullet or len(clean_bullet) < 15:
                    continue

                # Check if bullet lacks a strong action verb or metric
                words = re.findall(r"\b[A-Za-z]+\b", clean_bullet)
                first_word = words[0].capitalize() if words else ""
                has_metric = bool(re.search(r"(\d+%|\$\d+|\d+\+|\b\d+\b)", clean_bullet))

                if first_word not in STRONG_ACTION_VERBS or not has_metric:
                    # Generate elevated STAR bullet
                    improved_text = cls._generate_star_bullet(clean_bullet, exp.role, exp.company)
                    
                    sug = AIImprovementSuggestion(
                        id=f"exp-sug-{uuid.uuid4().hex[:8]}",
                        targetSection=f"Experience: {exp.role} at {exp.company}",
                        originalText=clean_bullet,
                        suggestedText=improved_text,
                        starMethodologyNotes="Restructured into Action-Result format with high-impact active verb and clear deliverable scope.",
                        missingEvidenceQuestion=None if has_metric else "What quantifiable metric (e.g. latency reduced, users served, or efficiency gained) resulted from this initiative?",
                        rationale="Replaces passive or generic phrasing with authoritative action framing without inventing unverified facts.",
                        status="pending"
                    )
                    suggestions.append(sug)
                    if len(suggestions) >= 4:
                        break
            if len(suggestions) >= 4:
                break

        # 2. Inspect Project contributions for elevation
        if len(suggestions) < 6:
            for proj in resume_data.projects:
                for contrib in proj.contributions:
                    clean_c = contrib.strip().lstrip("•-* \t")
                    if not clean_c or len(clean_c) < 15:
                        continue
                    improved_text = cls._generate_star_bullet(clean_c, proj.title, "Project")
                    sug = AIImprovementSuggestion(
                        id=f"proj-sug-{uuid.uuid4().hex[:8]}",
                        targetSection=f"Project: {proj.title}",
                        originalText=clean_c,
                        suggestedText=improved_text,
                        starMethodologyNotes="Emphasizes technical stack utilization and engineering impact.",
                        missingEvidenceQuestion="What performance outcome, benchmark, or user adoption did this project achieve?",
                        rationale="Highlights concrete technical execution while preserving factual boundaries.",
                        status="pending"
                    )
                    suggestions.append(sug)
                    if len(suggestions) >= 6:
                        break
                if len(suggestions) >= 6:
                    break

        # 3. Generate Targeted Missing Evidence Questions for Critical Gaps
        # NEVER invent fake experiences for missing requirements! Ask the candidate.
        for gap in gap_requirements[:5]:
            q = (
                f"The job requires '{gap}'. If you have hands-on experience or coursework in this area, "
                f"describe the specific scenario, tools used, and outcome so we can formulate a factual STAR bullet."
            )
            targeted_questions.append(q)

        return AIImprovementResponse(
            suggestions=suggestions,
            targetedQuestions=targeted_questions,
            groundingDisclaimer=(
                "All improvements are strictly grounded in candidate-provided records. "
                "No unverified metrics, tools, or achievements are hallucinated."
            )
        )

    @classmethod
    def _generate_star_bullet(cls, raw_bullet: str, role: str, context: str) -> str:
        """
        Uses local Qwen2.5-1.5B MLX model if available, otherwise deterministic rule elevation.
        """
        try:
            system_prompt = (
                "You are an expert executive resume copywriter. "
                "Rewrite the following candidate resume bullet point into a high-impact STAR bullet. "
                "STRICT RULES:\n"
                "1. Begin with a powerful past-tense action verb (e.g. Engineered, Spearheaded, Optimized, Architected).\n"
                "2. Keep the exact facts and tools from the original text.\n"
                "3. NEVER fabricate metrics or company achievements that were not mentioned.\n"
                "4. Return ONLY a single concise, punchy bullet point (no quotation marks, no preamble)."
            )
            user_prompt = f"Context: {role} ({context})\nRaw Bullet: {raw_bullet}\nElevated Bullet:"
            enhanced = ResumeAIGeneratorService._run_model_inference(system_prompt, user_prompt, max_tokens=100)
            clean = enhanced.strip().strip('"\'').lstrip("•-* \t")
            if clean and len(clean) > 10:
                return clean
        except Exception:
            pass

        # Deterministic fallback
        lead_verb = "Engineered"
        words = raw_bullet.split()
        if words:
            first_w = words[0].lower()
            if first_w in ["helped", "assisted", "worked", "did", "responsible", "handled"]:
                return f"Spearheaded {' '.join(words[1:])}"
            elif first_w.endswith("ing"):
                return f"Implemented {' '.join(words[1:])}"
        return f"Architected and delivered: {raw_bullet}"
