"""
reproduce_all_tables.py
================================================================================
Single source of truth for the IMDS manuscript's quantitative results
(rev10 replication package).

ONE canonical specification is used everywhere so that Table 3, the section-4.2
simple slopes, Figure 1, the alternative-outcome table (Table 4), the subgroup
table (Table 6) and the AI-type decomposition (Table 7) are mutually consistent
and reproduce to the third decimal.

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

Design decisions:
  * Model 5 is WEIGHTED.
  * The ai_use_sum:dmi interaction is NOT in the headline model; DMI is treated
    as a readiness condition (main effect only). AI x DMI is reported ONLY as an
    exploratory row in the comprehensive robustness table (manuscript Table 5),
    never in Table 3, Table 4, Table 6 or Table 7.
  * firm_size enters linearly (one coefficient).

Table 6 industry-group definition (KSIC 16-sector scheme, exhaustive 4-way split)
---------------------------------------------------------------------------------
    Manufacturing  : industry == 2                                  (N = 2,769)
    Information    : industry == 8                                  (N =   785)
    Services       : industry in {5,6,7,9,10,11,12,13,14,15,16}     (N = 6,441)
    Other          : industry in {1,3,4}                            (N = 2,208)
  Single-industry groups (Manufacturing, Information) use region + firm-type
  fixed effects only; multi-industry groups (Services, Other) additionally
  include industry fixed effects. This is the exact grouping behind the
  manuscript's Table 6 numbers.
================================================================================
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA_PATH = Path("working/analysis/nia_2024_analysis_total.csv")  # <-- adjust
OUT = Path("outputs/w14/canonical"); OUT.mkdir(parents=True, exist_ok=True)

FE = "C(industry) + C(region) + C(firm_type)"
RHS_FULL = f"ai_use_sum + it_org_any + ai_use_sum:it_org_any + dmi + it_invest_sum + firm_size + {FE}"

# Exhaustive 4-way industry partition used in manuscript Table 6
INDUSTRY_GROUPS = {
    "Manufacturing": [2],
    "Information":    [8],
    "Services":       [5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16],
    "Other":          [1, 3, 4],
}

AI_TYPE_LABELS = {
    "ai_use_doc_info_collect": "Document creation and information retrieval",
    "ai_use_task_automation": "Task automation support",
    "ai_use_decision_support": "Decision support",
    "ai_use_speech_to_text": "Speech-to-machine-readable conversion (STT)",
    "ai_use_gen_summarize_edit": "Generative AI (text / image / audio)",
    "ai_use_image_video_recognition": "Computer vision (object / person identification)",
    "ai_use_ml_data_analysis": "Machine learning for data analytics",
    "ai_use_text_language_analysis": "Natural language processing (text analysis)",
    "ai_use_autonomous_mobility": "Autonomous mobility AI (autonomous vehicles / robotics)",
    "ai_use_other": "Other AI applications",
}


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else "+" if p < .10 else ""


def wls(formula, df):
    return smf.wls(formula, data=df, weights=df["weight"]).fit(cov_type="HC3")


def cell(m, term):
    if term not in m.params.index:
        return ""
    return f"{m.params[term]:+.3f}{stars(m.pvalues[term])} ({m.bse[term]:.3f})"


def linear_combo_stats(m, terms, weights=None):
    if weights is None:
        weights = [1.0] * len(terms)
    contrast = np.zeros(len(m.params))
    for term, weight in zip(terms, weights):
        contrast[m.params.index.get_loc(term)] = weight
    test = m.t_test(contrast)
    beta = float(np.squeeze(test.effect))
    se = float(np.squeeze(test.sd))
    t = float(np.squeeze(test.tvalue))
    p = float(np.squeeze(test.pvalue))
    return beta, se, t, p


def table3(df):
    """Nested M1-M5; M1-M4 unweighted baselines, M5 weighted headline."""
    specs = {
        "M1 AI only":     ("effect_proc_improve ~ ai_use_sum + firm_size + " + FE, False),
        "M2 +ITorg":      ("effect_proc_improve ~ ai_use_sum + it_org_any + ai_use_sum:it_org_any + firm_size + " + FE, False),
        "M3 +investment": ("effect_proc_improve ~ ai_use_sum + it_org_any + ai_use_sum:it_org_any + it_invest_sum + firm_size + " + FE, False),
        "M4 +DMI":        ("effect_proc_improve ~ " + RHS_FULL, False),
        "M5 weighted":    ("effect_proc_improve ~ " + RHS_FULL, True),
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
    """Table 4. Headline spec on alternative DVs. NO AI x DMI column (by design)."""
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
    """Table 6 heterogeneity. Exhaustive firm-size and industry partitions."""
    rows = []

    def add(split, group, sub, fe):
        rhs = f"ai_use_sum + it_org_any + ai_use_sum:it_org_any + dmi + it_invest_sum + firm_size + {fe}"
        m = wls("effect_proc_improve ~ " + rhs, sub)
        rows.append(dict(Split=split, Group=group, N=int(m.nobs),
                         AI=cell(m, "ai_use_sum"), AIxITorg=cell(m, "ai_use_sum:it_org_any")))

    # Firm-size split
    add("firm_large", "Large_250plus", df[df.firm_size >= 3], "C(industry) + C(region) + C(firm_type)")
    add("firm_large", "SME_10_249",    df[df.firm_size <= 2], "C(industry) + C(region) + C(firm_type)")

    # Industry split (exhaustive 4-way). Industry FE only when group spans >1 code.
    base = "C(region) + C(firm_type)"
    for group in ["Information", "Manufacturing", "Other", "Services"]:
        codes = INDUSTRY_GROUPS[group]
        fe = ("C(industry) + " + base) if len(codes) > 1 else base
        add("industry_group", group, df[df.industry.isin(codes)], fe)
    return pd.DataFrame(rows)


def table7_ai_type_decomposition(df):
    rows = []
    n_total = int(len(df))
    for ai_col, label in AI_TYPE_LABELS.items():
        if ai_col not in df.columns:
            continue
        formula = (
            f"effect_proc_improve ~ {ai_col} + it_org_any + {ai_col}:it_org_any "
            f"+ dmi + it_invest_sum + firm_size + {FE}"
        )
        m = wls(formula, df)
        interaction = f"{ai_col}:it_org_any"
        slope_beta, slope_se, _, slope_p = linear_combo_stats(m, [ai_col, interaction])
        rows.append({
            "AI type": label,
            "Q28 item": ai_col,
            "Prevalence (%)": round(100 * df[ai_col].mean(), 1),
            "N": n_total,
            "beta_AI alone": cell(m, ai_col),
            "beta_AI x ITorg": cell(m, interaction),
            "Simple slope at ITorg=1": f"{slope_beta:+.3f}{stars(slope_p)} ({slope_se:.3f})",
            "R-squared": round(m.rsquared, 3),
        })
    return pd.DataFrame(rows)


def main():
    df = pd.read_csv(DATA_PATH)
    tables = [
        ("table3_main", table3(df)),
        ("simple_slopes", simple_slopes(df)),
        ("table4_alt_outcomes", alt_outcomes(df)),
        ("table6_subgroup", subgroups(df)),
        ("table7_ai_type_decomposition", table7_ai_type_decomposition(df)),
    ]
    for name, tbl in tables:
        print(f"\n===== {name} =====")
        print(tbl.to_string())
        tbl.to_csv(OUT / f"{name}.csv", index=False)
    print(f"\nAll tables written to {OUT.resolve()}")


if __name__ == "__main__":
    main()
