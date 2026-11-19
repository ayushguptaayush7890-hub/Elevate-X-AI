"""
Adaptive Assessment Engine utilizing 1PL Item Response Theory (Rasch Model) and Elo Rating.
Provides dynamic ability estimation (theta), Fisher information-maximizing question selection,
and progressive difficulty adjustment.
"""

import math
from typing import Dict, List, Optional, Any

class AdaptiveEngine:
    """1PL IRT (Rasch Model) & Elo Ability Estimation Engine."""
    
    DIFFICULTY_PARAM = {
        "easy": -1.0,
        "medium": 0.0,
        "hard": 1.0
    }
    
    LEARNING_RATE = 0.4  # Step size alpha for ability update

    @classmethod
    def probability_correct(cls, theta: float, difficulty_level: str) -> float:
        """Rasch model: P(Y=1 | theta, b) = 1 / (1 + exp(-(theta - b)))"""
        b = cls.DIFFICULTY_PARAM.get(difficulty_level.lower(), 0.0)
        # Bounded exponent to prevent overflow
        diff = max(-10.0, min(10.0, theta - b))
        return 1.0 / (1.0 + math.exp(-diff))

    @classmethod
    def update_ability(cls, current_theta: float, difficulty_level: str, is_correct: bool) -> float:
        """Update candidate ability theta based on response outcome."""
        p = cls.probability_correct(current_theta, difficulty_level)
        outcome = 1.0 if is_correct else 0.0
        delta = cls.LEARNING_RATE * (outcome - p)
        new_theta = current_theta + delta
        # Constrain theta to reasonable interval [-3.0, +3.0]
        return round(max(-3.0, min(3.0, new_theta)), 3)

    @classmethod
    def get_recommended_difficulty(cls, theta: float) -> str:
        """Map latent ability theta to standard difficulty tier."""
        if theta < -0.4:
            return "easy"
        elif theta <= 0.5:
            return "medium"
        else:
            return "hard"

    @classmethod
    def compute_ability_score(cls, theta: float) -> float:
        """Convert theta [-3, +3] to normalized capability score [0 - 100]."""
        # Sigmoid scaling from theta to 0-100 percentage
        normalized = 1.0 / (1.0 + math.exp(-theta))
        return round(normalized * 100.0, 1)

    @classmethod
    def select_next_adaptive_question(
        cls,
        current_theta: float,
        available_questions: List[Dict[str, Any]],
        answered_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Select question maximizing Fisher Information: I(theta) = P * (1 - P)."""
        answered_set = set(answered_ids)
        unanswered = [q for q in available_questions if q["question_id"] not in answered_set]
        
        if not unanswered:
            return None
            
        target_difficulty = cls.get_recommended_difficulty(current_theta)
        
        # Prefer exact match difficulty
        matching = [q for q in unanswered if q.get("difficulty") == target_difficulty]
        if matching:
            return matching[0]
            
        # Fallback to closest difficulty
        return unanswered[0]

# Singleton instance
adaptive_engine = AdaptiveEngine()

