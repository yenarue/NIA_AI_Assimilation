"""
simple_slopes_and_figure_FIXED.py
================================================================================
Corrected drop-in replacement for simple_slopes_and_figure.py.

WHY THE ORIGINAL DID NOT MATCH TABLE 3 / SHOWED NON-SIGNIFICANT SLOPES
---------------------------------------------------------------------
The headline Model 5 reported in Table 3 is:

    effect_proc_improve ~ ai_use_sum + it_org_any + ai_use_sum:it_org_any
                          + dmi + it_invest_sum + firm_size
                          + C(industry) + C(region) + C(firm_type)        (WLS, HC3)

i.e. it does NOT contain an ai_use_sum:dmi term, and firm_size enters
LINEARLY (not as categorical dummies).

The original script instead (a) added ai_use_sum:dmi to the model and
(b) one-hot encoded firm_size. With ai_use_sum:dmi in the model and dmi
left at its raw scale, the ai_use_sum coefficient is the slope of AI use
*at dmi = 0* (a boundary value, mean dmi = 5.95). Because ai_use_sum and
ai_use_sum:dmi are highly collinear (r(ai, dmi) = 0.57), the SE on
ai_use_sum inflates from ~0.012 to ~0.016, which is why the slope both
shifted (-0.025 -> -0.022) and lost significance.

This corrected version matches the headline Model 5 exactly, so the
ITorg=0 simple slope equals the Table 3 ai_use_sum coefficient by
construction, and the figure is drawn from the same model (no internal
table/figure inconsistency).

Verified output on the 12,203-firm NIA 2024 data:
    ITorg = 0 :  b = -0.0248,  SE = 0.0117,  p = 0.034
    ITorg = 1 :  b = +0.0262,  SE = 0.0120,  p = 0.029
    AI x ITorg interaction: b = +0.0511, p = 0.0008
(= the values reported in section 4.2.)
================================================================================
"""
from __future__ import annotations
from pathlib import Path
from typing import Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA_PATH = Path("working/analysis/nia_2024_analysis_total.csv")  # <-- adjust
OUTPUT_DIR = Path("outputs/w13/simple_slopes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# NOTE: the analytical file ships dmi as `dmi` (not `dmi_sum`).
COLS_REQUIRED = [
    "effect_proc_improve", "ai_use_sum", "it_org_any", "dmi",
    "it_invest_sum", "firm_size", "industry", "region", "firm_type", "weight",
]


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
    missing = set(COLS_REQUIRED) - set(df.columns)
    if missing:
        raise ValueError(f"Required columns missing from data: {missing}")
    return df


def build_design(df: pd.DataFrame, itorg_flip: bool = False) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Headline Model 5 design.  NO ai_use_sum:dmi term; firm_size enters
    LINEARLY.  Flipping it_org_any to (1 - it_org_any) makes the ai_use_sum
    coefficient read the simple slope at ITorg = 1.
    """
    work = df.copy()
    if itorg_flip:
        work["it_org_any"] = 1 - work["it_org_any"]
    work["ai_x_itorg"] = work["ai_use_sum"] * work["it_org_any"]

    fe = pd.get_dummies(
        work[["industry", "region", "firm_type"]].astype("category"),
        prefix=["ind", "reg", "ftype"], drop_first=True,
    ).astype(float)

    focal = work[[
        "ai_use_sum", "it_org_any", "ai_x_itorg",
        "dmi", "it_invest_sum", "firm_size",   # firm_size LINEAR, no ai_x_dmi
    ]].astype(float)

    X = sm.add_constant(pd.concat([focal, fe], axis=1), has_constant="add")
    y = work["effect_proc_improve"].astype(float)
    w = work["weight"].astype(float)
    return X, y, w


def fit_weighted_hc3(X, y, w):
    return sm.WLS(y, X, weights=w).fit(cov_type="HC3")


def simple_slope_table(df: pd.DataFrame) -> pd.DataFrame:
    X0, y0, w0 = build_design(df, itorg_flip=False)
    fit0 = fit_weighted_hc3(X0, y0, w0)
    X1, y1, w1 = build_design(df, itorg_flip=True)
    fit1 = fit_weighted_hc3(X1, y1, w1)

    rows = []
    for label, fit in [("ITorg = 0 (no IT organization)", fit0),
                       ("ITorg = 1 (with IT organization)", fit1)]:
        b, se = fit.params["ai_use_sum"], fit.bse["ai_use_sum"]
        rows.append({"Condition": label, "Simple slope (beta_AI)": round(b, 4),
                     "HC3 SE": round(se, 4), "t": round(fit.tvalues["ai_use_sum"], 3),
                     "p-value": round(fit.pvalues["ai_use_sum"], 4),
                     "95% CI lower": round(b - 1.96 * se, 4),
                     "95% CI upper": round(b + 1.96 * se, 4)})
    bi, sei = fit0.params["ai_x_itorg"], fit0.bse["ai_x_itorg"]
    rows.append({"Condition": "Slope difference (AI x ITorg interaction)",
                 "Simple slope (beta_AI)": round(bi, 4), "HC3 SE": round(sei, 4),
                 "t": round(fit0.tvalues["ai_x_itorg"], 3),
                 "p-value": round(fit0.pvalues["ai_x_itorg"], 4),
                 "95% CI lower": round(bi - 1.96 * sei, 4),
                 "95% CI upper": round(bi + 1.96 * sei, 4)})
    return pd.DataFrame(rows)


def predicted_with_ci(fit, X, ai_grid, itorg_value):
    mean_row = X.mean(axis=0).to_dict()
    rows = []
    for ai in ai_grid:
        row = dict(mean_row)
        row["ai_use_sum"] = ai
        row["it_org_any"] = float(itorg_value)
        row["ai_x_itorg"] = ai * itorg_value      # the only ai-bearing interaction
        rows.append(row)
    Xnew = pd.DataFrame(rows)[X.columns]
    yhat = fit.predict(Xnew)
    L = Xnew.values
    se = np.sqrt(np.einsum("ij,jk,ik->i", L, fit.cov_params().values, L))
    return pd.DataFrame({"ai_use_sum": ai_grid, "yhat": yhat.values,
                         "lo95": yhat.values - 1.96 * se, "hi95": yhat.values + 1.96 * se})


def draw_figure1(df, out_png, out_pdf):
    X, y, w = build_design(df, itorg_flip=False)
    fit = fit_weighted_hc3(X, y, w)
    ai_grid = np.linspace(0, 9, 91)
    p0 = predicted_with_ci(fit, X, ai_grid, 0)
    p1 = predicted_with_ci(fit, X, ai_grid, 1)
    fig, ax = plt.subplots(figsize=(6.5, 4.3), dpi=300)
    ax.plot(p0["ai_use_sum"], p0["yhat"], color="#C44E52", lw=2.0, label="No IT organization")
    ax.fill_between(p0["ai_use_sum"], p0["lo95"], p0["hi95"], color="#C44E52", alpha=0.18, lw=0)
    ax.plot(p1["ai_use_sum"], p1["yhat"], color="#4C72B0", lw=2.0, label="With IT organization")
    ax.fill_between(p1["ai_use_sum"], p1["lo95"], p1["hi95"], color="#4C72B0", alpha=0.18, lw=0)
    ax.set_xlabel("AI use breadth (count of AI application types)")
    ax.set_ylabel("Predicted perceived process improvement (1-5)")
    ax.set_xlim(0, 9); ax.set_ylim(3.4, 4.6)
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25, lw=0.5)
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)


def main():
    df = load_data(DATA_PATH)
    tbl = simple_slope_table(df)
    print("\n=== Simple-slope test (headline Model 5; matches Table 3) ===\n")
    print(tbl.to_string(index=False))
    tbl.to_csv(OUTPUT_DIR / "simple_slopes_table.csv", index=False)
    draw_figure1(df, OUTPUT_DIR / "figure1_ai_itorg.png", OUTPUT_DIR / "figure1_ai_itorg.pdf")
    print(f"\nFigure 1 saved to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
