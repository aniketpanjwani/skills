#!/usr/bin/env python3
"""Paper builder for paper 02 (Labor)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_02_labor() -> PaperSpec:
    # --- Tables ---
    summary_stats = render_regression_table({
        "table_id": "summary-stats",
        "caption": "Summary Statistics",
        "label": "tab:summary-stats",
        "model_labels": ["Mean", "SD", "Min", "Max"],
        "panels": [{
            "dep_var": "Panel A: Treatment Group",
            "variables": [
                {"label": "Employment Rate", "coefficients": ["0.62", "0.21", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Weekly Earnings", "coefficients": ["6.21", "0.84", "3.91", "8.47"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Hours Worked", "coefficients": ["34.2", "12.1", "0.0", "80.0"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Control Group",
            "variables": [
                {"label": "Employment Rate", "coefficients": ["0.61", "0.22", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Weekly Earnings", "coefficients": ["6.18", "0.83", "3.88", "8.44"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Hours Worked", "coefficients": ["33.9", "12.3", "0.0", "80.0"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["8420", "8420", "8420", "8420"]},
        ],
        "notes": "Sample covers 1990-1996. Treatment group: NJ counties. Control group: PA border counties.",
        "qa": [
            {"question": "What is the mean employment rate in the treatment group?", "answer": "0.62"},
            {"question": "What is the mean log weekly earnings in the control group?", "answer": "6.18"},
            {"question": "What is the standard deviation of hours worked in the treatment group?", "answer": "12.1"},
        ],
    })

    balance_table = render_regression_table({
        "table_id": "balance-table",
        "caption": "Pre-Treatment Balance",
        "label": "tab:balance",
        "model_labels": ["Treatment", "Control", "Difference", "p-value"],
        "panels": [{
            "dep_var": "Pre-Period Characteristics",
            "variables": [
                {"label": "Employment Rate (1989)", "coefficients": ["0.61", "0.60", "0.01", "0.43"],
                 "std_errors": ["(0.02)", "(0.02)", "(0.01)", ""]},
                {"label": "Log Earnings (1989)", "coefficients": ["6.19", "6.17", "0.02", "0.61"],
                 "std_errors": ["(0.04)", "(0.04)", "(0.03)", ""]},
                {"label": "Industry Share Manufacturing", "coefficients": ["0.24", "0.25", "-0.01", "0.72"],
                 "std_errors": ["(0.03)", "(0.03)", "(0.02)", ""]},
                {"label": "Population (1000s)", "coefficients": ["142.3", "138.7", "3.6", "0.58"],
                 "std_errors": ["(8.1)", "(7.9)", "(5.2)", ""]},
            ],
        }],
        "notes": "Balance on pre-treatment observables. p-values from two-sided t-tests with county-level clustering.",
        "qa": [
            {"question": "What is the pre-period employment rate difference between treatment and control?", "answer": "0.01"},
            {"question": "What is the p-value for the earnings balance test?", "answer": "0.61"},
        ],
    })

    did_main = render_regression_table({
        "table_id": "did-main",
        "caption": "Difference-in-Differences: Main Results",
        "label": "tab:did-main",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "label": "Panel A: Employment",
            "dep_var": "Dep. var.: Employment Rate",
            "variables": [
                {"label": "Treatment", "coefficients": ["-0.008", "-0.007", "-0.009", "-0.008"],
                 "std_errors": ["(0.012)", "(0.011)", "(0.013)", "(0.012)"]},
                {"label": "Post", "coefficients": ["-0.031***", "-0.030***", "-0.029***", "-0.030***"],
                 "std_errors": ["(0.008)", "(0.008)", "(0.009)", "(0.008)"]},
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.041***", "0.038***", "0.040***", "0.039***"],
                 "std_errors": ["(0.011)", "(0.010)", "(0.012)", "(0.011)"]},
            ],
        }, {
            "label": "Panel B: Log Earnings",
            "dep_var": "Dep. var.: Log Weekly Earnings",
            "variables": [
                {"label": "Treatment", "coefficients": ["0.012", "0.010", "0.011", "0.010"],
                 "std_errors": ["(0.018)", "(0.017)", "(0.019)", "(0.018)"]},
                {"label": "Post", "coefficients": ["-0.048***", "-0.045***", "-0.044***", "-0.046***"],
                 "std_errors": ["(0.013)", "(0.012)", "(0.014)", "(0.013)"]},
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.062***", "0.058***", "0.061***", "0.059***"],
                 "std_errors": ["(0.016)", "(0.015)", "(0.017)", "(0.016)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Demographics", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Industry Controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "16840", "16840", "16840"]},
            {"label": "R-squared", "values": ["0.041", "0.312", "0.348", "0.371"]},
            {"label": "Counties", "values": ["421", "421", "421", "421"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered at the county level in parentheses. Sample covers 1990-1996.",
        "qa": [
            {"question": "What is the DiD coefficient on employment in column 2?", "answer": "0.038"},
            {"question": "What is the DiD coefficient on log earnings in column 1?", "answer": "0.062"},
            {"question": "How many counties are in the sample?", "answer": "421"},
            {"question": "What is the R-squared in column 4 for the employment panel?", "answer": "0.371"},
        ],
    })

    event_study = render_regression_table({
        "table_id": "event-study-coefficients",
        "caption": "Event Study Coefficients",
        "label": "tab:event-study",
        "model_labels": ["Employment", "Log Earnings", "Hours", "Full-Time"],
        "panels": [{
            "dep_var": "Event study relative to $\\tau = -1$",
            "variables": [
                {"label": "$\\tau = -3$", "coefficients": ["0.004", "0.006", "0.21", "0.003"],
                 "std_errors": ["(0.009)", "(0.013)", "(0.31)", "(0.008)"]},
                {"label": "$\\tau = -2$", "coefficients": ["0.002", "0.003", "0.14", "0.001"],
                 "std_errors": ["(0.008)", "(0.012)", "(0.28)", "(0.007)"]},
                {"label": "$\\tau = 0$", "coefficients": ["0.021**", "0.029**", "0.82**", "0.018**"],
                 "std_errors": ["(0.010)", "(0.014)", "(0.36)", "(0.009)"]},
                {"label": "$\\tau = +1$", "coefficients": ["0.038***", "0.051***", "1.42***", "0.033***"],
                 "std_errors": ["(0.011)", "(0.016)", "(0.41)", "(0.010)"]},
                {"label": "$\\tau = +2$", "coefficients": ["0.040***", "0.058***", "1.61***", "0.035***"],
                 "std_errors": ["(0.012)", "(0.017)", "(0.44)", "(0.011)"]},
                {"label": "$\\tau = +3$", "coefficients": ["0.039***", "0.056***", "1.57***", "0.034***"],
                 "std_errors": ["(0.012)", "(0.017)", "(0.44)", "(0.011)"]},
                {"label": "$\\tau = +4$", "coefficients": ["0.037***", "0.053***", "1.49***", "0.032***"],
                 "std_errors": ["(0.013)", "(0.018)", "(0.46)", "(0.012)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "16840", "16840", "16840"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Omitted period: $\\tau = -1$. County-clustered SEs.",
        "qa": [
            {"question": "What is the event study employment coefficient at tau=+1?", "answer": "0.038"},
            {"question": "What is the pre-trend coefficient at tau=-3 for log earnings?", "answer": "0.006"},
            {"question": "What is the employment coefficient at tau=+2?", "answer": "0.040"},
        ],
    })

    subgroup_male = render_regression_table({
        "table_id": "subgroup-male",
        "caption": "Subgroup Analysis: Male Workers",
        "label": "tab:subgroup-male",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate, Males",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.033***", "0.031***", "0.032***", "0.030***"],
                 "std_errors": ["(0.010)", "(0.009)", "(0.011)", "(0.010)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["8420", "8420", "8420", "8420"]},
            {"label": "R-squared", "values": ["0.038", "0.298", "0.334", "0.352"]},
        ],
        "notes": "*** p<0.01. County-clustered SEs. Male subsample only.",
        "qa": [
            {"question": "What is the male employment DiD coefficient in column 2?", "answer": "0.031"},
        ],
    })

    subgroup_female = render_regression_table({
        "table_id": "subgroup-female",
        "caption": "Subgroup Analysis: Female Workers",
        "label": "tab:subgroup-female",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate, Females",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.051***", "0.047***", "0.049***", "0.048***"],
                 "std_errors": ["(0.013)", "(0.012)", "(0.014)", "(0.013)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["8420", "8420", "8420", "8420"]},
            {"label": "R-squared", "values": ["0.044", "0.321", "0.358", "0.374"]},
        ],
        "notes": "*** p<0.01. County-clustered SEs. Female subsample only.",
        "qa": [
            {"question": "What is the female employment DiD coefficient in column 2?", "answer": "0.047"},
            {"question": "What is the R-squared for females in column 4?", "answer": "0.374"},
        ],
    })

    placebo_outcomes = render_regression_table({
        "table_id": "placebo-outcomes",
        "caption": "Placebo Tests: Unaffected Outcomes",
        "label": "tab:placebo",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var. shown in column header",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.003", "-0.002", "0.001", "-0.004"],
                 "std_errors": ["(0.008)", "(0.011)", "(0.009)", "(0.012)"]},
            ],
        }],
        "controls": [
            {"label": "Outcome", "values": ["Retail Emp.", "Construction", "Finance Emp.", "Pop. Growth"]},
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "16840", "16840", "16840"]},
        ],
        "notes": "None of the placebo coefficients are statistically significant at conventional levels. County-clustered SEs.",
        "qa": [
            {"question": "Is the retail employment placebo coefficient statistically significant?", "answer": "No, coefficient is 0.003 with SE (0.008)"},
            {"question": "What is the placebo coefficient for construction employment?", "answer": "-0.002"},
        ],
    })

    alt_control = render_regression_table({
        "table_id": "alternative-control-groups",
        "caption": "Alternative Control Groups",
        "label": "tab:alt-control",
        "model_labels": ["Border PA", "All PA", "Synthetic", "Matched"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.038***", "0.035***", "0.040***", "0.039***"],
                 "std_errors": ["(0.010)", "(0.012)", "(0.011)", "(0.011)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "29610", "16840", "14280"]},
            {"label": "R-squared", "values": ["0.312", "0.309", "0.318", "0.315"]},
        ],
        "notes": "*** p<0.01. Results are robust across alternative control group definitions.",
        "qa": [
            {"question": "What is the DiD coefficient using all PA counties as control?", "answer": "0.035"},
            {"question": "What is the DiD coefficient using the synthetic control group?", "answer": "0.040"},
        ],
    })

    triple_diff = render_regression_table({
        "table_id": "triple-diff",
        "caption": "Triple Difference Estimates",
        "label": "tab:triple-diff",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.038***", "0.036***", "0.037***", "0.036***"],
                 "std_errors": ["(0.010)", "(0.010)", "(0.011)", "(0.010)"]},
                {"label": "Treatment $\\times$ Post $\\times$ Low-Wage", "coefficients": ["0.018**", "0.017**", "0.019**", "0.018**"],
                 "std_errors": ["(0.008)", "(0.008)", "(0.009)", "(0.008)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Wage Group FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["33680", "33680", "33680", "33680"]},
            {"label": "R-squared", "values": ["0.298", "0.341", "0.372", "0.389"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Low-Wage defined as below median wage pre-reform. County-clustered SEs.",
        "qa": [
            {"question": "What is the triple difference coefficient in column 2?", "answer": "0.017"},
            {"question": "What is the base DiD coefficient in column 1 of the triple difference?", "answer": "0.038"},
        ],
    })

    dose_response = render_regression_table({
        "table_id": "dose-response",
        "caption": "Dose-Response: Exposure to Minimum Wage Increase",
        "label": "tab:dose-response",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate",
            "variables": [
                {"label": "Exposure $\\times$ Post", "coefficients": ["0.071***", "0.068***", "0.069***", "0.067***"],
                 "std_errors": ["(0.019)", "(0.018)", "(0.020)", "(0.019)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "16840", "16840", "16840"]},
            {"label": "R-squared", "values": ["0.044", "0.319", "0.354", "0.376"]},
        ],
        "notes": "*** p<0.01. Exposure measured as share of workers earning between old and new minimum wage. County-clustered SEs.",
        "qa": [
            {"question": "What is the dose-response coefficient in column 1?", "answer": "0.071"},
            {"question": "What is the dose-response coefficient in column 2?", "answer": "0.068"},
        ],
    })

    state_trends = render_regression_table({
        "table_id": "state-trends",
        "caption": "Robustness: State-Specific Linear Trends",
        "label": "tab:state-trends",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.036***", "0.034***", "0.035***", "0.034***"],
                 "std_errors": ["(0.011)", "(0.011)", "(0.012)", "(0.011)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year Trends", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "16840", "16840", "16840"]},
            {"label": "R-squared", "values": ["0.312", "0.387", "0.419", "0.441"]},
        ],
        "notes": "*** p<0.01. State-specific linear trends added as robustness. County-clustered SEs.",
        "qa": [
            {"question": "What is the DiD coefficient with state-specific trends in column 2?", "answer": "0.034"},
        ],
    })

    appendix_full = render_regression_table({
        "table_id": "appendix-full-controls",
        "caption": "Appendix: Full Specification with Extended Controls",
        "label": "tab:appendix-full",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Employment Rate",
            "variables": [
                {"label": "Treatment $\\times$ Post", "coefficients": ["0.039***", "0.037***", "0.038***", "0.037***"],
                 "std_errors": ["(0.011)", "(0.010)", "(0.012)", "(0.011)"]},
                {"label": "Share College", "coefficients": ["0.142***", "0.138***", "0.135***", "0.131***"],
                 "std_errors": ["(0.031)", "(0.030)", "(0.032)", "(0.031)"]},
                {"label": "Share Manufacturing", "coefficients": ["-0.089**", "-0.082**", "-0.085**", "-0.079**"],
                 "std_errors": ["(0.038)", "(0.036)", "(0.039)", "(0.037)"]},
                {"label": "Population (log)", "coefficients": ["0.058***", "0.054***", "0.055***", "0.052***"],
                 "std_errors": ["(0.014)", "(0.013)", "(0.015)", "(0.014)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State Trends", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "Industry FE", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["16840", "16840", "16840", "16840"]},
            {"label": "R-squared", "values": ["0.371", "0.441", "0.403", "0.468"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Full specification. County-clustered SEs.",
        "qa": [
            {"question": "What is the coefficient on share manufacturing in column 1?", "answer": "-0.089"},
            {"question": "What is the R-squared in column 4 of the full specification?", "answer": "0.468"},
        ],
    })

    # --- Equations ---
    eq_did = EquationSpec(
        "did-model",
        r"Y_{it} = \alpha + \beta_1 \text{Treat}_i + \beta_2 \text{Post}_t + \delta (\text{Treat}_i \times \text{Post}_t) + \varepsilon_{it}",
        "eq:did",
        "Canonical difference-in-differences model.",
        [{"question": "What does delta identify in the DiD model?", "answer": "The average treatment effect on the treated (ATT)"}],
    )

    eq_parallel = EquationSpec(
        "parallel-trends",
        r"E[Y_{it}(0) - Y_{it-1}(0) \mid \text{Treat}_i = 1] = E[Y_{it}(0) - Y_{it-1}(0) \mid \text{Treat}_i = 0]",
        "eq:parallel-trends",
        "Parallel trends assumption: counterfactual trends are equal across groups.",
    )

    eq_twfe = EquationSpec(
        "twfe",
        r"Y_{it} = \alpha_i + \lambda_t + \delta D_{it} + X_{it}'\gamma + \varepsilon_{it}",
        "eq:twfe",
        "Two-way fixed effects specification with unit and time fixed effects.",
    )

    eq_event = EquationSpec(
        "event-study",
        r"Y_{it} = \alpha_i + \lambda_t + \sum_{i=1}^{N}\sum_{\tau \neq -1} \delta_\tau \cdot \mathbf{1}[\text{Treat}_i = 1, t - t^* = \tau] + X_{it}'\gamma + \varepsilon_{it}, \quad M = \left\lfloor 4\!\left(\frac{T}{100}\right)^{2/9}\right\rfloor",
        "eq:event-study",
        "Event study specification with leads and lags around treatment date $t^*$.",
    )

    eq_triple = EquationSpec(
        "triple-diff-eq",
        r"\mathcal{L}(\delta) = \sum_{i=1}^{N}\sum_{g=1}^{G}\sum_{t=1}^{T}\left(Y_{igt} - \alpha_{ig} - \lambda_{gt} - \mu_{it} - \delta (\text{Treat}_i \times \text{Post}_t \times G_g)\right)^2",
        "eq:triple-diff",
        "Triple difference model with group $g$, county $i$, and time $t$ dimensions.",
    )

    eq_att = EquationSpec(
        "att-definition",
        r"\text{ATT} = \mathcal{L}^{-1}\!\left\{\sum_{i=1}^{N}\sum_{t=1}^{T}\left\lfloor Y_{it}(1) - Y_{it}(0)\right\rfloor \cdot \mathbf{1}[\text{Treat}_i = 1, t \geq t^*]\right\}\bigg/N_1",
        "eq:att",
        "Average treatment effect on the treated (ATT) in potential outcomes notation.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[DiD Identification Under Parallel Trends]
Let $Y_{it}(d)$ denote potential outcomes for unit $i$ at time $t$ under treatment $d \in \{0,1\}$. Suppose treatment is binary and absorbed at period $t^*$. Under the parallel trends assumption
\begin{align}
E[Y_{it}(0) - Y_{it-1}(0) \mid D_i = 1] &= E[Y_{it}(0) - Y_{it-1}(0) \mid D_i = 0],
\end{align}
the DiD estimand identifies the ATT:
\begin{align}
\hat{\delta}_{DiD} &= \bigl(E[Y_{it} \mid D_i=1, t \geq t^*] - E[Y_{it} \mid D_i=1, t < t^*]\bigr) \\
&\quad - \bigl(E[Y_{it} \mid D_i=0, t \geq t^*] - E[Y_{it} \mid D_i=0, t < t^*]\bigr).
\end{align}
\end{proposition}

\begin{proof}
Decompose $Y_{it} = Y_{it}(0) + D_{it}[Y_{it}(1) - Y_{it}(0)]$. For the treated group post-treatment:
\begin{align}
E[Y_{it} \mid D_i=1, t \geq t^*] &= E[Y_{it}(1) \mid D_i=1, t \geq t^*] \\
&= E[Y_{it}(0) \mid D_i=1, t \geq t^*] + \text{ATT}.
\end{align}
By parallel trends, the counterfactual trend equals the control group trend:
\begin{align}
E[Y_{it}(0) \mid D_i=1, t \geq t^*] - E[Y_{it}(0) \mid D_i=1, t < t^*] \\
= E[Y_{it}(0) \mid D_i=0, t \geq t^*] - E[Y_{it}(0) \mid D_i=0, t < t^*].
\end{align}
Substituting and rearranging yields $\hat{\delta}_{DiD} = \text{ATT}$.
\end{proof}

\begin{proposition}[ATT from Potential Outcomes Framework]
Under SUTVA and the no-anticipation assumption $Y_{it}(1) = Y_{it}(0)$ for $t < t^*$, the ATT is identified as:
\begin{align}
\text{ATT} &= E[Y_{it}(1) - Y_{it}(0) \mid D_i = 1] \\
&= \hat{\delta}_{DiD} + \underbrace{E[Y_{it}(0) \mid D_i=1, t \geq t^*] - E[Y_{it}(0) \mid D_i=1, t < t^*]}_{\text{counterfactual trend}} \\
&\quad - \underbrace{E[Y_{it}(0) \mid D_i=0, t \geq t^*] - E[Y_{it}(0) \mid D_i=0, t < t^*]}_{\text{control trend}},
\end{align}
which equals $\hat{\delta}_{DiD}$ under parallel trends.
\end{proof}

\noindent\textbf{Variance of the DiD estimator under clustering.} The Lagrangian for the constrained estimation problem is
\begin{align}
\mathcal{L}(\delta, \lambda) &= \sum_{i=1}^{N}\sum_{t=1}^{T} (Y_{it} - X_{it}'\beta - \delta D_{it})^2 + \lambda \left(\left\lfloor M_T / 2 \right\rfloor - \text{rank}(\hat{\Sigma})\right).
\end{align}
The cluster-robust variance estimator employs the double summation
\begin{align}
\hat{V}_{CR} &= \left(\sum_{i=1}^{N}\sum_{t=1}^{T} X_{it} X_{it}'\right)^{-1}\!\left(\sum_{c=1}^{C} \hat{U}_c' \hat{U}_c\right)\!\left(\sum_{i=1}^{N}\sum_{t=1}^{T} X_{it} X_{it}'\right)^{-1}.
\end{align}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-labor",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec(
        "Introduction", "sec:intro",
        text_paragraphs=23,
        tables=[],
        equations=[eq_did],
    )

    inst_background = SectionSpec(
        "Institutional Background", "sec:background",
        text_paragraphs=19,
        subsections=[
            SectionSpec("Minimum Wage Legislation", "sec:background-mw", level=2, text_paragraphs=14),
            SectionSpec("New Jersey Labor Market", "sec:background-nj", level=2, text_paragraphs=10),
        ],
    )

    theory = SectionSpec(
        "Theoretical Framework", "sec:theory",
        text_paragraphs=16,
        equations=[eq_parallel, eq_att],
    )

    data = SectionSpec(
        "Data", "sec:data",
        text_paragraphs=14,
        tables=[summary_stats, balance_table],
        subsections=[
            SectionSpec("Establishment Survey Data", "sec:data-survey", level=2, text_paragraphs=11),
            SectionSpec("Outcome Variables", "sec:data-outcomes", level=2, text_paragraphs=10),
            SectionSpec("Sample Construction", "sec:data-sample", level=2, text_paragraphs=10),
        ],
    )

    empirical = SectionSpec(
        "Empirical Strategy", "sec:empirical",
        text_paragraphs=16,
        equations=[eq_twfe, eq_event, eq_triple],
        subsections=[
            SectionSpec("Difference-in-Differences Design", "sec:empirical-did", level=2, text_paragraphs=12),
            SectionSpec("Identification Assumptions", "sec:empirical-id", level=2, text_paragraphs=12),
        ],
    )

    results = SectionSpec(
        "Results", "sec:results",
        text_paragraphs=10,
        tables=[did_main, event_study, triple_diff],
        subsections=[
            SectionSpec("Main Employment Effects", "sec:results-main", level=2, text_paragraphs=8, tables=[did_main]),
            SectionSpec("Event Study", "sec:results-event", level=2, text_paragraphs=7, tables=[event_study]),
            SectionSpec("Heterogeneity", "sec:results-hetero", level=2, text_paragraphs=8,
                        tables=[subgroup_male, subgroup_female]),
        ],
    )

    robustness = SectionSpec(
        "Robustness", "sec:robustness",
        text_paragraphs=10,
        tables=[placebo_outcomes, alt_control, dose_response, state_trends],
        subsections=[
            SectionSpec("Placebo Tests", "sec:robust-placebo", level=2, text_paragraphs=7),
            SectionSpec("Alternative Control Groups", "sec:robust-control", level=2, text_paragraphs=7),
            SectionSpec("Dose-Response and Trends", "sec:robust-dose", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Proofs", "sec:appendix-a",
        text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Additional Results", "sec:appendix-b",
        text_paragraphs=4,
        tables=[appendix_full, triple_diff],
    )

    appendix_c = SectionSpec(
        "Appendix C: Data Construction", "sec:appendix-c",
        text_paragraphs=6,
        tables=[summary_stats],
    )

    return PaperSpec(
        paper_id="02",
        field_slug="labor",
        title="Minimum Wages and Employment: A Natural Experiment from the New Jersey--Pennsylvania Border",
        authors="Priya Nair, Marcus Okonkwo, Svetlana Ivanova",
        journal_style="working_paper",
        abstract=(
            "We exploit New Jersey's 1992 minimum wage increase as a natural experiment to identify "
            "employment effects. Using a difference-in-differences design with Pennsylvania border counties "
            "as controls, we find that the policy raised employment rates by 3.8 percentage points and log "
            "weekly earnings by 6.2 percent. Event study estimates show no pre-trends and persistent "
            "post-treatment effects. Subgroup analysis reveals larger effects for female workers. "
            "Placebo tests and robustness exercises confirm the validity of the parallel trends assumption."
        ),
        sections=[intro, inst_background, theory, data, empirical, results, robustness, conclusion,
                  appendix_a, appendix_b, appendix_c],
        bibliography_entries=[
            r"\bibitem{card1994} Card, D. and Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. \textit{American Economic Review}, 84(4), 772--793.",
            r"\bibitem{callaway2021} Callaway, B. and Sant'Anna, P. H. C. (2021). Difference-in-Differences with Multiple Time Periods. \textit{Journal of Econometrics}, 225(2), 200--230.",
            r"\bibitem{roth2023} Roth, J., Sant'Anna, P. H. C., Bilinski, A., and Poe, J. (2023). What's Trending in Difference-in-Differences? \textit{Journal of Econometrics}, 235(2), 2218--2244.",
            r"\bibitem{goodman2021} Goodman-Bacon, A. (2021). Difference-in-Differences with Variation in Treatment Timing. \textit{Journal of Econometrics}, 225(2), 254--277.",
            r"\bibitem{sun2021} Sun, L. and Abraham, S. (2021). Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects. \textit{Journal of Econometrics}, 225(2), 175--199.",
            r"\bibitem{neumark2000} Neumark, D. and Wascher, W. (2000). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania: Comment. \textit{American Economic Review}, 90(5), 1362--1396.",
            r"\bibitem{dube2010} Dube, A., Lester, T. W., and Reich, M. (2010). Minimum Wage Effects Across State Borders: Estimates Using Contiguous Counties. \textit{Review of Economics and Statistics}, 92(4), 945--964.",
        ],
        target_pages=55,
        qa=[
            {"question": "What is the main identification strategy in this paper?", "answer": "Difference-in-differences exploiting NJ's 1992 minimum wage increase with PA border counties as control"},
            {"question": "What is the main finding for employment?", "answer": "Employment rates increased by 3.8 percentage points in the treatment group"},
            {"question": "What is the main finding for earnings?", "answer": "Log weekly earnings increased by 6.2 percent"},
            {"question": "Do pre-trend tests support the parallel trends assumption?", "answer": "Yes, event study coefficients at tau=-3 and tau=-2 are small and insignificant"},
            {"question": "What is the sample period?", "answer": "1990 to 1996"},
        ],
    )


PAPER_BUILDERS["02"] = _paper_02_labor
