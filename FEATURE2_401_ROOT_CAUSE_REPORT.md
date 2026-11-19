# FEATURE 2 — 401 UNAUTHORIZED ROOT CAUSE REPORT
**Elevate X AI | Feature 2: Technical Assessment & Career Intelligence Engine**
**Investigation Date:** 2026-11-15 | **Status:** ✅ RESOLVED

---

## 1. Original Symptom

```
Page: http://localhost:3002/assessment
Action: Click "Start AI/ML Engineer Assessment"
Error: HTTP 401 Unauthorized
```

All 9 technical career roles loaded correctly, role selection and skill display worked, but clicking "Start Assessment" always returned 401.

---

## 2. Investigation Path

### Step 1 — Backend Logs
```
WARNING | elevate_x:http_exception_handler:78 - HTTP 401 at /api/v1/assessments/technical/start: Not authenticated
```

### Step 2 — Token Inspection
Checked what token was actually being sent in the `Authorization` header by logging `localStorage.getItem("elevate_auth_token")`:

```
"demo-token-1731659421234"
```

This is not a JWT. It was written by `AuthContext.login()` as `"demo-token-" + Date.now()`.

### Step 3 — Backend JWT Decoder
FastAPI's `get_current_active_user` dependency calls `decode_jwt()` which uses `python-jose` to verify the token. `"demo-token-1731659421234"` fails `JWTError` immediately — backend returns 401 correctly.

### Step 4 — Source of Fake Token
`AuthContext.login()` (line 44 original): `localStorage.setItem("elevate_auth_token", "demo-token-" + Date.now())`

This was always called because `src/app/login/page.tsx` called `login(email, selectedRole)` without passing the token returned by the API.

### Step 5 — Silent Fallback Compounding Issue
`src/services/api-service.ts` `login()` and `register()` both passed `fallbackData` to `apiClient()`. When the backend was down (PostgreSQL not running), `apiClient()` swallowed the network error and returned `{access_token: "demo-jwt-token-elevate-x"}`. This fake token was then stored, making auth appear to succeed while backend was broken.

### Step 6 — Database Root Cause
`backend/.env` DATABASE_URL = `postgresql+psycopg://...@localhost:5432/...` but no PostgreSQL process runs on this machine. Every DB operation (including token verification lookup) threw a connection error.

---

## 3. Compounding Root Cause Chain

```
PostgreSQL not running
      ↓
backend /auth/login throws 500
      ↓
api-service.ts fallbackData catches error
      ↓
returns {access_token: "demo-jwt-token-elevate-x"}
      ↓
login/page.tsx passes this to AuthContext.login()
BUT AuthContext.login() ignores the token argument
      ↓
writes "demo-token-{timestamp}" to localStorage
      ↓
assessment page sends "demo-token-{timestamp}" as Bearer
      ↓
backend JWT decoder: JWTError → 401 Unauthorized
```

---

## 4. Fixes Applied

### Fix 1: DATABASE_URL → SQLite
```diff
- DATABASE_URL=postgresql+psycopg://postgres:postgres_password@localhost:5432/elevate_x_ai
+ DATABASE_URL=sqlite:///./elevate_x_local.db
```

### Fix 2: SQLite connect args
```python
# backend/app/core/database.py
if "sqlite" in db_url:
    engine_kwargs.update({"connect_args": {"check_same_thread": False}})
```

### Fix 3: AuthContext accepts real token
```diff
- const login = (email: string, role: "user" | "admin" = "user") => {
-   localStorage.setItem("elevate_auth_token", "demo-token-" + Date.now());
+ const login = (email: string, role: "user" | "admin" = "user", token?: string) => {
+   if (token) { localStorage.setItem("elevate_auth_token", token); }
```

### Fix 4: Removed fallback from login/register
```diff
  async login(email: string, password: string) {
    return apiClient<...>("/auth/login", { method: "POST", body: ... });
-   // removed fallbackData: { token: { access_token: "demo-jwt-token-elevate-x" } }
  }
```

### Fix 5: login/page.tsx passes real token
```diff
  const res = await apiService.login(email, password);
  const token = res?.data?.token?.access_token;
  if (token) { localStorage.setItem("elevate_auth_token", token); }
  login(email, selectedRole, token);
```

---

## 5. Verification After Fix

| Test | Before Fix | After Fix |
|---|---|---|
| Wrong password → 401 | Silently succeeded (fake token) | ✅ 401 returned, error shown |
| Correct login → real JWT | Fake token stored | ✅ Real JWT stored |
| Start Assessment with real JWT | 401 | ✅ 200 with questions |
| Unauthenticated request | Reached backend (fake token passed) | ✅ 401 at backend |

---

## 6. Status

**401 ROOT CAUSE: ✅ FULLY RESOLVED**

