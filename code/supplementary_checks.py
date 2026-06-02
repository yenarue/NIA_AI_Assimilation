"""
supplementary_checks.py
================================================================================
Reproduces the supplementary diagnostics added in manuscript rev11:
  (1) Harman's single-factor test (common-method-variance diagnostic)
  (2) Practical effect-size contrasts from the headline Model 5
  (3) AI x IT-organisation interaction with firm size entered as CATEGORICAL
      (rules out a firm-size-proxy explanation for the AI use-breadth count)

All estimates use the same canonical data and weighting as reproduce_all_tables.py.
================================================================================
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

DATA_PATH = Path("working/analysis/nia_2024_analysis_total.csv")  # <-- adjust
df = pd.read_csv(DATA_PATH)

FE = "C(industry) + C(region) + C(firm_type)"
RHS = f"ai_use_sum + it_org_any + ai_use_sum:it_org_any + dmi + it_invest_sum + firm_size + {FE}"


# (1) Harman's single-factor test ------------------------------------------------
effect_items = [c for c in ["effect_proc_improve", "effect_innov_outcome",
                            "effect_decision_improve", "effect_competitiveness",
                            "effect_stakeholders", "effect_hr_change",
                            "effect_cost_reduce", "effect_new_business"] if c in df.columns]
harman_vars = effect_items + ["ai_use_sum", "it_org_any", "dmi", "it_invest_sum"]
H = df[harman_vars].dropna()
Z = (H - H.mean()) / H.std(ddof=0)
# unrotated PCA: share of variance from the first component
u, s, vt = np.linalg.svd(Z.values, full_matrices=False)
var = s**2
first_factor_pct = 100 * var[0] / var.sum()
print("=== (1) Harman single-factor test ===")
print("items entered:", harman_vars)
print(f"variance explained by first unrotated factor: {first_factor_pct:.1f}%  "
      f"(threshold of concern = 50%)")


# (2) Practical effect-size contrasts -------------------------------------------
m = smf.wls("effect_proc_improve ~ " + RHS, data=df, weights=df["weight"]).fit(cov_type="HC3")
lo, hi = 1, 6  # low vs high AI use breadth (hi ~ 90th percentile of users)
base = {"dmi": df.dmi.mean(), "it_invest_sum": df.it_invest_sum.mean(),
        "firm_size": df.firm_size.mean(),
        "industry": int(df.industry.mode()[0]), "region": int(df.region.mode()[0]),
        "firm_type": int(df.firm_type.mode()[0])}

def yhat(ai, itorg):
    row = dict(base); row["ai_use_sum"] = ai; row["it_org_any"] = itorg
    return float(m.predict(pd.DataFrame([row]))[0])

print("\n=== (2) Predicted perceived process improvement (1-5), covariates at mean ===")
print(f"AI breadth = {hi} (high):  ITorg=0 -> {yhat(hi,0):.3f} ;  ITorg=1 -> {yhat(hi,1):.3f}"
      f"  (gap = {yhat(hi,1)-yhat(hi,0):+.3f})")
print(f"AI breadth = {lo} (low) :  ITorg=0 -> {yhat(lo,0):.3f} ;  ITorg=1 -> {yhat(lo,1):.3f}"
      f"  (gap = {yhat(lo,1)-yhat(lo,0):+.3f})")
print(f"Change low->high within ITorg=0: {yhat(hi,0)-yhat(lo,0):+.3f}")
print(f"Change low->high within ITorg=1: {yhat(hi,1)-yhat(lo,1):+.3f}")


# (3) Firm size as CATEGORICAL --------------------------------------------------
RHS_cat = f"ai_use_sum + it_org_any + ai_use_sum:it_org_any + dmi + it_invest_sum + C(firm_size) + {FE}"
mc = smf.wls("effect_proc_improve ~ " + RHS_cat, data=df, weights=df["weight"]).fit(cov_type="HC3")
b = mc.params["ai_use_sum:it_org_any"]; se = mc.bse["ai_use_sum:it_org_any"]; p = mc.pvalues["ai_use_sum:it_org_any"]
print("\n=== (3) AI x ITorg interaction with firm size as categorical dummies ===")
print(f"beta = {b:+.3f}  (SE {se:.3f}, p = {p:.4f}, N = {int(mc.nobs)})")
