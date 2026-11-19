"""
Security & Isolation Test Suite for Feature 2:
Validates SQL Sandbox, Python Code Sandbox, Environment Isolation, and Auth Boundary Controls.
"""

import pytest
import sqlite3
from fastapi.testclient import TestClient
from app.services.sandboxes import SQLSandbox, CodeSandbox

def _register_user(client: TestClient, email: str, name: str) -> tuple[dict, str]:
    res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "full_name": name},
    )
    assert res.status_code == 201
    data = res.json()
    token = data["token"]["access_token"]
    user_id = data["user"]["id"]
    return {"Authorization": f"Bearer {token}"}, user_id


class TestSQLSandboxSecurity:
    """Verifies SQLite memory sandbox restrictions, query_only mode, and C-level authorizer."""

    def test_sql_drop_table_blocked(self):
        res = SQLSandbox.execute_and_grade(
            schema_sql="CREATE TABLE accounts (id INT, balance INT);",
            sample_db_sql="INSERT INTO accounts VALUES (1, 1000);",
            candidate_query="DROP TABLE accounts;"
        )
        assert res["passed"] is False
        assert "Only read-only queries" in res["error"] or "Disallowed" in res["error"] or "Blocked" in res["error"]

    def test_sql_insert_mutation_blocked(self):
        res = SQLSandbox.execute_and_grade(
            schema_sql="CREATE TABLE users (id INT, name TEXT);",
            sample_db_sql="INSERT INTO users VALUES (1, 'Alice');",
            candidate_query="INSERT INTO users VALUES (2, 'Hacker');"
        )
        assert res["passed"] is False

    def test_sql_attach_database_blocked(self):
        # Attempt to attach host filesystem database
        res = SQLSandbox.execute_and_grade(
            schema_sql="CREATE TABLE items (id INT);",
            sample_db_sql="INSERT INTO items VALUES (1);",
            candidate_query="ATTACH DATABASE '/tmp/pwned.db' AS pwned; SELECT * FROM items;"
        )
        assert res["passed"] is False

    def test_sql_pragma_tampering_blocked(self):
        res = SQLSandbox.execute_and_grade(
            schema_sql="CREATE TABLE items (id INT);",
            sample_db_sql="INSERT INTO items VALUES (1);",
            candidate_query="PRAGMA journal_mode = OFF; SELECT * FROM items;"
        )
        assert res["passed"] is False

    def test_sql_valid_query_succeeds(self):
        res = SQLSandbox.execute_and_grade(
            schema_sql="CREATE TABLE stats (category TEXT, val INT);",
            sample_db_sql="INSERT INTO stats VALUES ('A', 10), ('B', 20);",
            candidate_query="SELECT category, val FROM stats WHERE val > 15;",
            expected_result=[{"category": "B", "val": 20}]
        )
        assert res["passed"] is True
        assert res["score"] == 1.0
        assert res["actual_rows"] == [{"category": "B", "val": 20}]


class TestCodeSandboxSecurity:
    """Verifies Python sandbox static analysis, child process isolation, timeouts, and network blocks."""

    def test_file_read_attempt_blocked(self):
        evil_code = """
with open('/etc/passwd', 'r') as f:
    data = f.read()
"""
        res = CodeSandbox.execute_and_grade("python", evil_code, [{"input": "test", "output": "ok"}])
        # Either static analysis blocks open() or runtime fails
        assert res["passed"] is False

    def test_os_system_command_blocked(self):
        evil_code = "import os\nos.system('whoami')"
        res = CodeSandbox.execute_and_grade("python", evil_code, [{"input": "test", "output": "ok"}])
        assert res["passed"] is False
        assert "Security Alert" in res["error"]

    def test_subprocess_spawning_blocked(self):
        evil_code = "import subprocess\nsubprocess.run(['ls', '-la'])"
        res = CodeSandbox.execute_and_grade("python", evil_code, [{"input": "test", "output": "ok"}])
        assert res["passed"] is False
        assert "Security Alert" in res["error"]

    def test_os_environ_inspection_blocked(self):
        evil_code = "import os\nsecrets = os.environ.get('SECRET_KEY', '')"
        res = CodeSandbox.execute_and_grade("python", evil_code, [{"input": "test", "output": "ok"}])
        assert res["passed"] is False
        assert "Security Alert" in res["error"]

    def test_socket_network_access_blocked(self):
        evil_code = "import socket\ns = socket.socket()"
        res = CodeSandbox.execute_and_grade("python", evil_code, [{"input": "test", "output": "ok"}])
        assert res["passed"] is False
        assert "Security Alert" in res["error"]

    def test_infinite_loop_timeout_enforced(self):
        loop_code = """
x = 0
while True:
    x += 1
"""
        res = CodeSandbox.execute_and_grade("python", loop_code, [{"input": "1", "output": "1"}], timeout_seconds=1.5)
        assert res["passed"] is False
        assert "Timeout" in res["error"]

    def test_safe_computation_passes(self):
        safe_code = """
def solution(nums):
    return sum(nums)

assert solution([1, 2, 3, 4]) == 10
"""
        res = CodeSandbox.execute_and_grade("python", safe_code, [{"input": "[1, 2, 3, 4]", "output": "10"}])
        assert res["passed"] is True
        assert res["score"] == 1.0


class TestAuthAndDataIsolation:
    """Verifies that unauthorized requests are denied and user data is isolated."""

    def test_unauthenticated_requests_denied(self, client: TestClient):
        # Start without token
        res1 = client.post("/api/v1/assessments/technical/start", json={"role_id": "software_engineer"})
        assert res1.status_code == 401

        # Submit without token
        res2 = client.post("/api/v1/assessments/technical/submit", json={"session_id": "fake", "role_id": "software_engineer", "answers": []})
        assert res2.status_code == 401

        # History without token
        res3 = client.get("/api/v1/assessments/technical/history")
        assert res3.status_code == 401

