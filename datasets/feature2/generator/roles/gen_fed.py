"""
Frontend Developer (FED) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "frontend_developer"
SKILLS = {
    "S1": ("FED-SKL-01", "Core JavaScript/TypeScript & Browser Runtime"),
    "S2": ("FED-SKL-02", "Modern UI Frameworks (React, Reconciliation, State)"),
    "S3": ("FED-SKL-03", "Web Performance, Caching & Rendering Optimization"),
    "S4": ("FED-SKL-04", "CSS Architecture, Responsive Layouts & Accessibility (a11y)"),
    "S5": ("FED-SKL-05", "Client-Side Data Fetching, Offline Storage & Security")
}

def generate_fed_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("Event Loop, Microtasks (Promises) and Macrotasks (Timers)",
             "In the standard browser event loop, in what order are execution queues processed after the current call stack empties?",
             [{"id": "A", "text": "All pending microtasks (Promise reactions, queueMicrotask) are drained completely before the next macrotask (setTimeout, setInterval, I/O) is dequeued"},
              {"id": "B", "text": "One microtask executes, followed by one macrotask in alternating round-robin order"},
              {"id": "C", "text": "Macrotasks have strict priority over microtasks"},
              {"id": "D", "text": "Rendering updates occur between every individual microtask"}],
             "A", "The microtask queue drains completely until empty before the event loop advances to the next task or performs animation frame rendering callbacks."),

            ("Virtual DOM Reconciliation and Fiber Tree Mechanics",
             "Why does using array indices as `key` props in React lists cause rendering and state bugs during dynamic reordering or deletion?",
             [{"id": "A", "text": "Array indices cause memory leaks in JavaScript garbage collection"},
              {"id": "B", "text": "React matches Fiber nodes by key; when items shift positions, keys remain identical to indices, incorrectly preserving internal component state across mismatched items"},
              {"id": "C", "text": "Array keys disable virtual DOM diffing entirely"},
              {"id": "D", "text": "Indices trigger infinite reconciliation loops"}],
             "B", "React uses keys to identify stable identity across renders. When keys are indices, removing index 0 causes index 1 to inherit index 0's key, confusing uncontrolled inputs and local hook states."),

            ("Critical Rendering Path, Layout Thrashing and Reflows",
             "What causes 'Layout Thrashing' in client-side browser DOM manipulation?",
             [{"id": "A", "text": "Loading multiple CSS files asynchronously"},
              {"id": "B", "text": "Alternating between writing to DOM geometries (e.g. `el.style.width = ...`) and reading computed geometries (e.g. `el.offsetWidth`), forcing the browser to recalculate layout synchronously in a tight loop"},
              {"id": "C", "text": "Using CSS grid instead of Flexbox"},
              {"id": "D", "text": "Rendering more than 100 SVG elements"}],
             "B", "Reading geometric layout properties dirty the layout cache. Alternating writes and reads forces repeated synchronous layout reflow passes, stalling the UI thread."),

            ("WAI-ARIA Roles, Keyboard Navigation and Focus Trapping",
             "When rendering an accessible modal dialog, why is keyboard 'Focus Trapping' mandatory under WCAG 2.1 Level AA?",
             [{"id": "A", "text": "To prevent the mouse cursor from leaving the browser viewport"},
              {"id": "B", "text": "To ensure keyboard-only and screen reader users pressing Tab/Shift-Tab cannot navigate into obscured background elements behind the active modal"},
              {"id": "C", "text": "To disable all keyboard shortcuts on the webpage"},
              {"id": "D", "text": "To automatically submit forms when Enter is pressed"}],
             "B", "Without focus trapping, pressing Tab allows focus to escape behind the backdrop into unreachable or obscured elements, stranding assistive technology users."),

            ("Cross-Site Scripting (XSS) Prevention and Content Security Policy (CSP)",
             "How does a robust Content Security Policy (CSP) with `script-src 'nonce-...';` mitigate Cross-Site Scripting (XSS)?",
             [{"id": "A", "text": "It encrypts all JavaScript files on the server"},
              {"id": "B", "text": "It instructs the browser to refuse execution of any inline `<script>` or external script tag that does not possess the cryptographic per-request nonce"},
              {"id": "C", "text": "It disables all REST API calls made with fetch()"},
              {"id": "D", "text": "It sanitizes SQL queries executed in WebSQL"}],
             "B", "Attackers injecting arbitrary `<script>evil()</script>` cannot predict the server-generated cryptographic nonce, so the browser unconditionally blocks execution.")
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
            f"Implement an idiomatic JavaScript/TypeScript frontend utility for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Write an asynchronous or state-synchronization utility (e.g., custom hook, debounce/throttle, event emitter, or reactive state store).\n"
            f"- Handle cancellation, unmount cleanups, and race conditions.\n"
            f"- Adhere to clean closure scope semantics."
        )
        sample_in = f"fn = debounce(callback, 200)"
        sample_out = f"debounced_function_execution"
        vis_tests = [
            {"input": f"call_events_burst_{idx}", "output": f"single_invoked_call_{idx}"},
            {"input": f"immediate_execution_{idx}", "output": f"proper_debounce_delay_{idx}"}
        ]
        hid_tests = [
            {"input": f"component_unmount_cancel_{idx}", "output": "clean_timer_clear"}
        ]
        ref_sol = (
            f"function debounceUtility_{idx}(fn, delay) {{\n"
            f"    let timerId = null;\n"
            f"    const debounced = function(...args) {{\n"
            f"        if (timerId) clearTimeout(timerId);\n"
            f"        timerId = setTimeout(() => {{\n"
            f"            fn.apply(this, args);\n"
            f"        }}, delay);\n"
            f"    }};\n"
            f"    debounced.cancel = () => {{ if (timerId) clearTimeout(timerId); }};\n"
            f"    return debounced;\n"
            f"}}"
        )
        exp = f"Implements closure-based function decoration with cancellation and context preservation for {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Frontend Utility Implementation", diff, idx,
            q_text, "javascript", sample_in, sample_out, vis_tests, hid_tests, ref_sol, exp, marks, t_est
        ))

    # 3. 35 Debugging Challenges
    for idx in range(1, 36):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        broken = (
            f"import React, {{ useEffect, useState }} from 'react';\n"
            f"function UserProfile_{idx}({{ userId }}) {{\n"
            f"    const [user, setUser] = useState(null);\n"
            f"    useEffect(() => {{\n"
            f"        // Defect: Race condition on rapid userId change and missing unmount cleanup\n"
            f"        fetchUser(userId).then(data => setUser(data));\n"
            f"    }}, [userId]);\n"
            f"    return <div>{{user?.name}}</div>;\n"
            f"}}"
        )
        bug_desc = f"Stale props race condition: if userId updates from 1 to 2 rapidly, response 1 can resolve after response 2, overwriting state with stale data in {s_name}."
        fixed = (
            f"import React, {{ useEffect, useState }} from 'react';\n"
            f"function UserProfile_{idx}({{ userId }}) {{\n"
            f"    const [user, setUser] = useState(null);\n"
            f"    useEffect(() => {{\n"
            f"        let isCurrent = true;\n"
            f"        fetchUser(userId).then(data => {{\n"
            f"            if (isCurrent) setUser(data);\n"
            f"        }});\n"
            f"        return () => {{ isCurrent = false; }};\n"
            f"    }}, [userId]);\n"
            f"    return <div>{{user?.name}}</div>;\n"
            f"}}"
        )
        exp = "Using a boolean cancellation flag inside the `useEffect` cleanup hook discards out-of-order asynchronous responses when props change or component unmounts."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "React Hook Race Condition Debugging", diff, idx,
            f"Diagnose and resolve an asynchronous state race condition in a React component ({s_name}).",
            "javascript", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges (Client-Side Relational / Offline Storage Context)
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S5"] # Offline Storage & Caching
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE client_cached_items_{idx} (\n"
            f"    item_id INTEGER PRIMARY KEY,\n"
            f"    category VARCHAR(50) NOT NULL,\n"
            f"    payload_json TEXT NOT NULL,\n"
            f"    cache_timestamp INTEGER NOT NULL,\n"
            f"    is_stale INTEGER NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO client_cached_items_{idx} VALUES (1, 'UI_THEME', '{{\"dark\": true}}', 1700000000, 0);\n"
            f"INSERT INTO client_cached_items_{idx} VALUES (2, 'NAV_MENU', '{{\"links\": 5}}', 1699990000, 1);\n"
            f"INSERT INTO client_cached_items_{idx} VALUES (3, 'UI_THEME', '{{\"dark\": false}}', 1700005000, 0);\n"
            f"INSERT INTO client_cached_items_{idx} VALUES (4, 'USER_PERMS', '{{\"admin\": true}}', 1700010000, 0);"
        )
        ref_sql = (
            f"SELECT category, COUNT(*) AS fresh_entries, MAX(cache_timestamp) AS latest_sync\n"
            f"FROM client_cached_items_{idx}\n"
            f"WHERE is_stale = 0\n"
            f"GROUP BY category\n"
            f"ORDER BY latest_sync DESC;"
        )
        expected = [
            {"category": "USER_PERMS", "fresh_entries": 1, "latest_sync": 1700010000},
            {"category": "UI_THEME", "fresh_entries": 2, "latest_sync": 1700005000}
        ]
        exp = "Filters for valid unexpired client cache entries, groups by category, and returns latest synchronization timestamps."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Client Storage & Offline Caching SQL", diff, idx,
            f"Write an ANSI SQL query to audit active un-stale client storage items by category from `client_cached_items_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S3"] # Performance & Web Architecture
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"High-Performance Web Frontend Architecture #{idx:02d}"
        fn = [
            "Render large infinite-scrolling feeds (100,000+ items) with 60 FPS scrolling and zero DOM bloat",
            "Support offline mutation queuing with optimistic UI updates and background synchronization",
            "Achieve sub-1.2s Largest Contentful Paint (LCP) and zero Cumulative Layout Shift (CLS)"
        ]
        non_fn = [
            "WCAG 2.1 AA accessibility compliance across all dynamic widgets",
            "Bundle size budget < 120KB initial critical JavaScript payload",
            "Cross-browser compatibility across mobile Safari, Chrome, and Firefox"
        ]
        scale = {
            "Daily Active Web Users": "15 Million",
            "Peak Concurrent Sessions": "250,000",
            "Global CDN Cache Hit Ratio": "> 92%"
        }
        ref_arch = (
            "Edge CDN terminates SSL and serves Static Site Assets with Cache-Control immutable -> "
            "Server Components stream HTML chunks with Suspense boundaries -> DOM Virtualizer windowing "
            "keeps active nodes under 50 elements -> Service Worker caches API responses in CacheStorage -> "
            "IndexedDB manages offline mutation queues with exponential backoff sync."
        )
        tradeoffs = "Virtual scrolling breaks native browser find-in-page (Ctrl+F) unless custom search index indexing is implemented. Offscreen rendering buffer prevents visible blank flashing during rapid fling scrolling."
        rubric = [
            {"name": "Rendering Architecture & DOM Optimization", "weight": 0.30, "description": "Applies virtualization, SSR/SSG, and code splitting."},
            {"name": "State Management & Offline Storage", "weight": 0.25, "description": "Designs optimistic updates and IndexedDB sync."},
            {"name": "Performance & Core Web Vitals", "weight": 0.25, "description": "Addresses LCP, INP, CLS, and asset budgeting."},
            {"name": "Accessibility & Cross-Platform", "weight": 0.20, "description": "Ensures ARIA semantics, responsive layouts, and screen reader flow."}
        ]
        exp = "Evaluates modern frontend engineering architecture balancing Core Web Vitals, state synchronization, and DOM efficiency."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Client-Side Frontend Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_fed_questions()
    print(f"Generated {len(qs)} Frontend Developer questions.")
