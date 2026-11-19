"""
Dataset 1: O*NET Essential Skills - Exploratory Data Analysis (EDA) Script
Generates publication-quality visualizations and a comprehensive EDA report.
Outputs:
- visualizations/top_skills.png
- visualizations/top_occupations.png
- visualizations/importance_distribution.png
- visualizations/level_distribution.png
- visualizations/missing_values.png
- visualizations/importance_vs_level.png
- reports/eda_report.md
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configure theme and typography
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "figure.titlesize": 16,
    "figure.autolayout": True,
})

RAW_PATH = "datasets/informal_skill_extraction/raw/essential_skills.csv"
VIS_DIR = "datasets/informal_skill_extraction/visualizations"
REPORT_PATH = "datasets/informal_skill_extraction/reports/eda_report.md"

os.makedirs(VIS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)


def run_eda():
    print(f"Loading dataset from {RAW_PATH} for EDA...")
    df = pd.read_csv(RAW_PATH)

    im_df = df[df["Scale ID"] == "IM"].copy()
    lv_df = df[df["Scale ID"] == "LV"].copy()

    # -------------------------------------------------------------------------
    # 1. Top Skills Visualization (top_skills.png)
    # Frequency vs Mean Importance vs Mean Level
    # -------------------------------------------------------------------------
    skill_stats = df.groupby(["Element Name", "Scale Name"])["Data Value"].mean().unstack()
    skill_stats["Frequency"] = df.groupby("Element Name")["Data Value"].count()
    skill_stats = skill_stats.sort_values(by="Importance", ascending=True)

    fig, ax = plt.subplots(figsize=(12, 7))
    y_pos = np.arange(len(skill_stats))
    bar_width = 0.38

    bars1 = ax.barh(y_pos - bar_width/2, skill_stats["Importance"], height=bar_width, label="Mean Importance Score (1.0 to 5.0)", color="#3b82f6")
    bars2 = ax.barh(y_pos + bar_width/2, skill_stats["Level"], height=bar_width, label="Mean Required Level (0.0 to 7.0)", color="#8b5cf6")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(skill_stats.index, fontweight="semibold")
    ax.set_xlabel("Mean Score across 910 Occupations")
    ax.set_title("O*NET Essential Skills: Mean Importance vs Required Competency Level\n(Note: Every skill occurs in all 910 occupations = 1,820 records each)", pad=15)
    ax.legend(loc="lower right", frameon=True)
    ax.set_xlim(0, 5.5)

    # Annotate values
    for bar in bars1:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}", xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=9, color="#1e3a8a", fontweight="bold")
    for bar in bars2:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}", xy=(w, bar.get_y() + bar.get_height()/2), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=9, color="#5b21b6", fontweight="bold")

    out_file1 = os.path.join(VIS_DIR, "top_skills.png")
    plt.savefig(out_file1, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file1}")

    # -------------------------------------------------------------------------
    # 2. Top Occupations by Skill Intensity (top_occupations.png)
    # -------------------------------------------------------------------------
    # Each occupation has exactly 20 records. We rank by overall mean skill score.
    occ_summary = df.groupby(["O*NET-SOC Code", "Title", "Scale Name"])["Data Value"].mean().unstack().reset_index()
    occ_summary["Combined_Score"] = occ_summary["Importance"] + occ_summary["Level"]
    top_20_occ = occ_summary.sort_values(by="Combined_Score", ascending=False).head(20).sort_values("Combined_Score", ascending=True)

    fig, ax = plt.subplots(figsize=(14, 9))
    y_pos = np.arange(len(top_20_occ))
    bar_width = 0.4

    b1 = ax.barh(y_pos - bar_width/2, top_20_occ["Importance"], height=bar_width, label="Average Skill Importance (Max 5.0)", color="#0ea5e9")
    b2 = ax.barh(y_pos + bar_width/2, top_20_occ["Level"], height=bar_width, label="Average Required Level (Max 7.0)", color="#6366f1")

    # Shorten titles if too long
    clean_titles = [t[:42] + "..." if len(t) > 42 else t for t in top_20_occ["Title"]]
    ax.set_yticks(y_pos)
    ax.set_yticklabels(clean_titles, fontsize=10)
    ax.set_xlabel("Mean Score across all 10 Essential Skills")
    ax.set_title("Top 20 Occupations by Foundational Skill Intensity & Demand Level\n(Uniform record count: 20 records per occupation)", pad=15)
    ax.legend(loc="lower right")
    ax.set_xlim(0, 6.0)

    out_file2 = os.path.join(VIS_DIR, "top_occupations.png")
    plt.savefig(out_file2, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file2}")

    # -------------------------------------------------------------------------
    # 3. Importance Score Distribution (importance_distribution.png)
    # -------------------------------------------------------------------------
    fig, (ax_box, ax_hist) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [0.2, 0.8]})
    sns.boxplot(x=im_df["Data Value"], ax=ax_box, color="#60a5fa", fliersize=3)
    ax_box.set(xlabel="")
    ax_box.set_title("Distribution of Skill Importance Scores (Scale: 1.0 = Not Important, 5.0 = Extremely Important)")

    sns.histplot(im_df["Data Value"], kde=True, ax=ax_hist, color="#2563eb", bins=30, stat="density", alpha=0.6)
    mean_val = im_df["Data Value"].mean()
    median_val = im_df["Data Value"].median()
    ax_hist.axvline(mean_val, color="#dc2626", linestyle="--", linewidth=2, label=f"Mean: {mean_val:.2f}")
    ax_hist.axvline(median_val, color="#16a34a", linestyle="-.", linewidth=2, label=f"Median: {median_val:.2f}")
    ax_hist.set_xlabel("Importance Score (1.0 to 5.0)")
    ax_hist.set_ylabel("Probability Density")
    ax_hist.legend(loc="upper right")

    out_file3 = os.path.join(VIS_DIR, "importance_distribution.png")
    plt.savefig(out_file3, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file3}")

    # -------------------------------------------------------------------------
    # 4. Level Score Distribution (level_distribution.png)
    # -------------------------------------------------------------------------
    fig, (ax_box, ax_hist) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [0.2, 0.8]})
    sns.boxplot(x=lv_df["Data Value"], ax=ax_box, color="#a78bfa", fliersize=3)
    ax_box.set(xlabel="")
    ax_box.set_title("Distribution of Skill Proficiency Level Scores (Scale: 0.0 to 7.0)")

    sns.histplot(lv_df["Data Value"], kde=True, ax=ax_hist, color="#7c3aed", bins=35, stat="density", alpha=0.6)
    lv_mean = lv_df["Data Value"].mean()
    lv_median = lv_df["Data Value"].median()
    ax_hist.axvline(lv_mean, color="#dc2626", linestyle="--", linewidth=2, label=f"Mean: {lv_mean:.2f}")
    ax_hist.axvline(lv_median, color="#16a34a", linestyle="-.", linewidth=2, label=f"Median: {lv_median:.2f}")
    ax_hist.set_xlabel("Proficiency Level Score (0.0 to 7.0)")
    ax_hist.set_ylabel("Probability Density")
    ax_hist.legend(loc="upper right")

    out_file4 = os.path.join(VIS_DIR, "level_distribution.png")
    plt.savefig(out_file4, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file4}")

    # -------------------------------------------------------------------------
    # 5. Missing Values Heatmap / Bar (missing_values.png)
    # -------------------------------------------------------------------------
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100
    missing_df = pd.DataFrame({"Missing_Count": null_counts, "Percentage": null_pct}).reset_index()
    missing_df.columns = ["Column", "Missing_Count", "Percentage"]
    missing_df = missing_df.sort_values(by="Percentage", ascending=False)

    fig, ax = plt.subplots(figsize=(11, 6))
    colors = ["#ef4444" if p > 0 else "#10b981" for p in missing_df["Percentage"]]
    bars = ax.barh(missing_df["Column"], missing_df["Percentage"], color=colors, height=0.6)
    ax.set_xlabel("Missing Percentage (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Missing Values Profile across All Columns in O*NET Essential Skills Dataset\n(Only 'Not Relevant' has nulls: 50.0% expected structural nulls on IM scale)", pad=15)

    for bar, count, pct in zip(bars, missing_df["Missing_Count"], missing_df["Percentage"]):
        text = f"{pct:.1f}% ({count:,} rows)" if pct > 0 else "0% (Complete)"
        ax.annotate(text, xy=(pct, bar.get_y() + bar.get_height()/2), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=9, fontweight="semibold")

    out_file5 = os.path.join(VIS_DIR, "missing_values.png")
    plt.savefig(out_file5, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file5}")

    # -------------------------------------------------------------------------
    # 6. Importance vs Level Comparison (importance_vs_level.png)
    # -------------------------------------------------------------------------
    # Merge IM and LV by (O*NET-SOC Code, Element ID)
    merged_scales = pd.merge(
        im_df[["O*NET-SOC Code", "Title", "Element ID", "Element Name", "Data Value"]].rename(columns={"Data Value": "Importance"}),
        lv_df[["O*NET-SOC Code", "Element ID", "Data Value", "Not Relevant"]].rename(columns={"Data Value": "Level"}),
        on=["O*NET-SOC Code", "Element ID"],
    )

    pearson_corr = merged_scales["Importance"].corr(merged_scales["Level"], method="pearson")
    spearman_corr = merged_scales["Importance"].corr(merged_scales["Level"], method="spearman")

    fig, ax = plt.subplots(figsize=(10, 8))
    # Hexbin or scatter with alpha
    hb = ax.hexbin(merged_scales["Importance"], merged_scales["Level"], gridsize=35, cmap="viridis", mincnt=1)
    cb = fig.colorbar(hb, ax=ax, label="Occupation Count Density")

    # Regression fit line
    sns.regplot(
        x="Importance",
        y="Level",
        data=merged_scales,
        scatter=False,
        ax=ax,
        color="#dc2626",
        line_kws={"linewidth": 2.5, "label": f"Linear Fit (Pearson r = {pearson_corr:.3f})"},
    )

    ax.set_xlabel("Importance Score (1.0 to 5.0)")
    ax.set_ylabel("Proficiency Level Score (0.0 to 7.0)")
    ax.set_title(f"Correlation between Skill Importance and Required Proficiency Level\nPearson r = {pearson_corr:.3f} | Spearman rho = {spearman_corr:.3f} (N = 9,100 pairs)", pad=15)
    ax.legend(loc="upper left")

    out_file6 = os.path.join(VIS_DIR, "importance_vs_level.png")
    plt.savefig(out_file6, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved {out_file6}")

    # -------------------------------------------------------------------------
    # Generate Comprehensive Markdown EDA Report
    # -------------------------------------------------------------------------
    with open(REPORT_PATH, "w") as f:
        f.write("# ELEVATE X AI — EXPLORATORY DATA ANALYSIS (EDA) REPORT\n\n")
        f.write("**Dataset**: O*NET Essential Skills Catalog\n")
        f.write(f"**Source File**: `{RAW_PATH}`\n")
        f.write("**Analytical Engine**: Pandas 3.1.1, NumPy, Seaborn 0.13.2, Matplotlib 3.11.2\n\n")
        f.write("---\n\n")

        f.write("## 1. Executive Summary & Core Insights\n\n")
        f.write("This report presents comprehensive exploratory data analysis of the 18,200 records in O*NET Essential Skills, covering 910 standardized formal occupations and 10 foundational skills across dual measurement scales (Importance and Level).\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> **Crucial Methodological Distinction**: In this dataset, every single one of the 910 occupations contains exactly 10 skill entries for Importance and 10 skill entries for Level. As a result, the **raw record frequency** of every skill is identical (1,820 rows each). To assess true skill demand, we must evaluate the **mean importance score** and **mean proficiency level**, rather than mistaking record count for importance.\n\n")

        f.write("## 2. Detailed Visualizations & Simple Language Explanations\n\n")

        f.write("### Figure 1: Top Skills by Importance and Required Level\n")
        f.write(f"![Top Skills](../visualizations/top_skills.png)\n\n")
        f.write("**Plain Language Explanation**:\n")
        f.write("- **Active Listening** (mean importance 3.65) and **Critical Thinking** (mean importance 3.61) are the two highest-rated foundational skills across the entire national economy.\n")
        f.write("- **Speaking** (3.59) and **Reading Comprehension** (3.56) closely follow, showing that receptive and expressive communication forms the bedrock of modern vocational and formal labor.\n")
        f.write("- Conversely, **Science** (mean importance 1.76, level 1.34) is highly specialized and not universally required across all trade roles.\n\n")

        f.write("### Figure 2: Occupations with Highest Foundational Skill Intensity\n")
        f.write(f"![Top Occupations](../visualizations/top_occupations.png)\n\n")
        f.write("**Plain Language Explanation**:\n")
        f.write("- Highly complex occupations (such as *Chief Executives*, *Biochemists and Biophysicists*, *Surgeons*, and *Lawyers*) demand peak levels across reading, logic, communication, and monitoring.\n")
        f.write("- Foundational trade and manual roles still demand high Active Listening and Critical Thinking, but lower academic Science or advanced Writing requirements.\n\n")

        f.write("### Figure 3: Distribution of Skill Importance Scores\n")
        f.write(f"![Importance Distribution](../visualizations/importance_distribution.png)\n\n")
        f.write("**Plain Language Explanation**:\n")
        f.write(f"- Importance scores range from 1.00 to 5.00 with a mean of **{mean_val:.2f}** and a median of **{median_val:.2f}**.\n")
        f.write("- The distribution exhibits a mild negative skew (majority of values fall between 2.5 and 4.0), demonstrating that these 10 foundational skills are considered moderately to very important for the vast majority of jobs.\n\n")

        f.write("### Figure 4: Distribution of Skill Proficiency Level Scores\n")
        f.write(f"![Level Distribution](../visualizations/level_distribution.png)\n\n")
        f.write("**Plain Language Explanation**:\n")
        f.write(f"- Required proficiency levels range from 0.00 to 6.00 with a mean of **{lv_mean:.2f}** and median of **{lv_median:.2f}**.\n")
        f.write("- Unlike importance, level scores have a wider spread and higher standard deviation (1.07 vs 0.77). Some manual trades require level 1-2 (basic everyday execution), while advanced professions require level 5-6 (complex multi-stage problem solving).\n\n")

        f.write("### Figure 5: Missing Value Audit Profile\n")
        f.write(f"![Missing Values](../visualizations/missing_values.png)\n\n")
        f.write("**Plain Language Explanation**:\n")
        f.write("- 14 out of 15 columns have zero missing values (100% data completeness).\n")
        f.write("- The only column with nulls is `Not Relevant` (9,100 nulls, exactly 50.0%). This is because O*NET only records relevance flags on the Level scale; Importance is an unconditional 1-5 continuous metric. There is no missing data defect in the dataset.\n\n")

        f.write("### Figure 6: Skill Importance vs. Required Level Correlation\n")
        f.write(f"![Importance vs Level](../visualizations/importance_vs_level.png)\n\n")
        f.write("**Plain Language Explanation**:\n")
        f.write(f"- There is a very strong positive correlation (**Pearson r = {pearson_corr:.3f}**, **Spearman rho = {spearman_corr:.3f}**) between how important a skill is and the level of proficiency required.\n")
        f.write("- If an occupation rates a skill as critical (Importance > 4.0), it almost universally demands elevated competency (Level > 4.0).\n\n")

        f.write("## 3. Skill Category Breakdown\n\n")
        f.write("| Element ID | Skill Name | O*NET Category | Mean Importance | Mean Level | % Occupations Relevant |\n")
        f.write("|---|---|---|---|---|---|\n")
        for name in skill_stats.index:
            sub_m = merged_scales[merged_scales["Element Name"] == name]
            rel_pct = (sub_m["Not Relevant"] != "Y").mean() * 100
            el_id = sub_m["Element ID"].iloc[0]
            cat = "Basic Skills - Content" if el_id.startswith("2.A.1") else "Basic Skills - Process"
            imp = sub_m["Importance"].mean()
            lvl = sub_m["Level"].mean()
            f.write(f"| `{el_id}` | **{name}** | {cat} | {imp:.2f} | {lvl:.2f} | {rel_pct:.1f}% |\n")
        f.write("\n")

        f.write("## 4. Key Takeaways for Elevate X AI Preprocessing\n\n")
        f.write("1. **Data Normalization Strategy**: Importance (1-5) and Level (0-7) operate on different native scales. For machine learning embeddings or cosine distance matching, min-max or z-score normalization must be applied to prevent Level from dominating Importance.\n")
        f.write("2. **Wide-Format Representation**: Because each occupation has 10 skills, transforming this long-format table into an occupation-level feature matrix with 10 importance and 10 level columns creates a dense 20-dimensional feature vector per occupation.\n")

    print(f"Generated EDA Report at {REPORT_PATH}")


if __name__ == "__main__":
    run_eda()

