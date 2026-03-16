#!/usr/bin/env python3
"""Paper builder for paper 07 (Econometric Theory)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table, render_math_table,
    PAPER_BUILDERS,
)

def _paper_07_econometric_theory() -> PaperSpec:
    # --- Tables ---
    monte_carlo_size_ols = render_regression_table({
        "table_id": "monte-carlo-size-ols",
        "caption": "Monte Carlo Size of OLS t-Tests Under Heteroskedasticity and Serial Correlation",
        "label": "tab:mc-size-ols",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "Panel A: Rejection Rate at Nominal 5\\% Level (iid errors)",
            "variables": [
                {"label": "OLS t-test (homoskedastic)", "coefficients": ["5.2", "5.1", "5.0", "5.0"],
                 "std_errors": ["(0.4)", "(0.4)", "(0.3)", "(0.3)"]},
                {"label": "OLS t-test (heteroskedastic HC0)", "coefficients": ["6.8", "6.1", "5.4", "5.2"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
                {"label": "OLS t-test (HC3 bias-corrected)", "coefficients": ["5.8", "5.4", "5.1", "5.0"],
                 "std_errors": ["(0.4)", "(0.4)", "(0.3)", "(0.3)"]},
            ],
        }, {
            "dep_var": "Panel B: Rejection Rate at Nominal 5\\% Level (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "OLS t-test (no correction)", "coefficients": ["18.4", "19.1", "19.8", "20.1"],
                 "std_errors": ["(0.8)", "(0.8)", "(0.8)", "(0.8)"]},
                {"label": "OLS t-test (heteroskedastic HC0)", "coefficients": ["17.9", "18.6", "19.2", "19.8"],
                 "std_errors": ["(0.8)", "(0.8)", "(0.8)", "(0.8)"]},
                {"label": "OLS t-test (HC3 bias-corrected)", "coefficients": ["17.1", "17.8", "18.4", "19.1"],
                 "std_errors": ["(0.8)", "(0.8)", "(0.8)", "(0.8)"]},
            ],
        }],
        "summary": [
            {"label": "DGP", "values": ["AR(1)", "AR(1)", "AR(1)", "AR(1)"]},
            {"label": "Monte Carlo replications", "values": ["10,000", "10,000", "10,000", "10,000"]},
        ],
        "notes": "Size is empirical rejection rate (\\%) at 5\\% nominal level. Standard deviations across replications in parentheses. DGP: $y_t = 1 + 0.5 x_t + u_t$ with $u_t = \\rho u_{t-1} + \\varepsilon_t$.",
        "qa": [
            {"question": "What is the OLS rejection rate with AR(1) errors (rho=0.5) and no correction at T=250?", "answer": "19.8"},
            {"question": "What is the HC3 rejection rate with iid errors at T=100?", "answer": "5.4"},
            {"question": "What is the nominal test level used?", "answer": "5 percent"},
            {"question": "How many Monte Carlo replications are used?", "answer": "10,000"},
        ],
    })

    monte_carlo_size_hac = render_regression_table({
        "table_id": "monte-carlo-size-hac",
        "caption": "Monte Carlo Size of HAC-Corrected t-Tests",
        "label": "tab:mc-size-hac",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "Panel A: AR(1) errors, rho=0.3",
            "variables": [
                {"label": "Bartlett (Andrews BW)", "coefficients": ["6.1", "5.6", "5.2", "5.1"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
                {"label": "Parzen (Andrews BW)", "coefficients": ["6.4", "5.8", "5.3", "5.1"],
                 "std_errors": ["(0.5)", "(0.5)", "(0.4)", "(0.3)"]},
                {"label": "QS (Andrews BW)", "coefficients": ["5.9", "5.5", "5.1", "5.0"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
            ],
        }, {
            "dep_var": "Panel B: AR(1) errors, rho=0.7",
            "variables": [
                {"label": "Bartlett (Andrews BW)", "coefficients": ["9.2", "7.4", "6.1", "5.5"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.5)", "(0.4)"]},
                {"label": "Parzen (Andrews BW)", "coefficients": ["8.8", "7.1", "5.9", "5.4"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.5)", "(0.4)"]},
                {"label": "QS (Andrews BW)", "coefficients": ["8.4", "6.9", "5.7", "5.2"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.4)", "(0.4)"]},
            ],
        }, {
            "dep_var": "Panel C: MA(1) errors, theta=0.5",
            "variables": [
                {"label": "Bartlett (Andrews BW)", "coefficients": ["5.8", "5.4", "5.1", "5.0"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
                {"label": "Parzen (Andrews BW)", "coefficients": ["5.9", "5.5", "5.2", "5.1"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
                {"label": "QS (Andrews BW)", "coefficients": ["5.7", "5.3", "5.0", "5.0"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.3)", "(0.3)"]},
            ],
        }],
        "summary": [
            {"label": "Monte Carlo replications", "values": ["10,000", "10,000", "10,000", "10,000"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1 (size distortion from nominal). HAC estimators use data-driven bandwidths. QS kernel achieves smallest size distortion under AR(1) with high persistence.",
        "qa": [
            {"question": "Which kernel achieves the smallest size distortion under AR(1) with rho=0.7?", "answer": "QS kernel"},
            {"question": "What is the Bartlett HAC rejection rate at T=100 with rho=0.7?", "answer": "7.4"},
            {"question": "What is the QS HAC size at T=500 with MA(1) errors?", "answer": "5.0"},
            {"question": "What is the Bartlett size at T=50 with rho=0.3?", "answer": "6.1"},
        ],
    })

    monte_carlo_power = render_regression_table({
        "table_id": "monte-carlo-power",
        "caption": "Monte Carlo Power of HAC t-Tests Against Slope Alternatives",
        "label": "tab:mc-power",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "Panel A: Alternative beta=0.10 (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "Bartlett HAC power (\\%)", "coefficients": ["21.4", "38.2", "74.1", "96.8"],
                 "std_errors": ["(0.8)", "(1.0)", "(0.9)", "(0.4)"]},
                {"label": "QS HAC power (\\%)", "coefficients": ["22.1", "39.4", "75.8", "97.2"],
                 "std_errors": ["(0.8)", "(1.0)", "(0.9)", "(0.3)"]},
                {"label": "OLS power (infeasible oracle)", "coefficients": ["30.1", "52.4", "91.2", "99.8"],
                 "std_errors": ["(0.9)", "(1.0)", "(0.6)", "(0.1)"]},
            ],
        }, {
            "dep_var": "Panel B: Alternative beta=0.20 (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "Bartlett HAC power (\\%)", "coefficients": ["48.2", "74.8", "98.1", "100.0"],
                 "std_errors": ["(1.0)", "(0.9)", "(0.3)", "(0.0)"]},
                {"label": "QS HAC power (\\%)", "coefficients": ["49.8", "76.2", "98.4", "100.0"],
                 "std_errors": ["(1.0)", "(0.9)", "(0.3)", "(0.0)"]},
                {"label": "OLS power (infeasible oracle)", "coefficients": ["64.1", "89.4", "99.8", "100.0"],
                 "std_errors": ["(1.0)", "(0.6)", "(0.1)", "(0.0)"]},
            ],
        }],
        "summary": [
            {"label": "Monte Carlo replications", "values": ["10,000", "10,000", "10,000", "10,000"]},
        ],
        "notes": "Power is empirical rejection rate (\\%) against $H_1: \\beta \\neq 0$ at 5\\% nominal level. Oracle test uses known true covariance structure. Power gap relative to oracle reflects bandwidth estimation uncertainty.",
        "qa": [
            {"question": "What is Bartlett HAC power against beta=0.10 at T=250?", "answer": "74.1"},
            {"question": "What is QS HAC power against beta=0.20 at T=100?", "answer": "76.2"},
            {"question": "At what sample size does HAC power exceed 90% against beta=0.10?", "answer": "T=250 (74.1%) to T=500 (96.8%)"},
        ],
    })

    bandwidth_comparison = render_regression_table({
        "table_id": "bandwidth-comparison",
        "caption": "Bandwidth Selection: Andrews (1991) vs. Newey-West (1994) Rule",
        "label": "tab:bandwidth-comparison",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "Panel A: Mean selected bandwidth (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "Andrews (1991) plug-in", "coefficients": ["4.1", "5.8", "9.4", "13.2"],
                 "std_errors": ["(1.2)", "(1.6)", "(2.4)", "(3.1)"]},
                {"label": "Newey-West (1994) fixed", "coefficients": ["3.5", "4.9", "7.8", "11.0"],
                 "std_errors": ["(0.0)", "(0.0)", "(0.0)", "(0.0)"]},
                {"label": "Optimal (MSE-minimizing)", "coefficients": ["4.8", "6.7", "10.8", "15.1"],
                 "std_errors": ["(0.6)", "(0.9)", "(1.4)", "(1.8)"]},
            ],
        }, {
            "dep_var": "Panel B: Mean selected bandwidth (AR(1) errors, rho=0.8)",
            "variables": [
                {"label": "Andrews (1991) plug-in", "coefficients": ["7.8", "11.2", "18.4", "26.1"],
                 "std_errors": ["(2.1)", "(2.8)", "(4.2)", "(5.6)"]},
                {"label": "Newey-West (1994) fixed", "coefficients": ["3.5", "4.9", "7.8", "11.0"],
                 "std_errors": ["(0.0)", "(0.0)", "(0.0)", "(0.0)"]},
                {"label": "Optimal (MSE-minimizing)", "coefficients": ["9.1", "12.8", "21.4", "30.2"],
                 "std_errors": ["(1.1)", "(1.4)", "(2.1)", "(2.8)"]},
            ],
        }],
        "summary": [
            {"label": "Monte Carlo replications", "values": ["10,000", "10,000", "10,000", "10,000"]},
        ],
        "notes": "Standard deviations of selected bandwidth in parentheses. Newey-West rule: $M = \\lfloor 4(T/100)^{2/9} \\rfloor$. Andrews plug-in uses AR(1) prewhitening. Optimal bandwidth minimizes asymptotic MSE of HAC estimator.",
        "qa": [
            {"question": "What is the Andrews plug-in bandwidth at T=100 with rho=0.5?", "answer": "5.8"},
            {"question": "What is the Newey-West fixed bandwidth at T=250?", "answer": "7.8"},
            {"question": "Which bandwidth rule most closely tracks the MSE-optimal bandwidth?", "answer": "Andrews (1991) plug-in"},
            {"question": "What is the optimal bandwidth at T=500 with rho=0.8?", "answer": "30.2"},
        ],
    })

    kernel_comparison = render_math_table({
        "table_id": "kernel-comparison",
        "caption": "Properties of HAC Kernel Functions",
        "label": "tab:kernel-comparison",
        "col_headers": [
            {"text": "K(u)"},
            {"text": "Support"},
            {"text": "Efficiency"},
        ],
        "rows": [
            {"label": "Bartlett (Newey-West)", "cells": [
                {"text": "1 - |u|", "latex": r"$1 - |u|$"},
                {"text": "[-1, 1]", "latex": r"$[-1, 1]$"},
                {"text": "1.00"},
            ]},
            {"label": "Parzen", "cells": [
                {"text": "1 - 6u^2 + 6|u|^3 (|u| <= 1/2)", "latex": r"$1 - 6u^2 + 6|u|^3 \; (|u| \le 1/2)$"},
                {"text": "[-1, 1]", "latex": r"$[-1, 1]$"},
                {"text": "0.539"},
            ]},
            {"label": "Quadratic Spectral (QS)", "cells": [
                {"text": "sin/cos formula", "latex": r"$\frac{25}{12\pi^2 u^2}\left(\frac{\sin(6\pi u/5)}{6\pi u/5} - \cos(6\pi u/5)\right)$"},
                {"text": "(-inf, inf)", "latex": r"$(-\infty,\infty)$"},
                {"text": "1.421"},
            ]},
            {"label": "Tukey-Hanning", "cells": [
                {"text": "(1 + cos(pi u))/2", "latex": r"$\frac{1}{2}(1 + \cos(\pi u))$"},
                {"text": "[-1, 1]", "latex": r"$[-1, 1]$"},
                {"text": "0.885"},
            ]},
            {"label": "Daniell", "cells": [
                {"text": "sin(pi u)/(pi u)", "latex": r"$\frac{\sin(\pi u)}{\pi u}$"},
                {"text": "(-inf, inf)", "latex": r"$(-\infty,\infty)$"},
                {"text": "1.000"},
            ]},
        ],
        "notes": "Efficiency is Andrews (1991) asymptotic efficiency relative to Bartlett for AR(1) DGP. QS kernel is asymptotically optimal (highest efficiency) and guaranteed positive semi-definite.",
        "qa": [
            {"question": "Which kernel has the highest asymptotic efficiency?", "answer": "Quadratic Spectral (QS) with efficiency 1.421"},
            {"question": "What is the support of the Bartlett kernel?", "answer": "[-1, 1]"},
            {"question": "What is the Parzen kernel efficiency relative to Bartlett?", "answer": "0.539"},
            {"question": "Which kernels have unbounded support?", "answer": "QS and Daniell kernels"},
        ],
    })

    finite_sample_coverage = render_regression_table({
        "table_id": "finite-sample-coverage",
        "caption": "Finite-Sample Coverage of HAC Confidence Intervals",
        "label": "tab:finite-sample-coverage",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "Panel A: 95\\% nominal CI coverage rate (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "Bartlett HAC", "coefficients": ["89.2", "91.8", "93.6", "94.4"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.5)", "(0.4)"]},
                {"label": "QS HAC", "coefficients": ["90.4", "92.6", "94.1", "94.7"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.5)", "(0.4)"]},
                {"label": "Pre-whitened Bartlett", "coefficients": ["91.8", "93.4", "94.4", "94.8"],
                 "std_errors": ["(0.5)", "(0.5)", "(0.4)", "(0.4)"]},
            ],
        }, {
            "dep_var": "Panel B: 95\\% nominal CI coverage rate (AR(1) errors, rho=0.8)",
            "variables": [
                {"label": "Bartlett HAC", "coefficients": ["82.1", "87.4", "91.8", "93.6"],
                 "std_errors": ["(0.8)", "(0.7)", "(0.5)", "(0.5)"]},
                {"label": "QS HAC", "coefficients": ["83.8", "88.9", "92.8", "94.1"],
                 "std_errors": ["(0.7)", "(0.6)", "(0.5)", "(0.5)"]},
                {"label": "Pre-whitened Bartlett", "coefficients": ["86.4", "90.8", "93.9", "94.6"],
                 "std_errors": ["(0.7)", "(0.6)", "(0.5)", "(0.4)"]},
            ],
        }],
        "summary": [
            {"label": "Monte Carlo replications", "values": ["10,000", "10,000", "10,000", "10,000"]},
        ],
        "notes": "Coverage rates (\\%) for 95\\% nominal confidence interval. Pre-whitened estimator fits AR(1) to residuals before HAC weighting. Coverage shortfall most severe at high persistence and small samples.",
        "qa": [
            {"question": "What is pre-whitened Bartlett coverage at T=100 with rho=0.8?", "answer": "90.8"},
            {"question": "What is QS HAC coverage at T=250 with rho=0.5?", "answer": "94.1"},
            {"question": "Which method achieves highest coverage at T=50 with rho=0.8?", "answer": "Pre-whitened Bartlett at 86.4"},
            {"question": "What is the Bartlett HAC coverage at T=50 with rho=0.5?", "answer": "89.2"},
        ],
    })

    pre_whitening = render_regression_table({
        "table_id": "pre-whitening",
        "caption": "Pre-Whitening: Comparison of HAC Estimator Performance",
        "label": "tab:pre-whitening",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "MSE of HAC estimator (x 100, normalized by true long-run variance)",
            "variables": [
                {"label": "Bartlett, no pre-whitening", "coefficients": ["8.41", "4.82", "2.14", "1.08"],
                 "std_errors": ["(1.21)", "(0.68)", "(0.29)", "(0.14)"]},
                {"label": "Bartlett, AR(1) pre-whitening", "coefficients": ["6.18", "3.41", "1.58", "0.81"],
                 "std_errors": ["(0.89)", "(0.48)", "(0.21)", "(0.10)"]},
                {"label": "QS, no pre-whitening", "coefficients": ["7.24", "4.01", "1.78", "0.89"],
                 "std_errors": ["(1.04)", "(0.57)", "(0.24)", "(0.11)"]},
                {"label": "QS, AR(1) pre-whitening", "coefficients": ["5.41", "2.98", "1.32", "0.68"],
                 "std_errors": ["(0.78)", "(0.42)", "(0.18)", "(0.09)"]},
            ],
        }],
        "summary": [
            {"label": "DGP", "values": ["AR(2)", "AR(2)", "AR(2)", "AR(2)"]},
            {"label": "Monte Carlo replications", "values": ["10,000", "10,000", "10,000", "10,000"]},
        ],
        "notes": "AR(2) DGP: $\\rho_1 = 0.6$, $\\rho_2 = 0.2$. MSE scaled by 100 for readability. Pre-whitening reduces MSE by approximately 25-35\\% at all sample sizes.",
        "qa": [
            {"question": "What is the MSE reduction from pre-whitening for Bartlett at T=100?", "answer": "From 4.82 to 3.41, a reduction of about 29%"},
            {"question": "Which estimator has the lowest MSE at T=500?", "answer": "QS with AR(1) pre-whitening at 0.68"},
            {"question": "What is the QS no-pre-whitening MSE at T=250?", "answer": "1.78"},
        ],
    })

    appendix_dgp = render_regression_table({
        "table_id": "appendix-dgp",
        "caption": "Appendix: Data-Generating Process Parameters for Monte Carlo Study",
        "label": "tab:appendix-dgp",
        "model_labels": ["DGP 1", "DGP 2", "DGP 3", "DGP 4"],
        "panels": [{
            "dep_var": "Error Process Parameters",
            "variables": [
                {"label": "Error type", "coefficients": ["AR(1)", "AR(1)", "MA(1)", "ARMA(1,1)"],
                 "std_errors": ["", "", "", ""]},
                {"label": "AR coefficient rho", "coefficients": ["0.3", "0.7", "0.0", "0.5"],
                 "std_errors": ["", "", "", ""]},
                {"label": "MA coefficient theta", "coefficients": ["0.0", "0.0", "0.5", "0.3"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Innovation variance", "coefficients": ["1.0", "1.0", "1.0", "1.0"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Long-run variance", "coefficients": ["2.04", "11.11", "2.25", "8.16"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Regression Parameters",
            "variables": [
                {"label": "Intercept", "coefficients": ["1.0", "1.0", "1.0", "1.0"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Slope (null)", "coefficients": ["0.5", "0.5", "0.5", "0.5"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Regressor type", "coefficients": ["iid N", "iid N", "iid N", "iid N"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Long-run variance computed as $\\sigma^2 / (1-\\rho)^2$ for AR(1) or $\\sigma^2(1+\\theta)^2$ for MA(1). ARMA(1,1) long-run variance computed analytically.",
        "qa": [
            {"question": "What is the long-run variance for the AR(1) DGP with rho=0.7?", "answer": "11.11"},
            {"question": "What is the MA coefficient in DGP 3?", "answer": "0.5"},
            {"question": "What is the slope parameter under the null across all DGPs?", "answer": "0.5"},
        ],
    })

    empirical_application = render_regression_table({
        "table_id": "empirical-application",
        "caption": "Empirical Application: HAC Inference on U.S. Inflation Dynamics",
        "label": "tab:empirical-application",
        "model_labels": ["OLS", "NW (4)", "NW (8)", "QS (Andrews)"],
        "panels": [{
            "dep_var": "Panel A: Dependent variable — CPI Inflation (quarterly, 1960Q1–2019Q4)",
            "variables": [
                {"label": "Lagged inflation", "coefficients": ["0.684***", "0.684***", "0.684***", "0.684***"],
                 "std_errors": ["(0.041)", "(0.082)", "(0.094)", "(0.088)"]},
                {"label": "Output gap", "coefficients": ["0.128***", "0.128**", "0.128*", "0.128**"],
                 "std_errors": ["(0.034)", "(0.058)", "(0.067)", "(0.061)"]},
                {"label": "Oil price change", "coefficients": ["0.019***", "0.019**", "0.019**", "0.019**"],
                 "std_errors": ["(0.005)", "(0.008)", "(0.009)", "(0.009)"]},
                {"label": "Constant", "coefficients": ["0.412***", "0.412**", "0.412*", "0.412**"],
                 "std_errors": ["(0.091)", "(0.184)", "(0.211)", "(0.198)"]},
            ],
        }, {
            "dep_var": "Panel B: Diagnostics",
            "variables": [
                {"label": "Breusch-Godfrey LM (4 lags)", "coefficients": ["18.42***", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "White heteroskedasticity test", "coefficients": ["14.81**", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Selected bandwidth", "coefficients": ["--", "4", "8", "6.2"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["240", "240", "240", "240"]},
            {"label": "Adj. R-sq", "values": ["0.714", "0.714", "0.714", "0.714"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. OLS standard errors are inconsistent under serial correlation. NW (k) = Newey-West with k fixed lags. QS (Andrews) uses Andrews (1991) data-driven bandwidth with Quadratic Spectral kernel. OLS standard errors are about half the HAC standard errors, illustrating severe over-rejection without HAC correction.",
        "qa": [
            {"question": "What is the OLS standard error on lagged inflation?", "answer": "0.041"},
            {"question": "What is the Newey-West (4 lags) standard error on lagged inflation?", "answer": "0.082, approximately double the OLS standard error"},
            {"question": "What bandwidth does the Andrews QS procedure select?", "answer": "6.2"},
            {"question": "Is the output gap coefficient significant under QS HAC?", "answer": "Yes, at the 5% level (p<0.05)"},
        ],
    })

    bootstrap_vs_asymptotic = render_regression_table({
        "table_id": "bootstrap-vs-asymptotic",
        "caption": "Bootstrap vs. Asymptotic HAC Inference: Size and Coverage Comparison",
        "label": "tab:bootstrap-vs-asymptotic",
        "model_labels": ["T=50", "T=100", "T=250", "T=500"],
        "panels": [{
            "dep_var": "Panel A: Empirical rejection rate at 5\\% nominal level (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "Asymptotic Bartlett HAC", "coefficients": ["8.4", "6.8", "5.6", "5.2"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.5)", "(0.4)"]},
                {"label": "Wild bootstrap (Bartlett HAC)", "coefficients": ["5.8", "5.4", "5.1", "5.0"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
                {"label": "Block bootstrap (circular)", "coefficients": ["6.2", "5.6", "5.2", "5.1"],
                 "std_errors": ["(0.5)", "(0.4)", "(0.4)", "(0.3)"]},
            ],
        }, {
            "dep_var": "Panel B: Empirical rejection rate at 5\\% nominal level (AR(1) errors, rho=0.8)",
            "variables": [
                {"label": "Asymptotic Bartlett HAC", "coefficients": ["14.2", "10.1", "7.2", "5.8"],
                 "std_errors": ["(0.7)", "(0.6)", "(0.5)", "(0.5)"]},
                {"label": "Wild bootstrap (Bartlett HAC)", "coefficients": ["7.4", "6.1", "5.4", "5.1"],
                 "std_errors": ["(0.5)", "(0.5)", "(0.4)", "(0.4)"]},
                {"label": "Block bootstrap (circular)", "coefficients": ["8.1", "6.4", "5.6", "5.2"],
                 "std_errors": ["(0.5)", "(0.5)", "(0.4)", "(0.4)"]},
            ],
        }, {
            "dep_var": "Panel C: Coverage of 95\\% CI (AR(1) errors, rho=0.5)",
            "variables": [
                {"label": "Asymptotic Bartlett HAC", "coefficients": ["89.2", "91.8", "93.6", "94.4"],
                 "std_errors": ["(0.6)", "(0.5)", "(0.5)", "(0.4)"]},
                {"label": "Wild bootstrap (Bartlett HAC)", "coefficients": ["93.4", "94.2", "94.8", "95.0"],
                 "std_errors": ["(0.5)", "(0.5)", "(0.4)", "(0.3)"]},
                {"label": "Block bootstrap (circular)", "coefficients": ["92.8", "93.8", "94.6", "94.9"],
                 "std_errors": ["(0.5)", "(0.5)", "(0.4)", "(0.3)"]},
            ],
        }],
        "summary": [
            {"label": "Bootstrap replications", "values": ["999", "999", "999", "999"]},
            {"label": "Monte Carlo replications", "values": ["5,000", "5,000", "5,000", "5,000"]},
        ],
        "notes": "Wild bootstrap uses Rademacher weights following Goncalves and Kiefer (2004). Block bootstrap uses circular blocks of length $\\ell = \\lfloor 1.75 T^{1/3} \\rfloor$. Bootstrap methods provide asymptotic refinement, yielding rejection rates closer to nominal 5\\% in small samples.",
        "qa": [
            {"question": "What is the asymptotic Bartlett rejection rate at T=50 with rho=0.8?", "answer": "14.2, far above the 5% nominal level"},
            {"question": "What is the wild bootstrap rejection rate at T=50 with rho=0.8?", "answer": "7.4, much closer to the 5% nominal level than the asymptotic rate of 14.2"},
            {"question": "What is the wild bootstrap coverage at T=100 with rho=0.5?", "answer": "94.2"},
            {"question": "How many bootstrap replications are used?", "answer": "999"},
        ],
    })

    # --- Equations ---
    eq_hac_variance = EquationSpec(
        "hac-variance",
        r"\hat{\Omega}_{HAC} = \frac{1}{T} \sum_{j=-(T-1)}^{T-1} k\!\left(\frac{j}{\left\lfloor M_T \right\rfloor}\right) \hat{\Gamma}(j), \quad \hat{\Gamma}(j) = \frac{1}{T} \sum_{s=1}^{T}\sum_{t=|j|+1}^{T} \hat{u}_t \hat{u}_{t-|j|} x_t x_{t-|j|}'",
        "eq:hac",
        "HAC variance estimator with kernel $k(\\cdot)$ and bandwidth $M_T$. Autocovariance $\\hat{\\Gamma}(j)$ uses OLS residuals $\\hat{u}_t$.",
        [{"question": "What does the bandwidth M_T control in the HAC estimator?", "answer": "The truncation point: autocovariances at lag |j| > M_T receive zero weight"}],
    )

    eq_bartlett_kernel = EquationSpec(
        "bartlett-kernel",
        r"k_{BT}(u) = \begin{cases} 1 - |u| & |u| \le 1 \\ 0 & |u| > 1 \end{cases}",
        "eq:bartlett",
        "Bartlett (tent) kernel used in Newey-West HAC estimator. Compactly supported and guarantees non-negative weights on autocovariances.",
        [{"question": "What is the Bartlett kernel value at u=0.5?", "answer": "0.5"}],
    )

    eq_bandwidth_rule = EquationSpec(
        "bandwidth-rule",
        r"M_T^{NW} = \left\lfloor 4 \left(\frac{T}{100}\right)^{2/9} \right\rfloor",
        "eq:nw-bw",
        "Newey-West (1994) bandwidth rule: a deterministic function of sample size $T$. Grows at rate $O(T^{2/9})$, satisfying $M_T \\to \\infty$ and $M_T / T^{1/2} \\to 0$.",
    )

    eq_newey_west = EquationSpec(
        "newey-west-formula",
        r"\hat{V}_{NW} = \hat{Q}_{xx}^{-1} \hat{\Omega}_{NW} \hat{Q}_{xx}^{-1}, \quad \hat{\Omega}_{NW} = \hat{\Gamma}(0) + \sum_{j=1}^{\left\lceil M_T \right\rceil} \left(1 - \frac{j}{\left\lfloor M_T \right\rfloor +1}\right)\left[\hat{\Gamma}(j) + \hat{\Gamma}(j)'\right]",
        "eq:nw",
        "Newey-West sandwich variance estimator. $\\hat{Q}_{xx} = T^{-1}\\sum x_t x_t'$ is the sample second moment matrix.",
        [{"question": "What is the weight on autocovariance at lag j in the Newey-West formula?", "answer": "1 - j/(M_T + 1)"}],
    )

    eq_prewhitened = EquationSpec(
        "prewhitened-estimator",
        r"\hat{v}_t = \hat{u}_t - \hat{\phi} \hat{u}_{t-1}, \quad \hat{\Omega}_{PW} = \frac{\hat{\Omega}_{HAC}(\hat{v})}{(1-\hat{\phi})^2}",
        "eq:prewhiten",
        "Pre-whitened HAC estimator: fit AR(1) to residuals, apply HAC to AR residuals $\\hat{v}_t$, then rescale by $(1-\\hat{\\phi})^{-2}$.",
    )

    eq_consistency = EquationSpec(
        "consistency-condition",
        r"\left\lfloor M_T \right\rfloor \to \infty, \quad \frac{\left\lceil M_T \right\rceil}{T^{1/2}} \to 0 \implies \hat{\Omega}_{HAC} \xrightarrow{p} \Omega, \quad \oint_{\|z\|=1} S_{uu}(z)\, dz = \Omega",
        "eq:consistency",
        "Consistency conditions on bandwidth $M_T$: must grow with $T$ to capture all relevant autocovariances, but grow slower than $T^{1/2}$ to ensure averaging reduces variance.",
        [{"question": "What conditions on bandwidth M_T ensure HAC consistency?", "answer": "M_T -> infinity and M_T / T^(1/2) -> 0"}],
    )

    eq_mse_expansion = EquationSpec(
        "mse-expansion",
        r"MSE(\hat{\Omega}_{HAC}) = \frac{M_T}{T} \cdot c_k \cdot \kappa_4 + \frac{1}{M_T^{2q}} \cdot d_k \cdot \|\\Omega^{(q)}\\|^2 + o\!\left(\frac{M_T}{T} + M_T^{-2q}\right)",
        "eq:mse",
        "MSE decomposition: variance term grows as $M_T / T$; bias term decays as $M_T^{-2q}$ where $q$ is the kernel characteristic exponent.",
    )

    eq_data_driven_bw = EquationSpec(
        "data-driven-bandwidth",
        r"M_T^* = c_k \left(\frac{\hat{\alpha}(q) T}{1}\right)^{1/(2q+1)}, \quad \hat{\\alpha}(q) = \\frac{\\sum_j |j|^{2q} \\hat{\\gamma}(j)}{\\hat{\\gamma}(0)}",
        "eq:opt-bw",
        "Andrews (1991) MSE-optimal bandwidth formula, where $c_k$ is a kernel-specific constant, $q$ is the kernel characteristic exponent, and $\\hat{\\alpha}(q)$ is a nuisance parameter estimated from data.",
        [{"question": "What does the kernel characteristic exponent q determine?", "answer": "The rate at which bias decays with bandwidth: bias = O(M_T^{-2q})"}],
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[HAC Consistency]
Let $\{w_t\}_{t=1}^T = \{u_t x_t\}_{t=1}^T$ be a stationary, ergodic, strong mixing sequence with mixing coefficients $\alpha(m) = O(m^{-r})$ for $r > (2+\delta)/\delta$ and $E\|w_t\|^{2+\delta} < \infty$ for some $\delta > 0$. Let $k(\cdot)$ be a kernel satisfying (i) $k(0)=1$, (ii) $k(-u)=k(u)$, (iii) $|k(u)| \le 1$, (iv) $k$ continuous at 0. If $M_T \to \infty$ and $M_T / T^{1/2} \to 0$, then:
\begin{align}
\hat{\Omega}_{HAC} - \Omega &= o_p(1).
\end{align}
\end{proposition}

\begin{proof}
Decompose $\hat{\Omega}_{HAC} - \Omega$ into sampling error (I) and approximation error (II):
\begin{align}
\hat{\Omega}_{HAC} - \Omega &= \underbrace{\sum_{|j| \le M_T} k(j/M_T)[\hat{\Gamma}(j) - \Gamma(j)]}_{\text{(I)}} + \underbrace{\sum_{|j| \le M_T} k(j/M_T)\Gamma(j) - \Omega}_{\text{(II)}}.
\end{align}
For (I): under strong mixing, $E\|\hat{\Gamma}(j) - \Gamma(j)\|^2 \le C T^{-1}$ uniformly in $j$, so $\|\text{(I)}\| = O_p(M_T / T^{1/2}) = o_p(1)$.
For (II): since $\sum_{j} \|\Gamma(j)\| < \infty$, the tail $\sum_{|j|>M_T}\|\Gamma(j)\| \to 0$ as $M_T \to \infty$, and the bias from kernel weighting vanishes by dominated convergence. Hence $\hat{\Omega}_{HAC} \xrightarrow{p} \Omega$.
\end{proof}

\begin{lemma}[Convergence Rate Under Mixing]
Under the mixing conditions of Proposition 1, for each fixed lag $j$:
\begin{align}
\sqrt{T}(\hat{\Gamma}(j) - \Gamma(j)) &\xrightarrow{d} \mathcal{N}(0, W_j),
\end{align}
where $W_j = \sum_{h=-\infty}^{\infty} E[w_t w_t' \otimes w_{t+h-j} w_{t+h-j}'] - \text{vec}(\Gamma(j))\text{vec}(\Gamma(j))'$. The uniform rate is $\sup_{|j| \le M_T} \|\hat{\Gamma}(j) - \Gamma(j)\| = O_p(\sqrt{\log(M_T)/T})$.
\end{lemma}

\begin{proposition}[MSE-Optimal Bandwidth]
For the Bartlett kernel ($q=1$), the MSE-optimal bandwidth minimizes:
\begin{align}
MSE(M_T) &= \frac{M_T}{T} c_1 + \frac{1}{M_T^2} d_1 \|\Omega'\|^2,
\end{align}
where $c_1 = 2\sum_{j} \Gamma(j)^2$ and $d_1 = (\sum_{j} |j| \Gamma(j))^2$. Setting $\partial MSE / \partial M_T = 0$:
\begin{align}
M_T^* &= \left(\frac{2 d_1 \|\Omega'\|^2}{c_1 T}\right)^{1/3} = c_{BT} \left(\frac{\hat{\alpha}(1) T}{1}\right)^{1/3},
\end{align}
with $c_{BT} = 2^{1/3} \cdot 1.1447$. The QS kernel achieves smaller asymptotic MSE at $M_T^* \propto T^{1/5}$ ($q=2$).
\end{proposition}

\noindent\textbf{Spectral density connection.} The long-run variance equals the contour integral of the spectral density:
\begin{align}
\Omega &= \oint_{\|z\|=1} S_{uu}(z)\, dz = \frac{1}{2\pi}\sum_{j=-\infty}^{\infty}\sum_{k=-\infty}^{\infty} \Gamma(j)\, e^{-ij\omega}, \quad \text{with } \left\lfloor M_T / 2\right\rfloor \leq \left\lceil T^{1/3}\right\rceil.
\end{align}
The double summation is absolutely convergent under the mixing conditions of Proposition~1.
"""

    appendix_proof_table = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-et", text_paragraphs=14,
                        equations=[eq_hac_variance])

    motivation = SectionSpec(
        "The Problem of Serial Correlation in Regression Inference", "sec:motivation", text_paragraphs=12,
        tables=[monte_carlo_size_ols],
        subsections=[
            SectionSpec("OLS Standard Errors Under Serial Correlation", "sec:ols-sc", level=2, text_paragraphs=8),
            SectionSpec("Why Classical Corrections Are Insufficient", "sec:ols-insuf", level=2, text_paragraphs=7),
        ],
    )

    kernel_theory = SectionSpec(
        "Kernel Functions and Spectral Density Estimation", "sec:kernels", text_paragraphs=11,
        equations=[eq_bartlett_kernel],
        tables=[kernel_comparison],
        subsections=[
            SectionSpec("Kernel Properties and Positive Semi-Definiteness", "sec:kernel-psd", level=2, text_paragraphs=9),
            SectionSpec("Efficiency Bounds for Kernel Estimators", "sec:kernel-eff", level=2, text_paragraphs=8),
        ],
    )

    hac_theory = SectionSpec(
        "HAC Variance Estimation", "sec:hac-theory", text_paragraphs=12,
        equations=[eq_newey_west, eq_consistency],
        tables=[empirical_application],
        subsections=[
            SectionSpec("The Newey-West Estimator", "sec:nw-estimator", level=2, text_paragraphs=9),
            SectionSpec("Consistency and Asymptotic Normality", "sec:hac-asymptotics", level=2, text_paragraphs=8),
            SectionSpec("Rate of Convergence", "sec:hac-rate", level=2, text_paragraphs=7),
        ],
    )

    bandwidth_selection = SectionSpec(
        "Bandwidth Selection", "sec:bw-selection", text_paragraphs=11,
        equations=[eq_bandwidth_rule, eq_mse_expansion, eq_data_driven_bw],
        tables=[bandwidth_comparison],
        subsections=[
            SectionSpec("Deterministic Bandwidth Rules", "sec:bw-deterministic", level=2, text_paragraphs=8),
            SectionSpec("Data-Driven Bandwidth Selection", "sec:bw-datadriven", level=2, text_paragraphs=9),
        ],
    )

    prewhitening_section = SectionSpec(
        "Pre-Whitening", "sec:prewhitening", text_paragraphs=10,
        equations=[eq_prewhitened],
        tables=[pre_whitening],
        subsections=[
            SectionSpec("AR(1) Pre-Whitening Procedure", "sec:pw-procedure", level=2, text_paragraphs=7),
            SectionSpec("Finite-Sample Performance Improvements", "sec:pw-performance", level=2, text_paragraphs=7),
        ],
    )

    monte_carlo_section = SectionSpec(
        "Monte Carlo Evidence", "sec:mc", text_paragraphs=11,
        tables=[monte_carlo_size_hac, monte_carlo_power, finite_sample_coverage, bootstrap_vs_asymptotic],
        subsections=[
            SectionSpec("Size Performance", "sec:mc-size", level=2, text_paragraphs=8),
            SectionSpec("Power Performance", "sec:mc-power", level=2, text_paragraphs=7),
            SectionSpec("Coverage Rates", "sec:mc-coverage", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-et", text_paragraphs=11)

    appendix_a = SectionSpec(
        "Appendix A: Mathematical Proofs", "sec:appendix-a-et", text_paragraphs=3,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Monte Carlo Design", "sec:appendix-b-et", text_paragraphs=5,
        tables=[appendix_dgp],
    )

    return PaperSpec(
        paper_id="07",
        field_slug="econometric-theory",
        title="Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation: Theory, Bandwidth Selection, and Finite-Sample Performance",
        authors="Miriam Osei-Bonsu, Takeshi Nakamura, Elsa Lindqvist",
        journal_style="old_school",
        abstract=(
            "We provide a unified treatment of heteroskedasticity and autocorrelation consistent (HAC) "
            "covariance matrix estimation, synthesizing the contributions of Newey and West (1987, 1994) "
            "and Andrews (1991). We characterize the asymptotic properties of HAC estimators under strong "
            "mixing, derive MSE-optimal bandwidth sequences, and compare five kernel functions on the "
            "basis of asymptotic efficiency. Monte Carlo experiments across 10,000 replications confirm "
            "that the Quadratic Spectral kernel with data-driven bandwidth achieves the best size control "
            "under high serial correlation, while pre-whitening uniformly reduces MSE by 25-35\\% at all "
            "sample sizes. Formal proofs of HAC consistency, convergence rates, and positive "
            "semi-definiteness of the Bartlett estimator are provided in the appendix."
        ),
        sections=[intro, motivation, kernel_theory, hac_theory, bandwidth_selection,
                  prewhitening_section, monte_carlo_section, conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{newey1987} Newey, W. K. and West, K. D. (1987). A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix. \textit{Econometrica}, 55(3), 703--708.",
            r"\bibitem{newey1994} Newey, W. K. and West, K. D. (1994). Automatic Lag Selection in Covariance Matrix Estimation. \textit{Review of Economic Studies}, 61(4), 631--653.",
            r"\bibitem{andrews1991} Andrews, D. W. K. (1991). Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation. \textit{Econometrica}, 59(3), 817--858.",
            r"\bibitem{andrews1992} Andrews, D. W. K. and Monahan, J. C. (1992). An Improved Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimator. \textit{Econometrica}, 60(4), 953--966.",
            r"\bibitem{white1980} White, H. (1980). A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity. \textit{Econometrica}, 48(4), 817--838.",
            r"\bibitem{hansen1992} Hansen, B. E. (1992). Consistent Covariance Matrix Estimation for Dependent Heterogeneous Processes. \textit{Econometrica}, 60(4), 967--972.",
            r"\bibitem{kiefer2005} Kiefer, N. M. and Vogelsang, T. J. (2005). A New Asymptotic Theory for Heteroskedasticity-Autocorrelation Robust Tests. \textit{Econometric Theory}, 21(6), 1130--1164.",
            r"\bibitem{sun2008} Sun, Y., Phillips, P. C. B., and Jin, S. (2008). Optimal Bandwidth Selection in Heteroskedasticity-Autocorrelation Robust Testing. \textit{Econometrica}, 76(1), 175--194.",
        ],
        target_pages=50,
        qa=[
            {"question": "What conditions on bandwidth M_T ensure HAC consistency?", "answer": "M_T -> infinity and M_T / T^(1/2) -> 0"},
            {"question": "Which kernel has the highest asymptotic efficiency?", "answer": "Quadratic Spectral (QS) kernel with efficiency 1.421 relative to Bartlett"},
            {"question": "What is the Newey-West bandwidth rule?", "answer": "floor(4 * (T/100)^(2/9))"},
            {"question": "By how much does pre-whitening reduce MSE?", "answer": "Approximately 25-35% at all sample sizes"},
            {"question": "What is the empirical rejection rate of OLS t-tests under AR(1) errors with rho=0.5 at T=250?", "answer": "19.8 percent (versus 5 percent nominal)"},
        ],
    )


PAPER_BUILDERS["07"] = _paper_07_econometric_theory
