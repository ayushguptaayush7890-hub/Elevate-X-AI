# FEATURE 2 — BUGS AND FIXES LOG
**Elevate X AI | Feature 2: Technical Assessment & Career Intelligence Engine**
**Last Updated:** 2026-11-15

---

## Critical Bugs Fixed

### BUG-001: HTTP 401 Unauthorized on "Start Assessment" (CRITICAL)
**Symptom:** Clicking "Start Assessment" always returned 401 even after successful login  
**Root Cause Chain:**
1. `AuthContext.login()` wrote `"demo-token-" + Date.now()` to localStorage instead of real JWT
2. `api-service.ts login()` had `fallbackData` returning fake `"demo-jwt-token-elevate-x"` on network errors
3. `login/page.tsx` passed token to `login()` but `login()` ignored it
4. Backend DATABASE_URL pointed to unavailable PostgreSQL

**Files Fixed:**
- `src/context/AuthContext.tsx` — accept and store real JWT token
- `src/services/api-service.ts` — remove fallbackData from login() and register()
- `src/app/login/page.tsx` — pass real token; show error on failure
- `src/app/signup/page.tsx` — same fix
- `backend/.env` — DATABASE_URL → SQLite
- `backend/app/core/database.py` — add SQLite check_same_thread=False

**Status:** ✅ FIXED | **Verified:** HTTP 200 on /start with real JWT

---

### BUG-002: HTTP 404 on /api/v1/assessments/technical/roles (HIGH)
**Symptom:** Assessment page showed "Failed to load technical roles: API Error: 404 Not Found"  
**Root Cause:** Backend process was started before the technical assessment router was registered; stale process serving old routes  
**Fix:** Killed old uvicorn process; started new instance with --reload flag; router registration confirmed  
**Status:** ✅ FIXED

---

### BUG-003: PostgreSQL Not Running — All Backend Requests Failed (HIGH)
**Symptom:** All authenticated API requests returned HTTP 500  
**Root Cause:** `backend/.env` DATABASE_URL = PostgreSQL, but no PostgreSQL process running  
**Fix:** Switched DATABASE_URL to `sqlite:///./elevate_x_local.db`; added SQLite connect_args  
**Status:** ✅ FIXED

---

## Medium Bugs Fixed

### BUG-004: Duplicate React Key Warning for `SP-01` (MEDIUM)
**Symptom:** Console warning: Encountered two children with the same key, SP-01  
**Root Cause:** `skill_performance` map used `sp.skill_id` as React key; multiple items could share the same skill_id  
**Fix:** Changed key to `${sp.skill_id}-${idx}` using array index as tiebreaker  
**Status:** ✅ FIXED

---

### BUG-005: Bayesian Test `KeyError: 'attempts'` (MEDIUM)
**Symptom:** Backend unit test failed with KeyError  
**Root Cause:** Test used field `attempts` but schema uses `evidence_count`  
**Fix:** Updated test assertions to use correct field names (`evidence_count`, not `attempts`; `overall_score_percentage` not `overall_score`)  
**Status:** ✅ FIXED

---

### BUG-006: Matrix Test `KeyError: 'total_attempts'` (MEDIUM)
**Symptom:** Role-assessment matrix test failed  
**Root Cause:** Test referenced `total_attempts` which does not exist in response schema  
**Fix:** Updated test to use `overall_score_percentage`  
**Status:** ✅ FIXED

---

### BUG-007: Matrix Tests 401 Errors from Shared User Email (MEDIUM)
**Symptom:** When multiple matrix test iterations used the same email, SQLite unique constraint violated  
**Root Cause:** Tests sharing a single user email across all 54 combinations  
**Fix:** Each combination uses unique email `auditor.{role_id}.{type}@elevatex.ai`  
**Status:** ✅ FIXED

---

### BUG-008: Code Sandbox File Read Not Blocked (MEDIUM)
**Symptom:** `open('/etc/passwd')` returned `passed: True` in sandbox security test  
**Root Cause:** Static regex pattern only blocked `open(..., 'w')` write-mode calls  
**Fix:** Broadened pattern to `r'\bopen\s*\('` to block all `open()` calls  
**Status:** ✅ FIXED

---

### BUG-009: `NameError: name 'json' is not defined` in Dataset Generator (MEDIUM)
**Symptom:** Dataset generator script crashed  
**Root Cause:** `import json` missing from module  
**Fix:** Added `import json` at top of file  
**Status:** ✅ FIXED

---

## Shell Script Bugs (Test Infrastructure Only)

### BUG-010: 54-Combination Matrix Shell Script Falsely Reported 45 Failures (LOW)
**Symptom:** Shell matrix test reported "9 PASSED, 45 FAILED" but Python test reported "54 PASSED"  
**Root Cause:** Coding/SQL/scenario question texts contain literal newline control characters embedded in JSON; shell variable substitution breaks `python3 -c "json.load(sys.stdin)"` when control chars are present  
**Fix:** Rewrote matrix test using Python `requests` library instead of shell curl + variable substitution  
**Status:** ✅ FIXED (test infrastructure only; backend was always correct)

---

### BUG-011: Assessment Page Allowed Unauthenticated Users to Click "Start Assessment" (HIGH)
**Symptom:** Users visiting `/assessment` directly without logging in could configure an assessment and click "Start Assessment", resulting in a jarring `API Error: 401 Unauthorized` popup.  
**Root Cause:** The assessment page loaded roles and skill taxonomies publicly (unauthenticated GET endpoints), but `/api/v1/assessments/technical/start` requires an authenticated JWT bearer token. `src/app/assessment/page.tsx` had no client-side pre-flight authentication check before dispatching the start request.  
**Fix:** 
1. Added `useAuth` and `useRouter` integration in `src/app/assessment/page.tsx`.
2. Added client-side token detection (`localStorage.getItem("elevate_auth_token")`).
3. Displayed header auth badge: "Verified Candidate" (green) when authenticated, or "Sign In to Save Results" (gold) with a direct login button when unauthenticated.
4. Added an authentication callout banner in the setup card for unauthenticated users.
5. In `handleStartAssessment()`, performed a pre-flight token check: if unauthenticated, displayed a friendly error notification and redirected cleanly to `/login?from=/assessment`.
6. Gracefully caught 401 response errors to redirect expired sessions to login.  
**Status:** ✅ FIXED

---

### BUG-012: Login Page Defaulted to Non-Existent User and Google Demo Bypassed JWT (HIGH)
**Symptom:** Quick-fill login button used non-existent email `ramesh.sharma@example.com` / `Password@123`, and "Continue with Google" demo called `login(email, "user")` without a valid JWT, leaving `localStorage` empty and causing 401 on `/start`.  
**Root Cause:** Mismatch between seeded DB users (`candidate@elevatex.ai` / `Password123!`) and hardcoded demo credentials in `src/app/login/page.tsx`.  
**Fix:**
1. Changed default credentials in `src/app/login/page.tsx` to `candidate@elevatex.ai` / `Password123!`.
2. Updated `handleGoogleDemo` to perform real API login/registration via `authService.login()` or `authService.register()` to issue and store a genuine cryptographic JWT token.
3. Added `?from=` query parameter support so logging in returns candidates directly back to `/assessment`.  
**Status:** ✅ FIXED

---

### BUG-013: Heavy PyTorch Import Blocked FastAPI Backend Server Cold Start (HIGH)
**Symptom:** Backend process took over 12 minutes to start, blocking port 8000 from binding due to top-level `from datasets.informal_skill_extraction.models.model_service import SkillExtractionService` in `app/api/v1/skill.py`.  
**Root Cause:** Module-level import triggered loading of PyTorch, CUDA/MPS checks, and transformer model weights on initial module import, stalling Uvicorn server startup.  
**Fix:** Refactored `backend/app/api/v1/skill.py` to lazily import `SkillExtractionService` and `default_config` inside accessor functions (`_get_skill_extraction_service()`), deferring PyTorch load until `/skills/extract` endpoints are actually invoked. Server cold-start latency dropped from 12+ minutes to < 1.0 second.  
**Status:** ✅ FIXED

---

## Open Issues (Non-Critical)

| Issue | Severity | Status |
|---|---|---|
| Python sandbox has no OS-level isolation (no gVisor/Firecracker) | MEDIUM | Known blocker; arbitrary execution disabled by default |
| `AuthContext.isAuthenticated` resets on page refresh until `useEffect` hydrates | LOW | Expected behavior for localStorage auth; no security impact |
