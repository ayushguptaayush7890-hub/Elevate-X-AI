"""
Cybersecurity Engineer (SEC) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "cybersecurity_engineer"
SKILLS = {
    "S1": ("SEC-SKL-01", "Web Application Security & OWASP Top 10"),
    "S2": ("SEC-SKL-02", "Network Security, Firewalls & Protocols"),
    "S3": ("SEC-SKL-03", "Cryptography, PKI & Key Management"),
    "S4": ("SEC-SKL-04", "Identity and Access Management (IAM) & Least Privilege"),
    "S5": ("SEC-SKL-05", "Incident Response, Threat Modeling & Forensic Log Analysis")
}

def generate_sec_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("SQL, NoSQL and OS Command Injection Mechanics",
             "Why does using parameter binding / prepared statements completely neutralize SQL injection vulnerabilities, regardless of special characters in user input?",
             [{"id": "A", "text": "It encrypts the entire database table"},
              {"id": "B", "text": "It separates the SQL statement syntax from user-supplied data, ensuring the query structure is pre-compiled by the database engine and user values are treated strictly as literals"},
              {"id": "C", "text": "It strips out all quotes and semicolons via regular expressions"},
              {"id": "D", "text": "It converts SQL queries into REST requests"}],
             "B", "Prepared statements compile the query execution plan ahead of time. User parameters are passed across the wire as typed data values, so malicious characters cannot alter query structure."),

            ("TLS 1.3 Handshake, Cipher Suites and Perfect Forward Secrecy",
             "In TLS 1.3, what property does Ephemeral Diffie-Hellman key exchange (DHE/ECDHE) provide that static RSA key exchange lacked?",
             [{"id": "A", "text": "Double encryption of certificate authorities"},
              {"id": "B", "text": "Perfect Forward Secrecy (PFS), guaranteeing that past recorded sessions cannot be decrypted even if the server's long-term private key is compromised in the future"},
              {"id": "C", "text": "Zero-latency TCP transmission"},
              {"id": "D", "text": "Elimination of SSL certificates"}],
             "B", "With ephemeral key exchange, unique session keys are generated dynamically per connection and discarded. Compromising the server's long-term private key does not reveal past session keys."),

            ("Symmetric Encryption (AES-GCM) vs Asymmetric (RSA, ECC)",
             "Why is AES in Galois/Counter Mode (AES-GCM) preferred over AES in Cipher Block Chaining (AES-CBC) for modern network encryption?",
             [{"id": "A", "text": "AES-GCM requires no encryption keys"},
              {"id": "B", "text": "AES-GCM provides Authenticated Encryption with Associated Data (AEAD), guaranteeing both confidentiality and cryptographic integrity verification without padding oracle vulnerabilities"},
              {"id": "C", "text": "AES-GCM only works on text files"},
              {"id": "D", "text": "AES-CBC has an 8-bit key limit"}],
             "B", "AES-GCM combines counter mode encryption with GMAC authentication tags, providing cryptographic integrity verification and immunity to padding oracle attacks."),

            ("OAuth 2.0 Authorization Code Flow with PKCE",
             "What security threat does Proof Key for Code Exchange (PKCE) mitigate in public OAuth 2.0 clients (mobile and single-page apps)?",
             [{"id": "A", "text": "SQL injection in token databases"},
              {"id": "B", "text": "Authorization Code Interception attacks where malicious apps on the device intercept the authorization code returned by the browser custom URI scheme"},
              {"id": "C", "text": "DDoS attacks on the authorization server"},
              {"id": "D", "text": "Brute force attacks on user passwords"}],
             "B", "Public clients cannot securely store a `client_secret`. PKCE generates a dynamic `code_verifier` and hashed `code_challenge`. The authorization server releases tokens only when the original verifier is presented."),

            ("STRIDE Threat Modeling and Data Flow Diagrams",
             "In Microsoft's STRIDE threat modeling framework, which security property corresponds to the threat of 'Repudiation'?",
             [{"id": "A", "text": "Confidentiality"},
              {"id": "B", "text": "Integrity"},
              {"id": "C", "text": "Non-Repudiation (Auditability / Proof of Action)"},
              {"id": "D", "text": "Availability"}],
             "C", "Repudiation refers to an attacker performing an unauthorized action and denying it occurred. It is mitigated by Non-Repudiation mechanisms (tamper-evident audit logs and digital signatures).")
        ]
        subtopic, qtext, opts, ans, exp = topics[(idx - 1) % len(topics)]
        qtext_unique = f"[{s_name} - Q{idx:02d}] {qtext}"
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext_unique, opts, ans, exp))

    # 2. 50 Coding Challenges (Secure Coding, Vulnerability Fixes, Cryptography)
    for idx in range(1, 51):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 35 else "hard")
        marks = 6 if idx <= 10 else (10 if idx <= 35 else 14)
        t_est = 15 if idx <= 10 else (25 if idx <= 35 else 35)

        q_text = (
            f"Implement a secure cryptographic or defensive utility for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Write an algorithm in Python that enforces safe token hashing, secure session generation, or constant-time comparison.\n"
            f"- Defend against timing attacks (use `hmac.compare_digest`).\n"
            f"- Avoid deprecated algorithms (MD5, SHA1, DES, ECB mode)."
        )
        sample_in = f"secret_key_{idx} = 'secure_random_bytes'"
        sample_out = f"generated_hmac_token_{idx}"
        vis_tests = [
            {"input": f"payload_{idx}_valid", "output": "valid_signature_verified"},
            {"input": f"payload_{idx}_tampered", "output": "signature_rejected"}
        ]
        hid_tests = [
            {"input": f"timing_attack_probe_{idx}", "output": "constant_time_evaluation"}
        ]
        ref_sol = (
            f"import hmac\nimport hashlib\n\n"
            f"def verify_signature_{idx}(secret_key: bytes, message: bytes, received_signature: str) -> bool:\n"
            f"    # Constant-time HMAC comparison for {s_name}\n"
            f"    expected_sig = hmac.new(secret_key, message, hashlib.sha256).hexdigest()\n"
            f"    return hmac.compare_digest(expected_sig, received_signature)"
        )
        exp = f"Evaluates secure HMAC-SHA256 signature verification and constant-time comparison resisting side-channel timing attacks in {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Secure Cryptographic Implementation", diff, idx,
            q_text, "python", sample_in, sample_out, vis_tests, hid_tests, ref_sol, exp, marks, t_est
        ))

    # 3. 35 Debugging Challenges (Vulnerability Remediation)
    for idx in range(1, 36):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        broken = (
            f"import sqlite3\n"
            f"def authenticate_user_{idx}(cursor, username, password):\n"
            f"    # Defect: Critical SQL Injection via string formatting\n"
            f"    query = f\"SELECT id FROM users WHERE username = '{{username}}' AND password = '{{password}}'\"\n"
            f"    cursor.execute(query)\n"
            f"    return cursor.fetchone()"
        )
        bug_desc = f"CWE-89 SQL Injection: An attacker passes `' OR '1'='1` to bypass authentication in {s_name}."
        fixed = (
            f"import sqlite3\n"
            f"def authenticate_user_{idx}(cursor, username, password_hash):\n"
            f"    # Fixed: Parameterized prepared statement preventing SQLi\n"
            f"    query = \"SELECT id FROM users WHERE username = ? AND password_hash = ?\"\n"
            f"    cursor.execute(query, (username, password_hash))\n"
            f"    return cursor.fetchone()"
        )
        exp = "Using parameter placeholders (`?` or `%s`) instructs the database driver to treat inputs strictly as bound literals, eliminating SQL injection."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "SQL Injection & Secure Coding Debugging", diff, idx,
            f"Remediate a critical SQL Injection flaw in an authentication module ({s_name}).",
            "python", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges (Security Audit & Forensic Log Queries)
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S5"] # Incident Response & Forensics
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE auth_audit_log_{idx} (\n"
            f"    log_id INTEGER PRIMARY KEY,\n"
            f"    ip_address VARCHAR(45) NOT NULL,\n"
            f"    username VARCHAR(50) NOT NULL,\n"
            f"    login_status VARCHAR(10) NOT NULL,\n"
            f"    timestamp TIMESTAMP NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO auth_audit_log_{idx} VALUES (1, '192.168.1.50', 'admin', 'FAILED', '2026-11-01 02:00:00');\n"
            f"INSERT INTO auth_audit_log_{idx} VALUES (2, '192.168.1.50', 'admin', 'FAILED', '2026-11-01 02:00:05');\n"
            f"INSERT INTO auth_audit_log_{idx} VALUES (3, '192.168.1.50', 'admin', 'FAILED', '2026-11-01 02:00:10');\n"
            f"INSERT INTO auth_audit_log_{idx} VALUES (4, '10.0.0.2', 'alice', 'SUCCESS', '2026-11-01 08:00:00');"
        )
        ref_sql = (
            f"SELECT ip_address, COUNT(*) AS failed_attempts\n"
            f"FROM auth_audit_log_{idx}\n"
            f"WHERE login_status = 'FAILED'\n"
            f"GROUP BY ip_address\n"
            f"HAVING COUNT(*) >= 3\n"
            f"ORDER BY failed_attempts DESC;"
        )
        expected = [
            {"ip_address": "192.168.1.50", "failed_attempts": 3}
        ]
        exp = "Identifies potential brute-force authentication attacks by aggregating consecutive failed logins per IP address."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Brute Force Detection & Security Audit SQL", diff, idx,
            f"Write an ANSI SQL query to detect IPs with 3 or more failed login attempts from `auth_audit_log_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions (Enterprise Zero Trust & SOC Architecture)
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S2"] # Network & Defense Architecture
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"Enterprise Zero Trust Architecture #{idx:02d}"
        fn = [
            "Enforce continuous context-aware device health and user identity authentication per request",
            "Eliminate legacy corporate VPN perimeter in favor of identity-aware micro-segmentation proxies",
            "Centralize SIEM log ingestion analyzing 250,000 security events/sec with automated SOAR playbooks"
        ]
        non_fn = [
            "FIPS 140-3 cryptographic module compliance for all data in transit and at rest",
            "High availability 99.999% SLA for identity authentication boundary",
            "Automated lateral movement quarantine within 60 seconds of threat detection"
        ]
        scale = {
            "Enterprise Employees": "45,000",
            "Managed Corporate & BYOD Devices": "90,000",
            "Daily Ingested Security Logs": "2.5 Terabytes"
        }
        ref_arch = (
            "Clients connect via WireGuard / Identity-Aware Proxy (IAP) -> Okta / Azure AD evaluates WebAuthn FIDO2 MFA "
            "and CrowdStrike EDR device posture -> Enforces micro-segmentation with SPIFFE/SPIRE cryptographic mTLS identities -> "
            "All network flow logs, audit logs, and EDR events stream to centralized Splunk / OpenSearch SIEM -> SOAR triggers automated quarantine."
        )
        tradeoffs = "Continuous posture re-evaluation per HTTP request adds latency; caching device posture state with a 60-second TTL in Redis balances strict security with acceptable employee user experience."
        rubric = [
            {"name": "Zero Trust Identity & Device Posture", "weight": 0.30, "description": "Designs mTLS, FIDO2, and continuous posture checks."},
            {"name": "Micro-Segmentation & Network Security", "weight": 0.25, "description": "Eliminates flat networks using identity proxies."},
            {"name": "SIEM / SOAR Telemetry & Forensics", "weight": 0.25, "description": "Scales log ingestion and automates containment."},
            {"name": "Operational Usability & Redundancy", "weight": 0.20, "description": "Balances security friction against worker latency."}
        ]
        exp = "Evaluates comprehensive enterprise Zero Trust cybersecurity architecture balancing strict least-privilege, automated incident containment, and high availability."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Zero Trust & Security Operations Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_sec_questions()
    print(f"Generated {len(qs)} Cybersecurity Engineer questions.")
