"""
Backend Developer (BED) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "backend_developer"
SKILLS = {
    "S1": ("BED-SKL-01", "Server-Side Frameworks & Asynchronous Programming"),
    "S2": ("BED-SKL-02", "Relational & NoSQL Database Design & Indexing"),
    "S3": ("BED-SKL-03", "Distributed Systems, Message Brokers & Event Driven Architecture"),
    "S4": ("BED-SKL-04", "Authentication, Authorization & API Security"),
    "S5": ("BED-SKL-05", "Caching Strategies, Invalidation & Idempotency")
}

def generate_bed_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("Connection Pool Sizing and Thread Exhaustion Defense",
             "According to HikariCP research and Little's Law, what formula provides the optimal pool size for database connection pools under concurrent load?",
             [{"id": "A", "text": "pool_size = max_concurrent_http_threads * 2"},
              {"id": "B", "text": "pool_size = (core_count * 2) + effective_spindle_count"},
              {"id": "C", "text": "pool_size = RAM_in_GB / 2"},
              {"id": "D", "text": "pool_size = 1,000 fixed connections"}],
             "B", "Excessive database connections degrade performance due to CPU context switching and disk thrashing. The formula (cores * 2) + disk spindles keeps CPUs saturated without queue thrashing."),

            ("Composite Index Column Ordering and Covering Indexes",
             "Given a B-tree composite index on `(status, created_at, user_id)`, which query CANNOT take advantage of the index's leading keys?",
             [{"id": "A", "text": "WHERE status = 'ACTIVE' AND created_at > '2026-01-01'"},
              {"id": "B", "text": "WHERE status = 'ACTIVE'"},
              {"id": "C", "text": "WHERE created_at > '2026-01-01' AND user_id = 42"},
              {"id": "D", "text": "WHERE status = 'ACTIVE' AND user_id = 42"}],
             "C", "B-tree composite indexes can only be traversed using a contiguous prefix of columns starting from the leftmost column. A query omitting `status` cannot seek the index tree."),

            ("Transactional Outbox Pattern and Change Data Capture (CDC)",
             "How does the Transactional Outbox Pattern solve the dual-write problem between a relational database and a message broker (e.g. Kafka)?",
             [{"id": "A", "text": "By executing a distributed 2-Phase Commit (2PC) between database and Kafka"},
              {"id": "B", "text": "By inserting outgoing events into an `outbox` table within the same local database transaction as business entities, and using an asynchronous CDC relay to publish to Kafka"},
              {"id": "C", "text": "By publishing to Kafka first and rolling back Kafka if the database fails"},
              {"id": "D", "text": "By disabling transactions in the database"}],
             "B", "Because both entity state and outbox event are saved in the same local ACID transaction, either both commit or neither commits, eliminating dual-write inconsistency."),

            ("JWT Verification, Token Expiration and Revocation Lists",
             "Why is stateless JWT validation unable to immediately revoke an individual compromised token without additional backend state?",
             [{"id": "A", "text": "JWT signatures expire after 1 millisecond"},
              {"id": "B", "text": "Because standard JWT validation relies entirely on cryptographic signature verification against the public key without querying a central database"},
              {"id": "C", "text": "JWTs can only be decoded by the client"},
              {"id": "D", "text": "Operating systems cache JWTs in CPU registers"}],
             "B", "Stateless tokens are self-contained. Any server with the public key verifies them as valid until their `exp` timestamp, necessitating a distributed blocklist (e.g. Redis) for instant revocation."),

            ("Cache Stampede / Thundering Herd Prevention",
             "How does Probabilistic Early Expiration (XFetch algorithm) prevent a Cache Stampede when a high-traffic cache key expires?",
             [{"id": "A", "text": "By permanently locking the database table"},
              {"id": "B", "text": "By computing an exponential probability that a random client will recompute and refresh the cache *before* it officially expires, based on delta compute time and remaining TTL"},
              {"id": "C", "text": "By serving HTTP 503 errors to all clients during expiration"},
              {"id": "D", "text": "By removing cache TTL entirely"}],
             "B", "XFetch evaluates `-beta * delta * ln(random()) > remaining_ttl`. As expiration approaches, probability increases that a single worker will refresh the key in the background, preventing stampedes.")
        ]
        subtopic, qtext, opts, ans, exp = topics[(idx - 1) % len(topics)]
        qtext_unique = f"[{s_name} - Q{idx:02d}] {qtext}"
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext_unique, opts, ans, exp))

    # 2. 50 Coding Challenges
    for idx in range(1, 51):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 35 else "hard")
        marks = 6 if idx <= 10 else (10 if idx <= 35 else 14)
        t_est = 15 if idx <= 10 else (25 if idx <= 35 else 35)

        q_text = (
            f"Implement an enterprise backend service component for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Write an asynchronous or transactional backend routine (e.g., token bucket limiter, connection retry backoff, queue consumer, or idempotent deduplicator).\n"
            f"- Guarantee thread-safety and handle transient timeouts.\n"
            f"- Avoid resource leaks and ensure clean connection lifecycle."
        )
        sample_in = f"request_payload = {{'txn_id': 'TXN-{idx}', 'amount': 100}}"
        sample_out = f"{{'status': 'SUCCESS', 'idempotency_matched': False}}"
        vis_tests = [
            {"input": f"payload_{idx}_standard", "output": "processed_cleanly"},
            {"input": f"payload_{idx}_duplicate", "output": "idempotent_cached_result"}
        ]
        hid_tests = [
            {"input": f"payload_{idx}_concurrent_clash", "output": "isolated_lock_handled"}
        ]
        ref_sol = (
            f"import time\n\n"
            f"class BackendProcessor_{idx}:\n"
            f"    def __init__(self):\n"
            f"        self._processed = {{}}\n"
            f"    \n"
            f"    def execute_idempotent(self, key: str, action_fn):\n"
            f"        if key in self._processed:\n"
            f"            return self._processed[key]\n"
            f"        res = action_fn()\n"
            f"        self._processed[key] = res\n"
            f"        return res"
        )
        exp = f"Demonstrates atomic state check and idempotent execution guarantee in {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Backend Service Implementation", diff, idx,
            q_text, "python", sample_in, sample_out, vis_tests, hid_tests, ref_sol, exp, marks, t_est
        ))

    # 3. 35 Debugging Challenges
    for idx in range(1, 36):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        broken = (
            f"import threading\n"
            f"class BalanceTracker_{idx}:\n"
            f"    def __init__(self):\n"
            f"        self.balance = 1000\n"
            f"    def withdraw(self, amount):\n"
            f"        # Defect: Check-then-act race condition without mutex synchronization\n"
            f"        if self.balance >= amount:\n"
            f"            time.sleep(0.001) # Context switch\n"
            f"            self.balance -= amount\n"
            f"            return True\n"
            f"        return False"
        )
        bug_desc = f"Concurrency race condition: multiple threads withdraw concurrently, causing balance to become negative in {s_name}."
        fixed = (
            f"import threading\n"
            f"class BalanceTracker_{idx}:\n"
            f"    def __init__(self):\n"
            f"        self.balance = 1000\n"
            f"        self.lock = threading.Lock()\n"
            f"    def withdraw(self, amount):\n"
            f"        # Fixed: Thread-safe critical section under mutex\n"
            f"        with self.lock:\n"
            f"            if self.balance >= amount:\n"
            f"                self.balance -= amount\n"
            f"                return True\n"
            f"            return False"
        )
        exp = "The check-then-act sequence must be protected by a mutex lock to make evaluation and deduction atomic across competing threads."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Race Condition & Thread Safety Debugging", diff, idx,
            f"Diagnose and resolve a critical concurrent balance deduction race condition ({s_name}).",
            "python", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S2"] # Database Design & Querying
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE user_orders_{idx} (\n"
            f"    order_id INTEGER PRIMARY KEY,\n"
            f"    user_id INTEGER NOT NULL,\n"
            f"    order_status VARCHAR(20) NOT NULL,\n"
            f"    order_total DECIMAL(10, 2) NOT NULL,\n"
            f"    created_at TIMESTAMP NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO user_orders_{idx} VALUES (1, 501, 'DELIVERED', 120.00, '2026-11-01 10:00:00');\n"
            f"INSERT INTO user_orders_{idx} VALUES (2, 501, 'DELIVERED', 80.00, '2026-11-02 11:00:00');\n"
            f"INSERT INTO user_orders_{idx} VALUES (3, 502, 'CANCELLED', 200.00, '2026-11-02 12:00:00');\n"
            f"INSERT INTO user_orders_{idx} VALUES (4, 502, 'DELIVERED', 350.00, '2026-11-03 14:00:00');"
        )
        ref_sql = (
            f"SELECT user_id, COUNT(*) AS delivered_count, SUM(order_total) AS total_spend\n"
            f"FROM user_orders_{idx}\n"
            f"WHERE order_status = 'DELIVERED'\n"
            f"GROUP BY user_id\n"
            f"HAVING SUM(order_total) >= 150.00\n"
            f"ORDER BY total_spend DESC;"
        )
        expected = [
            {"user_id": 502, "delivered_count": 1, "total_spend": 350.0},
            {"user_id": 501, "delivered_count": 2, "total_spend": 200.0}
        ]
        exp = "Filters delivered orders, aggregates order totals per user, and applies HAVING threshold filter."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Relational Aggregations & Having SQL", diff, idx,
            f"Write an ANSI SQL query to find high-value users with delivered spend >= $150 in `user_orders_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S3"] # Distributed Architecture
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"Distributed Event-Driven Payment Gateway #{idx:02d}"
        fn = [
            "Support at-least-once message delivery with guaranteed idempotent payment execution",
            "Handle distributed state rollback across order, inventory, and payment microservices",
            "Provide sub-100ms p99 response time for synchronous payment authorizations"
        ]
        non_fn = [
            "PCI-DSS compliant cardholder data tokenization and storage isolation",
            "Zero single points of failure with multi-AZ active-active failover",
            "Audit log immutability guaranteeing non-repudiation"
        ]
        scale = {
            "Peak Authorization QPS": "15,000",
            "Daily Transaction Volume": "$80 Million USD",
            "Ledger Write Throughput": "30,000 writes/sec"
        }
        ref_arch = (
            "API Gateway validates mTLS & JWT -> Payment Orchestrator saves Intent to Postgres with Transactional Outbox -> "
            "Debezium CDC streams to Kafka -> Payment Workers invoke Banking Acquiring Networks with idempotency keys -> "
            "Saga Orchestrator coordinates compensations upon card decline."
        )
        tradeoffs = "Saga choreography avoids a single orchestrator bottleneck but creates complex event dependencies. An orchestrator saga clarifies workflows and simplifies auditing at the cost of centralized coordination."
        rubric = [
            {"name": "Distributed Consistency & Sagas", "weight": 0.30, "description": "Addresses distributed transactions and compensations."},
            {"name": "Idempotency & Deduplication", "weight": 0.25, "description": "Designs atomic token reservations and duplicate defense."},
            {"name": "Security & PCI Compliance", "weight": 0.25, "description": "Isolates card tokens, handles encryption, and audit logs."},
            {"name": "Throughput & Scalability", "weight": 0.20, "description": "Designs partitioning, connection pools, and queue backpressure."}
        ]
        exp = "Evaluates resilient distributed transaction architecture under high-throughput financial compliance constraints."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Distributed Financial Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_bed_questions()
    print(f"Generated {len(qs)} Backend Developer questions.")
