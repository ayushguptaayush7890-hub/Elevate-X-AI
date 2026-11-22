"""
User Profile Context Aggregator Service.
Aggregates authentic candidate profile, skills, work experience, career transitions,
and gap analyses into a consolidated context prompt for the AI Career Mentor.
"""

from typing import Optional, Dict, Any, List
import json
import uuid
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.user import User
from app.models.profile import UserProfile, Education, WorkExperience
from app.models.skill import UserSkill, Skill
from app.models.career_transition import UserCareerTransitionGoal
from app.models.skill_gap import SkillGapReport
from app.models.resume import ResumeDocument

logger = logging.getLogger(__name__)


class AssistantContextService:
    """Extracts authentic candidate profile and skills context from the database."""

    @staticmethod
    def get_candidate_context(db: Session, user_id: Optional[uuid.UUID] = None) -> str:
        """
        Builds a comprehensive, grounded candidate background summary.
        If user_id is None, tries to find a demo user (e.g. Ramesh Sharma) or returns general context.
        """
        user: Optional[User] = None
        if user_id:
            user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        
        # If no user specified or found, fallback to live demo candidate Ramesh Sharma
        if not user:
            user = db.execute(
                select(User).where(User.email == "live.demo@elevatex.ai")
            ).scalar_one_or_none()

        if not user:
            # Fallback to any active user
            user = db.execute(select(User).where(User.is_active == True)).first()
            if user:
                user = user[0]

        if not user:
            return (
                "Candidate Context: Guest Vocational Candidate. "
                "Interested in vocational career progression, technical upskilling, and formal job placement."
            )

        context_lines: List[str] = []
        context_lines.append(f"### Candidate Profile:")
        context_lines.append(f"- **Name:** {user.full_name or 'Candidate'}")

        # Profile
        profile: Optional[UserProfile] = db.execute(
            select(UserProfile).where(UserProfile.user_id == user.id)
        ).scalar_one_or_none()

        if profile:
            if profile.headline:
                context_lines.append(f"- **Current Role/Headline:** {profile.headline}")
            if profile.trade_category:
                context_lines.append(f"- **Trade Category:** {profile.trade_category}")
            if profile.years_of_experience:
                context_lines.append(f"- **Experience:** {profile.years_of_experience} years")
            if profile.location:
                context_lines.append(f"- **Location:** {profile.location}")
            if profile.bio:
                context_lines.append(f"- **Bio / Summary:** {profile.bio[:300]}")

            # Work Experiences
            work_exps = db.execute(
                select(WorkExperience)
                .where(WorkExperience.profile_id == profile.id)
                .order_by(desc(WorkExperience.start_date))
                .limit(4)
            ).scalars().all()

            if work_exps:
                context_lines.append("\n### Work & Practical Experience:")
                for wx in work_exps:
                    tools = f" (Tools: {wx.trade_tools_used})" if wx.trade_tools_used else ""
                    context_lines.append(f"- {wx.job_title} at {wx.company_or_workshop}{tools}")

            # Education
            edus = db.execute(
                select(Education)
                .where(Education.profile_id == profile.id)
                .order_by(desc(Education.start_date))
                .limit(3)
            ).scalars().all()

            if edus:
                context_lines.append("\n### Education & Qualifications:")
                for ed in edus:
                    field = f" in {ed.field_of_study}" if ed.field_of_study else ""
                    context_lines.append(f"- {ed.degree_or_certificate}{field} from {ed.institution}")

            # Skills
            user_skills = db.execute(
                select(UserSkill, Skill.name)
                .join(Skill, Skill.id == UserSkill.skill_id)
                .where(UserSkill.profile_id == profile.id)
                .limit(15)
            ).all()

            if user_skills:
                context_lines.append("\n### Verified & Practiced Skills:")
                skill_items = []
                for us, skill_name in user_skills:
                    skill_items.append(f"{skill_name} ({us.proficiency_level})")
                context_lines.append(", ".join(skill_items))

        # Career Transition Goals
        transition_goal = db.execute(
            select(UserCareerTransitionGoal)
            .where(UserCareerTransitionGoal.user_id == user.id)
            .order_by(desc(UserCareerTransitionGoal.updated_at))
        ).scalars().first()

        if transition_goal:
            context_lines.append("\n### Active Career Transition:")
            context_lines.append(f"- **From:** {transition_goal.from_occupation_title}")
            context_lines.append(f"- **Target Occupation:** {transition_goal.target_occupation_title}")
            if transition_goal.fit_percentage is not None:
                context_lines.append(f"- **Fit Percentage:** {transition_goal.fit_percentage:.1f}%")
            if transition_goal.difficulty_category:
                context_lines.append(f"- **Transition Difficulty:** {transition_goal.difficulty_category}")

            # Transferable & Missing skills
            if transition_goal.transferable_skills_json:
                try:
                    t_skills = json.loads(transition_goal.transferable_skills_json)
                    if isinstance(t_skills, list) and t_skills:
                        names = [s.get("title", s) if isinstance(s, dict) else str(s) for s in t_skills[:6]]
                        context_lines.append(f"- **Key Transferable Skills:** {', '.join(names)}")
                except Exception:
                    pass

            if transition_goal.missing_skills_json:
                try:
                    m_skills = json.loads(transition_goal.missing_skills_json)
                    if isinstance(m_skills, list) and m_skills:
                        names = [s.get("title", s) if isinstance(s, dict) else str(s) for s in m_skills[:6]]
                        context_lines.append(f"- **Bridge/Missing Skills To Acquire:** {', '.join(names)}")
                except Exception:
                    pass

        # Skill Gap Report
        skill_gap = db.execute(
            select(SkillGapReport)
            .where(SkillGapReport.user_id == user.id)
            .order_by(desc(SkillGapReport.created_at))
        ).scalars().first()

        if skill_gap and skill_gap.overall_match_percentage is not None:
            context_lines.append(f"\n### Skill Gap Match:")
            context_lines.append(f"- Overall Match: {skill_gap.overall_match_percentage:.1f}%")

        return "\n".join(context_lines)
