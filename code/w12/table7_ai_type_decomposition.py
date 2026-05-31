"""
table7_ai_type_decomposition.py
================================================================================
Manuscript: "AI Use Without Complementary Assets? IT-Organization Boundary
Conditions of AI-Driven Process Improvement in Korean Firms"
Target journal: Industrial Management & Data Systems (IMDS)

Purpose of this script
----------------------
Reviewer-anticipated robustness check: decompose the AI use-breadth × IT-
organization interaction by AI application type.  The Q28 module of the 2024
NIA Survey on Information Society Statistics for Enterprises records ten
binary AI-use indicators (Q28_1, Q28_2, …, Q28_10).  Aggregating these into a
single count variable (``ai_use_sum``) obscures whether the organisational-
complementarity pattern is driven by a particular application type
(e.g. predictive analytics, computer vision, generative text AI) or whether
it is a uniform feature of broad AI engagement.

For each of the ten AI types we re-estimate the weighted Model 5
specification, replacing ``ai_use_sum`` (and the interaction ``ai_use_sum ×
it_org_any``) with the type-specific binary and its corresponding interaction:

    ProcessImprove_i = α + β_1 · AI_k_i + β_2 · ITorg_i
                       + β_3 · (AI_k_i × ITorg_i)
                       + β_4 · DMI_i + β_5 · ITinvest_i
                       + γ′X_i + ε_i ,                        k = 1, …, 10

All other controls and HC3 robust standard errors are identical to the main
specification.  Output is Table 7 of the manuscript: AI type label, sample
prevalence, β_AI alone, β_AI×ITorg, simple slope at ITorg=1, and corresponding
p-values.

Inputs
------
    DATA_PATH : path to the cleaned 12,203-firm NIA 2024 analytical dataset
                with the columns listed in COLS_REQUIRED below.

Outputs
-------
    outputs/w12/table7_ai_type_decomposition.csv
    outputs/w12/table7_ai_type_decomposition.xlsx

Dependencies
------------
    numpy, pandas, statsmodels >= 0.14, openpyxl

Author
------
    [Anonymized for review]
================================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
import statsmodels.api as sm

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DATA_PATH = Path("working/analysis/nia_2024_analysis_total.csv")
OUTPUT_DIR = Path("outputs/w12")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Labels for the ten Q28 sub-items.  NOTE: confirm these against the 2024 NIA
# codebook before publication; the labels below are taken from the codebook
# preview shipped with the 2024 release and may require minor wording edits.
AI_TYPE_LABELS: Dict[str, str] = {
    "ai_use_doc_info_collect":  "Document creation and information retrieval",   # 문서작성 및 정보 수집
    "ai_use_task_automation":  "Task automation support",                        # 업무자동화 지원
    "ai_use_decision_support":  "Decision support",                               # 의사 결정 지원
    "ai_use_speech_to_text":  "Speech-to-machine-readable conversion (STT)",    # 음성→기계 형식 변환
    "ai_use_gen_summarize_edit":  "Generative AI (text / image / audio)",           # 생성·요약·편집 AI
    "ai_use_image_video_recognition":  "Computer vision (object / person identification)", # 이미지·영상 기반 식별
    "ai_use_ml_data_analysis":  "Machine learning for data analytics",            # 데이터 분석 머신러닝
    "ai_use_text_language_analysis":  "Natural language processing (text analysis)",    # 문자 언어 분석 AI
    "ai_use_autonomous_mobility":  "Autonomous mobility AI (autonomous vehicles / robotics)", # 자율이동 AI
    "ai_use_other": "Other AI applications",                          # 기타
}

COLS_BASE = [
    "effect_proc_improve",   # DV
    "it_org_any",            # focal moderator
    "dmi",               # continuous moderator
    "it_invest_sum",         # control
    "firm_size",         # control
    "industry",              # control
    "region",                # control
    "firm_type",             # control
    "weight",                # NIA sampling weight
]


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def load_data(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)
    missing = set(COLS_BASE) - set(df.columns)
    if missing:
        raise ValueError(f"Required columns missing from data: {missing}")
    return df


def fit_type_specific(df: pd.DataFrame, ai_col: str) -> sm.regression.linear_model.RegressionResultsWrapper:
    """Refit the weighted Model 5 with one AI application type at a time."""
    work = df.copy()
    work["ai_focal"]  = work[ai_col].astype(float)
    work["ai_x_org"]  = work["ai_focal"] * work["it_org_any"].astype(float)
    work["ai_x_dmi"]  = work["ai_focal"] * work["dmi"].astype(float)

    fe = pd.get_dummies(
        work[["industry", "region", "firm_type", "firm_size"]].astype("category"),
        prefix=["ind", "reg", "ftype", "fsize"],
        drop_first=True,
    ).astype(float)

    focal = work[[
        "ai_focal", "it_org_any", "ai_x_org",
        "dmi", "ai_x_dmi", "it_invest_sum",
    ]].astype(float)

    X = pd.concat([focal, fe], axis=1)
    X = sm.add_constant(X, has_constant="add")
    y = work["effect_proc_improve"].astype(float)
    w = work["weight"].astype(float)
    return sm.WLS(y, X, weights=w).fit(cov_type="HC3")


def sig_stars(p: float) -> str:
    if p < .001: return "***"
    if p < .01:  return "**"
    if p < .05:  return "*"
    if p < .10:  return "†"
    return ""


def format_coef(b: float, se: float, p: float) -> str:
    return f"{b:+.4f}{sig_stars(p)} ({se:.4f})"


# -----------------------------------------------------------------------------
# Main routine
# -----------------------------------------------------------------------------
def build_table7(df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict] = []
    n_total = len(df)
    for col, label in AI_TYPE_LABELS.items():
        if col not in df.columns:
            print(f"[skip] {col} not in data")
            continue
        prevalence = df[col].mean()

        fit = fit_type_specific(df, col)
        b_ai   = fit.params["ai_focal"]
        se_ai  = fit.bse["ai_focal"]
        p_ai   = fit.pvalues["ai_focal"]
        b_x    = fit.params["ai_x_org"]
        se_x   = fit.bse["ai_x_org"]
        p_x    = fit.pvalues["ai_x_org"]

        # Simple slope at ITorg=1 = b_ai + b_x; SE via delta method
        slope1   = b_ai + b_x
        vcov     = fit.cov_params()
        var_sum  = (vcov.loc["ai_focal", "ai_focal"]
                    + vcov.loc["ai_x_org", "ai_x_org"]
                    + 2.0 * vcov.loc["ai_focal", "ai_x_org"])
        se_slope = float(np.sqrt(max(var_sum, 0.0)))
        t_slope  = slope1 / se_slope if se_slope > 0 else np.nan
        from scipy import stats
        p_slope = 2.0 * (1.0 - stats.norm.cdf(abs(t_slope))) if np.isfinite(t_slope) else np.nan

        rows.append({
            "AI type": label,
            "Q28 item": col,
            "Prevalence (%)": round(100 * prevalence, 1),
            "N": n_total,
            "β_AI alone": format_coef(b_ai, se_ai, p_ai),
            "β_AI × ITorg": format_coef(b_x, se_x, p_x),
            "Simple slope at ITorg=1": format_coef(slope1, se_slope, p_slope),
            "R²": round(fit.rsquared, 3),
        })

    return pd.DataFrame(rows)


def main() -> None:
    df = load_data(DATA_PATH)
    tbl = build_table7(df)
    print("\n=== Table 7. AI application-type decomposition (weighted Model 5) ===\n")
    print(tbl.to_string(index=False))

    csv_path = OUTPUT_DIR / "table7_ai_type_decomposition.csv"
    xlsx_path = OUTPUT_DIR / "table7_ai_type_decomposition.xlsx"
    tbl.to_csv(csv_path, index=False)
    tbl.to_excel(xlsx_path, index=False)
    print(f"\nTable 7 written to:\n  {csv_path}\n  {xlsx_path}")


if __name__ == "__main__":
    main()
