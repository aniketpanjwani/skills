#!/usr/bin/env python3
"""Paper builder for paper 19 (Inequality -- Piketty-Saez top income shares style)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)


def _paper_19_inequality() -> PaperSpec:
    """Paper 19: Inequality -- top income shares, Piketty-Saez style."""

    # ── Tables ──

    tab_tax_summary = render_regression_table({
        "table_id": "tax-data-summary",
        "caption": "Tax Return Data Summary Statistics, Selected Years",
        "label": "tab:tax-data-summary",
        "model_labels": ["1940", "1960", "1980", "2000", "2019"],
        "panels": [
            {
                "variables": [
                    {"label": "Total tax units (millions)",
                     "coefficients": ["42.7", "58.3", "93.1", "127.4", "155.8"]},
                    {"label": "Mean AGI (2019 \\$000s)",
                     "coefficients": ["18.4", "29.7", "48.2", "72.1", "89.4"]},
                    {"label": "Median AGI (2019 \\$000s)",
                     "coefficients": ["11.2", "21.4", "36.8", "48.3", "54.7"]},
                    {"label": "Top 1\\% threshold (2019 \\$000s)",
                     "coefficients": ["241.3", "318.7", "412.4", "723.8", "981.4"]},
                    {"label": "Top 0.1\\% threshold (2019 \\$000s)",
                     "coefficients": ["1,124", "1,418", "1,874", "3,982", "6,241"]},
                    {"label": "Fraction with wage income (\\%)",
                     "coefficients": ["68.4", "74.2", "82.1", "79.4", "76.8"]},
                    {"label": "Fraction with capital income (\\%)",
                     "coefficients": ["31.8", "28.4", "24.7", "29.1", "31.4"]},
                ],
            },
        ],
        "notes": "All dollar amounts deflated to 2019 dollars using the CPI-U-RS. Tax units defined following Piketty and Saez (2003): married couples filing jointly count as one tax unit; unmarried individuals count separately. Sample excludes dependent returns.",
        "qa": [
            {"question": "How many tax units were there in 2019?", "answer": "155.8 million"},
            {"question": "What was the top 1% AGI threshold in 2019?", "answer": "$981,400 (2019 dollars)"},
        ],
    })

    tab_top01_decade = render_regression_table({
        "table_id": "top-01-shares-by-decade",
        "caption": "Top 0.1\\% Income Shares by Decade, 1920-2020 (\\%)",
        "label": "tab:top-01-shares-by-decade",
        "model_labels": ["1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s"],
        "panels": [
            {
                "variables": [
                    {"label": "Top 0.1\\% share (all income)",
                     "coefficients": ["8.41", "6.28", "4.12", "3.74", "3.41", "3.18", "4.87", "6.21", "7.84", "8.12"]},
                    {"label": "Top 0.1\\% share (excl. cap. gains)",
                     "coefficients": ["7.84", "5.91", "3.88", "3.52", "3.22", "3.01", "4.41", "5.74", "6.87", "7.41"]},
                    {"label": "Wage component",
                     "coefficients": ["2.14", "1.84", "1.42", "1.21", "1.31", "1.38", "2.12", "2.84", "3.41", "4.02"]},
                    {"label": "Capital income component",
                     "coefficients": ["5.12", "3.81", "2.18", "2.11", "1.84", "1.48", "2.18", "2.74", "3.84", "3.71"]},
                    {"label": "Business income component",
                     "coefficients": ["1.15", "0.63", "0.52", "0.41", "0.26", "0.32", "0.57", "0.63", "0.59", "0.68"]},
                ],
            },
        ],
        "notes": "Decade averages of annual estimates. All income shares expressed as percentage of total personal income. Capital gains included at realization; estimates excluding capital gains also reported. Source: IRS Statistics of Income, authors' calculations.",
        "qa": [
            {"question": "What was the top 0.1% share in the 1920s?", "answer": "8.41%"},
            {"question": "When was the top 0.1% share at its lowest?", "answer": "The 1970s (3.18%)"},
        ],
    })

    tab_top1_decade = render_regression_table({
        "table_id": "top-1-shares-by-decade",
        "caption": "Top 1\\% Income Shares by Decade, 1920-2020 (\\%)",
        "label": "tab:top-1-shares-by-decade",
        "model_labels": ["1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s"],
        "panels": [
            {
                "variables": [
                    {"label": "Top 1\\% share (all income)",
                     "coefficients": ["18.42", "14.87", "11.28", "10.84", "10.41", "9.87", "12.34", "15.84", "17.41", "18.74"]},
                    {"label": "Top 1\\% share (excl. cap. gains)",
                     "coefficients": ["17.14", "13.91", "10.84", "10.41", "9.98", "9.48", "11.47", "14.21", "15.48", "17.18"]},
                    {"label": "Wage component",
                     "coefficients": ["5.84", "4.91", "4.12", "3.84", "3.74", "3.91", "5.41", "7.84", "8.42", "9.71"]},
                    {"label": "Capital income component",
                     "coefficients": ["10.14", "7.81", "5.48", "5.12", "4.81", "4.12", "5.18", "5.84", "6.48", "6.21"]},
                    {"label": "Business income component",
                     "coefficients": ["2.44", "2.15", "1.68", "1.88", "1.86", "1.84", "1.75", "2.16", "2.51", "2.82"]},
                ],
            },
        ],
        "notes": "Decade averages. See notes to Table~\\ref{tab:top-01-shares-by-decade}.",
        "qa": [
            {"question": "What was the top 1% income share in the 2010s?", "answer": "18.74%"},
            {"question": "What was the top 1% share in the 1970s (the low point)?", "answer": "9.87%"},
        ],
    })

    tab_top10_decade = render_regression_table({
        "table_id": "top-10-shares-by-decade",
        "caption": "Top 10\\% Income Shares by Decade, 1920-2020 (\\%)",
        "label": "tab:top-10-shares-by-decade",
        "model_labels": ["1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s"],
        "panels": [
            {
                "variables": [
                    {"label": "Top 10\\% share (all income)",
                     "coefficients": ["43.84", "40.12", "35.74", "33.48", "32.84", "32.14", "38.41", "42.18", "46.84", "47.21"]},
                    {"label": "Top 10\\% share (excl. cap. gains)",
                     "coefficients": ["42.14", "38.84", "34.91", "32.74", "32.14", "31.48", "37.14", "40.84", "44.41", "45.84"]},
                    {"label": "P90-P99 (next 9\\%)",
                     "coefficients": ["25.42", "25.25", "24.46", "22.64", "22.43", "22.27", "26.07", "26.34", "29.43", "28.47"]},
                    {"label": "P99-P99.9 (next 0.9\\%)",
                     "coefficients": ["9.48", "8.42", "7.68", "6.84", "6.74", "6.47", "7.41", "8.74", "9.84", "9.94"]},
                ],
            },
        ],
        "notes": "Decade averages. P90-P99 is the income share of the 90th-99th percentile group.",
        "qa": [
            {"question": "What was the top 10% income share in the 2010s?", "answer": "47.21%"},
            {"question": "What fraction of the top 10% share belongs to the top 1%?", "answer": "Approximately 39.7% (18.74/47.21) in the 2010s"},
        ],
    })

    tab_comp_wages = render_regression_table({
        "table_id": "composition-wages-vs-capital",
        "caption": "Composition of Top Incomes: Wages vs. Capital, Selected Years",
        "label": "tab:composition-wages-vs-capital",
        "model_labels": ["1950", "1970", "1990", "2005", "2019"],
        "panels": [
            {
                "label": "Panel A: Top 1\\% income shares by source (\\%)",
                "variables": [
                    {"label": "Wages and salaries",
                     "coefficients": ["38.4", "42.1", "47.8", "52.4", "54.8"]},
                    {"label": "Dividends",
                     "coefficients": ["24.1", "18.4", "12.8", "9.4", "8.7"]},
                    {"label": "Interest",
                     "coefficients": ["14.8", "12.1", "9.4", "6.2", "4.8"]},
                    {"label": "Business income",
                     "coefficients": ["14.2", "17.4", "19.8", "21.4", "22.1"]},
                    {"label": "Capital gains",
                     "coefficients": ["8.5", "10.0", "10.2", "10.6", "9.6"]},
                ],
            },
            {
                "label": "Panel B: Capital share of top 0.1\\% income (\\%)",
                "variables": [
                    {"label": "Capital income (dividends + interest + realized CG)",
                     "coefficients": ["68.4", "62.1", "53.8", "46.2", "44.1"]},
                    {"label": "Labor income (wages + business income share)",
                     "coefficients": ["31.6", "37.9", "46.2", "53.8", "55.9"]},
                ],
            },
        ],
        "notes": "Capital income includes dividends, interest, rent, and realized capital gains. Business income split between labor and capital components following Piketty-Saez (2003) adjustment. Percentages within each year sum to 100.",
        "qa": [
            {"question": "Has the labor income share of the top 1% increased or decreased since 1950?", "answer": "Increased: from 38.4% in 1950 to 54.8% in 2019"},
            {"question": "What happened to the dividend share of top 1% income from 1950 to 2019?", "answer": "Declined substantially, from 24.1% to 8.7%"},
        ],
    })

    tab_comp_pctile = render_regression_table({
        "table_id": "composition-by-percentile",
        "caption": "Income Composition by Percentile Group, 2019",
        "label": "tab:composition-by-percentile",
        "model_labels": ["P90-P95", "P95-P99", "P99-P99.5", "P99.5-P99.9", "Top 0.1\\%"],
        "panels": [
            {
                "variables": [
                    {"label": "Wages and salaries (\\%)",
                     "coefficients": ["73.4", "66.8", "62.1", "57.4", "34.8"]},
                    {"label": "Business income (\\%)",
                     "coefficients": ["14.2", "17.4", "21.8", "24.4", "28.1"]},
                    {"label": "Capital gains (\\%)",
                     "coefficients": ["4.8", "6.4", "7.4", "9.1", "21.4"]},
                    {"label": "Dividends (\\%)",
                     "coefficients": ["4.2", "5.8", "5.9", "6.4", "12.2"]},
                    {"label": "Interest (\\%)",
                     "coefficients": ["3.4", "3.6", "2.8", "2.7", "3.5"]},
                    {"label": "Mean income (2019 \\$000s)",
                     "coefficients": ["128.4", "208.7", "342.1", "621.4", "5,218"]},
                ],
            },
        ],
        "notes": "2019 data from IRS Statistics of Income. Percentages within each column sum to 100. All income includes realized capital gains.",
        "qa": [
            {"question": "What was the mean income of the top 0.1% in 2019?", "answer": "$5.218 million"},
            {"question": "How does wage share vary across the top of the distribution?", "answer": "Decreasing: 73.4% at P90-P95 to 34.8% at the top 0.1%"},
        ],
    })

    tab_cross_country = render_regression_table({
        "table_id": "cross-country-comparison",
        "caption": "Cross-Country Comparison of Top 1\\% Income Shares (\\%)",
        "label": "tab:cross-country-comparison",
        "model_labels": ["United States", "United Kingdom", "France", "Japan", "Sweden"],
        "panels": [
            {
                "variables": [
                    {"label": "1950", "coefficients": ["10.8", "11.7", "11.4", "11.2", "9.2"]},
                    {"label": "1960", "coefficients": ["10.4", "10.8", "10.8", "9.8", "8.4"]},
                    {"label": "1970", "coefficients": ["9.9", "9.4", "9.1", "8.6", "7.4"]},
                    {"label": "1980", "coefficients": ["10.0", "8.4", "8.2", "7.8", "6.4"]},
                    {"label": "1990", "coefficients": ["13.1", "10.7", "8.4", "8.9", "6.8"]},
                    {"label": "2000", "coefficients": ["16.5", "12.8", "8.7", "9.2", "7.1"]},
                    {"label": "2010", "coefficients": ["17.4", "13.4", "8.2", "9.4", "7.8"]},
                    {"label": "2019", "coefficients": ["18.8", "14.1", "8.8", "10.4", "8.4"]},
                ],
            },
        ],
        "notes": "Data from the World Inequality Database (WID). Top 1\\% share of pre-tax national income. For Japan: fiscal income concept. Country series cover varying periods; earlier estimates involve larger interpolation uncertainty.",
        "qa": [
            {"question": "Which country had the highest top 1% share in 2019?", "answer": "United States (18.8%)"},
            {"question": "Which country has the lowest top 1% share throughout the sample?", "answer": "Sweden, with shares consistently below 9%"},
        ],
    })

    tab_gini = render_regression_table({
        "table_id": "gini-coefficient-time-series",
        "caption": "Gini Coefficient Time Series, United States, 1913-2019",
        "label": "tab:gini-coefficient-time-series",
        "model_labels": ["1920", "1940", "1960", "1980", "2000", "2019"],
        "panels": [
            {
                "variables": [
                    {"label": "Gini (pre-tax income)",
                     "coefficients": ["0.532", "0.481", "0.448", "0.462", "0.531", "0.582"]},
                    {"label": "Gini (post-tax income)",
                     "coefficients": ["0.481", "0.421", "0.381", "0.388", "0.448", "0.494"]},
                    {"label": "Gini (consumption)",
                     "coefficients": ["0.441", "0.381", "0.348", "0.352", "0.388", "0.412"]},
                    {"label": "Gini (wealth)",
                     "coefficients": ["0.814", "0.781", "0.748", "0.748", "0.821", "0.869"]},
                    {"label": "Top 10\\% share (ref.)",
                     "coefficients": ["43.8", "40.1", "32.8", "32.1", "46.8", "47.2"]},
                ],
            },
        ],
        "notes": "Pre-tax Gini computed from tax return microdata using Pareto interpolation. Post-tax Gini adjusts for federal income and payroll taxes. Consumption Gini from CEX/PCE. Wealth Gini from SCF and estate tax records.",
        "qa": [
            {"question": "What was the pre-tax Gini coefficient in 2019?", "answer": "0.582"},
            {"question": "Is wealth more unequally distributed than income?", "answer": "Yes, the wealth Gini (0.869) is substantially higher than the income Gini (0.582) in 2019"},
        ],
    })

    tab_pareto = render_regression_table({
        "table_id": "pareto-coefficients-by-year",
        "caption": "Pareto Coefficients at the Top of the Income Distribution, Selected Years",
        "label": "tab:pareto-coefficients-by-year",
        "model_labels": ["Top 1\\% threshold", "Top 0.5\\% threshold", "Top 0.1\\% threshold", "Top 0.01\\% threshold"],
        "panels": [
            {
                "variables": [
                    {"label": "1929 (Pareto alpha)",
                     "coefficients": ["1.714", "1.624", "1.512", "1.387"]},
                    {"label": "1950 (Pareto alpha)",
                     "coefficients": ["2.142", "2.084", "2.018", "1.948"]},
                    {"label": "1970 (Pareto alpha)",
                     "coefficients": ["2.381", "2.314", "2.247", "2.182"]},
                    {"label": "1990 (Pareto alpha)",
                     "coefficients": ["1.987", "1.924", "1.847", "1.771"]},
                    {"label": "2010 (Pareto alpha)",
                     "coefficients": ["1.748", "1.684", "1.601", "1.524"]},
                    {"label": "2019 (Pareto alpha)",
                     "coefficients": ["1.692", "1.628", "1.549", "1.471"]},
                ],
            },
        ],
        "notes": "Pareto coefficient alpha estimated from the Hill estimator applied to tax return microdata. Lower alpha indicates heavier tails (higher inequality). Estimates above 2 are consistent with finite variance; below 2, the distribution has infinite variance.",
        "qa": [
            {"question": "What does a lower Pareto alpha indicate?", "answer": "Heavier tails and greater inequality at the top"},
            {"question": "Is the 2019 Pareto alpha above or below 2?", "answer": "Below 2 (1.692 at the top 1% threshold), indicating potentially infinite variance"},
        ],
    })

    tab_wealth_income = render_regression_table({
        "table_id": "wealth-vs-income-top-shares",
        "caption": "Wealth vs. Income Top Shares: United States, 1913-2019",
        "label": "tab:wealth-vs-income-top-shares",
        "model_labels": ["1929", "1950", "1970", "1990", "2007", "2019"],
        "panels": [
            {
                "label": "Panel A: Top 1\\% shares (\\%)",
                "variables": [
                    {"label": "Wealth share", "coefficients": ["44.8", "28.4", "24.1", "29.8", "34.2", "38.1"]},
                    {"label": "Income share", "coefficients": ["19.6", "10.8", "9.9", "13.1", "18.4", "18.8"]},
                    {"label": "Wealth-to-income ratio", "coefficients": ["2.29", "2.63", "2.43", "2.27", "1.86", "2.03"]},
                ],
            },
            {
                "label": "Panel B: Top 0.1\\% shares (\\%)",
                "variables": [
                    {"label": "Wealth share", "coefficients": ["22.4", "10.4", "7.8", "12.8", "18.1", "19.4"]},
                    {"label": "Income share", "coefficients": ["8.4", "4.1", "3.2", "4.9", "7.8", "8.1"]},
                    {"label": "Wealth-to-income ratio", "coefficients": ["2.67", "2.54", "2.44", "2.61", "2.32", "2.40"]},
                ],
            },
        ],
        "notes": "Wealth data from SCF, estate multiplier estimates, and Saez-Zucman (2016) capitalization method. Income data from IRS SOI. Wealth-to-income ratios are cross-sectional ratios of shares, not individual-level wealth-to-income.",
        "qa": [
            {"question": "What was the top 1% wealth share in 2019?", "answer": "38.1%"},
            {"question": "Is wealth more concentrated than income at the top?", "answer": "Yes, top 1% wealth share (38.1%) exceeds income share (18.8%) in 2019"},
        ],
    })

    tab_gender = render_regression_table({
        "table_id": "gender-decomposition",
        "caption": "Gender Decomposition of Top Income Shares, United States",
        "label": "tab:gender-decomposition",
        "model_labels": ["1980", "1990", "2000", "2010", "2019"],
        "panels": [
            {
                "label": "Panel A: Women's share of top income groups (\\%)",
                "variables": [
                    {"label": "P90-P99", "coefficients": ["14.8", "18.4", "22.1", "27.4", "31.8"]},
                    {"label": "Top 1\\%", "coefficients": ["8.4", "10.8", "13.4", "17.8", "21.4"]},
                    {"label": "Top 0.1\\%", "coefficients": ["4.8", "6.2", "7.8", "10.4", "13.1"]},
                    {"label": "Top 0.01\\%", "coefficients": ["3.2", "4.1", "5.4", "7.2", "9.8"]},
                ],
            },
        ],
        "notes": "Fraction of total income in each group earned by female tax filers. Married couples allocated 50/50 following Piketty-Saez convention. Female share of total income = 39.8\\% in 2019.",
        "qa": [
            {"question": "What share of top 0.1% income did women earn in 2019?", "answer": "13.1%"},
            {"question": "Has women's representation at the top grown over time?", "answer": "Yes, consistently increasing at all percentile groups from 1980 to 2019"},
        ],
    })

    tab_industry = render_regression_table({
        "table_id": "industry-decomposition",
        "caption": "Industry Decomposition of Top 1\\% Income, 2000 and 2019 (\\%)",
        "label": "tab:industry-decomposition",
        "model_labels": ["2000 share", "2019 share", "Change", "Relative to econ. share"],
        "panels": [
            {
                "variables": [
                    {"label": "Finance and insurance",
                     "coefficients": ["22.4", "24.1", "1.7", "3.8"]},
                    {"label": "Technology / information",
                     "coefficients": ["12.8", "18.4", "5.6", "3.2"]},
                    {"label": "Healthcare",
                     "coefficients": ["9.4", "11.2", "1.8", "1.4"]},
                    {"label": "Real estate",
                     "coefficients": ["7.8", "8.4", "0.6", "1.6"]},
                    {"label": "Manufacturing",
                     "coefficients": ["11.4", "7.8", "-3.6", "0.9"]},
                    {"label": "Retail and wholesale",
                     "coefficients": ["5.8", "4.2", "-1.6", "0.6"]},
                    {"label": "Other",
                     "coefficients": ["30.4", "25.9", "-4.5", "--"]},
                ],
            },
        ],
        "notes": "Share of top 1\\% income by industry of the primary employer (or of self-employment activity for business income). Relative to economic share = top 1\\% industry share divided by that industry's share of total GDP.",
        "qa": [
            {"question": "Which sector has the highest representation in the top 1% in 2019?", "answer": "Finance and insurance (24.1%)"},
            {"question": "Which sector grew most in top 1% share from 2000 to 2019?", "answer": "Technology/information, rising 5.6 percentage points"},
        ],
    })

    tab_tax_rate = render_regression_table({
        "table_id": "tax-rate-changes",
        "caption": "Average Effective Tax Rates by Income Group, Selected Years (\\%)",
        "label": "tab:tax-rate-changes",
        "model_labels": ["1960", "1980", "2000", "2010", "2019"],
        "panels": [
            {
                "variables": [
                    {"label": "Bottom 50\\%",
                     "coefficients": ["15.8", "19.4", "17.2", "15.4", "14.8"]},
                    {"label": "P50-P90",
                     "coefficients": ["22.4", "28.1", "26.4", "22.8", "22.1"]},
                    {"label": "P90-P99",
                     "coefficients": ["31.2", "37.4", "32.1", "28.4", "27.8"]},
                    {"label": "Top 1\\%",
                     "coefficients": ["51.4", "42.1", "34.8", "29.4", "28.1"]},
                    {"label": "Top 0.1\\%",
                     "coefficients": ["62.8", "48.4", "38.4", "32.1", "30.4"]},
                    {"label": "Top 0.01\\%",
                     "coefficients": ["71.4", "51.2", "40.1", "33.8", "31.2"]},
                ],
            },
        ],
        "notes": "Average effective federal income tax rate including payroll taxes. Capital gains taxed at realization. Does not include state and local taxes. 2019 estimates for top groups subject to greater uncertainty due to pass-through income measurement.",
        "qa": [
            {"question": "What was the top 0.01% effective tax rate in 1960?", "answer": "71.4%"},
            {"question": "How much has the top 0.1% effective tax rate changed from 1960 to 2019?", "answer": "Declined from 62.8% to 30.4%, a reduction of 32.4 percentage points"},
        ],
    })

    tab_agi = render_regression_table({
        "table_id": "agi-adjustments",
        "caption": "AGI Adjustments: Effect of Including Excluded Income Sources",
        "label": "tab:agi-adjustments",
        "model_labels": ["Baseline AGI", "+Unrealized CG", "+Retained earnings", "+Transfer income", "Comprehensive"],
        "panels": [
            {
                "label": "Top 1\\% share under alternative income definitions (\\%)",
                "variables": [
                    {"label": "2000", "coefficients": ["16.5", "18.4", "19.8", "14.8", "21.4"]},
                    {"label": "2010", "coefficients": ["17.4", "19.8", "21.4", "15.8", "22.8"]},
                    {"label": "2019", "coefficients": ["18.8", "22.1", "24.4", "16.4", "25.1"]},
                ],
            },
        ],
        "notes": "Baseline = realized income as reported on tax returns. +Unrealized CG imputes unrealized capital gains using changes in portfolio values from Fed Flow of Funds. +Retained earnings imputes corporate retained earnings. +Transfer income adds SNAP, Medicaid, and other transfers (which mainly benefit lower-income groups and reduce measured top shares).",
        "qa": [
            {"question": "What is the top 1% share under the comprehensive income definition in 2019?", "answer": "25.1%"},
            {"question": "Does including transfer income increase or decrease the top 1% share?", "answer": "Decrease: from 18.8% baseline to 16.4% with transfers, as transfers mainly benefit lower-income groups"},
        ],
    })

    tab_cg = render_regression_table({
        "table_id": "capital-gains-inclusion",
        "caption": "Effect of Capital Gains on Top Income Shares",
        "label": "tab:capital-gains-inclusion",
        "model_labels": ["Excl. CG", "Realized CG", "Realized+Unrealized", "Mark-to-market"],
        "panels": [
            {
                "label": "Top 1\\% share (\\%)",
                "variables": [
                    {"label": "2000", "coefficients": ["15.5", "16.5", "18.4", "19.1"]},
                    {"label": "2007", "coefficients": ["17.4", "18.4", "21.4", "22.8"]},
                    {"label": "2010", "coefficients": ["16.1", "17.4", "19.8", "20.2"]},
                    {"label": "2019", "coefficients": ["17.2", "18.8", "22.1", "23.4"]},
                ],
            },
        ],
        "notes": "Mark-to-market treatment taxes all capital gains and losses as they accrue. Unrealized CG imputed from portfolio value changes. CG timing creates bunching in realized CG series (visible 2007 spike).",
        "qa": [
            {"question": "How much higher is the top 1% share under mark-to-market vs excluding capital gains in 2019?", "answer": "6.2 percentage points higher (23.4% vs 17.2%)"},
            {"question": "Why is 2007 an outlier in the realized CG series?", "answer": "High realized capital gains in 2007 before the financial crisis created a spike in top income shares"},
        ],
    })

    tab_estate = render_regression_table({
        "table_id": "estate-tax-data",
        "caption": "Estate Tax Returns: Wealth Concentration Estimates",
        "label": "tab:estate-tax-data",
        "model_labels": ["1960", "1980", "2000", "2010", "2019"],
        "panels": [
            {
                "variables": [
                    {"label": "Number of taxable estates (000s)",
                     "coefficients": ["71.4", "139.8", "52.4", "15.2", "40.8"]},
                    {"label": "Mean net estate (2019 \\$M)",
                     "coefficients": ["2.84", "3.14", "7.21", "8.84", "9.41"]},
                    {"label": "Top 0.1\\% wealth share (\\%)",
                     "coefficients": ["8.4", "7.8", "10.4", "12.8", "13.4"]},
                    {"label": "Estate multiplier (estates / deaths)",
                     "coefficients": ["2.14", "1.98", "3.41", "7.84", "6.24"]},
                    {"label": "Effective estate tax rate (\\%)",
                     "coefficients": ["18.4", "24.1", "28.4", "14.8", "16.2"]},
                ],
            },
        ],
        "notes": "Estate multiplier = inverse mortality rate for filing age-sex group. Sharp drop in taxable estates after 2001 EGTRRA tax cuts raised the filing threshold from \\$675k to \\$1M (2002) then to \\$5M (2011). 2019 estimates based on \\$11.4M filing threshold.",
        "qa": [
            {"question": "Why did the number of taxable estates fall sharply from 2000 to 2010?", "answer": "The 2001 EGTRRA raised the filing threshold from $675k to $1M then to $5M, removing most estates"},
            {"question": "What was the top 0.1% wealth share estimated from estate tax data in 2019?", "answer": "13.4%"},
        ],
    })

    tab_app_tax_units = render_regression_table({
        "table_id": "appendix-tax-units",
        "caption": "Appendix: Tax Unit Adjustments for Changing Filing Patterns",
        "label": "tab:appendix-tax-units",
        "model_labels": ["1950", "1970", "1990", "2010", "2019"],
        "panels": [
            {
                "variables": [
                    {"label": "Married filing jointly (\\%)",
                     "coefficients": ["74.4", "71.2", "56.8", "51.4", "48.2"]},
                    {"label": "Single filers (\\%)",
                     "coefficients": ["21.4", "24.8", "37.4", "43.2", "46.8"]},
                    {"label": "Head of household (\\%)",
                     "coefficients": ["4.2", "4.0", "5.8", "5.4", "5.0"]},
                    {"label": "Adjustment factor (MFJ = 1.0)",
                     "coefficients": ["1.00", "1.00", "1.00", "1.00", "1.00"]},
                    {"label": "Top 1\\% share (unadjusted, \\%)",
                     "coefficients": ["10.8", "9.9", "13.1", "17.4", "18.8"]},
                    {"label": "Top 1\\% share (adjusted for filing units, \\%)",
                     "coefficients": ["10.4", "9.7", "12.8", "17.1", "18.4"]},
                ],
            },
        ],
        "notes": "Adjustment for changing composition of filing units following Piketty-Saez (2003). Married couples always counted as one tax unit regardless of filing status. The adjustment is minor (<0.5 pp) in most years.",
        "qa": [
            {"question": "Has the fraction of married-filing-jointly returns changed since 1950?", "answer": "Yes, declined from 74.4% to 48.2%, reflecting rising rates of single filing"},
        ],
    })

    tab_deflators = render_regression_table({
        "table_id": "appendix-price-deflators",
        "caption": "Appendix: Price Deflators Used for Income Series",
        "label": "tab:appendix-price-deflators",
        "model_labels": ["CPI-U", "CPI-U-RS", "PCE deflator", "GDP deflator"],
        "panels": [
            {
                "variables": [
                    {"label": "Annualized growth 1950-2019 (\\%)",
                     "coefficients": ["3.82", "3.41", "3.28", "3.11"]},
                    {"label": "Annualized growth 1980-2019 (\\%)",
                     "coefficients": ["3.14", "2.87", "2.71", "2.58"]},
                    {"label": "Top 1\\% share 2019 (with deflator, \\%)",
                     "coefficients": ["18.8", "18.8", "18.9", "18.7"]},
                    {"label": "Mean income growth 1980-2019 (\\%)",
                     "coefficients": ["1.24", "1.51", "1.64", "1.77"]},
                ],
            },
        ],
        "notes": "All deflators rebased to 2019 = 100. CPI-U-RS is the research series that corrects for methodological improvements. Income shares are invariant to the choice of deflator (only nominal ratios matter). Deflator choice matters for real income growth rates.",
        "qa": [
            {"question": "Does the choice of price deflator affect estimated top income shares?", "answer": "No, income shares are ratios and are deflator-invariant (top 1% share ranges only 18.7-18.9% in 2019 across deflators)"},
        ],
    })

    # ── Main Equations ──
    eqs_19 = [
        EquationSpec("pareto-dist",
                     r"1 - F(y) = \left(\frac{y_{\min}}{y}\right)^\alpha, \quad y \geq y_{\min}, \; \alpha > 1",
                     "eq:pareto",
                     "Pareto distribution: upper tail probability for income above threshold y_min",
                     [{"question": "What is the Pareto distribution?",
                       "answer": "P(Y > y) = (y_min/y)^alpha for y >= y_min, where alpha > 1 is the Pareto coefficient"}]),
        EquationSpec("top-share-formula",
                     r"S(p) = \frac{\int_{Q(p)}^\infty y \, dF(y)}{\int_0^\infty y \, dF(y)} = 1 - L(p), \quad L(p) = \frac{1}{\mu}\int_0^p Q(u)\,du, \quad \frac{\partial L(p)}{\partial p} = \frac{Q(p)}{\mu}",
                     "eq:top-share",
                     "Top income share formula: mean income above p-th quantile times share of population",
                     [{"question": "How is the top p income share computed?",
                       "answer": "S(p) = mean income above the p-th quantile times (1-p), divided by overall mean income"}]),
        EquationSpec("gini-pareto",
                     r"G = 1 - 2\int_0^1 L(p)\,dp = \frac{1}{2\alpha - 1}, \quad \frac{\partial G}{\partial \alpha} = \frac{-2}{(2\alpha - 1)^2} < 0",
                     "eq:gini-pareto",
                     "Gini coefficient as a function of the Pareto alpha",
                     [{"question": "What is the Gini coefficient for a Pareto distribution with alpha = 2?",
                       "answer": "G = 1/(2*2-1) = 1/3 = 0.333"}]),
        EquationSpec("pareto-interpolation",
                     r"\hat{y}_p = y_k \left(\frac{n_k}{n_k - n \cdot p}\right)^{1/\hat{\alpha}_k}, \quad \hat{\alpha}_k = \frac{\ln(n_k/n_{k+1})}{\ln(y_{k+1}/y_k)}",
                     "eq:pareto-interp",
                     "Pareto interpolation between tax brackets to estimate quantile income",
                     [{"question": "What is the Pareto interpolation formula?",
                       "answer": "y_p = y_k * (n_k / (n_k - n*p))^{1/alpha_k}, where alpha_k is estimated from adjacent bracket counts and thresholds"}]),
        EquationSpec("capital-share-top",
                     r"\\kappa(p) = \\frac{\\int_{Q(p)}^\\infty y^K \\, dF(y)}{\\int_{Q(p)}^\\infty y \\, dF(y)}, \\quad \\frac{\\partial \\kappa(p)}{\\partial p} = \\frac{Q^K(p) - \\kappa(p) Q(p)}{\\int_{Q(p)}^\\infty y\\,dF(y)}",
                     "eq:capital-share-top",
                     "Capital income share within the top p percent group",
                     [{"question": "How is the capital share of top incomes defined?",
                       "answer": "kappa(p) = mean capital income above the p-th quantile divided by mean total income above the p-th quantile"}]),
    ]

    # ── Appendix math ──
    appendix_proofs_19 = r"""
\subsection*{B.1 Pareto Coefficient Estimation from Grouped Tax Data}

Given tabulated data with $K$ income brackets with thresholds $y_1 < y_2 < \cdots < y_K$ and counts $n_1 > n_2 > \cdots > n_K$ (number of returns above each threshold), the Pareto coefficient between brackets $k$ and $k+1$ is estimated by:
\begin{equation}
\hat{\alpha}_k = \frac{\ln(n_k/n_{k+1})}{\ln(y_{k+1}/y_k)}
\end{equation}
This follows directly from the Pareto survival function: $n_k/n = (y_{\min}/y_k)^\alpha$, so $\ln(n_k/n_{k+1}) = \alpha \ln(y_{k+1}/y_k)$.

\subsection*{B.2 Interpolation Method Derivation}

To estimate income at quantile $p$ when $Q(p)$ falls within bracket $k$ (i.e., $n_{k+1}/n < 1-p \leq n_k/n$):
\begin{align}
1 - F(y) &= \left(\frac{y_k}{y}\right)^{\hat{\alpha}_k} \cdot \frac{n_k}{n} \nonumber \\
\implies \hat{y}_p &= y_k \left(\frac{n_k/n}{1-p}\right)^{1/\hat{\alpha}_k}
\end{align}
The mean income above threshold $y_k$ under the Pareto assumption is:
\begin{equation}
E[Y \mid Y > y_k] = \frac{\hat{\alpha}_k}{\hat{\alpha}_k - 1} \cdot y_k \quad \text{(provided } \hat{\alpha}_k > 1\text{)}
\end{equation}

\subsection*{B.3 Adjustment for Tax Unit Changes}

When the fraction of married-filing-jointly (MFJ) returns changes from $m_0$ to $m_1$, the number of ``economic units'' changes. A two-adult MFJ household has income $y = y_1 + y_2$, while under separate filing it would appear as two units with incomes $y_1$ and $y_2$. The adjustment factor is:
\begin{equation}
\text{Adjusted top share}(p) = S(p) \times \frac{1 + (1-m_0)}{1 + (1-m_1)}
\end{equation}
where the correction is approximately $1 + O(m_1 - m_0)$ and is quantitatively small ($< 0.5$ pp) for the changes in MFJ rates observed in the data.

\subsection*{B.4 Relationship Between Pareto Alpha and Inequality}

The Pareto coefficient $\alpha$ is related to several standard inequality measures:
\begin{align}
\text{Top income share: } & S(p) = (1-p)^{1 - 1/\alpha} \\
\text{Gini coefficient: } & G = \frac{1}{2\alpha - 1} \\
\text{Theil T index: } & T = \frac{1}{\alpha - 1} - \ln\left(\frac{\alpha}{\alpha-1}\right) \\
\text{Mean-to-median ratio: } & \frac{\mu}{Q(0.5)} = \frac{\alpha}{\alpha-1} \cdot 2^{1/\alpha}
\end{align}
All of these are decreasing in $\alpha$: lower $\alpha$ means heavier tails and more inequality.

\subsection*{B.5 Lorenz Curve Integral and Gini Derivation}

The Lorenz curve for the Pareto distribution with parameter $\alpha > 1$ satisfies:
\begin{align}
L(p) &= \frac{1}{\mu}\int_0^p Q(u)\,du = 1 - (1-p)^{1-1/\alpha}, \quad \frac{\partial L}{\partial p} = \frac{Q(p)}{\mu} = \left(\frac{1-p}{1}\right)^{-1/\alpha}.
\end{align}
The Gini coefficient follows from the double integration:
\begin{align}
G = 1 - 2\int_0^1 L(p)\,dp = 1 - 2\int_0^1 \left[1 - (1-p)^{1-1/\alpha}\right]dp = \frac{1}{2\alpha - 1}.
\end{align}
The partial derivative $\frac{\partial G}{\partial \alpha} = -2(2\alpha - 1)^{-2} < 0$ confirms that higher $\alpha$ reduces inequality.
"""

    proof_block_19 = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proofs_19,
    )

    # ── Appendix equations ──
    eqs_appendix_19 = [
        EquationSpec("pareto-est-19",
                     r"\hat{\alpha}_k = \frac{\ln(n_k / n_{k+1})}{\ln(y_{k+1} / y_k)}",
                     "eq:pareto-est-19", "Pareto coefficient estimation from adjacent bracket counts"),
        EquationSpec("pareto-mean-19",
                     r"E[Y \mid Y > y_k] = \frac{\hat{\alpha}_k}{\hat{\alpha}_k - 1} \cdot y_k",
                     "eq:pareto-mean-19", "Mean income above threshold under Pareto assumption"),
        EquationSpec("gini-theil-19",
                     r"G = \frac{1}{2\alpha-1}, \quad T = \frac{1}{\alpha-1} - \ln\!\left(\frac{\alpha}{\alpha-1}\right)",
                     "eq:gini-theil-19", "Gini and Theil inequality measures as functions of Pareto alpha"),
    ]

    # ── Sections ──
    sections_19 = [
        SectionSpec("Introduction", "sec:intro-19", text_paragraphs=18),
        SectionSpec("Literature and Context", "sec:lit-19", text_paragraphs=16),
        SectionSpec("Tax Data and Methodology", "sec:data-19", text_paragraphs=18,
                    tables=[tab_tax_summary],
                    subsections=[
                        SectionSpec("IRS Statistics of Income Data", "sec:irs-19", level=2,
                                    text_paragraphs=14),
                        SectionSpec("Tax Unit Definitions and Adjustments", "sec:tax-units-19", level=2,
                                    text_paragraphs=12, tables=[tab_app_tax_units]),
                        SectionSpec("Pareto Interpolation Method", "sec:pareto-method-19", level=2,
                                    text_paragraphs=14, equations=[eqs_19[3]]),
                        SectionSpec("Income Concepts and Capital Gains", "sec:income-concepts-19", level=2,
                                    text_paragraphs=12, tables=[tab_cg, tab_agi]),
                    ]),
        SectionSpec("Top Income Shares: 1913-2020", "sec:shares-19", text_paragraphs=18,
                    equations=[eqs_19[0], eqs_19[1]],
                    tables=[tab_top01_decade, tab_top1_decade],
                    subsections=[
                        SectionSpec("Long-Run Trends in the Top 0.1\\%", "sec:top01-19", level=2,
                                    text_paragraphs=14),
                        SectionSpec("The Top 1\\% and Top 10\\%", "sec:top1-10-19", level=2,
                                    text_paragraphs=14, tables=[tab_top10_decade]),
                        SectionSpec("Pareto Coefficients Over Time", "sec:pareto-time-19", level=2,
                                    text_paragraphs=12, equations=[eqs_19[2]], tables=[tab_pareto]),
                        SectionSpec("Comparison with Survey-Based Measures", "sec:survey-19", level=2,
                                    text_paragraphs=12, tables=[tab_gini]),
                    ]),
        SectionSpec("Composition of Top Incomes", "sec:composition-19", text_paragraphs=15,
                    equations=[eqs_19[4]],
                    tables=[tab_comp_wages, tab_comp_pctile],
                    subsections=[
                        SectionSpec("The Rise of Working Rich", "sec:working-rich-19", level=2,
                                    text_paragraphs=13),
                        SectionSpec("Capital Income at the Very Top", "sec:capital-top-19", level=2,
                                    text_paragraphs=11),
                        SectionSpec("Heterogeneity by Gender and Industry", "sec:gender-ind-19", level=2,
                                    text_paragraphs=11, tables=[tab_gender, tab_industry]),
                    ]),
        SectionSpec("International Comparison", "sec:intl-19", text_paragraphs=15,
                    tables=[tab_cross_country],
                    subsections=[
                        SectionSpec("Anglo-Saxon vs. Continental Europe", "sec:anglosaxon-19", level=2,
                                    text_paragraphs=13),
                        SectionSpec("Institutional Drivers of Cross-Country Differences", "sec:institutions-19", level=2,
                                    text_paragraphs=10),
                    ]),
        SectionSpec("Mechanisms", "sec:mechanisms-19", text_paragraphs=12,
                    tables=[tab_tax_rate],
                    subsections=[
                        SectionSpec("Tax Policy and Behavioral Responses", "sec:tax-policy-19", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Capital Accumulation and r > g", "sec:r-g-19", level=2,
                                    text_paragraphs=10, tables=[tab_wealth_income]),
                    ]),
        SectionSpec("Conclusion", "sec:conclusion-19", text_paragraphs=10),
        SectionSpec("Appendix A: Data Construction", "sec:appendix-a-19", text_paragraphs=10,
                    tables=[tab_deflators, tab_estate]),
        SectionSpec("Appendix B: Pareto Methods", "sec:appendix-b-19", text_paragraphs=8,
                    equations=eqs_appendix_19),
        SectionSpec("Appendix C: Additional Tables", "sec:appendix-c-19", text_paragraphs=6),
        SectionSpec("Appendix D: Price Adjustments", "sec:appendix-d-19", text_paragraphs=6),
    ]

    # inject proof block into Appendix B
    sections_19[9].tables.append(proof_block_19)

    bib_19 = [
        r"\bibitem{piketty2003} Piketty, T. and E. Saez (2003). ``Income Inequality in the United States, 1913--1998.'' \textit{Quarterly Journal of Economics}, 118(1), 1--41.",
        r"\bibitem{piketty2014} Piketty, T. (2014). \textit{Capital in the Twenty-First Century}. Harvard University Press.",
        r"\bibitem{saez2016} Saez, E. and G. Zucman (2016). ``Wealth Inequality in the United States Since 1913: Evidence from Capitalized Income Tax Data.'' \textit{Quarterly Journal of Economics}, 131(2), 519--578.",
        r"\bibitem{atkinson2011} Atkinson, A.B., T. Piketty, and E. Saez (2011). ``Top Incomes in the Long Run of History.'' \textit{Journal of Economic Literature}, 49(1), 3--71.",
        r"\bibitem{kopczuk2010} Kopczuk, W. and E. Saez (2004). ``Top Wealth Shares in the United States, 1916--2000.'' \textit{National Tax Journal}, 57(2), 445--487.",
        r"\bibitem{goldin2010} Goldin, C. and L.F. Katz (2008). \textit{The Race between Education and Technology}. Harvard University Press.",
        r"\bibitem{kaplan2013} Kaplan, S.N. and J. Rauh (2013). ``It's the Market: The Broad-Based Rise in the Return to Top Talent.'' \textit{Journal of Economic Perspectives}, 27(3), 35--56.",
        r"\bibitem{wid} World Inequality Database (2023). \textit{WID.world}. Available at: \url{https://wid.world}.",
    ]

    return PaperSpec(
        paper_id="19",
        field_slug="inequality",
        title="Top Income Shares in the United States, 1913-2020: New Evidence from Tax Records",
        authors="Miriam Okonkwo \\and Stefan Bergmann \\and Yuki Takahashi",
        journal_style="two_column",
        abstract=(
            "We construct new estimates of top income shares in the United States from 1913 to 2020 "
            "using a comprehensive database of IRS Statistics of Income tabulations. The top 1 percent "
            "income share peaked at 19.6 percent in 1928, fell to 9.9 percent by 1970, and has "
            "subsequently rebounded to 18.8 percent in 2019. The top 0.1 percent share exhibits "
            "even more dramatic variation: from 8.4 percent in the 1920s, to a low of 3.2 percent "
            "in 1970, to 8.1 percent by 2019. We document a striking compositional shift: "
            "whereas the top incomes of the 1950s and 1960s were dominated by capital income "
            "(dividends, interest), the top incomes of the 2010s are driven primarily by wages "
            "and salaries, reflecting the rise of the working rich. Cross-country comparisons "
            "show the United States has experienced the largest increase in inequality among "
            "major economies since 1980, with the Pareto coefficient declining from 2.38 in "
            "1970 to 1.69 in 2019. Concurrent sharp reductions in top marginal tax rates "
            "account for a substantial fraction of the rise in top income shares."
        ),
        sections=sections_19,
        bibliography_entries=bib_19,
        target_pages=80,
        qa=[
            {"question": "What was the top 1% income share in 2019?",
             "answer": "18.8%"},
            {"question": "When was the top 0.1% income share at its lowest?",
             "answer": "The 1970s, at 3.18%"},
            {"question": "What compositional shift has occurred in top incomes since the 1950s?",
             "answer": "A shift from capital income (dividends, interest) to wage and salary income -- the rise of the working rich"},
            {"question": "What has happened to the Pareto alpha since 1970?",
             "answer": "Declined from 2.381 in 1970 to 1.692 in 2019, indicating heavier tails and more inequality"},
            {"question": "What is the top 0.1% wealth share in 2019?",
             "answer": "19.4%"},
        ],
    )


PAPER_BUILDERS["19"] = _paper_19_inequality
