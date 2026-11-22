"""
Comprehensive Automated Test Suite for Career Transition & Skill Transferability Engine.
Tests all endpoints, services, PyTorch graph embeddings, and blueprint generation.
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add project root and backend to path
ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR / "backend"))
sys.path.insert(0, str(ROOT_DIR))

# Ensure local sqlite database is used with absolute path
abs_db_path = (ROOT_DIR / "backend" / "elevate_x_local.db").resolve()
os.environ["DATABASE_URL"] = f"sqlite:///{abs_db_path}"

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.user import User
from app.models.career_transition import UserCareerTransitionGoal
from app.services.career_transition_service import CareerTransitionService
from app.core.security import create_access_token

class TestCareerTransitionEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.db = SessionLocal()
        
        # Find or create a test user
        user = cls.db.query(User).filter(User.email == "transition_tester@example.com").first()
        if not user:
            user = User(
                email="transition_tester@example.com",
                hashed_password="testpasswordhashed",
                full_name="Transition Test Worker",
                is_active=True,
                role="candidate",
            )
            cls.db.add(user)
            cls.db.commit()
            cls.db.refresh(user)
        cls.user = user
        cls.token = create_access_token(subject=str(user.id))
        cls.headers = {"Authorization": f"Bearer {cls.token}"}

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "user") and cls.user:
            cls.db.query(UserCareerTransitionGoal).filter(UserCareerTransitionGoal.user_id == cls.user.id).delete()
            cls.db.query(User).filter(User.id == cls.user.id).delete()
            cls.db.commit()
        cls.db.close()

    def test_01_search_occupations(self):
        """Test search occupations across ESCO, O*NET, and India NCO."""
        response = self.client.get(
            "/api/v1/career-transitions/occupations?q=electrician&limit=5",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("title", data[0])
        self.assertIn("source", data[0])

    def test_02_get_occupation_details(self):
        """Test occupation profile and required competencies lookup."""
        response = self.client.get(
            "/api/v1/career-transitions/occupations/Electrician",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("occupation", data)
        self.assertIn("skills", data)
        self.assertIn("market", data)

    def test_03_recommendations_endpoint(self):
        """Test dynamic transition recommendations with graph embeddings and fit ranking."""
        payload = {
            "current_occupation": "Electrician",
            "candidate_skills": ["wiring", "circuit breakers", "safety compliance"],
            "limit": 4,
        }
        response = self.client.post(
            "/api/v1/career-transitions/recommendations",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        
        # Verify first recommendation schema
        first = data[0]
        self.assertIn("target_title", first)
        self.assertIn("fit_percentage", first)
        self.assertIn("transition_delta", first)
        self.assertIn("difficulty_category", first)
        self.assertIn("transferable_skills_count", first)
        self.assertIn("salary_range", first)

    def test_04_analyze_endpoint(self):
        """Test 5-tier evidence state transferability audit."""
        payload = {
            "from_occupation": "Electrician",
            "to_occupation": "Solar Photovoltaic Installer",
            "candidate_skills": ["electrical safety", "wiring", "power tools"],
        }
        response = self.client.post(
            "/api/v1/career-transitions/analyze",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["from_occupation_title"].lower(), "electrician")
        self.assertIn("transferable_competencies", data)
        self.assertIn("bridgeable_competencies", data)
        self.assertIn("missing_competencies", data)
        self.assertGreaterEqual(data["fit_percentage"], 0.0)

    def test_05_compare_endpoint(self):
        """Test multi-target comparison."""
        payload = {
            "current_occupation": "Electrician",
            "target_occupations": ["Solar Photovoltaic Installer", "Wind Turbine Technician"],
            "candidate_skills": ["electrical maintenance", "diagnostics"],
        }
        response = self.client.post(
            "/api/v1/career-transitions/compare",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("comparisons", data)
        self.assertEqual(len(data["comparisons"]), 2)

    def test_06_blueprint_endpoint(self):
        """Test 4-stage Transition Bridge Blueprint generation."""
        payload = {
            "from_occupation": "Electrician",
            "to_occupation": "Solar Photovoltaic Installer",
            "candidate_skills": ["wiring", "diagnostics"],
        }
        response = self.client.post(
            "/api/v1/career-transitions/blueprint",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("stages", data)
        self.assertEqual(len(data["stages"]), 4)
        for stg in data["stages"]:
            self.assertIn("stage_number", stg)
            self.assertIn("stage_name", stg)
            self.assertIn("milestones", stg)
            self.assertIn("tasks", stg)

    def test_07_adopt_goal_and_progress(self):
        """Test adopting a goal, DB persistence, and retrieving user progress."""
        payload = {
            "from_occupation_title": "Electrician",
            "target_occupation_id": "ESCO:solar-pv-installer",
            "target_occupation_title": "Solar Photovoltaic Installer",
            "fit_percentage": 78.5,
            "transition_delta": 21.5,
            "difficulty_category": "Low Friction",
            "blueprint": {"stages_count": 4},
        }
        response = self.client.post(
            "/api/v1/career-transitions/adopt-goal",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("goal_id", data)

        # Retrieve user progress
        progress_res = self.client.get(
            "/api/v1/career-transitions/progress",
            headers=self.headers,
        )
        self.assertEqual(progress_res.status_code, 200)
        progress_data = progress_res.json()
        self.assertIsInstance(progress_data, list)
        self.assertGreater(len(progress_data), 0)
        self.assertEqual(progress_data[0]["target_occupation_title"], "Solar Photovoltaic Installer")

if __name__ == "__main__":
    unittest.main()
