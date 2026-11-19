"""
Question Bank and Retrieval Service for Feature 2 Technical Assessments.
Loads and indexes the 2,250 production questions and provides secure, masked question delivery.
"""

import json
import os
import random
from typing import Dict, List, Optional, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
QUESTIONS_FILE = os.path.join(BASE_DIR, "datasets", "feature2", "questions.jsonl")
ROLES_FILE = os.path.join(BASE_DIR, "datasets", "feature2", "roles_and_skills.json")

class QuestionService:
    def __init__(self):
        self._questions_by_id: Dict[str, Dict[str, Any]] = {}
        self._questions_by_role: Dict[str, List[Dict[str, Any]]] = {}
        self._roles_data: Optional[Dict[str, Any]] = None
        self._loaded = False

    def load(self):
        if self._loaded:
            return
            
        # 1. Load roles and skills taxonomy
        if os.path.exists(ROLES_FILE):
            with open(ROLES_FILE, "r") as f:
                self._roles_data = json.load(f)
        else:
            self._roles_data = {"roles": []}

        # 2. Load and index all 2,250 questions
        if os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        q = json.loads(line)
                        qid = q["question_id"]
                        self._questions_by_id[qid] = q
                        
                        rid = q.get("role_id")
                        if rid not in self._questions_by_role:
                            self._questions_by_role[rid] = []
                        self._questions_by_role[rid].append(q)
                        
        self._loaded = True

    def get_roles(self) -> List[Dict[str, Any]]:
        self.load()
        return self._roles_data.get("roles", [])

    def get_role_by_id(self, role_id: str) -> Optional[Dict[str, Any]]:
        self.load()
        for r in self._roles_data.get("roles", []):
            if r["role_id"] == role_id:
                return r
        return None

    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        self.load()
        return self._questions_by_id.get(question_id)

    def mask_question_for_client(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """Strip answer keys, hidden test cases, and reference solutions before sending to client."""
        masked = dict(question)
        # Remove server-side secrets
        masked.pop("correct_answer", None)
        masked.pop("answer_explanation", None)
        masked.pop("reference_solution", None)
        masked.pop("hidden_test_cases", None)
        return masked

    def select_questions(
        self,
        role_id: str,
        skill_id: Optional[str] = None,
        assessment_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        count: int = 10,
        exclude_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        self.load()
        exclude_set = set(exclude_ids or [])
        candidates = self._questions_by_role.get(role_id, [])

        filtered = []
        for q in candidates:
            if q["question_id"] in exclude_set:
                continue
            if skill_id and q.get("skill_id") != skill_id:
                continue
            if assessment_type and q.get("assessment_type") != assessment_type:
                continue
            if difficulty and q.get("difficulty") != difficulty:
                continue
            filtered.append(q)

        # Fallback if too strict
        if len(filtered) < count and difficulty:
            # loosen difficulty constraint
            for q in candidates:
                if q["question_id"] in exclude_set:
                    continue
                if skill_id and q.get("skill_id") != skill_id:
                    continue
                if assessment_type and q.get("assessment_type") != assessment_type:
                    continue
                if q not in filtered:
                    filtered.append(q)

        random.shuffle(filtered)
        return filtered[:count]

# Singleton instance
question_service = QuestionService()

