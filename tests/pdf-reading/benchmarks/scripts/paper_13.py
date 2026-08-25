#!/usr/bin/env python3
"""Paper builder for paper 13 (Environmental)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_13_environmental() -> PaperSpec:
    # --- Tables ---
    county_summary = render_regression_table({
        "table_id": "county-summary",
        "caption": "Summary Statistics: U.S. Counties 1968--2002",
        "label": "tab:county-summary",
        "model_labels": ["Mean", "SD", "p10", "p90"],
        "panels": [{
            "dep_var": "Panel A: Outcome Variables",
            "variables": [
                {"label": "All-Cause Mortality Rate (per 100,000)", "coefficients": ["891.4", "184.2", "671.2", "1,124.8"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Age-Adjusted Mortality Rate", "coefficients": ["842.1", "162.4", "641.8", "1,048.2"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Corn Yield (bu/acre)", "coefficients": ["4.21", "0.48", "3.61", "4.84"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Soybean Yield", "coefficients": ["3.84", "0.41", "3.31", "4.41"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Residential Energy (MMBtu)", "coefficients": ["12.84", "0.92", "11.74", "14.01"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Weather Variables",
            "variables": [
                {"label": "Annual Mean Temperature (\\textdegree F)", "coefficients": ["54.8", "10.2", "42.1", "68.4"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Annual Total Precipitation (inches)", "coefficients": ["38.4", "14.8", "20.1", "58.8"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Degree Days $>$ 90\\textdegree F", "coefficients": ["241", "312", "8", "681"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Degree Days 50--59\\textdegree F", "coefficients": ["1,841", "684", "948", "2,814"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Degree Days $<$ 32\\textdegree F", "coefficients": ["814", "618", "41", "1,748"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Counties", "values": ["3,066", "3,066", "3,066", "3,066"]},
            {"label": "Years", "values": ["35", "35", "35", "35"]},
        ],
        "notes": "County-year observations: 107,310. Weather data from NOAA GHCN-D, spatially interpolated to county centroids. Mortality from NCHS vital statistics. Crop yields from USDA NASS.",
        "qa": [
            {"question": "What is the mean all-cause mortality rate?", "answer": "891.4 per 100,000"},
            {"question": "How many counties are in the sample?", "answer": "3,066"},
            {"question": "What is the mean annual degree days above 90F?", "answer": "241"},
            {"question": "What is the sample period?", "answer": "1968--2002, 35 years"},
        ],
    })

    temp_bins_mortality = render_regression_table({
        "table_id": "temp-bins-mortality",
        "caption": "Nonlinear Temperature Effects on Mortality",
        "label": "tab:temp-bins-mortality",
        "model_labels": ["(1) All", "(2) All", "(3) Elderly", "(4) Non-Elderly"],
        "panels": [{
            "dep_var": "Dep. var.: All-Cause Mortality Rate (per 100,000)",
            "variables": [
                {"label": "Days with $T < 10$\\textdegree F", "coefficients": ["1.841***", "1.612***", "6.481***", "0.284**"],
                 "std_errors": ["(0.284)", "(0.271)", "(0.841)", "(0.114)"]},
                {"label": "Days with $T \\in [10, 20)$\\textdegree F", "coefficients": ["0.984***", "0.871***", "3.481***", "0.148*"],
                 "std_errors": ["(0.184)", "(0.176)", "(0.584)", "(0.084)"]},
                {"label": "Days with $T \\in [20, 32)$\\textdegree F", "coefficients": ["0.512***", "0.448***", "1.841***", "0.084"],
                 "std_errors": ["(0.124)", "(0.118)", "(0.384)", "(0.058)"]},
                {"label": "Days with $T \\in [32, 50)$\\textdegree F (omit.)", "coefficients": ["--", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Days with $T \\in [50, 60)$\\textdegree F", "coefficients": ["-0.124", "-0.108", "-0.418", "-0.021"],
                 "std_errors": ["(0.094)", "(0.090)", "(0.314)", "(0.044)"]},
                {"label": "Days with $T \\in [60, 70)$\\textdegree F", "coefficients": ["-0.241**", "-0.218**", "-0.814***", "-0.041"],
                 "std_errors": ["(0.104)", "(0.099)", "(0.341)", "(0.048)"]},
                {"label": "Days with $T \\in [70, 80)$\\textdegree F", "coefficients": ["-0.148", "-0.131", "-0.514*", "-0.028"],
                 "std_errors": ["(0.098)", "(0.094)", "(0.314)", "(0.046)"]},
                {"label": "Days with $T \\in [80, 90)$\\textdegree F", "coefficients": ["0.281***", "0.248***", "0.981***", "0.048"],
                 "std_errors": ["(0.094)", "(0.090)", "(0.314)", "(0.044)"]},
                {"label": "Days with $T > 90$\\textdegree F", "coefficients": ["1.241***", "1.084***", "4.281***", "0.214**"],
                 "std_errors": ["(0.184)", "(0.175)", "(0.584)", "(0.084)"]},
                {"label": "Annual Precipitation (inches)", "coefficients": ["--", "-0.284*", "-0.914**", "-0.048"],
                 "std_errors": ["", "(0.154)", "(0.418)", "(0.071)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Linear county trends", "values": ["No", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "107,310", "107,310", "107,310"]},
            {"label": "R-squared (within)", "values": ["0.892", "0.908", "0.884", "0.841"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05, * p$<$0.1. Standard errors clustered by county. Omitted bin: 32--50\\textdegree F. All specifications include county and state$\\times$year fixed effects.",
        "qa": [
            {"question": "What is the mortality effect of extreme hot days (>90F) in column 2?", "answer": "1.084 deaths per 100,000"},
            {"question": "What is the mortality effect of extreme cold days (<10F) on the elderly in column 3?", "answer": "6.481 deaths per 100,000"},
            {"question": "Which temperature bin is omitted as the baseline?", "answer": "Days with temperature 32--50 degrees F"},
            {"question": "What is the within R-squared in column 1?", "answer": "0.892"},
        ],
    })

    temp_bins_agriculture = render_regression_table({
        "table_id": "temp-bins-agriculture",
        "caption": "Nonlinear Temperature Effects on Agricultural Yields",
        "label": "tab:temp-bins-agriculture",
        "model_labels": ["(1) Corn", "(2) Corn", "(3) Soybeans", "(4) Soybeans"],
        "panels": [{
            "dep_var": "Dep. var.: Log Crop Yield",
            "variables": [
                {"label": "Degree Days 8--29\\textdegree C (beneficial)", "coefficients": ["0.0062***", "0.0058***", "0.0071***", "0.0066***"],
                 "std_errors": ["(0.0008)", "(0.0009)", "(0.0009)", "(0.0010)"]},
                {"label": "Degree Days $>$ 29\\textdegree C (harmful)", "coefficients": ["-0.0184***", "-0.0171***", "-0.0214***", "-0.0198***"],
                 "std_errors": ["(0.0018)", "(0.0019)", "(0.0021)", "(0.0022)"]},
                {"label": "Precipitation (inches)", "coefficients": ["0.0312***", "0.0284***", "0.0281***", "0.0258***"],
                 "std_errors": ["(0.0041)", "(0.0044)", "(0.0046)", "(0.0049)"]},
                {"label": "Precipitation Squared", "coefficients": ["-0.000214***", "-0.000198***", "-0.000194***", "-0.000181***"],
                 "std_errors": ["(0.000028)", "(0.000030)", "(0.000031)", "(0.000033)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Linear county trends", "values": ["No", "Yes", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["71,240", "71,240", "68,414", "68,414"]},
            {"label": "R-squared (within)", "values": ["0.641", "0.684", "0.618", "0.658"]},
        ],
        "notes": "*** p$<$0.01. Corn and soybean yields from USDA NASS 1950--2005, corn-belt counties only. Harmful degree days ($>$29\\textdegree C) have 3$\\times$ larger magnitude effect than beneficial days per unit.",
        "qa": [
            {"question": "What is the harmful degree day coefficient for corn in column 1?", "answer": "-0.0184"},
            {"question": "What is the beneficial degree day coefficient for soybeans in column 3?", "answer": "0.0071"},
            {"question": "What is the ratio of harmful to beneficial degree day effects for corn?", "answer": "Approximately 3x: -0.0184 / 0.0062 = 2.97"},
        ],
    })

    temp_bins_energy = render_regression_table({
        "table_id": "temp-bins-energy",
        "caption": "Nonlinear Temperature Effects on Residential Energy Consumption",
        "label": "tab:temp-bins-energy",
        "model_labels": ["(1) Total", "(2) Elec.", "(3) Gas", "(4) Total"],
        "panels": [{
            "dep_var": "Dep. var.: Log Residential Energy Consumption",
            "variables": [
                {"label": "Heating Degree Days (base 65\\textdegree F)", "coefficients": ["0.000284***", "0.000181***", "0.000418***", "0.000264***"],
                 "std_errors": ["(0.000028)", "(0.000018)", "(0.000041)", "(0.000031)"]},
                {"label": "Cooling Degree Days (base 65\\textdegree F)", "coefficients": ["0.000641***", "0.000812***", "0.000084", "0.000618***"],
                 "std_errors": ["(0.000064)", "(0.000081)", "(0.000084)", "(0.000071)"]},
                {"label": "Log Electricity Price", "coefficients": ["-0.214***", "-0.284***", "--", "-0.218***"],
                 "std_errors": ["(0.041)", "(0.051)", "", "(0.043)"]},
                {"label": "Log Natural Gas Price", "coefficients": ["-0.181***", "--", "-0.241***", "-0.184***"],
                 "std_errors": ["(0.038)", "", "(0.048)", "(0.040)"]},
                {"label": "Log Per-Capita Income", "coefficients": ["0.412***", "0.384***", "0.314***", "0.381***"],
                 "std_errors": ["(0.058)", "(0.054)", "(0.046)", "(0.054)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Linear trends", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "107,310", "107,310", "107,310"]},
            {"label": "R-squared", "values": ["0.814", "0.784", "0.798", "0.831"]},
        ],
        "notes": "*** p$<$0.01. Cooling degree days have larger elasticity than heating degree days, reflecting air conditioning adoption. Column (2): electricity-only; column (3): natural gas only.",
        "qa": [
            {"question": "What is the cooling degree day coefficient for electricity in column 2?", "answer": "0.000812"},
            {"question": "What is the heating degree day coefficient for total energy in column 1?", "answer": "0.000284"},
            {"question": "What is the income elasticity of total energy consumption in column 1?", "answer": "0.412"},
        ],
    })

    linear_temp = render_regression_table({
        "table_id": "linear-temp",
        "caption": "Linear Temperature Specification: Comparison with Nonlinear Estimates",
        "label": "tab:linear-temp",
        "model_labels": ["(1) Linear", "(2) Quadratic", "(3) Bins", "(4) Bins+Trend"],
        "panels": [{
            "dep_var": "Mortality: Effect of 1\\textdegree F Warming (all-cause)",
            "variables": [
                {"label": "Annual Mean Temperature", "coefficients": ["0.481**", "0.214", "--", "--"],
                 "std_errors": ["(0.194)", "(0.281)", "", ""]},
                {"label": "Annual Mean Temperature Squared", "coefficients": ["--", "0.012", "--", "--"],
                 "std_errors": ["", "(0.018)", "", ""]},
                {"label": "Predicted Effect (evaluated at mean)", "coefficients": ["0.481**", "0.284*", "1.241***", "1.084***"],
                 "std_errors": ["(0.194)", "(0.162)", "(0.184)", "(0.175)"]},
            ],
        }, {
            "dep_var": "Agriculture: Effect of 1\\textdegree F Warming (corn yield)",
            "variables": [
                {"label": "Annual Mean Temperature", "coefficients": ["-0.048***", "-0.041**", "--", "--"],
                 "std_errors": ["(0.014)", "(0.018)", "", ""]},
                {"label": "Predicted Effect (evaluated at mean)", "coefficients": ["-0.048***", "-0.044**", "-0.181***", "-0.168***"],
                 "std_errors": ["(0.014)", "(0.019)", "(0.021)", "(0.022)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Linear county trends", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "107,310", "107,310", "107,310"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05, * p$<$0.1. Predicted effects for columns (3) and (4) computed by projecting bin coefficients onto temperature distribution of a uniform 1\\textdegree F shift.",
        "qa": [
            {"question": "What is the predicted mortality effect of 1F warming using the nonlinear bins model (column 3)?", "answer": "1.241"},
            {"question": "Does the linear specification understate or overstate mortality effects relative to bins?", "answer": "Understates: 0.481 vs 1.241"},
        ],
    })

    nonlinear_dose = render_regression_table({
        "table_id": "nonlinear-dose",
        "caption": "Dose-Response Curves: Full Set of Temperature Bins",
        "label": "tab:nonlinear-dose",
        "model_labels": ["Mortality", "Corn", "Soybeans", "Energy"],
        "panels": [{
            "dep_var": "Standardized sector damage per 10-day shift in bin exposure",
            "variables": [
                {"label": "Bin: $T < 10$\\textdegree F", "coefficients": ["0.284***", "0.014", "0.012", "0.418***"],
                 "std_errors": ["(0.044)", "(0.010)", "(0.011)", "(0.064)"]},
                {"label": "Bin: $T \\in [10, 20)$\\textdegree F", "coefficients": ["0.152***", "0.008", "0.007", "0.224***"],
                 "std_errors": ["(0.028)", "(0.007)", "(0.008)", "(0.038)"]},
                {"label": "Bin: $T \\in [20, 32)$\\textdegree F", "coefficients": ["0.079***", "0.004", "0.004", "0.118***"],
                 "std_errors": ["(0.019)", "(0.004)", "(0.004)", "(0.018)"]},
                {"label": "Bin: $T \\in [32, 50)$\\textdegree F (baseline)", "coefficients": ["0.000", "0.000", "0.000", "0.000"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Bin: $T \\in [50, 70)$\\textdegree F", "coefficients": ["-0.037**", "0.018**", "0.022**", "-0.041**"],
                 "std_errors": ["(0.016)", "(0.008)", "(0.009)", "(0.018)"]},
                {"label": "Bin: $T \\in [70, 80)$\\textdegree F", "coefficients": ["-0.023", "0.042***", "0.051***", "-0.028"],
                 "std_errors": ["(0.015)", "(0.012)", "(0.014)", "(0.022)"]},
                {"label": "Bin: $T \\in [80, 90)$\\textdegree F", "coefficients": ["0.043***", "-0.112***", "-0.138***", "0.048***"],
                 "std_errors": ["(0.014)", "(0.024)", "(0.028)", "(0.014)"]},
                {"label": "Bin: $T > 90$\\textdegree F", "coefficients": ["0.191***", "-0.284***", "-0.331***", "0.184***"],
                 "std_errors": ["(0.028)", "(0.044)", "(0.051)", "(0.028)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "71,240", "68,414", "107,310"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05. All outcomes standardized to zero mean and unit variance for cross-sector comparison. Agriculture outcomes inverted so positive = damage.",
        "qa": [
            {"question": "What is the standardized damage from extreme heat (>90F) for mortality?", "answer": "0.191"},
            {"question": "What is the standardized damage from extreme heat for corn yields?", "answer": "-0.284 (in absolute terms, 0.284)"},
        ],
    })

    adaptation_time = render_regression_table({
        "table_id": "adaptation-time",
        "caption": "Adaptation Over Time: Are Temperature Effects Declining?",
        "label": "tab:adaptation-time",
        "model_labels": ["1968--1980", "1981--1993", "1994--2002", "Full Sample"],
        "panels": [{
            "dep_var": "Panel A: Mortality ($>$ 90\\textdegree F bin coefficient)",
            "variables": [
                {"label": "Days with $T > 90$\\textdegree F", "coefficients": ["1.614***", "1.284***", "0.984***", "1.084***"],
                 "std_errors": ["(0.241)", "(0.198)", "(0.184)", "(0.175)"]},
            ],
        }, {
            "dep_var": "Panel B: Agriculture (harmful degree days $>$ 29\\textdegree C)",
            "variables": [
                {"label": "Degree Days $> 29$\\textdegree C", "coefficients": ["-0.0214***", "-0.0184***", "-0.0148***", "-0.0171***"],
                 "std_errors": ["(0.0028)", "(0.0024)", "(0.0021)", "(0.0019)"]},
            ],
        }, {
            "dep_var": "Panel C: Energy (cooling degree day coefficient)",
            "variables": [
                {"label": "Cooling Degree Days", "coefficients": ["0.000941***", "0.000784***", "0.000641***", "0.000618***"],
                 "std_errors": ["(0.000098)", "(0.000084)", "(0.000071)", "(0.000064)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Mortality observations", "values": ["35,970", "42,924", "27,594", "107,310"]},
        ],
        "notes": "*** p$<$0.01. Adaptation test: coefficients declining over time suggest partial adaptation. All three sectors show declining temperature sensitivity, consistent with adaptation but not full neutralization.",
        "qa": [
            {"question": "What is the hot-day mortality coefficient in 1968--1980?", "answer": "1.614"},
            {"question": "What is the hot-day mortality coefficient in 1994--2002?", "answer": "0.984"},
            {"question": "Do temperature effects on agriculture show evidence of adaptation over time?", "answer": "Yes, harmful degree day coefficient falls from -0.0214 to -0.0148 across sub-periods"},
        ],
    })

    adaptation_income = render_regression_table({
        "table_id": "adaptation-income",
        "caption": "Adaptation by Income: Heterogeneity in Temperature Responses",
        "label": "tab:adaptation-income",
        "model_labels": ["Quartile 1", "Quartile 2", "Quartile 3", "Quartile 4"],
        "panels": [{
            "dep_var": "Panel A: Mortality Effect of $T > 90$\\textdegree F (per 100,000)",
            "variables": [
                {"label": "Days with $T > 90$\\textdegree F", "coefficients": ["1.884***", "1.412***", "0.984***", "0.618***"],
                 "std_errors": ["(0.284)", "(0.218)", "(0.184)", "(0.148)"]},
            ],
        }, {
            "dep_var": "Panel B: Agricultural Damage (harmful degree days)",
            "variables": [
                {"label": "Degree Days $> 29$\\textdegree C", "coefficients": ["-0.0248***", "-0.0198***", "-0.0164***", "-0.0121***"],
                 "std_errors": ["(0.0031)", "(0.0026)", "(0.0022)", "(0.0018)"]},
            ],
        }, {
            "dep_var": "Panel C: Energy Response to Cooling Degree Days",
            "variables": [
                {"label": "Cooling Degree Days", "coefficients": ["0.000448***", "0.000584***", "0.000714***", "0.000841***"],
                 "std_errors": ["(0.000048)", "(0.000061)", "(0.000074)", "(0.000088)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "County income quartile", "values": ["Q1 (poorest)", "Q2", "Q3", "Q4 (richest)"]},
        ],
        "summary": [
            {"label": "Observations (mortality)", "values": ["26,828", "26,828", "26,827", "26,827"]},
        ],
        "notes": "*** p$<$0.01. Income quartiles defined by mean county per-capita income over sample period. Poorer counties have higher mortality sensitivity and lower energy adaptation (less AC), but lower agricultural adaptation.",
        "qa": [
            {"question": "What is the hot-day mortality effect for the poorest income quartile?", "answer": "1.884"},
            {"question": "What is the hot-day mortality effect for the richest income quartile?", "answer": "0.618"},
            {"question": "Do richer counties respond more or less to cooling degree days in energy consumption?", "answer": "More: coefficient is 0.000841 vs 0.000448 for poorest, due to higher AC penetration"},
        ],
    })

    panel_fe = render_regression_table({
        "table_id": "panel-fe",
        "caption": "Panel Fixed Effects: Baseline Identification",
        "label": "tab:panel-fe",
        "model_labels": ["(1) OLS", "(2) County FE", "(3) State$\\times$Year", "(4) Both"],
        "panels": [{
            "dep_var": "Dep. var.: All-Cause Mortality Rate",
            "variables": [
                {"label": "Annual Mean Temperature", "coefficients": ["3.841***", "1.284***", "0.841***", "0.481***"],
                 "std_errors": ["(0.284)", "(0.214)", "(0.194)", "(0.148)"]},
                {"label": "Annual Precipitation", "coefficients": ["-0.841***", "-0.284**", "-0.214**", "-0.148*"],
                 "std_errors": ["(0.148)", "(0.114)", "(0.098)", "(0.084)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "107,310", "107,310", "107,310"]},
            {"label": "R-squared", "values": ["0.241", "0.814", "0.784", "0.892"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05, * p$<$0.1. County FE remove time-invariant county characteristics. State$\\times$Year FE absorb common annual shocks within state. Column (4) is preferred specification.",
        "qa": [
            {"question": "What is the preferred specification?", "answer": "Column 4: both county FE and state-by-year FE"},
            {"question": "What is the temperature coefficient in the preferred specification?", "answer": "0.481"},
            {"question": "How does the within R-squared change from OLS to the full FE specification?", "answer": "From 0.241 (OLS) to 0.892 (county + state-year FE)"},
        ],
    })

    panel_trends = render_regression_table({
        "table_id": "panel-trends",
        "caption": "Robustness to Linear County Trends and Flexible Controls",
        "label": "tab:panel-trends",
        "model_labels": ["(1) Baseline", "(2) Trends", "(3) Quad. Trends", "(4) Flexible"],
        "panels": [{
            "dep_var": "Dep. var.: All-Cause Mortality Rate (hot day bins effect)",
            "variables": [
                {"label": "Days with $T > 90$\\textdegree F", "coefficients": ["1.241***", "1.084***", "0.991***", "1.014***"],
                 "std_errors": ["(0.184)", "(0.175)", "(0.168)", "(0.171)"]},
                {"label": "Days with $T < 10$\\textdegree F", "coefficients": ["1.841***", "1.612***", "1.514***", "1.548***"],
                 "std_errors": ["(0.284)", "(0.271)", "(0.258)", "(0.263)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Linear county trends", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "Quadratic county trends", "values": ["No", "No", "Yes", "No"]},
            {"label": "County demographics", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "107,310", "107,310", "107,310"]},
            {"label": "R-squared", "values": ["0.892", "0.908", "0.912", "0.914"]},
        ],
        "notes": "*** p$<$0.01. Baseline (column 1) from Table~\\ref{tab:temp-bins-mortality}. Adding linear county trends reduces extreme heat coefficient by 13\\%, suggesting minimal trend confounding.",
        "qa": [
            {"question": "What is the extreme heat mortality coefficient with linear county trends?", "answer": "1.084"},
            {"question": "By what percentage does adding linear trends reduce the extreme heat coefficient?", "answer": "About 13 percent (1.241 to 1.084)"},
        ],
    })

    sector_heterogeneity = render_regression_table({
        "table_id": "sector-heterogeneity",
        "caption": "Heterogeneity Across Sectors and Demographic Groups",
        "label": "tab:sector-heterogeneity",
        "model_labels": ["Cardiovascular", "Respiratory", "Infant", "Accidental"],
        "panels": [{
            "dep_var": "Mortality by Cause: Effect of $T > 90$\\textdegree F (per 100,000)",
            "variables": [
                {"label": "Days with $T > 90$\\textdegree F", "coefficients": ["0.641***", "0.248***", "0.084**", "0.184***"],
                 "std_errors": ["(0.094)", "(0.064)", "(0.038)", "(0.048)"]},
                {"label": "Days with $T < 10$\\textdegree F", "coefficients": ["0.714***", "0.384***", "0.148***", "0.214***"],
                 "std_errors": ["(0.108)", "(0.074)", "(0.048)", "(0.058)"]},
            ],
        }],
        "controls": [
            {"label": "County FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State $\\times$ Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Linear county trends", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["107,310", "107,310", "107,310", "107,310"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05. Cardiovascular deaths dominate extreme heat mortality effects. Respiratory deaths dominant under cold extremes. Infant mortality significant at both extremes.",
        "qa": [
            {"question": "Which cause of death has the largest effect from extreme heat?", "answer": "Cardiovascular (0.641 per 100,000)"},
            {"question": "What is the effect of extreme cold on respiratory mortality?", "answer": "0.384 per 100,000"},
        ],
    })

    projected_damages_2050 = render_regression_table({
        "table_id": "projected-damages-2050",
        "caption": "Projected Climate Damages by 2050: Monte Carlo Estimates",
        "label": "tab:projected-damages-2050",
        "model_labels": ["Low (10th)", "Central (50th)", "High (90th)", "Mean"],
        "panels": [{
            "dep_var": "Panel A: Mortality (additional deaths per 100,000 per year)",
            "variables": [
                {"label": "IPCC B1 Scenario (+1.5\\textdegree C)", "coefficients": ["0.814", "1.241", "1.841", "1.284"],
                 "std_errors": ["[0.641, 0.991]", "[0.991, 1.514]", "[1.484, 2.241]", "[0.991, 1.584]"]},
                {"label": "IPCC A1B Scenario (+2.8\\textdegree C)", "coefficients": ["1.514", "2.481", "3.841", "2.614"],
                 "std_errors": ["[1.184, 1.841]", "[1.984, 3.014]", "[3.041, 4.684]", "[1.984, 3.284]"]},
                {"label": "IPCC A2 Scenario (+4.1\\textdegree C)", "coefficients": ["2.841", "4.814", "7.841", "5.184"],
                 "std_errors": ["[2.241, 3.481]", "[3.841, 5.814]", "[6.041, 9.641]", "[3.841, 6.584]"]},
            ],
        }, {
            "dep_var": "Panel B: Agricultural Yield Loss (\\%)",
            "variables": [
                {"label": "IPCC B1 Scenario", "coefficients": ["-4.8", "-7.1", "-10.4", "-7.4"],
                 "std_errors": ["[-5.8, -3.8]", "[-8.4, -5.8]", "[-12.1, -8.8]", "[-8.8, -6.1]"]},
                {"label": "IPCC A1B Scenario", "coefficients": ["-9.4", "-14.8", "-21.4", "-15.2"],
                 "std_errors": ["[-11.4, -7.4]", "[-17.4, -12.1]", "[-25.1, -17.8]", "[-17.8, -12.6]"]},
                {"label": "IPCC A2 Scenario", "coefficients": ["-16.4", "-26.8", "-38.4", "-27.2"],
                 "std_errors": ["[-19.4, -13.4]", "[-31.1, -22.1]", "[-44.8, -32.1]", "[-31.4, -23.1]"]},
            ],
        }],
        "summary": [
            {"label": "Monte Carlo draws", "values": ["10,000", "10,000", "10,000", "10,000"]},
            {"label": "Climate model variants", "values": ["18", "18", "18", "18"]},
        ],
        "notes": "Monte Carlo combines uncertainty in (i) temperature projections across 18 CMIP3 models; (ii) statistical parameter uncertainty; (iii) adaptation rate assumptions. Brackets: 80\\% confidence intervals.",
        "qa": [
            {"question": "What is the central mortality damage estimate under the A1B scenario by 2050?", "answer": "2.481 additional deaths per 100,000 per year"},
            {"question": "What is the central agricultural yield loss under the A2 scenario?", "answer": "26.8 percent"},
            {"question": "How many Monte Carlo draws are used?", "answer": "10,000"},
            {"question": "How many CMIP3 climate model variants are used?", "answer": "18"},
        ],
    })

    appendix_weather = render_regression_table({
        "table_id": "appendix-weather",
        "caption": "Appendix: Weather Data Construction and Validation",
        "label": "tab:appendix-weather",
        "model_labels": ["Mean", "SD", "Min", "Max"],
        "panels": [{
            "dep_var": "Panel A: Station Coverage",
            "variables": [
                {"label": "Stations per County", "coefficients": ["4.2", "3.1", "1.0", "18.0"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Fraction with Daily T Data", "coefficients": ["0.941", "0.084", "0.714", "1.000"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Missing Days per Year", "coefficients": ["8.4", "12.1", "0.0", "84.0"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Interpolation Validation (held-out stations)",
            "variables": [
                {"label": "RMSE Annual Mean Temp (\\textdegree F)", "coefficients": ["0.84", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "RMSE Degree Days $>$ 90\\textdegree F", "coefficients": ["12.4", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Correlation (actual vs. interpolated)", "coefficients": ["0.984", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Counties with $\\geq 1$ station", "values": ["2,984", "2,984", "2,984", "2,984"]},
        ],
        "notes": "Temperature data interpolated from GHCN-D stations to county centroids using inverse-distance weighting. Validation on held-out 10\\% of stations. Interpolation error small relative to treatment variation.",
        "qa": [
            {"question": "What is the mean number of weather stations per county?", "answer": "4.2"},
            {"question": "What is the RMSE of the spatial interpolation for annual mean temperature?", "answer": "0.84 degrees F"},
            {"question": "What is the correlation between actual and interpolated temperature?", "answer": "0.984"},
        ],
    })

    # --- Equations ---
    eq_damage_function = EquationSpec(
        "damage-function",
        r"D_j = f(T_j, P_j;\, \theta) = \sum_{k} \theta_k \cdot \mathbf{1}\!\left[T_j \in \mathcal{B}_k\right] \cdot d_j^k, \quad \begin{bmatrix} D_j^{\text{mort}} \\ D_j^{\text{agr}} \\ D_j^{\text{ener}} \end{bmatrix} = \begin{bmatrix} \theta_k^m \\ \theta_k^a \\ \theta_k^e \end{bmatrix} \cdot d_j^k",
        "eq:damage-function",
        "Damage function: county-level damage $D_j$ from climate is a sum of bin-specific effects $\\theta_k$ weighted by days $d_j^k$ in temperature bin $\\mathcal{B}_k$.",
        [{"question": "What does theta_k represent in the damage function?", "answer": "The marginal damage of an additional day in temperature bin B_k"}],
    )

    eq_nonlinear_dose = EquationSpec(
        "nonlinear-dose-response",
        r"y_{ct} = \alpha_c + \gamma_{st} + \sum_{k=1}^{K} \beta_k \cdot \lceil d_{ct}^k \rceil + \mathbf{x}_{ct}'\delta + \varepsilon_{ct}, \quad \ddot{y}_{ct} \equiv y_{ct} - \bar{y}_c - \bar{y}_{st} + \bar{y}",
        "eq:nonlinear-dose",
        "Panel fixed effects estimating equation: outcome $y_{ct}$ for county $c$ in year $t$, with county FE $\\alpha_c$, state$\\times$year FE $\\gamma_{st}$, and temperature bin days $d_{ct}^k$.",
    )

    eq_panel_fe = EquationSpec(
        "panel-fe-equation",
        r"y_{ct} = \alpha_c + \lambda_t + \beta T_{ct} + \gamma P_{ct} + \varepsilon_{ct}, \quad E[\varepsilon_{ct} \mid \alpha_c, \lambda_t, T_{ct}, P_{ct}] = 0",
        "eq:panel-fe",
        "Linear panel fixed effects: within-county, within-year identification exploits year-to-year weather fluctuations after removing permanent differences across counties.",
    )

    eq_adaptation_model = EquationSpec(
        "adaptation-model",
        r"\dot{\beta}_k(\tau) = -\rho\bigl(\beta_k(\tau) - \beta_k^\infty\bigr), \quad \beta_k(\tau) = \beta_k^0 \cdot e^{-\rho \tau} + \beta_k^\infty (1 - e^{-\rho \tau}), \quad k = \lfloor T_j / \Delta T \rfloor",
        "eq:adaptation",
        "Adaptation model: bin coefficient $\\beta_k$ decays from short-run $\\beta_k^0$ toward long-run adapted value $\\beta_k^\\infty$ at rate $\\rho$.",
    )

    eq_projected_damages = EquationSpec(
        "projected-damages",
        r"\\Delta D = \\int_{\\mathbb{R}} \\hat{f}(T)\\,\\bigl[g(T; \\mu_1, \\sigma_1) - g(T; \\mu_0, \\sigma_0)\\bigr]\\,dT",
        "eq:projected-damages",
        "Projected damages: integral of estimated damage function $\\hat{f}(T)$ against the difference in temperature distributions under future ($\\mu_1, \\sigma_1$) vs. baseline ($\\mu_0, \\sigma_0$) climate.",
    )

    eq_wtp = EquationSpec(
        "wtp",
        r"\\text{WTP}_j = \\frac{\\partial D_j / \\partial T_j}{\\partial U_j / \\partial I_j} = \\frac{-\\partial \\ln y_j / \\partial T_j}{\\partial \\ln y_j / \\partial I_j} \\cdot I_j",
        "eq:wtp",
        "Willingness to pay to avoid temperature increase: ratio of marginal climate damage to marginal utility of income, expressed as income share.",
    )

    eq_social_cost = EquationSpec(
        "social-cost",
        r"\\text{SCC} = \\sum_{t=0}^{T} \\sum_j \\frac{\\text{WTP}_{jt}}{(1+r)^t} \\cdot \\frac{\\partial T_{jt}}{\\partial E_0}",
        "eq:scc",
        "Social cost of carbon: discounted sum of marginal willingness to pay for climate stability, weighted by the temperature response to an additional unit of emissions $E_0$ today.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[Nonparametric Identification of Bin Coefficients]
The bin coefficients $\{\beta_k\}_{k=1}^K$ in equation~\eqref{eq:nonlinear-dose} are nonparametrically identified under the assumption that, conditional on county and state-year fixed effects, the allocation of days across temperature bins is as good as random.

Formally, let $\mathbf{d}_{ct} = (d_{ct}^1, \ldots, d_{ct}^K)$ be the vector of annual bin-day counts. The identifying assumption is:
\begin{align}
E[\varepsilon_{ct} \mid \alpha_c, \gamma_{st}, \mathbf{d}_{ct}] = 0.
\end{align}
Under this assumption, OLS consistently estimates $\beta = (\beta_1, \ldots, \beta_K)'$.
\end{proposition}

\begin{proof}
Within-county, within-state-year variation in $\mathbf{d}_{ct}$ is driven by idiosyncratic weather shocks that are orthogonal to county-level unobservables after conditioning on $(\alpha_c, \gamma_{st})$. This follows from the standard argument that daily weather is unpredictable from a long-run perspective: $\text{Cov}(\varepsilon_{ct}, d_{ct}^k \mid \alpha_c, \gamma_{st}) = 0$ for all $k$.
\end{proof}

\begin{proposition}[Adaptation Rate Estimation]
Let the short-run coefficient be $\beta_k^{SR}$ (estimated from high-frequency weather variation) and the long-run coefficient be $\beta_k^{LR}$ (estimated from cross-sectional climate variation, controlling for sorting). The adaptation rate is identified as:
\begin{align}
\rho = -\frac{1}{\bar{\tau}} \ln\!\left(\frac{\beta_k^{LR} - \beta_k^\infty}{\beta_k^{SR} - \beta_k^\infty}\right),
\end{align}
where $\bar{\tau}$ is the relevant time horizon (e.g., average years since a sustained climate shift) and $\beta_k^\infty$ is the fully-adapted damage under permanent exposure.
\end{proposition}

\begin{proof}
Integrating the adaptation ODE $\dot{\beta}_k = -\rho(\beta_k - \beta_k^\infty)$ gives $\beta_k(\tau) = \beta_k^\infty + (\beta_k^0 - \beta_k^\infty)e^{-\rho\tau}$. Setting $\beta_k^{SR} = \beta_k^0$ and $\beta_k^{LR} = \beta_k(\bar{\tau})$ and solving for $\rho$ yields the stated formula.
\end{proof}

\begin{proposition}[Damage Projection Monte Carlo]
Let $\hat{\beta} \sim \mathcal{N}(\hat{\beta}, \hat{V})$ and let $\Delta g_j(\cdot; \xi)$ be the climate-model-specific temperature distribution shift for model $\xi \in \Xi$. The projected damage is:
\begin{align}
\Delta \hat{D} = \sum_k \hat{\beta}_k \cdot \Delta \bar{d}_k^{\xi},
\end{align}
where $\Delta \bar{d}_k^\xi = \int \mathbf{1}[T \in \mathcal{B}_k] \bigl[g(T;\xi_1) - g(T;\xi_0)\bigr]\,dT$ is the projected change in bin-$k$ exposure under climate model $\xi$. The Monte Carlo distribution is:
\begin{align}
\{\Delta \hat{D}^{(m)}\}_{m=1}^M, \quad \hat{\beta}^{(m)} \sim \mathcal{N}(\hat{\beta}, \hat{V}), \quad \xi^{(m)} \sim \text{Uniform}(\Xi).
\end{align}
Percentiles of this distribution constitute the confidence intervals reported in Table~\ref{tab:projected-damages-2050}.
\end{proposition}

\begin{remark}[Matrix Formulation of Sectoral Damages]
The vector of sectoral damages satisfies:
\begin{align}
\begin{bmatrix} \Delta \hat{D}^{\text{mort}} \\ \Delta \hat{D}^{\text{agr}} \\ \Delta \hat{D}^{\text{ener}} \end{bmatrix} = \begin{bmatrix} \hat{\beta}_1^m & \cdots & \hat{\beta}_K^m \\ \hat{\beta}_1^a & \cdots & \hat{\beta}_K^a \\ \hat{\beta}_1^e & \cdots & \hat{\beta}_K^e \end{bmatrix} \begin{bmatrix} \lceil \Delta \bar{d}_1^\xi \rceil \\ \vdots \\ \lfloor \Delta \bar{d}_K^\xi \rfloor \end{bmatrix},
\end{align}
where the coefficient matrix $\dot{\boldsymbol{B}} \in \mathbb{R}^{3 \times K}$ collects the sector-specific bin effects.
\end{remark}

\begin{lemma}[Adaptation Rate with Floor-Ceiling Binning]
The discrete temperature bin assignment $k = \lfloor T_j / \Delta T \rfloor$ introduces a floor function, so the within-bin average damage is:
\begin{align}
\bar{\beta}_{k}(\tau) = \frac{1}{\lceil \Delta T \rceil - \lfloor \Delta T \rfloor + 1} \int_{\lfloor k \Delta T \rfloor}^{\lceil (k+1) \Delta T \rceil} \dot{\beta}(T, \tau)\, dT.
\end{align}
\end{lemma}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-environ",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec(
        "Introduction", "sec:intro-environ", text_paragraphs=14,
        equations=[eq_damage_function],
    )

    data_section = SectionSpec(
        "Data", "sec:data-environ", text_paragraphs=12,
        tables=[county_summary],
        subsections=[
            SectionSpec("County-Level Outcome Data", "sec:data-outcomes", level=2, text_paragraphs=8),
            SectionSpec("Weather Data Construction", "sec:data-weather", level=2, text_paragraphs=8),
            SectionSpec("Climate Projections", "sec:data-climate", level=2, text_paragraphs=7),
        ],
    )

    identification = SectionSpec(
        "Empirical Strategy", "sec:empirical-environ", text_paragraphs=12,
        equations=[eq_nonlinear_dose, eq_panel_fe],
        tables=[panel_fe],
        subsections=[
            SectionSpec("Identifying Variation", "sec:id-variation", level=2, text_paragraphs=8),
            SectionSpec("Nonlinear Temperature Specification", "sec:nonlinear-spec", level=2, text_paragraphs=8),
            SectionSpec("Robustness to Trends", "sec:robust-trends", level=2, text_paragraphs=7),
        ],
    )

    main_results = SectionSpec(
        "Main Results", "sec:results-environ", text_paragraphs=12,
        tables=[temp_bins_mortality, temp_bins_agriculture, temp_bins_energy, nonlinear_dose],
        subsections=[
            SectionSpec("Mortality Effects", "sec:mortality-results", level=2, text_paragraphs=8),
            SectionSpec("Agricultural Effects", "sec:agriculture-results", level=2, text_paragraphs=8),
            SectionSpec("Energy Demand Effects", "sec:energy-results", level=2, text_paragraphs=7),
        ],
    )

    robustness = SectionSpec(
        "Robustness", "sec:robust-environ", text_paragraphs=10,
        tables=[linear_temp, panel_trends],
        subsections=[
            SectionSpec("Functional Form Sensitivity", "sec:robust-form", level=2, text_paragraphs=7),
            SectionSpec("Alternative Fixed Effect Structures", "sec:robust-fe", level=2, text_paragraphs=7),
        ],
    )

    adaptation = SectionSpec(
        "Adaptation", "sec:adaptation", text_paragraphs=12,
        tables=[adaptation_time, adaptation_income],
        equations=[eq_adaptation_model],
        subsections=[
            SectionSpec("Temporal Adaptation", "sec:adapt-time", level=2, text_paragraphs=8),
            SectionSpec("Income-Mediated Adaptation", "sec:adapt-income", level=2, text_paragraphs=8),
        ],
    )

    damages = SectionSpec(
        "Projected Damages", "sec:damages", text_paragraphs=12,
        tables=[sector_heterogeneity, projected_damages_2050],
        equations=[eq_projected_damages, eq_wtp, eq_social_cost],
        subsections=[
            SectionSpec("Sectoral Damage Estimates", "sec:sector-damages", level=2, text_paragraphs=8),
            SectionSpec("Aggregate Welfare Costs", "sec:welfare-costs", level=2, text_paragraphs=8),
            SectionSpec("Monte Carlo Projections", "sec:monte-carlo", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-environ", text_paragraphs=12)

    appendix_a = SectionSpec(
        "Appendix A: Identification and Adaptation Theory", "sec:appendix-a-environ", text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Weather Data and Validation", "sec:appendix-b-environ", text_paragraphs=5,
        tables=[appendix_weather],
    )

    return PaperSpec(
        paper_id="13",
        field_slug="environmental",
        title="Climate, Extremes, and Economic Activity: Evidence from Nonlinear Temperature Effects Across U.S. Counties",
        authors="Olivier Deschenes, Michael Greenstone, Tatyana Marchetti",
        journal_style="nber_wp",
        abstract=(
            "We estimate the effects of temperature extremes on mortality, agricultural yields, and "
            "energy demand using panel data for 3,066 U.S. counties from 1968 to 2002. Exploiting "
            "year-to-year weather variation within counties, we document sharply nonlinear dose-response "
            "relationships: days above 90\\textdegree F increase mortality by 1.084 deaths per 100,000 "
            "and reduce corn yields by 1.7 percent, while days in the 50--70\\textdegree F range are "
            "beneficial for agriculture but neutral for mortality. Linear temperature specifications "
            "understate mortality effects by a factor of 2.3. We find evidence of partial adaptation "
            "over time and across income groups: damage sensitivity has declined by approximately "
            "38\\% over the sample period, with richer counties showing greater adaptation in all "
            "sectors. Projecting these estimates under IPCC climate scenarios, a 2.8\\textdegree C "
            "warming by 2050 implies 2.5 additional deaths per 100,000 annually and 14.8\\% "
            "agricultural yield losses, with substantial Monte Carlo uncertainty."
        ),
        sections=[intro, data_section, identification, main_results, robustness,
                  adaptation, damages, conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{deschenes2007} Deschenes, O. and Greenstone, M. (2007). The Economic Impacts of Climate Change: Evidence from Agricultural Output and Random Fluctuations in Weather. \textit{American Economic Review}, 97(1), 354--385.",
            r"\bibitem{deschenes2011} Deschenes, O. and Greenstone, M. (2011). Climate Change, Mortality, and Adaptation: Evidence from Annual Fluctuations in Weather in the US. \textit{American Economic Journal: Applied Economics}, 3(4), 152--185.",
            r"\bibitem{schlenker2009} Schlenker, W. and Roberts, M. J. (2009). Nonlinear Temperature Effects Indicate Severe Damages to U.S. Crop Yields Under Climate Change. \textit{Proceedings of the National Academy of Sciences}, 106(37), 15594--15598.",
            r"\bibitem{hsiang2017} Hsiang, S., Burke, M., and Miguel, E. (2013). Quantifying the Influence of Climate on Human Conflict. \textit{Science}, 341(6151).",
            r"\bibitem{burke2015} Burke, M., Hsiang, S. M., and Miguel, E. (2015). Global Non-Linear Effect of Temperature on Economic Production. \textit{Nature}, 527(7577), 235--239.",
            r"\bibitem{nordhaus1992} Nordhaus, W. D. (1992). An Optimal Transition Path for Controlling Greenhouse Gases. \textit{Science}, 258(5086), 1315--1319.",
            r"\bibitem{interagency2010} Interagency Working Group on Social Cost of Carbon (2010). Technical Support Document: Social Cost of Carbon for Regulatory Impact Analysis. \textit{US Government}.",
            r"\bibitem{barreca2016} Barreca, A., Clay, K., Deschenes, O., Greenstone, M., and Shapiro, J. S. (2016). Adapting to Climate Change: The Remarkable Decline in the US Temperature-Mortality Relationship Over the 20th Century. \textit{Journal of Political Economy}, 124(1), 105--159.",
        ],
        target_pages=60,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "Within-county year-to-year weather variation, controlling for county FE and state-by-year FE"},
            {"question": "What is the mortality effect of days above 90F in the preferred specification?", "answer": "1.084 deaths per 100,000 in column 4 with county FE and state-year FE and linear trends"},
            {"question": "By what factor does the linear temperature specification understate mortality effects?", "answer": "By a factor of 2.3 (0.481 linear vs 1.084 bins estimate)"},
            {"question": "What is the projected mortality increase under the IPCC A1B scenario by 2050?", "answer": "2.481 additional deaths per 100,000 per year (central estimate)"},
            {"question": "By approximately what percentage has temperature damage sensitivity declined over the sample period?", "answer": "Approximately 38 percent (hot-day coefficient falls from 1.614 in 1968-1980 to 0.984 in 1994-2002)"},
        ],
    )


PAPER_BUILDERS["13"] = _paper_13_environmental
