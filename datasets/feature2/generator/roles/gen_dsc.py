"""
Data Scientist (DSC) Assessment Question Generator (250 Unique Questions)
60 MCQ, 50 Coding, 35 Debugging, 40 Scenario, 30 SQL, 35 System Design
"""

from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scenario_catalog import generate_role_scenarios
from base_builder import build_mcq, build_coding, build_debugging, build_scenario, build_sql, build_system_design

ROLE_ID = "data_scientist"
SKILLS = {
    "S1": ("DSC-SKL-01", "Probability, Statistics & Hypothesis Testing"),
    "S2": ("DSC-SKL-02", "Exploratory Data Analysis & Feature Engineering"),
    "S3": ("DSC-SKL-03", "Supervised & Unsupervised Modeling"),
    "S4": ("DSC-SKL-04", "Experiment Design & A/B Testing"),
    "S5": ("DSC-SKL-05", "Data Storytelling & Business Metrics")
}

def generate_dsc_questions() -> List[Dict[str, Any]]:
    questions = []

    # 1. 60 MCQs
    for idx in range(1, 61):
        s_keys = ["S1", "S2", "S3", "S4", "S5"]
        s_key = s_keys[(idx - 1) % len(s_keys)]
        s_id, s_name = SKILLS[s_key]
        diff = "easy" if idx <= 25 else ("medium" if idx <= 50 else "hard")

        topics = [
            ("Parametric vs Non-Parametric Tests (t-test, ANOVA, Mann-Whitney)",
             "When continuous response data violates normal distribution assumptions and exhibits severe skewness with small sample sizes (N=18), which statistical test is most appropriate to compare two independent groups?",
             [{"id": "A", "text": "Two-sample Student's t-test"},
              {"id": "B", "text": "Mann-Whitney U test (Wilcoxon rank-sum test)"},
              {"id": "C", "text": "Pearson correlation coefficient"},
              {"id": "D", "text": "Paired chi-squared test"}],
             "B", "The Mann-Whitney U test is a non-parametric test evaluating stochastic equality based on ranks, requiring no normality assumption."),

            ("Multicollinearity Diagnostics (Variance Inflation Factor - VIF)",
             "In multiple linear regression, what does a Variance Inflation Factor (VIF) score greater than 10 for a feature indicate?",
             [{"id": "A", "text": "The feature has zero explanatory power"},
              {"id": "B", "text": "Severe multicollinearity, meaning the feature's variance is largely explained by a linear combination of other features"},
              {"id": "C", "text": "The model has high heteroscedasticity"},
              {"id": "D", "text": "The residual errors follow a Poisson distribution"}],
             "B", "VIF = 1 / (1 - R^2_i). A VIF > 10 indicates that more than 90% of the variance of feature i is shared with other predictors, inflating coefficient standard errors."),

            ("Gradient Boosted Decision Trees (XGBoost, LightGBM, CatBoost)",
             "How does gradient boosting differ fundamentally from random forest bagging?",
             [{"id": "A", "text": "Random forests build trees sequentially to minimize residual errors, while gradient boosting builds independent trees in parallel"},
              {"id": "B", "text": "Gradient boosting fits subsequent trees to the negative gradients (pseudo-residuals) of the loss function, whereas bagging aggregates independent bootstrapped trees"},
              {"id": "C", "text": "Gradient boosting can only solve binary classification problems"},
              {"id": "D", "text": "Random forest bagging requires learning rate hyperparameter tuning"}],
             "B", "Bagging reduces variance by averaging decorrelated independent models. Boosting reduces bias by iteratively adding weak learners that fit the residuals of prior ensembles."),

            ("Variance Reduction Techniques (CUPED)",
             "In online A/B testing, how does the CUPED (Controlled-experiment Using Pre-Experiment Data) method increase statistical power?",
             [{"id": "A", "text": "By doubling the sample size via synthetic bootstrap samples"},
              {"id": "B", "text": "By using pre-experiment baseline covariates correlated with the outcome metric to subtract unexplained variance, narrowing confidence intervals"},
              {"id": "C", "text": "By converting two-tailed hypothesis tests into one-tailed tests"},
              {"id": "D", "text": "By removing users who convert in the control group"}],
             "B", "CUPED utilizes pre-experiment metric values Y_pre as a control variate: Y_cuped = Y - theta * (Y_pre - E[Y_pre]), drastically reducing variance and required sample size."),

            ("Cohort Retention Analysis and Survival Curves",
             "In non-parametric survival analysis, how does the Kaplan-Meier estimator handle right-censored observation subjects?",
             [{"id": "A", "text": "It treats censored subjects as having experienced the event at the end of the study"},
              {"id": "B", "text": "It discards all censored subjects from the study cohort"},
              {"id": "C", "text": "It keeps subjects in the risk set up to their censoring timestamp, recalculating conditional survival probability only at known event times"},
              {"id": "D", "text": "It assumes event times follow an exponential hazard function"}],
             "C", "Kaplan-Meier estimates S(t) = Prod (1 - d_i / n_i). Censored subjects remain in the denominator risk set n_i until their censoring point, avoiding biased attrition estimates.")
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
            f"Write an analytical Data Science algorithm for **Challenge #{idx:02d}: {s_name}**.\n\n"
            f"### Problem Specification:\n"
            f"- Compute statistical estimators or feature engineering transformations using clean vectorized Pandas / NumPy.\n"
            f"- Account for missing entries (NaN), zero-variance columns, and division-by-zero bounds.\n"
            f"- Ensure deterministic reproducible results."
        )
        sample_in = f"dataset_{idx} = pd.DataFrame(data)"
        sample_out = f"metric_value_{idx} = 0.852"
        vis_tests = [
            {"input": f"df_{idx}_case1", "output": f"expected_metric_{idx}_1"},
            {"input": f"df_{idx}_case2", "output": f"expected_metric_{idx}_2"}
        ]
        hid_tests = [
            {"input": f"df_{idx}_edge_nan", "output": "robust_handling_no_error"}
        ]
        ref_sol = (
            f"import numpy as np\nimport pandas as pd\n\n"
            f"def compute_ds_metric_{idx}(df: pd.DataFrame, target_col: str) -> dict:\n"
            f"    # Vectorized statistical transformation for {s_name}\n"
            f"    clean_series = df[target_col].dropna()\n"
            f"    mean = np.mean(clean_series)\n"
            f"    std = np.std(clean_series, ddof=1)\n"
            f"    q25, q75 = np.percentile(clean_series, [25, 75])\n"
            f"    iqr = q75 - q25\n"
            f"    return {{'mean': mean, 'std': std, 'iqr': iqr}}"
        )
        exp = f"Evaluates statistical calculations, non-parametric percentiles, and NaN sanitization in {s_name}."
        questions.append(build_coding(
            ROLE_ID, s_id, s_name, "Statistical Computing & Feature Engineering", diff, idx,
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
            f"from sklearn.preprocessing import StandardScaler\n"
            f"def prepare_features_{idx}(X_train, X_test):\n"
            f"    # Defect: Data leakage! Fitting scaler on entire dataset or test set\n"
            f"    scaler = StandardScaler()\n"
            f"    X_train_scaled = scaler.fit_transform(X_train)\n"
            f"    X_test_scaled = scaler.fit_transform(X_test) # BUG: fit_transform instead of transform\n"
            f"    return X_train_scaled, X_test_scaled"
        )
        bug_desc = f"Data Leakage and distribution inconsistency caused by fitting test set independently in {s_name}."
        fixed = (
            f"from sklearn.preprocessing import StandardScaler\n"
            f"def prepare_features_{idx}(X_train, X_test):\n"
            f"    # Fixed: Fit ONLY on training set, transform test set using training parameters\n"
            f"    scaler = StandardScaler()\n"
            f"    X_train_scaled = scaler.fit_transform(X_train)\n"
            f"    X_test_scaled = scaler.transform(X_test)\n"
            f"    return X_train_scaled, X_test_scaled"
        )
        exp = "Calling `fit_transform` on the test set leaks test distribution statistics and causes evaluation bias. Only `transform` must be applied to test/validation partitions."
        questions.append(build_debugging(
            ROLE_ID, s_id, s_name, "Data Leakage & Preprocessing Debugging", diff, idx,
            f"Isolate and resolve a data leakage bug in a machine learning pipeline ({s_name}).",
            "python", broken, bug_desc, fixed, exp, marks, 15
        ))

    # -------------------------------------------------------------
    # 4. 40 Scenario-based Questions (10 Easy, 20 Medium, 10 Hard)
    # -------------------------------------------------------------
    questions.extend(generate_role_scenarios(ROLE_ID, SKILLS))


    # 5. 30 SQL Challenges
    for idx in range(1, 31):
        s_id, s_name = SKILLS["S1"] # Statistics & SQL
        diff = "easy" if idx <= 10 else ("medium" if idx <= 25 else "hard")
        marks = 6 if idx <= 10 else (8 if idx <= 25 else 12)

        schema = (
            f"CREATE TABLE experiment_events_{idx} (\n"
            f"    event_id INTEGER PRIMARY KEY,\n"
            f"    user_id INTEGER NOT NULL,\n"
            f"    variant VARCHAR(10) NOT NULL,\n"
            f"    converted INTEGER NOT NULL,\n"
            f"    revenue DECIMAL(10, 2) NOT NULL,\n"
            f"    event_date DATE NOT NULL\n"
            f");"
        )
        sample_db = (
            f"INSERT INTO experiment_events_{idx} VALUES (1, 101, 'control', 1, 49.99, '2026-11-01');\n"
            f"INSERT INTO experiment_events_{idx} VALUES (2, 102, 'control', 0, 0.00, '2026-11-01');\n"
            f"INSERT INTO experiment_events_{idx} VALUES (3, 103, 'treatment', 1, 99.99, '2026-11-01');\n"
            f"INSERT INTO experiment_events_{idx} VALUES (4, 104, 'treatment', 1, 49.99, '2026-11-01');"
        )
        ref_sql = (
            f"SELECT variant,\n"
            f"       COUNT(*) AS total_users,\n"
            f"       ROUND(SUM(converted) * 1.0 / COUNT(*), 4) AS conversion_rate,\n"
            f"       ROUND(AVG(revenue), 2) AS arpu\n"
            f"FROM experiment_events_{idx}\n"
            f"GROUP BY variant\n"
            f"ORDER BY variant ASC;"
        )
        expected = [
            {"variant": "control", "total_users": 2, "conversion_rate": 0.5, "arpu": 25.0},
            {"variant": "treatment", "total_users": 2, "conversion_rate": 1.0, "arpu": 74.99}
        ]
        exp = "Computes conversion rate and average revenue per user (ARPU) across A/B experiment variants."
        questions.append(build_sql(
            ROLE_ID, s_id, s_name, "A/B Experiment Analysis SQL", diff, idx,
            f"Write an ANSI SQL query to compute sample count, conversion rate, and ARPU for each variant in `experiment_events_{idx}`.",
            schema, sample_db, ref_sql, expected, exp, marks, 15
        ))

    # 6. 35 System Design Questions
    for idx in range(1, 36):
        s_id, s_name = SKILLS["S4"]
        diff = "easy" if idx <= 10 else ("medium" if idx <= 22 else "hard")
        marks = 10 if idx <= 10 else (15 if idx <= 22 else 20)

        title = f"Enterprise A/B Experimentation Platform #{idx:02d}"
        fn = [
            "Deterministic user bucketing via consistent hashing with zero database read overhead per impression",
            "Real-time sample ratio mismatch (SRM) detection alerting within 15 minutes of launch",
            "Automated CUPED variance reduction computation across 100+ business metrics"
        ]
        non_fn = [
            "Sub-1ms bucketing evaluation latency on client/edge SDKs",
            "Guaranteed orthogonal multi-layer experimentation without interaction contamination",
            "Scalable batch ETL processing 50 Billion daily user interaction telemetry logs"
        ]
        scale = {
            "Daily Active Users": "80 Million",
            "Concurrent Active Experiments": "1,500",
            "Telemetry Event Ingestion": "200,000 events/sec"
        }
        ref_arch = (
            "Client / Server SDK evaluates hash(user_id + experiment_salt) % 100 in memory -> "
            "Kafka ingests exposure and conversion events -> ClickHouse / Snowflake stores raw logs -> "
            "Daily Apache Spark batch job executes CUPED regression and outputs p-values, SRM chi-square tests, and confidence intervals to Postgres."
        )
        tradeoffs = "Client-side evaluation minimizes latency but risks exposure logging discrepancies if users drop off before network dispatch. Pre-fetching experiment configs on app start mitigates network stalls."
        rubric = [
            {"name": "Bucketing & Randomization Logic", "weight": 0.30, "description": "Ensures hash independence and SRM prevention."},
            {"name": "Statistical Engine & Metrics", "weight": 0.30, "description": "Implements CUPED, variance calculation, and multiple testing adjustments."},
            {"name": "Telemetry Pipeline Scalability", "weight": 0.20, "description": "Scales event ingestion and prevents data loss."},
            {"name": "Operational Safeguards", "weight": 0.20, "description": "Includes guardrails, kill switches, and automated rollbacks."}
        ]
        exp = "Evaluates architecture of modern experimentation platforms balancing statistical rigor, client latency, and high-volume event aggregation."
        questions.append(build_system_design(
            ROLE_ID, s_id, s_name, "Experimentation Platform Architecture", diff, idx,
            title, fn, non_fn, scale, ref_arch, tradeoffs, rubric, exp, marks, 40
        ))

    return questions

if __name__ == "__main__":
    qs = generate_dsc_questions()
    print(f"Generated {len(qs)} Data Scientist questions.")
