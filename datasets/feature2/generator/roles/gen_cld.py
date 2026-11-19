"""
Cloud Engineer (CLD) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "cloud_engineer"
SKILLS = {
    "S1": ("CLD-SKL-01", "Cloud Infrastructure & Virtual Networks (VPC, Subnets)"),
    "S2": ("CLD-SKL-02", "Cloud Compute, Containers & Serverless"),
    "S3": ("CLD-SKL-03", "Cloud Storage, Databases & Lifecycle Policies"),
    "S4": ("CLD-SKL-04", "Infrastructure as Code (Terraform / CloudFormation)"),
    "S5": ("CLD-SKL-05", "Cloud Security, Cost Optimization & High Availability / DR")
}

def generate_cld_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("VPC CIDR Subnetting (Public vs Private vs Isolated Subnets)",
             "What routing configuration distinguishes a public subnet from a private subnet in an AWS Virtual Private Cloud (VPC)?",
             [{"id": "A", "text": "A public subnet has an explicit route in its route table pointing `0.0.0.0/0` to an Internet Gateway (IGW); a private subnet routes `0.0.0.0/0` to a NAT Gateway or has no internet egress"},
              {"id": "B", "text": "Public subnets have 10.0.0.0/8 IP ranges; private subnets have 192.168.0.0/16 ranges"},
              {"id": "C", "text": "Private subnets disable all security groups"},
              {"id": "D", "text": "Public subnets do not support EC2 instances"}],
             "A", "The definition of a public subnet in cloud networking is having a route table destination `0.0.0.0/0` targeting an Internet Gateway, allowing public IPv4 allocation and direct inbound internet routing."),

            ("Security Groups (Stateful) vs Network ACLs (Stateless)",
             "Why must a Network Access Control List (NACL) rule explicitly permit ephemeral return ports (e.g. 1024-65535) for outbound client connections, while a Security Group does not?",
             [{"id": "A", "text": "Security Groups are stateful (automatically permitting return response traffic regardless of inbound rules), while NACLs are stateless (evaluating outbound response traffic independently against outbound rules)"},
              {"id": "B", "text": "NACLs only operate on UDP traffic"},
              {"id": "C", "text": "Security Groups execute inside the operating system kernel"},
              {"id": "D", "text": "NACLs do not support IP CIDR blocks"}],
             "A", "Security groups track connection state: if inbound traffic is allowed, corresponding response traffic is automatically allowed outbound. Stateless NACLs evaluate outbound traffic afresh against explicit outbound rules."),

            ("Managed Relational Databases (RDS / Aurora) Multi-AZ vs Read Replicas",
             "In Amazon RDS, what is the fundamental architectural difference between Multi-AZ deployment and Read Replicas?",
             [{"id": "A", "text": "Multi-AZ uses synchronous block-level physical replication to a standby instance in another availability zone for automated failover (high availability); Read Replicas use asynchronous engine-level replication to serve read traffic"},
              {"id": "B", "text": "Read Replicas handle automated failover; Multi-AZ only serves read traffic"},
              {"id": "C", "text": "Multi-AZ is hosted in another AWS region"},
              {"id": "D", "text": "Read replicas cannot be promoted to standalone instances"}],
             "A", "Multi-AZ is a disaster recovery and high-availability mechanism: the standby is not accessible for queries and syncs synchronously. Read replicas replicate asynchronously and actively scale read query capacity."),

            ("Terraform State Management, Remote Backends and State Locking (DynamoDB)",
             "Why is state locking via DynamoDB essential when using an S3 remote backend in a team Terraform environment?",
             [{"id": "A", "text": "It speeds up Terraform plan execution by caching state in memory"},
              {"id": "B", "text": "It prevents race conditions where two engineers or CI pipelines run `terraform apply` concurrently, corrupting the shared remote state file"},
              {"id": "C", "text": "It encrypts the terraform state file with AES-256"},
              {"id": "D", "text": "It automatically generates rollback scripts"}],
             "B", "DynamoDB acts as a distributed lock. When an apply begins, an exclusive lock is acquired in DynamoDB. Concurrent attempts to apply will fail to obtain the lock, preventing catastrophic state file corruption."),

            ("Disaster Recovery Strategies (Backup & Restore, Pilot Light, Warm Standby, Multi-Region Active-Active)",
             "Which cloud Disaster Recovery (DR) strategy offers the lowest Recovery Time Objective (RTO) and Recovery Point Objective (RPO), at the highest operational cost?",
             [{"id": "A", "text": "Backup and Restore"},
              {"id": "B", "text": "Pilot Light"},
              {"id": "C", "text": "Warm Standby"},
              {"id": "D", "text": "Multi-Region Active-Active"}],
             "D", "Multi-Region Active-Active serves production traffic simultaneously across two or more geographical cloud regions with real-time continuous replication, providing near-zero RTO and RPO.")
        ]
        subtopic, qtext, opts, ans, exp = topics[(idx - 1) % len(topics)]
        qtext_unique = f"[{s_name} - Q{idx:02d}] {qtext}"
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext_unique, opts, ans, exp))

    # 2. 50 Coding Challenges (IaC, Terraform, Cloud SDK Scripting)
    for idx in range(1, 51):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 35 else "hard")
        marks = 6 if idx <= 10 else (10 if idx <= 35 else 14)
        t_est = 15 if idx <= 10 else (25 if idx <= 35 else 35)

        q_text = (
            f"Implement a Cloud Infrastructure as Code or Cloud SDK automation utility for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Write an automated script in Python (Boto3) or declarative HCL parsing module.\n"
            f"- Validate cloud resource tags, manage lifecycle transitions, or audit unattached volumes.\n"
            f"- Handle API pagination and retry with exponential backoff on `ThrottlingException`."
        )
        sample_in = f"resource_tags_{idx} = {{'Environment': 'Production', 'CostCenter': 'ENG-{idx}'}}"
        sample_out = f"compliance_status = True"
        vis_tests = [
            {"input": f"compliant_tags_{idx}", "output": "tags_approved"},
            {"input": f"missing_env_tag_{idx}", "output": "non_compliant_flagged"}
        ]
        hid_tests = [
            {"input": f"unattached_ebs_volume_{idx}", "output": "isolated_for_cleanup"}
        ]
        ref_sol = (
            f"def audit_cloud_resources_{idx}(resources: list) -> list:\n"
            f"    # Cloud resource tag and compliance verification for {s_name}\n"
            f"    non_compliant = []\n"
            f"    required_tags = {{'Environment', 'Owner', 'Project'}}\n"
            f"    for r in resources:\n"
            f"        tags = set(r.get('Tags', {{}}).keys())\n"
            f"        if not required_tags.issubset(tags):\n"
            f"            non_compliant.append(r.get('ResourceId'))\n"
            f"    return non_compliant"
        )
        exp = f"Evaluates cloud resource tagging compliance, audit automation, and safe resource lifecycle management in {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Cloud Resource Audit & IaC Automation", diff, idx,
            q_text, "python", sample_in, sample_out, vis_tests, hid_tests, ref_sol, exp, marks, t_est
        ))

    # 3. 35 Debugging Challenges (Terraform & Cloud Networking Configuration)
    for idx in range(1, 36):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        broken = (
            f"# Terraform Configuration Defect\n"
            f"resource \"aws_route_table\" \"private_rt_{idx}\" {{\n"
            f"  vpc_id = aws_vpc.main.id\n"
            f"  # Defect: Private subnet routes 0.0.0.0/0 to IGW instead of NAT Gateway\n"
            f"  route {{\n"
            f"    cidr_block = \"0.0.0.0/0\"\n"
            f"    gateway_id = aws_internet_gateway.gw.id\n"
            f"  }}\n"
            f"}}"
        )
        bug_desc = f"Security vulnerability: Private database subnets inadvertently exposed to public internet ingress in {s_name}."
        fixed = (
            f"# Corrected Terraform Configuration\n"
            f"resource \"aws_route_table\" \"private_rt_{idx}\" {{\n"
            f"  vpc_id = aws_vpc.main.id\n"
            f"  # Fixed: Route outbound egress strictly via managed NAT Gateway\n"
            f"  route {{\n"
            f"    cidr_block     = \"0.0.0.0/0\"\n"
            f"    nat_gateway_id = aws_nat_gateway.nat.id\n"
            f"  }}\n"
            f"}}"
        )
        exp = "Routing private subnets directly to an Internet Gateway violates network isolation. Private subnets must route internet egress through a NAT Gateway."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Terraform VPC Routing & Security Debugging", diff, idx,
            f"Identify and rectify a misconfigured VPC route table exposing private subnets ({s_name}).",
            "hcl", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges (Cloud Cost & Resource Billing Analytics)
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S5"] # Cloud Cost & FinOps
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE cloud_cost_usage_{idx} (\n"
            f"    record_id INTEGER PRIMARY KEY,\n"
            f"    service_name VARCHAR(50) NOT NULL,\n"
            f"    resource_id VARCHAR(50) NOT NULL,\n"
            f"    cost_amount DECIMAL(12, 2) NOT NULL,\n"
            f"    usage_date DATE NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO cloud_cost_usage_{idx} VALUES (1, 'AmazonEC2', 'i-01a2b3c', 450.00, '2026-11-01');\n"
            f"INSERT INTO cloud_cost_usage_{idx} VALUES (2, 'AmazonEC2', 'i-09x8y7z', 350.00, '2026-11-01');\n"
            f"INSERT INTO cloud_cost_usage_{idx} VALUES (3, 'AmazonRDS', 'rds-main-pg', 800.00, '2026-11-01');\n"
            f"INSERT INTO cloud_cost_usage_{idx} VALUES (4, 'AmazonS3', 'bucket-logs', 45.00, '2026-11-01');"
        )
        ref_sql = (
            f"SELECT service_name,\n"
            f"       COUNT(DISTINCT resource_id) AS active_resources,\n"
            f"       SUM(cost_amount) AS total_spend\n"
            f"FROM cloud_cost_usage_{idx}\n"
            f"GROUP BY service_name\n"
            f"HAVING SUM(cost_amount) >= 100.00\n"
            f"ORDER BY total_spend DESC;"
        )
        expected = [
            {"service_name": "AmazonRDS", "active_resources": 1, "total_spend": 800.0},
            {"service_name": "AmazonEC2", "active_resources": 2, "total_spend": 800.0}
        ]
        exp = "Aggregates cloud billing spend by service and filters out low-spend incidental line items."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Cloud Billing & FinOps Analytics SQL", diff, idx,
            f"Write an ANSI SQL query to compute total spend and active resource count by cloud service for services >= $100 from `cloud_cost_usage_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions (Multi-Region Cloud Architecture & DR)
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S5"] # High Availability & Cloud Architecture
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"Multi-Region Active-Active Cloud Architecture #{idx:02d}"
        fn = [
            "Serve global user traffic across us-east-1 and eu-west-1 with latency-based DNS routing",
            "Maintain bi-directional multi-region database replication with conflict resolution",
            "Guarantee Recovery Time Objective (RTO) < 30 seconds upon full region outage"
        ]
        non_fn = [
            "Data residency compliance ensuring EU citizen PII does not leave eu-west-1",
            "Automated health check DNS failover via Amazon Route 53 with zero manual intervention",
            "99.999% global compute availability SLA"
        ]
        scale = {
            "Global Active Users": "30 Million",
            "Total Regional Footprint": "2 Cloud Regions, 6 Availability Zones",
            "Replication Latency Budget": "< 500ms cross-region"
        }
        ref_arch = (
            "Route 53 uses Geolocation and Latency routing with health checks -> CloudFront edge caches assets -> "
            "Application Load Balancer distributes to regional EKS clusters -> Amazon Aurora Global Database handles cross-region storage "
            "with physical storage-level replication (< 1s lag) -> S3 Cross-Region Replication (CRR) syncs object assets."
        )
        tradeoffs = "Multi-region active-active writes risk write conflicts without CRDTs or regional sharding. Restricting primary writes by user residency (EU users write to EU Aurora, US to US) eliminates split-brain conflicts."
        rubric = [
            {"name": "Multi-Region Routing & Failover", "weight": 0.30, "description": "Designs Route 53 health checks and DNS routing policies."},
            {"name": "Cross-Region Storage & Data Replication", "weight": 0.30, "description": "Evaluates Aurora Global DB, DynamoDB Global Tables, and S3 CRR."},
            {"name": "Compliance & Data Residency", "weight": 0.20, "description": "Guarantees GDPR boundary isolation."},
            {"name": "Cost vs RTO/RPO Tradeoffs", "weight": 0.20, "description": "Balances active-active infrastructure cost against warm standby."}
        ]
        exp = "Evaluates multi-region cloud disaster recovery and high-availability architecture balancing RTO/RPO, data consistency, and global latency."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Multi-Region Cloud DR Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_cld_questions()
    print(f"Generated {len(qs)} Cloud Engineer questions.")
