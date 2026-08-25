#!/usr/bin/env python3
"""Paper builder for paper 08 (Finance)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_08_finance() -> PaperSpec:
    # --- Tables ---
    summary_stats_factors = render_regression_table({
        "table_id": "summary-stats-factors",
        "caption": "Summary Statistics: Fama-French Factors",
        "label": "tab:summary-stats-factors",
        "model_labels": ["Mean", "SD", "Skew", "Kurt"],
        "panels": [{
            "dep_var": "Panel A: Monthly Returns (\\%), 1963-2022",
            "variables": [
                {"label": "MKT-RF (Excess Market)", "coefficients": ["0.64", "4.49", "-0.55", "4.18"],
                 "std_errors": ["(0.19)", "", "", ""]},
                {"label": "SMB (Small Minus Big)", "coefficients": ["0.22", "3.14", "0.22", "5.41"],
                 "std_errors": ["(0.13)", "", "", ""]},
                {"label": "HML (High Minus Low)", "coefficients": ["0.38", "3.01", "-0.08", "5.68"],
                 "std_errors": ["(0.13)", "", "", ""]},
                {"label": "RMW (Robust Minus Weak)", "coefficients": ["0.29", "2.18", "-0.41", "6.12"],
                 "std_errors": ["(0.09)", "", "", ""]},
                {"label": "CMA (Conservative Minus Aggressive)", "coefficients": ["0.31", "1.98", "0.18", "5.91"],
                 "std_errors": ["(0.08)", "", "", ""]},
                {"label": "RF (Risk-Free Rate)", "coefficients": ["0.34", "0.28", "1.12", "4.02"],
                 "std_errors": ["(0.01)", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714"]},
            {"label": "Start date", "values": ["Jul-1963", "Jul-1963", "Jul-1963", "Jul-1963"]},
        ],
        "notes": "Monthly returns in percent. Standard errors of mean in parentheses under Mean column. Skewness and excess kurtosis reported. Data from Kenneth French Data Library.",
        "qa": [
            {"question": "What is the mean monthly excess market return?", "answer": "0.64 percent"},
            {"question": "How many monthly observations span the sample?", "answer": "714"},
        ],
    })

    summary_stats_portfolios = render_regression_table({
        "table_id": "summary-stats-portfolios",
        "caption": "Summary Statistics: Test Portfolios",
        "label": "tab:summary-stats-portfolios",
        "model_labels": ["Mean", "SD", "Sharpe", "Auto"],
        "panels": [{
            "dep_var": "Panel A: Size-Sorted Quintile Portfolios (excess returns, \\%/month)",
            "variables": [
                {"label": "Small", "coefficients": ["0.81", "5.62", "0.144", "0.08"],
                 "std_errors": ["(0.22)", "", "", ""]},
                {"label": "2", "coefficients": ["0.71", "5.01", "0.142", "0.09"],
                 "std_errors": ["(0.20)", "", "", ""]},
                {"label": "3", "coefficients": ["0.62", "4.71", "0.132", "0.10"],
                 "std_errors": ["(0.18)", "", "", ""]},
                {"label": "4", "coefficients": ["0.58", "4.48", "0.129", "0.10"],
                 "std_errors": ["(0.17)", "", "", ""]},
                {"label": "Big", "coefficients": ["0.54", "4.21", "0.128", "0.11"],
                 "std_errors": ["(0.16)", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Book-to-Market Quintile Portfolios (excess returns, \\%/month)",
            "variables": [
                {"label": "Growth (Low BM)", "coefficients": ["0.48", "4.84", "0.099", "0.09"],
                 "std_errors": ["(0.18)", "", "", ""]},
                {"label": "2", "coefficients": ["0.56", "4.51", "0.124", "0.10"],
                 "std_errors": ["(0.17)", "", "", ""]},
                {"label": "3", "coefficients": ["0.64", "4.38", "0.146", "0.10"],
                 "std_errors": ["(0.16)", "", "", ""]},
                {"label": "4", "coefficients": ["0.71", "4.42", "0.161", "0.11"],
                 "std_errors": ["(0.17)", "", "", ""]},
                {"label": "Value (High BM)", "coefficients": ["0.84", "5.01", "0.168", "0.12"],
                 "std_errors": ["(0.19)", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714"]},
        ],
        "notes": "Excess returns above risk-free rate (\\%/month). Sharpe ratio: annualized mean divided by annualized SD. Auto: first-order autocorrelation.",
        "qa": [
            {"question": "What is the mean excess return of the Small portfolio?", "answer": "0.81 percent per month"},
            {"question": "What is the Sharpe ratio of the Value portfolio?", "answer": "0.168"},
            {"question": "What is the standard deviation of the Growth portfolio?", "answer": "4.84 percent"},
        ],
    })

    size_sorted_5 = render_regression_table({
        "table_id": "size-sorted-5",
        "caption": "Time-Series Regressions: Size-Sorted Quintile Portfolios",
        "label": "tab:size-sorted",
        "model_labels": ["Small", "2", "3", "4", "Big"],
        "panels": [{
            "dep_var": "Panel A: CAPM",
            "variables": [
                {"label": "Alpha (\\%/month)", "coefficients": ["0.28***", "0.18**", "0.07", "-0.02", "-0.08**"],
                 "std_errors": ["(0.09)", "(0.08)", "(0.07)", "(0.06)", "(0.04)"]},
                {"label": "MKT-RF", "coefficients": ["1.12***", "1.08***", "1.02***", "0.98***", "0.94***"],
                 "std_errors": ["(0.02)", "(0.02)", "(0.01)", "(0.01)", "(0.01)"]},
            ],
        }, {
            "dep_var": "Panel B: FF3",
            "variables": [
                {"label": "Alpha (\\%/month)", "coefficients": ["0.04", "0.01", "-0.02", "-0.03", "-0.06**"],
                 "std_errors": ["(0.05)", "(0.04)", "(0.04)", "(0.04)", "(0.03)"]},
                {"label": "MKT-RF", "coefficients": ["0.98***", "0.99***", "1.00***", "1.00***", "0.99***"],
                 "std_errors": ["(0.02)", "(0.01)", "(0.01)", "(0.01)", "(0.01)"]},
                {"label": "SMB", "coefficients": ["1.42***", "1.01***", "0.72***", "0.42***", "-0.14***"],
                 "std_errors": ["(0.04)", "(0.03)", "(0.03)", "(0.02)", "(0.02)"]},
                {"label": "HML", "coefficients": ["-0.04", "0.02", "0.04", "0.06*", "0.02"],
                 "std_errors": ["(0.04)", "(0.03)", "(0.03)", "(0.03)", "(0.02)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714", "714"]},
            {"label": "Adj. R-sq (CAPM)", "values": ["0.891", "0.921", "0.954", "0.968", "0.981"]},
            {"label": "Adj. R-sq (FF3)", "values": ["0.962", "0.978", "0.982", "0.984", "0.988"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Newey-West standard errors (4 lags). Portfolios sorted annually by NYSE size breakpoints.",
        "qa": [
            {"question": "What is the CAPM alpha for the Small portfolio?", "answer": "0.28 percent per month"},
            {"question": "What is the FF3 SMB loading for the Big portfolio?", "answer": "-0.14"},
        ],
    })

    bm_sorted_5 = render_regression_table({
        "table_id": "bm-sorted-5",
        "caption": "Time-Series Regressions: Book-to-Market Quintile Portfolios",
        "label": "tab:bm-sorted",
        "model_labels": ["Growth", "2", "3", "4", "Value"],
        "panels": [{
            "dep_var": "Panel A: CAPM",
            "variables": [
                {"label": "Alpha (\\%/month)", "coefficients": ["-0.14***", "-0.04", "0.04", "0.12**", "0.24***"],
                 "std_errors": ["(0.05)", "(0.04)", "(0.04)", "(0.05)", "(0.07)"]},
                {"label": "MKT-RF", "coefficients": ["1.06***", "1.01***", "0.98***", "0.99***", "1.04***"],
                 "std_errors": ["(0.01)", "(0.01)", "(0.01)", "(0.01)", "(0.02)"]},
            ],
        }, {
            "dep_var": "Panel B: FF3",
            "variables": [
                {"label": "Alpha (\\%/month)", "coefficients": ["-0.06*", "-0.01", "0.01", "0.03", "0.05"],
                 "std_errors": ["(0.03)", "(0.03)", "(0.03)", "(0.04)", "(0.05)"]},
                {"label": "MKT-RF", "coefficients": ["1.01***", "0.99***", "0.98***", "0.98***", "1.01***"],
                 "std_errors": ["(0.01)", "(0.01)", "(0.01)", "(0.01)", "(0.02)"]},
                {"label": "SMB", "coefficients": ["0.08**", "0.12***", "0.18***", "0.24***", "0.38***"],
                 "std_errors": ["(0.03)", "(0.03)", "(0.03)", "(0.04)", "(0.05)"]},
                {"label": "HML", "coefficients": ["-0.84***", "-0.41***", "0.12***", "0.58***", "1.08***"],
                 "std_errors": ["(0.04)", "(0.03)", "(0.03)", "(0.04)", "(0.05)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714", "714"]},
            {"label": "Adj. R-sq (CAPM)", "values": ["0.948", "0.961", "0.964", "0.951", "0.908"]},
            {"label": "Adj. R-sq (FF3)", "values": ["0.981", "0.974", "0.972", "0.968", "0.944"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Newey-West standard errors (4 lags). Annual NYSE BM breakpoints. HML loading increases monotonically from Growth to Value.",
        "qa": [
            {"question": "What is the CAPM alpha for the Value portfolio?", "answer": "0.24 percent per month"},
            {"question": "What is the FF3 HML loading for the Value portfolio?", "answer": "1.08"},
        ],
    })

    double_sorted_25 = render_regression_table({
        "table_id": "double-sorted-25",
        "caption": "Average Excess Returns (\\%/month): 25 Size- and Book-to-Market-Sorted Portfolios",
        "label": "tab:double-sorted-25",
        "model_labels": ["Low", "2", "3", "4", "High"],
        "panels": [{
            "dep_var": "Small",
            "variables": [
                {"label": "Average excess return", "coefficients": ["0.48", "0.72", "0.88", "1.01", "1.18"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }, {
            "dep_var": "2",
            "variables": [
                {"label": "Average excess return", "coefficients": ["0.44", "0.64", "0.74", "0.88", "0.98"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }, {
            "dep_var": "3",
            "variables": [
                {"label": "Average excess return", "coefficients": ["0.41", "0.58", "0.68", "0.78", "0.88"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }, {
            "dep_var": "4",
            "variables": [
                {"label": "Average excess return", "coefficients": ["0.38", "0.52", "0.61", "0.71", "0.82"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }, {
            "dep_var": "Big",
            "variables": [
                {"label": "Average excess return", "coefficients": ["0.34", "0.46", "0.55", "0.64", "0.74"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714", "714"]},
        ],
        "notes": "Average monthly excess returns (\\%) for 25 portfolios double-sorted on size (rows) and book-to-market (columns, Low=Growth, High=Value). Portfolios reformed annually using NYSE breakpoints. July 1963--December 2022.",
        "qa": [
            {"question": "What is the average excess return for the Small-High BM portfolio?", "answer": "1.18 percent per month"},
            {"question": "What is the average excess return for the Big-Low BM portfolio?", "answer": "0.34 percent per month"},
        ],
    })

    ts_capm = render_regression_table({
        "table_id": "ts-regressions-capm",
        "caption": "Time-Series Regressions: CAPM (25 Size/BM Portfolios)",
        "label": "tab:ts-capm",
        "model_labels": ["Mean alpha", "SD alpha", "Mean |t|", "GRS stat"],
        "panels": [{
            "dep_var": "CAPM Performance on 25 Size-BM Portfolios",
            "variables": [
                {"label": "All 25 portfolios", "coefficients": ["0.082", "0.091", "1.84", "4.12***"],
                 "std_errors": ["(0.018)", "(0.009)", "(0.21)", "(0.00)"]},
                {"label": "Size quintiles (5)", "coefficients": ["0.041", "0.052", "1.41", "2.14**"],
                 "std_errors": ["(0.022)", "(0.014)", "(0.28)", "(0.04)"]},
                {"label": "BM quintiles (5)", "coefficients": ["0.058", "0.062", "1.62", "3.21***"],
                 "std_errors": ["(0.019)", "(0.016)", "(0.24)", "(0.00)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714"]},
            {"label": "Avg. Adj. R-sq", "values": ["0.942", "0.942", "0.942", "0.942"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. GRS p-value in parentheses. Mean alpha is cross-sectional average of time-series intercepts (\\%/month). CAPM is rejected at all conventional significance levels.",
        "qa": [
            {"question": "What is the GRS statistic for CAPM on all 25 portfolios?", "answer": "4.12"},
            {"question": "What is the mean absolute alpha under CAPM?", "answer": "0.082 percent per month"},
            {"question": "What is the average adjusted R-squared for CAPM?", "answer": "0.942"},
        ],
    })

    ts_ff3 = render_regression_table({
        "table_id": "ts-regressions-ff3",
        "caption": "Time-Series Regressions: Fama-French Three-Factor Model",
        "label": "tab:ts-ff3",
        "model_labels": ["Mean alpha", "SD alpha", "Mean |t|", "GRS stat"],
        "panels": [{
            "dep_var": "FF3 Performance on 25 Size-BM Portfolios",
            "variables": [
                {"label": "All 25 portfolios", "coefficients": ["0.031", "0.038", "1.12", "1.54"],
                 "std_errors": ["(0.008)", "(0.007)", "(0.18)", "(0.07)"]},
                {"label": "Size quintiles (5)", "coefficients": ["0.018", "0.021", "0.94", "0.88"],
                 "std_errors": ["(0.008)", "(0.010)", "(0.22)", "(0.48)"]},
                {"label": "BM quintiles (5)", "coefficients": ["0.024", "0.028", "1.01", "1.12"],
                 "std_errors": ["(0.010)", "(0.011)", "(0.21)", "(0.34)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714"]},
            {"label": "Avg. Adj. R-sq", "values": ["0.971", "0.971", "0.971", "0.971"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. GRS p-value in parentheses. FF3 fails to reject the null that all alphas are jointly zero at 5\\% level for 25 size-BM portfolios.",
        "qa": [
            {"question": "What is the GRS statistic for FF3 on all 25 portfolios?", "answer": "1.54"},
            {"question": "What is the mean alpha under FF3?", "answer": "0.031 percent per month"},
            {"question": "What is the average adjusted R-squared for FF3?", "answer": "0.971"},
        ],
    })

    ts_ff5 = render_regression_table({
        "table_id": "ts-regressions-ff5",
        "caption": "Time-Series Regressions: Fama-French Five-Factor Model",
        "label": "tab:ts-ff5",
        "model_labels": ["Mean alpha", "SD alpha", "Mean |t|", "GRS stat"],
        "panels": [{
            "dep_var": "FF5 Performance on 25 Size-BM Portfolios",
            "variables": [
                {"label": "All 25 portfolios", "coefficients": ["0.021", "0.027", "0.88", "1.18"],
                 "std_errors": ["(0.006)", "(0.005)", "(0.16)", "(0.28)"]},
                {"label": "Size quintiles (5)", "coefficients": ["0.014", "0.018", "0.74", "0.71"],
                 "std_errors": ["(0.007)", "(0.008)", "(0.20)", "(0.58)"]},
                {"label": "BM quintiles (5)", "coefficients": ["0.018", "0.022", "0.82", "0.91"],
                 "std_errors": ["(0.008)", "(0.009)", "(0.19)", "(0.44)"]},
            ],
        }, {
            "dep_var": "FF5 Performance on 25 Size-OP Portfolios",
            "variables": [
                {"label": "All 25 portfolios", "coefficients": ["0.018", "0.024", "0.81", "1.04"],
                 "std_errors": ["(0.005)", "(0.005)", "(0.15)", "(0.38)"]},
                {"label": "OP quintiles (5)", "coefficients": ["0.012", "0.014", "0.68", "0.62"],
                 "std_errors": ["(0.005)", "(0.006)", "(0.18)", "(0.64)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714"]},
            {"label": "Avg. Adj. R-sq", "values": ["0.974", "0.974", "0.974", "0.974"]},
        ],
        "notes": "*** p<0.01. FF5 adds profitability (RMW) and investment (CMA) to FF3. Improves performance on profitability-sorted portfolios relative to FF3.",
        "qa": [
            {"question": "What is the GRS statistic for FF5 on 25 size-BM portfolios?", "answer": "1.18"},
            {"question": "What is the mean alpha under FF5 for 25 size-BM portfolios?", "answer": "0.021 percent per month"},
            {"question": "Does FF5 improve on FF3 for BM-sorted portfolios?", "answer": "Yes, GRS falls from 1.12 (FF3) to 0.91 (FF5)"},
        ],
    })

    cross_section_fm = render_regression_table({
        "table_id": "cross-section-fm",
        "caption": "Fama-MacBeth Cross-Sectional Regressions",
        "label": "tab:fm-cross-section",
        "model_labels": ["(1) CAPM", "(2) FF3", "(3) FF5", "(4) FF5+MOM"],
        "panels": [{
            "dep_var": "Estimated factor risk premia (\\%/month)",
            "variables": [
                {"label": "Intercept (lambda_0)", "coefficients": ["0.41***", "0.28**", "0.24**", "0.22**"],
                 "std_errors": ["(0.11)", "(0.12)", "(0.11)", "(0.10)"]},
                {"label": "lambda_MKT", "coefficients": ["0.28", "0.31", "0.29", "0.28"],
                 "std_errors": ["(0.21)", "(0.20)", "(0.19)", "(0.18)"]},
                {"label": "lambda_SMB", "coefficients": ["--", "0.18**", "0.16**", "0.15**"],
                 "std_errors": ["", "(0.08)", "(0.07)", "(0.07)"]},
                {"label": "lambda_HML", "coefficients": ["--", "0.22***", "0.19***", "0.17***"],
                 "std_errors": ["", "(0.07)", "(0.07)", "(0.07)"]},
                {"label": "lambda_RMW", "coefficients": ["--", "--", "0.14**", "0.13**"],
                 "std_errors": ["", "", "(0.06)", "(0.06)"]},
                {"label": "lambda_CMA", "coefficients": ["--", "--", "0.12**", "0.11**"],
                 "std_errors": ["", "", "(0.06)", "(0.06)"]},
                {"label": "lambda_MOM", "coefficients": ["--", "--", "--", "0.41***"],
                 "std_errors": ["", "", "", "(0.14)"]},
            ],
        }],
        "summary": [
            {"label": "Test portfolios", "values": ["25", "25", "25", "25"]},
            {"label": "Avg. R-sq (cross-section)", "values": ["0.712", "0.842", "0.881", "0.904"]},
            {"label": "Months", "values": ["714", "714", "714", "714"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. Shanken-corrected standard errors in parentheses. Test assets: 25 size-BM portfolios. Monthly cross-sectional regressions of excess returns on betas estimated from full-sample rolling 60-month windows.",
        "qa": [
            {"question": "What is the Fama-MacBeth HML risk premium in the FF3 specification?", "answer": "0.22 percent per month"},
            {"question": "What is the cross-sectional R-squared for FF5+MOM?", "answer": "0.904"},
        ],
    })

    grs_test = render_regression_table({
        "table_id": "grs-test",
        "caption": "GRS Test Statistics Across Asset Pricing Models and Test Portfolios",
        "label": "tab:grs-test",
        "model_labels": ["CAPM", "FF3", "FF5", "FF5+MOM"],
        "panels": [{
            "dep_var": "GRS F-statistic",
            "variables": [
                {"label": "25 Size-BM portfolios", "coefficients": ["4.12***", "1.54", "1.18", "1.08"],
                 "std_errors": ["[0.000]", "[0.068]", "[0.276]", "[0.368]"]},
                {"label": "25 Size-OP portfolios", "coefficients": ["5.41***", "2.18***", "1.04", "0.98"],
                 "std_errors": ["[0.000]", "[0.002]", "[0.412]", "[0.498]"]},
                {"label": "25 Size-INV portfolios", "coefficients": ["3.88***", "1.98**", "1.12", "1.04"],
                 "std_errors": ["[0.000]", "[0.016]", "[0.332]", "[0.402]"]},
                {"label": "32 Size-BM-OP portfolios", "coefficients": ["6.12***", "2.84***", "1.48*", "1.21"],
                 "std_errors": ["[0.000]", "[0.000]", "[0.069]", "[0.228]"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. GRS p-values in brackets. GRS null: all portfolio alphas are jointly zero. FF5 not rejected at 5\\% for 25 size-BM, 25 size-OP, or 25 size-INV portfolios.",
        "qa": [
            {"question": "What is the GRS statistic for CAPM on 25 size-BM portfolios?", "answer": "4.12"},
            {"question": "Is FF5 rejected for 25 size-BM portfolios at 5% level?", "answer": "No, GRS p-value is 0.276"},
        ],
    })

    factor_correlations = render_regression_table({
        "table_id": "factor-correlations",
        "caption": "Correlations Among Fama-French Five Factors",
        "label": "tab:factor-correlations",
        "model_labels": ["MKT-RF", "SMB", "HML", "RMW"],
        "panels": [{
            "dep_var": "Pairwise Pearson Correlations",
            "variables": [
                {"label": "SMB", "coefficients": ["0.28***", "1.00", "--", "--"],
                 "std_errors": ["(0.04)", "", "", ""]},
                {"label": "HML", "coefficients": ["-0.31***", "-0.08**", "1.00", "--"],
                 "std_errors": ["(0.04)", "(0.04)", "", ""]},
                {"label": "RMW", "coefficients": ["-0.22***", "-0.38***", "0.12***", "1.00"],
                 "std_errors": ["(0.04)", "(0.04)", "(0.04)", ""]},
                {"label": "CMA", "coefficients": ["-0.41***", "-0.11***", "0.68***", "0.16***"],
                 "std_errors": ["(0.04)", "(0.04)", "(0.03)", "(0.04)"]},
            ],
        }],
        "notes": "*** p<0.01, ** p<0.05. Standard errors from Newey-West with 4 lags. CMA and HML are highly correlated (0.68), reflecting the investment-value connection documented in Fama and French (2015).",
        "qa": [
            {"question": "What is the correlation between CMA and HML?", "answer": "0.68"},
            {"question": "What is the correlation between SMB and RMW?", "answer": "-0.38"},
        ],
    })

    momentum = render_regression_table({
        "table_id": "momentum",
        "caption": "Momentum-Sorted Portfolios and the Fama-French Models",
        "label": "tab:momentum",
        "model_labels": ["Loser", "2", "3", "4", "Winner"],
        "panels": [{
            "dep_var": "Panel A: Average excess returns (\\%/month)",
            "variables": [
                {"label": "Excess return", "coefficients": ["-0.28", "0.42", "0.64", "0.84", "1.41***"],
                 "std_errors": ["(0.28)", "(0.14)", "(0.11)", "(0.10)", "(0.12)"]},
            ],
        }, {
            "dep_var": "Panel B: FF3 alphas",
            "variables": [
                {"label": "FF3 alpha", "coefficients": ["-0.81***", "-0.08", "0.08", "0.24***", "0.81***"],
                 "std_errors": ["(0.18)", "(0.08)", "(0.07)", "(0.08)", "(0.14)"]},
            ],
        }, {
            "dep_var": "Panel C: FF5 alphas",
            "variables": [
                {"label": "FF5 alpha", "coefficients": ["-0.74***", "-0.06", "0.07", "0.21***", "0.74***"],
                 "std_errors": ["(0.17)", "(0.07)", "(0.06)", "(0.07)", "(0.13)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["714", "714", "714", "714", "714"]},
        ],
        "notes": "*** p<0.01. Momentum portfolios sorted on prior 12-2 month returns. Loser-winner spread (-0.28 - 1.41 = -1.69\\%/month) is unexplained by both FF3 and FF5.",
        "qa": [
            {"question": "What is the average excess return of the Winner portfolio?", "answer": "1.41 percent per month"},
            {"question": "Does FF5 explain momentum?", "answer": "No, FF5 alpha for Winner is 0.74 and Loser is -0.74, both significant"},
        ],
    })

    industry_portfolios = render_regression_table({
        "table_id": "industry-portfolios",
        "caption": "FF5 Alphas: 12 Industry Portfolios",
        "label": "tab:industry",
        "model_labels": ["Alpha", "MKT-RF", "SMB", "HML"],
        "panels": [{
            "dep_var": "FF5 time-series regression coefficients",
            "variables": [
                {"label": "Consumer NoDur", "coefficients": ["0.11**", "0.84***", "-0.04", "0.18***"],
                 "std_errors": ["(0.05)", "(0.02)", "(0.03)", "(0.04)"]},
                {"label": "Consumer Dur", "coefficients": ["-0.08", "1.14***", "0.28***", "0.14***"],
                 "std_errors": ["(0.07)", "(0.03)", "(0.04)", "(0.05)"]},
                {"label": "Manufacturing", "coefficients": ["0.04", "1.02***", "0.12***", "0.22***"],
                 "std_errors": ["(0.04)", "(0.02)", "(0.03)", "(0.03)"]},
                {"label": "Energy", "coefficients": ["0.14*", "0.88***", "-0.08**", "0.41***"],
                 "std_errors": ["(0.08)", "(0.03)", "(0.04)", "(0.06)"]},
                {"label": "HiTec", "coefficients": ["-0.04", "1.18***", "0.08**", "-0.28***"],
                 "std_errors": ["(0.05)", "(0.02)", "(0.04)", "(0.04)"]},
                {"label": "Telecom", "coefficients": ["0.02", "0.94***", "-0.11***", "0.08"],
                 "std_errors": ["(0.06)", "(0.02)", "(0.04)", "(0.05)"]},
                {"label": "Shops", "coefficients": ["0.08", "0.98***", "0.04", "-0.04"],
                 "std_errors": ["(0.05)", "(0.02)", "(0.03)", "(0.04)"]},
                {"label": "Health", "coefficients": ["0.14**", "0.78***", "-0.12***", "0.04"],
                 "std_errors": ["(0.06)", "(0.02)", "(0.04)", "(0.04)"]},
                {"label": "Utils", "coefficients": ["0.04", "0.61***", "-0.14***", "0.48***"],
                 "std_errors": ["(0.05)", "(0.02)", "(0.03)", "(0.05)"]},
                {"label": "Finance", "coefficients": ["-0.02", "1.08***", "-0.04", "0.28***"],
                 "std_errors": ["(0.04)", "(0.02)", "(0.03)", "(0.04)"]},
                {"label": "Other", "coefficients": ["0.01", "1.01***", "0.18***", "0.14***"],
                 "std_errors": ["(0.04)", "(0.02)", "(0.03)", "(0.03)"]},
                {"label": "Mean |alpha|", "coefficients": ["0.061", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "GRS stat", "values": ["1.44", "--", "--", "--"]},
            {"label": "GRS p-value", "values": ["[0.142]", "--", "--", "--"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. FF5 not rejected at 10\\% for 12 industry portfolios (GRS p=0.142). Energy and Consumer NoDur have marginally significant positive alphas.",
        "qa": [
            {"question": "What is the FF5 GRS statistic for 12 industry portfolios?", "answer": "1.44"},
            {"question": "What is the market beta for Utils?", "answer": "0.61"},
        ],
    })

    international = render_regression_table({
        "table_id": "international",
        "caption": "International Evidence: FF3 Alphas by Region",
        "label": "tab:international",
        "model_labels": ["North Am.", "Europe", "Asia-Pac.", "Global"],
        "panels": [{
            "dep_var": "Panel A: Value premium (High-Low BM alpha, \\%/month)",
            "variables": [
                {"label": "FF3 alpha", "coefficients": ["0.31***", "0.28***", "0.24**", "0.29***"],
                 "std_errors": ["(0.08)", "(0.09)", "(0.11)", "(0.06)"]},
                {"label": "t-statistic", "coefficients": ["3.88", "3.11", "2.18", "4.83"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Size premium (Small-Big alpha, \\%/month)",
            "variables": [
                {"label": "FF3 alpha", "coefficients": ["0.18**", "0.14*", "0.21**", "0.17***"],
                 "std_errors": ["(0.08)", "(0.08)", "(0.09)", "(0.06)"]},
                {"label": "t-statistic", "coefficients": ["2.25", "1.75", "2.33", "2.83"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Sample start", "values": ["Jul-1963", "Nov-1990", "Nov-1990", "Nov-1990"]},
            {"label": "Sample end", "values": ["Dec-2022", "Dec-2022", "Dec-2022", "Dec-2022"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Newey-West standard errors. International data from MSCI indices and Datastream. Value and size premia are present in all major regions.",
        "qa": [
            {"question": "What is the value premium alpha in Europe?", "answer": "0.28 percent per month"},
            {"question": "What is the t-statistic for the global value premium?", "answer": "4.83"},
        ],
    })

    sub_period_early = render_regression_table({
        "table_id": "sub-period-early",
        "caption": "Sub-Period Analysis: 1963-1992",
        "label": "tab:sub-period-early",
        "model_labels": ["CAPM", "FF3", "FF5", "FF5+MOM"],
        "panels": [{
            "dep_var": "GRS statistics: 25 size-BM portfolios",
            "variables": [
                {"label": "GRS F-statistic", "coefficients": ["4.88***", "1.84**", "1.41", "1.18"],
                 "std_errors": ["[0.000]", "[0.024]", "[0.108]", "[0.281]"]},
                {"label": "Mean |alpha| (\\%/month)", "coefficients": ["0.098", "0.041", "0.028", "0.022"],
                 "std_errors": ["(0.022)", "(0.009)", "(0.007)", "(0.006)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["354", "354", "354", "354"]},
            {"label": "Period", "values": ["1963-92", "1963-92", "1963-92", "1963-92"]},
        ],
        "notes": "*** p<0.01, ** p<0.05. GRS p-values in brackets. Sub-period July 1963 -- December 1992.",
        "qa": [
            {"question": "What is the CAPM GRS statistic in the early sub-period?", "answer": "4.88"},
            {"question": "What is the FF3 GRS p-value in the early sub-period?", "answer": "0.024"},
        ],
    })

    sub_period_late = render_regression_table({
        "table_id": "sub-period-late",
        "caption": "Sub-Period Analysis: 1993-2022",
        "label": "tab:sub-period-late",
        "model_labels": ["CAPM", "FF3", "FF5", "FF5+MOM"],
        "panels": [{
            "dep_var": "GRS statistics: 25 size-BM portfolios",
            "variables": [
                {"label": "GRS F-statistic", "coefficients": ["3.44***", "1.28", "1.01", "0.94"],
                 "std_errors": ["[0.000]", "[0.211]", "[0.461]", "[0.548]"]},
                {"label": "Mean |alpha| (\\%/month)", "coefficients": ["0.068", "0.022", "0.014", "0.011"],
                 "std_errors": ["(0.016)", "(0.006)", "(0.004)", "(0.003)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["360", "360", "360", "360"]},
            {"label": "Period", "values": ["1993-22", "1993-22", "1993-22", "1993-22"]},
        ],
        "notes": "*** p<0.01. GRS p-values in brackets. Sub-period January 1993 -- December 2022. CAPM continues to be strongly rejected; FF3 and FF5 cannot be rejected in the more recent period.",
        "qa": [
            {"question": "What is the CAPM GRS statistic in the late sub-period?", "answer": "3.44"},
            {"question": "What is the FF5 GRS p-value in the late sub-period?", "answer": "0.461"},
        ],
    })

    appendix_construction = render_regression_table({
        "table_id": "appendix-construction",
        "caption": "Appendix: Portfolio Construction Details",
        "label": "tab:appendix-construction",
        "model_labels": ["Variable", "Source", "Breakpoint", "Frequency"],
        "panels": [{
            "dep_var": "Factor Construction",
            "variables": [
                {"label": "Market cap (ME)", "coefficients": ["Market cap", "CRSP", "NYSE median", "Monthly"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Book-to-market (BM)", "coefficients": ["Book eq./ME", "Compustat", "NYSE 30/70", "Annual"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Operating profitability (OP)", "coefficients": ["RevProfit/Assets", "Compustat", "NYSE 30/70", "Annual"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Investment (INV)", "coefficients": ["DeltaAssets/Assets", "Compustat", "NYSE 30/70", "Annual"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Momentum (MOM)", "coefficients": ["Ret(-12,-2)", "CRSP", "NYSE 30/70", "Monthly"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Portfolios reformed annually in July using prior fiscal year accounting data. Six-month gap between fiscal year end and portfolio formation (June) ensures data availability.",
        "qa": [
            {"question": "Which exchange provides size breakpoints?", "answer": "NYSE"},
            {"question": "When are portfolios reformed annually?", "answer": "July of each year"},
        ],
    })

    appendix_returns = render_regression_table({
        "table_id": "appendix-returns",
        "caption": "Appendix: Annual Returns by Factor Quintile",
        "label": "tab:appendix-returns",
        "model_labels": ["Q1 (Low)", "Q2", "Q3", "Q4", "Q5 (High)"],
        "panels": [{
            "dep_var": "Panel A: Annual returns by size quintile (\\%/year, excess)",
            "variables": [
                {"label": "Value-weighted", "coefficients": ["9.12", "7.88", "7.41", "7.08", "6.74"],
                 "std_errors": ["(2.21)", "(1.98)", "(1.84)", "(1.74)", "(1.62)"]},
            ],
        }, {
            "dep_var": "Panel B: Annual returns by BM quintile (\\%/year, excess)",
            "variables": [
                {"label": "Value-weighted", "coefficients": ["5.81", "6.74", "7.68", "8.52", "9.98"],
                 "std_errors": ["(2.14)", "(1.88)", "(1.78)", "(1.84)", "(2.08)"]},
            ],
        }],
        "summary": [
            {"label": "Sample", "values": ["1963-2022", "1963-2022", "1963-2022", "1963-2022", "1963-2022"]},
        ],
        "notes": "Annualized excess returns (\\%) and standard errors (in parentheses). Standard errors computed from annual observations.",
        "qa": [
            {"question": "What is the annual excess return for the High BM quintile?", "answer": "9.98 percent"},
            {"question": "What is the annual excess return for the Small size quintile?", "answer": "9.12 percent"},
        ],
    })

    # --- Equations ---
    eq_capm = EquationSpec(
        "capm",
        r"\mathbb{E}[R_i] - R_f = \hat{\beta}_i \left(\mathbb{E}[R_m] - R_f\right), \quad \hat{\beta}_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}, \quad \mathbb{P}\!\left(\hat{\beta}_i \in \mathbb{R}^+\right) > 0",
        "eq:capm",
        "CAPM: expected excess return of asset $i$ equals market beta times the equity risk premium.",
        [{"question": "What does beta_i measure in the CAPM?", "answer": "The covariance of asset return with market return, divided by market return variance"}],
    )

    eq_ff3 = EquationSpec(
        "ff3-model",
        r"R_{it} - R_{ft} = \alpha_i + b_i (R_{mt} - R_{ft}) + s_i \text{SMB}_t + h_i \text{HML}_t + \varepsilon_{it}",
        "eq:ff3",
        "Fama-French three-factor model: asset excess return regressed on market, size (SMB), and value (HML) factors.",
        [{"question": "What do the loadings s_i and h_i measure in FF3?", "answer": "Sensitivity to the size factor (SMB) and value factor (HML) respectively"}],
    )

    eq_expected_return = EquationSpec(
        "expected-return",
        r"E[R_i - R_f] = b_i \lambda_{MKT} + s_i \lambda_{SMB} + h_i \lambda_{HML} + r_i \lambda_{RMW} + c_i \lambda_{CMA}",
        "eq:expected-return",
        "Expected excess return in FF5 cross-sectional model: factor loadings times factor risk premia $\\lambda$.",
    )

    eq_fama_macbeth = EquationSpec(
        "fama-macbeth",
        r"\bar{\lambda} = \frac{1}{T} \sum_{t=1}^T \hat{\lambda}_t, \quad \hat{\lambda}_t = (\hat{B}' \hat{B})^{-1} \hat{B}' R_t, \quad \text{se}(\bar{\lambda}) = \frac{1}{\sqrt{T}} \text{sd}(\hat{\lambda}_t)",
        "eq:fama-macbeth",
        "Fama-MacBeth (1973) two-pass procedure: estimate betas in the first pass, then run monthly cross-sectional regressions to estimate risk premia $\\hat{\\lambda}_t$.",
        [{"question": "How are standard errors computed in Fama-MacBeth?", "answer": "Standard deviation of the time series of monthly cross-sectional estimates, divided by sqrt(T)"}],
    )

    eq_grs = EquationSpec(
        "grs-test",
        r"GRS = \frac{T}{N} \cdot \frac{T - N - K}{T - K - 1} \cdot \frac{\hat{\alpha}' \hat{\Sigma}^{-1} \hat{\alpha}}{1 + \bar{\mu}' \hat{\Omega}^{-1} \bar{\mu}} \sim F(N, T-N-K), \quad \hat{\Sigma} = \begin{bmatrix}\tilde{\sigma}_{11} & \cdots & \tilde{\sigma}_{1N} \\ \vdots & \ddots & \vdots \\ \tilde{\sigma}_{N1} & \cdots & \tilde{\sigma}_{NN}\end{bmatrix}",
        "eq:grs",
        "Gibbons-Ross-Shanken (1989) test statistic. $\\hat{\\alpha}$ is the $N\\times1$ vector of OLS intercepts, $\\hat{\\Sigma}$ is the residual covariance, $\\bar{\\mu}$ is the mean factor vector, and $K$ is the number of factors.",
        [{"question": "What is the null hypothesis of the GRS test?", "answer": "All N portfolio alphas are jointly equal to zero: alpha = 0"}],
    )

    eq_alpha = EquationSpec(
        "alpha",
        r"\hat{\alpha}_i = \mathbb{E}[R_i - R_f] - \sum_{k=1}^K \hat{\beta}_{ik} \tilde{\lambda}_k, \quad \mathbb{P}\!\left(\hat{\alpha}_i = 0 \mid \mathcal{H}_0\right) = 1 - \mathbb{P}\!\left(\text{GRS} > F_{N,T-N-K}^{-1}(1-\alpha)\right)",
        "eq:alpha",
        "Jensen's alpha: the difference between a portfolio's expected excess return and the expected return predicted by the factor model.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[GRS Test Derivation]
Let $R_t = \alpha + B f_t + \varepsilon_t$ for $t=1,\ldots,T$, where $R_t$ is $N\times 1$, $f_t$ is $K\times 1$, and $\varepsilon_t \sim \mathcal{N}(0,\Sigma)$ iid. The GRS test of $H_0: \alpha = 0$ uses the likelihood ratio:
\begin{align}
LR &= T \left(\log |\hat{\Sigma}_0| - \log |\hat{\Sigma}_1|\right),
\end{align}
where $\hat{\Sigma}_1$ is the unrestricted and $\hat{\Sigma}_0$ the restricted MLE. Gibbons, Ross, and Shanken (1989) show this simplifies to:
\begin{align}
\frac{T-N-K}{N} \cdot \frac{\hat{\alpha}' \hat{\Sigma}^{-1} \hat{\alpha}}{1 + \hat{\mu}_f' \hat{\Omega}_f^{-1} \hat{\mu}_f} &\sim F(N, T-N-K),
\end{align}
exactly under normality. The denominator $1 + \hat{\mu}_f' \hat{\Omega}_f^{-1} \hat{\mu}_f$ is the squared Sharpe ratio of the tangency portfolio of the $K$ factors plus one; it captures the precision with which factors span the mean-variance frontier.
\end{proposition}

\begin{proposition}[Fama-MacBeth Standard Error Correction]
The naive Fama-MacBeth standard error $\text{se}(\bar{\lambda}) = T^{-1/2} \text{sd}(\hat{\lambda}_t)$ is downward biased because the betas $\hat{B}$ are estimated with error. Shanken (1992) shows the corrected asymptotic covariance is:
\begin{align}
\text{Avar}(\bar{\lambda}) &= \frac{1}{T}\left[(B'\Sigma^{-1}B)^{-1} B'\Sigma^{-1} \text{Var}(R_t) \Sigma^{-1} B (B'\Sigma^{-1}B)^{-1}\right](1 + \lambda' \Omega_f^{-1} \lambda),
\end{align}
where $(1 + \lambda' \Omega_f^{-1} \lambda)$ is the Shanken correction factor. Under the null $\lambda = 0$, the correction factor equals 1 and the naive standard error is asymptotically valid.
\end{proposition}

\begin{proposition}[Shanken Correction Factor]
Define $c = \lambda' \Omega_f^{-1} \lambda$ as the squared Sharpe ratio of the factor mimicking portfolio. The Shanken-corrected covariance satisfies:
\begin{align}
\text{Avar}(\bar{\lambda}) &= (1 + c) \cdot \text{Avar}_{naive}(\bar{\lambda}) + O(T^{-1}),
\end{align}
so the asymptotic inflation of standard errors equals $\sqrt{1 + c}$. For the FF3 model with typical sample Sharpe ratios, $c \approx 0.08$-$0.18$, implying standard error inflation of 4-8\\%. Empirically, Shanken-corrected and naive t-statistics differ modestly, but the correction matters for inference when risk premia are large relative to factor standard deviations.
\end{proposition}

\noindent\textbf{Matrix representation of the cross-sectional regression.} Define the hat matrix $\hat{H} = \hat{B}(\hat{B}'\hat{B})^{-1}\hat{B}'$ and the residual covariance with tilde notation:
\begin{align}
\tilde{\Sigma} &= \begin{bmatrix} \tilde{\sigma}_{11} & \tilde{\sigma}_{12} & \cdots & \tilde{\sigma}_{1N} \\ \tilde{\sigma}_{21} & \tilde{\sigma}_{22} & \cdots & \tilde{\sigma}_{2N} \\ \vdots & \vdots & \ddots & \vdots \\ \tilde{\sigma}_{N1} & \tilde{\sigma}_{N2} & \cdots & \tilde{\sigma}_{NN}\end{bmatrix}, \quad \mathbb{P}\!\left(\hat{\lambda}_t \in \mathbb{R}^K\right) = 1.
\end{align}
Under the assumption that factor returns are drawn from a multivariate distribution with $\mathbb{E}[f_t f_t'] = \hat{\Omega}_f$, the GRS statistic converges in probability.
"""

    appendix_proof_table = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-finance", text_paragraphs=15,
                        equations=[eq_capm])

    data_section = SectionSpec(
        "Data", "sec:data-finance", text_paragraphs=12,
        tables=[summary_stats_factors, summary_stats_portfolios],
        subsections=[
            SectionSpec("Factor Construction", "sec:data-factors", level=2, text_paragraphs=9),
            SectionSpec("Test Portfolio Construction", "sec:data-portfolios", level=2, text_paragraphs=8),
        ],
    )

    theoretical_framework = SectionSpec(
        "Theoretical Framework", "sec:theory-finance", text_paragraphs=12,
        equations=[eq_ff3, eq_expected_return, eq_alpha],
        subsections=[
            SectionSpec("The CAPM and Its Limitations", "sec:theory-capm", level=2, text_paragraphs=9),
            SectionSpec("The Fama-French Model", "sec:theory-ff", level=2, text_paragraphs=8),
            SectionSpec("The Five-Factor Extension", "sec:theory-ff5", level=2, text_paragraphs=8),
        ],
    )

    univariate_sorts = SectionSpec(
        "Univariate Portfolio Sorts", "sec:univariate", text_paragraphs=11,
        tables=[size_sorted_5, bm_sorted_5],
        subsections=[
            SectionSpec("Size-Sorted Portfolios", "sec:size-sorts", level=2, text_paragraphs=8),
            SectionSpec("Book-to-Market-Sorted Portfolios", "sec:bm-sorts", level=2, text_paragraphs=8),
        ],
    )

    double_sorts = SectionSpec(
        "Double-Sorted Portfolios", "sec:double-sorts", text_paragraphs=12,
        tables=[double_sorted_25],
        subsections=[
            SectionSpec("25 Size-BM Portfolios: Average Returns", "sec:25-avg-returns", level=2, text_paragraphs=9),
            SectionSpec("Patterns in the Double-Sort Matrix", "sec:25-patterns", level=2, text_paragraphs=8),
        ],
    )

    ts_regressions = SectionSpec(
        "Time-Series Regressions and Model Tests", "sec:ts-regressions", text_paragraphs=11,
        equations=[eq_grs],
        tables=[ts_capm, ts_ff3, ts_ff5, grs_test],
        subsections=[
            SectionSpec("CAPM Performance", "sec:ts-capm", level=2, text_paragraphs=8),
            SectionSpec("FF3 Performance", "sec:ts-ff3", level=2, text_paragraphs=8),
            SectionSpec("FF5 Performance", "sec:ts-ff5", level=2, text_paragraphs=7),
        ],
    )

    cross_section_section = SectionSpec(
        "Cross-Sectional Asset Pricing", "sec:cross-section", text_paragraphs=11,
        equations=[eq_fama_macbeth],
        tables=[cross_section_fm, factor_correlations],
        subsections=[
            SectionSpec("Fama-MacBeth Estimation", "sec:fm-estimation", level=2, text_paragraphs=9),
            SectionSpec("Factor Risk Premia", "sec:factor-premia", level=2, text_paragraphs=8),
        ],
    )

    further_evidence = SectionSpec(
        "Further Evidence", "sec:further-evidence", text_paragraphs=10,
        tables=[momentum, industry_portfolios, international],
        subsections=[
            SectionSpec("Momentum: A Challenge for FF5", "sec:momentum", level=2, text_paragraphs=8),
            SectionSpec("Industry Portfolios", "sec:industry", level=2, text_paragraphs=7),
            SectionSpec("International Evidence", "sec:international", level=2, text_paragraphs=7),
        ],
    )

    robustness = SectionSpec(
        "Robustness", "sec:robustness-finance", text_paragraphs=10,
        tables=[sub_period_early, sub_period_late],
        subsections=[
            SectionSpec("Sub-Period Stability", "sec:sub-periods", level=2, text_paragraphs=8),
            SectionSpec("Alternative Factor Definitions", "sec:alt-factors", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-finance", text_paragraphs=11)

    appendix_a = SectionSpec(
        "Appendix A: Econometric Theory", "sec:appendix-a-finance", text_paragraphs=3,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Data and Construction", "sec:appendix-b-finance", text_paragraphs=4,
        tables=[appendix_construction, appendix_returns],
    )

    return PaperSpec(
        paper_id="08",
        field_slug="finance",
        title="The Cross-Section of Expected Stock Returns: A Comprehensive Test of the Fama-French Five-Factor Model",
        authors="Priya Venkataraman, Marcus Holbrook, Yuki Tanaka",
        journal_style="jfe",
        abstract=(
            "We provide comprehensive evidence on the Fama-French five-factor (FF5) model using 60 years "
            "of data from July 1963 to December 2022. On the benchmark 25 size- and book-to-market-sorted "
            "portfolios, the GRS test fails to reject FF5 (F = 1.18, p = 0.276), while CAPM is strongly "
            "rejected (F = 4.12, p < 0.001). The high BM portfolio earns 1.18\\% per month for the smallest "
            "size quintile, compared to 0.34\\% for large-growth stocks. Fama-MacBeth estimates confirm "
            "economically significant HML (0.22\\%/month) and SMB (0.18\\%/month) premia. However, "
            "momentum portfolios generate FF5 alphas of $\\pm 0.74\\%$/month, confirming that momentum "
            "remains unexplained. Evidence from 12 industry portfolios and international data across "
            "three regions corroborates the model. Sub-period analysis shows model performance has "
            "improved in the post-1993 sample."
        ),
        sections=[intro, data_section, theoretical_framework, univariate_sorts, double_sorts,
                  ts_regressions, cross_section_section, further_evidence, robustness,
                  conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{fama1993} Fama, E. F. and French, K. R. (1993). Common Risk Factors in the Returns on Stocks and Bonds. \textit{Journal of Financial Economics}, 33(1), 3--56.",
            r"\bibitem{fama2015} Fama, E. F. and French, K. R. (2015). A Five-Factor Asset Pricing Model. \textit{Journal of Financial Economics}, 116(1), 1--22.",
            r"\bibitem{fama1973} Fama, E. F. and MacBeth, J. D. (1973). Risk, Return, and Equilibrium: Empirical Tests. \textit{Journal of Political Economy}, 81(3), 607--636.",
            r"\bibitem{gibbons1989} Gibbons, M. R., Ross, S. A., and Shanken, J. (1989). A Test of the Efficiency of a Given Portfolio. \textit{Econometrica}, 57(5), 1121--1152.",
            r"\bibitem{shanken1992} Shanken, J. (1992). On the Estimation of Beta-Pricing Models. \textit{Review of Financial Studies}, 5(1), 1--33.",
            r"\bibitem{carhart1997} Carhart, M. M. (1997). On Persistence in Mutual Fund Performance. \textit{Journal of Finance}, 52(1), 57--82.",
            r"\bibitem{jegadeesh1993} Jegadeesh, N. and Titman, S. (1993). Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency. \textit{Journal of Finance}, 48(1), 65--91.",
            r"\bibitem{hou2015} Hou, K., Xue, C., and Zhang, L. (2015). Digesting Anomalies: An Investment Approach. \textit{Review of Financial Studies}, 28(3), 650--705.",
            r"\bibitem{harvey2016} Harvey, C. R., Liu, Y., and Zhu, H. (2016). ... and the Cross-Section of Expected Returns. \textit{Review of Financial Studies}, 29(1), 5--68.",
        ],
        target_pages=65,
        qa=[
            {"question": "What is the GRS statistic for FF5 on 25 size-BM portfolios?", "answer": "1.18 with p-value 0.276 (not rejected at 5% level)"},
            {"question": "Does FF5 explain momentum?", "answer": "No, Winner and Loser portfolios have FF5 alphas of +0.74 and -0.74 percent per month respectively"},
            {"question": "What is the mean monthly excess market return over the sample?", "answer": "0.64 percent"},
        ],
    )


PAPER_BUILDERS["08"] = _paper_08_finance
