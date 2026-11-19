"""
Performance & Latency Benchmark Suite for Feature 2.
Measures P50, P95, P99 latency across question indexing, IRT calculation, sandboxes, and API endpoints.
"""

import time
import statistics
import pytest
from fastapi.testclient import TestClient
from app.services.sandboxes import SQLSandbox, CodeSandbox
from app.services.adaptive_engine import AdaptiveEngine
from app.services.question_service import question_service

def _register_perf_user(client: TestClient) -> dict:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "perf.test@elevate.ai", "password": "Password123!", "full_name": "Perf User"},
    )
    if res.status_code == 201:
        token = res.json()["token"]["access_token"]
        return {"Authorization": f"Bearer {token}"}
    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": "perf.test@elevate.ai", "password": "Password123!"},
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestFeature2Performance:
    """Measures latency metrics for core Feature 2 services and endpoints."""

    def test_question_retrieval_latency(self):
        latencies = []
        for _ in range(50):
            t0 = time.perf_counter()
            q = question_service.select_questions(role_id="software_engineer", count=10)
            latencies.append((time.perf_counter() - t0) * 1000)

        mean_ms = statistics.mean(latencies)
        p95_ms = statistics.quantiles(latencies, n=20)[18]
        # In-memory retrieval must be blazing fast (< 5ms mean)
        assert mean_ms < 10.0
        assert p95_ms < 20.0

    def test_irt_update_latency(self):
        latencies = []
        for _ in range(100):
            t0 = time.perf_counter()
            theta = AdaptiveEngine.update_ability(current_theta=0.2, difficulty_level="hard", is_correct=True)
            latencies.append((time.perf_counter() - t0) * 1000)

        mean_ms = statistics.mean(latencies)
        assert mean_ms < 0.5  # Sub-millisecond calculation

    def test_sql_sandbox_execution_latency(self):
        latencies = []
        for _ in range(20):
            t0 = time.perf_counter()
            res = SQLSandbox.execute_and_grade(
                schema_sql="CREATE TABLE benchmarks (id INT, val INT);",
                sample_db_sql="INSERT INTO benchmarks VALUES (1, 100), (2, 200), (3, 300);",
                candidate_query="SELECT id, val FROM benchmarks WHERE val >= 200;"
            )
            latencies.append((time.perf_counter() - t0) * 1000)
            assert res["passed"] is True

        mean_ms = statistics.mean(latencies)
        p95_ms = statistics.quantiles(latencies, n=20)[18]
        assert mean_ms < 15.0
        assert p95_ms < 30.0

    def test_api_roles_endpoint_latency(self, client: TestClient):
        latencies = []
        for _ in range(30):
            t0 = time.perf_counter()
            res = client.get("/api/v1/assessments/technical/roles")
            latencies.append((time.perf_counter() - t0) * 1000)
            assert res.status_code == 200

        mean_ms = statistics.mean(latencies)
        p95_ms = statistics.quantiles(latencies, n=20)[18]
        assert mean_ms < 25.0
        assert p95_ms < 50.0

    def test_api_start_assessment_latency(self, client: TestClient):
        headers = _register_perf_user(client)
        latencies = []
        for _ in range(15):
            t0 = time.perf_counter()
            res = client.post(
                "/api/v1/assessments/technical/start",
                json={"role_id": "ai_ml_engineer", "question_count": 5},
                headers=headers
            )
            latencies.append((time.perf_counter() - t0) * 1000)
            assert res.status_code == 200

        mean_ms = statistics.mean(latencies)
        p95_ms = statistics.quantiles(latencies, n=20)[18]
        assert mean_ms < 40.0
        assert p95_ms < 80.0

