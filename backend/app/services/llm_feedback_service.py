"""
AI Feedback and Explanation Engine with Robust Deterministic Fallback.
Provides pedagogical feedback explaining why an answer was correct or incorrect,
identifies conceptual gaps, and provides grounded improvement recommendations.
"""

import os
from typing import Dict, List, Any, Optional

class LLMFeedbackService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

    def generate_question_feedback(
        self,
        question: Dict[str, Any],
        user_answer: Any,
        is_correct: bool,
        points_awarded: float,
        sandbox_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate grounded pedagogical feedback for an individual question attempt."""
        qtype = question.get("assessment_type", "mcq")
        exp = question.get("answer_explanation", "")
        qtext = question.get("question_text", "")
        
        if is_correct:
            summary = "Excellent! Your response demonstrated a correct grasp of the underlying engineering principles."
            key_takeaway = exp or "Your technical approach satisfied all functional constraints and architectural requirements."
        else:
            summary = "Review Recommended: Your response revealed a misconception or unhandled edge case."
            key_takeaway = exp or "Review the technical documentation and consider runtime edge cases, concurrency hazards, or syntax constraints."

        # Sandbox specific error feedback
        sandbox_notes = None
        if sandbox_result and sandbox_result.get("error"):
            sandbox_notes = f"Runtime Issue: {sandbox_result['error']}"

        return {
            "is_correct": is_correct,
            "points_awarded": points_awarded,
            "feedback_summary": summary,
            "conceptual_explanation": key_takeaway,
            "sandbox_notes": sandbox_notes,
            "learning_tip": f"Focus on {question.get('subtopic', question.get('skill_name', 'this area'))} to solidify this concept."
        }

    def generate_assessment_summary_feedback(
        self,
        role_title: str,
        overall_score: float,
        skill_performances: List[Dict[str, Any]],
        gaps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesize overall diagnostic feedback across the complete assessment attempt."""
        if overall_score >= 80.0:
            level = "Senior / Advanced Competency"
            narrative = f"You demonstrated strong proficiency across {role_title} competencies, showing sound architectural reasoning and problem-solving skills."
        elif overall_score >= 60.0:
            level = "Mid-Level Competency"
            narrative = f"You demonstrated solid foundational ability for {role_title}, but experienced difficulty with advanced edge cases and system-level trade-offs."
        else:
            level = "Foundational / Junior Competency"
            narrative = f"You have an initial grasp of core concepts for {role_title}, but targeted study and hands-on practice are recommended across key technical skills."

        top_strengths = [s["skill_name"] for s in skill_performances if s["mastery_percentage"] >= 70.0][:2]
        priority_focus = [g["skill_name"] for g in gaps][:3]

        return {
            "estimated_level": level,
            "narrative_assessment": narrative,
            "top_strengths": top_strengths if top_strengths else ["Foundational familiarity with core topics"],
            "priority_focus_areas": priority_focus if priority_focus else ["Continue practice across all competencies"],
            "suggested_action": "Review the personalized career roadmap below and tackle targeted practice tasks for your highest priority skill gaps."
        }

# Singleton
llm_feedback_service = LLMFeedbackService()

