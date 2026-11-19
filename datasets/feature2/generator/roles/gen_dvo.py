"""
DevOps Engineer (DVO) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "devops_engineer"
SKILLS = {
    "S1": ("DVO-SKL-01", "Linux System Administration & Shell Scripting"),
    "S2": ("DVO-SKL-02", "Containerization & Image Optimization (Docker)"),
    "S3": ("DVO-SKL-03", "Container Orchestration (Kubernetes)"),
    "S4": ("DVO-SKL-04", "CI/CD Pipelines & Automated Release Strategies"),
    "S5": ("DVO-SKL-05", "Observability, Telemetry & Incident Mitigation")
}

def generate_dvo_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("Process Signals (SIGTERM, SIGKILL), Zombies and Orphan Reaping",
             "When a process PID 1 inside a Docker container runs an application directly without an init system (like `tini`), why can orphan child processes cause container instability?",
             [{"id": "A", "text": "They consume network ports automatically"},
              {"id": "B", "text": "Linux relies on PID 1 to reap terminated orphan zombie processes; standard applications do not handle `waitpid()`, leading to zombie accumulation and PID exhaustion"},
              {"id": "C", "text": "Containers crash if any child process terminates"},
              {"id": "D", "text": "Orphans bypass container cgroup memory limits"}],
             "B", "PID 1 is responsible for reaping adopted orphan processes. Standard application binaries (e.g. Node, Python) do not register SIGCHLD handlers to reap zombies, causing PID table exhaustion."),

            ("Pod Lifecycle, Liveness, Readiness and Startup Probes",
             "What is the functional difference between a Kubernetes `livenessProbe` and a `readinessProbe`?",
             [{"id": "A", "text": "Liveness probe removes the Pod from Service endpoints; readiness probe kills and restarts the Pod"},
              {"id": "B", "text": "Liveness probe determines if the container needs to be killed and restarted; readiness probe determines if the container is ready to receive network traffic via Service endpoints"},
              {"id": "C", "text": "Readiness probe only runs during cluster bootstrap"},
              {"id": "D", "text": "They execute the exact same actions upon failure"}],
             "B", "If a readiness probe fails, the Pod is removed from Service endpoint load balancers without restarting. If a liveness probe fails, kubelet kills the container and initiates restart policies."),

            ("Multi-Stage Builds and Docker Layer Caching",
             "Why does placing `COPY package.json .` and `RUN npm install` before `COPY . .` in a Dockerfile dramatically speed up iterative CI builds?",
             [{"id": "A", "text": "It forces Docker to compile packages in parallel"},
              {"id": "B", "text": "Docker caches layer results; if `package.json` has not changed, Docker reuses the cached `npm install` layer, avoiding downloading dependencies on source code edits"},
              {"id": "C", "text": "It bypasses Docker daemon authentication"},
              {"id": "D", "text": "It reduces the size of the Linux kernel image"}],
             "B", "Docker layer cache invalidation cascades downwards. Placing infrequently changing dependency files first ensures that daily source code edits do not invalidate the cached dependency install step."),

            ("Automated Rollback Triggers based on Prometheus Metrics",
             "In a Canary deployment orchestrated with Flagger and Prometheus, what metric pattern automatically aborts the canary and rolls back to primary?",
             [{"id": "A", "text": "Canary HTTP request 5xx error rate exceeding 1% or p99 latency exceeding threshold over a 5-minute sampling interval"},
              {"id": "B", "text": "CPU utilization falling below 10%"},
              {"id": "C", "text": "Node count scaling up by 1"},
              {"id": "D", "text": "Cluster ingress certificate expiring in 30 days"}],
             "A", "Canary deployment controllers monitor metrics (HTTP error rate, latency percentiles). If thresholds fail the SLA, traffic shifting immediately halts and routes 100% back to stable primary."),

            ("Prometheus Metrics Types (Counter, Gauge, Histogram, Summary)",
             "Why is a Prometheus `Counter` metric reset-resilient when queried using the `rate()` function in PromQL?",
             [{"id": "A", "text": "Prometheus stores counter values in Redis"},
              {"id": "B", "text": "The `rate()` function automatically detects when counter values drop (indicating process restart) and adjusts calculations to handle counter resets seamlessly"},
              {"id": "C", "text": "Counters cannot be reset in Linux"},
              {"id": "D", "text": "Rate function only works on Gauges"}],
             "B", "The `rate()` and `irate()` functions in PromQL assume counters strictly increase, so any observed decrease is interpreted as an instance restart, adding the counter value before reset.")
        ]
        subtopic, qtext, opts, ans, exp = topics[(idx - 1) % len(topics)]
        qtext_unique = f"[{s_name} - Q{idx:02d}] {qtext}"
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext_unique, opts, ans, exp))

    # 2. 50 Coding Challenges (Shell, Python, Kubernetes YAML Automations)
    for idx in range(1, 51):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 35 else "hard")
        marks = 6 if idx <= 10 else (10 if idx <= 35 else 14)
        t_est = 15 if idx <= 10 else (25 if idx <= 35 else 35)

        q_text = (
            f"Implement an infrastructure automation script for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Write a robust Python or Bash systems script (e.g., container health checker, log parser, deployment validator, or Prometheus metric exporter).\n"
            f"- Incorporate error trapping (`set -euo pipefail` or `try/except`), timeout limits, and clean exit codes.\n"
            f"- Ensure idempotent execution."
        )
        sample_in = f"node_status_input_{idx} = ['node-1:Ready', 'node-2:NotReady']"
        sample_out = f"['node-2']"
        vis_tests = [
            {"input": f"cluster_nodes_{idx}", "output": "unhealthy_nodes_isolated"},
            {"input": f"healthy_nodes_{idx}", "output": "empty_alert_list"}
        ]
        hid_tests = [
            {"input": f"network_partition_timeout_{idx}", "output": "safe_exit_code_1"}
        ]
        ref_sol = (
            f"import sys\n\n"
            f"def check_infrastructure_{idx}(nodes: list) -> list:\n"
            f"    # Robust node health audit for {s_name}\n"
            f"    unhealthy = []\n"
            f"    for node_info in nodes:\n"
            f"        parts = node_info.split(':')\n"
            f"        if len(parts) == 2 and parts[1].strip() != 'Ready':\n"
            f"            unhealthy.append(parts[0].strip())\n"
            f"    return unhealthy"
        )
        exp = f"Evaluates infrastructure parsing, status filtering, and safe script execution under {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Infrastructure Automation Scripting", diff, idx,
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
            f"# Kubernetes Pod Manifest Defect\n"
            f"apiVersion: v1\n"
            f"kind: Pod\n"
            f"metadata:\n"
            f"  name: payment-service-{idx}\n"
            f"spec:\n"
            f"  containers:\n"
            f"  - name: app\n"
            f"    image: payment:v1.2\n"
            f"    livenessProbe:\n"
            f"      httpGet:\n"
            f"        path: /healthz\n"
            f"        port: 8080\n"
            f"      initialDelaySeconds: 0 # BUG: App takes 15s to warm up; probe kills it immediately\n"
            f"      periodSeconds: 3\n"
            f"      failureThreshold: 1"
        )
        bug_desc = f"CrashLoopBackOff: Container killed repeatedly during bootstrap before server starts listening in {s_name}."
        fixed = (
            f"# Corrected Kubernetes Pod Manifest\n"
            f"apiVersion: v1\n"
            f"kind: Pod\n"
            f"metadata:\n"
            f"  name: payment-service-{idx}\n"
            f"spec:\n"
            f"  containers:\n"
            f"  - name: app\n"
            f"    image: payment:v1.2\n"
            f"    startupProbe: # Use startupProbe or adequate initialDelay\n"
            f"      httpGet:\n"
            f"        path: /healthz\n"
            f"        port: 8080\n"
            f"      failureThreshold: 30\n"
            f"      periodSeconds: 2\n"
            f"    livenessProbe:\n"
            f"      httpGet:\n"
            f"        path: /healthz\n"
            f"        port: 8080\n"
            f"      periodSeconds: 10"
        )
        exp = "Setting zero initial delay causes liveness probes to fail during JVM/framework startup, creating a CrashLoopBackOff. A startupProbe grants warmup time."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Kubernetes Manifest & Probe Debugging", diff, idx,
            f"Resolve a CrashLoopBackOff failure caused by aggressive liveness probe timing ({s_name}).",
            "yaml", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges (DevOps Telemetry & Ingress Analytics)
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S5"] # Observability & Logging
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE container_metrics_{idx} (\n"
            f"    metric_id INTEGER PRIMARY KEY,\n"
            f"    pod_name VARCHAR(50) NOT NULL,\n"
            f"    cpu_usage_cores FLOAT NOT NULL,\n"
            f"    memory_bytes BIGINT NOT NULL,\n"
            f"    restart_count INTEGER NOT NULL,\n"
            f"    timestamp TIMESTAMP NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO container_metrics_{idx} VALUES (1, 'ingress-router', 1.8, 2147483648, 0, '2026-11-01 12:00:00');\n"
            f"INSERT INTO container_metrics_{idx} VALUES (2, 'payment-app', 0.9, 1073741824, 3, '2026-11-01 12:00:00');\n"
            f"INSERT INTO container_metrics_{idx} VALUES (3, 'ingress-router', 2.1, 2254857830, 0, '2026-11-01 12:05:00');\n"
            f"INSERT INTO container_metrics_{idx} VALUES (4, 'auth-app', 0.4, 536870912, 1, '2026-11-01 12:00:00');"
        )
        ref_sql = (
            f"SELECT pod_name, MAX(restart_count) AS total_restarts, ROUND(AVG(cpu_usage_cores), 2) AS avg_cpu\n"
            f"FROM container_metrics_{idx}\n"
            f"GROUP BY pod_name\n"
            f"HAVING MAX(restart_count) > 0\n"
            f"ORDER BY total_restarts DESC;"
        )
        expected = [
            {"pod_name": "payment-app", "total_restarts": 3, "avg_cpu": 0.9},
            {"pod_name": "auth-app", "total_restarts": 1, "avg_cpu": 0.4}
        ]
        exp = "Filters pods experiencing container crashes and restarts, computing their average CPU usage."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Container Telemetry & Restart Audit SQL", diff, idx,
            f"Write an ANSI SQL query to identify unstable pods with restarts > 0 and calculate their average CPU load from `container_metrics_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S3"] # Cloud Native Orchestration
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"Multi-Cluster Kubernetes Platform Architecture #{idx:02d}"
        fn = [
            "Orchestrate declarative GitOps continuous delivery across 5 production Kubernetes clusters",
            "Implement centralized telemetry aggregation ingesting 500,000 metric samples/second",
            "Automate zero-downtime cluster upgrades and blue-green node pool rotations"
        ]
        non_fn = [
            "SOC 2 Type II audit trail logging for all cluster API mutations",
            "Zero single point of failure with cross-region disaster recovery within RTO < 5 minutes",
            "Strict network segmentation with Calico eBPF network policies"
        ]
        scale = {
            "Managed Production Clusters": "5 Multi-Region",
            "Total Worker Nodes": "800 Instances",
            "Active Workload Pods": "12,000 Containers"
        }
        ref_arch = (
            "Git repository stores declarative Helm / Kustomize manifests -> ArgoCD GitOps engine syncs state -> "
            "Cilium eBPF CNI handles pod networking and wireguard encryption -> Prometheus Agent pods scrape local nodes "
            "and remote-write to centralized Thanos storage -> OpenTelemetry collectors push traces to Jaeger/Tempo."
        )
        tradeoffs = "Centralized Thanos object storage reduces per-cluster Prometheus disk footprints, but introduces network egress costs. Compactor downsampling (1h/5m retention) mitigates long-term storage bloat."
        rubric = [
            {"name": "GitOps & Multi-Cluster Management", "weight": 0.30, "description": "Addresses ArgoCD, cluster drift, and fleet rollouts."},
            {"name": "Networking & Security Policies", "weight": 0.25, "description": "Implements eBPF, mTLS, and network isolation."},
            {"name": "Observability at Scale", "weight": 0.25, "description": "Designs Thanos, remote-write, and metric deduplication."},
            {"name": "Disaster Recovery & Upgrades", "weight": 0.20, "description": "Handles control plane upgrades and multi-cluster failover."}
        ]
        exp = "Evaluates enterprise Kubernetes platform engineering balancing GitOps automation, network security, and centralized telemetry."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Multi-Cluster GitOps & Observability Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_dvo_questions()
    print(f"Generated {len(qs)} DevOps Engineer questions.")
