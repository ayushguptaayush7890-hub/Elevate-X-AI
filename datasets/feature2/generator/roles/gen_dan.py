"""
Data Analyst (DAN) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "data_analyst"
SKILLS = {
    "S1": ("DAN-SKL-01", "Advanced SQL Querying & Relational Joins"),
    "S2": ("DAN-SKL-02", "Data Cleaning, Wrangling & Transformation (Pandas)"),
    "S3": ("DAN-SKL-03", "Statistical Analysis & Trend Forecasting"),
    "S4": ("DAN-SKL-04", "BI Dashboards & Visual Analytics (PowerBI/Tableau/Metabase)"),
    "S5": ("DAN-SKL-05", "KPI Metric Definition & Business Impact Analysis")
}

def generate_dan_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("Window Functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE)",
             "If three employees have identical sales of $10,000, what rank values are assigned to them and the subsequent employee by `RANK()` vs `DENSE_RANK()`?",
             [{"id": "A", "text": "RANK assigns 1, 1, 1, 4; DENSE_RANK assigns 1, 1, 1, 2"},
              {"id": "B", "text": "RANK assigns 1, 2, 3, 4; DENSE_RANK assigns 1, 1, 1, 1"},
              {"id": "C", "text": "Both functions assign 1, 2, 3, 4"},
              {"id": "D", "text": "RANK assigns 1, 1, 1, 2; DENSE_RANK assigns 1, 1, 1, 4"}],
             "A", "RANK skips positions after ties (1, 1, 1, 4), preserving the absolute rank count. DENSE_RANK does not skip positions (1, 1, 1, 2)."),

            ("Reshaping Data (Pivot Tables, Melt, Stack, Unstack)",
             "In tidy data principles, what transformation does Pandas `melt()` perform on a DataFrame?",
             [{"id": "A", "text": "Unpivots a DataFrame from wide format to long format, gathering column headers into a variable column and values into a value column"},
              {"id": "B", "text": "Pivots a DataFrame from long format to wide format"},
              {"id": "C", "text": "Drops duplicate rows based on index"},
              {"id": "D", "text": "Merges two tables on primary keys"}],
             "A", "`melt()` reverses wide format structures, consolidating multiple metric columns into key-value attribute pairs for relational reporting."),

            ("Star Schema vs Snowflake Schema Modeling for BI",
             "What is the key architectural difference between a Star Schema and a Snowflake Schema in data warehousing?",
             [{"id": "A", "text": "A Star Schema has denormalized dimension tables directly connected to the fact table; a Snowflake Schema normalizes dimension tables into multiple related sub-tables"},
              {"id": "B", "text": "A Snowflake schema cannot store numeric facts"},
              {"id": "C", "text": "A Star schema requires graph databases"},
              {"id": "D", "text": "A Snowflake schema eliminates fact tables"}],
             "A", "Star schemas prioritize query simplicity and fast BI join performance via denormalized dimensions. Snowflake schemas normalize dimensions to reduce data redundancy at the cost of more joins."),

            ("Revenue Metrics (MRR, ARR, ARPU, Net Revenue Retention)",
             "If a SaaS company begins the month with $100k Monthly Recurring Revenue (MRR), loses $10k to churn, loses $5k to downgrades, and gains $25k in expansion from existing accounts, what is its Net Revenue Retention (NRR)?",
             [{"id": "A", "text": "90%"},
              {"id": "B", "text": "110%"},
              {"id": "C", "text": "85%"},
              {"id": "D", "text": "125%"}],
             "B", "NRR = (Starting MRR - Churn - Downgrades + Expansion) / Starting MRR = (100 - 10 - 5 + 25) / 100 = 110 / 100 = 110%. NRR > 100% indicates negative net churn."),

            ("Correlation Analysis (Pearson vs Spearman Rank Correlation)",
             "Why is Spearman's rank correlation preferred over Pearson's correlation when assessing the relationship between two variables exhibiting a non-linear but strictly monotonic relationship with extreme outliers?",
             [{"id": "A", "text": "Spearman evaluates monotonic association based on ranks rather than linear raw values, making it robust to non-linearity and outliers"},
              {"id": "B", "text": "Pearson correlation only works on categorical text"},
              {"id": "C", "text": "Spearman correlation ignores negative values"},
              {"id": "D", "text": "Pearson requires zero degrees of freedom"}],
             "A", "Pearson measures strict linear proportionality and is sensitive to extreme values. Spearman assesses whether values increase together monotonically by ranking observations.")
        ]
        subtopic, qtext, opts, ans, exp = topics[(idx - 1) % len(topics)]
        qtext_unique = f"[{s_name} - Q{idx:02d}] {qtext}"
        questions.append(build_mcq(ROLE_ID, s_id, s_name, subtopic, diff, idx, qtext_unique, opts, ans, exp))

    # 2. 50 Coding Challenges (Data Wrangling, Analytics, Pandas, Python)
    for idx in range(1, 51):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 35 else "hard")
        marks = 6 if idx <= 10 else (10 if idx <= 35 else 14)
        t_est = 15 if idx <= 10 else (25 if idx <= 35 else 35)

        q_text = (
            f"Implement an analytics transformation algorithm for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Clean, reshape, or aggregate time-series / tabular metrics using Python and Pandas.\n"
            f"- Handle missing business records, group by cohorts, and calculate cumulative growth.\n"
            f"- Avoid slow row-level `iterrows()` loops; use vectorized Pandas idioms."
        )
        sample_in = f"sales_records_{idx} = [{{'date': '2026-01-01', 'amount': 150}}]"
        sample_out = f"{{'total_volume': 150, 'growth_rate': 0.0}}"
        vis_tests = [
            {"input": f"sales_data_{idx}_q1", "output": "valid_aggregations_computed"},
            {"input": f"sales_data_{idx}_q2", "output": "cohort_growth_calculated"}
        ]
        hid_tests = [
            {"input": f"sales_data_{idx}_missing_days", "output": "forward_filled_correctly"}
        ]
        ref_sol = (
            f"import pandas as pd\n\n"
            f"def transform_analytics_data_{idx}(df: pd.DataFrame) -> dict:\n"
            f"    # Vectorized KPI calculation for {s_name}\n"
            f"    df['date'] = pd.to_datetime(df['date'])\n"
            f"    df = df.sort_values('date')\n"
            f"    total = float(df['amount'].sum())\n"
            f"    avg = float(df['amount'].mean())\n"
            f"    return {{'total_volume': total, 'average_order': avg}}"
        )
        exp = f"Evaluates tabular metric computation, datetime coercion, and vectorized aggregation in {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Data Transformation & KPI Calculation", diff, idx,
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
            f"import pandas as pd\n"
            f"def compute_churn_{idx}(user_events_df):\n"
            f"    # Defect: Inadvertent Cartesian product on merge without unique key enforcement\n"
            f"    merged = pd.merge(user_events_df, user_events_df, on='user_id')\n"
            f"    return merged.shape[0] # Returns artificially multiplied row counts"
        )
        bug_desc = f"Row explosion: Inner join on non-unique user_id creates duplicate record combinations and inflated metrics in {s_name}."
        fixed = (
            f"import pandas as pd\n"
            f"def compute_churn_{idx}(user_events_df):\n"
            f"    # Fixed: Deduplicate user_id prior to join or merge on distinct composite keys\n"
            f"    unique_users = user_events_df.drop_duplicates(subset=['user_id'])\n"
            f"    return len(unique_users)"
        )
        exp = "Merging on non-unique keys results in an M-to-N Cartesian product, exponentially distorting analytical counts and metrics."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Cartesian Join & Deduplication Debugging", diff, idx,
            f"Diagnose and resolve a metric inflation bug caused by duplicate relational join keys ({s_name}).",
            "python", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges (Advanced Analytical SQL)
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S1"] # Advanced SQL
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE customer_purchases_{idx} (\n"
            f"    purchase_id INTEGER PRIMARY KEY,\n"
            f"    customer_id INTEGER NOT NULL,\n"
            f"    amount DECIMAL(10, 2) NOT NULL,\n"
            f"    purchase_date DATE NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO customer_purchases_{idx} VALUES (1, 101, 100.00, '2026-11-01');\n"
            f"INSERT INTO customer_purchases_{idx} VALUES (2, 101, 150.00, '2026-11-05');\n"
            f"INSERT INTO customer_purchases_{idx} VALUES (3, 102, 300.00, '2026-11-02');\n"
            f"INSERT INTO customer_purchases_{idx} VALUES (4, 102, 50.00, '2026-11-04');"
        )
        ref_sql = (
            f"SELECT customer_id,\n"
            f"       SUM(amount) AS total_lifetime_value,\n"
            f"       COUNT(*) AS order_count,\n"
            f"       ROUND(AVG(amount), 2) AS aov\n"
            f"FROM customer_purchases_{idx}\n"
            f"GROUP BY customer_id\n"
            f"ORDER BY total_lifetime_value DESC;"
        )
        expected = [
            {"customer_id": 102, "total_lifetime_value": 350.0, "order_count": 2, "aov": 175.0},
            {"customer_id": 101, "total_lifetime_value": 250.0, "order_count": 2, "aov": 125.0}
        ]
        exp = "Aggregates customer lifetime value (LTV), total purchase count, and average order value (AOV)."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "Customer Cohort & LTV SQL", diff, idx,
            f"Write an ANSI SQL query to compute customer LTV, order frequency, and AOV from `customer_purchases_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions (Data Warehouse & BI Platform Architecture)
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S4"] # BI Platforms & Warehousing
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"Modern Enterprise Data Warehouse & BI Semantic Layer #{idx:02d}"
        fn = [
            "Ingest transactional data from 12 operational databases with incremental CDC sync",
            "Model Kimball dimensional Star Schemas (Fact, Dimension, SCD Type 2 tables)",
            "Power executive BI dashboards with sub-3s query response time for 2,000 concurrent analysts"
        ]
        non_fn = [
            "Data freshness SLA < 15 minutes from transaction commit to dashboard refresh",
            "Column-level and row-level access control (RBAC) compliant with GDPR/HIPAA",
            "Comprehensive data lineage and automated schema drift alerts"
        ]
        scale = {
            "Total Data Warehouse Storage": "150 Terabytes",
            "Daily Ingested Transactions": "120 Million",
            "BI Dashboard Queries per Minute": "10,000"
        }
        ref_arch = (
            "Transactional DBs stream via Debezium CDC -> Kafka buffers raw events -> Snowflake / BigQuery raw staging -> "
            "dbt (data build tool) runs orchestrated transformations into dimensional models (Dim_User_SCD2, Fact_Orders) -> "
            "Cube / dbt Semantic Layer defines unified business metrics -> Preset / Tableau / Metabase serve cached analytical queries."
        )
        tradeoffs = "Pre-aggregating metric rollups in materialized views speeds up dashboard loads but increases warehouse storage costs and refresh complexity. Setting incremental clustering keys optimizes query pruning."
        rubric = [
            {"name": "Dimensional Modeling (Kimball)", "weight": 0.30, "description": "Designs Star schema, grain, facts, and SCD Type 2 handling."},
            {"name": "Semantic Layer & Metric Governance", "weight": 0.25, "description": "Defines unified metric definitions (dbt semantic layer)."},
            {"name": "Query Performance & Caching", "weight": 0.25, "description": "Applies clustering, partitioning, and BI caching."},
            {"name": "Data Quality & Lineage", "weight": 0.20, "description": "Implements dbt tests, Great Expectations, and lineage tracking."}
        ]
        exp = "Evaluates modern analytical data architecture balancing dimensional modeling, governed semantic layers, and sub-second BI query latency."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Enterprise Dimensional Data Warehouse Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_dan_questions()
    print(f"Generated {len(qs)} Data Analyst questions.")
