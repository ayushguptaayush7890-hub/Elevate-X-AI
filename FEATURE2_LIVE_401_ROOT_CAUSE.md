# FEATURE 2 — LIVE BROWSER 401 UNAUTHORIZED ROOT CAUSE ANALYSIS & RESOLUTION
**Elevate X AI — Feature 2: Technical Assessment & Career Intelligence Engine**
**Author:** Senior Security, QA & Full-Stack Systems Engineer
**Status:** ✅ RESOLVED & VERIFIED

---

## 1. Executive Summary & Root Cause Confirmation

The recurring browser-level `HTTP 401 Unauthorized` on clicking **"Start Assessment"** at `http://localhost:3002/assessment` was NOT caused by invalid JWT signatures, nor was it caused by backend route misconfiguration.

### The True Root Cause Chain Discovered

1. **Missing Authentication Guard in `AssessmentPage` (`src/app/assessment/page.tsx`)**:
   - The `/api/v1/assessments/technical/roles` and `/roles/{role_id}` endpoints are public diagnostic endpoints that do NOT require a JWT token (`Depends(get_current_active_user)` was deliberately not placed on catalog queries so roles can be browsed freely).
   - However, the `POST /api/v1/assessments/technical/start` endpoint strictly enforces `current_user: User = Depends(get_current_active_user)`.
   - When any browser user navigated directly to `http://localhost:3002/assessment`, the page loaded all 9 roles and skills without requiring login.
   - When clicking **"Start Assessment"**, `handleStartAssessment()` immediately dispatched `POST /assessments/technical/start`.
   - In `src/lib/api.ts`, `localStorage.getItem("elevate_auth_token")` returned `null` because the user had not logged in.
   - `apiClient` omitted the `Authorization` header entirely.
   - The FastAPI backend logged:
     ```
     WARNING | elevate_x:http_exception_handler:78 - HTTP 401 at /api/v1/assessments/technical/start: Not authenticated
     ```
   - The UI toasted: `"Failed to start assessment: API Error: 401 Unauthorized"`, leaving the user stranded without explaining that authentication was required or redirecting them to log in.

2. **Login Page Default Credentials Mismatch (`src/app/login/page.tsx`)**:
   - `LoginPage` defaulted to `ramesh.sharma@example.com` / `Password@123`.
   - `ramesh.sharma@example.com` did NOT exist in `backend/elevate_x_local.db` (only `candidate@elevatex.ai`, `live.demo@elevatex.ai`, and test accounts were seeded).
   - Attempting to log in with the pre-filled form failed with `HTTP 401 / 400`.
   - `handleGoogleDemo` ("Continue with Demo Profile") bypassed the API call and called `login("demo.candidate@example.com", "user")` without providing a JWT token, leaving `localStorage.getItem("elevate_auth_token")` empty.

---

## 2. Evidence from Live Request Tracing

| Attribute | Captured Value |
|---|---|
| Request URL | `http://localhost:8000/api/v1/assessments/technical/start` |
| HTTP Method | `POST` |
| Request Payload | `{"role_id":"backend_developer","assessment_type":"mcq","difficulty":"adaptive","question_count":10}` |
| Response Status | `401 Unauthorized` |
| Response Body | `{"detail":"Not authenticated"}` |
| Authorization Header | **MISSING** (`null` read from `localStorage`) |
| Backend Log | `WARNING elevate_x: HTTP 401 at /api/v1/assessments/technical/start: Not authenticated` |

---

## 3. Implemented Fixes

### Fix A: Frontend Assessment Authentication Gate (`src/app/assessment/page.tsx`)
- Integrated `useAuth` from `@/context/AuthContext`.
- Added dynamic token detection:
  ```typescript
  const [hasToken, setHasToken] = useState<boolean>(false);
  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("elevate_auth_token") : null;
    setHasToken(Boolean(token));
  }, [isAuthenticated]);
  ```
- Added in-page **Candidate Authentication Status Badge**:
  - Authenticated: Displays green **Verified Candidate** pill.
  - Unauthenticated: Displays **Sign In to Save Results** with link to `/login?from=/assessment`.
- Added **Authentication Setup Callout Banner** on the Assessment Setup Card if unauthenticated, preventing confusion before the user clicks Start.
- Added proactive check in `handleStartAssessment()`:
  ```typescript
  const token = typeof window !== "undefined" ? localStorage.getItem("elevate_auth_token") : null;
  if (!token) {
    toast.error("Authentication required. Please sign in to start your technical assessment.");
    router.push("/login?from=/assessment");
    return;
  }
  ```

### Fix B: Login Page Authentication & Demo Flow (`src/app/login/page.tsx`)
- Changed pre-filled default credentials to verified existing database account:
  - Email: `candidate@elevatex.ai`
  - Password: `Password123!`
- Fixed `handleGoogleDemo` to perform authentic login against backend API:
  - Obtains real JWT `access_token`.
  - Persists token to `localStorage.setItem("elevate_auth_token", token)`.
  - Updates `AuthContext`.
  - Automatically redirects to the referring page (e.g., `/assessment`).

---

## 4. Verification & Status

- Unauthenticated click on Start Assessment now gracefully alerts user and redirects to `/login?from=/assessment`.
- Logging in via either standard credentials or Demo Profile writes verified JWT to `localStorage`.
- Subsequent Start Assessment requests attach valid `Bearer <token>` and return `HTTP 200 OK` with session ID and questions.
- **Root Cause Permanently Closed**: ✅ YES

