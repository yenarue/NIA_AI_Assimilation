# IMDS manuscript — analysis replication package (w13)

This package reproduces every quantitative result in the manuscript
(`yena_imds_main_rev10`) from a single canonical specification. Running the two
scripts below regenerates Table 3, the §4.2 simple slopes, Figure 1, Table 4,
Table 6, and Table 7, all mutually consistent to the third decimal.

## Canonical headline specification (Model 5)

    effect_proc_improve ~ ai_use_sum
                        + it_org_any
                        + ai_use_sum:it_org_any
                        + dmi
                        + it_invest_sum
                        + firm_size                  # LINEAR, not C()
                        + C(industry) + C(region) + C(firm_type)
    estimator : WLS, weights = weight (NIA RIM_WT)
    cov_type  : HC3

Two design rules are load-bearing and used everywhere:
- `ai_use_sum:dmi` is **not** in the headline model. DMI is a readiness
  condition (main effect only). AI × DMI is reported only as an exploratory row
  in the manuscript's Table 5, never in Table 3, 4, 6 or 7.
- `firm_size` enters linearly (one coefficient).

## What changed from the previous version of `reproduce_all_tables.py`

Only `subgroups()` (manuscript Table 6) changed. The previous version defined
the industry groups with the wrong codes — `Other = industry 16` and
`Services = industry 11–15` — which do **not** reproduce the manuscript numbers
and left ~5,000 firms unassigned. The manuscript uses an **exhaustive four-way
partition of the 16-sector KSIC scheme**:

| Group         | KSIC industry codes                      | N      |
| ------------- | ---------------------------------------- | ------ |
| Manufacturing | 2                                        | 2,769  |
| Information   | 8                                        | 785    |
| Services      | 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16   | 6,441  |
| Other         | 1, 3, 4                                  | 2,208  |

(Services = wholesale/retail, transport, accommodation/food, finance, real
estate, and professional / business-support / education / health / arts-leisure
/ personal services. Other = agriculture-mining, utilities/recycling,
construction.)

Single-industry groups (Manufacturing, Information) use region + firm-type
fixed effects only; multi-sector groups (Services, Other) additionally include
industry fixed effects. With this definition all six Table 6 rows reproduce
exactly. The same definition is documented in the Note under Table 6 in the
manuscript.

`simple_slopes_and_figure.py` is unchanged and already matches the canonical
spec.

## Files

| File                          | Produces                                            |
| ----------------------------- | --------------------------------------------------- |
| `reproduce_all_tables.py`     | Table 3, simple slopes, Table 4, Table 6, Table 7   |
| `simple_slopes_and_figure.py` | §4.2 simple-slope table + Figure 1 (PNG/PDF)        |
| `outputs/canonical/`          | CSV outputs of `reproduce_all_tables.py`            |
| `outputs/simple_slopes/`      | simple-slope CSV + Figure 1                         |

## How to run

1. Put the analysis dataset at `working/analysis/nia_2024_analysis_total.csv`
   (or edit `DATA_PATH` at the top of each script).
2. From the repository root:

   ```bash
   python reproduce_all_tables.py
   python simple_slopes_and_figure.py
   ```

3. Requirements: `pandas`, `numpy`, `statsmodels`, and `matplotlib`
   (figure only).

## Reference values (for self-check)

Simple slopes (§4.2): ITorg=0 β = −0.025 (SE 0.012, p = .034); ITorg=1
β = +0.026 (SE 0.012, p = .029); interaction β = +0.051 (p = .001).

## rev11 supplementary diagnostics

`supplementary_checks.py` reproduces three diagnostics added to the manuscript
in rev11 (text only; no table changes):

- **Harman single-factor test** (common-method-variance): first unrotated factor
  explains 42.6% of variance, below the 50% threshold of concern.
- **Practical effect-size contrasts** from the headline Model 5: at three AI
  application types the IT-organisation gap in predicted process improvement is
  ~0.12 points (~0.16 SD); across the full range (up to nine) it widens to ~0.43
  points (~0.56 SD); the groups are indistinguishable at zero breadth.
- **Firm-size as categorical**: the AI × IT-organisation interaction is unchanged
  (β = +0.051, SE = 0.015, p = .001), so AI use breadth is not a firm-size proxy.

Run with: `python supplementary_checks.py`
