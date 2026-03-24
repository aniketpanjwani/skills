#!/usr/bin/env python3
"""Paper builder for paper 17 (International Macro)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table, render_math_table,
    PAPER_BUILDERS,
)

# ═══════════════════════════════════════════════════════════════════════════
# Paper 17: International Macro (Obstfeld-Rogoff two-country DSGE style)
# ═══════════════════════════════════════════════════════════════════════════

def _paper_17_international_macro() -> PaperSpec:
    """Paper 17: International Macro — two-country DSGE, Obstfeld-Rogoff style."""

    # ── Tables ──

    tab_calibration = render_math_table({
        "table_id": "calibration-parameters",
        "caption": "Calibration Parameters",
        "label": "tab:calibration-parameters",
        "col_headers": [
            {"text": "Parameter", "latex": "Parameter"},
            {"text": "Symbol", "latex": "Symbol"},
            {"text": "Value", "latex": "Value"},
            {"text": "Source", "latex": "Source"},
        ],
        "rows": [
            {"label": "Discount factor", "label_latex": "Discount factor",
             "cells": [{"text": "beta", "latex": r"$\beta$"},
                       {"text": "0.99", "latex": "0.99"},
                       {"text": "Standard", "latex": "Standard"}]},
            {"label": "Inverse Frisch elasticity", "label_latex": "Inverse Frisch elasticity",
             "cells": [{"text": "phi", "latex": r"$\phi$"},
                       {"text": "1.00", "latex": "1.00"},
                       {"text": "Kimball (1995)", "latex": "Kimball (1995)"}]},
            {"label": "Risk aversion", "label_latex": "Risk aversion",
             "cells": [{"text": "sigma", "latex": r"$\sigma$"},
                       {"text": "2.00", "latex": "2.00"},
                       {"text": "Obstfeld-Rogoff (1996)", "latex": "Obstfeld-Rogoff (1996)"}]},
            {"label": "Trade elasticity", "label_latex": "Trade elasticity",
             "cells": [{"text": "theta", "latex": r"$\theta$"},
                       {"text": "1.50", "latex": "1.50"},
                       {"text": "Hooper-Marquez (1995)", "latex": "Hooper-Marquez (1995)"}]},
            {"label": "Home bias", "label_latex": "Home bias",
             "cells": [{"text": "alpha", "latex": r"$\alpha$"},
                       {"text": "0.72", "latex": "0.72"},
                       {"text": "Trade data", "latex": "Trade data"}]},
            {"label": "Calvo price-stickiness", "label_latex": "Calvo price-stickiness",
             "cells": [{"text": "xi", "latex": r"$\xi$"},
                       {"text": "0.75", "latex": "0.75"},
                       {"text": "Gali-Gertler (1999)", "latex": "Gali-Gertler (1999)"}]},
            {"label": "Taylor rule weight on inflation", "label_latex": "Taylor rule weight on inflation",
             "cells": [{"text": "phi_pi", "latex": r"$\phi_\pi$"},
                       {"text": "1.50", "latex": "1.50"},
                       {"text": "Taylor (1993)", "latex": "Taylor (1993)"}]},
            {"label": "Taylor rule weight on output", "label_latex": "Taylor rule weight on output",
             "cells": [{"text": "phi_y", "latex": r"$\phi_y$"},
                       {"text": "0.50", "latex": "0.50"},
                       {"text": "Taylor (1993)", "latex": "Taylor (1993)"}]},
            {"label": "Steady-state trade share", "label_latex": "Steady-state trade share",
             "cells": [{"text": "gamma", "latex": r"$\gamma$"},
                       {"text": "0.28", "latex": "0.28"},
                       {"text": "BEA/Eurostat", "latex": "BEA/Eurostat"}]},
            {"label": "AR(1) coefficient productivity", "label_latex": "AR(1) coefficient productivity",
             "cells": [{"text": "rho_a", "latex": r"$\rho_a$"},
                       {"text": "0.90", "latex": "0.90"},
                       {"text": "Backus et al. (1992)", "latex": "Backus et al. (1992)"}]},
            {"label": "Std. dev. productivity shock", "label_latex": "Std. dev. productivity shock",
             "cells": [{"text": "sigma_a", "latex": r"$\sigma_a$"},
                       {"text": "0.0071", "latex": "0.0071"},
                       {"text": "Backus et al. (1992)", "latex": "Backus et al. (1992)"}]},
        ],
        "qa": [
            {"question": "What is the calibrated value of the discount factor beta?", "answer": "0.99"},
            {"question": "What is the Calvo price-stickiness parameter?", "answer": "0.75"},
            {"question": "What is the Taylor rule coefficient on inflation?", "answer": "1.50"},
            {"question": "What is the home bias parameter alpha?", "answer": "0.72"},
        ],
    })

    tab_moments = render_regression_table({
        "table_id": "model-moments-vs-data",
        "caption": "Model Moments vs. Data: Business Cycle Statistics",
        "label": "tab:model-moments-vs-data",
        "model_labels": ["Data", "Baseline", "No Rigidities", "Financial Frictions"],
        "panels": [
            {
                "label": "Panel A: Volatilities (\\% std. dev.)",
                "variables": [
                    {"label": "Output", "coefficients": ["1.68", "1.71", "1.89", "1.74"]},
                    {"label": "Consumption", "coefficients": ["1.27", "1.24", "1.41", "1.31"]},
                    {"label": "Investment", "coefficients": ["5.61", "5.43", "6.12", "5.87"]},
                    {"label": "Real exchange rate", "coefficients": ["11.24", "9.87", "4.32", "10.14"]},
                    {"label": "Terms of trade", "coefficients": ["3.14", "3.08", "2.11", "3.19"]},
                    {"label": "Current account / GDP", "coefficients": ["1.82", "1.76", "1.53", "1.91"]},
                ],
            },
            {
                "label": "Panel B: Cross-correlations with output",
                "variables": [
                    {"label": "Consumption", "coefficients": ["0.87", "0.84", "0.92", "0.81"]},
                    {"label": "Investment", "coefficients": ["0.91", "0.88", "0.94", "0.86"]},
                    {"label": "Real exchange rate", "coefficients": ["-0.13", "-0.09", "0.41", "-0.18"]},
                    {"label": "Net exports / GDP", "coefficients": ["-0.47", "-0.44", "-0.51", "-0.49"]},
                ],
            },
        ],
        "notes": "Data moments from G7 countries, 1973Q1-2019Q4, HP-filtered. Baseline model includes nominal rigidities (Calvo pricing) and monetary policy rule. No Rigidities is a flex-price version. Financial Frictions adds Bernanke-Gertler-Gilchrist accelerator.",
        "qa": [
            {"question": "What is the data volatility of the real exchange rate?", "answer": "11.24%"},
            {"question": "What is the baseline model's volatility of the real exchange rate?", "answer": "9.87%"},
            {"question": "What is the cross-correlation of the real exchange rate with output in the data?", "answer": "-0.13"},
            {"question": "Does the flex-price model match the real exchange rate cross-correlation with output?", "answer": "No, it predicts 0.41 vs -0.13 in data"},
        ],
    })

    tab_irf_prod = render_regression_table({
        "table_id": "impulse-response-productivity",
        "caption": "Impulse Responses to a Home Productivity Shock (1\\% Innovation)",
        "label": "tab:impulse-response-productivity",
        "model_labels": ["Impact", "1 Year", "2 Years", "5 Years"],
        "panels": [
            {
                "label": "Panel A: Home country",
                "variables": [
                    {"label": "Output", "coefficients": ["0.71", "0.58", "0.43", "0.14"]},
                    {"label": "Consumption", "coefficients": ["0.38", "0.37", "0.35", "0.21"]},
                    {"label": "Investment", "coefficients": ["1.84", "1.52", "1.11", "0.39"]},
                    {"label": "Real exchange rate (depreciation +)", "coefficients": ["-0.62", "-0.44", "-0.28", "-0.07"]},
                    {"label": "Current account / GDP", "coefficients": ["0.41", "0.29", "0.18", "0.03"]},
                ],
            },
            {
                "label": "Panel B: Foreign country (spillovers)",
                "variables": [
                    {"label": "Output", "coefficients": ["0.12", "0.11", "0.09", "0.04"]},
                    {"label": "Consumption", "coefficients": ["0.18", "0.17", "0.14", "0.07"]},
                    {"label": "Terms of trade (home TOT, deterioration +)", "coefficients": ["0.31", "0.22", "0.14", "0.04"]},
                ],
            },
        ],
        "notes": "All responses are percentage deviations from steady state. Shock is a 1 standard deviation (0.71\\%) innovation to home total factor productivity. Monetary policy follows the estimated Taylor rule. Shaded regions are 90\\% confidence bands from 500 bootstrap replications.",
        "qa": [
            {"question": "What is the impact response of home output to a 1% productivity shock?", "answer": "0.71%"},
            {"question": "What is the impact response of the real exchange rate?", "answer": "-0.62% (appreciation)"},
            {"question": "What is the spillover to foreign output at impact?", "answer": "0.12%"},
            {"question": "What happens to the current account at impact?", "answer": "Rises by 0.41% of GDP"},
        ],
    })

    tab_irf_mon = render_regression_table({
        "table_id": "impulse-response-monetary",
        "caption": "Impulse Responses to a Home Monetary Policy Shock (25 bp Tightening)",
        "label": "tab:impulse-response-monetary",
        "model_labels": ["Impact", "1 Year", "2 Years", "5 Years"],
        "panels": [
            {
                "label": "Panel A: Home country",
                "variables": [
                    {"label": "Output", "coefficients": ["-0.22", "-0.38", "-0.29", "-0.06"]},
                    {"label": "Inflation (annualized pp)", "coefficients": ["-0.09", "-0.27", "-0.31", "-0.08"]},
                    {"label": "Nominal interest rate (pp)", "coefficients": ["0.25", "0.19", "0.11", "0.02"]},
                    {"label": "Real exchange rate (appreciation +)", "coefficients": ["0.84", "0.61", "0.38", "0.07"]},
                ],
            },
            {
                "label": "Panel B: Foreign country (spillovers)",
                "variables": [
                    {"label": "Output", "coefficients": ["-0.07", "-0.11", "-0.08", "-0.02"]},
                    {"label": "Inflation (annualized pp)", "coefficients": ["-0.03", "-0.09", "-0.11", "-0.03"]},
                    {"label": "Nominal interest rate (pp)", "coefficients": ["0.04", "0.07", "0.06", "0.01"]},
                ],
            },
        ],
        "notes": "Responses are percentage deviations from steady state (except interest rates and inflation, which are percentage point deviations). The monetary shock is identified as an unexpected 25 bp increase in the policy rate.",
        "qa": [
            {"question": "What is the impact response of home output to a 25bp tightening?", "answer": "-0.22%"},
            {"question": "What is the peak appreciation of the real exchange rate?", "answer": "0.84% at impact"},
            {"question": "What is the spillover to foreign output at impact?", "answer": "-0.07%"},
        ],
    })

    tab_var_decomp = render_regression_table({
        "table_id": "variance-decomposition",
        "caption": "Variance Decomposition: Share of Variance Explained by Each Shock (\\%)",
        "label": "tab:variance-decomposition",
        "model_labels": ["Home TFP", "Foreign TFP", "Home Mon.", "Foreign Mon.", "Cost-push"],
        "panels": [
            {
                "label": "Panel A: Home country variables",
                "variables": [
                    {"label": "Output", "coefficients": ["62.4", "8.3", "14.2", "4.1", "11.0"]},
                    {"label": "Consumption", "coefficients": ["48.7", "12.1", "18.4", "6.3", "14.5"]},
                    {"label": "Inflation", "coefficients": ["11.3", "3.2", "31.4", "9.8", "44.3"]},
                    {"label": "Interest rate", "coefficients": ["24.1", "5.8", "41.7", "12.3", "16.1"]},
                ],
            },
            {
                "label": "Panel B: International variables",
                "variables": [
                    {"label": "Real exchange rate", "coefficients": ["21.4", "19.8", "27.3", "25.6", "5.9"]},
                    {"label": "Terms of trade", "coefficients": ["31.2", "29.4", "18.1", "17.8", "3.5"]},
                    {"label": "Current account / GDP", "coefficients": ["44.6", "38.7", "8.1", "7.2", "1.4"]},
                ],
            },
        ],
        "notes": "Variance decomposition at the business cycle frequency (6-32 quarters). Columns sum to 100 within rounding error. Home TFP = home total factor productivity shock; Home Mon. = home monetary policy shock.",
        "qa": [
            {"question": "What fraction of home output variance is explained by home TFP shocks?", "answer": "62.4%"},
            {"question": "What is the largest driver of real exchange rate variance?", "answer": "Home monetary policy shocks (27.3%)"},
            {"question": "What fraction of current account variance is explained by TFP shocks combined?", "answer": "83.3% (44.6 + 38.7)"},
        ],
    })

    tab_erd = render_regression_table({
        "table_id": "exchange-rate-disconnect",
        "caption": "Exchange Rate Disconnect: Correlations Between Exchange Rates and Macro Aggregates",
        "label": "tab:exchange-rate-disconnect",
        "model_labels": ["Data", "Baseline", "Incomplete Mkts", "PCP Pricing"],
        "panels": [
            {
                "variables": [
                    {"label": "Corr(RER, rel. output)", "coefficients": ["-0.13", "-0.09", "-0.21", "0.58"]},
                    {"label": "Corr(RER, rel. consumption)", "coefficients": ["0.08", "0.11", "0.71", "0.64"]},
                    {"label": "Corr(NER, price level)", "coefficients": ["0.04", "0.07", "0.03", "0.39"]},
                    {"label": "Backus-Smith correlation", "coefficients": ["0.08", "0.14", "0.68", "0.61"]},
                    {"label": "RER volatility / relative output vol.", "coefficients": ["6.69", "5.77", "3.12", "1.84"]},
                    {"label": "NER volatility / relative price vol.", "coefficients": ["7.34", "6.98", "6.41", "1.72"]},
                ],
            },
        ],
        "notes": "Data: G7, 1973Q1-2019Q4. RER = real exchange rate, NER = nominal exchange rate, PCP = producer currency pricing. Backus-Smith correlation is corr(RER, C/C*). Baseline uses local currency pricing (LCP); PCP pricing uses producer currency.",
        "qa": [
            {"question": "What is the Backus-Smith correlation in the data?", "answer": "0.08"},
            {"question": "What does the incomplete markets model predict for the Backus-Smith correlation?", "answer": "0.68"},
            {"question": "What is the ratio of RER volatility to relative output volatility in the data?", "answer": "6.69"},
        ],
    })

    tab_ca = render_regression_table({
        "table_id": "current-account-dynamics",
        "caption": "Current Account Dynamics: Empirical Evidence and Model Fit",
        "label": "tab:current-account-dynamics",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "dep_var": "Dep. var.: Current account / GDP (t+1)",
                "variables": [
                    {"label": "Current account / GDP (t)",
                     "coefficients": ["0.71***", "0.68***", "0.66***", "0.64***"],
                     "std_errors": ["(0.04)", "(0.04)", "(0.05)", "(0.05)"]},
                    {"label": "Relative output growth",
                     "coefficients": ["", "-0.31***", "-0.28***", "-0.27***"],
                     "std_errors": ["", "(0.08)", "(0.08)", "(0.08)"]},
                    {"label": "Real exchange rate change",
                     "coefficients": ["", "", "0.04**", "0.04**"],
                     "std_errors": ["", "", "(0.02)", "(0.02)"]},
                    {"label": "Terms of trade change",
                     "coefficients": ["", "", "", "0.12***"],
                     "std_errors": ["", "", "", "(0.04)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Country FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["780", "780", "780", "780"]},
            {"label": "$R^2$", "values": ["0.51", "0.57", "0.61", "0.63"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Panel of 20 OECD countries, 1980-2019. Standard errors clustered by country.",
        "qa": [
            {"question": "What is the AR(1) coefficient for the current account in column 1?", "answer": "0.71"},
            {"question": "Does relative output growth increase or decrease the current account?", "answer": "Decrease; coefficient is -0.31"},
            {"question": "How many country-year observations?", "answer": "780"},
        ],
    })

    tab_tot = render_regression_table({
        "table_id": "terms-of-trade",
        "caption": "Terms of Trade and International Transmission",
        "label": "tab:terms-of-trade",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "dep_var": "Dep. var.: Log terms of trade",
                "variables": [
                    {"label": "Log relative productivity",
                     "coefficients": ["-0.44***", "-0.41***", "-0.38***", "-0.36***"],
                     "std_errors": ["(0.07)", "(0.07)", "(0.08)", "(0.08)"]},
                    {"label": "Log relative money supply",
                     "coefficients": ["", "0.18***", "0.16***", "0.15***"],
                     "std_errors": ["", "(0.05)", "(0.05)", "(0.05)"]},
                    {"label": "Trade balance / GDP",
                     "coefficients": ["", "", "-0.21**", "-0.19**"],
                     "std_errors": ["", "", "(0.09)", "(0.09)"]},
                    {"label": "Relative fiscal balance",
                     "coefficients": ["", "", "", "0.07"],
                     "std_errors": ["", "", "", "(0.06)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Country-pair FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1560", "1560", "1560", "1560"]},
            {"label": "$R^2$", "values": ["0.22", "0.41", "0.47", "0.48"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Sample: 40 country pairs (G7 cross-pairs), 1980-2019. Standard errors clustered by country pair.",
        "qa": [
            {"question": "What is the elasticity of terms of trade with respect to relative productivity?", "answer": "-0.44 in baseline"},
            {"question": "Is the effect of relative fiscal balance statistically significant?", "answer": "No, coefficient 0.07 is not significant"},
        ],
    })

    tab_hist = render_regression_table({
        "table_id": "historical-decomposition",
        "caption": "Historical Decomposition of Real Exchange Rate Fluctuations, 1980-2019 (Share of Variance, \\%)",
        "label": "tab:historical-decomposition",
        "model_labels": ["1980-1989", "1990-1999", "2000-2009", "2010-2019"],
        "panels": [
            {
                "variables": [
                    {"label": "Productivity shocks", "coefficients": ["28.4", "31.2", "24.6", "22.1"]},
                    {"label": "Monetary policy shocks", "coefficients": ["41.2", "29.8", "33.7", "38.4"]},
                    {"label": "Demand shocks", "coefficients": ["18.6", "24.3", "21.4", "19.8"]},
                    {"label": "Cost-push shocks", "coefficients": ["11.8", "14.7", "20.3", "19.7"]},
                ],
            },
        ],
        "notes": "Rows sum to 100 within rounding error. Structural shocks identified via sign restrictions following Canova-De Nicolo (2002). Columns correspond to decade subperiods.",
        "qa": [
            {"question": "What was the dominant driver of RER variance in the 1980s?", "answer": "Monetary policy shocks (41.2%)"},
            {"question": "Did the role of productivity shocks increase or decrease from the 1980s to the 2010s?", "answer": "Decreased, from 28.4% to 22.1%"},
        ],
    })

    tab_sensitivity = render_regression_table({
        "table_id": "appendix-sensitivity",
        "caption": "Sensitivity Analysis: Key Model Moments Under Alternative Parameterizations",
        "label": "tab:appendix-sensitivity",
        "model_labels": ["Baseline", "Low sigma", "High theta", "Low xi", "Open economy"],
        "panels": [
            {
                "variables": [
                    {"label": "RER volatility", "coefficients": ["9.87", "7.41", "8.12", "11.34", "10.28"]},
                    {"label": "RER-output corr.", "coefficients": ["-0.09", "-0.07", "-0.14", "-0.11", "-0.08"]},
                    {"label": "Backus-Smith corr.", "coefficients": ["0.14", "0.42", "0.09", "0.08", "0.21"]},
                    {"label": "CA volatility", "coefficients": ["1.76", "1.54", "2.11", "1.83", "2.34"]},
                    {"label": "TOT volatility", "coefficients": ["3.08", "2.84", "2.41", "3.31", "3.67"]},
                ],
            },
        ],
        "notes": "Baseline: sigma=2, theta=1.5, xi=0.75, alpha=0.72. Low sigma: sigma=1. High theta: theta=3. Low xi: xi=0.50 (more price flexibility). Open economy: alpha=0.50.",
        "qa": [
            {"question": "How does lower risk aversion (low sigma) affect the Backus-Smith correlation?", "answer": "It increases from 0.14 to 0.42"},
            {"question": "Which parameterization produces the highest current account volatility?", "answer": "Open economy (2.34)"},
            {"question": "What is the baseline current account volatility?", "answer": "1.76"},
        ],
    })

    # ── Main Equations ──
    eqs_model = [
        EquationSpec("euler-household",
                     r"E_t \left[ \beta \left(\frac{\dot{C}_{t+1}}{\dot{C}_t}\right)^{-\sigma} \frac{P_t}{P_{t+1}} (1 + i_t) \right] = 1, \quad \ddot{C}_t \equiv \frac{d^2 C}{dt^2}, \quad \mathcal{F}_t = \sigma\bigl\{C_s, P_s : s \leq t\bigr\}",
                     "eq:euler",
                     "Household Euler equation for optimal consumption smoothing",
                     [{"question": "What does the Euler equation equate?",
                       "answer": "The marginal cost and marginal benefit of saving: beta * (C_{t+1}/C_t)^{-sigma} * P_t/P_{t+1} * (1+i_t) = 1"}]),
        EquationSpec("budget-constraint",
                     r"P_t C_t + B_t + S_t B_t^* = (1 + i_{t-1}) B_{t-1} + S_t (1 + i_{t-1}^*) B_{t-1}^* + W_t L_t + T_t",
                     "eq:budget",
                     "Household nominal budget constraint with home and foreign bonds",
                     [{"question": "What assets appear in the household budget constraint?",
                       "answer": "Home bonds B_t and foreign bonds B_t* (valued in domestic currency via S_t)"}]),
        EquationSpec("ces-aggregator",
                     r"C_t = \left[ (1-\alpha)^{1/\theta} C_{H,t}^{(\theta-1)/\theta} + \alpha^{1/\theta} C_{F,t}^{(\theta-1)/\theta} \right]^{\theta/(\theta-1)}",
                     "eq:ces",
                     "CES consumption aggregator over home and foreign varieties",
                     [{"question": "What is the trade elasticity in the CES aggregator?",
                       "answer": "theta, the elasticity of substitution between home and foreign goods"}]),
        EquationSpec("uip",
                     r"i_t - i_t^* = E_t \Delta s_{t+1} + \phi_b b_t + \xi_t^{UIP}",
                     "eq:uip",
                     "Uncovered interest parity condition with bond adjustment cost and risk premium",
                     [{"question": "What modification to standard UIP does the model include?",
                       "answer": "A bond adjustment cost term phi_b * b_t and an exogenous risk premium shock xi_t^UIP"}]),
        EquationSpec("current-account",
                     r"\text{CA}_t = \frac{S_t B_t^* - S_{t-1} B_{t-1}^*}{P_t Y_t} = \text{NX}_t + (i_{t-1}^* - \pi_t^*) \frac{S_t B_{t-1}^*}{P_t Y_t}",
                     "eq:current-account",
                     "Current account identity: net exports plus net investment income",
                     [{"question": "How is the current account decomposed?",
                       "answer": "Net exports NX_t plus net investment income on foreign assets"}]),
        EquationSpec("terms-of-trade-eq",
                     r"T_t = \frac{P_{F,t}}{P_{H,t}} = \frac{S_t P_{F,t}^*}{P_{H,t}}",
                     "eq:terms-of-trade",
                     "Terms of trade as ratio of import to export prices",
                     [{"question": "How are the terms of trade defined?",
                       "answer": "Ratio of the foreign good price to home good price: P_F/P_H"}]),
        EquationSpec("nkpc",
                     r"\pi_{H,t} = \beta E_t \pi_{H,t+1} + \kappa \hat{mc}_t, \quad \kappa = \frac{(1-\xi)(1-\beta\xi)}{\xi}, \quad \dot{p}_{H,t} \equiv \iint_{\mathcal{F}_t} \frac{\partial^2 p_H}{\partial z \partial \omega}\, dz\, d\omega",
                     "eq:nkpc",
                     "New Keynesian Phillips Curve for home tradeable goods",
                     [{"question": "What determines the slope of the NKPC?",
                       "answer": "kappa = (1-xi)(1-beta*xi)/xi, which decreases in the Calvo parameter xi"}]),
        EquationSpec("taylor-rule",
                     r"i_t = \rho_i i_{t-1} + (1-\rho_i)\left[\bar{\imath} + \phi_\pi \pi_t + \phi_y \hat{y}_t\right] + \varepsilon_t^m",
                     "eq:taylor",
                     "Monetary policy rule (Taylor rule with interest rate smoothing)",
                     [{"question": "Does the Taylor rule include interest rate smoothing?",
                       "answer": "Yes, the parameter rho_i captures interest rate smoothing"}]),
        EquationSpec("goods-clearing",
                     r"Y_t = C_{H,t} + C_{H,t}^* + G_t, \quad C_{H,t}^* = \alpha^* \left(\frac{S_t P_{H,t}}{P_t^*}\right)^{-\theta} C_t^*",
                     "eq:goods-clearing",
                     "Goods market clearing: home output equals home and foreign demand",
                     [{"question": "What determines foreign demand for home goods?",
                       "answer": "Foreign demand C_{H,t}* depends on the real exchange rate and foreign consumption via the CES demand system"}]),
        EquationSpec("real-exchange-rate",
                     r"\dot{q}_t = \dot{s}_t + \dot{p}_t^* - \dot{p}_t, \quad q_t = (2\alpha - 1) T_t + (2\alpha^* - 1) T_t^*, \quad \ddot{q}_t = \mathcal{F}\!\left(\dot{T}_t, \dot{T}_t^*\right)",
                     "eq:rer",
                     "Real exchange rate as function of terms of trade under LCP pricing",
                     [{"question": "How does the real exchange rate relate to the terms of trade?",
                       "answer": "q_t = (2*alpha - 1)*T_t + (2*alpha* - 1)*T_t*, proportional to home bias and terms of trade"}]),
    ]

    # ── Appendix math (~45 lines) ──
    appendix_proofs_17 = r"""
\subsection*{A.1 Household Lagrangian and First-Order Conditions}

The representative household in the home country maximizes:
\begin{equation}
E_0 \sum_{t=0}^{\infty} \beta^t \left[ \frac{C_t^{1-\sigma}}{1-\sigma} - \frac{L_t^{1+\phi}}{1+\phi} \right]
\end{equation}
subject to the budget constraint (Equation~\ref{eq:budget}). The Lagrangian is:
\begin{align}
\mathcal{L} &= E_0 \sum_{t=0}^\infty \beta^t \Bigg[ \frac{C_t^{1-\sigma}}{1-\sigma} - \frac{L_t^{1+\phi}}{1+\phi} \nonumber \\
&\quad + \lambda_t \Big( (1+i_{t-1})B_{t-1} + S_t(1+i_{t-1}^*)B_{t-1}^* + W_t L_t + T_t - P_t C_t - B_t - S_t B_t^* \Big) \Bigg]
\end{align}
First-order conditions with respect to $C_t$, $B_t$, $B_t^*$, and $L_t$:
\begin{align}
C_t^{-\sigma} &= \lambda_t P_t \label{eq:foc-c} \\
\lambda_t &= \beta (1+i_t) E_t \lambda_{t+1} \label{eq:foc-b} \\
\lambda_t S_t &= \beta (1+i_t^*) E_t [\lambda_{t+1} S_{t+1}] \label{eq:foc-bstar} \\
\frac{L_t^\phi}{W_t/P_t} &= \lambda_t P_t \implies L_t^\phi = C_t^{-\sigma} \frac{W_t}{P_t} \label{eq:foc-l}
\end{align}
Combining (\ref{eq:foc-c}) and (\ref{eq:foc-b}) yields the standard Euler equation~(\ref{eq:euler}). Dividing (\ref{eq:foc-bstar}) by (\ref{eq:foc-b}) gives the UIP condition~(\ref{eq:uip}) up to a Jensen's inequality correction term.

\subsection*{A.2 Log-Linearization Around Steady State}

Let lower-case variables denote log-deviations from steady state: $\hat{x}_t \equiv \ln(X_t/\bar{X})$. The log-linearized Euler equation is:
\begin{equation}
\hat{c}_t = E_t \hat{c}_{t+1} - \frac{1}{\sigma}(i_t - E_t \pi_{t+1} - \bar{r})
\end{equation}
where $\bar{r} = 1/\beta - 1$ is the steady-state real interest rate. Log-linearizing the CES aggregator:
\begin{equation}
\hat{c}_t = (1-\alpha)\hat{c}_{H,t} + \alpha \hat{c}_{F,t}
\end{equation}
and the demand system gives:
\begin{align}
\hat{c}_{H,t} &= -\theta(\hat{p}_{H,t} - \hat{p}_t) + \hat{c}_t \\
\hat{c}_{F,t} &= -\theta(\hat{p}_{F,t} - \hat{p}_t) + \hat{c}_t
\end{align}

\subsection*{A.3 Blanchard-Kahn Conditions for Determinacy}

The model can be written in state-space form:
\begin{equation}
\begin{pmatrix} \hat{\mathbf{x}}_{t+1} \\ E_t \hat{\mathbf{y}}_{t+1} \end{pmatrix} = \mathbf{A} \begin{pmatrix} \hat{\mathbf{x}}_t \\ \hat{\mathbf{y}}_t \end{pmatrix} + \mathbf{B} \hat{\boldsymbol{\varepsilon}}_{t+1}
\end{equation}
where $\hat{\mathbf{x}}_t$ is the vector of predetermined state variables and $\hat{\mathbf{y}}_t$ is the vector of jump variables. The Blanchard-Kahn conditions for a unique stable equilibrium require that the number of eigenvalues of $\mathbf{A}$ outside the unit circle equals the number of jump variables. Under the estimated Taylor rule parameters ($\phi_\pi = 1.5 > 1$), the model satisfies the Taylor principle and determinacy obtains.

\subsection*{A.4 Solution via Undetermined Coefficients}

Conjecture that the solution takes the form $\hat{\mathbf{y}}_t = \mathbf{M} \hat{\mathbf{x}}_t$. Substituting into the system and matching coefficients:
\begin{equation}
\mathbf{M} = \mathbf{A}_{22}^{-1}(\mathbf{M} - \mathbf{A}_{21} - \mathbf{A}_{22}\mathbf{M}\mathbf{A}_{11} - \mathbf{M}\mathbf{A}_{11})
\end{equation}
This matrix equation can be solved via the QZ (generalized Schur) decomposition of $\mathbf{A}$, implemented in the Klein (2000) algorithm. The solution matrices $\mathbf{M}$ and the impulse response functions reported in Tables~\ref{tab:impulse-response-productivity} and~\ref{tab:impulse-response-monetary} are computed using this method.

\subsection*{A.5 Double Integral Representation of Exchange Rate Dynamics}

The continuous-time real exchange rate satisfies:
\begin{equation}
\dot{q}_t = \iint_{\mathcal{F}_t \times \mathcal{F}_t^*} \frac{\partial^2 q}{\partial a \partial a^*}\, da\, da^* + \ddot{q}_t^{\text{residual}},
\end{equation}
where the double integral captures the second-order interaction between home and foreign productivity shocks, and the $\mathcal{F}_t$-measurable filtration defines the information set at time $t$.

\subsection*{A.6 Calligraphic Likelihood for Bayesian Estimation}

The posterior density of the structural parameters $\boldsymbol{\theta}$ conditional on the observed data $\mathbf{Y}$ satisfies:
\begin{equation}
p(\boldsymbol{\theta} \mid \mathbf{Y}) \propto \mathcal{L}(\mathbf{Y} \mid \boldsymbol{\theta}) \cdot p(\boldsymbol{\theta}), \quad \mathcal{L}(\mathbf{Y} \mid \boldsymbol{\theta}) = \prod_{t=1}^{T} \mathcal{F}\!\left(\dot{Y}_t \mid \dot{Y}_{t-1}, \boldsymbol{\theta}\right).
\end{equation}
"""

    proof_block_17 = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proofs_17,
    )

    # ── Sections ──
    sections_17 = [
        SectionSpec("Introduction", "sec:intro-17", text_paragraphs=20),
        SectionSpec("A Two-Country DSGE Model", "sec:model-17", text_paragraphs=18,
                    subsections=[
                        SectionSpec("Households", "sec:households-17", level=2,
                                    text_paragraphs=13, equations=[eqs_model[0], eqs_model[1], eqs_model[2]]),
                        SectionSpec("Firms and Price Setting", "sec:firms-17", level=2,
                                    text_paragraphs=10, equations=[eqs_model[6]]),
                        SectionSpec("Government and Monetary Policy", "sec:government-17", level=2,
                                    text_paragraphs=8, equations=[eqs_model[7]]),
                        SectionSpec("Equilibrium and Market Clearing", "sec:equilibrium-17", level=2,
                                    text_paragraphs=8, equations=[eqs_model[3], eqs_model[4], eqs_model[5], eqs_model[8], eqs_model[9]]),
                    ]),
        SectionSpec("Calibration", "sec:calibration-17", text_paragraphs=14,
                    tables=[tab_calibration],
                    subsections=[
                        SectionSpec("Parameter Values and Sources", "sec:param-values-17", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Model Fit: Moments vs. Data", "sec:moments-17", level=2,
                                    text_paragraphs=8, tables=[tab_moments]),
                    ]),
        SectionSpec("Solution Method", "sec:solution-17", text_paragraphs=12),
        SectionSpec("Quantitative Results", "sec:results-17", text_paragraphs=12,
                    tables=[tab_irf_prod, tab_irf_mon],
                    subsections=[
                        SectionSpec("Impulse Responses to Technology Shocks", "sec:irf-tech-17", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Impulse Responses to Monetary Policy Shocks", "sec:irf-mon-17", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Variance Decomposition and Historical Analysis", "sec:var-decomp-17", level=2,
                                    text_paragraphs=10, tables=[tab_var_decomp, tab_hist]),
                    ]),
        SectionSpec("Sensitivity Analysis", "sec:sensitivity-17", text_paragraphs=10,
                    tables=[tab_erd, tab_ca, tab_tot],
                    subsections=[
                        SectionSpec("Exchange Rate Disconnect", "sec:erd-17", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Current Account and Terms of Trade Dynamics", "sec:ca-tot-17", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Conclusion", "sec:conclusion-17", text_paragraphs=10),
        SectionSpec("Appendix A: Model Derivation", "sec:appendix-a-17", text_paragraphs=6),
        SectionSpec("Appendix B: Log-Linearization", "sec:appendix-b-17", text_paragraphs=6),
        SectionSpec("Appendix C: Additional Results", "sec:appendix-c-17", text_paragraphs=6,
                    tables=[tab_sensitivity, proof_block_17]),
    ]

    bib_17 = [
        r"\bibitem{obstfeld1996} Obstfeld, M. and K. Rogoff (1996). \textit{Foundations of International Macroeconomics}. MIT Press.",
        r"\bibitem{backus1992} Backus, D., P. Kehoe, and F. Kydland (1992). ``International Real Business Cycles.'' \textit{Journal of Political Economy}, 100(4), 745--775.",
        r"\bibitem{gali1999} Gali, J. and M. Gertler (1999). ``Inflation Dynamics: A Structural Econometric Analysis.'' \textit{Journal of Monetary Economics}, 44(2), 195--222.",
        r"\bibitem{clarida1999} Clarida, R., J. Gali, and M. Gertler (1999). ``The Science of Monetary Policy: A New Keynesian Perspective.'' \textit{Journal of Economic Literature}, 37(4), 1661--1707.",
        r"\bibitem{coeurdacier2010} Coeurdacier, N. and H. Rey (2013). ``Home Bias in Open Economy Financial Macroeconomics.'' \textit{Journal of Economic Literature}, 51(1), 63--115.",
        r"\bibitem{engel1999} Engel, C. (1999). ``Accounting for U.S. Real Exchange Rate Changes.'' \textit{Journal of Political Economy}, 107(3), 507--538.",
        r"\bibitem{betts2000} Betts, C. and M. Devereux (2000). ``Exchange Rate Dynamics in a Model of Pricing-to-Market.'' \textit{Journal of International Economics}, 50(1), 215--244.",
        r"\bibitem{klein2000} Klein, P. (2000). ``Using the Generalized Schur Form to Solve a Multivariate Linear Rational Expectations Model.'' \textit{Journal of Economic Dynamics and Control}, 24(10), 1405--1423.",
    ]

    return PaperSpec(
        paper_id="17",
        field_slug="international-macro",
        title="Exchange Rate Dynamics and International Transmission in a Two-Country DSGE Model",
        authors="Chiara Benedetti \\and Kwame Asante \\and Linh Nguyen",
        journal_style="jpe",
        abstract=(
            "We develop and estimate a two-country dynamic stochastic general equilibrium model "
            "with nominal rigidities, local currency pricing, and incomplete international financial "
            "markets. The model is calibrated to G7 data for 1973-2019. We find that the model "
            "can account for the high volatility and low cross-correlations of real exchange rates -- "
            "the exchange rate disconnect puzzle -- when combined with local currency pricing and "
            "incomplete markets. Variance decomposition reveals that monetary policy shocks account "
            "for 27 percent of real exchange rate variance, while productivity shocks explain 21 "
            "percent. Impulse responses show that a home productivity shock appreciates the "
            "real exchange rate on impact and improves the current account, with significant "
            "spillovers to the foreign country. A 25 basis point monetary tightening generates "
            "a real appreciation of 0.84 percent and contracts foreign output by 0.07 percent. "
            "These results are robust to alternative parameterizations of the trade elasticity, "
            "risk aversion, and degree of price stickiness."
        ),
        sections=sections_17,
        bibliography_entries=bib_17,
        target_pages=65,
        qa=[
            {"question": "What puzzle does the model address?",
             "answer": "The exchange rate disconnect puzzle -- real exchange rates are highly volatile but weakly correlated with macro fundamentals"},
            {"question": "What fraction of real exchange rate variance do monetary policy shocks explain?",
             "answer": "27 percent"},
            {"question": "What is the Calvo price stickiness parameter?",
             "answer": "0.75"},
            {"question": "What is the impact real exchange rate appreciation from a 25bp monetary tightening?",
             "answer": "0.84 percent"},
            {"question": "What journal style is this paper written in?",
             "answer": "JPE (Journal of Political Economy)"},
        ],
    )



PAPER_BUILDERS["17"] = _paper_17_international_macro
