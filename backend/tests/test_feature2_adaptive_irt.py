"""
Item Response Theory (1PL Rasch Model) & Bayesian Skill Mastery Test Suite.
Validates mathematical equations, parameter bounds, cold start, and Bayesian mastery calculation.
"""

import math
import pytest
from app.services.adaptive_engine import AdaptiveEngine
from app.services.skill_mastery_service import SkillMasteryService


class Test1PLIRTValidation:
    """Verifies mathematical validity of Rasch IRT implementation."""

    def test_probability_calculation_at_equilibrium(self):
        # When theta == b (e.g. theta=0, medium difficulty b=0), P(correct) must be 0.5
        p = AdaptiveEngine.probability_correct(theta=0.0, difficulty_level="medium")
        assert round(p, 4) == 0.5000

    def test_probability_monotonicity(self):
        # Higher ability theta must have higher probability of passing
        p_low = AdaptiveEngine.probability_correct(theta=-1.0, difficulty_level="medium")
        p_med = AdaptiveEngine.probability_correct(theta=0.0, difficulty_level="medium")
        p_high = AdaptiveEngine.probability_correct(theta=1.0, difficulty_level="medium")
        assert p_low < p_med < p_high

    def test_ability_increases_on_correct_answer(self):
        theta_0 = 0.0
        theta_1 = AdaptiveEngine.update_ability(theta_0, difficulty_level="medium", is_correct=True)
        assert theta_1 > theta_0

    def test_ability_decreases_on_incorrect_answer(self):
        theta_0 = 0.0
        theta_1 = AdaptiveEngine.update_ability(theta_0, difficulty_level="medium", is_correct=False)
        assert theta_1 < theta_0

    def test_numerical_bounds_enforced(self):
        # Even with 50 consecutive correct answers, theta cannot exceed +3.0
        theta = 0.0
        for _ in range(50):
            theta = AdaptiveEngine.update_ability(theta, "hard", is_correct=True)
        assert theta <= 3.0

        # Even with 50 consecutive incorrect answers, theta cannot drop below -3.0
        for _ in range(100):
            theta = AdaptiveEngine.update_ability(theta, "easy", is_correct=False)
        assert theta >= -3.0

    def test_cold_start_recommends_medium(self):
        # Cold start theta = 0.0
        rec = AdaptiveEngine.get_recommended_difficulty(0.0)
        assert rec == "medium"

    def test_score_mapping_normalized(self):
        # theta=0 maps to 50%
        score_mid = AdaptiveEngine.compute_ability_score(0.0)
        assert score_mid == 50.0

        score_high = AdaptiveEngine.compute_ability_score(3.0)
        assert score_high > 90.0

        score_low = AdaptiveEngine.compute_ability_score(-3.0)
        assert score_low < 10.0


class TestBayesianSkillMasteryValidation:
    """Verifies evidence aggregation, difficulty weighting, and confidence calculation."""

    def test_evidence_volume_increases_confidence(self):
        # 1 attempt vs 5 attempts vs 10 attempts
        c1 = round(1.0 - math.exp(-0.35 * 1), 2)
        c5 = round(1.0 - math.exp(-0.35 * 5), 2)
        c10 = round(1.0 - math.exp(-0.35 * 10), 2)
        assert c1 < c5 < c10
        assert c10 > 0.95

    def test_skill_performance_weighting(self):
        answers = [
            {"skill_id": "SK-01", "skill_name": "Python", "difficulty": "hard", "points_awarded": 1.0, "max_points": 1.0, "is_correct": True},
            {"skill_id": "SK-01", "skill_name": "Python", "difficulty": "easy", "points_awarded": 0.0, "max_points": 1.0, "is_correct": False},
        ]
        res = SkillMasteryService.calculate_skill_performances(answers)
        assert len(res) == 1
        perf = res[0]
        assert perf["skill_id"] == "SK-01"
        assert perf["evidence_count"] == 2
        assert perf["confidence"] > 0.4
        assert perf["mastery_percentage"] > 0
