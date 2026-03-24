#!/usr/bin/env python3
"""Paper builder for paper 15 (Economic History)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_15_economic_history() -> PaperSpec:
    # --- Tables ---
    country_summary = render_regression_table({
        "table_id": "country-summary",
        "caption": "Summary Statistics: Country-Level Variables",
        "label": "tab:country-summary",
        "model_labels": ["Mean", "SD", "Min", "Max"],
        "panels": [{
            "dep_var": "Panel A: Economic Outcomes (2000)",
            "variables": [
                {"label": "Log GDP per capita (PPP, 2000)", "coefficients": ["7.84", "1.14", "5.42", "10.21"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Real GDP Growth 1970-2000 (\\%/yr)", "coefficients": ["1.84", "2.41", "-3.12", "8.14"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Investment Rate (\\% GDP)", "coefficients": ["21.4", "8.2", "4.1", "42.8"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Slave Trade Variables",
            "variables": [
                {"label": "Slaves Exported (log, normalized by area)", "coefficients": ["0.421", "1.842", "-5.298", "4.211"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Atlantic Slave Trade Exports", "coefficients": ["0.281", "1.614", "0.00", "4.012"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Indian Ocean Slave Trade Exports", "coefficients": ["0.112", "0.814", "0.00", "2.814"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Red Sea Slave Trade Exports", "coefficients": ["0.028", "0.241", "0.00", "1.214"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel C: Institutional and Social Outcomes",
            "variables": [
                {"label": "Ethnic Fractionalization (ELF index)", "coefficients": ["0.614", "0.248", "0.041", "0.981"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Trust (World Values Survey)", "coefficients": ["0.148", "0.114", "0.021", "0.481"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Rule of Law Index", "coefficients": ["-0.412", "0.814", "-2.141", "1.984"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Countries", "values": ["52", "52", "52", "52"]},
            {"label": "Sub-Saharan African countries", "values": ["40", "40", "40", "40"]},
        ],
        "notes": "Sample: 52 African countries. Slave trade data from Nunn (2008) historical shipping records. Trust from WVS waves 1, 2, 3. Ethnic fractionalization from Alesina et al. (2003).",
        "qa": [
            {"question": "What is the mean log GDP per capita (PPP, 2000) for the sample?", "answer": "7.84"},
            {"question": "How many African countries are in the sample?", "answer": "52"},
            {"question": "What is the mean ethnic fractionalization index?", "answer": "0.614"},
            {"question": "What is the mean trust level from the World Values Survey?", "answer": "0.148"},
        ],
    })

    ols_slave_gdp = render_regression_table({
        "table_id": "ols-slave-gdp",
        "caption": "OLS: Slave Trade and Contemporary Economic Development",
        "label": "tab:ols-slave-gdp",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita (2000)",
            "variables": [
                {"label": "Log Slaves Exported (normalized)", "coefficients": ["-0.214***", "-0.184***", "-0.162***", "-0.148***"],
                 "std_errors": ["(0.041)", "(0.038)", "(0.040)", "(0.038)"]},
                {"label": "Log Atlantic Slave Trade", "coefficients": ["--", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Area (log)", "coefficients": ["0.141**", "0.128**", "0.121**", "0.114**"],
                 "std_errors": ["(0.064)", "(0.061)", "(0.064)", "(0.062)"]},
                {"label": "Latitude (absolute)", "coefficients": ["0.842***", "0.814***", "0.784***", "0.761***"],
                 "std_errors": ["(0.184)", "(0.178)", "(0.182)", "(0.179)"]},
                {"label": "Fraction Muslim", "coefficients": ["--", "-0.481**", "-0.441**", "-0.418**"],
                 "std_errors": ["", "(0.218)", "(0.222)", "(0.218)"]},
                {"label": "Fraction Catholic", "coefficients": ["--", "0.284", "0.261", "0.248"],
                 "std_errors": ["", "(0.214)", "(0.218)", "(0.214)"]},
                {"label": "Legal Origin: French", "coefficients": ["--", "--", "-0.284**", "-0.261**"],
                 "std_errors": ["", "", "(0.128)", "(0.124)"]},
                {"label": "Former British Colony", "coefficients": ["--", "--", "--", "0.318**"],
                 "std_errors": ["", "", "", "(0.148)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
            {"label": "R-squared", "values": ["0.341", "0.398", "0.421", "0.448"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Robust SEs. All regressions include a constant. Slave trade exports normalized by country land area.",
        "qa": [
            {"question": "What is the OLS coefficient on log slaves exported in column 1?", "answer": "-0.214"},
            {"question": "What is the R-squared in column 4?", "answer": "0.448"},
            {"question": "What is the coefficient on absolute latitude in column 1?", "answer": "0.842"},
        ],
    })

    iv_first_stage = render_regression_table({
        "table_id": "iv-first-stage",
        "caption": "IV First Stage: Distance to Coast as Instrument",
        "label": "tab:iv-first-stage",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Log Slaves Exported (normalized)",
            "variables": [
                {"label": "Log Distance to Coast (coastline weighted)", "coefficients": ["-0.814***", "-0.784***", "-0.761***", "-0.741***"],
                 "std_errors": ["(0.084)", "(0.081)", "(0.084)", "(0.082)"]},
                {"label": "Log Distance to Ocean (area weighted)", "coefficients": ["--", "-0.218***", "-0.204***", "-0.198***"],
                 "std_errors": ["", "(0.048)", "(0.051)", "(0.049)"]},
                {"label": "Area (log)", "coefficients": ["0.214***", "0.198***", "0.188***", "0.181***"],
                 "std_errors": ["(0.048)", "(0.046)", "(0.048)", "(0.047)"]},
                {"label": "Latitude (absolute)", "coefficients": ["-0.481***", "-0.461***", "-0.441***", "-0.428***"],
                 "std_errors": ["(0.108)", "(0.104)", "(0.108)", "(0.106)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Colonial controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
            {"label": "F-statistic (excluded)", "values": ["94.1", "81.4", "78.2", "72.8"]},
            {"label": "Partial R-squared", "values": ["0.648", "0.698", "0.712", "0.724"]},
        ],
        "notes": "*** p<0.01. Distance to coast instruments: coastline-weighted and area-weighted mean distance from population centers to the ocean. F-statistic tests excluded instrument(s). All F-statistics exceed 10.",
        "qa": [
            {"question": "What is the first-stage F-statistic on excluded instruments in column 1?", "answer": "94.1"},
            {"question": "What is the first-stage coefficient on log distance to coast in column 1?", "answer": "-0.814"},
            {"question": "Is the instrument strong (F > 10)?", "answer": "Yes, all first-stage F-statistics exceed 72"},
        ],
    })

    iv_second_stage = render_regression_table({
        "table_id": "iv-second-stage",
        "caption": "IV Second Stage: Slave Trade and Economic Development",
        "label": "tab:iv-second-stage",
        "model_labels": ["(1) 2SLS", "(2) 2SLS", "(3) LIML", "(4) 2SLS+FE"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita (2000)",
            "variables": [
                {"label": "Log Slaves Exported (instrumented)", "coefficients": ["-0.318***", "-0.284***", "-0.291***", "-0.262***"],
                 "std_errors": ["(0.068)", "(0.064)", "(0.071)", "(0.062)"]},
                {"label": "Area (log)", "coefficients": ["0.161**", "0.148**", "0.152**", "0.141**"],
                 "std_errors": ["(0.071)", "(0.068)", "(0.074)", "(0.066)"]},
                {"label": "Latitude (absolute)", "coefficients": ["0.924***", "0.894***", "0.908***", "0.878***"],
                 "std_errors": ["(0.198)", "(0.191)", "(0.204)", "(0.188)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Colonial controls", "values": ["No", "No", "No", "Yes"]},
            {"label": "Region FE", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
            {"label": "First-stage F", "values": ["94.1", "78.2", "78.2", "72.8"]},
            {"label": "Hansen J p-value", "values": ["--", "0.481", "0.481", "0.514"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Instruments: coastline-weighted and area-weighted mean distance to ocean. LIML in column (3). Hansen J tests overidentification (columns 2-4). Robust SEs.",
        "qa": [
            {"question": "What is the 2SLS coefficient on log slaves exported in column 1?", "answer": "-0.318"},
            {"question": "What is the Hansen J overidentification p-value in column 2?", "answer": "0.481"},
            {"question": "What is the LIML coefficient on log slaves exported?", "answer": "-0.291"},
            {"question": "Is the IV coefficient larger or smaller in magnitude than the OLS?", "answer": "Larger in magnitude: IV is -0.318 vs OLS -0.214, consistent with attenuation bias in OLS"},
        ],
    })

    persistence_1400_2000 = render_regression_table({
        "table_id": "persistence-1400-2000",
        "caption": "Long-Run Persistence: 1400 to 2000",
        "label": "tab:persistence-1400-2000",
        "model_labels": ["(1) OLS", "(2) IV", "(3) 1800", "(4) 1900"],
        "panels": [{
            "dep_var": "Panel A: Dep. var. = Log GDP per capita (2000)",
            "variables": [
                {"label": "Slave Trade Intensity (log, 1400-1900)", "coefficients": ["-0.214***", "-0.318***", "-0.248***", "-0.281***"],
                 "std_errors": ["(0.041)", "(0.068)", "(0.048)", "(0.058)"]},
            ],
        }, {
            "dep_var": "Panel B: Dep. var. = Rule of Law Index (2000)",
            "variables": [
                {"label": "Slave Trade Intensity (log, 1400-1900)", "coefficients": ["-0.184***", "-0.271***", "-0.214***", "-0.241***"],
                 "std_errors": ["(0.038)", "(0.062)", "(0.044)", "(0.052)"]},
            ],
        }, {
            "dep_var": "Panel C: Dep. var. = Trust (WVS 1990s)",
            "variables": [
                {"label": "Slave Trade Intensity (log, 1400-1900)", "coefficients": ["-0.041***", "-0.062***", "-0.048***", "-0.054***"],
                 "std_errors": ["(0.008)", "(0.014)", "(0.010)", "(0.011)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Colonial controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
        ],
        "notes": "*** p<0.01. Slave trade measured over the full 1400-1900 period. Columns (3)-(4) use trade intensity through 1800 and 1900 respectively. IV uses distance instruments.",
        "qa": [
            {"question": "What is the IV coefficient on slave trade intensity for log GDP per capita?", "answer": "-0.318"},
            {"question": "What is the OLS coefficient on slave trade for the trust outcome?", "answer": "-0.041"},
            {"question": "Does the effect persist when measuring trade only through 1800?", "answer": "Yes, coefficient is -0.248 (column 3)"},
        ],
    })

    mechanisms_ethnic_frac = render_regression_table({
        "table_id": "mechanisms-ethnic-frac",
        "caption": "Mechanisms: Slave Trade and Ethnic Fractionalization",
        "label": "tab:mechanisms-ethnic-frac",
        "model_labels": ["(1) OLS", "(2) IV", "(3) + Controls", "(4) IV + Controls"],
        "panels": [{
            "dep_var": "Dep. var.: Ethnic Fractionalization Index",
            "variables": [
                {"label": "Log Slaves Exported (normalized)", "coefficients": ["0.084***", "0.121***", "0.074***", "0.108***"],
                 "std_errors": ["(0.018)", "(0.028)", "(0.016)", "(0.026)"]},
                {"label": "Area (log)", "coefficients": ["0.028**", "0.031**", "0.024**", "0.027**"],
                 "std_errors": ["(0.012)", "(0.014)", "(0.011)", "(0.013)"]},
                {"label": "Latitude (absolute)", "coefficients": ["-0.148", "-0.162", "-0.131", "-0.144"],
                 "std_errors": ["(0.098)", "(0.108)", "(0.094)", "(0.104)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
            {"label": "R-squared / First-stage F", "values": ["0.284", "72.8", "0.321", "72.8"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Ethnic fractionalization from Alesina et al. (2003). IV uses distance-to-coast instruments. Robust SEs.",
        "qa": [
            {"question": "What is the IV coefficient on log slaves exported for ethnic fractionalization?", "answer": "0.121"},
            {"question": "What is the OLS coefficient on slave trade for ethnic fractionalization in column 1?", "answer": "0.084"},
            {"question": "Is the IV coefficient larger than the OLS coefficient?", "answer": "Yes, IV (0.121) > OLS (0.084), suggesting attenuation bias in OLS"},
        ],
    })

    mechanisms_trust = render_regression_table({
        "table_id": "mechanisms-trust",
        "caption": "Mechanisms: Slave Trade, Ethnic Fractionalization, and Trust",
        "label": "tab:mechanisms-trust",
        "model_labels": ["(1) Direct", "(2) Through EF", "(3) Full Chain", "(4) 2SLS"],
        "panels": [{
            "dep_var": "Dep. var.: Trust (World Values Survey)",
            "variables": [
                {"label": "Log Slaves Exported (normalized)", "coefficients": ["-0.041***", "--", "-0.018**", "-0.062***"],
                 "std_errors": ["(0.008)", "", "(0.008)", "(0.014)"]},
                {"label": "Ethnic Fractionalization", "coefficients": ["--", "-0.181***", "-0.148***", "-0.174***"],
                 "std_errors": ["", "(0.038)", "(0.036)", "(0.042)"]},
                {"label": "Area (log)", "coefficients": ["0.008", "0.011", "0.009", "0.010"],
                 "std_errors": ["(0.008)", "(0.009)", "(0.008)", "(0.009)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Colonial controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
            {"label": "R-squared", "values": ["0.421", "0.384", "0.448", "--"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Column (2): slave trade excluded, only ethnic frac. Column (3): mediation specification. Column (4): 2SLS instrumenting slave trade. Robust SEs.",
        "qa": [
            {"question": "What is the direct effect of slave trade on trust in column 1?", "answer": "-0.041"},
            {"question": "What is the coefficient on ethnic fractionalization in the full chain model (column 3)?", "answer": "-0.148"},
            {"question": "What is the 2SLS coefficient on slave trade in column 4?", "answer": "-0.062"},
            {"question": "What is the residual direct effect of slave trade after including ethnic fractionalization?", "answer": "-0.018"},
        ],
    })

    falsification_geography = render_regression_table({
        "table_id": "falsification-geography",
        "caption": "Falsification Tests: Geographic Predictors of Slave Trade",
        "label": "tab:falsification-geography",
        "model_labels": ["Malaria", "Soil Quality", "Rainfall", "Ruggedness"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita 2000 (geography controls added)",
            "variables": [
                {"label": "Log Slaves Exported $\\times$ Geographic var.", "coefficients": ["-0.008", "0.004", "-0.006", "0.003"],
                 "std_errors": ["(0.012)", "(0.011)", "(0.010)", "(0.009)"]},
                {"label": "Log Slaves Exported (main effect)", "coefficients": ["-0.201***", "-0.198***", "-0.204***", "-0.196***"],
                 "std_errors": ["(0.042)", "(0.041)", "(0.043)", "(0.040)"]},
                {"label": "Geographic variable (direct)", "coefficients": ["-0.214***", "0.124**", "0.084*", "-0.041"],
                 "std_errors": ["(0.058)", "(0.052)", "(0.048)", "(0.041)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "52", "52"]},
            {"label": "R-squared", "values": ["0.488", "0.474", "0.461", "0.452"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Each column adds one geographic variable and its interaction with slave trade. Interaction coefficients insignificant, ruling out geographic heterogeneity as confound.",
        "qa": [
            {"question": "Is the slave trade interaction with malaria index statistically significant?", "answer": "No, coefficient is -0.008 with SE (0.012)"},
            {"question": "Does the main effect of slave trade remain significant after adding geographic interactions?", "answer": "Yes, the main effect remains around -0.20 and statistically significant in all columns"},
        ],
    })

    robustness_progressive = render_regression_table({
        "table_id": "robustness-progressive",
        "caption": "Robustness: Progressive Controls and Alternative Samples",
        "label": "tab:robustness-progressive",
        "model_labels": ["Baseline", "+ Religion", "+ Settler Mort.", "+ Legal Origin"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita (2000), 2SLS",
            "variables": [
                {"label": "Log Slaves Exported (instrumented)", "coefficients": ["-0.318***", "-0.298***", "-0.284***", "-0.271***"],
                 "std_errors": ["(0.068)", "(0.064)", "(0.061)", "(0.058)"]},
                {"label": "Fraction Muslim", "coefficients": ["--", "-0.498**", "-0.461**", "-0.444**"],
                 "std_errors": ["", "(0.224)", "(0.218)", "(0.214)"]},
                {"label": "Settler mortality (log)", "coefficients": ["--", "--", "-0.241***", "-0.224***"],
                 "std_errors": ["", "", "(0.068)", "(0.064)"]},
                {"label": "Legal Origin: French", "coefficients": ["--", "--", "--", "-0.298**"],
                 "std_errors": ["", "", "", "(0.134)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["52", "52", "49", "49"]},
            {"label": "First-stage F", "values": ["78.2", "76.4", "71.8", "69.4"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Baseline uses geographic controls only. Each column adds a new control progressively. Sample shrinks in columns 3-4 due to data availability for settler mortality.",
        "qa": [
            {"question": "What is the baseline 2SLS coefficient on slave trade?", "answer": "-0.318"},
            {"question": "Does the slave trade coefficient remain significant when adding settler mortality?", "answer": "Yes, coefficient is -0.284 with SE (0.061)"},
            {"question": "What is the sample size with settler mortality controls?", "answer": "49 countries"},
        ],
    })

    appendix_historical = render_regression_table({
        "table_id": "appendix-historical",
        "caption": "Appendix: Historical Slave Trade Data Validation",
        "label": "tab:appendix-historical",
        "model_labels": ["Atlantic", "Indian Ocean", "Red Sea", "Total"],
        "panels": [{
            "dep_var": "Panel A: Slave Exports by Trade Route (thousands)",
            "variables": [
                {"label": "Total Exports (all periods)", "coefficients": ["8,141", "2,414", "1,241", "11,796"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Peak period exports (per decade)", "coefficients": ["481", "142", "64", "687"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Countries with exports > 0", "coefficients": ["41", "28", "21", "48"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Data Quality Checks",
            "variables": [
                {"label": "Correlation: shipping vs. census", "coefficients": ["0.841", "0.784", "0.714", "0.871"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Correlation: trade route variants", "coefficients": ["0.924", "0.894", "0.841", "0.941"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Countries with data", "values": ["52", "52", "52", "52"]},
        ],
        "notes": "Data assembled from Lovejoy (2000), Eltis and Richardson (2010), and Nunn (2008). Cross-validation against independent census estimates shows correlations above 0.71.",
        "qa": [
            {"question": "How many total slaves were exported across all trade routes?", "answer": "11,796 thousand"},
            {"question": "What fraction of countries have positive Atlantic slave exports?", "answer": "41 out of 52 countries (79 percent)"},
        ],
    })

    # --- Equations ---
    eq_persistence = EquationSpec(
        "persistence-equation",
        r"\log \hat{y}_i = \alpha + \hat{\beta} \log \bar{S}_i + X_i'\gamma + \varepsilon_i, \quad \frac{\partial^2 \log y_i}{\partial (\log S_i) \partial X_i} = \mathcal{F}(\gamma, \beta)",
        "eq:persistence",
        "Main persistence equation: current income $\\log y_i$ on normalized slave exports $\\log S_i$ and geographic controls $X_i$.",
        [{"question": "What is the null hypothesis of no persistence?", "answer": "Beta = 0: slave trade has no long-run effect on current income"}],
    )

    eq_iv_model = EquationSpec(
        "iv-model",
        r"\log S_i = \pi_0 + \pi_1 \log D_i^{coast} + X_i'\pi_2 + \nu_i, \quad \log y_i = \alpha + \beta \widehat{\log S_i} + X_i'\gamma + \varepsilon_i",
        "eq:iv-model",
        "Two-stage least squares: first stage uses distance to coast $D_i^{coast}$ to instrument slave exports; second stage uses predicted exports.",
    )

    eq_historical_channel = EquationSpec(
        "historical-channel",
        r"\log y_i = \alpha + \hat{\beta}_D \log \bar{S}_i + \hat{\beta}_I \text{EF}_i + \hat{\beta}_T \text{Trust}_i + X_i'\gamma + \varepsilon_i, \quad \frac{\partial \log y_i}{\partial \log S_i} = \hat{\beta}_D + \hat{\beta}_I \frac{\partial \text{EF}_i}{\partial \log S_i} + \hat{\beta}_T \frac{\partial \text{Trust}_i}{\partial \log S_i}",
        "eq:historical-channel",
        "Mechanism equation: slave trade affects income through ethnic fractionalization (EF) and social trust. $\\beta_D$ is the direct effect; $\\beta_I \\cdot \\partial\\text{EF}/\\partial S$ and $\\beta_T \\cdot \\partial\\text{Trust}/\\partial S$ are indirect channels.",
    )

    eq_gravity_slave = EquationSpec(
        "gravity-slave-trade",
        r"\\log T_{ij} = \\mu + \\alpha_1 \\log D_{ij} + \\alpha_2 \\log Y_j + \\alpha_3 \\log P_j + \\xi_{ij}",
        "eq:gravity-slave",
        "Gravity model of slave trade flows: bilateral trade $T_{ij}$ from origin $i$ to destination $j$ depends on distance $D_{ij}$, demand $Y_j$, and price $P_j$.",
    )

    eq_ethnic_frac = EquationSpec(
        "ethnic-fractionalization",
        r"\\text{EF}_i = 1 - \\sum_{k=1}^{K_i} \\sum_{l=1}^{K_i} \\bar{s}_{ik} \\bar{s}_{il} \\mathbf{1}[k = l] = 1 - \\sum_{k=1}^{K_i} \\hat{s}_{ik}^2",
        "eq:ethnic-frac",
        "Herfindahl-based ethnic fractionalization index: $s_{ik}$ is the population share of ethnic group $k$ in country $i$.",
    )

    eq_trust_formation = EquationSpec(
        "trust-formation",
        r"\\text{Trust}_{it} = \\rho_0 + \\rho_1 \\text{Trust}_{i,t-1} + \\rho_2 \\text{EF}_{it} + \\rho_3 \\text{Conflict}_{it} + \\eta_{it}",
        "eq:trust-formation",
        "Intergenerational trust formation: current trust depends on lagged trust, ethnic fractionalization, and conflict history.",
        [{"question": "What parameter captures intergenerational persistence of trust?", "answer": "rho_1, the coefficient on lagged trust"}],
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[IV Identification for the Historical Channel]
Let $S_i$ denote slave trade intensity, $\text{EF}_i$ ethnic fractionalization, $\text{Trust}_i$ social trust, and $y_i$ current income. The full causal chain is:
\begin{align}
S_i &\to \text{EF}_i \to \text{Trust}_i \to y_i.
\end{align}
The instrument $Z_i$ (distance to coast) satisfies: (i) relevance: $\text{Cov}(Z_i, S_i) \neq 0$; (ii) exclusion: $\text{Cov}(Z_i, \varepsilon_i) = 0$ conditional on $X_i$; (iii) monotonicity: $\partial S_i / \partial Z_i \leq 0$ for all $i$.

Under these conditions, 2SLS identifies the LATE for the subpopulation of compliers:
\begin{align}
\text{LATE} &= \frac{\text{Cov}(Z_i, y_i)}{\text{Cov}(Z_i, S_i)},
\end{align}
where the exclusion restriction ensures indirect channel effects are absorbed into the structural equation.
\end{proposition}

\begin{proposition}[Persistence Under Intergenerational Transmission]
Let $W_{it}$ be a latent state variable (e.g., trust, institutional quality) with transition:
\begin{align}
W_{it} = \rho W_{i,t-1} + \phi S_i + u_{it},
\end{align}
where $S_i$ is the permanent slave trade shock and $|\rho| < 1$ governs intergenerational persistence. The long-run steady state is:
\begin{align}
W_i^* = \frac{\phi}{1-\rho} S_i + \frac{E[u_{it}]}{1-\rho}.
\end{align}
The long-run effect of slave trade on income through $W$ is:
\begin{align}
\frac{\partial \log y_i}{\partial S_i}\bigg|_{\text{long-run}} &= \beta_W \cdot \frac{\phi}{1-\rho},
\end{align}
exceeding the short-run impact $\beta_W \phi$ by the persistence multiplier $1/(1-\rho)$. For $\rho = 0.8$ (estimated), the long-run multiplier is 5.
\end{proposition}

\begin{proposition}[Decomposition: Direct vs. Indirect Effects of Slave Trade]
The total effect of slave trade on income decomposes as:
\begin{align}
\frac{d \log y_i}{d \log S_i} &= \underbrace{\beta_D}_{\text{direct}} + \underbrace{\beta_I \frac{\partial \text{EF}_i}{\partial \log S_i}}_{\text{ethnic channel}} + \underbrace{\beta_T \frac{\partial \text{Trust}_i}{\partial \log S_i}}_{\text{trust channel}},
\end{align}
where $\hat{\beta}_D$ is the residual direct effect and the two indirect channels operate through ethnic fractionalization and trust. Under the parameter estimates ($\hat{\beta}_I = -0.181$, $\partial\text{EF}/\partial S = 0.121$, $\partial\text{Trust}/\partial S = -0.041$), the ethnic fractionalization channel accounts for approximately 69\% of the total effect, the trust channel for 6\%, and the residual direct effect for 6\%.
\end{proposition}

\begin{lemma}[Mixed Partial Derivative of the Slave Trade Channel]
The cross-partial of income with respect to slave trade intensity and geographic controls satisfies:
\begin{align}
\frac{\partial^2 \log y_i}{\partial (\log \bar{S}_i) \partial X_i} = \hat{\beta}_I \frac{\partial^2 \text{EF}_i}{\partial (\log S_i) \partial X_i} + \hat{\beta}_T \frac{\partial^2 \text{Trust}_i}{\partial (\log S_i) \partial X_i} + \mathcal{F}_{\text{direct}}(X_i).
\end{align}
Under the null hypothesis of no geographic heterogeneity, $\frac{\partial^2 \log y_i}{\partial (\log \bar{S}_i) \partial X_i} = 0$ for all $X_i$.
\end{lemma}

\begin{remark}[Double Summation in the EF Index]
The ethnic fractionalization index can be written using a double sum over ethnic groups:
\begin{align}
\text{EF}_i = \sum_{k=1}^{K_i} \sum_{l=1}^{K_i} \hat{s}_{ik} \hat{s}_{il} \mathcal{L}(k \neq l), \quad \mathcal{L}(k \neq l) = 1 - \mathbf{1}[k = l],
\end{align}
where $\mathcal{L}$ denotes the indicator for distinct group membership.
\end{remark}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-econhist",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec(
        "Introduction", "sec:intro-econhist",
        text_paragraphs=14,
        equations=[eq_persistence],
    )

    historical_background = SectionSpec(
        "Historical Background: The African Slave Trades", "sec:history",
        text_paragraphs=12,
        tables=[appendix_historical],
        subsections=[
            SectionSpec("Four Slave Trades of Africa", "sec:history-trades", level=2, text_paragraphs=8),
            SectionSpec("Mechanisms of Economic Disruption", "sec:history-mechanisms", level=2, text_paragraphs=8),
            SectionSpec("Historical Data Sources", "sec:history-data", level=2, text_paragraphs=7),
        ],
    )

    empirical_strategy = SectionSpec(
        "Empirical Strategy", "sec:empirical-econhist",
        text_paragraphs=12,
        equations=[eq_iv_model, eq_gravity_slave],
        tables=[country_summary],
        subsections=[
            SectionSpec("OLS Specification", "sec:empirical-ols", level=2, text_paragraphs=8),
            SectionSpec("Instrumental Variables Strategy", "sec:empirical-iv", level=2, text_paragraphs=9),
            SectionSpec("Identification Concerns", "sec:empirical-id", level=2, text_paragraphs=8),
        ],
    )

    main_results = SectionSpec(
        "Main Results", "sec:results-econhist",
        text_paragraphs=12,
        tables=[ols_slave_gdp, iv_first_stage, iv_second_stage, persistence_1400_2000],
        subsections=[
            SectionSpec("OLS Evidence", "sec:results-ols", level=2, text_paragraphs=8),
            SectionSpec("Instrumental Variables Estimates", "sec:results-iv", level=2, text_paragraphs=9),
            SectionSpec("Long-Run Persistence", "sec:results-persistence", level=2, text_paragraphs=8),
        ],
    )

    mechanisms = SectionSpec(
        "Mechanisms", "sec:mechanisms-econhist",
        text_paragraphs=12,
        equations=[eq_historical_channel, eq_ethnic_frac, eq_trust_formation],
        tables=[mechanisms_ethnic_frac, mechanisms_trust],
        subsections=[
            SectionSpec("Ethnic Fractionalization Channel", "sec:mech-ethnic", level=2, text_paragraphs=9),
            SectionSpec("Social Trust Channel", "sec:mech-trust", level=2, text_paragraphs=9),
            SectionSpec("Institutional Channel", "sec:mech-institutions", level=2, text_paragraphs=8),
        ],
    )

    robustness = SectionSpec(
        "Robustness", "sec:robustness-econhist",
        text_paragraphs=10,
        tables=[falsification_geography, robustness_progressive],
        subsections=[
            SectionSpec("Falsification Tests", "sec:robust-falsify", level=2, text_paragraphs=8),
            SectionSpec("Alternative Specifications", "sec:robust-specs", level=2, text_paragraphs=8),
            SectionSpec("Addressing Measurement Error", "sec:robust-meas", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-econhist", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Theoretical Proofs", "sec:appendix-a-econhist",
        text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Data Construction", "sec:appendix-b-econhist",
        text_paragraphs=6,
    )

    appendix_c = SectionSpec(
        "Appendix C: Additional Robustness", "sec:appendix-c-econhist",
        text_paragraphs=4,
    )

    return PaperSpec(
        paper_id="15",
        field_slug="economic-history",
        title="The Long-Run Effects of the Slave Trade on Economic Development in Africa",
        authors="Amara Kouyate, Isabela Ferreira-Santos, Henrik Lindqvist",
        journal_style="typewriter",
        abstract=(
            "We examine the long-run economic consequences of Africa's four slave trades (Atlantic, Indian "
            "Ocean, Red Sea, and Trans-Saharan) on contemporary development. Using distance to the ocean "
            "as an instrument for slave trade intensity, we find that a one standard deviation increase in "
            "log slave exports reduces current log GDP per capita by 0.318 log points. The IV estimate is "
            "50\\% larger than OLS, consistent with attenuation from measurement error. We trace the "
            "mechanism through two channels: slave trade increased ethnic fractionalization, which in turn "
            "reduced social trust, together accounting for approximately 75\\% of the income effect. "
            "Falsification tests using geographic variables show no spurious interactions. The results "
            "document one of the largest and most persistent effects of historical institutions on "
            "contemporary development documented in the literature."
        ),
        sections=[intro, historical_background, empirical_strategy, main_results, mechanisms,
                  robustness, conclusion, appendix_a, appendix_b, appendix_c],
        bibliography_entries=[
            r"\bibitem{nunn2008} Nunn, N. (2008). The Long-Term Effects of Africa's Slave Trades. \textit{Quarterly Journal of Economics}, 123(1), 139--176.",
            r"\bibitem{nunn2011} Nunn, N. and Wantchekon, L. (2011). The Slave Trade and the Origins of Mistrust in Africa. \textit{American Economic Review}, 101(7), 3221--3252.",
            r"\bibitem{acemoglu2001} Acemoglu, D., Johnson, S., and Robinson, J. A. (2001). The Colonial Origins of Comparative Development. \textit{American Economic Review}, 91(5), 1369--1401.",
            r"\bibitem{alesina2003} Alesina, A., Devleeschauwer, A., Easterly, W., Kurlat, S., and Wacziarg, R. (2003). Fractionalization. \textit{Journal of Economic Growth}, 8(2), 155--194.",
            r"\bibitem{easterly1997} Easterly, W. and Levine, R. (1997). Africa's Growth Tragedy: Policies and Ethnic Divisions. \textit{Quarterly Journal of Economics}, 112(4), 1203--1250.",
            r"\bibitem{lovejoy2000} Lovejoy, P. E. (2000). \textit{Transformations in Slavery: A History of Slavery in Africa}. Cambridge University Press.",
            r"\bibitem{eltis2010} Eltis, D. and Richardson, D. (2010). \textit{Atlas of the Transatlantic Slave Trade}. Yale University Press.",
            r"\bibitem{putnam1993} Putnam, R. D. (1993). \textit{Making Democracy Work: Civic Traditions in Modern Italy}. Princeton University Press.",
        ],
        target_pages=50,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "IV using distance to coast as instrument for slave trade intensity, exploiting the fact that coastal proximity increased slave export exposure"},
            {"question": "What is the 2SLS coefficient on log slaves exported for log GDP per capita?", "answer": "-0.318"},
            {"question": "Why is the IV estimate larger than OLS?", "answer": "Consistent with attenuation bias from measurement error in slave trade data: IV corrects downward bias in OLS"},
            {"question": "What fraction of the income effect operates through ethnic fractionalization?", "answer": "Approximately 69 percent of the total effect"},
            {"question": "What is the first-stage F-statistic?", "answer": "94.1 with one instrument, well above conventional weak-instrument threshold of 10"},
        ],
    )


PAPER_BUILDERS["15"] = _paper_15_economic_history
