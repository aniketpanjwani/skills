#!/usr/bin/env python3
"""Paper builder for paper 04 (Public Finance)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_04_public_finance() -> PaperSpec:
    # --- Tables ---
    summary_stats = render_regression_table({
        "table_id": "summary-stats-pf",
        "caption": "Summary Statistics",
        "label": "tab:summary-stats-pf",
        "model_labels": ["Mean", "SD", "p25", "p75"],
        "panels": [{
            "dep_var": "Panel A: Child Outcomes at Age 26",
            "variables": [
                {"label": "Earnings Rank (0-100)", "coefficients": ["49.8", "28.3", "27.1", "73.2"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Annual Earnings", "coefficients": ["10.21", "1.04", "9.58", "10.91"],
                 "std_errors": ["", "", "", ""]},
                {"label": "College Attendance (0/1)", "coefficients": ["0.412", "0.492", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Mover Characteristics",
            "variables": [
                {"label": "Age at Move", "coefficients": ["9.4", "5.1", "5.0", "13.0"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Destination CZ Rank", "coefficients": ["52.1", "26.8", "30.2", "74.9"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Origin CZ Rank", "coefficients": ["48.7", "27.2", "26.8", "71.4"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations (children)", "values": ["3,048,412", "3,048,412", "3,048,412", "3,048,412"]},
            {"label": "Observations (movers)", "values": ["412,819", "412,819", "412,819", "412,819"]},
        ],
        "notes": "Sample: children born 1980-1988 tracked to age 26. Earnings from tax records.",
        "qa": [
            {"question": "What is the mean earnings rank at age 26?", "answer": "49.8"},
            {"question": "How many mover observations are in the sample?", "answer": "412,819"},
            {"question": "What is the mean age at move?", "answer": "9.4"},
        ],
    })

    summary_dest = render_regression_table({
        "table_id": "summary-by-destination",
        "caption": "Summary Statistics by Destination CZ Quintile",
        "label": "tab:summary-dest",
        "model_labels": ["Q1 (Worst)", "Q2", "Q3", "Q4", "Q5 (Best)"],
        "panels": [{
            "dep_var": "Mean Child Outcomes by Destination",
            "variables": [
                {"label": "Earnings Rank at 26", "coefficients": ["38.2", "44.1", "49.8", "55.7", "62.4"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "College Attendance", "coefficients": ["0.312", "0.362", "0.412", "0.464", "0.521"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Married at 30", "coefficients": ["0.421", "0.452", "0.482", "0.511", "0.544"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Movers", "values": ["82,564", "82,564", "82,564", "82,564", "82,564"]},
        ],
        "notes": "CZ quintiles based on mean earnings rank for permanent residents. Equal-sized quintiles.",
        "qa": [
            {"question": "What is the mean earnings rank for movers to the best quintile destination?", "answer": "62.4"},
            {"question": "What is the college attendance rate for movers to the worst quintile destination?", "answer": "0.312"},
        ],
    })

    movers_first_stage = render_regression_table({
        "table_id": "movers-first-stage",
        "caption": "First Stage: Predicted Outcomes for Permanent Residents",
        "label": "tab:movers-fs",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank",
            "variables": [
                {"label": "Predicted Rank (Dest. Perm. Residents)", "coefficients": ["0.641***", "0.612***", "0.598***", "0.584***"],
                 "std_errors": ["(0.041)", "(0.039)", "(0.042)", "(0.040)"]},
            ],
        }],
        "controls": [
            {"label": "Origin CZ FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year of Move FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Parent Income Controls", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Demographic Controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["412,819", "412,819", "412,819", "412,819"]},
            {"label": "F-statistic", "values": ["243.1", "258.4", "241.8", "236.2"]},
        ],
        "notes": "*** p<0.01. Instrument: mean earnings rank of permanent residents in destination CZ. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the first-stage coefficient in column 2?", "answer": "0.612"},
            {"question": "What is the first-stage F-statistic in column 1?", "answer": "243.1"},
        ],
    })

    exposure_main = render_regression_table({
        "table_id": "exposure-effects-main",
        "caption": "Main Exposure Effects Estimates",
        "label": "tab:exposure-main",
        "model_labels": ["OLS", "IV", "IV", "IV"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank at 26",
            "variables": [
                {"label": "Destination Place Effect", "coefficients": ["0.291***", "0.394***", "0.381***", "0.372***"],
                 "std_errors": ["(0.028)", "(0.041)", "(0.039)", "(0.037)"]},
            ],
        }],
        "controls": [
            {"label": "Origin FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Parent Income", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Demographics", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["412,819", "412,819", "412,819", "412,819"]},
            {"label": "R-squared", "values": ["0.312", "", "", ""]},
        ],
        "notes": "*** p<0.01. Place effect measured as mean rank of permanent resident children in destination CZ. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the IV exposure effect in column 2?", "answer": "0.394"},
            {"question": "What is the OLS exposure effect in column 1?", "answer": "0.291"},
            {"question": "What is the IV exposure effect in column 4?", "answer": "0.372"},
        ],
    })

    exposure_by_age = render_regression_table({
        "table_id": "exposure-by-age",
        "caption": "Exposure Effects by Age at Move",
        "label": "tab:exposure-age",
        "model_labels": ["Age 0-5", "Age 6-10", "Age 11-15", "Age 16-19"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank at 26",
            "variables": [
                {"label": "Destination Place Effect", "coefficients": ["0.452***", "0.381***", "0.284***", "0.118***"],
                 "std_errors": ["(0.059)", "(0.041)", "(0.038)", "(0.029)"]},
            ],
        }],
        "controls": [
            {"label": "Origin FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["98,412", "124,819", "118,348", "71,240"]},
        ],
        "notes": "*** p<0.01. Exposure effects decline monotonically with age at move, consistent with childhood exposure gradient.",
        "qa": [
            {"question": "What is the place effect for children moving at age 0-5?", "answer": "0.452"},
            {"question": "What is the place effect for children moving at age 16-19?", "answer": "0.118"},
        ],
    })

    childhood_exposure = render_regression_table({
        "table_id": "childhood-exposure",
        "caption": "Childhood Exposure Gradient",
        "label": "tab:childhood-exp",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank",
            "variables": [
                {"label": "Years in Destination $\\times$ Dest. Effect", "coefficients": ["0.024***", "0.023***", "0.022***", "0.021***"],
                 "std_errors": ["(0.003)", "(0.003)", "(0.004)", "(0.003)"]},
                {"label": "Years in Destination", "coefficients": ["-0.081**", "-0.078**", "-0.079**", "-0.075**"],
                 "std_errors": ["(0.038)", "(0.036)", "(0.040)", "(0.037)"]},
            ],
        }],
        "controls": [
            {"label": "Origin FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "Yes", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["412,819", "412,819", "412,819", "412,819"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Exposure gradient: each additional year in a one-rank better destination raises outcomes by 0.024 ranks.",
        "qa": [
            {"question": "What is the childhood exposure gradient coefficient in column 1?", "answer": "0.024"},
            {"question": "What is the childhood exposure gradient coefficient in column 4?", "answer": "0.021"},
        ],
    })

    event_study = render_regression_table({
        "table_id": "event-study-moves",
        "caption": "Event Study Around Family Moves",
        "label": "tab:event-moves",
        "model_labels": ["t-3", "t-2", "t+1", "t+3"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank Residual",
            "variables": [
                {"label": "Dest. Effect $\\times$ Indicator", "coefficients": ["0.002", "0.001", "0.019***", "0.034***"],
                 "std_errors": ["(0.004)", "(0.003)", "(0.006)", "(0.008)"]},
            ],
        }],
        "notes": "*** p<0.01. Pre-move coefficients are small and insignificant; post-move effects accumulate.",
        "qa": [
            {"question": "Is there evidence of pre-move sorting at t-2?", "answer": "No, coefficient is 0.001 with SE (0.003)"},
        ],
    })

    destination_chars = render_regression_table({
        "table_id": "destination-characteristics",
        "caption": "Place Effects and Destination Characteristics",
        "label": "tab:dest-chars",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: CZ-Level Place Effect",
            "variables": [
                {"label": "School Quality Index", "coefficients": ["0.218***", "0.189***", "0.194***", "0.181***"],
                 "std_errors": ["(0.041)", "(0.038)", "(0.042)", "(0.039)"]},
                {"label": "Social Capital Index", "coefficients": ["0.142***", "0.124***", "0.131***", "0.118***"],
                 "std_errors": ["(0.031)", "(0.028)", "(0.033)", "(0.030)"]},
                {"label": "Crime Rate (log)", "coefficients": ["-0.089***", "-0.081***", "-0.085***", "-0.078***"],
                 "std_errors": ["(0.019)", "(0.018)", "(0.021)", "(0.019)"]},
            ],
        }],
        "controls": [
            {"label": "Census Division FE", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "Income Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "CZs", "values": ["722", "722", "722", "722"]},
            {"label": "R-squared", "values": ["0.421", "0.491", "0.458", "0.521"]},
        ],
        "notes": "*** p<0.01. Cross-sectional regression of place effects on CZ characteristics.",
        "qa": [
            {"question": "What is the correlation between school quality and place effects in column 1?", "answer": "0.218"},
            {"question": "What is the correlation between crime rate and place effects in column 2?", "answer": "-0.081"},
        ],
    })

    origin_fe = render_regression_table({
        "table_id": "origin-fixed-effects",
        "caption": "Origin vs. Destination Fixed Effects Decomposition",
        "label": "tab:origin-fe",
        "model_labels": ["Origin Only", "Dest. Only", "Both", "Residual"],
        "panels": [{
            "dep_var": "Share of variance in child earnings rank explained",
            "variables": [
                {"label": "Share of Variance (\\%)", "coefficients": ["18.4", "21.3", "31.2", "68.8"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Variance decomposition using AKM-style estimation. Origin and destination effects together explain 31.2\\% of variance.",
        "qa": [
            {"question": "What share of variance is explained by destination fixed effects alone?", "answer": "21.3"},
            {"question": "What share of variance is explained by origin and destination together?", "answer": "31.2"},
        ],
    })

    mech_schools = render_regression_table({
        "table_id": "mechanisms-schools",
        "caption": "Mechanisms: School Quality",
        "label": "tab:mech-schools",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank",
            "variables": [
                {"label": "Dest. Effect $\\times$ School Quality (High)", "coefficients": ["0.441***", "0.418***", "0.412***", "0.401***"],
                 "std_errors": ["(0.058)", "(0.055)", "(0.061)", "(0.057)"]},
                {"label": "Dest. Effect $\\times$ School Quality (Low)", "coefficients": ["0.312***", "0.291***", "0.284***", "0.274***"],
                 "std_errors": ["(0.044)", "(0.042)", "(0.046)", "(0.043)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["412,819", "412,819", "412,819", "412,819"]},
        ],
        "notes": "*** p<0.01. High school quality defined as above-median test score growth. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the place effect for high school quality destinations in column 1?", "answer": "0.441"},
            {"question": "What is the place effect for low school quality destinations in column 2?", "answer": "0.291"},
        ],
    })

    mech_peers = render_regression_table({
        "table_id": "mechanisms-peers",
        "caption": "Mechanisms: Peer Effects",
        "label": "tab:mech-peers",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank",
            "variables": [
                {"label": "Dest. Effect $\\times$ Peer Income (High)", "coefficients": ["0.421***", "0.398***", "0.394***", "0.382***"],
                 "std_errors": ["(0.054)", "(0.051)", "(0.057)", "(0.053)"]},
                {"label": "Dest. Effect $\\times$ Peer Income (Low)", "coefficients": ["0.341***", "0.321***", "0.315***", "0.308***"],
                 "std_errors": ["(0.047)", "(0.045)", "(0.050)", "(0.046)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["412,819", "412,819", "412,819", "412,819"]},
        ],
        "notes": "*** p<0.01. Peer income measured as mean parental income in child's CZ. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the place effect for high peer income destinations in column 2?", "answer": "0.398"},
        ],
    })

    mech_crime = render_regression_table({
        "table_id": "mechanisms-crime",
        "caption": "Mechanisms: Crime and Safety",
        "label": "tab:mech-crime",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Child Earnings Rank",
            "variables": [
                {"label": "Dest. Effect $\\times$ Low Crime", "coefficients": ["0.412***", "0.389***", "0.382***", "0.371***"],
                 "std_errors": ["(0.052)", "(0.049)", "(0.054)", "(0.051)"]},
                {"label": "Dest. Effect $\\times$ High Crime", "coefficients": ["0.328***", "0.308***", "0.301***", "0.292***"],
                 "std_errors": ["(0.045)", "(0.042)", "(0.047)", "(0.044)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["412,819", "412,819", "412,819", "412,819"]},
        ],
        "notes": "*** p<0.01. Low crime defined as below-median violent crime rate per 100,000 residents.",
        "qa": [
            {"question": "What is the place effect for low crime destinations in column 1?", "answer": "0.412"},
        ],
    })

    geo_var = render_regression_table({
        "table_id": "geographic-variation",
        "caption": "Geographic Variation in Place Effects",
        "label": "tab:geo-var",
        "model_labels": ["Northeast", "Midwest", "South", "West"],
        "panels": [{
            "dep_var": "Mean Place Effect (Earnings Rank Points)",
            "variables": [
                {"label": "Mean Place Effect", "coefficients": ["52.4", "49.1", "46.8", "53.2"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Standard Deviation", "coefficients": ["12.1", "13.4", "14.8", "11.9"],
                 "std_errors": ["", "", "", ""]},
                {"label": "90th-10th Percentile Range", "coefficients": ["28.4", "31.2", "34.1", "27.8"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Geographic distribution of CZ-level place effects. West has highest mean and least within-region dispersion.",
        "qa": [
            {"question": "Which region has the highest mean place effect?", "answer": "West, with mean 53.2"},
            {"question": "Which region has the largest 90th-10th percentile range?", "answer": "South, with range 34.1"},
        ],
    })

    correlates = render_regression_table({
        "table_id": "correlates-of-place-effects",
        "caption": "Correlates of Place Effects",
        "label": "tab:correlates",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: CZ Place Effect (Earnings Rank)",
            "variables": [
                {"label": "Income Segregation (Theil)", "coefficients": ["-4.812***", "-4.219***", "-4.381***", "-4.018***"],
                 "std_errors": ["(0.841)", "(0.781)", "(0.862)", "(0.811)"]},
                {"label": "Upward Mobility (p25 parents)", "coefficients": ["0.641***", "0.598***", "0.612***", "0.581***"],
                 "std_errors": ["(0.081)", "(0.075)", "(0.084)", "(0.079)"]},
                {"label": "Single Parent Share", "coefficients": ["-8.142***", "-7.481***", "-7.812***", "-7.214***"],
                 "std_errors": ["(1.241)", "(1.181)", "(1.298)", "(1.218)"]},
            ],
        }],
        "controls": [
            {"label": "Division FE", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "Income Controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "CZs", "values": ["722", "722", "722", "722"]},
            {"label": "R-squared", "values": ["0.481", "0.541", "0.512", "0.568"]},
        ],
        "notes": "*** p<0.01. Cross-CZ regression. Income segregation measured by Theil index.",
        "qa": [
            {"question": "What is the correlation between income segregation and place effects in column 1?", "answer": "-4.812"},
            {"question": "What is the correlation between single parent share and place effects in column 2?", "answer": "-7.481"},
        ],
    })

    appendix_selection = render_regression_table({
        "table_id": "appendix-selection",
        "caption": "Appendix: Selection on Observables Tests",
        "label": "tab:appendix-selection",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Destination Place Effect",
            "variables": [
                {"label": "Parent Income (log)", "coefficients": ["0.018**", "0.012", "0.009", "0.007"],
                 "std_errors": ["(0.008)", "(0.009)", "(0.010)", "(0.011)"]},
                {"label": "Parent Education", "coefficients": ["0.014*", "0.009", "0.006", "0.004"],
                 "std_errors": ["(0.008)", "(0.009)", "(0.010)", "(0.011)"]},
            ],
        }],
        "notes": "** p<0.05, * p<0.1. Selection on observables is modest and controlled for in main specification.",
        "qa": [
            {"question": "Is parental income predictive of destination choice in column 3?", "answer": "No, coefficient is 0.009 and insignificant"},
        ],
    })

    appendix_attrition = render_regression_table({
        "table_id": "appendix-attrition",
        "caption": "Appendix: Attrition Analysis",
        "label": "tab:appendix-attrition",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Missing at Age 26 (0/1)",
            "variables": [
                {"label": "Destination Place Effect", "coefficients": ["0.002", "0.001", "0.001", "0.001"],
                 "std_errors": ["(0.003)", "(0.003)", "(0.004)", "(0.003)"]},
            ],
        }],
        "notes": "Destination place effect does not predict attrition, suggesting no differential selection out of sample.",
        "qa": [
            {"question": "Does the destination place effect predict attrition from the sample?", "answer": "No, coefficient is 0.002 and insignificant"},
        ],
    })

    # --- Equations ---
    eq_movers = EquationSpec(
        "movers-model",
        r"Y_{i,t-1}^{(k)} = \dot{\alpha}_{o(i)} + \ddot{\psi}_{d(i)} + \varepsilon_{i,t-1}^{(k)}, \quad \underset{\psi}{\operatorname{arg\,max}}\; \mathcal{L}(\psi | Y, X)",
        "eq:movers",
        "Movers model: child outcome $Y_i$ decomposed into origin $o(i)$ and destination $d(i)$ effects.",
        [{"question": "What does psi_d identify in the movers model?", "answer": "The place effect of destination CZ d"}],
    )

    eq_exposure = EquationSpec(
        "exposure-effects",
        r"Y_i = \alpha + \beta \cdot \psi_{d(i)} + X_i'\gamma + \varepsilon_i",
        "eq:exposure-pf",
        "Exposure effects regression: child outcome on destination place effect, conditional on origin.",
    )

    eq_childhood_gradient = EquationSpec(
        "childhood-gradient",
        r"Y_i = \alpha + \sum_a \delta_a \cdot \mathbf{1}[\text{Age at move} = a] \cdot \psi_{d(i)} + X_i'\gamma + \varepsilon_i",
        "eq:childhood-gradient",
        "Childhood exposure gradient: exposure effect varies by age at move $a$.",
    )

    eq_place_fe = EquationSpec(
        "place-fixed-effect",
        r"\psi_c = E[Y_i \mid o(i) = c, \text{perm. resident}] - \bar{Y}",
        "eq:place-fe",
        "Place fixed effect: demeaned mean outcome for permanent resident children in CZ $c$.",
    )

    eq_selection = EquationSpec(
        "selection-equation",
        r"D_{oc} = \Pr(\text{move to } c \mid \text{origin} = o) = f\!\left(\dot{\psi}_c - \dot{\psi}_o,\; x_{i,t-1}^{(k)},\; \ddot{X}_{o}\right)",
        "eq:selection",
        "Selection equation: probability of moving from $o$ to $c$ depends on place effect differential.",
    )

    eq_decomp = EquationSpec(
        "decomp-place",
        r"\text{Var}(Y_{i,t-1}^{(k)}) = \text{Var}(\dot{\alpha}_{o(i)}) + \text{Var}(\ddot{\psi}_{d(i)}) + 2\text{Cov}(\dot{\alpha}_{o(i)}, \ddot{\psi}_{d(i)}) + \text{Var}(\varepsilon_{i,t-1}^{(k)})",
        "eq:decomp-place",
        "Variance decomposition of child outcomes into origin, destination, and residual components.",
    )

    eq_ch_estimator = EquationSpec(
        "chetty-hendren-estimator",
        r"\hat{\\beta}_{CH} = \\frac{\\sum_i (\\psi_{d(i)} - \\bar{\\psi}) \\cdot (Y_i - \\hat{\\alpha}_{o(i)})}{\\sum_i (\\psi_{d(i)} - \\bar{\\psi})^2}",
        "eq:ch-estimator",
        "Chetty-Hendren estimator: IV estimator projecting residualized outcomes on place effects.",
    )

    eq_forecast_bias = EquationSpec(
        "forecast-bias",
        r"\\hat{\\beta}^{BC} = \\hat{\\beta} \\cdot \\left(1 - \\frac{\\text{Var}(\\hat{\\psi}_c - \\psi_c)}{\\text{Var}(\\hat{\\psi}_c)}\\right)^{-1}",
        "eq:forecast-bias",
        "Forecast-bias correction: shrinkage correction for estimation error in place effects.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[Identification of Place Effects with Selection]
Suppose movers select destinations on place effects, so $\text{Cov}(\alpha_{o(i)}, \psi_{d(i)}) \neq 0$. The OLS estimate of $\hat{\beta}$ is biased. Under the assumption that conditional on origin fixed effects, move timing is independent of unobservables,
\begin{align}
E[\hat{\beta}_{IV} \mid \text{origin FE}] &= \beta + \frac{\text{Cov}(\psi_{d(i)}, \varepsilon_i \mid \alpha_{o(i)})}{\text{Var}(\psi_{d(i)} \mid \alpha_{o(i)})}.
\end{align}
If $\text{Cov}(\psi_{d(i)}, \varepsilon_i \mid \alpha_{o(i)}) = 0$ (conditional mean independence), then $\hat{\beta}_{IV}$ is consistent.
\end{proposition}

\begin{proof}
Partial out origin fixed effects by regressing $Y_i$ and $\psi_{d(i)}$ on origin dummies. Let $\tilde{Y}_i = Y_i - \hat{\alpha}_{o(i)}$ and $\tilde{\psi}_{d(i)} = \psi_{d(i)} - E[\psi_{d(i)} \mid o(i)]$. Then
\begin{align}
\text{plim}\, \hat{\beta}_{IV} &= \beta + \frac{E[\tilde{\psi}_{d(i)} \varepsilon_i]}{E[\tilde{\psi}_{d(i)}^2]}.
\end{align}
The numerator is zero under conditional mean independence.
\end{proof}

\begin{proposition}[Bias Correction for Estimation Error in Place Effects]
Let $\hat{\psi}_c = \psi_c + \eta_c$ where $\eta_c \sim (0, \sigma^2_\eta)$ is estimation error. The OLS estimate satisfies
\begin{align}
\text{plim}\, \hat{\beta}_{OLS} &= \beta \cdot \frac{\text{Var}(\psi_c)}{\text{Var}(\psi_c) + \sigma^2_\eta} = \beta \cdot \lambda,
\end{align}
where $\lambda \in (0,1)$ is the reliability ratio. The bias-corrected estimator is
\begin{align}
\hat{\beta}^{BC} &= \hat{\beta}_{OLS} / \hat{\lambda}, \quad \hat{\lambda} = 1 - \frac{\hat{\sigma}^2_\eta}{\widehat{\text{Var}}(\hat{\psi}_c)}.
\end{align}
\end{proposition}

\begin{proposition}[Exposure Effects are Identified from Movers]
Let $m = \text{age at move}$ and $M = 18$ be the age of majority. Under the childhood exposure model $Y_i = \alpha_{o(i)} + (M - m_i)/M \cdot \psi_{d(i)} + \varepsilon_i$, the exposure effect is identified from cross-sibling variation in move timing:
\begin{align}
E[Y_i - Y_j \mid o(i) = o(j), d(i) = d(j)] &= \frac{m_j - m_i}{M} \cdot \psi_{d(i)},
\end{align}
which isolates the causal effect of additional years of exposure, purged of selection.
\end{proposition}

\noindent\textbf{Optimal allocation derivation.} The social planner's problem is
\begin{align}
\underset{\psi}{\operatorname{arg\,max}} &\sum_{c=1}^{C} \dot{W}_c(\ddot{\psi}_c), \quad \text{s.t.} \quad \sum_{c=1}^{C} x_{c,t-1}^{(k)} \leq B.
\end{align}
Under the maintained assumptions, the first-order condition yields the nested subscript expression
\begin{align}
\frac{\partial \dot{W}_c}{\partial \ddot{\psi}_{d(i)}} &= \lambda \cdot x_{i,t-1}^{(k)} \quad \forall\, c = 1,\ldots,C.
\end{align}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-pf",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-pf", text_paragraphs=14, equations=[eq_movers])

    background = SectionSpec("Institutional Background", "sec:bg-pf", text_paragraphs=10)

    theory = SectionSpec(
        "Theoretical Framework", "sec:theory-pf", text_paragraphs=12,
        equations=[eq_exposure, eq_place_fe, eq_decomp],
        subsections=[
            SectionSpec("Movers Model", "sec:theory-movers", level=2, text_paragraphs=8),
            SectionSpec("Selection and Identification", "sec:theory-id", level=2, text_paragraphs=8),
            SectionSpec("Variance Decomposition", "sec:theory-decomp", level=2, text_paragraphs=7),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-pf", text_paragraphs=10,
        tables=[summary_stats, summary_dest],
        subsections=[
            SectionSpec("Tax Records", "sec:data-tax", level=2, text_paragraphs=7),
            SectionSpec("Geographic Definitions", "sec:data-geo", level=2, text_paragraphs=6),
            SectionSpec("Outcome Measures", "sec:data-outcomes", level=2, text_paragraphs=6),
        ],
    )

    empirical = SectionSpec(
        "Empirical Strategy", "sec:empirical-pf", text_paragraphs=12,
        equations=[eq_childhood_gradient, eq_selection, eq_ch_estimator, eq_forecast_bias],
        tables=[movers_first_stage],
        subsections=[
            SectionSpec("Identification Strategy", "sec:empirical-id-pf", level=2, text_paragraphs=9),
            SectionSpec("Estimation of Place Effects", "sec:empirical-pe", level=2, text_paragraphs=8),
            SectionSpec("Bias Correction", "sec:empirical-bc", level=2, text_paragraphs=7),
        ],
    )

    main_results = SectionSpec(
        "Main Results", "sec:results-pf", text_paragraphs=10,
        tables=[exposure_main, exposure_by_age, childhood_exposure, event_study],
        subsections=[
            SectionSpec("Average Exposure Effects", "sec:results-avg", level=2, text_paragraphs=8),
            SectionSpec("Age Gradient", "sec:results-age", level=2, text_paragraphs=7),
            SectionSpec("Event Study Evidence", "sec:results-event", level=2, text_paragraphs=7),
            SectionSpec("Variance Decomposition Results", "sec:results-decomp", level=2, text_paragraphs=7, tables=[origin_fe]),
        ],
    )

    mechanisms = SectionSpec(
        "Mechanisms", "sec:mechanisms-pf", text_paragraphs=10,
        tables=[destination_chars, correlates, mech_schools, mech_peers, mech_crime],
        subsections=[
            SectionSpec("Schools", "sec:mech-schools", level=2, text_paragraphs=8),
            SectionSpec("Peers", "sec:mech-peers", level=2, text_paragraphs=7),
            SectionSpec("Crime and Safety", "sec:mech-crime", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-pf", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Identification Proofs", "sec:appendix-a-pf", text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Additional Results", "sec:appendix-b-pf", text_paragraphs=4,
        tables=[geo_var, appendix_selection],
    )

    appendix_c = SectionSpec(
        "Appendix C: Geographic Detail", "sec:appendix-c-pf", text_paragraphs=5,
    )

    appendix_d = SectionSpec(
        "Appendix D: Selection Analysis", "sec:appendix-d-pf", text_paragraphs=5,
        tables=[appendix_attrition],
    )

    return PaperSpec(
        paper_id="04",
        field_slug="public-finance",
        title="Where You Grow Up Matters: Childhood Exposure Effects and the Role of Place",
        authors="Amara Diallo, Yuki Nakamura, Sofia Herrera",
        journal_style="qje",
        abstract=(
            "We estimate the causal effect of growing up in higher-opportunity neighborhoods on children's "
            "long-run outcomes using tax records for 3 million children. Exploiting variation in age at move "
            "among families that relocate across commuting zones, we find that each year of childhood exposure "
            "to a one-rank-better destination raises earnings rank at age 26 by 0.024 ranks. The exposure "
            "gradient declines from 0.452 for moves at ages 0-5 to 0.118 for moves at ages 16-19. "
            "Mechanisms include school quality, peer effects, and crime rates. Selection tests confirm that "
            "the estimates reflect causal place effects rather than sorting."
        ),
        sections=[intro, background, theory, data, empirical, main_results, mechanisms, conclusion,
                  appendix_a, appendix_b, appendix_c, appendix_d],
        bibliography_entries=[
            r"\bibitem{chetty2018} Chetty, R. and Hendren, N. (2018). The Impacts of Neighborhoods on Intergenerational Mobility I: Childhood Exposure Effects. \textit{Quarterly Journal of Economics}, 133(3), 1107--1162.",
            r"\bibitem{chetty2016} Chetty, R., Hendren, N., and Katz, L. F. (2016). The Effects of Exposure to Better Neighborhoods on Children: New Evidence from the Moving to Opportunity Experiment. \textit{American Economic Review}, 106(4), 855--902.",
            r"\bibitem{abowd1999} Abowd, J., Kramarz, F., and Margolis, D. (1999). High Wage Workers and High Wage Firms. \textit{Econometrica}, 67(2), 251--333.",
            r"\bibitem{raj2020} Raj, A., Kline, P., and Walters, C. (2020). Leave-Out Estimation of Variance Components. \textit{Econometrica}, 88(5), 1859--1898.",
            r"\bibitem{chetty2014} Chetty, R., Hendren, N., Kline, P., and Saez, E. (2014). Where is the Land of Opportunity? The Geography of Intergenerational Mobility in the United States. \textit{Quarterly Journal of Economics}, 129(4), 1553--1623.",
        ],
        target_pages=85,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "Comparing siblings who moved at different ages to the same destination, exploiting variation in childhood exposure duration"},
            {"question": "What is the main finding on childhood exposure?", "answer": "Each additional year of exposure to a one-rank-better destination raises earnings rank by 0.024 ranks"},
            {"question": "How does the exposure effect vary with age at move?", "answer": "It declines from 0.452 for moves at age 0-5 to 0.118 for moves at age 16-19"},
            {"question": "What is the IV estimate of the average place effect?", "answer": "0.394 in the baseline specification"},
            {"question": "How many children are in the total sample?", "answer": "3,048,412"},
        ],
    )


PAPER_BUILDERS["04"] = _paper_04_public_finance
