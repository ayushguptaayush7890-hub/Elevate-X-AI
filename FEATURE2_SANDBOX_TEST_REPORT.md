# FEATURE 2: SECURE SANDBOX ARCHITECTURE & AUDIT REPORT
**Elevate X AI — Technical Assessment & Career Intelligence Engine**  
**Execution Date:** November 15, 2026  
**Auditor:** Lead Security & Infrastructure Engineer  

---

## 1. Overview & Security Objectives

Candidate evaluation requires executing untrusted, user-submitted code and SQL queries. The sandbox subsystem in [backend/app/services/sandboxes.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/app/services/sandboxes.py) guarantees:
1. **Total Prevention of Host Tampering:** No filesystem modifications, process spawning, or shell escapes.
2. **Confidentiality:** Host environment variables, API keys, database credentials, and other tenants' data are completely shielded.
3. **Availability & Resource Governance:** Strict execution timeouts and memory/CPU limits prevent denial-of-service loops.

---

## 2. Python Code Sandbox Architecture

### 2.1 Defense-in-Depth Layers
- **Layer 1 (Pre-Execution Static AST / Regex Gate):**  
  Scans submitted candidate code for dangerous keywords and patterns before writing to disk:
  - `os.system`, `subprocess`, `shutil`
  - `open(`, `pathlib`
  - `__import__`, `eval(`, `exec(`
  - `os.environ`, `os.getenv`
  - `socket`, `requests`, `urllib`, `http`
  - `pty`, `ctypes`
- **Layer 2 (Runtime Module Nullification):**  
  The generated test runner script explicitly disables sensitive network and socket libraries inside `sys.modules` prior to executing candidate code.
- **Layer 3 (Sanitized Process Environment):**  
  The child process is invoked with a stripped environment dictionary containing only `PATH`, `PYTHONPATH=""`, and `HOME=temp_dir`.
- **Layer 4 (Operating System Resource Limits):**  
  Unix `resource.setrlimit` restricts CPU execution time to `timeout_seconds + 1` and address space to 256MB.
- **Layer 5 (Isolated Ephemeral Directory):**  
  Runs inside a dedicated temporary directory (`mkdtemp`) which is cleaned up immediately in a `finally:` block.

---

## 3. SQL Sandbox Architecture

### 3.1 Defense-in-Depth Layers
- **Layer 1 (Lexical Grammar Gate):**  
  Strips SQL comments (`--`, `/* */`), validates that the initial statement is strictly `SELECT` or `WITH`, and checks for mutation keywords (`DROP`, `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `CREATE`, `ATTACH`, `PRAGMA`).
- **Layer 2 (Engine Read-Only Enforcement):**  
  Executes `PRAGMA query_only = ON;` before candidate query execution.
- **Layer 3 (SQLite C-Level Authorizer Callback):**  
  Registers `sqlite3.set_authorizer` callback. Rejects all actions other than `SQLITE_SELECT`, `SQLITE_READ`, and `SQLITE_FUNCTION`. Attempts to attach host databases or manipulate SQLite pragmas trigger immediate C-level termination.
- **Layer 4 (Transient Memory Isolation):**  
  Uses fresh `:memory:` SQLite connections per invocation, guaranteeing zero cross-session data leakage.

---

## 4. Test Verification Summary
All 13 adversarial test cases in [tests/test_feature2_security.py](file:///Users/ayushgupta/Desktop/Resume_Ai/backend/tests/test_feature2_security.py) passed:
- `test_sql_drop_table_blocked`: PASSED
- `test_sql_insert_mutation_blocked`: PASSED
- `test_sql_attach_database_blocked`: PASSED
- `test_sql_pragma_tampering_blocked`: PASSED
- `test_sql_valid_query_succeeds`: PASSED
- `test_file_read_attempt_blocked`: PASSED
- `test_os_system_command_blocked`: PASSED
- `test_subprocess_spawning_blocked`: PASSED
- `test_os_environ_inspection_blocked`: PASSED
- `test_socket_network_access_blocked`: PASSED
- `test_infinite_loop_timeout_enforced`: PASSED
- `test_safe_computation_passes`: PASSED
- `test_unauthenticated_requests_denied`: PASSED

