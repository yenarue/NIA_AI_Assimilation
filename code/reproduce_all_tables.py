"""
reproduce_all_tables.py
================================================================================
Single source of truth for the IMDS manuscript's quantitative results.

ONE canonical specification is used everywhere so that Table 3, the section-4.2
simple slopes, Figure 1, the alternative-outcome table and the subgroup table
are mutually consistent and reproduce to the third decimal.

Canonical headline specification (Model 5)
------------------------------------------
    effect_proc_improve ~ ai_use_sum
                        + it_org_any
                        + ai_use_sum:it_org_any
                        + dmi
                        + it_invest_sum
                        + firm_size                       # LINEAR, not C()
                        + C(industry) + C(region) + C(firm_type)
    estimator : WLS, weights = weight (NIA RIM_WT)
    cov_type  : HC3

Design decisions (relative to v1):
  * Model 5 is WEIGHTED (v1's headline was unweighted).
  * The ai_use_sum:dmi interaction is NOT in the headline model; DMI is treated
    as a readiness condition (main effect only). AI x DMI is reported separately
    as an exploratory robustness row, never inside the headline simple slopes.
  * firm_size enters linearly (one coefficient), matching Table 3's single
    "Firm size category" row.

This is what makes Table 3, 4.2 and Figure 1 agree. v1 differs because it was
unweighted AND carried ai_use_sum:dmi in Model 5; that is the entire source of
the v1 -> rev6 number change (the change-log note "Table 3 unchanged from v1"
referred only to the qualitative sign pattern, not the point estimates).
================================================================================
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA_PATH = Path("working/analysis/nia_2024_analysis_total.csv")  # <-- adjust
OUT = Path("outputs/w13/canonical"); OUT.mkdir(parents=True, exist_ok=True)

FE = "C(industry) + C(region) + C(firm_type)"
RHS_FULL = f"ai_use_sum + it_org_any + ai_use_sum:it_org_any + dmi + it_invest_sum + firm_size + {FE}"


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "+" if p < .10 else ""


def wls(formula, df):
    return smf.wls(formula, data=df, weights=df["weight"]).fit(cov_type="HC3")


def cell(m, term):
    if term not in m.params.index:
        return ""
    return f"{m.params[term]:+.3f}{stars(m.pvalues[term])} ({m.bse[term]:.3f})"


def table3(df):
    """Nested M1-M5; M1-M4 unweighted baselines, M5 weighted headline."""
    specs = {
        "M1 AI only":       ("effect_proc_improve ~ ai_use_sum + firm_size + " + FE, False),
        "M2 +ITorg":        ("effect_proc_improve ~ ai_use_sum + it_org_any + ai_use_sum:it_org_any + firm_size + " + FE, False),
        "M3 +investment":   ("effect_proc_improve ~ ai_use_sum + it_org_any + ai_use_sum:it_org_any + it_invest_sum + firm_size + " + FE, False),
        "M4 +DMI":          ("effect_proc_improve ~ " + RHS_FULL, False),
        "M5 weighted":      ("effect_proc_improve ~ " + RHS_FULL, True),
    }
    terms = ["ai_use_sum", "it_org_any", "ai_use_sum:it_org_any", "dmi", "it_invest_sum", "firm_size"]
    rows = {t: {} for t in terms}; r2 = {}; n = {}
    for name, (f, w) in specs.items():
        m = wls(f, df) if w else smf.ols(f, data=df).fit(cov_type="HC3")
        for t in terms:
            rows[t][name] = cell(m, t)
        r2[name] = round(m.rsquared, 3); n[name] = int(m.nobs)
    out = pd.DataFrame(rows).T
    out.loc["R-squared"] = r2; out.loc["N"] = n
    return out


def simple_slopes(df):
    m0 = wls("effect_proc_improve ~ " + RHS_FULL, df)
    d = df.copy(); d["it_org_any"] = 1 - d["it_org_any"]
    m1 = wls("effect_proc_improve ~ " + RHS_FULL, d)
    rows = []
    for lab, m in [("ITorg=0", m0), ("ITorg=1", m1)]:
        b, se = m.params["ai_use_sum"], m.bse["ai_use_sum"]
        rows.append(dict(Condition=lab, beta=round(b, 4), SE=round(se, 4),
                         t=round(m.tvalues["ai_use_sum"], 3), p=round(m.pvalues["ai_use_sum"], 4)))
    bi = "ai_use_sum:it_org_any"
    rows.append(dict(Condition="AIxITorg interaction", beta=round(m0.params[bi], 4),
                     SE=round(m0.bse[bi], 4), t=round(m0.tvalues[bi], 3), p=round(m0.pvalues[bi], 4)))
    return pd.DataFrame(rows)


def alt_outcomes(df):
    dvs = {"effect_average": "Average effect", "effect_innov_outcome": "Product/service innovation",
           "effect_decision_improve": "Decision-making", "effect_competitiveness": "Competitiveness",
           "effect_stakeholders": "External stakeholders"}
    rows = []
    for dv, lab in dvs.items():
        m = wls(f"{dv} ~ " + RHS_FULL, df)
        rows.append(dict(Outcome=lab, AI=cell(m, "ai_use_sum"),
                         AIxITorg=cell(m, "ai_use_sum:it_org_any"),
                         DMI=cell(m, "dmi"), N=int(m.nobs), R2=round(m.rsquared, 3)))
    return pd.DataFrame(rows)


def subgroups(df):
    rows = []
    service_industries = [11, 12, 13, 14, 15]

    def add(name, sub, fe=FE):
        rhs = f"ai_use_sum + it_org_any + ai_use_sum:it_org_any + dmi + it_invest_sum + firm_size + {fe}"
        m = wls("effect_proc_improve ~ " + rhs, sub)
        rows.append(dict(Subgroup=name, N=int(m.nobs), AI=cell(m, "ai_use_sum"),
                         AIxITorg=cell(m, "ai_use_sum:it_org_any")))
    add("Large (firm_size>=3)", df[df.firm_size >= 3])
    add("SME (firm_size<=2)",   df[df.firm_size <= 2])
    add("Information (industry=8)",        df[df.industry == 8], fe="C(region) + C(firm_type)")
    add("Manufacturing (industry=2)",        df[df.industry == 2], fe="C(region) + C(firm_type)")
    add("Other (industry=16)",        df[df.industry == 16], fe="C(region) + C(firm_type)")
    add("Services (industry=11,12,13,14,15)",        df[df.industry.isin(service_industries)], fe="C(region) + C(firm_type)")
    add("Services - 전문,과학 및 기술서비스업 (industry=11)",        df[df.industry == 11], fe="C(region) + C(firm_type)")
    add("Services - 사업시설관리, 사업지원 및 서비스업 (industry=12)",        df[df.industry == 12], fe="C(region) + C(firm_type)")
    add("Services - 교육 서비스업 (industry=13)",        df[df.industry == 13], fe="C(region) + C(firm_type)")
    add("Services - 보건업 및 사회복지서비스업 (industry=14)",        df[df.industry == 14], fe="C(region) + C(firm_type)")
    add("Services - 예술, 스포츠 및 여가관련 서비스업 (industry=15)",        df[df.industry == 15], fe="C(region) + C(firm_type)")
    return pd.DataFrame(rows)


def main():
    df = pd.read_csv(DATA_PATH)
    t3, ss, t4, sg = table3(df), simple_slopes(df), alt_outcomes(df), subgroups(df)
    for name, tbl in [("table3_main", t3), ("simple_slopes", ss),
                      ("table4_alt_outcomes", t4), ("table6_subgroup", sg)]:
        print(f"\n===== {name} =====")
        print(tbl.to_string())
        tbl.to_csv(OUT / f"{name}.csv")
    print(f"\nAll tables written to {OUT.resolve()}")


if __name__ == "__main__":
    main()
