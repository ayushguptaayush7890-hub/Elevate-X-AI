"""
Scenario Question Catalog Generator for Elevate X AI Feature 2
Provides 40 genuinely unique, technically detailed, production-incident scenarios
for each of the 9 roles (360 unique scenarios total).
"""

from typing import Dict, List, Any
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from base_builder import build_scenario

# Scenario matrix generator: 8 realistic incident scenarios per skill (5 skills = 40 scenarios)
# per role across all 9 roles.

def generate_role_scenarios(role_id: str, skills_dict: Dict[str, tuple]) -> List[Dict[str, Any]]:
    from scenario_data import ROLE_SCENARIOS_DATA
    
    data = ROLE_SCENARIOS_DATA.get(role_id, [])
    if len(data) != 40:
        raise ValueError(f"Expected 40 scenarios for {role_id}, found {len(data)}")
        
    questions = []
    for idx, item in enumerate(data, start=1):
        s_key = item["skill_key"]
        s_id, s_name = skills_dict[s_key]
        subtopic = item["subtopic"]
        diff = item["difficulty"]
        marks = 4 if diff == "easy" else (6 if diff == "medium" else 10)
        t_est = 8 if diff == "easy" else (12 if diff == "medium" else 18)
        
        ctx = item["context"]
        prompt = item["prompt"]
        opts = item["options"]
        ans = item["correct_answer"]
        exp = item["explanation"]
        
        q = build_scenario(
            role_id=role_id,
            skill_id=s_id,
            skill_name=s_name,
            subtopic=subtopic,
            difficulty=diff,
            index=idx,
            scenario_context=ctx,
            problem_prompt=prompt,
            options=opts,
            correct_answer=ans,
            explanation=exp,
            marks=marks,
            estimated_time=t_est
        )
        questions.append(q)
        
    return questions

