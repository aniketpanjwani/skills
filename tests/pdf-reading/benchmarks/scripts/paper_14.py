#!/usr/bin/env python3
"""Paper builder for paper 14 (Behavioral)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_14_behavioral() -> PaperSpec:
    # --- Tables ---
    gym_summary = render_regression_table({
        "table_id": "gym-summary",
        "caption": "Summary Statistics: Health Club Members",
        "label": "tab:gym-summary",
        "model_labels": ["Mean", "SD", "p10", "p90"],
        "panels": [{
            "dep_var": "Panel A: Contract Choice at Enrollment",
            "variables": [
                {"label": "Monthly Contract (1=yes)", "coefficients": ["0.614", "0.487", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Annual Contract (1=yes)", "coefficients": ["0.241", "0.428", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Pay-Per-Visit (1=yes)", "coefficients": ["0.145", "0.352", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Attendance and Tenure",
            "variables": [
                {"label": "Average Monthly Visits", "coefficients": ["4.17", "4.02", "0.50", "9.50"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Monthly Contract Duration (months)", "coefficients": ["8.22", "9.14", "1.00", "21.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Average Monthly Fee Paid (\\$)", "coefficients": ["70.14", "18.32", "49.00", "94.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Cost per Visit (\\$)", "coefficients": ["17.80", "19.41", "6.50", "42.00"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel C: Demographic Characteristics",
            "variables": [
                {"label": "Age", "coefficients": ["33.8", "10.2", "22.0", "49.0"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Female (1=yes)", "coefficients": ["0.481", "0.500", "0.00", "1.00"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Distance to Club (miles)", "coefficients": ["2.14", "1.88", "0.41", "4.82"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations (members)", "values": ["7,752", "7,752", "7,752", "7,752"]},
            {"label": "Member-month observations", "values": ["74,661", "74,661", "74,661", "74,661"]},
        ],
        "notes": "Sample covers three US health clubs, 1997-2001. Pay-per-visit fee is \\$10 per visit. Monthly flat rate \\$70/month. Annual contract \\$58.33/month equivalent.",
        "qa": [
            {"question": "What fraction of members choose the monthly contract?", "answer": "0.614"},
            {"question": "What is the average monthly visits for health club members?", "answer": "4.17"},
            {"question": "What is the average cost per visit for monthly contract holders?", "answer": "\\$17.80"},
            {"question": "How many member-month observations are in the sample?", "answer": "74,661"},
        ],
    })

    contract_choice = render_regression_table({
        "table_id": "contract-choice",
        "caption": "Contract Choice at Enrollment: Multinomial Logit",
        "label": "tab:contract-choice",
        "model_labels": ["Monthly", "Annual", "Pay-per-visit"],
        "panels": [{
            "dep_var": "Panel A: Predicted Attendance Beliefs",
            "variables": [
                {"label": "Forecasted Monthly Visits", "coefficients": ["0.312***", "0.284***", "--"],
                 "std_errors": ["(0.041)", "(0.052)", ""]},
                {"label": "Forecasted Visits$^2$", "coefficients": ["-0.018***", "-0.014**", "--"],
                 "std_errors": ["(0.005)", "(0.006)", ""]},
                {"label": "Survey: Expects to Go Often", "coefficients": ["0.841***", "0.612***", "--"],
                 "std_errors": ["(0.094)", "(0.108)", ""]},
            ],
        }, {
            "dep_var": "Panel B: Demographics",
            "variables": [
                {"label": "Age / 10", "coefficients": ["-0.084**", "-0.091**", "-0.071*"],
                 "std_errors": ["(0.038)", "(0.044)", "(0.041)"]},
                {"label": "Female", "coefficients": ["0.142***", "0.121**", "0.061"],
                 "std_errors": ["(0.051)", "(0.058)", "(0.054)"]},
                {"label": "Log Distance", "coefficients": ["-0.224***", "-0.198***", "-0.241***"],
                 "std_errors": ["(0.028)", "(0.034)", "(0.031)"]},
            ],
        }],
        "controls": [
            {"label": "Club FE", "values": ["Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["7,752", "7,752", "7,752"]},
            {"label": "Pseudo R-squared", "values": ["0.184", "0.184", "0.184"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Base category is pay-per-visit. Coefficients from joint multinomial logit. Robust SEs in parentheses.",
        "qa": [
            {"question": "What is the coefficient on forecasted monthly visits for choosing monthly contract?", "answer": "0.312"},
            {"question": "What is the coefficient on log distance for pay-per-visit?", "answer": "-0.241"},
            {"question": "What is the pseudo R-squared for the contract choice model?", "answer": "0.184"},
        ],
    })

    attendance = render_regression_table({
        "table_id": "attendance",
        "caption": "Monthly Attendance Regressions",
        "label": "tab:attendance",
        "model_labels": ["(1) OLS", "(2) Poisson", "(3) FE", "(4) FE+Controls"],
        "panels": [{
            "dep_var": "Dep. var.: Visits per Month",
            "variables": [
                {"label": "Monthly Contract", "coefficients": ["-1.842***", "-0.412***", "-1.614***", "-1.589***"],
                 "std_errors": ["(0.184)", "(0.041)", "(0.201)", "(0.198)"]},
                {"label": "Annual Contract", "coefficients": ["-0.914***", "-0.218***", "-0.781***", "-0.764***"],
                 "std_errors": ["(0.214)", "(0.051)", "(0.228)", "(0.224)"]},
                {"label": "Months Since Join", "coefficients": ["-0.084***", "-0.021***", "-0.091***", "-0.088***"],
                 "std_errors": ["(0.014)", "(0.004)", "(0.016)", "(0.015)"]},
                {"label": "Log Distance", "coefficients": ["-0.481***", "-0.118***", "--", "--"],
                 "std_errors": ["(0.061)", "(0.015)", "", ""]},
                {"label": "Summer (June-Aug)", "coefficients": ["0.312***", "0.074***", "0.298***", "0.291***"],
                 "std_errors": ["(0.082)", "(0.019)", "(0.084)", "(0.083)"]},
            ],
        }],
        "controls": [
            {"label": "Member FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Month FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Demographics", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["74,661", "74,661", "74,661", "74,661"]},
            {"label": "R-squared / Log-likelihood", "values": ["0.142", "--", "0.481", "0.494"]},
            {"label": "Mean Dep. Var.", "values": ["4.17", "4.17", "4.17", "4.17"]},
        ],
        "notes": "*** p<0.01. Omitted category: pay-per-visit. Column (2) is Poisson quasi-MLE. Robust SEs clustered by member.",
        "qa": [
            {"question": "What is the OLS coefficient on monthly contract in column 1?", "answer": "-1.842"},
            {"question": "What is the FE coefficient on monthly contract in column 3?", "answer": "-1.614"},
            {"question": "What is the mean of the dependent variable?", "answer": "4.17 visits per month"},
            {"question": "What is the R-squared in column 4?", "answer": "0.494"},
        ],
    })

    reduced_form = render_regression_table({
        "table_id": "reduced-form",
        "caption": "Reduced-Form Evidence for Present Bias: Monthly vs. Pay-Per-Visit",
        "label": "tab:reduced-form",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Panel A: Dep. var. = 1(Monthly Contract Dominated)",
            "variables": [
                {"label": "Average Monthly Visits $< 4.5$", "coefficients": ["0.484***", "0.471***", "0.468***", "0.461***"],
                 "std_errors": ["(0.038)", "(0.037)", "(0.039)", "(0.038)"]},
                {"label": "Survey Attendance Overestimate", "coefficients": ["0.214***", "0.208***", "0.211***", "0.204***"],
                 "std_errors": ["(0.041)", "(0.040)", "(0.042)", "(0.041)"]},
            ],
        }, {
            "dep_var": "Panel B: Dep. var. = Monthly Fee / Visits (Cost per Visit)",
            "variables": [
                {"label": "Monthly Contract $\\times$ Low Visits", "coefficients": ["11.84***", "11.21***", "10.98***", "10.74***"],
                 "std_errors": ["(1.41)", "(1.38)", "(1.44)", "(1.41)"]},
                {"label": "Months in Club", "coefficients": ["0.142***", "0.138***", "0.141***", "0.135***"],
                 "std_errors": ["(0.028)", "(0.027)", "(0.029)", "(0.028)"]},
            ],
        }],
        "controls": [
            {"label": "Club FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Demographics", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["7,752", "7,752", "7,752", "7,752"]},
            {"label": "R-squared", "values": ["0.091", "0.118", "0.134", "0.152"]},
        ],
        "notes": "*** p<0.01. Monthly contract is dominated when cost per visit exceeds \\$10 pay-per-visit fee. Robust SEs.",
        "qa": [
            {"question": "What is the coefficient on low-visit indicator in the dominated contract regression (column 1)?", "answer": "0.484"},
            {"question": "What is the R-squared in column 4 of panel A?", "answer": "0.152"},
            {"question": "What is the coefficient on monthly contract times low visits in panel B, column 1?", "answer": "11.84"},
        ],
    })

    hazard_cancellation = render_regression_table({
        "table_id": "hazard-cancellation",
        "caption": "Hazard Model of Contract Cancellation",
        "label": "tab:hazard-cancellation",
        "model_labels": ["Cox (1)", "Cox (2)", "Weibull", "Log-logistic"],
        "panels": [{
            "dep_var": "Hazard of Cancellation (monthly contract members)",
            "variables": [
                {"label": "Lagged Monthly Visits", "coefficients": ["-0.084***", "-0.081***", "-0.088***", "-0.086***"],
                 "std_errors": ["(0.011)", "(0.011)", "(0.012)", "(0.012)"]},
                {"label": "Lagged Visits$^2$", "coefficients": ["0.004***", "0.004***", "0.005***", "0.004***"],
                 "std_errors": ["(0.001)", "(0.001)", "(0.001)", "(0.001)"]},
                {"label": "Months in Club", "coefficients": ["0.021***", "0.020***", "--", "--"],
                 "std_errors": ["(0.004)", "(0.004)", "", ""]},
                {"label": "Female", "coefficients": ["-0.112***", "-0.104***", "-0.118***", "-0.114***"],
                 "std_errors": ["(0.038)", "(0.037)", "(0.040)", "(0.039)"]},
                {"label": "Age / 10", "coefficients": ["-0.048**", "-0.044**", "-0.051**", "-0.049**"],
                 "std_errors": ["(0.021)", "(0.020)", "(0.022)", "(0.021)"]},
            ],
        }],
        "controls": [
            {"label": "Club FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations (member-months)", "values": ["45,801", "45,801", "45,801", "45,801"]},
            {"label": "Cancellation events", "values": ["5,614", "5,614", "5,614", "5,614"]},
            {"label": "Log-likelihood", "values": ["-38,421", "-38,284", "-38,614", "-38,518"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Dependent variable: cancellation in month $t+1$. Coefficients are log hazard ratios. Robust SEs.",
        "qa": [
            {"question": "What is the hazard ratio coefficient on lagged monthly visits in Cox model (1)?", "answer": "-0.084"},
            {"question": "How many cancellation events are observed?", "answer": "5,614"},
            {"question": "What is the coefficient on months in club in Cox model (2)?", "answer": "0.020"},
        ],
    })

    structural_beta_delta = render_regression_table({
        "table_id": "structural-beta-delta",
        "caption": "Structural Estimates: Beta-Delta Parameters",
        "label": "tab:structural-beta-delta",
        "model_labels": ["(1) Baseline", "(2) + Demographics", "(3) Heterogeneous", "(4) Naive Only"],
        "panels": [{
            "dep_var": "Present Bias and Long-Run Patience Parameters",
            "variables": [
                {"label": "$\\hat{\\beta}$ (present bias)", "coefficients": ["0.712***", "0.718***", "--", "0.694***"],
                 "std_errors": ["(0.031)", "(0.033)", "", "(0.042)"]},
                {"label": "$\\hat{\\delta}$ (monthly discount factor)", "coefficients": ["0.981***", "0.982***", "0.980***", "0.983***"],
                 "std_errors": ["(0.004)", "(0.004)", "(0.005)", "(0.005)"]},
                {"label": "$\\hat{\\beta}$ (naive agents)", "coefficients": ["--", "--", "0.681***", "--"],
                 "std_errors": ["", "", "(0.048)", ""]},
                {"label": "$\\hat{\\beta}$ (sophisticated agents)", "coefficients": ["--", "--", "0.741***", "--"],
                 "std_errors": ["", "", "(0.038)", ""]},
            ],
        }, {
            "dep_var": "Overconfidence Parameters",
            "variables": [
                {"label": "$\\hat{\\theta}$ (overconfidence level)", "coefficients": ["0.591***", "0.582***", "0.614***", "0.641***"],
                 "std_errors": ["(0.048)", "(0.047)", "(0.051)", "(0.058)"]},
                {"label": "Sophistication share ($\\hat{\\pi}$)", "coefficients": ["--", "--", "0.381**", "--"],
                 "std_errors": ["", "", "(0.164)", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["7,752", "7,752", "7,752", "4,761"]},
            {"label": "Log-likelihood", "values": ["-14,821", "-14,684", "-14,512", "-9,284"]},
            {"label": "Parameters", "values": ["12", "18", "16", "10"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Estimated by MLE. Bootstrap SEs (500 replications). Column (3): mixture model with fraction $\\hat{\\pi}$ sophisticated. Column (4): naive agent subsample defined by overconfidence $\\theta > 0.5$.",
        "qa": [
            {"question": "What is the baseline estimate of beta (present bias)?", "answer": "0.712"},
            {"question": "What is the estimated monthly discount factor delta?", "answer": "0.981"},
            {"question": "What is the overconfidence parameter theta in the baseline?", "answer": "0.591"},
            {"question": "What fraction of agents are estimated to be sophisticated?", "answer": "0.381"},
        ],
    })

    structural_preferences = render_regression_table({
        "table_id": "structural-preferences",
        "caption": "Structural Estimates: Per-Visit Benefits and Costs",
        "label": "tab:structural-preferences",
        "model_labels": ["(1) Baseline", "(2) Log utility", "(3) Quadratic", "(4) Heterog."],
        "panels": [{
            "dep_var": "Per-Visit Benefit and Cost Parameters",
            "variables": [
                {"label": "Per-visit benefit $b$ (\\$/visit)", "coefficients": ["14.22***", "13.84***", "14.51***", "14.08***"],
                 "std_errors": ["(1.41)", "(1.38)", "(1.48)", "(1.44)"]},
                {"label": "Per-visit cost $c$ (effort, \\$-equiv.)", "coefficients": ["11.84***", "11.51***", "12.14***", "11.72***"],
                 "std_errors": ["(1.21)", "(1.18)", "(1.28)", "(1.24)"]},
                {"label": "Hassle cost $\\kappa$ (cancellation, \\$)", "coefficients": ["8.12***", "7.94***", "8.34***", "8.01***"],
                 "std_errors": ["(0.84)", "(0.82)", "(0.89)", "(0.86)"]},
                {"label": "Demand elasticity $\\eta$", "coefficients": ["-0.412***", "-0.398***", "-0.428***", "-0.408***"],
                 "std_errors": ["(0.041)", "(0.040)", "(0.044)", "(0.042)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["7,752", "7,752", "7,752", "7,752"]},
            {"label": "Log-likelihood", "values": ["-14,821", "-14,908", "-14,774", "-14,612"]},
        ],
        "notes": "*** p<0.01. Bootstrap SEs. Identification from contract choice, attendance, and cancellation moments jointly. Column (4) allows $b$ and $c$ to vary with demographics.",
        "qa": [
            {"question": "What is the estimated per-visit benefit in the baseline?", "answer": "\\$14.22 per visit"},
            {"question": "What is the estimated per-visit cost in the baseline?", "answer": "\\$11.84 per visit"},
            {"question": "What is the estimated cancellation hassle cost?", "answer": "\\$8.12"},
        ],
    })

    counterfactual_contract = render_regression_table({
        "table_id": "counterfactual-contract",
        "caption": "Counterfactual Contract Analysis",
        "label": "tab:counterfactual-contract",
        "model_labels": ["Monthly", "Annual", "Pay-per-visit", "Optimal"],
        "panels": [{
            "dep_var": "Panel A: Predicted Choices Under Each Contract Menu",
            "variables": [
                {"label": "Share Choosing Contract", "coefficients": ["0.614", "0.241", "0.145", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Predicted Avg Monthly Visits", "coefficients": ["4.17", "4.84", "3.02", "4.94"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Welfare per Member per Month (\\$)",
            "variables": [
                {"label": "Consumer Surplus (actual)", "coefficients": ["12.41", "19.84", "8.12", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Consumer Surplus (time-consistent)", "coefficients": ["18.24", "21.41", "8.12", "22.84"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Firm Profit", "coefficients": ["21.81", "14.12", "8.84", "16.44"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Total Surplus", "coefficients": ["34.22", "33.96", "16.96", "39.28"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations (simulations)", "values": ["7,752", "7,752", "7,752", "7,752"]},
        ],
        "notes": "Bootstrap SEs omitted for brevity. Optimal contract maximizes total surplus subject to firm break-even. Time-consistent surplus uses $\\beta=1$.",
        "qa": [
            {"question": "What is the consumer surplus under the monthly contract?", "answer": "\\$12.41 per member per month"},
            {"question": "What is the total surplus under the optimal contract?", "answer": "\\$39.28"},
            {"question": "What is the predicted average monthly visits under the annual contract?", "answer": "4.84"},
            {"question": "What is the firm profit under the monthly contract?", "answer": "\\$21.81"},
        ],
    })

    welfare = render_regression_table({
        "table_id": "welfare",
        "caption": "Welfare Analysis: Costs of Present Bias",
        "label": "tab:welfare",
        "model_labels": ["Monthly Holders", "Annual Holders", "All Members", "Low-Income"],
        "panels": [{
            "dep_var": "Panel A: Annual Welfare Loss from Present Bias (\\$/year)",
            "variables": [
                {"label": "Welfare loss (\\$)", "coefficients": ["179.4***", "48.2***", "136.1***", "201.8***"],
                 "std_errors": ["(18.4)", "(9.2)", "(14.2)", "(24.1)"]},
                {"label": "As \\% of annual fees paid", "coefficients": ["21.3\\%", "6.9\\%", "16.2\\%", "24.1\\%"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Decomposition of Welfare Loss",
            "variables": [
                {"label": "Excess fee payments (dominated contracts)", "coefficients": ["112.4", "28.1", "84.2", "127.1"],
                 "std_errors": ["(12.4)", "(6.8)", "(9.8)", "(15.2)"]},
                {"label": "Suboptimal attendance (procrastination)", "coefficients": ["67.0", "20.1", "51.9", "74.7"],
                 "std_errors": ["(8.4)", "(4.2)", "(6.8)", "(10.4)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["4,761", "1,868", "7,752", "1,941"]},
        ],
        "notes": "*** p<0.01. Welfare loss computed relative to time-consistent agent ($\\beta=1$). Bootstrap SEs from 500 draws. Low-income: below median income zip code.",
        "qa": [
            {"question": "What is the annual welfare loss from present bias for monthly contract holders?", "answer": "\\$179.4 per year"},
            {"question": "What fraction of annual fees paid represents welfare loss for monthly holders?", "answer": "21.3 percent"},
            {"question": "How much of the welfare loss for all members is due to excess fee payments?", "answer": "\\$84.2 per year"},
        ],
    })

    overconfidence = render_regression_table({
        "table_id": "overconfidence",
        "caption": "Evidence for Overconfidence in Attendance Forecasting",
        "label": "tab:overconfidence",
        "model_labels": ["(1) OLS", "(2) + FE", "(3) IV", "(4) Long-Run"],
        "panels": [{
            "dep_var": "Dep. var.: Actual Monthly Visits",
            "variables": [
                {"label": "Predicted Monthly Visits (survey)", "coefficients": ["0.481***", "0.462***", "0.498***", "0.414***"],
                 "std_errors": ["(0.041)", "(0.040)", "(0.058)", "(0.052)"]},
                {"label": "Constant (prediction error)", "coefficients": ["2.241***", "2.314***", "2.188***", "2.582***"],
                 "std_errors": ["(0.184)", "(0.188)", "(0.214)", "(0.228)"]},
            ],
        }, {
            "dep_var": "Dep. var.: Prediction Error (Survey $-$ Actual Visits)",
            "variables": [
                {"label": "Monthly Contract Holder", "coefficients": ["1.841***", "1.784***", "1.912***", "2.184***"],
                 "std_errors": ["(0.184)", "(0.181)", "(0.208)", "(0.241)"]},
                {"label": "Annual Contract Holder", "coefficients": ["0.912***", "0.881***", "0.941***", "1.084***"],
                 "std_errors": ["(0.121)", "(0.118)", "(0.138)", "(0.158)"]},
            ],
        }],
        "controls": [
            {"label": "Club FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["7,752", "7,752", "5,841", "3,284"]},
            {"label": "R-squared", "values": ["0.214", "0.248", "--", "0.198"]},
        ],
        "notes": "*** p<0.01. Column (3): IV using initial visit intentions from enrollment survey as instrument. Column (4): restricts to members observed 12+ months. Robust SEs.",
        "qa": [
            {"question": "What is the coefficient on predicted monthly visits in the baseline OLS?", "answer": "0.481"},
            {"question": "What is the prediction error constant in the baseline regression?", "answer": "2.241"},
            {"question": "What is the prediction error for monthly contract holders relative to pay-per-visit?", "answer": "1.841 additional visits per month"},
        ],
    })

    appendix_survey = render_regression_table({
        "table_id": "appendix-survey",
        "caption": "Appendix: Survey Instrument Validation and Attrition Analysis",
        "label": "tab:appendix-survey",
        "model_labels": ["Responded", "Attrited", "Difference", "p-value"],
        "panels": [{
            "dep_var": "Panel A: Survey Response and Attrition Balance",
            "variables": [
                {"label": "Monthly visits (pre-survey)", "coefficients": ["4.21", "4.08", "0.13", "0.412"],
                 "std_errors": ["(0.08)", "(0.12)", "(0.14)", ""]},
                {"label": "Contract type: Monthly", "coefficients": ["0.618", "0.604", "0.014", "0.614"],
                 "std_errors": ["(0.012)", "(0.018)", "(0.022)", ""]},
                {"label": "Months in club", "coefficients": ["8.41", "7.84", "0.57", "0.284"],
                 "std_errors": ["(0.21)", "(0.31)", "(0.38)", ""]},
            ],
        }, {
            "dep_var": "Panel B: Survey Forecast Accuracy",
            "variables": [
                {"label": "Forecast visits (next month)", "coefficients": ["5.84", "5.71", "0.13", "0.518"],
                 "std_errors": ["(0.14)", "(0.21)", "(0.25)", ""]},
                {"label": "Actual visits (next month)", "coefficients": ["4.14", "4.02", "0.12", "0.541"],
                 "std_errors": ["(0.08)", "(0.12)", "(0.14)", ""]},
                {"label": "Forecast error (overestimate)", "coefficients": ["1.70", "1.69", "0.01", "0.981"],
                 "std_errors": ["(0.12)", "(0.18)", "(0.22)", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["5,841", "1,911", "7,752", "7,752"]},
        ],
        "notes": "Survey administered to random 75\\% subsample in year 2 of data collection. Attrition defined as non-response. No significant differential attrition on observables.",
        "qa": [
            {"question": "What is the average forecast error (overestimate) for survey respondents?", "answer": "1.70 visits per month"},
            {"question": "Is there differential attrition in the survey by contract type?", "answer": "No, p-value for contract type balance is 0.614"},
        ],
    })

    # --- Equations ---
    eq_beta_delta = EquationSpec(
        "beta-delta-utility",
        r"U_t = u(c_t) + \beta \sum_{\tau=1}^{T} \delta^\tau u(c_{t+\tau}), \quad \mathbb{E}_t[U_t] = \mathbb{E}\!\left[u(c_t) + \beta \sum_{\tau=1}^{T} \delta^\tau u(c_{t+\tau}) \,\middle|\, \mathcal{F}_t\right]",
        "eq:beta-delta",
        "Beta-delta quasi-hyperbolic utility: $\\beta < 1$ captures present bias, $\\delta$ governs long-run patience.",
        [{"question": "What does beta < 1 capture in the beta-delta model?", "answer": "Present bias: extra discounting of all future periods relative to the present"}],
    )

    eq_contract_choice = EquationSpec(
        "contract-choice",
        r"V^M > V^{PPV} \iff \sum_{t=1}^{T} \delta^t \beta [b - c(\nu_t)] - p^M > \sum_{t=1}^{T} \delta^t \beta [b - c(\nu_t)] \mathbf{1}[\nu_t > 0] - p^{PPV} \nu_t",
        "eq:contract-choice",
        "A naive agent chooses monthly contract if perceived net value $V^M$ exceeds pay-per-visit $V^{PPV}$, based on forecasted $\\nu_t$ but evaluated at $\\beta=1$.",
    )

    eq_attendance = EquationSpec(
        "attendance-decision",
        r"\nu_t^* = 1 \iff \beta [b - c_t] \geq p_t, \quad c_t \sim F(\cdot)",
        "eq:attendance",
        "Period-$t$ attendance decision: member exercises if present-biased benefit net of stochastic effort cost $c_t$ exceeds the current-period price $p_t$.",
    )

    eq_hazard = EquationSpec(
        "cancellation-hazard",
        r"h(t \mid x) = h_0(t) \exp(x'\gamma), \quad h_0(t) = p \lambda (\lambda t)^{p-1}, \quad \mathbb{P}(T > t) = \prod_{k=1}^{K} \exp\!\left(-\binom{t}{k} \lambda_k \right)",
        "eq:hazard",
        "Proportional hazard model for cancellation: $h_0(t)$ is the Weibull baseline hazard with shape $p$ and scale $\\lambda$.",
    )

    eq_per_visit_cost = EquationSpec(
        "per-visit-cost",
        r"c(\nu) = c_0 + c_1 \nu + c_2 \nu^2 + c_3 \sqrt[3]{\nu}, \quad \mathbb{E}[c_t] = c_0 + c_1 \bar{\nu} + c_3 \mathbb{E}\!\left[\sqrt[3]{\nu_t}\right]",
        "eq:per-visit-cost",
        "Quadratic per-visit cost function: $c_0$ is fixed hassle cost, $c_1$ and $c_2$ capture increasing marginal effort.",
    )

    eq_overconfidence = EquationSpec(
        "overconfidence-param",
        r"\\tilde{\\beta} = \\theta + (1-\\theta)\\beta, \\quad \\theta \\in [0,1]",
        "eq:overconfidence",
        "Overconfidence parameter $\\theta$: $\\theta=1$ is fully naive (believes $\\beta=1$); $\\theta=0$ is fully sophisticated.",
    )

    eq_welfare_cs = EquationSpec(
        "welfare-cs",
        r"CS = E\\left[\\sum_{t=1}^{T} \\delta^t [b - c_t] \\mathbf{1}[\\nu_t^*=1] - p^M\\right] - E\\left[\\sum_{t=1}^{T} \\delta^t [b - c_t] \\mathbf{1}[\\tilde{\\nu}_t^*=1] - p^M\\right]",
        "eq:welfare-cs",
        "Consumer surplus loss from present bias: difference between time-consistent ($\\beta=1$) and biased ($\\beta<1$) surplus.",
    )

    eq_structural_lik = EquationSpec(
        "structural-likelihood",
        r"\\mathcal{L}(\\beta, \\delta, \\theta, b, c, \\kappa) = \\prod_{i=1}^N P(k_i \\mid \\beta, \\delta, \\theta) \\cdot \\prod_{t} P(\\nu_{it} \\mid \\beta, c, p_t) \\cdot P(s_i \\mid \\theta, c)",
        "eq:structural-lik",
        "Full information MLE: joint likelihood over contract choices $k_i$, monthly visits $\\nu_{it}$, and survey forecasts $s_i$.",
        [{"question": "What three sources of moments identify the structural parameters?", "answer": "Contract choices, monthly attendance, and survey forecast data"}],
    )

    eq_optimal_contract = EquationSpec(
        "optimal-contract",
        r"\\max_{p^F, p^M} \\pi = N \\cdot [p^F + p^M E[\\nu^*]] \\quad \\text{s.t.} \\quad CS(\\beta, p^F, p^M) \\geq \\bar{u}",
        "eq:optimal-contract",
        "Firm's optimal contract design: maximize profit from fixed fee $p^F$ and per-visit fee $p^M$ subject to consumer participation constraint.",
    )

    eq_identification = EquationSpec(
        "identification",
        r"\\frac{\\partial \\mathcal{L}}{\\partial \\beta} = 0, \\quad \\frac{\\partial^2 \\mathcal{L}}{\\partial \\beta^2} < 0 \\quad \\Leftrightarrow \\quad \\text{Cov}(k_i, \\nu_{it}) \\neq 0",
        "eq:identification",
        "Beta is identified by the covariance between contract choice and subsequent attendance: naive agents systematically choose costly contracts and attend infrequently.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[Identification of $\beta$ vs. $\delta$]
In the beta-delta model, $\beta$ and $\delta$ are separately identified if the data include choices over contracts with different intertemporal profiles. Let $V^M(\beta,\delta)$ and $V^{PPV}(\beta,\delta)$ denote the values of the monthly and pay-per-visit contracts. Then:
\begin{align}
V^M - V^{PPV} &= -p^M + p^{PPV} \bar{\nu}^{PPV} + \beta\delta [b - \bar{c}] (\bar{\nu}^M - \bar{\nu}^{PPV}),
\end{align}
where the $\beta\delta$ term multiplies the \emph{difference} in expected visits across contracts. Exogenous variation in $p^{PPV}$ across clubs identifies $\delta$, while $\beta$ is identified from the wedge between stated intentions and actual behavior.
\end{proposition}

\begin{proposition}[MLE Derivation for Present-Bias Parameters]
Let $\boldsymbol{\psi} = (\beta, \delta, \theta, b, c_0, c_1, \kappa)$. The log-likelihood is:
\begin{align}
\ell(\boldsymbol{\psi}) &= \sum_i \log P(k_i \mid \boldsymbol{\psi}) + \sum_{i,t} \log P(\nu_{it} \mid \boldsymbol{\psi}) + \sum_i \log P(s_i \mid \boldsymbol{\psi}),
\end{align}
where:
\begin{align}
P(k_i = M \mid \boldsymbol{\psi}) &= \Phi\!\left(\frac{V^M(\tilde{\beta}, \delta) - V^{PPV}(\tilde{\beta}, \delta)}{\sigma_\varepsilon}\right), \\
P(\nu_{it} = 1 \mid \boldsymbol{\psi}) &= F\!\left(\beta b - p_t\right),
\end{align}
and $\tilde{\beta} = \theta + (1-\theta)\beta$ is the perceived present-bias factor. The score equations $\partial\ell/\partial\boldsymbol{\psi} = 0$ are solved via BFGS with analytic gradients.
\end{proposition}

\begin{proposition}[Naive Agents Choose Dominated Contracts]
A member is naive if $\tilde{\beta} > \beta$. Let $\nu^*(\beta)$ denote actual visits and $\tilde{\nu}(\tilde{\beta})$ forecasted visits. The monthly contract is dominated when $p^M > p^{PPV} \cdot \nu^*(\beta)$. A naive agent chooses monthly if $p^M < p^{PPV} \cdot \tilde{\nu}(\tilde{\beta})$, so there exists a range:
\begin{align}
p^{PPV} \cdot \nu^*(\beta) < p^M < p^{PPV} \cdot \tilde{\nu}(\tilde{\beta}),
\end{align}
over which naive agents choose a dominated contract. Under estimated parameters ($\hat{\beta} = 0.712$, $\hat{\theta} = 0.591$, $\bar{\nu}^* = 4.17$, $p^{PPV} = \$10$), this range is $[\$41.70, \$58.40]$, containing the observed monthly fee of $\$70$.
\end{proposition}

\begin{proposition}[Welfare Formula Under Present Bias]
The welfare loss decomposes into excess fees under dominated contracts and procrastination loss:
\begin{align}
W(\beta=1) - W(\beta) &= \sum_{t=1}^T \delta^t\!\left[b\,\Delta\nu_t^* - \int_0^{\Delta\nu_t^*} c(\nu)\,dF(\nu)\right] - p^M \mathbf{1}[\Delta k = M\to PPV],
\end{align}
where $\Delta\nu_t^* = \nu^*(1) - \nu^*(\beta)$ is the attendance shortfall.
\end{proposition}

\begin{lemma}[Expected Visit Count via Binomial Expansion]
Under $T$ independent visit opportunities with per-period visit probability $\pi(\beta)$, the expected number of visits follows:
\begin{align}
\mathbb{E}[\nu] = \sum_{k=0}^{T} k \binom{T}{k} \pi(\beta)^k (1-\pi(\beta))^{T-k} = T \cdot \pi(\beta).
\end{align}
The $\sqrt[3]{\cdot}$ cost component induces a nonlinear expected cost:
\begin{align}
\mathbb{E}\!\left[\sqrt[3]{\nu}\right] = \sum_{k=0}^{T} \sqrt[3]{k} \binom{T}{k} \pi^k (1-\pi)^{T-k} \approx \sqrt[3]{T\pi} - \frac{1}{9}(T\pi)^{-2/3} T\pi(1-\pi).
\end{align}
\end{lemma}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-behavioral",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec(
        "Introduction", "sec:intro-beh",
        text_paragraphs=14,
        equations=[eq_beta_delta],
    )

    institutional = SectionSpec(
        "Institutional Background and Data", "sec:data-beh",
        text_paragraphs=10,
        tables=[gym_summary],
        subsections=[
            SectionSpec("Health Club Setting", "sec:data-clubs", level=2, text_paragraphs=7),
            SectionSpec("Contract Menu and Pricing", "sec:data-contracts", level=2, text_paragraphs=6),
            SectionSpec("Survey Data on Attendance Intentions", "sec:data-survey", level=2, text_paragraphs=7),
        ],
    )

    theory = SectionSpec(
        "Theoretical Framework", "sec:theory-beh",
        text_paragraphs=12,
        equations=[eq_contract_choice, eq_attendance, eq_overconfidence],
        subsections=[
            SectionSpec("Beta-Delta Preferences", "sec:theory-betadelta", level=2, text_paragraphs=8),
            SectionSpec("Contract Choice Under Naive Present Bias", "sec:theory-naive", level=2, text_paragraphs=8),
            SectionSpec("Optimal Firm Response", "sec:theory-firm", level=2, text_paragraphs=7),
        ],
    )

    reduced_form_section = SectionSpec(
        "Reduced-Form Evidence", "sec:rf-beh",
        text_paragraphs=12,
        tables=[contract_choice, attendance, reduced_form],
        subsections=[
            SectionSpec("Contract Choice Patterns", "sec:rf-choice", level=2, text_paragraphs=8),
            SectionSpec("Attendance Dynamics", "sec:rf-attendance", level=2, text_paragraphs=8),
            SectionSpec("Cancellation Delays", "sec:rf-cancel", level=2, text_paragraphs=7),
        ],
    )

    structural_section = SectionSpec(
        "Structural Estimation", "sec:structural-beh",
        text_paragraphs=12,
        equations=[eq_structural_lik, eq_identification, eq_per_visit_cost],
        tables=[hazard_cancellation, structural_beta_delta, structural_preferences],
        subsections=[
            SectionSpec("Likelihood Function", "sec:struct-lik", level=2, text_paragraphs=8),
            SectionSpec("Identification Strategy", "sec:struct-id", level=2, text_paragraphs=9),
            SectionSpec("Estimation Results", "sec:struct-results", level=2, text_paragraphs=8),
        ],
    )

    welfare_section = SectionSpec(
        "Welfare and Counterfactual Analysis", "sec:welfare-beh",
        text_paragraphs=12,
        equations=[eq_welfare_cs, eq_hazard, eq_optimal_contract],
        tables=[counterfactual_contract, welfare, overconfidence],
        subsections=[
            SectionSpec("Welfare Loss from Present Bias", "sec:welfare-loss", level=2, text_paragraphs=8),
            SectionSpec("Counterfactual Contract Menus", "sec:welfare-cf", level=2, text_paragraphs=8),
            SectionSpec("Policy Implications", "sec:welfare-policy", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-beh", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Theoretical Proofs", "sec:appendix-a-beh",
        text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Survey Instrument and Attrition", "sec:appendix-b-beh",
        text_paragraphs=5,
        tables=[appendix_survey],
    )

    appendix_c = SectionSpec(
        "Appendix C: Robustness of Structural Estimates", "sec:appendix-c-beh",
        text_paragraphs=6,
    )

    return PaperSpec(
        paper_id="14",
        field_slug="behavioral",
        title="Paying Not to Go to the Gym: Present Bias, Contract Choice, and Welfare in Health Club Membership",
        authors="Adriana Delgado-Voss, Kweku Mensah, Sophia Bergstrom",
        journal_style="jf",
        abstract=(
            "We use health club membership data from three US gyms (1997-2001) to estimate present bias "
            "and its welfare consequences. Members who choose flat-rate monthly contracts attend on average "
            "4.17 times per month, well below the break-even of 4.5 visits needed to justify the fee over "
            "pay-per-visit pricing. Structural estimation of a beta-delta model yields $\\hat{\\beta} = 0.712$ "
            "and an overconfidence parameter $\\hat{\\theta} = 0.591$, indicating that members are substantially "
            "naive about their future present bias. The average welfare loss from present bias is \\$136 per "
            "member per year, with 62\\% attributable to dominated contract choice and 38\\% to procrastination. "
            "Counterfactual analysis shows that a commitment contract eliminating present-bias distortions "
            "would raise total surplus by 15\\% and consumer surplus by 32\\%."
        ),
        sections=[intro, institutional, theory, reduced_form_section, structural_section,
                  welfare_section, conclusion, appendix_a, appendix_b, appendix_c],
        bibliography_entries=[
            r"\bibitem{dellavigna2006} DellaVigna, S. and Malmendier, U. (2006). Paying Not to Go to the Gym. \textit{American Economic Review}, 96(3), 694--719.",
            r"\bibitem{oquinn1999} O'Donoghue, T. and Rabin, M. (1999). Doing It Now or Later. \textit{American Economic Review}, 89(1), 103--124.",
            r"\bibitem{laibson1997} Laibson, D. (1997). Golden Eggs and Hyperbolic Discounting. \textit{Quarterly Journal of Economics}, 112(2), 443--478.",
            r"\bibitem{strotz1955} Strotz, R. H. (1955). Myopia and Inconsistency in Dynamic Utility Maximization. \textit{Review of Economic Studies}, 23(3), 165--180.",
            r"\bibitem{phelps1968} Phelps, E. S. and Pollak, R. A. (1968). On Second-Best National Saving and Game-Equilibrium Growth. \textit{Review of Economic Studies}, 35(2), 185--199.",
            r"\bibitem{gruber2009} Gruber, J. and Koszegi, B. (2009). A Modern Economic View of Tobacco Taxation. \textit{International Union Against Tuberculosis and Lung Disease}.",
            r"\bibitem{ashraf2006} Ashraf, N., Karlan, D., and Yin, W. (2006). Tying Odysseus to the Mast: Evidence from a Commitment Savings Product in the Philippines. \textit{Quarterly Journal of Economics}, 121(2), 635--672.",
            r"\bibitem{fudenberg2006} Fudenberg, D. and Levine, D. K. (2006). A Dual-Self Model of Impulse Control. \textit{American Economic Review}, 96(5), 1449--1476.",
        ],
        target_pages=55,
        qa=[
            {"question": "What is the main empirical finding about monthly contract choice?", "answer": "Monthly contract holders attend only 4.17 times/month on average, below the 4.5-visit break-even, paying more than pay-per-visit"},
            {"question": "What is the estimated beta (present bias) parameter?", "answer": "0.712"},
            {"question": "What is the estimated overconfidence parameter theta?", "answer": "0.591"},
            {"question": "What is the annual welfare loss from present bias for the average member?", "answer": "\\$136 per year"},
            {"question": "What fraction of the welfare loss is due to dominated contract choice?", "answer": "62 percent"},
        ],
    )


PAPER_BUILDERS["14"] = _paper_14_behavioral
