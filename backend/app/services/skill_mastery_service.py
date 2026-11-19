"""
Skill Mastery & Gap Analysis Service.
Computes Bayesian skill mastery scores, confidence bounds, and prioritized competency gaps.
"""

import math
from typing import Dict, List, Any, Optional

DIFFICULTY_WEIGHT = {
    "easy": 1.0,
    "medium": 1.5,
    "hard": 2.0
}

class SkillMasteryService:
    """Calculates skill-wise proficiency, confidence intervals, and career skill gaps."""
    
    @classmethod
    def calculate_skill_performances(
        cls,
        evaluated_answers: List[Dict[str, Any]],
        role_skills: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        # Group attempts by skill_id
        skill_groups = {}
        
        for ans in evaluated_answers:
            sid = ans.get("skill_id", "GENERAL")
            sname = ans.get("skill_name", "General Technical Skills")
            diff = ans.get("difficulty", "medium")
            score = float(ans.get("points_awarded", 0.0))
            max_points = max(1.0, float(ans.get("max_points", 1.0)))
            
            if sid not in skill_groups:
                skill_groups[sid] = {
                    "skill_id": sid,
                    "skill_name": sname,
                    "attempts": 0,
                    "weighted_score": 0.0,
                    "weighted_total": 0.0,
                    "correct_count": 0
                }
                
            w = DIFFICULTY_WEIGHT.get(diff.lower(), 1.0)
            skill_groups[sid]["attempts"] += 1
            skill_groups[sid]["weighted_score"] += (score / max_points) * w
            skill_groups[sid]["weighted_total"] += w
            if ans.get("is_correct", False):
                skill_groups[sid]["correct_count"] += 1

        performances = []
        for sid, data in skill_groups.items():
            attempts = data["attempts"]
            mastery_ratio = data["weighted_score"] / max(0.001, data["weighted_total"])
            mastery_pct = round(mastery_ratio * 100.0, 1)
            
            # Confidence based on evidence volume: C = 1 - exp(-0.35 * N)
            confidence = round(1.0 - math.exp(-0.35 * attempts), 2)
            
            if mastery_pct >= 75.0:
                status = "proficient"
            elif mastery_pct >= 50.0:
                status = "developing"
            else:
                status = "needs_improvement"
                
            performances.append({
                "skill_id": sid,
                "skill_name": data["skill_name"],
                "mastery_percentage": mastery_pct,
                "confidence": confidence,
                "evidence_count": attempts,
                "correct_count": data["correct_count"],
                "status": status
            })

        # If role_skills provided, fill in unassessed skills
        if role_skills:
            assessed_sids = {p["skill_id"] for p in performances}
            for rs in role_skills:
                if rs["skill_id"] not in assessed_sids:
                    performances.append({
                        "skill_id": rs["skill_id"],
                        "skill_name": rs["name"],
                        "mastery_percentage": 0.0,
                        "confidence": 0.0,
                        "evidence_count": 0,
                        "correct_count": 0,
                        "status": "not_assessed"
                    })

        return performances

    @classmethod
    def identify_skill_gaps(
        cls,
        skill_performances: List[Dict[str, Any]],
        target_proficiency_threshold: float = 75.0
    ) -> List[Dict[str, Any]]:
        gaps = []
        for sp in skill_performances:
            current = sp["mastery_percentage"]
            if current < target_proficiency_threshold:
                gap_delta = round(target_proficiency_threshold - current, 1)
                priority = "HIGH" if gap_delta >= 40.0 else ("MEDIUM" if gap_delta >= 20.0 else "LOW")
                gaps.append({
                    "skill_id": sp["skill_id"],
                    "skill_name": sp["skill_name"],
                    "current_level": current,
                    "target_level": target_proficiency_threshold,
                    "gap_delta": gap_delta,
                    "priority": priority,
                    "confidence": sp["confidence"]
                })
        # Sort by gap delta descending
        gaps.sort(key=lambda x: x["gap_delta"], reverse=True)
        return gaps

# Singleton
skill_mastery_service = SkillMasteryService()

