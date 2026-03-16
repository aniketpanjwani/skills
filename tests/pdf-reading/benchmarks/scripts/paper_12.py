#!/usr/bin/env python3
"""Paper builder for paper 12 (Urban)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_12_urban() -> PaperSpec:
    # --- Tables ---
    city_summary = render_regression_table({
        "table_id": "city-summary",
        "caption": "Summary Statistics: Metropolitan Areas 1980--2010",
        "label": "tab:city-summary",
        "model_labels": ["Mean", "SD", "p10", "p90"],
        "panels": [{
            "dep_var": "Panel A: Housing Market Outcomes",
            "variables": [
                {"label": "Log Median House Price", "coefficients": ["11.84", "0.62", "11.08", "12.61"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Median Rent", "coefficients": ["6.71", "0.41", "6.21", "7.24"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Housing Units per Capita", "coefficients": ["0.421", "0.074", "0.334", "0.518"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Annual Permit Rate (per 1,000 residents)", "coefficients": ["6.84", "5.21", "1.42", "14.18"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Price-to-Rent Ratio", "coefficients": ["18.4", "5.2", "12.1", "26.8"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: City Characteristics",
            "variables": [
                {"label": "Log Population", "coefficients": ["12.91", "1.18", "11.48", "14.52"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Population Growth 1980-2010 (\\%)", "coefficients": ["28.4", "31.8", "-4.1", "74.8"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log Median Household Income", "coefficients": ["10.71", "0.31", "10.32", "11.12"],
                 "std_errors": ["", "", "", ""]},
                {"label": "College Share (\\%)", "coefficients": ["28.4", "9.8", "17.1", "41.8"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Undevelopable Land Share (\\%)", "coefficients": ["19.8", "14.2", "4.1", "42.8"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Wharton Regulatory Index", "coefficients": ["0.04", "1.12", "-1.18", "1.42"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Metropolitan Areas", "values": ["318", "318", "318", "318"]},
            {"label": "Census Waves", "values": ["4", "4", "4", "4"]},
        ],
        "notes": "MSAs with population $>$ 50,000 in 1980. Housing prices deflated to 2010 dollars using CPI. Undevelopable land share from Saiz (2010).",
        "qa": [
            {"question": "What is the mean log median house price?", "answer": "11.84"},
            {"question": "What is the mean undevelopable land share?", "answer": "19.8 percent"},
            {"question": "How many MSAs are in the sample?", "answer": "318"},
            {"question": "What is the mean Wharton Regulatory Index?", "answer": "0.04"},
        ],
    })

    housing_price_ols = render_regression_table({
        "table_id": "housing-price-ols",
        "caption": "OLS Estimates: Determinants of House Price Growth",
        "label": "tab:housing-price-ols",
        "model_labels": ["(1)", "(2)", "(3)", "(4)", "(5)"],
        "panels": [{
            "dep_var": "Dep. var.: $\\Delta$ Log Median House Price (decade)",
            "variables": [
                {"label": "$\\Delta$ Log Employment", "coefficients": ["0.584***", "0.512***", "0.498***", "0.474***", "0.461***"],
                 "std_errors": ["(0.048)", "(0.051)", "(0.053)", "(0.058)", "(0.061)"]},
                {"label": "$\\Delta$ Log Population", "coefficients": ["0.312***", "0.284***", "0.271***", "0.248***", "0.231***"],
                 "std_errors": ["(0.041)", "(0.044)", "(0.046)", "(0.051)", "(0.054)"]},
                {"label": "$\\Delta$ Log Income", "coefficients": ["0.241***", "0.218***", "0.204***", "0.191***", "0.178***"],
                 "std_errors": ["(0.038)", "(0.041)", "(0.043)", "(0.047)", "(0.050)"]},
                {"label": "College Share Change", "coefficients": ["--", "0.412***", "0.398***", "0.371***", "0.348***"],
                 "std_errors": ["", "(0.062)", "(0.064)", "(0.068)", "(0.071)"]},
                {"label": "Amenity Index", "coefficients": ["--", "--", "0.184**", "0.162**", "0.141**"],
                 "std_errors": ["", "", "(0.074)", "(0.078)", "(0.081)"]},
                {"label": "Supply Elasticity", "coefficients": ["--", "--", "--", "-0.218***", "-0.204***"],
                 "std_errors": ["", "", "", "(0.044)", "(0.048)"]},
                {"label": "Wharton Index", "coefficients": ["--", "--", "--", "--", "0.094**"],
                 "std_errors": ["", "", "", "", "(0.038)"]},
            ],
        }],
        "controls": [
            {"label": "Census Division FE", "values": ["No", "Yes", "Yes", "Yes", "Yes"]},
            {"label": "Decade FE", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
            {"label": "1980 baseline controls", "values": ["No", "No", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["954", "954", "954", "954", "954"]},
            {"label": "R-squared", "values": ["0.421", "0.498", "0.531", "0.568", "0.582"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05, * p$<$0.1. Robust standard errors clustered at MSA level. Sample: 318 MSAs $\\times$ 3 decades (1980--1990, 1990--2000, 2000--2010).",
        "qa": [
            {"question": "What is the OLS coefficient on log employment growth in column 1?", "answer": "0.584"},
            {"question": "What is the R-squared in the most saturated specification (column 5)?", "answer": "0.582"},
            {"question": "What is the coefficient on supply elasticity in column 4?", "answer": "-0.218"},
            {"question": "What is the coefficient on the Wharton regulatory index in column 5?", "answer": "0.094"},
        ],
    })

    housing_supply_iv = render_regression_table({
        "table_id": "housing-supply-iv",
        "caption": "IV Estimates: Housing Supply Elasticity (Saiz Land Instrument)",
        "label": "tab:housing-supply-iv",
        "model_labels": ["OLS", "IV", "IV", "IV", "First Stage"],
        "panels": [{
            "dep_var": "Second Stage: Dep. var. $\\Delta$ Log Housing Units",
            "variables": [
                {"label": "$\\Delta$ Log House Price", "coefficients": ["0.412***", "1.841***", "1.712***", "1.684***", "--"],
                 "std_errors": ["(0.041)", "(0.284)", "(0.264)", "(0.271)", ""]},
                {"label": "$\\Delta$ Log Income", "coefficients": ["0.184***", "0.142**", "0.138**", "0.131**", "--"],
                 "std_errors": ["(0.038)", "(0.058)", "(0.061)", "(0.064)", ""]},
                {"label": "$\\Delta$ Log Employment", "coefficients": ["0.218***", "0.171***", "0.164***", "0.158***", "--"],
                 "std_errors": ["(0.032)", "(0.048)", "(0.051)", "(0.054)", ""]},
            ],
        }, {
            "dep_var": "First Stage: Dep. var. $\\Delta$ Log House Price",
            "variables": [
                {"label": "Undevelopable Land Share $\\times$ Pop. Growth", "coefficients": ["--", "--", "--", "--", "0.814***"],
                 "std_errors": ["", "", "", "", "(0.068)"]},
                {"label": "Slope Index $\\times$ Pop. Growth", "coefficients": ["--", "--", "--", "--", "0.641***"],
                 "std_errors": ["", "", "", "", "(0.074)"]},
            ],
        }],
        "controls": [
            {"label": "Census Division FE", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
            {"label": "Decade FE", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
            {"label": "Demographic controls", "values": ["No", "No", "Yes", "Yes", "Yes"]},
            {"label": "Regulation controls", "values": ["No", "No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["954", "954", "954", "954", "954"]},
            {"label": "Kleibergen-Paap F-stat", "values": ["--", "84.2", "81.4", "78.9", "--"]},
            {"label": "R-squared (first stage)", "values": ["--", "--", "--", "--", "0.618"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05. Instruments: undevelopable land share and terrain slope index (Saiz 2010) interacted with population growth. IV standard errors robust, clustered by MSA.",
        "qa": [
            {"question": "What is the IV estimate of the supply elasticity in column 2?", "answer": "1.841"},
            {"question": "What is the Kleibergen-Paap F-statistic in column 2?", "answer": "84.2"},
            {"question": "What is the OLS estimate of the supply elasticity?", "answer": "0.412"},
            {"question": "What is the first-stage coefficient on undevelopable land share interacted with population growth?", "answer": "0.814"},
        ],
    })

    elasticity_estimates = render_regression_table({
        "table_id": "elasticity-estimates",
        "caption": "Housing Supply Elasticity Estimates by City",
        "label": "tab:elasticity-estimates",
        "model_labels": ["Saiz IV", "Permit-Based", "Hedonic", "Combined"],
        "panels": [{
            "dep_var": "Panel A: Constrained Cities (Elasticity $<$ 1.5)",
            "variables": [
                {"label": "New York--Northern NJ", "coefficients": ["0.76", "0.82", "0.71", "0.76"],
                 "std_errors": ["(0.08)", "(0.11)", "(0.09)", "(0.06)"]},
                {"label": "San Francisco--Oakland", "coefficients": ["0.64", "0.71", "0.58", "0.64"],
                 "std_errors": ["(0.09)", "(0.12)", "(0.10)", "(0.07)"]},
                {"label": "Los Angeles--Long Beach", "coefficients": ["0.84", "0.91", "0.78", "0.84"],
                 "std_errors": ["(0.08)", "(0.11)", "(0.09)", "(0.06)"]},
                {"label": "Boston", "coefficients": ["0.91", "0.98", "0.85", "0.91"],
                 "std_errors": ["(0.09)", "(0.12)", "(0.10)", "(0.07)"]},
            ],
        }, {
            "dep_var": "Panel B: Elastic Cities (Elasticity $>$ 3.0)",
            "variables": [
                {"label": "Houston", "coefficients": ["5.41", "5.18", "5.62", "5.40"],
                 "std_errors": ["(0.48)", "(0.52)", "(0.51)", "(0.36)"]},
                {"label": "Phoenix", "coefficients": ["4.84", "4.61", "5.02", "4.82"],
                 "std_errors": ["(0.44)", "(0.48)", "(0.47)", "(0.33)"]},
                {"label": "Atlanta", "coefficients": ["4.12", "3.98", "4.28", "4.13"],
                 "std_errors": ["(0.38)", "(0.42)", "(0.41)", "(0.29)"]},
                {"label": "Dallas--Fort Worth", "coefficients": ["4.51", "4.34", "4.68", "4.51"],
                 "std_errors": ["(0.41)", "(0.45)", "(0.44)", "(0.31)"]},
            ],
        }],
        "summary": [
            {"label": "Mean elasticity (full sample)", "values": ["2.48", "2.41", "2.58", "2.49"]},
            {"label": "Std. dev.", "values": ["1.84", "1.79", "1.91", "1.82"]},
        ],
        "notes": "Standard errors in parentheses. Saiz IV: instrument based on undevelopable terrain (Saiz 2010). Permit-based: long-run price elasticity from permit autoregressions. Combined: precision-weighted average.",
        "qa": [
            {"question": "What is the Saiz IV elasticity for San Francisco?", "answer": "0.64"},
            {"question": "What is the Saiz IV elasticity for Houston?", "answer": "5.41"},
            {"question": "What is the mean supply elasticity across all methods in the combined column?", "answer": "2.49"},
        ],
    })

    amenity_capitalization = render_regression_table({
        "table_id": "amenity-capitalization",
        "caption": "Amenity Capitalization into House Prices and Wages",
        "label": "tab:amenity-capitalization",
        "model_labels": ["(1) Prices", "(2) Prices", "(3) Wages", "(4) Wages"],
        "panels": [{
            "dep_var": "Dep. var.: Log Median House Price / Log Median Wage",
            "variables": [
                {"label": "January Temperature (10-deg F)", "coefficients": ["0.184***", "0.172***", "-0.041**", "-0.038**"],
                 "std_errors": ["(0.028)", "(0.031)", "(0.018)", "(0.019)"]},
                {"label": "Coast Dummy", "coefficients": ["0.214***", "0.198***", "0.024", "0.021"],
                 "std_errors": ["(0.041)", "(0.044)", "(0.024)", "(0.026)"]},
                {"label": "Log Sunshine Hours", "coefficients": ["0.148***", "0.138***", "-0.018", "-0.016"],
                 "std_errors": ["(0.038)", "(0.041)", "(0.022)", "(0.024)"]},
                {"label": "Log Crime Rate", "coefficients": ["-0.124***", "-0.114***", "0.028**", "0.024*"],
                 "std_errors": ["(0.024)", "(0.026)", "(0.014)", "(0.015)"]},
                {"label": "School Quality Index", "coefficients": ["0.094***", "0.084***", "-0.008", "-0.007"],
                 "std_errors": ["(0.019)", "(0.021)", "(0.011)", "(0.012)"]},
            ],
        }],
        "controls": [
            {"label": "Census Division FE", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "MSA size controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["318", "318", "318", "318"]},
            {"label": "R-squared", "values": ["0.541", "0.584", "0.314", "0.348"]},
        ],
        "notes": "*** p$<$0.01, ** p$<$0.05, * p$<$0.1. Cross-section, 2000 Census. Amenity values from Albouy (2016) index. Rosen-Roback theory predicts positive price and negative wage amenity gradients.",
        "qa": [
            {"question": "What is the price effect of a 10-degree F increase in January temperature in column 1?", "answer": "0.184"},
            {"question": "What is the wage effect of the coastal dummy?", "answer": "0.024 (not statistically significant)"},
            {"question": "What is the price effect of school quality in column 2?", "answer": "0.084"},
        ],
    })

    sorting_income = render_regression_table({
        "table_id": "sorting-income",
        "caption": "Income Sorting and Skill Sorting Across Cities",
        "label": "tab:sorting-income",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: $\\Delta$ Log Median Income or $\\Delta$ College Share",
            "variables": [
                {"label": "Supply Elasticity (Saiz)", "coefficients": ["-0.048***", "-0.041***", "-0.081***", "-0.074***"],
                 "std_errors": ["(0.012)", "(0.013)", "(0.018)", "(0.019)"]},
                {"label": "Amenity Index", "coefficients": ["0.124***", "0.114***", "0.218***", "0.204***"],
                 "std_errors": ["(0.028)", "(0.031)", "(0.041)", "(0.044)"]},
                {"label": "Initial College Share", "coefficients": ["0.312***", "0.284***", "--", "--"],
                 "std_errors": ["(0.041)", "(0.044)", "", ""]},
                {"label": "Productivity Growth", "coefficients": ["0.248***", "0.228***", "0.412***", "0.384***"],
                 "std_errors": ["(0.038)", "(0.041)", "(0.058)", "(0.062)"]},
            ],
        }],
        "controls": [
            {"label": "Dep. var.", "values": ["$\\Delta$ Income", "$\\Delta$ Income", "$\\Delta$ College", "$\\Delta$ College"]},
            {"label": "Census Division FE", "values": ["No", "Yes", "No", "Yes"]},
            {"label": "Decade FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["954", "954", "954", "954"]},
            {"label": "R-squared", "values": ["0.481", "0.524", "0.514", "0.558"]},
        ],
        "notes": "*** p$<$0.01. Inelastic supply cities attract higher-income and higher-skill workers as housing constraints intensify income sorting. Supply elasticity coded so higher = more elastic.",
        "qa": [
            {"question": "What is the effect of supply elasticity on income growth in column 1?", "answer": "-0.048"},
            {"question": "What is the effect of the amenity index on college share change in column 3?", "answer": "0.218"},
        ],
    })

    spatial_equilibrium = render_regression_table({
        "table_id": "spatial-equilibrium",
        "caption": "Tests of Spatial Equilibrium: Utility Equalization Across Cities",
        "label": "tab:spatial-equilibrium",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Net Migration Rate (\\% per decade)",
            "variables": [
                {"label": "Real Wage Advantage (\\%)", "coefficients": ["0.618***", "0.584***", "0.541***", "0.512***"],
                 "std_errors": ["(0.071)", "(0.074)", "(0.078)", "(0.081)"]},
                {"label": "House Price Disadvantage (\\%)", "coefficients": ["-0.481***", "-0.452***", "-0.418***", "-0.394***"],
                 "std_errors": ["(0.058)", "(0.061)", "(0.064)", "(0.068)"]},
                {"label": "Amenity Differential", "coefficients": ["0.214***", "0.198***", "0.184***", "0.171***"],
                 "std_errors": ["(0.038)", "(0.041)", "(0.043)", "(0.046)"]},
                {"label": "Unemployment Differential", "coefficients": ["-0.284***", "-0.261***", "-0.241***", "-0.224***"],
                 "std_errors": ["(0.044)", "(0.047)", "(0.050)", "(0.053)"]},
                {"label": "Utility Equalization Test ($\\chi^2$)", "coefficients": ["2.84", "2.41", "2.18", "1.98"],
                 "std_errors": ["[0.241]", "[0.299]", "[0.336]", "[0.372]"]},
            ],
        }],
        "controls": [
            {"label": "Census Division FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Decade FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Skill group FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Race controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["954", "954", "954", "954"]},
            {"label": "R-squared", "values": ["0.468", "0.511", "0.548", "0.572"]},
        ],
        "notes": "*** p$<$0.01. Utility equalization test: $H_0$ that coefficients on wage and price differentials sum to zero (spatial indifference). $p$-values in brackets.",
        "qa": [
            {"question": "What is the coefficient on real wage advantage in column 1?", "answer": "0.618"},
            {"question": "What is the coefficient on house price disadvantage in column 1?", "answer": "-0.481"},
            {"question": "What is the p-value on the utility equalization test in column 4?", "answer": "0.372"},
        ],
    })

    migration_flows = render_regression_table({
        "table_id": "migration-flows",
        "caption": "Migration Gravity Model: Bilateral Flows Between MSAs",
        "label": "tab:migration-flows",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Log Bilateral Migration Flow",
            "variables": [
                {"label": "Log Distance", "coefficients": ["-1.284***", "-1.218***", "-1.184***", "-1.148***"],
                 "std_errors": ["(0.048)", "(0.051)", "(0.054)", "(0.058)"]},
                {"label": "Log Origin Population", "coefficients": ["0.841***", "0.812***", "0.784***", "0.754***"],
                 "std_errors": ["(0.031)", "(0.033)", "(0.035)", "(0.038)"]},
                {"label": "Log Destination Population", "coefficients": ["0.914***", "0.884***", "0.852***", "0.821***"],
                 "std_errors": ["(0.033)", "(0.036)", "(0.038)", "(0.041)"]},
                {"label": "Destination Wage Premium", "coefficients": ["0.481***", "0.448***", "0.412***", "0.384***"],
                 "std_errors": ["(0.064)", "(0.068)", "(0.071)", "(0.074)"]},
                {"label": "Destination Housing Cost", "coefficients": ["-0.314***", "-0.284***", "-0.261***", "-0.241***"],
                 "std_errors": ["(0.048)", "(0.051)", "(0.054)", "(0.058)"]},
                {"label": "Common State Dummy", "coefficients": ["0.684***", "0.648***", "0.614***", "0.584***"],
                 "std_errors": ["(0.081)", "(0.084)", "(0.088)", "(0.091)"]},
            ],
        }],
        "controls": [
            {"label": "Origin FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Destination FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Decade FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Skill group", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations (city pairs)", "values": ["30,258", "30,258", "30,258", "30,258"]},
            {"label": "R-squared", "values": ["0.641", "0.712", "0.748", "0.784"]},
        ],
        "notes": "*** p$<$0.01. Gravity model estimated by PPML. Bilateral flows from Census migration matrices (1990, 2000, 2010). Distance: great-circle between MSA centroids.",
        "qa": [
            {"question": "What is the distance elasticity in column 1?", "answer": "-1.284"},
            {"question": "What is the wage premium coefficient in column 4?", "answer": "0.384"},
            {"question": "What is the common-state dummy coefficient in column 1?", "answer": "0.684"},
        ],
    })

    land_regulation = render_regression_table({
        "table_id": "land-regulation",
        "caption": "Land Use Regulation and Housing Supply",
        "label": "tab:land-regulation",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Log Annual Housing Permits per Capita",
            "variables": [
                {"label": "Wharton Regulatory Index", "coefficients": ["-0.284***", "-0.261***", "-0.241***", "-0.218***"],
                 "std_errors": ["(0.038)", "(0.041)", "(0.044)", "(0.048)"]},
                {"label": "Minimum Lot Size (acres)", "coefficients": ["--", "-0.148***", "-0.138***", "-0.124***"],
                 "std_errors": ["", "(0.028)", "(0.030)", "(0.033)"]},
                {"label": "Zoning Strictness Index", "coefficients": ["--", "--", "-0.184***", "-0.168***"],
                 "std_errors": ["", "", "(0.034)", "(0.037)"]},
                {"label": "Log House Price (lagged)", "coefficients": ["0.218***", "0.198***", "0.184***", "0.168***"],
                 "std_errors": ["(0.031)", "(0.033)", "(0.035)", "(0.038)"]},
                {"label": "Undevelopable Land Share", "coefficients": ["-0.614***", "-0.581***", "-0.554***", "-0.524***"],
                 "std_errors": ["(0.074)", "(0.078)", "(0.081)", "(0.085)"]},
            ],
        }],
        "controls": [
            {"label": "State FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Decade FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "MSA size controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Income controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["954", "954", "954", "954"]},
            {"label": "R-squared", "values": ["0.514", "0.548", "0.574", "0.598"]},
        ],
        "notes": "*** p$<$0.01. Wharton Regulatory Index from Gyourko, Saiz, and Summers (2008): higher values indicate more restrictive regulation. Regulation reduces permit issuance conditional on physical constraints.",
        "qa": [
            {"question": "What is the effect of the Wharton index on permits in column 1?", "answer": "-0.284"},
            {"question": "What is the effect of undevelopable land share on permits in column 4?", "answer": "-0.524"},
            {"question": "What is the R-squared in column 4?", "answer": "0.598"},
        ],
    })

    construction_costs = render_regression_table({
        "table_id": "construction-costs",
        "caption": "Construction Costs, Land Costs, and the Marginal Cost of Housing",
        "label": "tab:construction-costs",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Panel A: Dep. var. Log Land Value per Sq. Ft.",
            "variables": [
                {"label": "Undevelopable Land Share", "coefficients": ["1.841***", "1.712***", "1.584***", "1.478***"],
                 "std_errors": ["(0.184)", "(0.192)", "(0.201)", "(0.214)"]},
                {"label": "Wharton Regulatory Index", "coefficients": ["0.512***", "0.484***", "0.454***", "0.421***"],
                 "std_errors": ["(0.068)", "(0.071)", "(0.074)", "(0.078)"]},
                {"label": "Log City Income", "coefficients": ["0.641***", "0.614***", "0.581***", "0.548***"],
                 "std_errors": ["(0.071)", "(0.074)", "(0.078)", "(0.081)"]},
            ],
        }, {
            "dep_var": "Panel B: Dep. var. Log Construction Cost per Sq. Ft.",
            "variables": [
                {"label": "Log Material Prices", "coefficients": ["0.481***", "0.452***", "0.424***", "0.398***"],
                 "std_errors": ["(0.058)", "(0.061)", "(0.064)", "(0.068)"]},
                {"label": "Log Wage (construction)", "coefficients": ["0.318***", "0.298***", "0.281***", "0.264***"],
                 "std_errors": ["(0.041)", "(0.044)", "(0.046)", "(0.049)"]},
                {"label": "Building Height Regulation", "coefficients": ["0.214***", "0.198***", "0.184***", "0.171***"],
                 "std_errors": ["(0.031)", "(0.033)", "(0.035)", "(0.037)"]},
            ],
        }],
        "controls": [
            {"label": "State FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "MSA controls", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Interaction terms", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations (Panel A)", "values": ["1,272", "1,272", "1,272", "1,272"]},
            {"label": "Observations (Panel B)", "values": ["1,272", "1,272", "1,272", "1,272"]},
        ],
        "notes": "*** p$<$0.01. Land and construction cost data from Lincoln Institute of Land Policy. Marginal cost of housing = construction cost + opportunity cost of land.",
        "qa": [
            {"question": "What is the effect of undevelopable land share on land values in column 1?", "answer": "1.841"},
            {"question": "What is the elasticity of construction costs with respect to material prices in column 1?", "answer": "0.481"},
        ],
    })

    appendix_geo = render_regression_table({
        "table_id": "appendix-geo",
        "caption": "Appendix: Geographic Land Availability and Instrument Validity",
        "label": "tab:appendix-geo",
        "model_labels": ["Mean", "SD", "Min", "Max"],
        "panels": [{
            "dep_var": "Panel A: Geographic Constraint Measures",
            "variables": [
                {"label": "Undevelopable Land Share (\\%)", "coefficients": ["19.8", "14.2", "0.0", "71.4"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Terrain Slope Index", "coefficients": ["2.84", "2.41", "0.12", "11.84"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Wetlands Share (\\%)", "coefficients": ["4.21", "6.84", "0.0", "38.4"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Floodplain Share (\\%)", "coefficients": ["8.14", "9.21", "0.0", "41.8"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Instrument Validity Tests",
            "variables": [
                {"label": "Correlation with 1900 Population Density", "coefficients": ["0.081", "--", "--", "--"],
                 "std_errors": ["[0.142]", "", "", ""]},
                {"label": "Correlation with 1900 Income", "coefficients": ["0.064", "--", "--", "--"],
                 "std_errors": ["[0.248]", "", "", ""]},
                {"label": "Correlation with 1900 Manufacturing Share", "coefficients": ["0.048", "--", "--", "--"],
                 "std_errors": ["[0.384]", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "MSAs", "values": ["318", "318", "318", "318"]},
        ],
        "notes": "Geographic constraint data from Saiz (2010) based on NLCD land cover and USGS slope data. Pre-determined geographic variables uncorrelated with historical economic conditions, supporting instrument exogeneity.",
        "qa": [
            {"question": "What is the mean undevelopable land share?", "answer": "19.8 percent"},
            {"question": "What is the correlation between undevelopable land share and 1900 population density?", "answer": "0.081 (p-value 0.142, not statistically significant)"},
            {"question": "What is the mean terrain slope index?", "answer": "2.84"},
        ],
    })

    # --- Equations ---
    eq_spatial_equil = EquationSpec(
        "spatial-equilibrium",
        r"V(w_j, r_j, A_j) = \bar{V} \quad \forall j \in \mathcal{J}",
        "eq:spatial-equil",
        "Spatial equilibrium: utility $V$ is equalized across all cities $j$ via adjustment of wages $w_j$, rents $r_j$, and amenities $A_j$.",
        [{"question": "What condition characterizes spatial equilibrium?", "answer": "Utility V is equalized across all cities via wages, rents, and amenities"}],
    )

    eq_housing_supply = EquationSpec(
        "housing-supply",
        r"H_j = S(r_j;\, \eta_j), \quad \frac{\partial \log H_j}{\partial \log r_j} = \varepsilon_j^S",
        "eq:housing-supply",
        "Housing supply in city $j$ as a function of rents; $\\varepsilon_j^S$ is the supply elasticity, which varies with physical geography.",
    )

    eq_hedonic_price = EquationSpec(
        "hedonic-price",
        r"\log P_{ij} = \hat{\alpha}_j + \tilde{\beta} X_{ij} + \varepsilon_{ij}, \quad \hat{\alpha}_j \xrightarrow{p} \alpha_j \text{ as } N_j \to \infty",
        "eq:hedonic-price",
        "Hedonic house price equation: log price of house $i$ in city $j$ as a function of structural characteristics $X_{ij}$ and city fixed effect $\\alpha_j$.",
    )

    eq_rosen_roback = EquationSpec(
        "rosen-roback",
        r"\frac{\partial \log r_j}{\partial A_j} = \frac{U_A}{U_r \cdot H}, \quad \frac{\partial \log w_j}{\partial A_j} = -\frac{U_A}{U_w}, \quad \hat{A}_j = \underset{A}{\operatorname{arg\,max}}\; \tilde{V}(w_j, r_j, A)",
        "eq:rosen-roback",
        "Rosen-Roback amenity gradients: amenities are capitalized into higher rents and lower wages in equilibrium.",
    )

    eq_bid_rent = EquationSpec(
        "bid-rent",
        r"r(d) = r_0 - \tau d, \quad r_0 = \hat{w} - c(\tilde{H}^*), \quad r'(d) = -\tau < 0, \quad \hat{r}(d) \overset{p}{\to} r(d)",
        "eq:bid-rent",
        "Monocentric bid-rent gradient: rents decline with distance $d$ from the CBD at rate $\\tau$ equal to commuting cost.",
    )

    eq_supply_elasticity = EquationSpec(
        "supply-elasticity",
        r"\varepsilon_j^S = \varepsilon^S_0 - \kappa_1 \\cdot \\text{Undev}_j - \\kappa_2 \\cdot \\text{Reg}_j",
        "eq:supply-elasticity",
        "Supply elasticity as a decreasing function of undevelopable land share $\\text{Undev}_j$ and regulatory stringency $\\text{Reg}_j$.",
    )

    eq_amenity_valuation = EquationSpec(
        "amenity-valuation",
        r"\\widetilde{A}_j = \\frac{\\partial \\log r_j / \\partial A_j}{\\partial \\log r_j / \\partial A_j - \\partial \\log w_j / \\partial A_j} \\cdot \\Delta \\log r_j + \\frac{\\partial \\log w_j / \\partial A_j}{\\partial \\log w_j / \\partial A_j - \\partial \\log r_j / \\partial A_j} \\cdot \\Delta \\log w_j",
        "eq:amenity-valuation",
        "Quality-of-life index: value of amenity $A_j$ recovered from observed rent and wage differentials using Rosen-Roback theory.",
    )

    eq_migration_gravity = EquationSpec(
        "migration-gravity",
        r"M_{ij} = \\exp\\!\\left(\\alpha_i + \\gamma_j + \\delta_1 \\log d_{ij} + \\delta_2 (\\log w_j - \\log r_j) + \\varepsilon_{ij}\\right)",
        "eq:migration-gravity",
        "Gravity model of migration: bilateral flow $M_{ij}$ depends on distance, origin FE $\\alpha_i$, destination FE $\\gamma_j$, and destination real wage $\\log w_j - \\log r_j$.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[Existence of Spatial Equilibrium]
Under standard regularity conditions on preferences $U(c, H, A)$ and production, a spatial equilibrium exists. Specifically, suppose: (i) $U$ is continuous, strictly quasi-concave, and strictly increasing in $c$, $H$, and $A$; (ii) the housing supply $S(r; \eta)$ is continuous and increasing in $r$ for all $\eta$; (iii) there exist upper and lower bounds on feasible wages and rents. Then there exists at least one equilibrium allocation $(w_j^*, r_j^*, n_j^*)_{j \in \mathcal{J}}$ such that $V(w_j^*, r_j^*, A_j) = \bar{V}$ for all populated cities.
\end{proposition}

\begin{proof}
Map $T: \Delta \to \Delta$ on the simplex of city population shares. Brouwer's fixed-point theorem applies since $T$ is continuous and $\Delta$ is compact and convex. At fixed point $n^*$, labor market clearing pins wages via $w_j = w_j(n_j^*)$ and housing market clearing pins rents via $r_j = r_j(n_j^*, S_j)$. Utility equalization follows from the definition of $T$.
\end{proof}

\begin{proposition}[Uniqueness with Linear Supply]
If housing supply is log-linear, $\log H_j = \varepsilon_j^S \log r_j + \zeta_j$, and preferences are Cobb-Douglas, $U = c^\alpha H^\beta A^\gamma$ with $\alpha + \beta + \gamma = 1$, then the spatial equilibrium is unique.
\end{proposition}

\begin{proof}
Log-linearizing around the equilibrium, the system reduces to:
\begin{align}
d\log r_j &= \frac{1}{\varepsilon_j^S} d\log n_j + \frac{1}{\varepsilon_j^S} d\log A_j^{supply}, \\
d\log w_j &= \frac{\phi}{\varepsilon_j^L} d\log n_j, \\
dV &= \alpha\, d\log w_j - \beta\, d\log r_j + \gamma\, dA_j = 0,
\end{align}
where $\varepsilon_j^L$ is the labor demand elasticity. Substituting and solving for $dn_j$: the Jacobian of this system has a unique zero under the assumption $\varepsilon_j^S > 0$, $\varepsilon_j^L < 0$.
\end{proof}

\begin{proposition}[Comparative Statics: Supply Constraint Effect]
Let $\varepsilon_j^S \to 0$ (perfectly inelastic supply). Then a positive amenity shock $dA_j > 0$ is fully capitalized into rents: $d\log r_j \to \infty$, with no change in population $dn_j = 0$. When $\varepsilon_j^S \to \infty$ (perfectly elastic), the same shock induces unbounded population growth with no rent increase.
\end{proposition}

\begin{proof}
From the log-linearized equilibrium:
\begin{align}
d\log r_j &= \frac{dA_j + \phi\, dn_j}{\varepsilon_j^S}, \\
dn_j &= \frac{\varepsilon_j^S \cdot \gamma\, dA_j}{\beta + (\alpha\phi/\varepsilon_j^L - \beta/\varepsilon_j^S) \cdot 0}.
\end{align}
Taking $\varepsilon_j^S \to 0$ and $\varepsilon_j^S \to \infty$ establishes the stated limits.
\end{proof}

\begin{lemma}[Convergence of Hedonic Estimator]
Let $\hat{\alpha}_j$ denote the city fixed effect from the hedonic regression. Then:
\begin{align}
\sqrt{N_j}\left(\hat{\alpha}_j - \alpha_j\right) \xrightarrow{d} \mathcal{N}\!\left(0, \tilde{\sigma}_\varepsilon^2 / \hat{\sigma}_X^2 \right), \quad \underset{j \in \mathcal{J}}{\operatorname{arg\,max}}\; \hat{A}_j \overset{p}{\to} \underset{j \in \mathcal{J}}{\operatorname{arg\,max}}\; A_j.
\end{align}
\end{lemma}

\begin{remark}[Amenity Capitalization under Heterogeneous Preferences]
When households differ in taste parameter $\tilde{\theta}_i$, the hedonic price gradient satisfies the integral condition:
\begin{align}
\frac{\partial \log r_j}{\partial A_j} = \int_0^\infty \frac{U_A(\tilde{\theta})}{U_r(\tilde{\theta}) \cdot H(\tilde{\theta})} \, dG(\tilde{\theta}).
\end{align}
\end{remark}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-urban",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec(
        "Introduction", "sec:intro-urban", text_paragraphs=14,
        equations=[eq_spatial_equil],
    )

    data_section = SectionSpec(
        "Data and Institutional Background", "sec:data-urban", text_paragraphs=12,
        tables=[city_summary],
        subsections=[
            SectionSpec("Metropolitan Area Data Sources", "sec:data-msa", level=2, text_paragraphs=8),
            SectionSpec("Housing Market Institutions", "sec:data-housing-inst", level=2, text_paragraphs=7),
            SectionSpec("Geographic Constraint Measures", "sec:data-geo", level=2, text_paragraphs=6),
        ],
    )

    theory = SectionSpec(
        "Theoretical Framework", "sec:theory-urban", text_paragraphs=12,
        equations=[eq_housing_supply, eq_rosen_roback, eq_bid_rent],
        subsections=[
            SectionSpec("Spatial Equilibrium", "sec:theory-spatial", level=2, text_paragraphs=8),
            SectionSpec("Housing Supply and Land Constraints", "sec:theory-supply", level=2, text_paragraphs=8),
            SectionSpec("Amenity Capitalization", "sec:theory-amenity", level=2, text_paragraphs=7),
        ],
    )

    identification = SectionSpec(
        "Identification Strategy", "sec:identification-urban", text_paragraphs=12,
        equations=[eq_supply_elasticity],
        tables=[housing_supply_iv],
        subsections=[
            SectionSpec("The Saiz Land Instrument", "sec:saiz-iv", level=2, text_paragraphs=8),
            SectionSpec("First Stage and Instrument Validity", "sec:first-stage", level=2, text_paragraphs=7),
        ],
    )

    housing_market = SectionSpec(
        "Housing Markets and Supply Elasticities", "sec:housing-market", text_paragraphs=12,
        tables=[housing_price_ols, elasticity_estimates, construction_costs],
        equations=[eq_hedonic_price],
        subsections=[
            SectionSpec("House Price Determinants", "sec:house-price-det", level=2, text_paragraphs=8),
            SectionSpec("Supply Elasticity Estimates", "sec:supply-elast-est", level=2, text_paragraphs=8),
            SectionSpec("Construction and Land Costs", "sec:costs", level=2, text_paragraphs=7),
        ],
    )

    amenities_sorting = SectionSpec(
        "Amenities and Income Sorting", "sec:amenities-sorting", text_paragraphs=12,
        tables=[amenity_capitalization, sorting_income],
        equations=[eq_amenity_valuation],
        subsections=[
            SectionSpec("Amenity Values and Quality of Life", "sec:qol", level=2, text_paragraphs=8),
            SectionSpec("Skill Sorting Across Cities", "sec:sorting", level=2, text_paragraphs=8),
        ],
    )

    equilibrium_migration = SectionSpec(
        "Spatial Equilibrium and Migration", "sec:equil-migration", text_paragraphs=12,
        tables=[spatial_equilibrium, migration_flows],
        equations=[eq_migration_gravity],
        subsections=[
            SectionSpec("Testing Utility Equalization", "sec:utility-test", level=2, text_paragraphs=8),
            SectionSpec("Migration Responses to City Shocks", "sec:migration-resp", level=2, text_paragraphs=7),
        ],
    )

    regulation = SectionSpec(
        "Land Use Regulation", "sec:regulation", text_paragraphs=12,
        tables=[land_regulation],
        subsections=[
            SectionSpec("Effects of Regulation on Supply", "sec:reg-supply", level=2, text_paragraphs=8),
            SectionSpec("Political Economy of Zoning", "sec:reg-political", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-urban", text_paragraphs=12)

    appendix_a = SectionSpec(
        "Appendix A: Spatial Equilibrium Theory", "sec:appendix-a-urban", text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Geographic Instrument Validity", "sec:appendix-b-urban", text_paragraphs=5,
        tables=[appendix_geo],
    )

    return PaperSpec(
        paper_id="12",
        field_slug="urban",
        title="Housing Supply, Land Constraints, and Urban Spatial Equilibrium",
        authors="Nathan Glaeser, Isabella Saiz, Marco Gyourko",
        journal_style="jpe",
        abstract=(
            "We study how geographic and regulatory constraints on housing supply shape spatial equilibrium "
            "across 318 U.S. metropolitan areas from 1980 to 2010. Using undevelopable terrain as an "
            "instrument for housing supply elasticity following Saiz (2010), we estimate that a unit "
            "increase in supply elasticity reduces decadal house price growth by 4.8 percentage points "
            "and increases housing unit growth by 1.84 log points per unit of demand shock. Constrained "
            "cities attract higher-skill workers, capitalized amenities into higher rents, and show "
            "stronger income sorting. Land use regulation amplifies geographic constraints, reducing "
            "annual permit rates by 28 percent per standard deviation increase in the Wharton Regulatory "
            "Index. Spatial equilibrium conditions are formally derived and empirically supported by "
            "bilateral migration flows consistent with utility equalization across cities."
        ),
        sections=[intro, data_section, theory, identification, housing_market, amenities_sorting,
                  equilibrium_migration, regulation, conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{saiz2010} Saiz, A. (2010). The Geographic Determinants of Housing Supply. \textit{Quarterly Journal of Economics}, 125(3), 1253--1296.",
            r"\bibitem{glaeser2008} Glaeser, E. L. and Gyourko, J. (2008). Rethinking Federal Housing Policy. \textit{American Enterprise Institute Press}.",
            r"\bibitem{roback1982} Roback, J. (1982). Wages, Rents, and the Quality of Life. \textit{Journal of Political Economy}, 90(6), 1257--1278.",
            r"\bibitem{rosen1979} Rosen, S. (1979). Wage-Based Indexes of Urban Quality of Life. In P. Mieszkowski and M. Straszheim (eds.), \textit{Current Issues in Urban Economics}. Johns Hopkins.",
            r"\bibitem{gyourko2008} Gyourko, J., Saiz, A., and Summers, A. (2008). A New Measure of the Local Regulatory Environment for Housing Markets. \textit{Urban Studies}, 45(3), 693--729.",
            r"\bibitem{albouy2016} Albouy, D. (2016). What Are Cities Worth? Land Rents, Local Productivity, and the Total Value of Amenities. \textit{Review of Economics and Statistics}, 98(3), 477--487.",
            r"\bibitem{diamond2016} Diamond, R. (2016). The Determinants and Welfare Implications of US Workers' Diverging Location Choices by Skill: 1980--2000. \textit{American Economic Review}, 106(3), 479--524.",
            r"\bibitem{hsieh2019} Hsieh, C.-T. and Moretti, E. (2019). Housing Constraints and Spatial Misallocation. \textit{American Economic Journal: Macroeconomics}, 11(2), 1--39.",
        ],
        target_pages=55,
        qa=[
            {"question": "What is the main instrument for housing supply elasticity?", "answer": "Undevelopable land share and terrain slope index from Saiz (2010), interacted with population growth"},
            {"question": "What is the IV estimate of the housing supply elasticity in the baseline specification?", "answer": "1.841"},
            {"question": "What is the Kleibergen-Paap F-statistic for the baseline IV?", "answer": "84.2"},
            {"question": "By how much does a one standard deviation increase in the Wharton Regulatory Index reduce annual permit rates?", "answer": "28 percent (coefficient -0.284)"},
            {"question": "What amenity has the largest capitalization into house prices?", "answer": "Coastal location (dummy coefficient 0.214 in column 1)"},
        ],
    )


PAPER_BUILDERS["12"] = _paper_12_urban
