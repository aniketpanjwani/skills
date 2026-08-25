#!/usr/bin/env python3
"""Paper builder for paper 03 (Trade)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_03_trade() -> PaperSpec:
    # --- Tables ---
    summary_stats = render_regression_table({
        "table_id": "summary-stats-trade",
        "caption": "Summary Statistics",
        "label": "tab:summary-stats-trade",
        "model_labels": ["Mean", "SD", "p10", "p90"],
        "panels": [{
            "dep_var": "Panel A: Commuting Zone Characteristics",
            "variables": [
                {"label": "Manufacturing Emp. Share", "coefficients": ["0.21", "0.09", "0.09", "0.33"],
                 "std_errors": ["", "", "", ""]},
                {"label": "China Import Exposure (\\$/worker)", "coefficients": ["1842", "1621", "312", "4218"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Mfg. Emp. Change 1990-2007", "coefficients": ["-0.041", "0.031", "-0.089", "-0.008"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Population 1990", "coefficients": ["12.21", "1.34", "10.62", "14.01"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Industry Characteristics",
            "variables": [
                {"label": "China Import Penetration Rate", "coefficients": ["0.089", "0.112", "0.002", "0.241"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Value Added per Worker", "coefficients": ["10.82", "0.61", "9.91", "11.72"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Commuting Zones", "values": ["722", "722", "722", "722"]},
            {"label": "Industries", "values": ["392", "392", "392", "392"]},
        ],
        "notes": "CZs weighted by 1990 population. Import exposure in constant 2000 dollars per worker.",
        "qa": [
            {"question": "What is the mean China import exposure per worker?", "answer": "1842"},
            {"question": "How many commuting zones are in the sample?", "answer": "722"},
            {"question": "What is the mean manufacturing employment share?", "answer": "0.21"},
        ],
    })

    first_stage = render_regression_table({
        "table_id": "first-stage-china-shock",
        "caption": "First Stage: China Import Exposure Instrument",
        "label": "tab:first-stage",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: China Import Exposure (US)",
            "variables": [
                {"label": "China Import Exposure (Other Countries)", "coefficients": ["0.812***", "0.798***", "0.781***", "0.775***"],
                 "std_errors": ["(0.061)", "(0.059)", "(0.063)", "(0.061)"]},
            ],
        }],
        "controls": [
            {"label": "CZ FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Census Division $\\times$ Period FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Pre-period Controls", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Industry Composition Controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1444", "1444", "1444", "1444"]},
            {"label": "F-statistic", "values": ["177.3", "182.1", "168.4", "161.8"]},
            {"label": "R-squared", "values": ["0.482", "0.561", "0.589", "0.612"]},
        ],
        "notes": "*** p<0.01. Instrument: China import exposure predicted from other high-income countries. Clustered SEs at CZ level.",
        "qa": [
            {"question": "What is the first stage coefficient in column 1?", "answer": "0.812"},
            {"question": "What is the first stage F-statistic in column 2?", "answer": "182.1"},
            {"question": "What is the first stage coefficient in column 4?", "answer": "0.775"},
        ],
    })

    main_employment = render_regression_table({
        "table_id": "main-employment",
        "caption": "Effects on Manufacturing Employment",
        "label": "tab:main-employment",
        "model_labels": ["OLS", "IV", "IV", "IV"],
        "panels": [{
            "dep_var": "Dep. var.: Change in Mfg. Emp./Working-Age Pop. (pp)",
            "variables": [
                {"label": "China Import Exposure (\\$/worker)", "coefficients": ["-0.189***", "-0.596***", "-0.549***", "-0.523***"],
                 "std_errors": ["(0.041)", "(0.107)", "(0.099)", "(0.094)"]},
            ],
        }],
        "controls": [
            {"label": "Census Division $\\times$ Period FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Pre-period Controls", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Industry Composition", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1444", "1444", "1444", "1444"]},
            {"label": "CZs", "values": ["722", "722", "722", "722"]},
            {"label": "R-squared", "values": ["0.201", "", "", ""]},
        ],
        "notes": "*** p<0.01. Import exposure in \\$1000 per worker. IV uses other-country exposure as instrument. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the IV coefficient on manufacturing employment in column 2?", "answer": "-0.596"},
            {"question": "What is the OLS coefficient on manufacturing employment in column 1?", "answer": "-0.189"},
            {"question": "What is the IV coefficient in column 4?", "answer": "-0.523"},
        ],
    })

    main_wages = render_regression_table({
        "table_id": "main-wages",
        "caption": "Effects on Wages",
        "label": "tab:main-wages",
        "model_labels": ["OLS", "IV", "IV", "IV"],
        "panels": [{
            "dep_var": "Dep. var.: Change in Log Weekly Wage",
            "variables": [
                {"label": "China Import Exposure (\\$/worker)", "coefficients": ["-0.142***", "-0.441***", "-0.408***", "-0.389***"],
                 "std_errors": ["(0.031)", "(0.088)", "(0.082)", "(0.078)"]},
            ],
        }],
        "controls": [
            {"label": "Census Division $\\times$ Period FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Pre-period Controls", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Industry Composition", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1444", "1444", "1444", "1444"]},
            {"label": "R-squared", "values": ["0.181", "", "", ""]},
        ],
        "notes": "*** p<0.01. IV uses other-country exposure as instrument. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the IV wage coefficient in column 2?", "answer": "-0.441"},
            {"question": "What is the OLS wage coefficient in column 1?", "answer": "-0.142"},
        ],
    })

    mfg_decline = render_regression_table({
        "table_id": "manufacturing-decline",
        "caption": "Decomposition of Manufacturing Employment Decline",
        "label": "tab:mfg-decline",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Change in Mfg. Emp. (pp)",
            "variables": [
                {"label": "China Exposure $\\times$ 1990--2000", "coefficients": ["-0.412***", "-0.489***", "-0.451***", "-0.431***"],
                 "std_errors": ["(0.091)", "(0.104)", "(0.097)", "(0.092)"]},
                {"label": "China Exposure $\\times$ 2000--2007", "coefficients": ["-0.688***", "-0.721***", "-0.697***", "-0.674***"],
                 "std_errors": ["(0.119)", "(0.131)", "(0.122)", "(0.117)"]},
            ],
        }],
        "controls": [
            {"label": "Division FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1444", "1444", "1444", "1444"]},
            {"label": "R-squared", "values": ["0.221", "0.278", "0.304", "0.328"]},
        ],
        "notes": "*** p<0.01. Effects intensified in the 2000s following China's WTO accession. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the IV effect of China exposure on manufacturing employment in the 1990-2000 period in column 2?", "answer": "-0.489"},
            {"question": "What is the IV effect for the 2000-2007 period in column 1?", "answer": "-0.688"},
        ],
    })

    stacked_panels = render_regression_table({
        "table_id": "stacked-panels",
        "caption": "Stacked Panel Estimates: Multiple Outcomes",
        "label": "tab:stacked",
        "model_labels": ["Mfg. Emp.", "Non-Mfg.", "Wages", "Unemp.", "NILF"],
        "panels": [{
            "dep_var": "Dep. var.: 10-year change (pp or log pts)",
            "variables": [
                {"label": "China Exposure (IV)", "coefficients": ["-0.549***", "-0.218***", "-0.408***", "0.214***", "0.391***"],
                 "std_errors": ["(0.099)", "(0.058)", "(0.082)", "(0.061)", "(0.088)"]},
            ],
        }],
        "controls": [
            {"label": "Division $\\times$ Period FE", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1444", "1444", "1444", "1444", "1444"]},
            {"label": "F-statistic", "values": ["168.4", "168.4", "168.4", "168.4", "168.4"]},
        ],
        "notes": "*** p<0.01. Single instrument used for all columns. CZ-clustered SEs.",
        "qa": [
            {"question": "What is the effect of China exposure on the unemployment rate?", "answer": "0.214"},
            {"question": "What is the effect on the not-in-labor-force share?", "answer": "0.391"},
            {"question": "What is the effect on non-manufacturing employment?", "answer": "-0.218"},
        ],
    })

    shift_share_diag = render_regression_table({
        "table_id": "shift-share-diagnostics",
        "caption": "Shift-Share Instrument Diagnostics",
        "label": "tab:ss-diagnostics",
        "model_labels": ["Stat", "Value", "p-value", "Benchmark"],
        "panels": [{
            "dep_var": "Instrument Validity Tests",
            "variables": [
                {"label": "Rotemberg $\\alpha$-weight (\\% positive)", "coefficients": ["72.4", "--", "--", ">50\\%"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Top-5 industry share of $\\hat{\\beta}_{ss}$", "coefficients": ["0.382", "--", "--", "<0.5"],
                 "std_errors": ["", "", "", ""]},
                {"label": "AKM standard error", "coefficients": ["0.118", "--", "0.001", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Overidentification (Hansen J)", "coefficients": ["--", "4.82", "0.421", "--"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "AKM = Adao-Kolesar-Morales inference. Rotemberg weights test whether a few industries drive IV variation.",
        "qa": [
            {"question": "What share of Rotemberg alpha-weights are positive?", "answer": "72.4"},
            {"question": "What is the p-value for the Hansen J overidentification test?", "answer": "0.421"},
        ],
    })

    robustness_clust = render_regression_table({
        "table_id": "robustness-clustering",
        "caption": "Robustness: Alternative Standard Error Approaches",
        "label": "tab:robust-clustering",
        "model_labels": ["CZ Cluster", "State Cluster", "AKM SE", "Conley"],
        "panels": [{
            "dep_var": "Dep. var.: Mfg. Emp. Change",
            "variables": [
                {"label": "China Exposure (IV)", "coefficients": ["-0.549***", "-0.549***", "-0.549***", "-0.549***"],
                 "std_errors": ["(0.099)", "(0.112)", "(0.118)", "(0.104)"]},
            ],
        }],
        "notes": "Coefficient identical across columns; only standard errors vary. *** p<0.01 throughout.",
        "qa": [
            {"question": "What is the AKM standard error for the China exposure coefficient?", "answer": "0.118"},
            {"question": "What is the state-clustered standard error?", "answer": "0.112"},
        ],
    })

    robustness_controls = render_regression_table({
        "table_id": "robustness-controls",
        "caption": "Robustness: Alternative Control Sets",
        "label": "tab:robust-controls",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Mfg. Emp. Change",
            "variables": [
                {"label": "China Exposure (IV)", "coefficients": ["-0.549***", "-0.521***", "-0.537***", "-0.514***"],
                 "std_errors": ["(0.099)", "(0.097)", "(0.101)", "(0.096)"]},
            ],
        }],
        "controls": [
            {"label": "Baseline Controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Automation Exposure", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "Offshorability Index", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1444", "1444", "1444", "1444"]},
        ],
        "notes": "*** p<0.01. Results robust to including alternative measures of technological change.",
        "qa": [
            {"question": "What is the IV coefficient when controlling for automation exposure in column 2?", "answer": "-0.521"},
        ],
    })

    industry_exposure = render_regression_table({
        "table_id": "industry-exposure",
        "caption": "Industry-Level Import Exposure Effects",
        "label": "tab:industry",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Log Industry Employment",
            "variables": [
                {"label": "Industry Import Penetration", "coefficients": ["-0.612***", "-0.589***", "-0.574***", "-0.558***"],
                 "std_errors": ["(0.098)", "(0.094)", "(0.101)", "(0.097)"]},
            ],
        }],
        "controls": [
            {"label": "Industry FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Controls", "values": ["No", "Yes", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["7840", "7840", "7840", "7840"]},
            {"label": "Industries", "values": ["392", "392", "392", "392"]},
        ],
        "notes": "*** p<0.01. Industry-level analysis. SEs clustered at 3-digit SIC code.",
        "qa": [
            {"question": "What is the industry-level effect of import penetration in column 1?", "answer": "-0.612"},
        ],
    })

    regional_var = render_regression_table({
        "table_id": "regional-variation",
        "caption": "Regional Heterogeneity in China Shock Effects",
        "label": "tab:regional",
        "model_labels": ["Northeast", "Midwest", "South", "West"],
        "panels": [{
            "dep_var": "Dep. var.: Mfg. Emp. Change",
            "variables": [
                {"label": "China Exposure (IV)", "coefficients": ["-0.481***", "-0.618***", "-0.529***", "-0.441***"],
                 "std_errors": ["(0.118)", "(0.127)", "(0.112)", "(0.124)"]},
            ],
        }],
        "summary": [
            {"label": "CZs", "values": ["142", "218", "248", "114"]},
        ],
        "notes": "*** p<0.01. Midwest shows largest effects due to higher initial manufacturing concentration.",
        "qa": [
            {"question": "What is the China shock effect in the Midwest?", "answer": "-0.618"},
            {"question": "What region has the smallest effect?", "answer": "West, with coefficient -0.441"},
        ],
    })

    gravity = render_regression_table({
        "table_id": "gravity-model",
        "caption": "Gravity Model Estimates",
        "label": "tab:gravity",
        "model_labels": ["OLS", "PPML", "PPML", "PPML"],
        "panels": [{
            "dep_var": "Dep. var.: Log Bilateral Trade Flows",
            "variables": [
                {"label": "Log Distance", "coefficients": ["-1.182***", "-1.074***", "-1.028***", "-0.994***"],
                 "std_errors": ["(0.041)", "(0.038)", "(0.040)", "(0.037)"]},
                {"label": "Contiguous", "coefficients": ["0.612***", "0.589***", "0.571***", "0.558***"],
                 "std_errors": ["(0.081)", "(0.077)", "(0.082)", "(0.078)"]},
                {"label": "Common Language", "coefficients": ["0.441***", "0.418***", "0.408***", "0.391***"],
                 "std_errors": ["(0.059)", "(0.056)", "(0.061)", "(0.058)"]},
                {"label": "RTA", "coefficients": ["0.321***", "0.298***", "0.285***", "0.274***"],
                 "std_errors": ["(0.047)", "(0.044)", "(0.048)", "(0.046)"]},
            ],
        }],
        "controls": [
            {"label": "Importer FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Exporter FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["48420", "48420", "48420", "48420"]},
            {"label": "R-squared", "values": ["0.681", "0.784", "0.812", "0.831"]},
        ],
        "notes": "*** p<0.01. PPML = Poisson Pseudo Maximum Likelihood. RTA = Regional trade agreement.",
        "qa": [
            {"question": "What is the PPML gravity coefficient on log distance in column 2?", "answer": "-1.074"},
            {"question": "What is the contiguous coefficient in column 1 OLS?", "answer": "0.612"},
        ],
    })

    appendix_instrument = render_regression_table({
        "table_id": "appendix-instrument",
        "caption": "Appendix: Instrument Construction Details",
        "label": "tab:appendix-instrument",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Mfg. Emp. Change (alternative IV)",
            "variables": [
                {"label": "Bartik Instrument (baseline)", "coefficients": ["-0.549***", "--", "--", "--"],
                 "std_errors": ["(0.099)", "", "", ""]},
                {"label": "Excluding Top Industry", "coefficients": ["--", "-0.531***", "--", "--"],
                 "std_errors": ["", "(0.102)", "", ""]},
                {"label": "Leave-one-out", "coefficients": ["--", "--", "-0.541***", "--"],
                 "std_errors": ["", "", "(0.100)", ""]},
                {"label": "Pre-1990 Shares", "coefficients": ["--", "--", "--", "-0.558***"],
                 "std_errors": ["", "", "", "(0.103)"]},
            ],
        }],
        "notes": "*** p<0.01. Various alternative instrument constructions to check robustness.",
        "qa": [
            {"question": "What is the IV coefficient using the leave-one-out instrument?", "answer": "-0.541"},
        ],
    })

    appendix_sectors = render_regression_table({
        "table_id": "appendix-sectors",
        "caption": "Appendix: Effects by Broad Sector",
        "label": "tab:appendix-sectors",
        "model_labels": ["Durables", "Non-Dur.", "Hi-Tech", "Low-Tech"],
        "panels": [{
            "dep_var": "Dep. var.: Emp. Change",
            "variables": [
                {"label": "China Exposure (IV)", "coefficients": ["-0.712***", "-0.418***", "-0.531***", "-0.689***"],
                 "std_errors": ["(0.131)", "(0.098)", "(0.114)", "(0.128)"]},
            ],
        }],
        "summary": [
            {"label": "Industries", "values": ["181", "211", "124", "268"]},
        ],
        "notes": "*** p<0.01. Durable and low-tech sectors show largest employment declines.",
        "qa": [
            {"question": "What is the China shock effect on durable goods employment?", "answer": "-0.712"},
            {"question": "What is the effect on high-tech employment?", "answer": "-0.531"},
        ],
    })

    # --- Equations ---
    eq_bartik = EquationSpec(
        "bartik-instrument",
        r"\Delta IPW_{uit} = \sum_j z_{ijt} \cdot \Delta IPW_{ojt}, \quad z_{ijt} = \frac{L_{ijt-1}}{L_{it-1}}",
        "eq:bartik",
        "Shift-share (Bartik) instrument: local employment shares $z_{ijt}$ interacted with national import growth from other countries.",
        [{"question": "What are the shares in the shift-share instrument?", "answer": "z_ijt = initial employment share of industry j in CZ i"}],
    )

    eq_exposure = EquationSpec(
        "exposure-measure",
        r"\Delta IPW_{uit} = \sum_j \frac{L_{ijt-1}}{L_{it-1}} \cdot \frac{\Delta M_{jt}^{US}}{L_{jt-1}}",
        "eq:exposure",
        "China import exposure per worker: weighted average of industry-level import growth by initial employment shares.",
    )

    eq_gravity = EquationSpec(
        "gravity-equation",
        r"\ln X_{ij} = \alpha + \beta_1 \ln d_{ij} + \beta_2 \text{Contig}_{ij} + \beta_3 \text{Lang}_{ij} + \mu_i + \nu_j + \varepsilon_{ij}, \quad X_{ij} = \int_0^\infty \prod_{k=1}^{K} q_{ijk}(p)\, dp",
        "eq:gravity",
        "Gravity equation with importer and exporter fixed effects.",
    )

    eq_labor_demand = EquationSpec(
        "labor-demand",
        r"\ln L_{ij} = \alpha + \gamma \ln w_{ij} + \delta \int_0^{1} \ln P_{ij}^M(\omega)\,d\omega + X_{ij}'\begin{bmatrix}\beta_1 \\ \beta_2 \\ \vdots \\ \beta_K\end{bmatrix} + \varepsilon_{ij}",
        "eq:labor-demand",
        "Local labor demand equation linking employment to wages and import price.",
    )

    eq_trade_shock = EquationSpec(
        "trade-shock",
        r"\Delta M_{jt} = M_{jt}^{CN} - M_{jt-1}^{CN}, \quad \text{where} \quad M_{jt}^{CN} = \sum_i X_{ijt}^{CN}",
        "eq:trade-shock",
        "Definition of the China trade shock as the change in US imports from China in industry $j$.",
    )

    eq_rotemberg = EquationSpec(
        "rotemberg-weights",
        r"\hat{\beta}_{ss} = \prod_{k=1}^{K}\!\left(\frac{1}{J_k}\right) \sum_j \alpha_j \hat{\beta}_j, \quad \alpha_j = \frac{z_j' M_Z z_j}{\sum_k z_k' M_Z z_k}, \quad M_Z = I - Z(Z'Z)^{-1}Z' = \begin{bmatrix} m_{11} & \cdots & m_{1n} \\ \vdots & \ddots & \vdots \\ m_{n1} & \cdots & m_{nn} \end{bmatrix}",
        "eq:rotemberg",
        "Rotemberg weight decomposition: shift-share IV estimator as weighted average of industry-specific IV estimates.",
    )

    eq_ssiv = EquationSpec(
        "ssiv-estimator",
        r"\hat{\beta}_{SSIV} = \frac{\sum_i \sum_j z_{ij} g_j (Y_i - \bar{Y})}{\sum_i \sum_j z_{ij} g_j (X_i - \bar{X})}",
        "eq:ssiv",
        "Shift-share IV estimator in terms of shares $z_{ij}$ and shocks $g_j$.",
    )

    eq_reduced_form = EquationSpec(
        "reduced-form",
        r"\Delta L_{it} = \alpha + \rho \cdot \Delta IPW_{oit} + X_{it}'\gamma + \varepsilon_{it}",
        "eq:reduced-form",
        "Reduced form regression of employment change on the instrument (other-country exposure).",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[Shift-Share Inference: Adao-Kolesar-Morales]
Let the shift-share instrument be $Z_i = \sum_j s_{ij} g_j$ where $s_{ij}$ are shares and $g_j$ are shocks. Under the assumption that shocks $\{g_j\}$ are independently distributed across industries,
\begin{align}
\sqrt{n} (\hat{\beta}_{SS} - \beta) &\xrightarrow{d} \mathcal{N}(0, V_{AKM}),
\end{align}
where the AKM variance is
\begin{align}
V_{AKM} &= \left(\sum_j s_j^2 \text{Var}(g_j)\right)^{-1} \sum_j s_j^2 \text{Var}(g_j \hat{\varepsilon}_j) \left(\sum_j s_j^2 \text{Var}(g_j)\right)^{-1}.
\end{align}
\end{proposition}

\begin{proof}
The shift-share estimator can be written as
\begin{align}
\hat{\beta}_{SS} - \beta &= \frac{\sum_j \tilde{s}_j g_j \bar{\varepsilon}_j}{\sum_j \tilde{s}_j g_j \bar{X}_j},
\end{align}
where $\tilde{s}_j = \sum_i s_{ij}$ is the aggregate share and $\bar{\varepsilon}_j = \sum_i (s_{ij}/\tilde{s}_j)\varepsilon_i$. Under independence of $g_j$ across $j$, the numerator is a sum of independent terms, enabling CLT application. The AKM variance follows from the delta method.
\end{proof}

\begin{proposition}[Rotemberg Weight Properties]
The Rotemberg weights $\{\alpha_j\}$ satisfy (i) $\sum_j \alpha_j = 1$, (ii) $\alpha_j \geq 0$ implies the instrument is locally identified by industry $j$, and
\begin{align}
\text{plim}\, \hat{\beta}_{SS} &= \sum_j \alpha_j \text{plim}\, \hat{\beta}_j,
\end{align}
so the shift-share estimator is a weighted average of industry-specific IV estimates.
\end{proposition}

\begin{proposition}[Equivalence of SSIV and Control Function]
Under linearity and homoscedasticity, the SSIV estimator is numerically equivalent to the control function estimator that includes $\sum_j z_{ij}(g_j - \bar{g})$ as an additional regressor:
\begin{align}
\hat{\beta}_{SSIV} &= \hat{\beta}_{CF} \quad \text{iff} \quad \text{Cov}(z_{ij}, \varepsilon_i) = 0 \text{ for all } j.
\end{align}
\end{proposition}

\noindent\textbf{General equilibrium adjustment.} The welfare integral over the product space of traded goods is
\begin{align}
\Delta W &= \int_0^1 \prod_{k=1}^{K}\left(\frac{p_k^{post}}{p_k^{pre}}\right)^{-s_k} d\omega - \begin{bmatrix} \Delta L_1 \\ \Delta L_2 \\ \vdots \\ \Delta L_J \end{bmatrix}' \begin{bmatrix} w_1 \\ w_2 \\ \vdots \\ w_J \end{bmatrix}.
\end{align}
The gravity model's structural residual satisfies
\begin{align}
\int_0^\infty \prod_{k=1}^{K} \tau_{ij,k}^{-\sigma_k+1}\, d\mu(k) &= \Gamma\!\left(\frac{\sigma_k - 1}{\theta}\right) \cdot T_{ij}.
\end{align}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-trade",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-trade", text_paragraphs=14, equations=[eq_exposure])

    background = SectionSpec(
        "Background on China's WTO Accession", "sec:background-trade", text_paragraphs=10,
        subsections=[
            SectionSpec("China's Export Growth", "sec:bg-china", level=2, text_paragraphs=7),
            SectionSpec("US Manufacturing Labor Markets", "sec:bg-us", level=2, text_paragraphs=6),
        ],
    )

    model = SectionSpec(
        "Model", "sec:model-trade", text_paragraphs=12,
        equations=[eq_gravity, eq_labor_demand],
        subsections=[
            SectionSpec("Open Economy Framework", "sec:model-open", level=2, text_paragraphs=8),
            SectionSpec("Local Labor Market Equilibrium", "sec:model-llm", level=2, text_paragraphs=7),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-trade", text_paragraphs=10,
        tables=[summary_stats],
        subsections=[
            SectionSpec("Trade Data", "sec:data-trade-data", level=2, text_paragraphs=7),
            SectionSpec("Employment Data", "sec:data-emp", level=2, text_paragraphs=6),
            SectionSpec("Commuting Zone Construction", "sec:data-cz", level=2, text_paragraphs=6),
        ],
    )

    empirical = SectionSpec(
        "Empirical Strategy", "sec:empirical-trade", text_paragraphs=12,
        equations=[eq_bartik, eq_ssiv, eq_rotemberg, eq_reduced_form, eq_trade_shock],
        tables=[first_stage, shift_share_diag],
        subsections=[
            SectionSpec("Shift-Share Instrument", "sec:empirical-ss", level=2, text_paragraphs=9),
            SectionSpec("Identification and Inference", "sec:empirical-id", level=2, text_paragraphs=8),
        ],
    )

    results = SectionSpec(
        "Results", "sec:results-trade", text_paragraphs=10,
        tables=[main_employment, main_wages, mfg_decline, stacked_panels],
        subsections=[
            SectionSpec("Employment Effects", "sec:results-emp", level=2, text_paragraphs=8, tables=[main_employment]),
            SectionSpec("Wage Effects", "sec:results-wages", level=2, text_paragraphs=7, tables=[main_wages]),
            SectionSpec("Decomposition Across Periods", "sec:results-periods", level=2, text_paragraphs=7, tables=[mfg_decline]),
            SectionSpec("Multiple Outcomes", "sec:results-multi", level=2, text_paragraphs=7, tables=[stacked_panels]),
        ],
    )

    robustness = SectionSpec(
        "Robustness", "sec:robust-trade", text_paragraphs=10,
        tables=[robustness_clust, robustness_controls, regional_var],
        subsections=[
            SectionSpec("Standard Error Approaches", "sec:robust-se", level=2, text_paragraphs=7),
            SectionSpec("Alternative Controls", "sec:robust-alt", level=2, text_paragraphs=7),
            SectionSpec("Regional Heterogeneity", "sec:robust-region", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-trade", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Inference Theory", "sec:appendix-a-trade", text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Additional Results", "sec:appendix-b-trade", text_paragraphs=4,
        tables=[industry_exposure, gravity, appendix_instrument],
    )

    appendix_c = SectionSpec(
        "Appendix C: Industry Classification", "sec:appendix-c-trade", text_paragraphs=5,
        tables=[appendix_sectors],
    )

    return PaperSpec(
        paper_id="03",
        field_slug="trade",
        title="The China Syndrome: Local Labor Market Effects of Import Competition in the United States",
        authors="Hiroshi Tanaka, Fatima Al-Rashid, Erik Lindqvist",
        journal_style="restud",
        abstract=(
            "We exploit China's WTO accession to identify the effect of import competition on US local labor markets. "
            "Using a shift-share instrument based on industry employment shares and import growth in other high-income "
            "countries, we find that a \\$1000 increase in China import exposure per worker reduces manufacturing "
            "employment by 0.55 percentage points and log weekly wages by 0.41 log points. Effects intensified "
            "following WTO accession in 2001. Shift-share inference using AKM standard errors confirms statistical "
            "significance. Rotemberg weight diagnostics show the instrument is not dominated by a single industry."
        ),
        sections=[intro, background, model, data, empirical, results, robustness, conclusion,
                  appendix_a, appendix_b, appendix_c],
        bibliography_entries=[
            r"\bibitem{autor2013} Autor, D., Dorn, D., and Hanson, G. H. (2013). The China Syndrome: Local Labor Market Effects of Import Competition in the United States. \textit{American Economic Review}, 103(6), 2121--2168.",
            r"\bibitem{adao2019} Adao, R., Koles\'{a}r, M., and Morales, E. (2019). Shift-Share Designs: Theory and Inference. \textit{Quarterly Journal of Economics}, 134(4), 1949--2010.",
            r"\bibitem{goldsmith2020} Goldsmith-Pinkham, P., Sorkin, I., and Swift, H. (2020). Bartik Instruments: What, When, Why, and How. \textit{American Economic Review}, 110(8), 2586--2624.",
            r"\bibitem{borusyak2022} Borusyak, K., Hull, P., and Jaravel, X. (2022). Quasi-Experimental Shift-Share Research Designs. \textit{Review of Economic Studies}, 89(1), 181--213.",
            r"\bibitem{acemoglu2016} Acemoglu, D., Autor, D., Dorn, D., Hanson, G. H., and Price, B. (2016). Import Competition and the Great US Employment Sag of the 2000s. \textit{Journal of Labor Economics}, 34(S1), S141--S198.",
            r"\bibitem{caliendo2019} Caliendo, L., Dvorkin, M., and Parro, F. (2019). Trade and Labor Market Dynamics: General Equilibrium Analysis of the China Trade Rise. \textit{Econometrica}, 87(3), 741--835.",
        ],
        target_pages=65,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "Shift-share (Bartik) instrument using other high-income countries' import exposure from China"},
            {"question": "What is the main finding for manufacturing employment?", "answer": "A $1000 increase in China import exposure reduces manufacturing employment by 0.549 percentage points (IV estimate)"},
            {"question": "What is the first-stage F-statistic in the baseline specification?", "answer": "182.1"},
            {"question": "How many commuting zones are in the sample?", "answer": "722"},
            {"question": "What is the effect of China exposure on the not-in-labor-force share?", "answer": "0.391 percentage points"},
        ],
    )


PAPER_BUILDERS["03"] = _paper_03_trade
