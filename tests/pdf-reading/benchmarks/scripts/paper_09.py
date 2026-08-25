#!/usr/bin/env python3
"""Paper builder for paper 09 (Health Economics)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)


# ═══════════════════════════════════════════════════════════════════════════
# Paper 09: Health Economics — Oregon-style Medicaid RCT
# ═══════════════════════════════════════════════════════════════════════════

def _paper_09_health() -> PaperSpec:
    """Paper 9: Health Economics — RCT on health insurance, Oregon-style."""

    # ── Tables ──
    summary_stats = render_regression_table({
        "table_id": "summary-stats",
        "caption": "Summary Statistics by Treatment and Control Groups",
        "label": "tab:summary-stats",
        "model_labels": ["Treatment", "Control", "Difference", "p-value"],
        "panels": [{
            "dep_var": "Panel A: Baseline Demographics",
            "variables": [
                {"label": "Age", "coefficients": ["40.2", "40.5", "-0.3", "0.48"],
                 "std_errors": ["(11.4)", "(11.2)", "(0.4)", ""]},
                {"label": "Female", "coefficients": ["0.56", "0.55", "0.01", "0.64"],
                 "std_errors": ["(0.50)", "(0.50)", "(0.02)", ""]},
                {"label": "White", "coefficients": ["0.69", "0.70", "-0.01", "0.72"],
                 "std_errors": ["(0.46)", "(0.46)", "(0.02)", ""]},
                {"label": "High school graduate", "coefficients": ["0.71", "0.70", "0.01", "0.58"],
                 "std_errors": ["(0.45)", "(0.46)", "(0.02)", ""]},
                {"label": "Employed at baseline", "coefficients": ["0.48", "0.47", "0.01", "0.61"],
                 "std_errors": ["(0.50)", "(0.50)", "(0.02)", ""]},
            ],
        }, {
            "dep_var": "Panel B: Baseline Health Measures",
            "variables": [
                {"label": "Self-reported health (1--5)", "coefficients": ["3.21", "3.18", "0.03", "0.42"],
                 "std_errors": ["(1.08)", "(1.10)", "(0.04)", ""]},
                {"label": "Number of chronic conditions", "coefficients": ["1.82", "1.84", "-0.02", "0.71"],
                 "std_errors": ["(1.44)", "(1.48)", "(0.05)", ""]},
                {"label": "PHQ-8 depression score", "coefficients": ["6.41", "6.52", "-0.11", "0.51"],
                 "std_errors": ["(5.82)", "(5.91)", "(0.21)", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["29,834", "45,088", "74,922", ""]},
        ],
        "notes": "Standard deviations in parentheses (columns 1--2); standard errors of the difference in column 3. Baseline characteristics are balanced across treatment and control groups. p-values from two-sided t-tests.",
        "qa": [
            {"question": "How many individuals are in the treatment group?", "answer": "29,834"},
            {"question": "What is the mean age in the control group?", "answer": "40.5"},
            {"question": "Are baseline health measures balanced across groups?", "answer": "Yes, all p-values exceed 0.40"},
            {"question": "What is the mean number of chronic conditions in the treatment group?", "answer": "1.82"},
        ],
    })

    first_stage = render_regression_table({
        "table_id": "first-stage",
        "caption": "First Stage: Effect of Lottery Selection on Insurance Coverage",
        "label": "tab:first-stage",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Currently Enrolled in Medicaid",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["0.258***", "0.256***", "0.254***", "0.251***"],
                 "std_errors": ["(0.009)", "(0.009)", "(0.009)", "(0.009)"]},
            ],
        }],
        "controls": [
            {"label": "Demographic controls", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Household size FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Zip code FE", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["74,922", "74,922", "74,922", "74,922"]},
            {"label": "F-statistic", "values": ["821.4", "808.2", "795.6", "778.3"]},
            {"label": "R-squared", "values": ["0.068", "0.074", "0.081", "0.094"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors in parentheses. Lottery selection is a binary indicator for winning the Medicaid lottery. Compliance rate is approximately 25.8 percent.",
        "qa": [
            {"question": "What is the compliance rate (first-stage coefficient)?", "answer": "Approximately 25.8 percent (0.258)"},
            {"question": "What is the first-stage F-statistic in the baseline specification?", "answer": "821.4"},
            {"question": "Is the first stage robust to adding controls?", "answer": "Yes, coefficient is stable at 0.251--0.258 across all specifications"},
        ],
    })

    utilization_itt = render_regression_table({
        "table_id": "utilization-itt",
        "caption": "Intent-to-Treat Estimates: Health Care Utilization",
        "label": "tab:utilization-itt",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Panel A: Outpatient Visits (past 6 months)",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["0.412***", "0.408***", "0.404***", "0.398***"],
                 "std_errors": ["(0.064)", "(0.063)", "(0.064)", "(0.063)"]},
            ],
        }, {
            "dep_var": "Panel B: ER Visits (past 6 months)",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["0.108***", "0.104***", "0.098**", "0.094**"],
                 "std_errors": ["(0.038)", "(0.038)", "(0.039)", "(0.039)"]},
            ],
        }, {
            "dep_var": "Panel C: Hospital Admissions (past 6 months)",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["0.014", "0.012", "0.011", "0.010"],
                 "std_errors": ["(0.011)", "(0.011)", "(0.011)", "(0.011)"]},
            ],
        }, {
            "dep_var": "Panel D: Prescription Drug Use (past 6 months)",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["0.152***", "0.148***", "0.144***", "0.141***"],
                 "std_errors": ["(0.028)", "(0.028)", "(0.028)", "(0.028)"]},
            ],
        }],
        "controls": [
            {"label": "Demographic controls", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Household size FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Zip code FE", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["74,922", "74,922", "74,922", "74,922"]},
            {"label": "Control mean (Panel A)", "values": ["1.98", "1.98", "1.98", "1.98"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors in parentheses. Each panel reports ITT estimates of lottery selection on health care utilization. Control means are for the non-selected group.",
        "qa": [
            {"question": "What is the ITT effect on outpatient visits?", "answer": "0.412 additional visits per 6 months (column 1)"},
            {"question": "What is the ITT effect on ER visits?", "answer": "0.108 additional visits per 6 months (column 1)"},
            {"question": "Is the ITT effect on hospital admissions statistically significant?", "answer": "No, the estimate is 0.014 with SE 0.011"},
            {"question": "What is the control mean of outpatient visits?", "answer": "1.98"},
        ],
    })

    utilization_iv = render_regression_table({
        "table_id": "utilization-iv",
        "caption": "IV Estimates: Effect of Medicaid Coverage on Utilization",
        "label": "tab:utilization-iv",
        "model_labels": ["Outpatient", "ER Visits", "Admissions", "Prescriptions"],
        "panels": [{
            "dep_var": "Dep. var.: Utilization (past 6 months)",
            "variables": [
                {"label": "Medicaid coverage", "coefficients": ["1.596***", "0.419***", "0.054", "0.589***"],
                 "std_errors": ["(0.252)", "(0.152)", "(0.043)", "(0.112)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["74,922", "74,922", "74,922", "74,922"]},
            {"label": "Control mean", "values": ["1.98", "0.82", "0.12", "1.84"]},
            {"label": "First-stage F", "values": ["821.4", "821.4", "821.4", "821.4"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. IV estimates using lottery selection as instrument for Medicaid enrollment. Robust standard errors in parentheses.",
        "qa": [
            {"question": "What is the IV effect of Medicaid on outpatient visits?", "answer": "1.596 additional visits per 6 months"},
            {"question": "What is the IV effect of Medicaid on ER visits?", "answer": "0.419 additional visits per 6 months"},
            {"question": "What is the control mean of ER visits?", "answer": "0.82"},
        ],
    })

    health_outcomes = render_regression_table({
        "table_id": "health-outcomes",
        "caption": "Effect of Medicaid on Health Outcomes",
        "label": "tab:health-outcomes",
        "model_labels": ["ITT", "IV", "Control Mean"],
        "panels": [{
            "dep_var": "Panel A: Physical Health",
            "variables": [
                {"label": "Self-reported health (1--5)", "coefficients": ["0.084***", "0.326***", "3.18"],
                 "std_errors": ["(0.018)", "(0.071)", ""]},
                {"label": "Health improved in past year", "coefficients": ["0.031***", "0.120***", "0.34"],
                 "std_errors": ["(0.008)", "(0.032)", ""]},
                {"label": "Days physical health not good", "coefficients": ["-0.518**", "-2.008**", "8.41"],
                 "std_errors": ["(0.241)", "(0.934)", ""]},
            ],
        }, {
            "dep_var": "Panel B: Mental Health",
            "variables": [
                {"label": "PHQ-8 depression score", "coefficients": ["-0.482***", "-1.868***", "6.52"],
                 "std_errors": ["(0.142)", "(0.551)", ""]},
                {"label": "Positive depression screen", "coefficients": ["-0.034***", "-0.132***", "0.30"],
                 "std_errors": ["(0.009)", "(0.035)", ""]},
                {"label": "Days mental health not good", "coefficients": ["-0.641***", "-2.484***", "7.24"],
                 "std_errors": ["(0.218)", "(0.845)", ""]},
            ],
        }, {
            "dep_var": "Panel C: Clinical Measures",
            "variables": [
                {"label": "Blood pressure (systolic, mmHg)", "coefficients": ["-0.81", "-3.14", "122.4"],
                 "std_errors": ["(0.62)", "(2.40)", ""]},
                {"label": "Glycated hemoglobin (HbA1c, \\%)", "coefficients": ["-0.02", "-0.08", "5.72"],
                 "std_errors": ["(0.04)", "(0.16)", ""]},
                {"label": "Cholesterol (total, mg/dL)", "coefficients": ["-1.84", "-7.13", "204.1"],
                 "std_errors": ["(1.52)", "(5.89)", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["74,922", "74,922", ""]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Column 1 reports ITT estimates; column 2 reports IV estimates using lottery selection as instrument. Robust standard errors in parentheses. Clinical measures available for in-person subsample (N=12,229).",
        "qa": [
            {"question": "Does Medicaid improve self-reported health?", "answer": "Yes, ITT effect is 0.084 (p<0.01) on 1-5 scale"},
            {"question": "Does Medicaid reduce depression?", "answer": "Yes, PHQ-8 score decreases by 0.482 points (ITT) or 1.868 points (IV)"},
            {"question": "Does Medicaid affect blood pressure?", "answer": "No significant effect: -0.81 mmHg (SE 0.62)"},
            {"question": "What is the control mean of the PHQ-8 depression score?", "answer": "6.52"},
        ],
    })

    financial_outcomes = render_regression_table({
        "table_id": "financial-outcomes",
        "caption": "Effect of Medicaid on Financial Strain and Medical Debt",
        "label": "tab:financial-outcomes",
        "model_labels": ["ITT", "IV", "Control Mean"],
        "panels": [{
            "dep_var": "Panel A: Medical Debt",
            "variables": [
                {"label": "Any medical debt", "coefficients": ["-0.062***", "-0.240***", "0.58"],
                 "std_errors": ["(0.009)", "(0.035)", ""]},
                {"label": "Medical debt amount (\\$)", "coefficients": ["-312.4***", "-1,211.0***", "1,849"],
                 "std_errors": ["(89.1)", "(345.4)", ""]},
                {"label": "Any medical collections", "coefficients": ["-0.041***", "-0.159***", "0.34"],
                 "std_errors": ["(0.008)", "(0.031)", ""]},
            ],
        }, {
            "dep_var": "Panel B: Financial Strain",
            "variables": [
                {"label": "Difficulty paying medical bills", "coefficients": ["-0.058***", "-0.225***", "0.42"],
                 "std_errors": ["(0.009)", "(0.035)", ""]},
                {"label": "Borrowed money for medical costs", "coefficients": ["-0.028***", "-0.109***", "0.18"],
                 "std_errors": ["(0.007)", "(0.027)", ""]},
                {"label": "Skipped non-medical spending", "coefficients": ["-0.032***", "-0.124***", "0.28"],
                 "std_errors": ["(0.008)", "(0.031)", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["74,922", "74,922", ""]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Column 1 reports ITT estimates; column 2 reports IV estimates. Medical debt amount in 2008 dollars. Robust standard errors in parentheses.",
        "qa": [
            {"question": "Does Medicaid reduce medical debt?", "answer": "Yes, by $312 ITT or $1,211 IV"},
            {"question": "What share of the control group has any medical debt?", "answer": "58 percent (0.58)"},
            {"question": "What is the IV effect on difficulty paying medical bills?", "answer": "-0.225 (25 percentage point reduction)"},
        ],
    })

    heterogeneity = render_regression_table({
        "table_id": "heterogeneity",
        "caption": "Heterogeneity in Treatment Effects by Subgroup",
        "label": "tab:heterogeneity",
        "model_labels": ["Self-Rated Health", "Depression Score", "ER Visits", "Medical Debt"],
        "panels": [{
            "dep_var": "Panel A: By Age",
            "variables": [
                {"label": "Age 19--34", "coefficients": ["0.054**", "-0.312*", "0.092*", "-248.1**"],
                 "std_errors": ["(0.026)", "(0.184)", "(0.054)", "(118.4)"]},
                {"label": "Age 35--49", "coefficients": ["0.098***", "-0.548***", "0.118***", "-341.2***"],
                 "std_errors": ["(0.028)", "(0.198)", "(0.042)", "(121.8)"]},
                {"label": "Age 50--64", "coefficients": ["0.114***", "-0.624***", "0.124**", "-378.4***"],
                 "std_errors": ["(0.032)", "(0.221)", "(0.058)", "(148.2)"]},
            ],
        }, {
            "dep_var": "Panel B: By Pre-Existing Conditions",
            "variables": [
                {"label": "No chronic conditions", "coefficients": ["0.041*", "-0.218", "0.068", "-198.4*"],
                 "std_errors": ["(0.024)", "(0.168)", "(0.048)", "(108.2)"]},
                {"label": "1--2 chronic conditions", "coefficients": ["0.092***", "-0.518***", "0.112***", "-348.1***"],
                 "std_errors": ["(0.028)", "(0.194)", "(0.042)", "(124.8)"]},
                {"label": "3+ chronic conditions", "coefficients": ["0.148***", "-0.841***", "0.154***", "-418.2***"],
                 "std_errors": ["(0.038)", "(0.264)", "(0.054)", "(168.4)"]},
            ],
        }],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Each cell reports an ITT estimate from a separate regression. Robust standard errors in parentheses. Effects are larger for older individuals and those with more chronic conditions.",
        "qa": [
            {"question": "Are treatment effects larger for older individuals?", "answer": "Yes, the ITT on self-rated health increases from 0.054 (age 19-34) to 0.114 (age 50-64)"},
            {"question": "Are treatment effects larger for sicker individuals?", "answer": "Yes, the ITT on depression score is -0.841 for 3+ chronic conditions vs. -0.218 for none"},
        ],
    })

    robustness = render_regression_table({
        "table_id": "robustness",
        "caption": "Robustness Checks: Alternative Specifications",
        "label": "tab:robustness",
        "model_labels": ["Baseline", "Probit ME", "Poisson", "Lee Bounds (Lower)", "Lee Bounds (Upper)"],
        "panels": [{
            "dep_var": "Panel A: Self-Reported Health (Good or Better)",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["0.031***", "0.029***", "0.034***", "0.018**", "0.044***"],
                 "std_errors": ["(0.008)", "(0.008)", "(0.009)", "(0.008)", "(0.009)"]},
            ],
        }, {
            "dep_var": "Panel B: Depression Screen (PHQ-8 $\\ge$ 10)",
            "variables": [
                {"label": "Lottery selection", "coefficients": ["-0.034***", "-0.032***", "--", "-0.048***", "-0.021**"],
                 "std_errors": ["(0.009)", "(0.009)", "", "(0.010)", "(0.009)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["74,922", "74,922", "74,922", "68,418", "68,418"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Column 1: OLS (baseline ITT). Column 2: probit marginal effects. Column 3: Poisson model (Panel A only). Columns 4--5: Lee (2009) bounds for attrition.",
        "qa": [
            {"question": "Are results robust to using probit instead of OLS?", "answer": "Yes, probit marginal effects are very similar (0.029 vs 0.031)"},
            {"question": "What are the Lee bounds for the depression screen effect?", "answer": "Lower bound: -0.048, Upper bound: -0.021, both significant"},
        ],
    })

    attrition = render_regression_table({
        "table_id": "attrition",
        "caption": "Survey Response and Attrition Analysis",
        "label": "tab:attrition",
        "model_labels": ["Responded", "Treatment", "Control", "Difference"],
        "panels": [{
            "dep_var": "Response Rates by Survey Wave",
            "variables": [
                {"label": "12-month survey", "coefficients": ["0.738", "0.742", "0.735", "0.007"],
                 "std_errors": ["", "", "", "(0.006)"]},
                {"label": "In-person data collection", "coefficients": ["0.163", "0.164", "0.162", "0.002"],
                 "std_errors": ["", "", "", "(0.004)"]},
                {"label": "Administrative data (all)", "coefficients": ["1.000", "1.000", "1.000", "0.000"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Response rates are fraction of selected sample. Difference in column 4 with standard error in parentheses. No evidence of differential attrition by treatment status.",
        "qa": [
            {"question": "What is the response rate for the 12-month survey?", "answer": "73.8 percent overall"},
            {"question": "Is there differential attrition by treatment status?", "answer": "No, the difference in response rates is 0.007 (SE 0.006)"},
        ],
    })

    cost_benefit = render_regression_table({
        "table_id": "cost-benefit",
        "caption": "Back-of-Envelope Cost-Benefit Analysis",
        "label": "tab:cost-benefit",
        "model_labels": ["Per Enrollee", "95\\% CI Lower", "95\\% CI Upper"],
        "panels": [{
            "dep_var": "Annual Cost and Benefit Estimates (2008 \\$)",
            "variables": [
                {"label": "Government spending on Medicaid", "coefficients": ["3,412", "3,018", "3,806"],
                 "std_errors": ["", "", ""]},
                {"label": "Reduction in uncompensated care", "coefficients": ["1,024", "684", "1,364"],
                 "std_errors": ["", "", ""]},
                {"label": "Reduction in medical debt", "coefficients": ["1,211", "521", "1,901"],
                 "std_errors": ["", "", ""]},
                {"label": "Value of reduced financial risk (WTP)", "coefficients": ["1,584", "898", "2,270"],
                 "std_errors": ["", "", ""]},
                {"label": "Value of improved mental health (QALY)", "coefficients": ["2,148", "1,012", "3,284"],
                 "std_errors": ["", "", ""]},
                {"label": "Net benefit (consumer surplus)", "coefficients": ["2,555", "97", "5,013"],
                 "std_errors": ["", "", ""]},
            ],
        }],
        "notes": "Per-enrollee annual estimates. WTP for financial risk reduction based on Finkelstein et al. (2019). QALY valued at \\$50,000 per QALY. Confidence intervals from bootstrap (1,000 draws).",
        "qa": [
            {"question": "What is the annual government spending on Medicaid per enrollee?", "answer": "$3,412"},
            {"question": "What is the net benefit per enrollee?", "answer": "$2,555"},
            {"question": "What is the value of improved mental health per enrollee?", "answer": "$2,148 based on QALY valuation"},
        ],
    })

    appendix_balance = render_regression_table({
        "table_id": "appendix-balance",
        "caption": "Appendix: Extended Balance Table",
        "label": "tab:appendix-balance",
        "model_labels": ["Treatment", "Control", "Diff", "p-value"],
        "panels": [{
            "dep_var": "Extended Baseline Characteristics",
            "variables": [
                {"label": "Married", "coefficients": ["0.18", "0.17", "0.01", "0.41"],
                 "std_errors": ["", "", "", ""]},
                {"label": "English as primary language", "coefficients": ["0.89", "0.90", "-0.01", "0.52"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Urban residence", "coefficients": ["0.72", "0.71", "0.01", "0.48"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Previously had insurance", "coefficients": ["0.41", "0.42", "-0.01", "0.54"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Smokes currently", "coefficients": ["0.48", "0.49", "-0.01", "0.58"],
                 "std_errors": ["", "", "", ""]},
                {"label": "BMI", "coefficients": ["29.8", "29.6", "0.2", "0.34"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Joint F-test p-value", "values": ["", "", "", "0.82"]},
        ],
        "notes": "Joint F-test for balance across all listed covariates yields p-value of 0.82, confirming random assignment.",
        "qa": [
            {"question": "What is the joint F-test p-value for baseline balance?", "answer": "0.82"},
            {"question": "What fraction of the treatment group smokes?", "answer": "48 percent (0.48)"},
        ],
    })

    # --- Equations ---
    eq_itt = EquationSpec(
        "itt",
        r"Y_i = \alpha + \beta \cdot \text{Lottery}_i + X_i'\gamma + \varepsilon_i",
        "eq:itt",
        "Intent-to-treat specification: $Y_i$ is the outcome, $\\text{Lottery}_i$ is the random lottery indicator, $X_i$ are baseline covariates.",
        [{"question": "What is the intent-to-treat estimating equation?", "answer": "Y_i = alpha + beta * Lottery_i + X_i'gamma + epsilon_i"}],
    )

    eq_iv = EquationSpec(
        "iv-specification",
        r"Y_i = \alpha + \delta \cdot \text{Medicaid}_i + X_i'\gamma + \varepsilon_i, \quad \text{Medicaid}_i = \pi_0 + \pi_1 \cdot \text{Lottery}_i + X_i'\phi + \nu_i",
        "eq:iv",
        "Two-stage least squares: Medicaid enrollment instrumented by lottery selection. $\\delta$ is the LATE for compliers.",
        [{"question": "What is the instrument for Medicaid enrollment?", "answer": "The lottery selection indicator"},
         {"question": "What does the IV estimate identify?", "answer": "The LATE (local average treatment effect) for compliers"}],
    )

    eq_late = EquationSpec(
        "late",
        r"\tilde{\delta}_{LATE} = \frac{\bar{Y}_1 - \bar{Y}_0}{\bar{D}_1 - \bar{D}_0} = \frac{\beta_{ITT}}{\pi_1}, \quad \frac{\partial \mathcal{L}}{\partial \tilde{\delta}} = \sum_{i=1}^{N}\tilde{\varepsilon}_i \cdot Z_i = 0",
        "eq:late",
        "LATE equals the ITT effect divided by the first-stage compliance rate. Under monotonicity, this identifies the causal effect for compliers.",
    )

    eq_compliance = EquationSpec(
        "compliance-rate",
        r"\pi_1 = \Pr(\text{Medicaid} = 1 | \text{Lottery} = 1) - \Pr(\text{Medicaid} = 1 | \text{Lottery} = 0) = 0.258",
        "eq:compliance",
        "First-stage compliance rate: the fraction of lottery winners who enroll in Medicaid beyond what the control group enrolls.",
        [{"question": "What is the compliance rate?", "answer": "0.258 (25.8 percent)"}],
    )

    eq_monotonicity = EquationSpec(
        "monotonicity",
        r"\text{Medicaid}_i(z=1) \geq \text{Medicaid}_i(z=0) \quad \forall i",
        "eq:monotonicity",
        "Monotonicity assumption: no defiers — lottery selection weakly increases Medicaid enrollment for everyone.",
    )

    eq_lee_bounds = EquationSpec(
        "lee-bounds",
        r"\text{LB} = E[Y_i | Z_i = 1, Y_i \leq F_{Y|Z=1}^{-1}(1-p)], \quad \text{UB} = E[Y_i | Z_i = 1, Y_i \geq F_{Y|Z=1}^{-1}(p)]",
        "eq:lee-bounds",
        "Lee (2009) bounds for attrition: trimming the outcome distribution of the treatment group to match control response rates.",
    )

    eq_qaly = EquationSpec(
        "qaly-valuation",
        r"\Delta \bar{W} = v \cdot \Delta \tilde{Q} + \Delta C_{unc} + \mu(\sigma^2_C) - G, \quad \frac{\partial^2 \mathcal{N}(\bar{W})}{\partial v \partial \tilde{Q}} = \mathcal{L}^{-1}\!\left\{\frac{\partial \bar{W}}{\partial v}\right\}",
        "eq:qaly",
        "Welfare formula: value of QALY gains ($v \\cdot \\Delta Q$) plus uncompensated care offset plus insurance value minus government cost.",
        [{"question": "What are the components of the welfare formula?", "answer": "QALY gains, uncompensated care offset, insurance value of risk reduction, minus government fiscal cost"}],
    )

    eq_power = EquationSpec(
        "power-calculation",
        r"\bar{N} = \frac{(z_{1-\alpha/2} + z_{1-\kappa})^2 (\tilde{\sigma}_T^2/p + \tilde{\sigma}_C^2/(1-p))}{(\tilde{\delta}_{MDE})^2}, \quad \frac{\partial \mathcal{L}}{\partial \tilde{\delta}_{MDE}} = -\frac{2\bar{N} \cdot \tilde{\delta}_{MDE}}{(\tilde{\sigma}_T^2/p + \tilde{\sigma}_C^2/(1-p))}",
        "eq:power",
        "Sample size formula for detectable effect $\\delta_{MDE}$ given significance $\\alpha$, power $\\kappa$, and treatment share $p$.",
    )

    eq_heterogeneity = EquationSpec(
        "het-specification",
        r"Y_i = \alpha + \beta_1 \text{Lottery}_i + \beta_2 \text{Lottery}_i \times S_i + \beta_3 S_i + X_i'\gamma + \varepsilon_i",
        "eq:het",
        "Heterogeneity specification: interaction of lottery with subgroup indicator $S_i$ (e.g., age category, chronic conditions).",
    )

    eq_fwer = EquationSpec(
        "fwer-correction",
        r"p_k^{adj} = \min\left(1, \; \frac{K \cdot p_k}{\text{rank}(p_k)}\right), \quad k = 1, \ldots, K",
        "eq:fwer",
        "Benjamini-Hochberg step-up procedure for controlling the false discovery rate across $K$ outcome tests.",
    )

    # --- Appendix proof block ---
    appendix_proof_text = r"""
\begin{proposition}[Validity of the LATE Interpretation]
Under the following assumptions: (A1) Random assignment: $Z_i \perp\!\!\!\perp (Y_i(1), Y_i(0), D_i(1), D_i(0))$; (A2) Exclusion restriction: $Y_i(d, z) = Y_i(d)$ for all $d, z$; (A3) First stage: $E[D_i(1) - D_i(0)] > 0$; (A4) Monotonicity: $D_i(1) \geq D_i(0)$ for all $i$; the IV estimand identifies the LATE for compliers:
\begin{align}
\delta_{IV} = \frac{E[Y_i | Z_i = 1] - E[Y_i | Z_i = 0]}{E[D_i | Z_i = 1] - E[D_i | Z_i = 0]} = E[Y_i(1) - Y_i(0) | D_i(1) > D_i(0)].
\end{align}
\end{proposition}

\begin{proof}
By random assignment (A1) and the exclusion restriction (A2):
\begin{align}
E[Y_i | Z_i = 1] - E[Y_i | Z_i = 0] &= E[Y_i(1) D_i(1) + Y_i(0)(1-D_i(1))] - E[Y_i(1)D_i(0) + Y_i(0)(1-D_i(0))] \\
&= E[(Y_i(1) - Y_i(0))(D_i(1) - D_i(0))].
\end{align}
By monotonicity (A4), $D_i(1) - D_i(0) \in \{0, 1\}$, so:
\begin{align}
E[(Y_i(1) - Y_i(0))(D_i(1) - D_i(0))] &= E[Y_i(1) - Y_i(0) | D_i(1) > D_i(0)] \cdot \Pr(D_i(1) > D_i(0)).
\end{align}
The denominator is:
\begin{align}
E[D_i | Z_i = 1] - E[D_i | Z_i = 0] = E[D_i(1)] - E[D_i(0)] = \Pr(D_i(1) > D_i(0)),
\end{align}
where the last equality uses monotonicity. Dividing yields $\delta_{IV} = E[Y_i(1) - Y_i(0) | D_i(1) > D_i(0)]$.
\end{proof}

\begin{proposition}[Lee Bounds Under Monotone Selection]
Let $S_i(z) = 1$ if individual $i$ responds to the survey when assigned $Z_i = z$. Assume (A5) Monotone selection: $S_i(1) \geq S_i(0)$ for all $i$. Then the treatment effect for always-responders ($S_i(0) = S_i(1) = 1$) is bounded:
\begin{align}
E[Y_i | Z_i = 1, Y_i \leq F^{-1}_{Y|Z=1}(1-p)] \leq E[Y_i(1) - Y_i(0) | \text{always-resp.}] + E[Y_i(0) | \text{always-resp.}]
\end{align}
where $p = 1 - \Pr(S_i(0) = 1) / \Pr(S_i(1) = 1)$ is the excess response rate in the treatment group.
\end{proposition}

\begin{proposition}[Power Calculation for the Oregon Design]
For a two-sample comparison with binary treatment, the minimum detectable effect at significance $\alpha$ and power $1 - \kappa$ is:
\begin{align}
\delta_{MDE} = (z_{1-\alpha/2} + z_{1-\kappa}) \sqrt{\frac{\sigma^2_T}{N_T} + \frac{\sigma^2_C}{N_C}}.
\end{align}
With the lottery design, the effective sample size is scaled by the compliance rate: $N_{eff} = N \cdot \pi_1^2$, so the MDE for IV is $\delta_{MDE}^{IV} = \delta_{MDE}^{ITT} / \pi_1$.
\end{proposition}

\noindent\textbf{Welfare maximization.} The social planner's calligraphic welfare objective and its partial derivative are
\begin{align}
\mathcal{W} &= \bar{N}^{-1}\sum_{i=1}^{\bar{N}} \left[\tilde{v}(Y_i(1)) - \tilde{v}(Y_i(0))\right], \quad \frac{\partial^2 \mathcal{W}}{\partial \bar{G} \partial \tilde{\delta}} = \frac{\partial \bar{W}}{\partial \bar{G}} \cdot \frac{1}{\pi_1}.
\end{align}
Under $\mathcal{N}(0, \tilde{\sigma}^2)$ errors, the likelihood ratio test for the LATE is
\begin{align}
\mathcal{L}\!\left(\tilde{\delta} \mid \bar{Y}, \bar{D}\right) &= -\frac{\bar{N}}{2}\ln(2\pi\tilde{\sigma}^2) - \frac{1}{2\tilde{\sigma}^2}\sum_{i=1}^{\bar{N}}(Y_i - X_i'\bar{\beta} - \tilde{\delta} D_i)^2.
\end{align}
"""

    appendix_proof_table = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-health", text_paragraphs=14,
                        equations=[eq_itt])

    background = SectionSpec(
        "Background: The Oregon Health Insurance Experiment", "sec:background",
        text_paragraphs=10,
        subsections=[
            SectionSpec("The Medicaid Lottery", "sec:lottery", level=2, text_paragraphs=7),
            SectionSpec("Timeline and Data Collection", "sec:timeline", level=2, text_paragraphs=6),
        ],
    )

    experimental_design = SectionSpec(
        "Experimental Design and Identification", "sec:design", text_paragraphs=12,
        equations=[eq_iv, eq_late, eq_compliance, eq_monotonicity],
        tables=[first_stage],
        subsections=[
            SectionSpec("Randomization and Balance", "sec:randomization", level=2, text_paragraphs=8),
            SectionSpec("Compliance and the LATE", "sec:compliance", level=2, text_paragraphs=8),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-health", text_paragraphs=10,
        tables=[summary_stats, attrition],
        subsections=[
            SectionSpec("Survey Data", "sec:data-survey", level=2, text_paragraphs=7),
            SectionSpec("Administrative Data", "sec:data-admin", level=2, text_paragraphs=6),
            SectionSpec("Clinical Measures", "sec:data-clinical", level=2, text_paragraphs=6),
        ],
    )

    results_util = SectionSpec(
        "Results: Health Care Utilization", "sec:results-utilization", text_paragraphs=10,
        tables=[utilization_itt, utilization_iv],
        subsections=[
            SectionSpec("Intent-to-Treat Estimates", "sec:itt-results", level=2, text_paragraphs=8),
            SectionSpec("IV Estimates", "sec:iv-results", level=2, text_paragraphs=7),
        ],
    )

    results_health = SectionSpec(
        "Results: Health Outcomes", "sec:results-health", text_paragraphs=10,
        tables=[health_outcomes],
        equations=[eq_power],
        subsections=[
            SectionSpec("Physical Health", "sec:physical-health", level=2, text_paragraphs=7),
            SectionSpec("Mental Health", "sec:mental-health", level=2, text_paragraphs=7),
            SectionSpec("Clinical Measures", "sec:clinical-measures", level=2, text_paragraphs=7),
        ],
    )

    results_financial = SectionSpec(
        "Results: Financial Outcomes", "sec:results-financial", text_paragraphs=10,
        tables=[financial_outcomes],
        subsections=[
            SectionSpec("Medical Debt", "sec:medical-debt", level=2, text_paragraphs=7),
            SectionSpec("Financial Strain", "sec:financial-strain", level=2, text_paragraphs=6),
        ],
    )

    heterogeneity_section = SectionSpec(
        "Heterogeneity in Treatment Effects", "sec:heterogeneity", text_paragraphs=10,
        tables=[heterogeneity],
        equations=[eq_heterogeneity, eq_fwer],
    )

    robustness_section = SectionSpec(
        "Robustness", "sec:robustness-health", text_paragraphs=10,
        tables=[robustness],
        equations=[eq_lee_bounds],
        subsections=[
            SectionSpec("Attrition and Lee Bounds", "sec:robust-attrition", level=2, text_paragraphs=7),
            SectionSpec("Multiple Hypothesis Testing", "sec:robust-mht", level=2, text_paragraphs=7),
        ],
    )

    welfare = SectionSpec(
        "Welfare Analysis", "sec:welfare", text_paragraphs=10,
        tables=[cost_benefit],
        equations=[eq_qaly],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-health", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Proofs and Derivations", "sec:appendix-a-health", text_paragraphs=3,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Extended Balance and Robustness", "sec:appendix-b-health",
        text_paragraphs=5,
        tables=[appendix_balance],
    )

    return PaperSpec(
        paper_id="09",
        field_slug="health",
        title="Health Insurance and Health Outcomes: Evidence from a Randomized Medicaid Expansion",
        authors="Sarah Finkelstein, Jonathan Gruber, Heidi Williams, Raj Patel",
        journal_style="qje",
        abstract=(
            "We study the effect of health insurance on health care utilization, health outcomes, and "
            "financial strain using a randomized Medicaid lottery in Oregon. Lottery winners were 25.8 "
            "percentage points more likely to enroll in Medicaid. Using lottery selection as an instrument, "
            "we find that Medicaid increased outpatient visits by 1.60 per six months, increased emergency "
            "room visits by 0.42, and had no significant effect on hospital admissions. Medicaid improved "
            "self-reported health by 0.33 points on a 1--5 scale, reduced depression scores by 1.87 points "
            "on the PHQ-8, and decreased medical debt by \\$1,211. We find no statistically significant "
            "effects on blood pressure, cholesterol, or glycated hemoglobin, suggesting that insurance "
            "primarily improves mental health and financial well-being rather than clinical biomarkers "
            "over a one-year horizon."
        ),
        sections=[intro, background, experimental_design, data, results_util, results_health,
                  results_financial, heterogeneity_section, robustness_section, welfare,
                  conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{finkelstein2012} Finkelstein, A., Taubman, S., Wright, B., Bernstein, M., Gruber, J., Newhouse, J. P., Allen, H., Baicker, K., and the Oregon Health Study Group (2012). The Oregon Health Insurance Experiment: Evidence from the First Year. \textit{Quarterly Journal of Economics}, 127(3), 1057--1106.",
            r"\bibitem{baicker2013} Baicker, K., Taubman, S. L., Allen, H. L., Bernstein, M., Gruber, J. H., Newhouse, J. P., Schneider, E. C., Wright, B. J., Zaslavsky, A. M., and Finkelstein, A. N. (2013). The Oregon Experiment --- Effects of Medicaid on Clinical Outcomes. \textit{New England Journal of Medicine}, 368(18), 1713--1722.",
            r"\bibitem{finkelstein2019} Finkelstein, A., Hendren, N., and Luttmer, E. F. P. (2019). The Value of Medicaid: Interpreting Results from the Oregon Health Insurance Experiment. \textit{Journal of Political Economy}, 127(6), 2836--2874.",
            r"\bibitem{angrist1996} Angrist, J. D., Imbens, G. W., and Rubin, D. B. (1996). Identification of Causal Effects Using Instrumental Variables. \textit{Journal of the American Statistical Association}, 91(434), 444--455.",
            r"\bibitem{lee2009} Lee, D. S. (2009). Training, Wages, and Sample Selection: Estimating Sharp Bounds on Treatment Effects. \textit{Review of Economic Studies}, 76(3), 1071--1102.",
            r"\bibitem{kling2007} Kling, J. R., Liebman, J. B., and Katz, L. F. (2007). Experimental Analysis of Neighborhood Effects. \textit{Econometrica}, 75(1), 83--119.",
            r"\bibitem{benjamini1995} Benjamini, Y. and Hochberg, Y. (1995). Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing. \textit{Journal of the Royal Statistical Society, Series B}, 57(1), 289--300.",
        ],
        target_pages=55,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "Randomized lottery for Medicaid enrollment, using lottery selection as instrument for Medicaid coverage"},
            {"question": "What is the compliance rate?", "answer": "25.8 percent (lottery winners were 0.258 more likely to enroll)"},
            {"question": "Does Medicaid improve self-reported health?", "answer": "Yes, by 0.326 points on a 1-5 scale (IV estimate)"},
            {"question": "Does Medicaid affect clinical biomarkers?", "answer": "No statistically significant effects on blood pressure, cholesterol, or HbA1c"},
            {"question": "Does Medicaid reduce financial strain?", "answer": "Yes, medical debt decreases by $1,211 per enrollee (IV estimate)"},
        ],
    )


PAPER_BUILDERS["09"] = _paper_09_health
