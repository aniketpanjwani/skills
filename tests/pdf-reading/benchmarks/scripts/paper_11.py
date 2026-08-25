#!/usr/bin/env python3
"""Paper builder for paper 11 (Education Economics)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)


# ═══════════════════════════════════════════════════════════════════════════
# Paper 11: Education Economics — Teacher Value-Added and Student Outcomes
# ═══════════════════════════════════════════════════════════════════════════

def _paper_11_education() -> PaperSpec:
    """Paper 11: Education Economics — teacher quality, class size, long-run outcomes."""

    # ── Tables ──
    summary_stats = render_regression_table({
        "table_id": "summary-stats",
        "caption": "Summary Statistics",
        "label": "tab:summary-stats",
        "model_labels": ["Mean", "SD", "Min", "Max", "N"],
        "panels": [{
            "dep_var": "Panel A: Student Characteristics",
            "variables": [
                {"label": "Math test score (standardized)", "coefficients": ["0.00", "1.00", "-3.42", "3.18", "2,541,918"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Reading test score (standardized)", "coefficients": ["0.00", "1.00", "-3.28", "3.54", "2,541,918"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Free/reduced lunch eligible", "coefficients": ["0.48", "0.50", "0", "1", "2,541,918"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Black", "coefficients": ["0.16", "0.37", "0", "1", "2,541,918"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Hispanic", "coefficients": ["0.21", "0.41", "0", "1", "2,541,918"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Teacher and Classroom Characteristics",
            "variables": [
                {"label": "Teacher experience (years)", "coefficients": ["12.4", "9.8", "0", "42", "148,284"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Teacher has master's degree", "coefficients": ["0.41", "0.49", "0", "1", "148,284"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Class size", "coefficients": ["23.8", "4.2", "12", "35", "148,284"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Teacher VA (math, SD units)", "coefficients": ["0.00", "0.14", "-0.68", "0.72", "148,284"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }],
        "notes": "Test scores standardized within grade-year to mean zero and unit variance. Teacher VA estimated using the leave-year-out procedure described in Section 4.",
        "qa": [
            {"question": "How many student-year observations are in the sample?", "answer": "2,541,918"},
            {"question": "What is the standard deviation of teacher value-added in math?", "answer": "0.14 SD units"},
            {"question": "What is the mean class size?", "answer": "23.8"},
            {"question": "What fraction of students are eligible for free/reduced lunch?", "answer": "0.48 (48 percent)"},
        ],
    })

    va_estimation = render_regression_table({
        "table_id": "va-estimation",
        "caption": "Teacher Value-Added Estimation: Forecast Bias Tests",
        "label": "tab:va-estimation",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Student Test Score (Math)",
            "variables": [
                {"label": "Predicted teacher VA (leave-year-out)", "coefficients": ["1.014***", "1.008***", "0.998***", "0.992***"],
                 "std_errors": ["(0.018)", "(0.018)", "(0.019)", "(0.019)"]},
            ],
        }],
        "controls": [
            {"label": "Student demographics", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Lagged test scores (cubic)", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "School fixed effects", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["2,541,918", "2,541,918", "2,541,918", "2,541,918"]},
            {"label": "R-squared", "values": ["0.018", "0.124", "0.584", "0.612"]},
            {"label": "p-value ($\\hat{\\beta} = 1$)", "values": ["0.44", "0.66", "0.92", "0.68"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered at teacher level. Predicted VA estimated using all years except the current year (leave-year-out). A coefficient of 1 confirms unbiased VA estimates.",
        "qa": [
            {"question": "Is teacher VA a forecast-unbiased predictor of student test scores?", "answer": "Yes, the coefficient is approximately 1.0 in all specifications and we cannot reject beta=1"},
            {"question": "What controls are included in column 4?", "answer": "Student demographics, lagged test scores (cubic), and school fixed effects"},
            {"question": "What is the p-value for the test that beta=1 in column 3?", "answer": "0.92"},
        ],
    })

    quasi_experimental = render_regression_table({
        "table_id": "quasi-experimental",
        "caption": "Quasi-Experimental Validation: Teacher Switching Design",
        "label": "tab:quasi-experimental",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Panel A: Effect of Teacher Arrival on School-Grade Mean Score",
            "variables": [
                {"label": "Arriving teacher VA", "coefficients": ["0.941***", "0.928***", "0.914***", "0.898***"],
                 "std_errors": ["(0.042)", "(0.041)", "(0.043)", "(0.044)"]},
            ],
        }, {
            "dep_var": "Panel B: Placebo — Effect on Non-Taught Grades",
            "variables": [
                {"label": "Arriving teacher VA", "coefficients": ["0.012", "0.008", "0.004", "0.002"],
                 "std_errors": ["(0.038)", "(0.037)", "(0.039)", "(0.040)"]},
            ],
        }],
        "controls": [
            {"label": "School-grade FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Year FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "School-grade trends", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Student demographics", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Class size controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "School-grade-year obs.", "values": ["84,216", "84,216", "84,216", "84,216"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered at school level. Panel A tests whether a high-VA teacher arriving at a school raises test scores in the taught grade. Panel B (placebo) checks non-taught grades in the same school. The near-unity coefficient in Panel A and null in Panel B validate the VA measure.",
        "qa": [
            {"question": "Does a high-VA teacher arriving at a school raise test scores?", "answer": "Yes, the coefficient is 0.941 in the baseline (near unity)"},
            {"question": "Is there a placebo effect on non-taught grades?", "answer": "No, the coefficient is 0.012 and insignificant"},
        ],
    })

    long_run_outcomes = render_regression_table({
        "table_id": "long-run-outcomes",
        "caption": "Long-Run Effects of Teacher Quality on Adult Outcomes",
        "label": "tab:long-run",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Panel A: College Attendance at Age 20",
            "variables": [
                {"label": "Teacher VA (1 SD increase)", "coefficients": ["0.0182***", "0.0168***", "0.0154***", "0.0148***"],
                 "std_errors": ["(0.0028)", "(0.0028)", "(0.0029)", "(0.0030)"]},
            ],
        }, {
            "dep_var": "Panel B: Earnings at Age 28 (Log)",
            "variables": [
                {"label": "Teacher VA (1 SD increase)", "coefficients": ["0.0128***", "0.0118***", "0.0104***", "0.0098***"],
                 "std_errors": ["(0.0024)", "(0.0024)", "(0.0025)", "(0.0026)"]},
            ],
        }, {
            "dep_var": "Panel C: Teenage Birth (Ages 15--19, Female Only)",
            "variables": [
                {"label": "Teacher VA (1 SD increase)", "coefficients": ["-0.0084***", "-0.0078***", "-0.0072***", "-0.0068**"],
                 "std_errors": ["(0.0024)", "(0.0024)", "(0.0025)", "(0.0026)"]},
            ],
        }, {
            "dep_var": "Panel D: Neighborhood Quality at Age 25 (Income Percentile)",
            "variables": [
                {"label": "Teacher VA (1 SD increase)", "coefficients": ["0.412***", "0.384***", "0.348***", "0.324***"],
                 "std_errors": ["(0.098)", "(0.098)", "(0.102)", "(0.104)"]},
            ],
        }],
        "controls": [
            {"label": "Student demographics", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Lagged test scores (cubic)", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "School fixed effects", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations (Panel A)", "values": ["1,841,212", "1,841,212", "1,841,212", "1,841,212"]},
            {"label": "Control mean (Panel A)", "values": ["0.514", "0.514", "0.514", "0.514"]},
            {"label": "Control mean (Panel B)", "values": ["10.24", "10.24", "10.24", "10.24"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered at teacher level. Teacher VA estimated in math using leave-year-out procedure. Long-run outcomes matched via tax records and vital statistics.",
        "qa": [
            {"question": "Does a 1 SD increase in teacher VA raise college attendance?", "answer": "Yes, by 1.82 percentage points (column 1)"},
            {"question": "Does teacher quality affect adult earnings?", "answer": "Yes, a 1 SD increase in teacher VA raises age-28 earnings by 1.28 percent"},
            {"question": "Does teacher quality reduce teenage birth?", "answer": "Yes, by 0.84 percentage points per 1 SD of teacher VA"},
            {"question": "What is the control mean of college attendance?", "answer": "0.514 (51.4 percent)"},
        ],
    })

    npv_calculations = render_regression_table({
        "table_id": "npv-calculations",
        "caption": "Net Present Value of Replacing a Low-VA Teacher",
        "label": "tab:npv",
        "model_labels": ["Baseline", "Lower Bound", "Upper Bound"],
        "panels": [{
            "dep_var": "NPV of Lifetime Earnings Gain Per Classroom (2010 \\$)",
            "variables": [
                {"label": "Replace bottom 5\\% with median", "coefficients": ["\\$252,000", "\\$148,000", "\\$356,000"],
                 "std_errors": ["", "", ""]},
                {"label": "Replace bottom 5\\% with 75th pctile", "coefficients": ["\\$378,000", "\\$222,000", "\\$534,000"],
                 "std_errors": ["", "", ""]},
                {"label": "Per-student NPV (bottom 5\\% to median)", "coefficients": ["\\$10,500", "\\$6,167", "\\$14,833"],
                 "std_errors": ["", "", ""]},
            ],
        }, {
            "dep_var": "Assumptions",
            "variables": [
                {"label": "Discount rate", "coefficients": ["3\\%", "5\\%", "2\\%"],
                 "std_errors": ["", "", ""]},
                {"label": "Years of teaching career remaining", "coefficients": ["25", "15", "30"],
                 "std_errors": ["", "", ""]},
                {"label": "Class size", "coefficients": ["24", "24", "24"],
                 "std_errors": ["", "", ""]},
                {"label": "Earnings growth rate", "coefficients": ["2\\%", "1\\%", "3\\%"],
                 "std_errors": ["", "", ""]},
            ],
        }],
        "notes": "NPV calculated using estimated effect of teacher VA on adult earnings, discounted over working life. Lower/upper bounds vary discount rate, career length, and earnings growth assumptions.",
        "qa": [
            {"question": "What is the NPV of replacing a bottom 5% teacher with a median teacher?", "answer": "$252,000 per classroom in baseline scenario"},
            {"question": "What is the per-student NPV of replacing a bottom 5% teacher?", "answer": "$10,500 per student"},
            {"question": "What discount rate is used in the baseline?", "answer": "3 percent"},
        ],
    })

    class_size = render_regression_table({
        "table_id": "class-size",
        "caption": "Class Size Effects: Maimonides' Rule IV Estimates",
        "label": "tab:class-size",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Math Test Score (Standardized)",
            "variables": [
                {"label": "Class size", "coefficients": ["-0.028***", "-0.024***", "-0.021***", "-0.018**"],
                 "std_errors": ["(0.008)", "(0.008)", "(0.008)", "(0.009)"]},
            ],
        }],
        "controls": [
            {"label": "Enrollment controls (quadratic)", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "School FE", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Student demographics", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Teacher FE", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["2,541,918", "2,541,918", "2,541,918", "2,541,918"]},
            {"label": "First-stage F", "values": ["284.1", "218.4", "204.8", "142.6"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. IV estimates using Maimonides' rule as instrument. Standard errors clustered at school level. A 1-student reduction in class size raises scores by 0.018--0.028 SD.",
        "qa": [
            {"question": "What is the IV estimate of the class size effect?", "answer": "-0.028 SD per additional student (column 1)"},
            {"question": "What is the instrument for class size?", "answer": "Maimonides' rule (enrollment-based discontinuity in predicted class size)"},
            {"question": "Is the class size effect robust to teacher fixed effects?", "answer": "Yes, the coefficient remains -0.018 and significant"},
        ],
    })

    va_by_subgroup = render_regression_table({
        "table_id": "va-by-subgroup",
        "caption": "Heterogeneity in Teacher Value-Added Effects",
        "label": "tab:va-subgroup",
        "model_labels": ["Test Score", "College", "Earnings", "Teen Birth"],
        "panels": [{
            "dep_var": "Panel A: By Student Socioeconomic Status",
            "variables": [
                {"label": "Teacher VA $\\times$ Low SES", "coefficients": ["0.172***", "0.0218***", "0.0148***", "-0.0098***"],
                 "std_errors": ["(0.018)", "(0.0034)", "(0.0028)", "(0.0028)"]},
                {"label": "Teacher VA $\\times$ High SES", "coefficients": ["0.124***", "0.0124***", "0.0088***", "-0.0054**"],
                 "std_errors": ["(0.016)", "(0.0030)", "(0.0026)", "(0.0024)"]},
                {"label": "p-value (equality)", "coefficients": ["0.018", "0.021", "0.068", "0.142"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: By Race",
            "variables": [
                {"label": "Teacher VA $\\times$ Black", "coefficients": ["0.168***", "0.0208***", "0.0142***", "-0.0094***"],
                 "std_errors": ["(0.022)", "(0.0038)", "(0.0032)", "(0.0032)"]},
                {"label": "Teacher VA $\\times$ Hispanic", "coefficients": ["0.158***", "0.0194***", "0.0132***", "-0.0088***"],
                 "std_errors": ["(0.020)", "(0.0036)", "(0.0030)", "(0.0030)"]},
                {"label": "Teacher VA $\\times$ White", "coefficients": ["0.128***", "0.0132***", "0.0094***", "-0.0058**"],
                 "std_errors": ["(0.016)", "(0.0030)", "(0.0026)", "(0.0024)"]},
            ],
        }],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered at teacher level. Low SES: eligible for free/reduced lunch. Effects of teacher quality are larger for disadvantaged students, suggesting teacher quality reduces achievement gaps.",
        "qa": [
            {"question": "Are teacher VA effects larger for low-SES students?", "answer": "Yes, the effect on test scores is 0.172 for low SES vs. 0.124 for high SES"},
            {"question": "Are teacher VA effects larger for Black students?", "answer": "Yes, the effect on test scores is 0.168 for Black vs. 0.128 for White students"},
            {"question": "Does teacher quality help close achievement gaps?", "answer": "Yes, effects are systematically larger for disadvantaged groups"},
        ],
    })

    persistence = render_regression_table({
        "table_id": "persistence",
        "caption": "Persistence of Teacher Effects Over Time",
        "label": "tab:persistence",
        "model_labels": ["$t+1$", "$t+2$", "$t+3$", "$t+4$"],
        "panels": [{
            "dep_var": "Dep. var.: Test Score in Year $t+k$",
            "variables": [
                {"label": "Teacher VA in year $t$", "coefficients": ["0.142***", "0.118***", "0.084***", "0.062***"],
                 "std_errors": ["(0.014)", "(0.014)", "(0.016)", "(0.018)"]},
            ],
        }],
        "controls": [
            {"label": "Student demographics", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Lagged test scores (cubic)", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "School FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["2,184,512", "1,841,284", "1,524,618", "1,248,412"]},
            {"label": "Fade-out rate per year", "values": ["--", "0.17", "0.29", "0.37"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Standard errors clustered at teacher level. Test score effects fade by approximately 50\\% after 3 years but remain statistically significant.",
        "qa": [
            {"question": "How much do teacher effects fade out after one year?", "answer": "From the original effect, scores drop to about 0.142 (vs. ~0.16 in year t), roughly 10-15% fade"},
            {"question": "Are teacher effects still significant after 4 years?", "answer": "Yes, the coefficient is 0.062 with SE 0.018"},
            {"question": "What is the fade-out rate after 3 years?", "answer": "0.29 (29 percent cumulative fade-out)"},
        ],
    })

    robustness = render_regression_table({
        "table_id": "robustness",
        "caption": "Robustness of Value-Added Estimates",
        "label": "tab:robustness",
        "model_labels": ["Baseline", "Drift-Adjusted", "Shrinkage", "Team VA", "VA w/o Demographics"],
        "panels": [{
            "dep_var": "Forecast Bias Coefficient ($\\hat{\\beta}$ on Predicted VA)",
            "variables": [
                {"label": "Math", "coefficients": ["0.998", "0.984", "1.012", "0.994", "0.942"],
                 "std_errors": ["(0.019)", "(0.020)", "(0.018)", "(0.022)", "(0.024)"]},
                {"label": "Reading", "coefficients": ["0.992", "0.978", "1.004", "0.988", "0.934"],
                 "std_errors": ["(0.020)", "(0.021)", "(0.019)", "(0.024)", "(0.026)"]},
            ],
        }, {
            "dep_var": "Long-Run Effect (College Attendance, per 1 SD VA)",
            "variables": [
                {"label": "Math VA", "coefficients": ["0.0154", "0.0148", "0.0162", "0.0144", "0.0138"],
                 "std_errors": ["(0.0029)", "(0.0030)", "(0.0028)", "(0.0032)", "(0.0034)"]},
            ],
        }],
        "notes": "All specifications significant at 1\\% level. Drift-adjusted allows VA to change over time. Shrinkage applies empirical Bayes shrinkage. Team VA estimates grade-team VA. VA w/o demographics omits student race and SES. Results stable across specifications.",
        "qa": [
            {"question": "Is the VA estimate robust to drift adjustment?", "answer": "Yes, the forecast bias coefficient is 0.984 (very close to 1)"},
            {"question": "Does shrinkage affect the VA estimates?", "answer": "The forecast bias is 1.012, indicating slight over-shrinkage but near-unbiased"},
            {"question": "What happens when demographics are excluded from the VA model?", "answer": "The forecast bias drops to 0.942, suggesting slight bias when demographics are omitted"},
        ],
    })

    appendix_specification = render_regression_table({
        "table_id": "appendix-specification",
        "caption": "Appendix: Alternative VA Estimation Methods",
        "label": "tab:appendix-spec",
        "model_labels": ["OLS", "EB Shrinkage", "BLUP", "Ridge"],
        "panels": [{
            "dep_var": "SD of Estimated Teacher VA (Math)",
            "variables": [
                {"label": "Raw SD", "coefficients": ["0.184", "0.142", "0.138", "0.144"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Signal SD ($\\hat{\\sigma}_{\\mu}$)", "coefficients": ["0.142", "0.141", "0.138", "0.140"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Noise SD ($\\hat{\\sigma}_{\\varepsilon}$)", "coefficients": ["0.118", "0.024", "0.018", "0.032"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Reliability ($\\hat{\\rho}$)", "coefficients": ["0.591", "0.972", "0.983", "0.950"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "OLS: no shrinkage. EB: empirical Bayes optimal shrinkage. BLUP: best linear unbiased predictor. Ridge: ridge regression with cross-validated penalty. Signal SD is consistent across methods; noise varies with shrinkage.",
        "qa": [
            {"question": "What is the signal standard deviation of teacher quality?", "answer": "Approximately 0.14 SD units, consistent across methods"},
            {"question": "What is the reliability of raw OLS VA estimates?", "answer": "0.591 (59.1 percent)"},
            {"question": "What is the reliability of empirical Bayes estimates?", "answer": "0.972 (97.2 percent)"},
        ],
    })

    # --- Equations ---
    eq_va_model = EquationSpec(
        "va-model",
        r"Y_{ijt} = \alpha_{j(i,t)} + \beta X_{ijt} + \gamma A_{i,t-1} + \varepsilon_{ijt}",
        "eq:va-model",
        "Value-added model: student $i$'s test score with teacher $j$ in year $t$, controlling for demographics $X$ and lagged achievement $A_{i,t-1}$. Teacher VA is $\\alpha_j$.",
        [{"question": "What is the value-added model?", "answer": "Y_ijt = alpha_j + beta*X_ijt + gamma*A_{i,t-1} + epsilon_ijt, where alpha_j is the teacher fixed effect"}],
    )

    eq_leave_out = EquationSpec(
        "leave-out",
        r"\hat{\mu}_{j,-t} = \frac{1}{|\mathcal{T}_j \setminus \{t\}|} \sum_{s \in \mathcal{T}_j \setminus \{t\}} \bar{e}_{js}, \quad \bar{e}_{js} = \frac{1}{n_{js}} \sum_{i \in \mathcal{C}_{js}} \hat{\varepsilon}_{ijs}",
        "eq:leave-out",
        "Leave-year-out VA estimate: average residual across all years except $t$ for teacher $j$. Avoids mechanical correlation between estimate and outcome.",
        [{"question": "Why use leave-year-out estimation?", "answer": "To avoid mechanical correlation between the VA estimate and the test scores being predicted, which would bias the forecast test toward 1"}],
    )

    eq_forecast_bias = EquationSpec(
        "forecast-bias",
        r"Y_{ijt} = a + b \cdot \hat{\mu}_{j,-t} + \Gamma X_{ijt} + \nu_{ijt}, \quad H_0: b = 1",
        "eq:forecast-bias",
        "Forecast bias test: regress current outcomes on predicted VA. Under unbiased VA, $b = 1$.",
    )

    eq_eb_shrinkage = EquationSpec(
        "eb-shrinkage",
        r"\hat{\mu}_j^{EB} = \hat{\rho}_j \cdot \hat{\mu}_j^{OLS} + (1-\hat{\rho}_j) \cdot 0, \quad \hat{\rho}_j = \frac{\hat{\sigma}_\mu^2}{\hat{\sigma}_\mu^2 + \hat{\sigma}_\varepsilon^2 / n_j}, \quad \hat{\sigma}_\mu^2 = \int_0^\infty \mu^2 \, d\hat{G}(\mu) - \frac{\hat{\sigma}_\varepsilon^2}{\bar{n}}",
        "eq:eb",
        "Empirical Bayes shrinkage: shrink OLS estimate toward zero with reliability weight $\\hat{\\rho}_j$ that depends on signal variance and sample size.",
    )

    eq_long_run = EquationSpec(
        "long-run-specification",
        r"Y_{i,\text{adult}} = \alpha + \delta \hat{\mu}_{j(i,t),-t}^{EB} + \beta X_{ijt} + \gamma A_{i,t-1} + \varepsilon_i",
        "eq:long-run",
        "Long-run outcomes regression: adult outcome $Y_{i,\\text{adult}}$ (college, earnings, etc.) regressed on teacher VA estimated from test scores.",
    )

    eq_maimonides = EquationSpec(
        "maimonides-rule",
        r"f(n_s) = \frac{n_s}{\left\lfloor (n_s - 1) / 40 \right\rfloor + 1}",
        "eq:maimonides",
        "Maimonides' rule: predicted class size as a function of enrollment $n_s$. Creates discontinuities at multiples of 40 that serve as instruments.",
        [{"question": "What is Maimonides' rule?", "answer": "A rule that caps class size at 40, creating a new class when enrollment exceeds multiples of 40. This generates quasi-experimental variation in class size."}],
    )

    eq_npv = EquationSpec(
        "npv-formula",
        r"NPV = n_s \sum_{t=0}^{T-1} \frac{1}{(1+r)^t} \int_0^{W} \frac{\Delta w(\hat{\mu}_j) \cdot w(\tau)}{(1+r)^\tau}\,d\tau, \quad \Delta w(\hat{\mu}_j) = \begin{bmatrix} \hat{\delta}_{\text{math}} \\ \hat{\delta}_{\text{read}} \end{bmatrix}' \begin{bmatrix} \hat{\mu}_j^{\text{math}} \\ \hat{\mu}_j^{\text{read}} \end{bmatrix}",
        "eq:npv",
        "Net present value of teacher quality: $n_s$ students per year, $T$ years of teaching, $\\Delta w$ earnings gain per unit of VA, $w_\\tau$ is base earnings at experience $\\tau$, $r$ is discount rate.",
    )

    eq_decomposition = EquationSpec(
        "variance-decomposition",
        r"\text{Var}(Y_{ijt}) = \underbrace{\sigma_\mu^2}_{\text{teacher}} + \underbrace{\sigma_\varepsilon^2}_{\text{residual}} + \underbrace{\sigma_X^2}_{\text{observables}}, \quad \text{teacher share} = \frac{\sigma_\mu^2}{\sum_{i=1}^{N} \sum_{j=1}^{M} (Y_{ijt} - \bar{Y})^2 / (NM-1)}",
        "eq:decomposition",
        "Variance decomposition: fraction of test score variance attributable to teachers. The teacher share measures how important teacher assignment is for student outcomes.",
        [{"question": "What fraction of test score variance is attributable to teachers?", "answer": "The teacher share sigma_mu^2 / Var(Y) is approximately 0.14^2 / 1 = 0.02, or about 2 percent"}],
    )

    eq_fade_out = EquationSpec(
        "fade-out",
        r"Y_{i,t+k} = \alpha + \lambda^k \delta \hat{\mu}_j + \beta X_{ijt} + \gamma A_{i,t-1} + \varepsilon_{i,t+k}, \quad \lambda \in (0,1)",
        "eq:fade-out",
        "Fade-out model: test score effects of teacher VA decay geometrically at rate $\\lambda$ per year. Even with $\\lambda < 1$, knowledge gains may persist through complementary human capital channels.",
    )

    eq_selection = EquationSpec(
        "selection-on-observables",
        r"\delta = \frac{\hat{\beta} - 0}{\hat{\beta}_{controlled} - 0} \cdot \left(\frac{R^2_{max} - \tilde{R}^2}{\tilde{R}^2 - R^2_0}\right)^{-1}",
        "eq:selection",
        "Oster (2019) proportional selection coefficient $\\delta$: ratio of selection on unobservables to observables needed to explain away the effect.",
    )

    # --- Appendix proof block ---
    appendix_proof_text = r"""
\begin{proposition}[Unbiasedness of Leave-Year-Out VA]
Let $Y_{ijt} = \mu_j + X_{ijt}'\beta + \varepsilon_{ijt}$ with $E[\varepsilon_{ijt} | \mu_j, X_{ijt}] = 0$. The leave-year-out estimator $\hat{\mu}_{j,-t}$ satisfies:
\begin{align}
E[\hat{\mu}_{j,-t} | j \text{ teaches in year } t] = \mu_j + O(1/n_{j,-t}),
\end{align}
where $n_{j,-t}$ is the number of student-years for teacher $j$ excluding year $t$.
\end{proposition}

\begin{proof}
The leave-year-out estimator is:
\begin{align}
\hat{\mu}_{j,-t} &= \frac{1}{n_{j,-t}} \sum_{s \neq t} \sum_{i \in \mathcal{C}_{js}} (Y_{ijs} - X_{ijs}'\hat{\beta}_{-t}) \\
&= \mu_j + \frac{1}{n_{j,-t}} \sum_{s \neq t} \sum_{i \in \mathcal{C}_{js}} \varepsilon_{ijs} + \frac{1}{n_{j,-t}} \sum_{s \neq t} \sum_{i \in \mathcal{C}_{js}} X_{ijs}'(\beta - \hat{\beta}_{-t}).
\end{align}
The second term has conditional expectation zero by the exogeneity assumption. The third term is $O(1/\sqrt{n_{j,-t}}) \cdot O(1/\sqrt{N})$ where $N$ is the total sample size, giving overall bias $O(1/n_{j,-t})$ which vanishes as classroom sizes grow.

Crucially, $\hat{\mu}_{j,-t}$ is independent of $\varepsilon_{ijt}$ for students $i$ in year $t$ because year $t$ data is excluded from estimation. This ensures that the forecast bias test $E[Y_{ijt} | \hat{\mu}_{j,-t}] = \hat{\mu}_{j,-t}$ holds without contamination.
\end{proof}

\begin{proposition}[Empirical Bayes Shrinkage is Optimal]
Under the hierarchical model $\mu_j \sim \mathcal{N}(0, \sigma_\mu^2)$ and $\hat{\mu}_j^{OLS} | \mu_j \sim \mathcal{N}(\mu_j, \sigma_\varepsilon^2/n_j)$, the minimum MSE estimator is:
\begin{align}
\hat{\mu}_j^{EB} = \rho_j \hat{\mu}_j^{OLS}, \quad \rho_j = \frac{\sigma_\mu^2}{\sigma_\mu^2 + \sigma_\varepsilon^2/n_j},
\end{align}
with MSE:
\begin{align}
MSE(\hat{\mu}_j^{EB}) = \rho_j \cdot \frac{\sigma_\varepsilon^2}{n_j} = \frac{\sigma_\mu^2 \sigma_\varepsilon^2/n_j}{\sigma_\mu^2 + \sigma_\varepsilon^2/n_j} \leq \frac{\sigma_\varepsilon^2}{n_j} = MSE(\hat{\mu}_j^{OLS}).
\end{align}
The improvement is largest when $n_j$ is small (noisy estimates are shrunk more toward zero).
\end{proposition}

\begin{proposition}[Identification of Long-Run Effects]
The long-run effect $\delta$ in $Y_{i,adult} = \delta \mu_{j(i,t)} + X_{ijt}'\beta + \varepsilon_i$ is identified under:
\begin{enumerate}
\item \textbf{Conditional random assignment:} $\mu_j \perp\!\!\!\perp \varepsilon_i | X_{ijt}, A_{i,t-1}$ (teacher assignment is quasi-random conditional on observables and lagged scores).
\item \textbf{Exclusion restriction:} Teacher quality affects adult outcomes only through its effect on knowledge/skills, not through direct effects on adult outcomes.
\end{enumerate}
Under these assumptions, the OLS estimator using the leave-year-out VA $\hat{\mu}_{j,-t}^{EB}$ is consistent:
\begin{align}
\hat{\delta}_{OLS} \xrightarrow{p} \delta.
\end{align}
The quasi-experimental validation (teacher switching design) provides evidence for assumption 1 by showing that changes in school-grade mean scores track arriving teachers' VA.
\end{proposition}

\begin{proposition}[NPV Calculation]
The NPV of replacing a teacher at the $p$-th percentile of VA with one at the $q$-th percentile is:
\begin{align}
NPV = n_s \cdot (\mu_q - \mu_p) \cdot \hat{\delta}_{\text{earnings}} \cdot \bar{w} \cdot \sum_{t=0}^{T-1} \frac{1}{(1+r)^t} \cdot \frac{1-(1+g)^W/(1+r)^W}{r-g},
\end{align}
where $n_s$ is class size, $\hat{\delta}_{\text{earnings}}$ is the earnings effect per unit VA, $\bar{w}$ is average earnings, $T$ is remaining teaching career, $W$ is working life, $g$ is earnings growth, and $r$ is the discount rate.
\end{proposition}

\begin{lemma}[Multivariate VA Estimator]
In the joint math-reading VA model, the teacher effect vector is $\boldsymbol{\mu}_j = (\mu_j^{\text{math}}, \mu_j^{\text{read}})'$ and the multivariate empirical Bayes estimator is:
\begin{align}
\hat{\boldsymbol{\mu}}_j^{EB} = \begin{bmatrix} \hat{\sigma}_{\mu,m}^2 & \hat{\sigma}_{\mu,mr} \\ \hat{\sigma}_{\mu,mr} & \hat{\sigma}_{\mu,r}^2 \end{bmatrix} \left( \begin{bmatrix} \hat{\sigma}_{\mu,m}^2 & \hat{\sigma}_{\mu,mr} \\ \hat{\sigma}_{\mu,mr} & \hat{\sigma}_{\mu,r}^2 \end{bmatrix} + \frac{1}{n_j} \begin{bmatrix} \hat{\sigma}_{\varepsilon,m}^2 & 0 \\ 0 & \hat{\sigma}_{\varepsilon,r}^2 \end{bmatrix} \right)^{-1} \hat{\boldsymbol{\mu}}_j^{OLS},
\end{align}
which generalizes the scalar shrinkage formula. The resulting reliability matrix is $\hat{\boldsymbol{\rho}}_j = \boldsymbol{\Sigma}_\mu (\boldsymbol{\Sigma}_\mu + n_j^{-1} \boldsymbol{\Sigma}_\varepsilon)^{-1}$.
\end{lemma}

\begin{remark}[Integral Representation of Lifetime NPV]
The continuous-time NPV of teacher quality improvement satisfies:
\begin{align}
NPV = n_s \int_0^T e^{-rt} \left[\int_0^W e^{-r\tau} \sum_{i=1}^{N} \sum_{j=1}^{M} \Delta w_{ij}(\hat{\boldsymbol{\mu}}_j) \, d\tau \right] dt.
\end{align}
\end{remark}
"""

    appendix_proof_table = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-educ", text_paragraphs=14,
                        equations=[eq_va_model])

    background = SectionSpec(
        "Background and Literature", "sec:background-educ", text_paragraphs=10,
        subsections=[
            SectionSpec("Teacher Quality and Student Achievement", "sec:lit-achievement", level=2, text_paragraphs=7),
            SectionSpec("Long-Run Effects of Education Inputs", "sec:lit-longrun", level=2, text_paragraphs=6),
            SectionSpec("Class Size Reduction Policies", "sec:lit-classsize", level=2, text_paragraphs=6),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-educ", text_paragraphs=10,
        tables=[summary_stats],
        subsections=[
            SectionSpec("Test Score Data", "sec:data-scores", level=2, text_paragraphs=7),
            SectionSpec("Tax Records and Long-Run Outcomes", "sec:data-tax", level=2, text_paragraphs=6),
            SectionSpec("Teacher-Student Matching", "sec:data-matching", level=2, text_paragraphs=6),
        ],
    )

    va_methodology = SectionSpec(
        "Value-Added Methodology", "sec:va-method", text_paragraphs=12,
        equations=[eq_leave_out, eq_forecast_bias, eq_eb_shrinkage, eq_decomposition],
        subsections=[
            SectionSpec("The Value-Added Model", "sec:va-spec", level=2, text_paragraphs=8),
            SectionSpec("Leave-Year-Out Estimation", "sec:va-lyo", level=2, text_paragraphs=7),
            SectionSpec("Empirical Bayes Shrinkage", "sec:va-eb", level=2, text_paragraphs=7),
        ],
    )

    validation = SectionSpec(
        "Validation of Value-Added Measures", "sec:validation", text_paragraphs=10,
        tables=[va_estimation, quasi_experimental],
        subsections=[
            SectionSpec("Forecast Bias Tests", "sec:forecast-bias", level=2, text_paragraphs=8),
            SectionSpec("Quasi-Experimental Evidence: Teacher Switching", "sec:teacher-switching", level=2, text_paragraphs=8),
        ],
    )

    results_test_scores = SectionSpec(
        "Results: Test Score Effects", "sec:results-scores", text_paragraphs=10,
        tables=[persistence],
        equations=[eq_fade_out],
        subsections=[
            SectionSpec("Contemporaneous Effects", "sec:contemp-effects", level=2, text_paragraphs=7),
            SectionSpec("Persistence and Fade-Out", "sec:fade-out", level=2, text_paragraphs=7),
        ],
    )

    results_long_run = SectionSpec(
        "Results: Long-Run Effects", "sec:results-longrun", text_paragraphs=10,
        tables=[long_run_outcomes, npv_calculations],
        equations=[eq_long_run, eq_npv],
        subsections=[
            SectionSpec("College and Labor Market Outcomes", "sec:college-labor", level=2, text_paragraphs=8),
            SectionSpec("Other Adult Outcomes", "sec:other-adult", level=2, text_paragraphs=7),
            SectionSpec("Net Present Value Calculations", "sec:npv-calc", level=2, text_paragraphs=7),
        ],
    )

    heterogeneity = SectionSpec(
        "Heterogeneity and Distributional Effects", "sec:heterogeneity-educ", text_paragraphs=10,
        tables=[va_by_subgroup],
        equations=[eq_selection],
    )

    class_size_section = SectionSpec(
        "Class Size and Teacher Quality", "sec:class-size", text_paragraphs=10,
        tables=[class_size],
        equations=[eq_maimonides],
        subsections=[
            SectionSpec("Maimonides' Rule IV", "sec:maimonides-iv", level=2, text_paragraphs=7),
            SectionSpec("Interaction of Class Size and Teacher VA", "sec:class-va-interact", level=2, text_paragraphs=7),
        ],
    )

    robustness_section = SectionSpec(
        "Robustness", "sec:robustness-educ", text_paragraphs=10,
        tables=[robustness],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-educ", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Proofs and Derivations", "sec:appendix-a-educ", text_paragraphs=3,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Alternative Specifications", "sec:appendix-b-educ", text_paragraphs=5,
        tables=[appendix_specification],
    )

    return PaperSpec(
        paper_id="11",
        field_slug="education",
        title="Teacher Quality and Student Outcomes: Evidence from Value-Added Models and Long-Run Data",
        authors="Raj Chetty, John N. Friedman, Jonah E. Rockoff, Amanda Chen",
        journal_style="aer",
        abstract=(
            "We estimate the causal effect of teacher quality on students' short- and long-run outcomes "
            "using value-added models applied to administrative data covering 2.5 million student-year "
            "observations linked to tax records. Our leave-year-out VA estimates pass stringent forecast "
            "bias tests (coefficient on predicted VA = 0.998 with school fixed effects) and are validated "
            "by quasi-experimental teacher switching designs. A one standard deviation increase in teacher VA "
            "(0.14 test score SD) raises college attendance by 1.5 percentage points and age-28 earnings by "
            "1.0 percent, while reducing teenage birth by 0.7 percentage points. Replacing a bottom-5\\% "
            "teacher with a median teacher generates \\$252,000 in present-value earnings gains per classroom. "
            "Effects are larger for disadvantaged students. Using Maimonides' rule as an instrument, we also "
            "find that reducing class size by one student raises test scores by 0.02 SD, a complementary "
            "but smaller effect than improving teacher quality."
        ),
        sections=[intro, background, data, va_methodology, validation, results_test_scores,
                  results_long_run, heterogeneity, class_size_section, robustness_section,
                  conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{chetty2014a} Chetty, R., Friedman, J. N., and Rockoff, J. E. (2014). Measuring the Impacts of Teachers I: Evaluating Bias in Teacher Value-Added Estimates. \textit{American Economic Review}, 104(9), 2593--2632.",
            r"\bibitem{chetty2014b} Chetty, R., Friedman, J. N., and Rockoff, J. E. (2014). Measuring the Impacts of Teachers II: Teacher Value-Added and Student Outcomes in Adulthood. \textit{American Economic Review}, 104(9), 2633--2679.",
            r"\bibitem{angrist1999} Angrist, J. D. and Lavy, V. (1999). Using Maimonides' Rule to Estimate the Effect of Class Size on Scholastic Achievement. \textit{Quarterly Journal of Economics}, 114(2), 533--575.",
            r"\bibitem{rivkin2005} Rivkin, S. G., Hanushek, E. A., and Kain, J. F. (2005). Teachers, Schools, and Academic Achievement. \textit{Econometrica}, 73(2), 417--458.",
            r"\bibitem{kane2008} Kane, T. J. and Staiger, D. O. (2008). Estimating Teacher Impacts on Student Achievement: An Experimental Evaluation. NBER Working Paper 14607.",
            r"\bibitem{rothstein2010} Rothstein, J. (2010). Teacher Quality in Educational Production: Tracking, Decay, and Student Achievement. \textit{Quarterly Journal of Economics}, 125(1), 175--214.",
            r"\bibitem{jackson2014} Jackson, C. K. (2014). Teacher Quality at the High School Level: The Importance of Accounting for Tracks. \textit{Journal of Labor Economics}, 32(4), 645--684.",
            r"\bibitem{oster2019} Oster, E. (2019). Unobservable Selection and Coefficient Stability: Theory and Evidence. \textit{Journal of Business \& Economic Statistics}, 37(2), 187--204.",
        ],
        target_pages=55,
        qa=[
            {"question": "What is the main identification strategy for teacher VA?", "answer": "Leave-year-out estimation validated by forecast bias tests (beta = 0.998) and quasi-experimental teacher switching designs"},
            {"question": "What is the standard deviation of teacher value-added?", "answer": "0.14 test score standard deviations"},
            {"question": "What is the effect of a 1 SD increase in teacher VA on college attendance?", "answer": "1.5 percentage point increase"},
            {"question": "What is the NPV of replacing a bottom-5% teacher with a median teacher?", "answer": "$252,000 per classroom"},
            {"question": "Are teacher VA effects larger for disadvantaged students?", "answer": "Yes, effects are systematically larger for low-SES, Black, and Hispanic students"},
        ],
    )


PAPER_BUILDERS["11"] = _paper_11_education
