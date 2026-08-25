#!/usr/bin/env python3
"""Paper builder for paper 18 (Applied Econometrics)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table, render_math_table,
    PAPER_BUILDERS,
)

# ═══════════════════════════════════════════════════════════════════════════
# Paper 18: Applied Econometrics (Imbens-Angrist LATE / MTE style)
# ═══════════════════════════════════════════════════════════════════════════

def _paper_18_applied_econometrics() -> PaperSpec:
    """Paper 18: Applied Econometrics -- LATE and MTE identification."""

    # ── Tables ──

    tab_mc_late_consist = render_regression_table({
        "table_id": "monte-carlo-late-consistency",
        "caption": "Monte Carlo: Consistency of LATE Estimators (N = 1,000 replications)",
        "label": "tab:monte-carlo-late-consistency",
        "model_labels": ["n=200", "n=500", "n=1000", "n=5000"],
        "panels": [
            {
                "label": "Panel A: Bias (true LATE = 1.000)",
                "variables": [
                    {"label": "Wald / 2SLS",
                     "coefficients": ["-0.042", "-0.017", "-0.009", "-0.002"]},
                    {"label": "Control function (bilinear)",
                     "coefficients": ["-0.038", "-0.015", "-0.007", "-0.001"]},
                    {"label": "LIML",
                     "coefficients": ["-0.011", "-0.004", "-0.002", "0.001"]},
                    {"label": "OLS (biased benchmark)",
                     "coefficients": ["0.312", "0.318", "0.321", "0.319"]},
                ],
            },
            {
                "label": "Panel B: RMSE",
                "variables": [
                    {"label": "Wald / 2SLS",
                     "coefficients": ["0.241", "0.148", "0.104", "0.046"]},
                    {"label": "Control function (bilinear)",
                     "coefficients": ["0.228", "0.141", "0.099", "0.044"]},
                    {"label": "LIML",
                     "coefficients": ["0.219", "0.136", "0.097", "0.043"]},
                    {"label": "OLS (biased benchmark)",
                     "coefficients": ["0.318", "0.319", "0.321", "0.319"]},
                ],
            },
        ],
        "notes": "DGP: binary instrument, binary treatment, continuous outcome. Compliance rate = 0.40. Selection on unobservables: rho = 0.50. True LATE = 1.000 by construction. All IV estimators use the single binary instrument.",
        "qa": [
            {"question": "What is the true LATE in the Monte Carlo DGP?", "answer": "1.000"},
            {"question": "Does 2SLS bias shrink as sample size grows?", "answer": "Yes, from -0.042 to -0.002"},
            {"question": "What is the OLS bias approximately?", "answer": "0.319 (substantial positive bias from selection)"},
            {"question": "Which estimator has the smallest RMSE at n=1000?", "answer": "LIML (0.097)"},
        ],
    })

    tab_mc_late_cov = render_regression_table({
        "table_id": "monte-carlo-late-coverage",
        "caption": "Monte Carlo: Coverage Rates of 95\\% Confidence Intervals for LATE",
        "label": "tab:monte-carlo-late-coverage",
        "model_labels": ["n=200", "n=500", "n=1000", "n=5000"],
        "panels": [
            {
                "label": "Panel A: Standard (asymptotic) confidence intervals",
                "variables": [
                    {"label": "2SLS (asymptotic SE)", "coefficients": ["0.906", "0.928", "0.938", "0.947"]},
                    {"label": "2SLS (heteroskedastic-robust SE)", "coefficients": ["0.912", "0.934", "0.942", "0.949"]},
                    {"label": "LIML (asymptotic SE)", "coefficients": ["0.931", "0.941", "0.946", "0.950"]},
                ],
            },
            {
                "label": "Panel B: Bootstrap confidence intervals (999 replications)",
                "variables": [
                    {"label": "2SLS (percentile bootstrap)", "coefficients": ["0.921", "0.938", "0.944", "0.950"]},
                    {"label": "2SLS (BC bootstrap)", "coefficients": ["0.934", "0.944", "0.948", "0.951"]},
                    {"label": "Anderson-Rubin (weak-IV robust)", "coefficients": ["0.948", "0.950", "0.950", "0.950"]},
                ],
            },
        ],
        "notes": "Coverage rates across 1,000 Monte Carlo replications. Nominal coverage = 0.95. DGP identical to Table~\\ref{tab:monte-carlo-late-consistency}. BC = bias-corrected bootstrap. Anderson-Rubin CI is exact under the null regardless of instrument strength.",
        "qa": [
            {"question": "Which confidence interval achieves exact nominal coverage?", "answer": "Anderson-Rubin (weak-IV robust) CI achieves 0.950 at all sample sizes"},
            {"question": "Does asymptotic 2SLS CI under-cover at n=200?", "answer": "Yes, coverage is 0.906 vs nominal 0.950"},
        ],
    })

    tab_mc_mte = render_regression_table({
        "table_id": "monte-carlo-mte",
        "caption": "Monte Carlo: MTE Estimation -- RMSE and Bias by Propensity Score Percentile",
        "label": "tab:monte-carlo-mte",
        "model_labels": ["p10-p20", "p30-p40", "p50-p60", "p70-p80", "p80-p90"],
        "panels": [
            {
                "label": "Panel A: Bias (true MTE by cell)",
                "variables": [
                    {"label": "Local IV (Heckman-Vytlacil)",
                     "coefficients": ["-0.082", "-0.041", "-0.018", "-0.037", "-0.091"]},
                    {"label": "Polynomial series (degree 3)",
                     "coefficients": ["-0.064", "-0.029", "-0.011", "-0.028", "-0.071"]},
                    {"label": "Local polynomial (bw = 0.15)",
                     "coefficients": ["-0.071", "-0.033", "-0.014", "-0.031", "-0.078"]},
                ],
            },
            {
                "label": "Panel B: RMSE",
                "variables": [
                    {"label": "Local IV (Heckman-Vytlacil)",
                     "coefficients": ["0.198", "0.142", "0.118", "0.147", "0.211"]},
                    {"label": "Polynomial series (degree 3)",
                     "coefficients": ["0.167", "0.121", "0.101", "0.127", "0.182"]},
                    {"label": "Local polynomial (bw = 0.15)",
                     "coefficients": ["0.183", "0.133", "0.110", "0.138", "0.196"]},
                ],
            },
        ],
        "notes": "n = 2,000. 500 replications. True MTE is decreasing in the propensity score: MTE(u) = 2.0 - 2.0u. Cells defined by propensity score percentile intervals. Boundary cells (p10-p20, p80-p90) exhibit larger bias due to boundary effects in local estimation.",
        "qa": [
            {"question": "Why is MTE estimation less precise at the boundaries?", "answer": "Boundary effects in local estimation lead to larger bias and RMSE at extreme propensity score values"},
            {"question": "What estimator has the smallest RMSE at the median propensity score?", "answer": "Polynomial series (degree 3) with RMSE 0.101"},
        ],
    })

    tab_wald = render_regression_table({
        "table_id": "wald-estimates",
        "caption": "Wald Estimates by Instrument",
        "label": "tab:wald-estimates",
        "model_labels": ["Instrument 1", "Instrument 2", "Instrument 3", "Joint"],
        "panels": [
            {
                "dep_var": "Dep. var.: Outcome Y",
                "variables": [
                    {"label": "Wald estimate (LATE)",
                     "coefficients": ["1.42***", "1.31***", "1.38***", "1.36***"],
                     "std_errors": ["(0.28)", "(0.31)", "(0.34)", "(0.18)"]},
                    {"label": "First-stage coefficient",
                     "coefficients": ["0.41***", "0.35***", "0.28***", ""],
                     "std_errors": ["(0.04)", "(0.04)", "(0.05)", ""]},
                    {"label": "Reduced-form coefficient",
                     "coefficients": ["0.58***", "0.46***", "0.39***", ""],
                     "std_errors": ["(0.11)", "(0.12)", "(0.14)", ""]},
                ],
            },
        ],
        "summary": [
            {"label": "First-stage F", "values": ["104.2", "76.8", "31.4", ""]},
            {"label": "Observations", "values": ["8,412", "8,412", "8,412", "8,412"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Each column uses a single instrument to form a Wald estimate. Joint uses all three instruments in 2SLS. Instruments are randomly assigned encouragement doses in a field experiment.",
        "qa": [
            {"question": "What is the Wald estimate using Instrument 1?", "answer": "1.42"},
            {"question": "Are the three Wald estimates statistically distinguishable?", "answer": "No, all three overlap within standard errors, suggesting consistent treatment effects across subgroups"},
            {"question": "What is the first-stage F-statistic for Instrument 3?", "answer": "31.4"},
        ],
    })

    tab_2sls = render_regression_table({
        "table_id": "two-stage-estimates",
        "caption": "Two-Stage Least Squares Estimates",
        "label": "tab:two-stage-estimates",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "label": "Panel A: Second Stage",
                "dep_var": "Dep. var.: Outcome Y",
                "variables": [
                    {"label": "Treatment D",
                     "coefficients": ["1.36***", "1.31***", "1.28***", "1.24***"],
                     "std_errors": ["(0.18)", "(0.17)", "(0.16)", "(0.16)"]},
                    {"label": "Age", "coefficients": ["", "0.02**", "0.02**", "0.02**"],
                     "std_errors": ["", "(0.01)", "(0.01)", "(0.01)"]},
                    {"label": "Female", "coefficients": ["", "-0.14***", "-0.13***", "-0.13***"],
                     "std_errors": ["", "(0.04)", "(0.04)", "(0.04)"]},
                ],
            },
            {
                "label": "Panel B: First Stage",
                "dep_var": "Dep. var.: Treatment D",
                "variables": [
                    {"label": "Instrument Z1",
                     "coefficients": ["0.41***", "0.40***", "0.39***", "0.39***"],
                     "std_errors": ["(0.04)", "(0.04)", "(0.04)", "(0.04)"]},
                    {"label": "Instrument Z2",
                     "coefficients": ["0.35***", "0.34***", "0.34***", "0.33***"],
                     "std_errors": ["(0.04)", "(0.04)", "(0.04)", "(0.04)"]},
                    {"label": "Instrument Z3",
                     "coefficients": ["0.28***", "0.27***", "0.27***", "0.27***"],
                     "std_errors": ["(0.05)", "(0.05)", "(0.05)", "(0.05)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Demographic controls", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Site FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Cohort FE", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["8,412", "8,412", "8,412", "8,412"]},
            {"label": "First-stage F (joint)", "values": ["104.2", "98.7", "91.3", "89.4"]},
            {"label": "Hansen J p-value", "values": ["0.84", "0.81", "0.79", "0.77"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered by site. Hansen J p-values indicate failure to reject the null of instrument validity.",
        "qa": [
            {"question": "What is the 2SLS estimate in the most saturated specification (column 4)?", "answer": "1.24"},
            {"question": "Is the overidentification test rejected?", "answer": "No, Hansen J p-value is 0.77 in column 4"},
            {"question": "Does adding fixed effects substantially change the treatment effect estimate?", "answer": "No, it moves from 1.36 to 1.24 across columns"},
        ],
    })

    tab_complier = render_math_table({
        "table_id": "complier-characteristics",
        "caption": "Characteristics of Compliers, Always-Takers, and Never-Takers",
        "label": "tab:complier-characteristics",
        "col_headers": [
            {"text": "Complier Mean", "latex": "Complier Mean"},
            {"text": "Always-taker Mean", "latex": "Always-taker Mean"},
            {"text": "Never-taker Mean", "latex": "Never-taker Mean"},
        ],
        "rows": [
            {"label": "Age", "label_latex": "Age",
             "cells": [{"text": "34.2", "latex": "34.2"},
                       {"text": "31.8", "latex": "31.8"},
                       {"text": "38.1", "latex": "38.1"}]},
            {"label": "Female (%)", "label_latex": "Female (\\%)",
             "cells": [{"text": "52.1", "latex": "52.1"},
                       {"text": "48.7", "latex": "48.7"},
                       {"text": "55.3", "latex": "55.3"}]},
            {"label": "Years of schooling", "label_latex": "Years of schooling",
             "cells": [{"text": "12.4", "latex": "12.4"},
                       {"text": "14.2", "latex": "14.2"},
                       {"text": "10.8", "latex": "10.8"}]},
            {"label": "Baseline income (\\$000s)", "label_latex": "Baseline income (\\$000s)",
             "cells": [{"text": "38.7", "latex": "38.7"},
                       {"text": "52.1", "latex": "52.1"},
                       {"text": "28.4", "latex": "28.4"}]},
            {"label": "Prior program participation (%)", "label_latex": "Prior program participation (\\%)",
             "cells": [{"text": "18.3", "latex": "18.3"},
                       {"text": "41.2", "latex": "41.2"},
                       {"text": "9.4", "latex": "9.4"}]},
            {"label": "Share of population", "label_latex": "Share of population",
             "cells": [{"text": "0.40", "latex": "0.40"},
                       {"text": "0.22", "latex": "0.22"},
                       {"text": "0.38", "latex": "0.38"}]},
        ],
        "qa": [
            {"question": "What share of the population are compliers?", "answer": "0.40 (40%)"},
            {"question": "Are compliers higher or lower income than always-takers?", "answer": "Lower: complier mean income $38.7k vs always-taker $52.1k"},
            {"question": "Which type has the highest prior program participation?", "answer": "Always-takers (41.2%)"},
        ],
    })

    tab_mte_prop = render_regression_table({
        "table_id": "mte-by-propensity",
        "caption": "Marginal Treatment Effects by Propensity Score Decile",
        "label": "tab:mte-by-propensity",
        "model_labels": ["MTE", "95\\% CI Low", "95\\% CI High", "IV Weight"],
        "panels": [
            {
                "variables": [
                    {"label": "Decile 1 (u = 0.05)", "coefficients": ["2.14***", "1.41", "2.87", "0.031"]},
                    {"label": "Decile 2 (u = 0.15)", "coefficients": ["1.91***", "1.31", "2.51", "0.067"]},
                    {"label": "Decile 3 (u = 0.25)", "coefficients": ["1.72***", "1.21", "2.23", "0.108"]},
                    {"label": "Decile 4 (u = 0.35)", "coefficients": ["1.54***", "1.08", "2.00", "0.141"]},
                    {"label": "Decile 5 (u = 0.45)", "coefficients": ["1.39***", "0.97", "1.81", "0.162"]},
                    {"label": "Decile 6 (u = 0.55)", "coefficients": ["1.21***", "0.81", "1.61", "0.158"]},
                    {"label": "Decile 7 (u = 0.65)", "coefficients": ["1.04***", "0.62", "1.46", "0.138"]},
                    {"label": "Decile 8 (u = 0.75)", "coefficients": ["0.87***", "0.41", "1.33", "0.101"]},
                    {"label": "Decile 9 (u = 0.85)", "coefficients": ["0.68***", "0.14", "1.22", "0.072"]},
                    {"label": "Decile 10 (u = 0.95)", "coefficients": ["0.44*", "-0.18", "1.06", "0.022"]},
                ],
            },
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. MTE estimated via local IV (Heckman-Vytlacil method). IV Weight is the 2SLS weight on each MTE cell under the three instruments. Weights sum to 1.0.",
        "qa": [
            {"question": "Is the MTE increasing or decreasing in the propensity score?", "answer": "Decreasing: from 2.14 at u=0.05 to 0.44 at u=0.95"},
            {"question": "What is the MTE at the median propensity score (u=0.45)?", "answer": "1.39"},
            {"question": "Which decile receives the highest 2SLS weight?", "answer": "Decile 5 (u=0.45) with weight 0.162"},
        ],
    })

    tab_bounds = render_regression_table({
        "table_id": "bounds-no-monotonicity",
        "caption": "Bounds on the Average Treatment Effect Without Monotonicity",
        "label": "tab:bounds-no-monotonicity",
        "model_labels": ["Lower Bound", "Point (LATE)", "Upper Bound", "Bound Width"],
        "panels": [
            {
                "variables": [
                    {"label": "Manski (1990) no-assumptions bounds",
                     "coefficients": ["-8.41", "1.36", "8.41", "16.82"]},
                    {"label": "Monotone treatment response",
                     "coefficients": ["0.00", "1.36", "8.41", "8.41"]},
                    {"label": "Monotone treatment selection",
                     "coefficients": ["-1.84", "1.36", "4.12", "5.96"]},
                    {"label": "MTR + MTS combined",
                     "coefficients": ["0.00", "1.36", "4.12", "4.12"]},
                    {"label": "Machina-Storti (IV bounds)",
                     "coefficients": ["0.78", "1.36", "1.94", "1.16"]},
                    {"label": "Horowitz-Manski (outcome support)",
                     "coefficients": ["0.61", "1.36", "2.11", "1.50"]},
                ],
            },
        ],
        "notes": "Bounds on the ATE for the full population. LATE is the 2SLS point estimate using all three instruments (1.36). MTR = monotone treatment response. MTS = monotone treatment selection. Machina-Storti bounds use the instruments as identifying information. Outcome Y is bounded in [0, 10].",
        "qa": [
            {"question": "What are the Manski no-assumptions bounds?", "answer": "[-8.41, 8.41]"},
            {"question": "What do Machina-Storti IV bounds imply for the ATE?", "answer": "[0.78, 1.94], consistent with the LATE of 1.36"},
            {"question": "Which bound set is tightest?", "answer": "Machina-Storti IV bounds (width 1.16)"},
        ],
    })

    tab_spec_tests = render_regression_table({
        "table_id": "specification-tests",
        "caption": "Specification Tests",
        "label": "tab:specification-tests",
        "model_labels": ["Statistic", "p-value", "Null hypothesis", "Verdict"],
        "panels": [
            {
                "variables": [
                    {"label": "Hansen J (overid.)",
                     "coefficients": ["0.47", "0.79", "Instruments valid", "Fail to reject"]},
                    {"label": "Hausman (OLS vs. 2SLS)",
                     "coefficients": ["18.4", "0.00", "OLS consistent", "Reject"]},
                    {"label": "First-stage F (joint)",
                     "coefficients": ["89.4", "0.00", "Instruments irrelevant", "Reject"]},
                    {"label": "Stock-Yogo 10% maximal bias",
                     "coefficients": ["CV=13.9", "pass", "Weak instruments", "Fail to reject"]},
                    {"label": "Monotonicity (Mourifie-Wan)",
                     "coefficients": ["0.81", "0.47", "Monotonicity violated", "Fail to reject"]},
                    {"label": "LATE = ATE (Vytlacil)",
                     "coefficients": ["1.84", "0.17", "MTE constant", "Fail to reject"]},
                ],
            },
        ],
        "notes": "Hausman test uses robust variance matrix. Stock-Yogo 10\\% maximal bias critical value is 13.9 for 3 instruments; F-stat of 89.4 comfortably exceeds this. Monotonicity test uses the nonparametric test of Mourifie and Wan (2017).",
        "qa": [
            {"question": "Is the OLS estimator rejected as consistent?", "answer": "Yes, Hausman test p-value is 0.00"},
            {"question": "Do the instruments pass the overidentification test?", "answer": "Yes, Hansen J p-value is 0.79"},
            {"question": "Is monotonicity rejected?", "answer": "No, Mourifie-Wan test p-value is 0.47"},
        ],
    })

    tab_appendix_dgp = render_regression_table({
        "table_id": "appendix-dgp",
        "caption": "Appendix: Monte Carlo DGP Specifications",
        "label": "tab:appendix-dgp",
        "model_labels": ["DGP 1", "DGP 2", "DGP 3", "DGP 4"],
        "panels": [
            {
                "variables": [
                    {"label": "True LATE", "coefficients": ["1.00", "1.50", "1.00", "2.00"]},
                    {"label": "True ATE", "coefficients": ["1.20", "1.50", "0.80", "2.00"]},
                    {"label": "Selection (rho)", "coefficients": ["0.50", "0.50", "0.70", "0.00"]},
                    {"label": "Compliance rate", "coefficients": ["0.40", "0.40", "0.25", "0.60"]},
                    {"label": "Instrument strength (E[Z-compliance])", "coefficients": ["0.40", "0.40", "0.25", "0.60"]},
                    {"label": "Outcome variance", "coefficients": ["1.00", "2.25", "1.00", "4.00"]},
                ],
            },
        ],
        "notes": "DGP 1 is the baseline; DGP 2 has a larger effect and more variance; DGP 3 has one-sided noncompliance (low compliance, strong selection); DGP 4 has no selection (rho=0, LATE=ATE).",
        "qa": [
            {"question": "In which DGP is LATE equal to ATE?", "answer": "DGP 2 (LATE = ATE = 1.50) and DGP 4 (LATE = ATE = 2.00)"},
            {"question": "Which DGP has the strongest selection on unobservables?", "answer": "DGP 3 (rho = 0.70)"},
        ],
    })

    # ── Main Equations ──
    eqs_18 = [
        EquationSpec("late-def",
                     r"\text{LATE} = E[Y_{1i} - Y_{0i} \mid D_{1i} > D_{0i}] = \frac{E[Y_i \mid Z_i=1] - E[Y_i \mid Z_i=0]}{E[D_i \mid Z_i=1] - E[D_i \mid Z_i=0]}",
                     "eq:late-def",
                     "LATE definition: average treatment effect for compliers",
                     [{"question": "How is LATE identified from the data?",
                       "answer": "As the ratio of the reduced form to the first stage: (E[Y|Z=1]-E[Y|Z=0])/(E[D|Z=1]-E[D|Z=0])"}]),
        EquationSpec("wald-est",
                     r"\hat{\tau}_{Wald} = \frac{\bar{Y}_1 - \bar{Y}_0}{\bar{D}_1 - \bar{D}_0} = \frac{\hat{\rho}_{YZ}}{\hat{\rho}_{DZ}}",
                     "eq:wald-est",
                     "Wald estimator for LATE with binary instrument",
                     [{"question": "What is the Wald estimator?",
                       "answer": "The ratio of the sample analog of E[Y|Z=1]-E[Y|Z=0] to E[D|Z=1]-E[D|Z=0]"}]),
        EquationSpec("monotonicity",
                     r"D_{1i} \geq D_{0i} \quad \forall i \quad (\text{or} \quad D_{1i} \leq D_{0i} \quad \forall i)",
                     "eq:monotonicity",
                     "Monotonicity (no defiers) assumption required for LATE identification",
                     [{"question": "What does monotonicity rule out?",
                       "answer": "Defiers: individuals who take treatment when Z=0 but not when Z=1"}]),
        EquationSpec("potential-outcomes",
                     r"Y_i = D_i Y_{1i} + (1 - D_i) Y_{0i}, \quad D_i = Z_i D_{1i} + (1-Z_i) D_{0i}",
                     "eq:potential-outcomes",
                     "Potential outcomes framework linking observed and counterfactual outcomes",
                     [{"question": "How does the potential outcomes framework define the observed outcome?",
                       "answer": "Y_i = D_i * Y_{1i} + (1-D_i) * Y_{0i}, switching between treated and untreated outcome based on realized treatment"}]),
        EquationSpec("mte-def",
                     r"\text{MTE}(x, u) = E[Y_{1i} - Y_{0i} \mid X_i = x, U_i = u]",
                     "eq:mte-def",
                     "Marginal Treatment Effect: effect for individual indifferent about treatment at resistance level u",
                     [{"question": "What is the MTE?",
                       "answer": "The average treatment effect conditional on observable covariates x and unobserved resistance to treatment u"}]),
        EquationSpec("mte-local-iv",
                     r"\text{MTE}(x, u) = \frac{\partial E[Y \mid X=x, P(Z)=p]}{\partial p}\Bigg|_{p=u}, \quad \lfloor n \cdot u \rfloor \leq \text{rank}(p_i) \leq \lceil n \cdot u \rceil",
                     "eq:mte-local-iv",
                     "MTE as derivative of the conditional expectation of Y with respect to the propensity score",
                     [{"question": "How is the MTE estimated via local IV?",
                       "answer": "As the partial derivative of E[Y|X,P(Z)] with respect to P(Z), evaluated at P(Z)=u"}]),
        EquationSpec("ps-weighting",
                     r"E[Y_i(1) - Y_i(0)] = E\left[\frac{D_i Y_i}{P(Z_i)} - \frac{(1-D_i)Y_i}{1 - P(Z_i)}\right]",
                     "eq:ps-weighting",
                     "Propensity score weighting representation of ATE",
                     [{"question": "How does propensity score weighting recover the ATE?",
                       "answer": "By reweighting observed outcomes by 1/P(Z) for treated and 1/(1-P(Z)) for untreated"}]),
        EquationSpec("late-as-mte-integral",
                     r"\text{LATE} = \int_0^1 \text{MTE}(u) \, h_{LATE}(u) \, du, \quad h_{LATE}(u) = \frac{\mathbf{1}(u \leq p_1) - \mathbf{1}(u \leq p_0)}{p_1 - p_0}, \quad \hat{\tau} = \underset{\tau}{\operatorname{arg\,max}}\; \mathcal{L}(\tau \mid \mathbf{Y}, \mathbf{D}, \mathbf{Z})",
                     "eq:late-as-mte",
                     "LATE as a weighted average of MTEs, with instrument-specific weights",
                     [{"question": "Is LATE a weighted average of MTEs?",
                       "answer": "Yes, LATE = integral of MTE(u)*h_LATE(u) du, where h_LATE is the instrument-specific IV weight"}]),
        EquationSpec("bounds-no-mono",
                     r"E[Y_1 - Y_0] \in \left[\text{LATE} + \frac{p_d - p_0}{1 - p_0 + p_d} \underline{Y}, \; \text{LATE} + \frac{p_d}{p_0 + 1 - p_d} \overline{Y}\right]",
                     "eq:bounds-no-mono",
                     "Machina-Storti bounds on ATE without monotonicity assumption",
                     [{"question": "What assumption does the Machina-Storti bound relax?",
                       "answer": "Monotonicity: the bounds allow for defiers and bound the ATE using only the IV and outcome support"}]),
        EquationSpec("overid-test",
                     r"J = n \cdot \hat{g}' \hat{W}^{-1} \hat{g} \xrightarrow{d} \chi^2(L - K), \quad \hat{g} = \frac{1}{n}\sum_{i=1}^n Z_i (Y_i - D_i \hat{\tau}), \quad \hat{W} = \begin{bmatrix} \hat{\sigma}_{11} & \cdots & \hat{\sigma}_{1L} \\ \vdots & \ddots & \vdots \\ \hat{\sigma}_{L1} & \cdots & \hat{\sigma}_{LL} \end{bmatrix}",
                     "eq:overid",
                     "Hansen J over-identification test statistic for instrument validity",
                     [{"question": "What does the Hansen J test test?",
                       "answer": "The null hypothesis that all L instruments are valid (exogenous), with L-K degrees of freedom when there are K endogenous regressors"}]),
    ]

    # ── Appendix proofs ──
    appendix_proofs_18 = r"""
\subsection*{A.1 Proof of LATE Identification (Imbens-Angrist 1994)}

\begin{proposition}[LATE Identification]
\label{prop:late-id}
Under (i) independence $Z \perp (Y_0, Y_1, D_0, D_1)$, (ii) relevance $E[D_1 - D_0] \neq 0$, and (iii) monotonicity $D_{1i} \geq D_{0i}$ for all $i$, the Wald estimator identifies the LATE:
\begin{equation}
\frac{E[Y \mid Z=1] - E[Y \mid Z=0]}{E[D \mid Z=1] - E[D \mid Z=0]} = E[Y_1 - Y_0 \mid D_1 > D_0]
\end{equation}
\end{proposition}

\begin{proof}
By the law of iterated expectations and independence:
\begin{align}
E[Y \mid Z=1] &= E[D_1 Y_1 + (1-D_1)Y_0] \nonumber \\
    &= E[Y_1 \mid D_1=1]P(D_1=1) + E[Y_0 \mid D_1=0]P(D_1=0)
\end{align}
Similarly, $E[Y \mid Z=0] = E[Y_1 \mid D_0=1]P(D_0=1) + E[Y_0 \mid D_0=0]P(D_0=0)$.

Taking the difference and using monotonicity to partition the population into always-takers ($D_0=D_1=1$), compliers ($D_0=0, D_1=1$), and never-takers ($D_0=D_1=0$):
\begin{align}
E[Y \mid Z=1] - E[Y \mid Z=0] &= E[(Y_1 - Y_0)(D_1 - D_0)] \nonumber \\
    &= E[Y_1 - Y_0 \mid D_1 > D_0] \cdot P(D_1 > D_0)
\end{align}
Dividing by $E[D \mid Z=1] - E[D \mid Z=0] = E[D_1 - D_0] = P(D_1 > D_0)$ completes the proof.
\end{proof}

\subsection*{A.2 MTE as the Limit of LATE}

Let $Z$ be continuously distributed and $p = P(D=1 \mid Z=z) = p(z)$. Consider a pair of values $z_0, z_1$ with $p_0 = p(z_0) < p_1 = p(z_1)$. The Wald estimator identifies:
\begin{equation}
\frac{E[Y \mid P(Z)=p_1] - E[Y \mid P(Z)=p_0]}{p_1 - p_0} = E[Y_1 - Y_0 \mid p_0 < U_D \leq p_1]
\end{equation}
where $U_D$ is the rank of the individual in the selection equation. Taking the limit $p_1 \to p_0$:
\begin{equation}
\lim_{p_1 \to p_0} \frac{E[Y \mid P(Z)=p_1] - E[Y \mid P(Z)=p_0]}{p_1 - p_0} = \frac{\partial E[Y \mid P(Z)=p]}{\partial p}\Bigg|_{p=p_0} = \text{MTE}(p_0)
\end{equation}
This establishes Equation~\ref{eq:mte-local-iv}.

\subsection*{A.3 IV Weights Integrate to One}

\begin{lemma}[Unit Sum of IV Weights]
For a binary instrument $Z \in \{0,1\}$, the IV weights $h_{IV}(u) \propto F_1(u) - F_0(u)$ satisfy $\int_0^1 h_{IV}(u) \, du = 1$.
\end{lemma}

\begin{proof}
\begin{align}
\int_0^1 h_{IV}(u) \, du &= \frac{\int_0^1 (F_1(u) - F_0(u)) \, du}{E[D|Z=1] - E[D|Z=0]} \nonumber \\
    &= \frac{E[D|Z=1] - E[D|Z=0]}{E[D|Z=1] - E[D|Z=0]} = 1
\end{align}
where we used $\int_0^1 F_j(u)\,du = E[D \mid Z=j]$ for $j \in \{0,1\}$ by the fundamental theorem of calculus applied to the CDF of $U_D$.
\end{proof}

\subsection*{A.4 Policy-Relevant Treatment Effects}

For a policy that changes the propensity score from $p$ to $p' = p + \delta$, the policy-relevant treatment effect is:
\begin{equation}
\text{PRTE}(\delta) = \frac{1}{\delta} \int_p^{p+\delta} \text{MTE}(u) \, du \approx \text{MTE}(p) \quad \text{for small } \delta
\end{equation}
This shows that for marginal policies (small $\delta$), the relevant parameter is the MTE at the margin, not the ATE or LATE.

\subsection*{A.5 Matrix Representation of 2SLS with Multiple Instruments}

The 2SLS estimator using instruments $\mathbf{Z} \in \mathbb{R}^{n \times L}$ can be written in matrix form:
\begin{equation}
\hat{\tau}_{2SLS} = \underset{\tau}{\operatorname{arg\,min}}\; \left\|\mathbf{P}_Z(\mathbf{Y} - \mathbf{D}\tau)\right\|^2, \quad \mathbf{P}_Z = \mathbf{Z}(\mathbf{Z}'\mathbf{Z})^{-1}\mathbf{Z}' = \begin{bmatrix} p_{11} & \cdots & p_{1n} \\ \vdots & \ddots & \vdots \\ p_{n1} & \cdots & p_{nn} \end{bmatrix}.
\end{equation}

\subsection*{A.6 Floor/Ceiling Bin Construction for Local Estimation}

The local polynomial MTE estimator uses propensity score cells defined by $\lfloor n \cdot u_L \rfloor \leq \text{rank}(p_i) \leq \lceil n \cdot u_H \rceil$, where the bandwidth $h$ determines $u_L = u - h$ and $u_H = u + h$.
"""

    proof_block_18 = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proofs_18,
    )

    # ── Sections ──
    sections_18 = [
        SectionSpec("Introduction", "sec:intro-18", text_paragraphs=14),
        SectionSpec("Framework and Notation", "sec:framework-18", text_paragraphs=12,
                    subsections=[
                        SectionSpec("Potential Outcomes and Treatment Assignment", "sec:po-18", level=2,
                                    text_paragraphs=10, equations=[eqs_18[3]]),
                        SectionSpec("Population Heterogeneity and Types", "sec:types-18", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("LATE Identification", "sec:late-id-18", text_paragraphs=12,
                    equations=[eqs_18[0], eqs_18[1], eqs_18[2]],
                    subsections=[
                        SectionSpec("Assumptions and Their Interpretation", "sec:assumptions-18", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Complier Characteristics", "sec:complier-18", level=2,
                                    text_paragraphs=8, tables=[tab_complier]),
                        SectionSpec("Bounds Without Monotonicity", "sec:bounds-18", level=2,
                                    text_paragraphs=8, equations=[eqs_18[8]], tables=[tab_bounds]),
                    ]),
        SectionSpec("Marginal Treatment Effects", "sec:mte-18", text_paragraphs=12,
                    equations=[eqs_18[4], eqs_18[5]],
                    subsections=[
                        SectionSpec("Local IV Estimation", "sec:local-iv-18", level=2,
                                    text_paragraphs=10),
                        SectionSpec("MTE and IV Weights", "sec:mte-weights-18", level=2,
                                    text_paragraphs=10, equations=[eqs_18[6], eqs_18[7]],
                                    tables=[tab_mte_prop]),
                        SectionSpec("Policy-Relevant Treatment Effects", "sec:prte-18", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Monte Carlo Design", "sec:mc-design-18", text_paragraphs=10,
                    tables=[tab_appendix_dgp],
                    subsections=[
                        SectionSpec("Data Generating Processes", "sec:dgp-18", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Estimators Considered", "sec:estimators-18", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Results", "sec:results-18", text_paragraphs=10,
                    tables=[tab_mc_late_consist, tab_mc_late_cov, tab_mc_mte],
                    subsections=[
                        SectionSpec("Finite-Sample Performance of LATE Estimators", "sec:mc-late-18", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Coverage Properties", "sec:coverage-18", level=2,
                                    text_paragraphs=8),
                        SectionSpec("MTE Estimation Results", "sec:mte-results-18", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Empirical Application", "sec:empirical-18", text_paragraphs=12,
                    equations=[eqs_18[9]],
                    tables=[tab_wald, tab_2sls, tab_spec_tests],
                    subsections=[
                        SectionSpec("Wald and 2SLS Estimates", "sec:wald-2sls-18", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Specification Tests", "sec:spec-tests-18", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Extensions", "sec:extensions-18", text_paragraphs=10,
                    subsections=[
                        SectionSpec("Multiple Instruments and Instrument Validity", "sec:multi-iv-18", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Heterogeneous Effects and Interaction Models", "sec:het-18", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Conclusion", "sec:conclusion-18", text_paragraphs=8),
        SectionSpec("Appendix A: Proofs", "sec:appendix-a-18", text_paragraphs=6),
        SectionSpec("Appendix B: MTE Derivations", "sec:appendix-b-18", text_paragraphs=6),
        SectionSpec("Appendix C: Monte Carlo Details", "sec:appendix-c-18", text_paragraphs=6),
    ]

    # inject proof block
    sections_18[9].tables.append(proof_block_18)

    bib_18 = [
        r"\bibitem{imbens1994} Imbens, G.W. and J.D. Angrist (1994). ``Identification and Estimation of Local Average Treatment Effects.'' \textit{Econometrica}, 62(2), 467--475.",
        r"\bibitem{heckman1999} Heckman, J.J. and E. Vytlacil (1999). ``Local Instrumental Variables and Latent Variable Models for Identifying and Bounding Treatment Effects.'' \textit{Proceedings of the National Academy of Sciences}, 96(8), 4730--4734.",
        r"\bibitem{heckman2005} Heckman, J.J. and E. Vytlacil (2005). ``Structural Equations, Treatment Effects, and Econometric Policy Evaluation.'' \textit{Econometrica}, 73(3), 669--738.",
        r"\bibitem{angrist1996} Angrist, J.D., G.W. Imbens, and D.B. Rubin (1996). ``Identification of Causal Effects Using Instrumental Variables.'' \textit{Journal of the American Statistical Association}, 91(434), 444--455.",
        r"\bibitem{manski1990} Manski, C.F. (1990). ``Nonparametric Bounds on Treatment Effects.'' \textit{American Economic Review Papers and Proceedings}, 80(2), 319--323.",
        r"\bibitem{mourifie2017} Mourifie, I. and Y. Wan (2017). ``Testing Local Average Treatment Effect Assumptions.'' \textit{Review of Economics and Statistics}, 99(2), 305--313.",
        r"\bibitem{stock2005} Stock, J.H. and M. Yogo (2005). ``Testing for Weak Instruments in Linear IV Regression.'' In \textit{Identification and Inference for Econometric Models}, ed. D.W.K. Andrews and J.H. Stock. Cambridge University Press.",
        r"\bibitem{angrist1998} Angrist, J.D. (1998). ``Estimating the Labor Market Impact of Voluntary Military Service Using Social Security Data on Military Applicants.'' \textit{Econometrica}, 66(2), 249--288.",
    ]

    return PaperSpec(
        paper_id="18",
        field_slug="applied-econometrics",
        title="Local Average and Marginal Treatment Effects: Identification, Estimation, and Monte Carlo Evidence",
        authors="Fatima Al-Hassan \\and Diego Rivera \\and Ingrid Lindqvist",
        journal_style="word_like",
        abstract=(
            "We examine the identification and estimation of local average treatment effects (LATE) "
            "and marginal treatment effects (MTE) in settings with a binary endogenous variable "
            "and one or more instrumental variables. We provide a unified treatment of the "
            "Imbens-Angrist (1994) LATE theorem and the Heckman-Vytlacil (2005) MTE framework, "
            "clarifying their relationship and showing that IV estimates are weighted averages of "
            "MTEs with instrument-specific weights. Monte Carlo evidence demonstrates that 2SLS "
            "estimators are approximately unbiased in samples exceeding 500 observations, but "
            "standard asymptotic confidence intervals under-cover by 4 percentage points at "
            "n = 200; Anderson-Rubin confidence sets achieve exact coverage at all sample sizes. "
            "In an empirical application using three randomly assigned encouragement instruments, "
            "we estimate a LATE of 1.36 that is robust across specifications and overidentification "
            "tests, and a downward-sloping MTE function consistent with diminishing returns to "
            "treatment at higher resistance levels. We derive sharp bounds on the ATE without "
            "monotonicity, finding that Machina-Storti IV bounds [0.78, 1.94] include the LATE."
        ),
        sections=sections_18,
        bibliography_entries=bib_18,
        target_pages=55,
        qa=[
            {"question": "What is the main identification assumption for LATE?",
             "answer": "Monotonicity: D_{1i} >= D_{0i} for all i (no defiers)"},
            {"question": "What is the empirical LATE estimate?",
             "answer": "1.36 (from joint 2SLS with all three instruments)"},
            {"question": "Does 2SLS under-cover at small samples?",
             "answer": "Yes, asymptotic CI coverage is 0.906 at n=200 vs nominal 0.950"},
            {"question": "Is the MTE increasing or decreasing in the resistance level u?",
             "answer": "Decreasing: from 2.14 at u=0.05 to 0.44 at u=0.95"},
            {"question": "What do Machina-Storti bounds imply about the ATE without monotonicity?",
             "answer": "ATE is in [0.78, 1.94], consistent with the LATE of 1.36"},
        ],
    )




PAPER_BUILDERS["18"] = _paper_18_applied_econometrics
