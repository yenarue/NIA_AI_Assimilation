"""
simple_slopes_and_figure.py
================================================================================
Manuscript: "AI Use Without Complementary Assets? IT-Organization Boundary
Conditions of AI-Driven Process Improvement in Korean Firms"
Target journal: Industrial Management & Data Systems (IMDS)

Purpose of this script
----------------------
1. Reproduce the weighted Model 5 reported in Table 3 of the manuscript.
2. Compute formal simple-slope statistics for AI use breadth at
       ITorg = 0 (no IT organization)  and  ITorg = 1 (with IT organization),
   using the re-parameterization method of Aiken and West (1991, ch. 2):
   the slope at ITorg=1 is obtained by refitting the same model after flipping
   the IT-organization indicator so that ITorg=1 becomes the reference category.
3. Draw Figure 1: predicted process improvement against AI use breadth (0-9),
   separately for ITorg=0 and ITorg=1, with shaded 95 % confidence bands
   computed from the model variance-covariance matrix via the delta method.

Inputs
------
Expected at run time:
    DATA_PATH  : path to the cleaned analytical CSV/Parquet that contains the
                 12,203-firm panel from the 2024 NIA Survey on Information
                 Society Statistics for Enterprises, including the columns
                 listed in COLS_REQUIRED below.

Outputs
-------
    outputs/simple_slopes_table.csv     # slope, SE, t, p, 95% CI
    outputs/figure1_ai_itorg.png        # publication-quality figure
    outputs/figure1_ai_itorg.pdf        # vector version for journal upload

Dependencies
------------
    numpy, pandas, statsmodels >= 0.14, matplotlib

Author
------
    [Anonymized for review]
================================================================================
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
DATA_PATH = Path("working/analysis/nia_2024_analysis_total.csv")
OUTPUT_DIR = Path("outputs/w12/simple_slopes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COLS_REQUIRED = [
    "effect_proc_improve",   # DV: perceived process improvement (1-5)
    "ai_use_sum",            # IV: AI use breadth (count of AI types, 0-10)
    "it_org_any",            # Moderator: 1 if IT-organization present, else 0
    "dmi",               # Continuous moderator: digital maturity count
    "it_invest_sum",         # Control: IT investment breadth (count)
    "firm_size",         # Control: firm-size category (1-4)
    "industry",              # Control: KSIC industry category (1-16)
    "region",                # Control: Korean region (1-17)
    "firm_type",             # Control: 1=individual, 2=corporation
    "weight",                # NIA RIM_WT sampling weight
]


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def load_data(path: Path) -> pd.DataFrame:
    """Load the cleaned NIA 2024 analytical dataset."""
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)
    missing = set(COLS_REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Required columns missing from data: {missing}")
    return df


def build_design(df: pd.DataFrame, itorg_flip: bool = False) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Construct the design matrix for the weighted Model 5 specification.

    If ``itorg_flip`` is True, the IT-organization indicator is replaced by
    (1 - it_org_any) before the interaction term is rebuilt.  Refitting on
    this flipped design yields the simple slope at ITorg=1 directly as the
    coefficient on ``ai_use_sum``, with its HC3-robust SE supplied by
    statsmodels.

    Returns
    -------
    X : pd.DataFrame
        Design matrix including constant, focal variables, interactions,
        and one-hot encoded fixed effects.
    y : pd.Series
        Dependent variable.
    w : pd.Series
        NIA sampling weights.
    """
    work = df.copy()
    if itorg_flip:
        work["it_org_any"] = 1 - work["it_org_any"]
    work["ai_x_itorg"] = work["ai_use_sum"] * work["it_org_any"]
    work["ai_x_dmi"]   = work["ai_use_sum"] * work["dmi"]

    # Fixed-effect dummies (drop first to avoid collinearity)
    fe = pd.get_dummies(
        work[["industry", "region", "firm_type", "firm_size"]].astype("category"),
        prefix=["ind", "reg", "ftype", "fsize"],
        drop_first=True,
    ).astype(float)

    focal = work[[
        "ai_use_sum", "it_org_any", "ai_x_itorg",
        "dmi", "ai_x_dmi",
        "it_invest_sum",
    ]].astype(float)

    X = pd.concat([focal, fe], axis=1)
    X = sm.add_constant(X, has_constant="add")
    y = work["effect_proc_improve"].astype(float)
    w = work["weight"].astype(float)
    return X, y, w


def fit_weighted_hc3(X: pd.DataFrame, y: pd.Series, w: pd.Series) -> sm.regression.linear_model.RegressionResultsWrapper:
    """Weighted OLS with HC3 robust standard errors, matching Table 3 Model 5."""
    model = sm.WLS(y, X, weights=w)
    fit = model.fit(cov_type="HC3")
    return fit


def simple_slope_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a tidy table with the two simple slopes (ITorg=0 and ITorg=1),
    their HC3 robust SEs, t-statistics, p-values, and 95 % CIs.
    """
    # Baseline (ITorg=0 is reference): coefficient on ai_use_sum is the
    # simple slope at ITorg=0.
    X0, y0, w0 = build_design(df, itorg_flip=False)
    fit0 = fit_weighted_hc3(X0, y0, w0)

    # Flipped parameterization (ITorg=1 is reference): coefficient on
    # ai_use_sum is the simple slope at ITorg=1.
    X1, y1, w1 = build_design(df, itorg_flip=True)
    fit1 = fit_weighted_hc3(X1, y1, w1)

    rows = []
    for label, fit in [("ITorg = 0 (no IT organization)", fit0),
                       ("ITorg = 1 (with IT organization)", fit1)]:
        b   = fit.params["ai_use_sum"]
        se  = fit.bse["ai_use_sum"]
        t   = fit.tvalues["ai_use_sum"]
        p   = fit.pvalues["ai_use_sum"]
        lo  = b - 1.96 * se
        hi  = b + 1.96 * se
        rows.append({
            "Condition": label,
            "Simple slope (β_AI)": round(b, 4),
            "HC3 SE": round(se, 4),
            "t": round(t, 3),
            "p-value": round(p, 4),
            "95% CI lower": round(lo, 4),
            "95% CI upper": round(hi, 4),
        })
    # Add slope difference (the AI × ITorg interaction coefficient)
    b_int  = fit0.params["ai_x_itorg"]
    se_int = fit0.bse["ai_x_itorg"]
    t_int  = fit0.tvalues["ai_x_itorg"]
    p_int  = fit0.pvalues["ai_x_itorg"]
    rows.append({
        "Condition": "Slope difference (AI × ITorg interaction)",
        "Simple slope (β_AI)": round(b_int, 4),
        "HC3 SE": round(se_int, 4),
        "t": round(t_int, 3),
        "p-value": round(p_int, 4),
        "95% CI lower": round(b_int - 1.96 * se_int, 4),
        "95% CI upper": round(b_int + 1.96 * se_int, 4),
    })
    return pd.DataFrame(rows)


def predicted_with_ci(fit, X: pd.DataFrame, ai_grid: np.ndarray, itorg_value: int) -> pd.DataFrame:
    """
    Compute predicted Ŷ and 95% CI for a grid of AI-use-breadth values,
    holding ITorg at itorg_value and all other covariates at their sample
    means.  The delta-method variance is

        Var(L β) = L Σ Lᵀ

    where L is the row of contrasts corresponding to each grid point and Σ
    is the HC3 robust variance-covariance matrix.
    """
    mean_row = X.mean(axis=0).to_dict()
    rows = []
    for ai in ai_grid:
        row = dict(mean_row)
        row["ai_use_sum"]  = ai
        row["it_org_any"]  = float(itorg_value)
        row["ai_x_itorg"]  = ai * itorg_value
        row["ai_x_dmi"]    = ai * mean_row["dmi"]
        rows.append(row)
    Xnew = pd.DataFrame(rows)[X.columns]

    yhat = fit.predict(Xnew)
    vcov = fit.cov_params()
    # Variance of each prediction: x · Σ · xᵀ
    L = Xnew.values
    se = np.sqrt(np.einsum("ij,jk,ik->i", L, vcov.values, L))
    return pd.DataFrame({
        "ai_use_sum": ai_grid,
        "yhat": yhat.values,
        "lo95": yhat.values - 1.96 * se,
        "hi95": yhat.values + 1.96 * se,
    })


def draw_figure1(df: pd.DataFrame, out_png: Path, out_pdf: Path) -> None:
    """Draw Figure 1 with 95% confidence bands for ITorg=0 vs ITorg=1."""
    X, y, w = build_design(df, itorg_flip=False)
    fit     = fit_weighted_hc3(X, y, w)

    ai_grid = np.linspace(0, 9, 91)
    pred0   = predicted_with_ci(fit, X, ai_grid, itorg_value=0)
    pred1   = predicted_with_ci(fit, X, ai_grid, itorg_value=1)

    fig, ax = plt.subplots(figsize=(6.5, 4.3), dpi=300)
    ax.plot(pred0["ai_use_sum"], pred0["yhat"], color="#C44E52",
            label="No IT organization", linewidth=2.0)
    ax.fill_between(pred0["ai_use_sum"], pred0["lo95"], pred0["hi95"],
                    color="#C44E52", alpha=0.18, linewidth=0)
    ax.plot(pred1["ai_use_sum"], pred1["yhat"], color="#4C72B0",
            label="With IT organization", linewidth=2.0)
    ax.fill_between(pred1["ai_use_sum"], pred1["lo95"], pred1["hi95"],
                    color="#4C72B0", alpha=0.18, linewidth=0)

    ax.set_xlabel("AI use breadth (count of AI application types)")
    ax.set_ylabel("Predicted perceived process improvement (1–5)")
    ax.set_xlim(0, 9)
    ax.set_ylim(3.4, 4.6)
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    df = load_data(DATA_PATH)
    tbl = simple_slope_table(df)
    print("\n=== Simple-slope test of AI use breadth on perceived process improvement ===\n")
    print(tbl.to_string(index=False))
    tbl.to_csv(OUTPUT_DIR / "simple_slopes_table.csv", index=False)

    draw_figure1(
        df,
        OUTPUT_DIR / "figure1_ai_itorg.png",
        OUTPUT_DIR / "figure1_ai_itorg.pdf",
    )
    print(f"\nFigure 1 saved to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
