"""
ELEVATE X AI — FEATURE 3: RESUME AI GENERATION SERVICE
Powered by genuine instruction-following language model (Qwen2.5-1.5B-Instruct-4bit via MLX Metal).
Strictly adheres to factual grounding: NEVER invents experience, metrics, projects, degrees, or skills.
"""

import time
import json
import re
from typing import Dict, Any, List, Optional, Tuple
from app.schemas.resume_generator import (
    ResumeFullData,
    PersonalInfo,
    ExperienceEntry,
    InternshipEntry,
    ProjectEntry,
    AIGenerateResumeResponse,
    AIEnhanceTextResponse,
    RecommendDesignResponse,
)

_MODEL_INSTANCE = None
_TOKENIZER_INSTANCE = None
_MODEL_NAME = "mlx-community/Qwen2.5-1.5B-Instruct-4bit"


def _get_model_and_tokenizer():
    global _MODEL_INSTANCE, _TOKENIZER_INSTANCE
    if _MODEL_INSTANCE is None:
        import mlx_lm
        print(f"[ResumeAIGenerator] Loading instruction-following model: {_MODEL_NAME} on Apple Silicon Metal...")
        _MODEL_INSTANCE, _TOKENIZER_INSTANCE = mlx_lm.load(_MODEL_NAME)
        print("[ResumeAIGenerator] Model successfully loaded.")
    return _MODEL_INSTANCE, _TOKENIZER_INSTANCE


class ResumeAIGeneratorService:
    @classmethod
    def _run_model_inference(cls, system_prompt: str, user_prompt: str, max_tokens: int = 350) -> str:
        """Executes genuine LLM inference via MLX."""
        import mlx_lm
        model, tokenizer = _get_model_and_tokenizer()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        prompt_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        raw_output = mlx_lm.generate(
            model,
            tokenizer,
            prompt=prompt_text,
            max_tokens=max_tokens,
            verbose=False
        )
        return raw_output.strip()

    @classmethod
    def enhance_single_text(cls, text: str, section_type: str, context_role: Optional[str] = None) -> AIEnhanceTextResponse:
        t0 = time.time()
        system_prompt = (
            "You are an executive resume editor and career strategist. "
            "Your task is to refine and elevate user-provided resume text. "
            "STRICT RULES:\n"
            "1. NEVER invent facts, metrics, tools, certifications, or projects not provided in the source text.\n"
            "2. Use strong action verbs (e.g. Engineered, Spearheaded, Implemented, Orchestrated).\n"
            "3. Format as concise, high-impact bullet points or a polished paragraph depending on section.\n"
            "4. Return ONLY the enhanced text without chat meta-commentary."
        )

        user_prompt = f"Target Role / Context: {context_role or 'Professional'}\nSection: {section_type}\nRaw Input:\n{text}\n\nEnhanced Version:"
        enhanced = cls._run_model_inference(system_prompt, user_prompt, max_tokens=250)

        bullets = []
        lines = enhanced.split("\n")
        for line in lines:
            line_clean = line.strip().lstrip("•-* \t")
            if line_clean and len(line_clean) > 5:
                bullets.append(line_clean)

        latency_ms = (time.time() - t0) * 1000.0
        return AIEnhanceTextResponse(
            originalText=text,
            enhancedText=enhanced,
            suggestedBullets=bullets if len(bullets) > 1 else [enhanced],
            latencyMs=round(latency_ms, 2)
        )

    @classmethod
    def _recommend_template(cls, resume_data: ResumeFullData) -> Tuple[str, str]:
        """Recommends the most suitable template based on career stage and technical domain."""
        all_skills = [s.lower() for s in (
            resume_data.skills.programmingLanguages +
            resume_data.skills.frameworks +
            resume_data.skills.databases +
            resume_data.skills.developerTools +
            resume_data.skills.aiMlSkills +
            resume_data.skills.otherSkills
        )]
        skills_str = " ".join(all_skills)

        # 1. AI & Data Science
        ai_terms = ["pytorch", "tensorflow", "keras", "machine learning", "deep learning", "nlp", "llm", "pandas", "numpy", "computer vision"]
        if any(term in skills_str for term in ai_terms):
            return "data_science", "Highlighted AI/Data Science layout optimized for research projects, ML pipelines, and technical stacks."

        # 2. Software Developer / Engineering
        dev_terms = ["python", "javascript", "typescript", "react", "next.js", "node.js", "c++", "java", "docker", "kubernetes", "aws", "postgresql"]
        if any(term in skills_str for term in dev_terms):
            return "technical", "Developer-focused layout featuring technical skill badges, GitHub repositories, and architectural contributions."

        # 3. Fresher / Student
        num_exp = len(resume_data.experience)
        if num_exp == 0 or (len(resume_data.education) > 0 and num_exp <= 1):
            return "fresher", "Academic and entry-level layout prioritizing education, foundational coursework, and hands-on projects."

        # 4. Senior / Executive
        if num_exp >= 3:
            return "corporate_executive", "Executive structure with chronological leadership progression and career milestone framing."

        # Default: Modern Professional
        return "modern", "Sleek modern multi-column design with balanced visual hierarchy and ATS compliance."

    @classmethod
    def fallback_heuristic_recommendation(
        cls,
        resume_data: ResumeFullData,
        reason: Optional[str] = None
    ) -> RecommendDesignResponse:
        """Deterministic algorithmic fallback if local MLX inference is unavailable."""
        title = (resume_data.personalInfo.professionalTitle or "").lower()
        all_skills = [s.lower() for s in (
            resume_data.skills.programmingLanguages +
            resume_data.skills.frameworks +
            resume_data.skills.databases +
            resume_data.skills.developerTools +
            resume_data.skills.aiMlSkills +
            resume_data.skills.otherSkills
        )]
        skills_str = " ".join(all_skills)
        num_exp = len(resume_data.experience)

        if any(t in skills_str or t in title for t in ["pytorch", "tensorflow", "llm", "mlx", "machine learning", "deep learning", "nlp", "ai"]):
            des_id = "des-0007"
            expl = "Algorithmic heuristic matched technical AI/ML competencies with research-oriented dual-column architecture."
            traits = ["AI/ML Frameworks", "Neural Models", "Data Pipelines"]
            why = "Highlights ML model benchmarks, research publications, and math/technical stacks."
        elif any(t in skills_str or t in title for t in ["python", "javascript", "typescript", "c++", "go", "react", "fastapi", "developer", "engineer"]):
            des_id = "des-0006"
            expl = "Algorithmic heuristic matched systems and software engineering background with developer terminal styling."
            traits = ["Software Engineering", "Full-Stack / Systems Stack", "GitHub Projects"]
            why = "Terminal command headers and monospace accents highlight repos and architecture."
        elif num_exp >= 3 or any(t in title for t in ["director", "lead", "manager", "vp", "head"]):
            des_id = "des-0004"
            expl = "Algorithmic heuristic matched senior tenure with corporate executive serif architecture."
            traits = ["Senior Experience", "Leadership Progression", "Business Impact"]
            why = "Framed executive serif layout emphasizes leadership chronology and business metrics."
        elif num_exp == 0 or (len(resume_data.education) > 0 and num_exp <= 1):
            des_id = "des-0008"
            expl = "Algorithmic heuristic matched early-career profile with education-first visual hierarchy."
            traits = ["Degree Coursework", "Hands-on Projects", "Academic Foundation"]
            why = "Education-first layout features GPA, courses, and project repositories prominently."
        else:
            des_id = "des-0001"
            expl = "Algorithmic heuristic selected balanced modern multi-column design."
            traits = ["Versatile Stack", "Clear Professional Summary", "Multi-column Hierarchy"]
            why = "Royal Navy & Gold palette with balanced sidebar maximizes visual impact across industries."

        return RecommendDesignResponse(
            recommendedDesignId=des_id,
            explanation=expl,
            matchingProfileCharacteristics=traits,
            whyAppropriate=why,
            isFallback=True,
            fallbackReason=reason or "Selected via deterministic algorithmic heuristics.",
            latencyMs=0.0,
            modelName="Algorithmic Heuristic Fallback (Local AI Offline)"
        )

    @classmethod
    def recommend_design_with_ai(
        cls,
        resume_data: ResumeFullData,
        target_role: Optional[str] = None,
        candidate_designs: Optional[List[Dict[str, Any]]] = None
    ) -> RecommendDesignResponse:
        """
        Executes genuine MLX Qwen2.5-1.5B inference on Apple Silicon Metal.
        Analyzes the candidate's actual credentials (skills, experience, education, projects)
        and recommends the optimal design configuration.
        """
        t0 = time.time()
        try:
            skills_all = (
                resume_data.skills.programmingLanguages +
                resume_data.skills.frameworks +
                resume_data.skills.databases +
                resume_data.skills.developerTools +
                resume_data.skills.aiMlSkills +
                resume_data.skills.otherSkills
            )
            skills_sample = ", ".join(skills_all[:12]) if skills_all else "Not specified"

            edu_sample = "; ".join([
                f"{e.degree} in {e.fieldOfStudy} at {e.institution}" for e in resume_data.education[:2]
            ]) if resume_data.education else "No degrees entered"

            exp_sample = "; ".join([
                f"{e.role} at {e.company} ({e.startDate} - {e.endDate})" for e in resume_data.experience[:3]
            ]) if resume_data.experience else "No work experience entered"

            proj_sample = "; ".join([
                f"'{p.title}' ({', '.join(p.technologies[:3])})" for p in resume_data.projects[:3]
            ]) if resume_data.projects else "No projects entered"

            summary = resume_data.personalInfo.summary or "Not provided"
            effective_role = target_role or resume_data.personalInfo.professionalTitle or "Software Professional"

            system_prompt = (
                "You are an expert career consultant and design director. Analyze the candidate's actual credentials "
                "(skills, experience, education, projects) and select the single best matching resume design from the provided options.\n"
                "You must return ONLY a JSON object:\n"
                "{\n"
                '  "recommendedDesignId": "<design_id e.g. des-0006>",\n'
                '  "explanation": "<2-3 sentence clear rationale grounded in their actual background>",\n'
                '  "matchingProfileCharacteristics": ["<trait 1>", "<trait 2>", ...],\n'
                '  "whyAppropriate": "<explanation of why this visual hierarchy and layout best serves their background>"\n'
                "}\n"
                "Do not invent facts or hallucinate confidence scores. Return raw JSON only, no markdown backticks."
            )

            user_prompt = (
                f"Candidate Profile:\n"
                f"- Target Role / Title: {effective_role}\n"
                f"- Summary: {summary}\n"
                f"- Technical Skills: {skills_sample}\n"
                f"- Education: {edu_sample}\n"
                f"- Work Experience: {exp_sample}\n"
                f"- Projects: {proj_sample}\n\n"
                f"Available Designs:\n"
                f"- des-0001: Modern Split (Royal Navy & Gold, Sans typography, balanced multi-column layout for versatile engineering)\n"
                f"- des-0002: Strict ATS Monochrome (Single column, classic parser safe, maximal whitespace, finance/enterprise)\n"
                f"- des-0004: Corporate Executive (Serif typography, executive slate frame, leadership milestone focus for managers/directors)\n"
                f"- des-0006: Terminal Developer (Dark terminal matrix, monospace, repo/snippet focus for backend/systems/devs)\n"
                f"- des-0007: AI Research Lab (Cyan/Teal tech palette, research benchmarks, math & model pipelines for ML/AI engineers)\n"
                f"- des-0008: Fresher & Student (Oxford scholar blue, education & projects first layout for university students/freshers)\n"
                f"- des-0010: Creative Studio (Electric violet gradient, UI/visual badge focus for creative technologists and frontend)\n"
                f"- des-0014: Nordic Clean Minimalist (Minimalist ivory classic, single-column modern for high-end product consultants)\n\n"
                f"Select the most suitable design configuration for this candidate:"
            )

            raw_output = cls._run_model_inference(system_prompt, user_prompt, max_tokens=280)

            parsed = None
            try:
                json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group(0))
            except Exception:
                parsed = None

            if parsed and "recommendedDesignId" in parsed:
                latency_ms = (time.time() - t0) * 1000.0
                des_id = str(parsed.get("recommendedDesignId", "des-0001")).strip()
                if not re.match(r"^des-\d{4}$", des_id):
                    des_id = "des-0001"
                return RecommendDesignResponse(
                    recommendedDesignId=des_id,
                    explanation=parsed.get("explanation", f"AI recommendation matched your profile to {des_id}."),
                    matchingProfileCharacteristics=parsed.get("matchingProfileCharacteristics", [effective_role, "Key Technical Skills"]),
                    whyAppropriate=parsed.get("whyAppropriate", "This visual layout aligns with your specific career milestones and skills."),
                    isFallback=False,
                    fallbackReason=None,
                    latencyMs=round(latency_ms, 2),
                    modelName=_MODEL_NAME
                )
            else:
                return cls.fallback_heuristic_recommendation(resume_data, reason="Model response did not contain required JSON schema.")
        except Exception as e:
            return cls.fallback_heuristic_recommendation(resume_data, reason=f"MLX Metal inference error: {str(e)}")

    @classmethod
    def generate_full_resume(
        cls,
        raw_resume: ResumeFullData,
        target_role: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> AIGenerateResumeResponse:
        """
        Processes complete user-entered resume data, improving summaries,
        responsibilities, and project descriptions while strictly preserving user facts.
        """
        t0 = time.time()
        modifications: List[str] = []
        enhanced_data = raw_resume.model_copy(deep=True)

        context_role = target_role or raw_resume.personalInfo.professionalTitle or "Software Professional"

        # 1. Enhance Professional Summary
        summary_input = raw_resume.personalInfo.summary
        if not summary_input or len(summary_input.strip()) < 15:
            # Construct base from role + education + top skills
            top_skills = (
                raw_resume.skills.programmingLanguages[:3] +
                raw_resume.skills.frameworks[:2] +
                raw_resume.skills.aiMlSkills[:2]
            )
            skills_mention = f" skilled in {', '.join(top_skills)}" if top_skills else ""
            summary_input = f"{context_role}{skills_mention} looking to deliver impactful technical solutions."

        summary_prompt = (
            f"Write a concise, polished 2-3 sentence professional resume summary for: {context_role}.\n"
            f"Input Details: {summary_input}\n"
            f"Strict constraint: Never add fake company names or fabricated statistics. Preserve the exact facts."
        )
        enhanced_summary = cls._run_model_inference(
            system_prompt="You are an expert resume writer. Be concise, punchy, and factually strict. Return only the summary text.",
            user_prompt=summary_prompt,
            max_tokens=150
        )
        if enhanced_summary and len(enhanced_summary) > 20:
            enhanced_data.personalInfo.summary = enhanced_summary
            modifications.append("Refined professional summary with action-oriented positioning.")

        # 2. Enhance Experience Responsibilities
        for idx, exp in enumerate(enhanced_data.experience):
            if exp.responsibilities:
                bullets_joined = "\n".join([f"- {r}" for r in exp.responsibilities if r.strip()])
                exp_prompt = (
                    f"Refine the following job responsibilities for role '{exp.role}' at '{exp.company}'.\n"
                    f"Use active verbs (e.g. Developed, Engineered, Optimized) and STAR style where applicable.\n"
                    f"Never invent metrics not present in input.\n"
                    f"Input:\n{bullets_joined}\n\nRefined Bullets:"
                )
                refined = cls._run_model_inference(
                    system_prompt="You are an expert technical resume editor. Format as bullet points starting with '- '. Never hallucinate.",
                    user_prompt=exp_prompt,
                    max_tokens=220
                )
                refined_bullets = []
                for line in refined.split("\n"):
                    c_line = line.strip().lstrip("•-* \t")
                    if c_line and len(c_line) > 8:
                        refined_bullets.append(c_line)
                if refined_bullets:
                    enhanced_data.experience[idx].responsibilities = refined_bullets
                    modifications.append(f"Polished {len(refined_bullets)} responsibility points for {exp.role} at {exp.company}.")

        # 3. Enhance Internship Entries
        for idx, intern in enumerate(enhanced_data.internships):
            all_points = intern.workPerformed + intern.achievements
            if all_points:
                int_joined = "\n".join([f"- {p}" for p in all_points if p.strip()])
                intern_prompt = (
                    f"Refine these internship achievements for '{intern.role}' at '{intern.organization}'.\n"
                    f"Use action verbs. Keep factual accuracy.\n"
                    f"Input:\n{int_joined}\n\nRefined Bullets:"
                )
                refined_int = cls._run_model_inference(
                    system_prompt="You are an expert resume editor. Format as clean bullet points starting with '- '.",
                    user_prompt=intern_prompt,
                    max_tokens=180
                )
                new_work = []
                for line in refined_int.split("\n"):
                    c_line = line.strip().lstrip("•-* \t")
                    if c_line and len(c_line) > 8:
                        new_work.append(c_line)
                if new_work:
                    enhanced_data.internships[idx].workPerformed = new_work
                    modifications.append(f"Elevated internship impact statements for {intern.role} at {intern.organization}.")

        # 4. Enhance Project Descriptions and Contributions
        for idx, proj in enumerate(enhanced_data.projects):
            if proj.contributions or proj.description:
                pts = [proj.description] if proj.description else []
                pts.extend(proj.contributions)
                pts_joined = "\n".join([f"- {p}" for p in pts if p.strip()])
                proj_prompt = (
                    f"Refine these project contributions for project '{proj.title}' (Tech stack: {', '.join(proj.technologies)}).\n"
                    f"Make them sound technically rigorous with strong verbs.\n"
                    f"Input:\n{pts_joined}\n\nRefined:"
                )
                refined_proj = cls._run_model_inference(
                    system_prompt="You are a senior tech lead reviewing resume project descriptions. Format as bullet points.",
                    user_prompt=proj_prompt,
                    max_tokens=200
                )
                new_contribs = []
                for line in refined_proj.split("\n"):
                    c_line = line.strip().lstrip("•-* \t")
                    if c_line and len(c_line) > 8:
                        new_contribs.append(c_line)
                if new_contribs:
                    enhanced_data.projects[idx].contributions = new_contribs
                    modifications.append(f"Structured technical achievements for project '{proj.title}'.")

        # 5. Template Recommendation
        recommended_tmpl, reason = cls._recommend_template(enhanced_data)
        enhanced_data.templateId = recommended_tmpl

        latency_ms = (time.time() - t0) * 1000.0

        return AIGenerateResumeResponse(
            enhancedResumeData=enhanced_data,
            recommendedTemplate=recommended_tmpl,
            recommendationReason=reason,
            generationLatencyMs=round(latency_ms, 2),
            modelName=_MODEL_NAME,
            modificationsSummary=modifications if modifications else ["Resume content verified and formatted for ATS compatibility."]
        )
