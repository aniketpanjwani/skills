#!/usr/bin/env python3
"""Paper builder for paper 06 (Macroeconomics)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)


def _paper_06_macro() -> PaperSpec:
    # --- Tables ---
    narrative_summary = render_regression_table({
        "table_id": "narrative-shocks-summary",
        "caption": "Summary of Narrative Monetary Policy Shocks",
        "label": "tab:narrative-shocks",
        "model_labels": ["Mean", "SD", "Min", "Max"],
        "panels": [{
            "dep_var": "Panel A: Full Sample 1960-2007",
            "variables": [
                {"label": "Narrative Shock (pp)", "coefficients": ["0.04", "0.82", "-3.00", "3.50"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Federal Funds Rate Change", "coefficients": ["0.02", "0.61", "-3.50", "4.25"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Number of Episodes", "coefficients": ["24", "--", "--", "--"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: By Sub-Period",
            "variables": [
                {"label": "1960-1979 Mean Shock", "coefficients": ["0.12", "0.91", "-2.50", "3.50"],
                 "std_errors": ["", "", "", ""]},
                {"label": "1980-2007 Mean Shock", "coefficients": ["-0.01", "0.74", "-3.00", "2.75"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Quarterly Observations", "values": ["192", "192", "192", "192"]},
        ],
        "notes": "Narrative shocks identified from Federal Reserve records, Greenbook forecasts, and FOMC minutes.",
        "qa": [
            {"question": "How many narrative monetary policy episodes are identified?", "answer": "24"},
            {"question": "What is the standard deviation of the narrative shock over the full sample?", "answer": "0.82"},
            {"question": "What is the minimum narrative shock value?", "answer": "-3.00"},
        ],
    })

    var_estimates = render_regression_table({
        "table_id": "var-estimates",
        "caption": "SVAR Coefficient Estimates",
        "label": "tab:var-estimates",
        "model_labels": ["Output", "Prices", "Fed Funds", "Unemployment"],
        "panels": [{
            "dep_var": "Own Lag 1 Coefficients",
            "variables": [
                {"label": "Lag 1 (own)", "coefficients": ["0.812***", "0.941***", "0.781***", "0.921***"],
                 "std_errors": ["(0.041)", "(0.028)", "(0.051)", "(0.032)"]},
                {"label": "Lag 2 (own)", "coefficients": ["0.084**", "0.041*", "0.091**", "0.051*"],
                 "std_errors": ["(0.038)", "(0.024)", "(0.044)", "(0.028)"]},
                {"label": "Lag 3 (own)", "coefficients": ["0.021", "0.018", "0.028", "0.024"],
                 "std_errors": ["(0.036)", "(0.022)", "(0.041)", "(0.026)"]},
                {"label": "Lag 4 (own)", "coefficients": ["-0.018", "0.012", "-0.024", "0.018"],
                 "std_errors": ["(0.034)", "(0.021)", "(0.039)", "(0.025)"]},
            ],
        }],
        "controls": [
            {"label": "Constant", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Lags", "values": ["4", "4", "4", "4"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["188", "188", "188", "188"]},
            {"label": "R-squared", "values": ["0.941", "0.978", "0.892", "0.961"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. SVAR estimated by OLS equation-by-equation. Newey-West SEs.",
        "qa": [
            {"question": "What is the first own-lag coefficient for output?", "answer": "0.812"},
            {"question": "What is the R-squared for the prices equation?", "answer": "0.978"},
        ],
    })

    irf_output = render_regression_table({
        "table_id": "impulse-responses-output",
        "caption": "Impulse Response: Effect of Monetary Shock on Output",
        "label": "tab:irf-output",
        "model_labels": ["h=1", "h=4", "h=8", "h=12"],
        "panels": [{
            "dep_var": "Response of Log Output to +100bp Monetary Shock",
            "variables": [
                {"label": "Point Estimate", "coefficients": ["-0.021", "-0.184***", "-0.312***", "-0.218**"],
                 "std_errors": ["(0.018)", "(0.048)", "(0.071)", "(0.094)"]},
                {"label": "90\\% CI Lower", "coefficients": ["-0.051", "-0.264", "-0.428", "-0.371"],
                 "std_errors": ["", "", "", ""]},
                {"label": "90\\% CI Upper", "coefficients": ["0.009", "-0.104", "-0.196", "-0.065"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "*** p<0.01, ** p<0.05. Bootstrap confidence intervals from 10,000 draws. Shock normalized to 100bp.",
        "qa": [
            {"question": "What is the peak output response to a 100bp monetary shock?", "answer": "-0.312 at h=8"},
            {"question": "What is the output response at h=4?", "answer": "-0.184"},
        ],
    })

    irf_prices = render_regression_table({
        "table_id": "impulse-responses-prices",
        "caption": "Impulse Response: Effect of Monetary Shock on Prices",
        "label": "tab:irf-prices",
        "model_labels": ["h=1", "h=4", "h=8", "h=12"],
        "panels": [{
            "dep_var": "Response of Log CPI to +100bp Monetary Shock",
            "variables": [
                {"label": "Point Estimate", "coefficients": ["0.008", "-0.042", "-0.198***", "-0.341***"],
                 "std_errors": ["(0.012)", "(0.038)", "(0.062)", "(0.089)"]},
                {"label": "90\\% CI Lower", "coefficients": ["-0.014", "-0.112", "-0.300", "-0.485"],
                 "std_errors": ["", "", "", ""]},
                {"label": "90\\% CI Upper", "coefficients": ["0.030", "0.028", "-0.096", "-0.197"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "*** p<0.01. Price puzzle: slight positive price response at h=1 before eventual decline.",
        "qa": [
            {"question": "What is the price response at h=12?", "answer": "-0.341"},
            {"question": "What is the price response at h=8?", "answer": "-0.198"},
        ],
    })

    irf_interest = render_regression_table({
        "table_id": "impulse-responses-interest",
        "caption": "Impulse Response: Effect of Monetary Shock on Federal Funds Rate",
        "label": "tab:irf-interest",
        "model_labels": ["h=1", "h=4", "h=8", "h=12"],
        "panels": [{
            "dep_var": "Response of Federal Funds Rate to +100bp Shock",
            "variables": [
                {"label": "Point Estimate", "coefficients": ["0.841***", "0.412***", "0.148**", "-0.021"],
                 "std_errors": ["(0.048)", "(0.071)", "(0.068)", "(0.081)"]},
                {"label": "90\\% CI Lower", "coefficients": ["0.761", "0.292", "0.034", "-0.154"],
                 "std_errors": ["", "", "", ""]},
                {"label": "90\\% CI Upper", "coefficients": ["0.921", "0.532", "0.262", "0.112"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "*** p<0.01, ** p<0.05. Rate returns to baseline within 3 years.",
        "qa": [
            {"question": "What is the interest rate response at h=1?", "answer": "0.841"},
            {"question": "What is the interest rate response at h=8?", "answer": "0.148"},
        ],
    })

    forecast_errors = render_regression_table({
        "table_id": "forecast-errors",
        "caption": "Forecast Error Regression: Narrative Identification",
        "label": "tab:forecast-errors",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Federal Funds Rate Change",
            "variables": [
                {"label": "Narrative Shock", "coefficients": ["0.891***", "0.872***", "0.864***", "0.851***"],
                 "std_errors": ["(0.041)", "(0.039)", "(0.042)", "(0.040)"]},
                {"label": "Greenbook Forecast (output)", "coefficients": ["--", "0.124**", "0.118**", "0.112**"],
                 "std_errors": ["", "(0.051)", "(0.053)", "(0.050)"]},
                {"label": "Greenbook Forecast (inflation)", "coefficients": ["--", "--", "0.084*", "0.081*"],
                 "std_errors": ["", "", "(0.044)", "(0.042)"]},
            ],
        }],
        "controls": [
            {"label": "Lagged FFR", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["192", "192", "192", "192"]},
            {"label": "R-squared", "values": ["0.621", "0.648", "0.661", "0.678"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Narrative shock predicts realized FFR changes after controlling for Fed forecasts.",
        "qa": [
            {"question": "What is the coefficient on the narrative shock in column 1?", "answer": "0.891"},
            {"question": "What is the R-squared in column 4?", "answer": "0.678"},
        ],
    })

    variance_decomp = render_regression_table({
        "table_id": "variance-decomposition",
        "caption": "Forecast Error Variance Decomposition (\\%)",
        "label": "tab:variance-decomp",
        "model_labels": ["h=1", "h=4", "h=8", "h=16"],
        "panels": [{
            "dep_var": "Share of variance explained by monetary shock",
            "variables": [
                {"label": "Output", "coefficients": ["3.2", "18.4", "24.1", "19.8"],
                 "std_errors": ["(1.4)", "(4.2)", "(5.1)", "(4.8)"]},
                {"label": "Prices", "coefficients": ["1.8", "8.4", "14.2", "18.1"],
                 "std_errors": ["(0.9)", "(2.8)", "(3.9)", "(4.2)"]},
                {"label": "Fed Funds Rate", "coefficients": ["42.1", "31.8", "22.4", "14.1"],
                 "std_errors": ["(6.1)", "(5.8)", "(5.2)", "(4.1)"]},
                {"label": "Unemployment", "coefficients": ["2.4", "12.1", "18.8", "15.4"],
                 "std_errors": ["(1.2)", "(3.4)", "(4.4)", "(4.1)"]},
            ],
        }],
        "notes": "Bootstrap standard errors in parentheses. Monetary shock explains up to 24\\% of output forecast error variance.",
        "qa": [
            {"question": "What share of output variance is explained by the monetary shock at h=8?", "answer": "24.1"},
            {"question": "What share of price variance is explained by the monetary shock at h=16?", "answer": "18.1"},
        ],
    })

    subperiod_1960 = render_regression_table({
        "table_id": "sub-period-1960-1979",
        "caption": "Sub-Period Analysis: 1960-1979",
        "label": "tab:subperiod-1960",
        "model_labels": ["Output h=8", "Prices h=12", "FFR h=1", "Unemp h=8"],
        "panels": [{
            "dep_var": "IRF Point Estimates (1960-1979)",
            "variables": [
                {"label": "Monetary Shock (+100bp)", "coefficients": ["-0.284***", "-0.318***", "0.812***", "0.241***"],
                 "std_errors": ["(0.084)", "(0.101)", "(0.058)", "(0.071)"]},
            ],
        }],
        "notes": "*** p<0.01. Pre-Volcker period: larger real effects, slower price adjustment.",
        "qa": [
            {"question": "What is the output effect at h=8 in the 1960-1979 subsample?", "answer": "-0.284"},
        ],
    })

    subperiod_1980 = render_regression_table({
        "table_id": "sub-period-1980-2007",
        "caption": "Sub-Period Analysis: 1980-2007",
        "label": "tab:subperiod-1980",
        "model_labels": ["Output h=8", "Prices h=12", "FFR h=1", "Unemp h=8"],
        "panels": [{
            "dep_var": "IRF Point Estimates (1980-2007)",
            "variables": [
                {"label": "Monetary Shock (+100bp)", "coefficients": ["-0.341***", "-0.362***", "0.871***", "0.284***"],
                 "std_errors": ["(0.094)", "(0.108)", "(0.061)", "(0.078)"]},
            ],
        }],
        "notes": "*** p<0.01. Post-Volcker period: comparable real effects, faster price adjustment.",
        "qa": [
            {"question": "What is the output effect at h=8 in the 1980-2007 subsample?", "answer": "-0.341"},
            {"question": "What is the FFR response at h=1 in the 1980-2007 subsample?", "answer": "0.871"},
        ],
    })

    robust_lag = render_regression_table({
        "table_id": "robustness-lag-length",
        "caption": "Robustness: Alternative Lag Lengths",
        "label": "tab:robust-lag",
        "model_labels": ["2 Lags", "4 Lags", "6 Lags", "8 Lags"],
        "panels": [{
            "dep_var": "Output IRF at h=8",
            "variables": [
                {"label": "Monetary Shock (+100bp)", "coefficients": ["-0.284***", "-0.312***", "-0.298***", "-0.301***"],
                 "std_errors": ["(0.068)", "(0.071)", "(0.074)", "(0.078)"]},
            ],
        }],
        "notes": "*** p<0.01. Results robust to choice of lag length. Baseline: 4 lags.",
        "qa": [
            {"question": "What is the output IRF at h=8 with 4 lags?", "answer": "-0.312"},
            {"question": "What is the output IRF at h=8 with 6 lags?", "answer": "-0.298"},
        ],
    })

    robust_order = render_regression_table({
        "table_id": "robustness-ordering",
        "caption": "Robustness: Alternative Cholesky Orderings",
        "label": "tab:robust-ordering",
        "model_labels": ["Baseline", "Alt 1", "Alt 2", "Alt 3"],
        "panels": [{
            "dep_var": "Output IRF at h=8",
            "variables": [
                {"label": "Monetary Shock (+100bp)", "coefficients": ["-0.312***", "-0.298***", "-0.321***", "-0.304***"],
                 "std_errors": ["(0.071)", "(0.074)", "(0.069)", "(0.073)"]},
            ],
        }],
        "notes": "*** p<0.01. Baseline: output, prices, FFR, unemployment. Alt orderings permute positions of output and prices.",
        "qa": [
            {"question": "What is the output IRF at h=8 with baseline ordering?", "answer": "-0.312"},
            {"question": "What is the output IRF with Alt 2 ordering?", "answer": "-0.321"},
        ],
    })

    narrative_dates = render_regression_table({
        "table_id": "appendix-narrative-dates",
        "caption": "Appendix: Narrative Monetary Policy Episode Dates",
        "label": "tab:narrative-dates",
        "model_labels": ["Date", "Fed Funds Chg", "Narrative Shock", "Episode Type"],
        "panels": [{
            "dep_var": "Selected Narrative Episodes",
            "variables": [
                {"label": "1968 Q4", "coefficients": ["1968Q4", "+0.50", "+0.42", "Contraction"],
                 "std_errors": ["", "", "", ""]},
                {"label": "1974 Q2", "coefficients": ["1974Q2", "+1.25", "+1.18", "Contraction"],
                 "std_errors": ["", "", "", ""]},
                {"label": "1979 Q4", "coefficients": ["1979Q4", "+3.50", "+3.21", "Contraction"],
                 "std_errors": ["", "", "", ""]},
                {"label": "1982 Q4", "coefficients": ["1982Q4", "-2.75", "-2.51", "Expansion"],
                 "std_errors": ["", "", "", ""]},
                {"label": "2001 Q1", "coefficients": ["2001Q1", "-0.50", "-0.44", "Expansion"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Selected major narrative episodes. Full list in Online Appendix.",
        "qa": [
            {"question": "What is the narrative shock size in 1979 Q4?", "answer": "+3.21"},
            {"question": "What type of episode was 1982 Q4?", "answer": "Expansion"},
        ],
    })

    # --- Equations ---
    eq_svar = EquationSpec(
        "svar-model",
        r"A_0 y_t = A_1 y_{t-1} + \cdots + A_p y_{t-p} + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, I), \quad \mathcal{F}_t = \sigma(y_{t}, y_{t-1}, \ldots)",
        "eq:svar",
        "Structural VAR model with $p$ lags. $A_0$ is the contemporaneous impact matrix; $\\varepsilon_t$ are structural shocks.",
        [{"question": "What assumption on epsilon_t identifies the SVAR?", "answer": "Structural shocks are orthonormal: Var(epsilon_t) = I"}],
    )

    eq_structural_shocks = EquationSpec(
        "structural-shocks",
        r"u_t = A_0^{-1} \varepsilon_t, \quad E[u_t u_t'] = A_0^{-1}(A_0^{-1})' = \Sigma_u",
        "eq:structural-shocks",
        "Relationship between reduced-form residuals $u_t$ and structural shocks $\\varepsilon_t$.",
    )

    eq_irf = EquationSpec(
        "irf",
        r"\text{IRF}(h) = \Phi_h A_0^{-1} e_i, \quad \hat{\Phi}_h \xrightarrow{d} \Phi_h \text{ as } T \to \infty, \quad \overset{p}{\to} \text{ under } \mathcal{F}_t\text{-measurability}",
        "eq:irf",
        "Impulse response function at horizon $h$: $\\Phi_h$ is the $h$-step coefficient matrix, $e_i$ selects shock $i$.",
    )

    eq_cholesky = EquationSpec(
        "cholesky",
        r"A_0 = P^{-1}, \quad \Sigma_u = PP', \quad P \text{ lower triangular}",
        "eq:cholesky",
        "Cholesky decomposition identification: $P$ is the lower-triangular Cholesky factor of the covariance matrix.",
    )

    eq_narrative = EquationSpec(
        "narrative-restriction",
        r"\varepsilon_t^m = s_t^{NR}, \quad s_t^{NR} = \Delta i_t - E_{t-1}[\Delta i_t]",
        "eq:narrative",
        "Narrative identification: monetary shock equals the change in policy rate minus the Fed's own forecast.",
    )

    eq_forecast = EquationSpec(
        "forecast-equation",
        r"\Delta i_t = \alpha + \beta s_t^{NR} + \gamma' \mathbf{f}_t + \eta_t",
        "eq:forecast",
        "Forecast equation: FFR change regressed on narrative shock and Greenbook macro forecasts $\\mathbf{f}_t$.",
    )

    eq_variance_decomp = EquationSpec(
        "variance-decomp-formula",
        r"\text{FEVD}_k(h) = \frac{e_k' \left(\sum_{j=0}^h \Phi_j A_0^{-1} e_i e_i' (A_0^{-1})' \Phi_j'\right) e_k}{\iint_{\mathcal{F}_t} \text{Var}(y_{k,t+h} \mid \mathcal{F}_t)\, d\mu(t)\, d\nu(k)}",
        "eq:fevd",
        "Forecast error variance decomposition: share of $y_k$ forecast error at horizon $h$ due to shock $i$.",
    )

    eq_policy_rule = EquationSpec(
        "monetary-policy-rule",
        r"i_t = \rho i_{t-1} + (1-\rho)[\phi_\pi \pi_t + \phi_y y_t] + \varepsilon_t^m",
        "eq:policy-rule",
        "Taylor-type monetary policy rule with interest rate smoothing $\\rho$.",
    )

    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[SVAR Identification: Order and Rank Conditions]
The SVAR $A_0 y_t = \sum_{l=1}^p A_l y_{t-l} + \varepsilon_t$ with $n$ variables requires $n(n-1)/2$ restrictions on $A_0$ for exact identification. The Cholesky decomposition imposes $n(n-1)/2$ zero restrictions on the upper triangle of $A_0^{-1}$, achieving exact identification.

The rank condition requires that the Jacobian of the moment conditions $E[\text{vech}(u_t u_t')] = \text{vech}(\Sigma_u)$ with respect to $\text{vech}(A_0)$ has full column rank at the true parameter value.
\end{proposition}

\begin{proof}
The reduced-form covariance is $\Sigma_u = (A_0)^{-1} (A_0^{-1})'$. The system $\Sigma_u = PP'$ (with $P$ lower triangular) has a unique solution for $P$ by the Cholesky factorization theorem, given $\Sigma_u$ positive definite. Therefore $A_0 = P^{-1}$ is uniquely identified.

For the rank condition: let $\mathcal{L} = \{A_0 : A_0^{-1} \text{ lower triangular}\}$. The map $f: \mathcal{L} \to \mathcal{S}_{++}^n$, $f(A_0) = (A_0 A_0')^{-1}$, has Jacobian
\begin{align}
Df(A_0)[dA_0] &= -(A_0 A_0')^{-1} (dA_0 \cdot A_0' + A_0 \cdot dA_0')(A_0 A_0')^{-1},
\end{align}
which has full column rank $n(n+1)/2$ at the lower triangular $A_0$.
\end{proof}

\begin{proposition}[IRF Confidence Band Derivation]
Let $\hat{\theta} = (\hat{A}_1, \ldots, \hat{A}_p, \hat{\Sigma}_u)$ be the OLS estimates. Under standard regularity conditions,
\begin{align}
\sqrt{T}(\hat{\theta} - \theta_0) &\xrightarrow{d} \mathcal{N}(0, V),
\end{align}
and by the delta method,
\begin{align}
\sqrt{T}(\widehat{\text{IRF}}(h) - \text{IRF}(h)) &\xrightarrow{d} \mathcal{N}(0, G_h V G_h'),
\end{align}
where $G_h = \partial \text{IRF}(h) / \partial \theta'$ is the IRF gradient. Confidence bands are constructed as $\widehat{\text{IRF}}(h) \pm z_{0.95} \cdot \sqrt{\hat{G}_h \hat{V} \hat{G}_h' / T}$.
\end{proposition}

\begin{proposition}[Narrative Restriction as Inequality Constraint]
The narrative identification approach (Romer and Romer 2004) imposes the restriction that the monetary shock is the component of policy changes unexplained by the Fed's information set:
\begin{align}
s_t^{NR} &= \Delta i_t - E[\Delta i_t \mid \mathcal{I}_t^{Fed}],
\end{align}
where $\mathcal{I}_t^{Fed}$ includes Greenbook forecasts. Under the assumption that $\text{Cov}(s_t^{NR}, \varepsilon_t^{non-m}) = 0$, this identifies the monetary policy shock.

The narrative restriction can be written as a set of sign restrictions:
\begin{align}
s_t^{NR} > 0 &\implies \varepsilon_t^m > 0, \\
s_t^{NR} < 0 &\implies \varepsilon_t^m < 0,
\end{align}
which are not-set-identifying in general but become point-identifying when combined with the linearity assumption $\varepsilon_t^m = \beta s_t^{NR} + \eta_t$ with $E[\eta_t | s_t^{NR}] = 0$.
\end{proposition}

\noindent\textbf{Spectral representation.} The spectral density of the SVAR process can be written as a double integral over the filtration $\mathcal{F}_t$:
\begin{align}
S_{yy}(\omega) &= \frac{1}{2\pi} \iint_{-\pi}^{\pi} A(e^{-i\omega})^{-1} \Sigma_\varepsilon \left(A(e^{i\omega})^{-1}\right)' \, d\omega\, d\lambda.
\end{align}
The parameter estimates satisfy the convergence $\hat{A}_0 \xrightarrow{d} A_0$ and $\hat{\Phi}_h \overset{p}{\to} \Phi_h$ under the $\mathcal{F}_t$-adapted regularity conditions.
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-macro",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-macro", text_paragraphs=21, equations=[eq_policy_rule])

    historical_bg = SectionSpec(
        "Historical Background", "sec:hist-bg", text_paragraphs=17,
        tables=[narrative_summary],
        subsections=[
            SectionSpec("Federal Reserve Policy History", "sec:hist-fed", level=2, text_paragraphs=10),
            SectionSpec("Narrative Sources", "sec:hist-narrative", level=2, text_paragraphs=9),
        ],
    )

    svar_framework = SectionSpec(
        "SVAR Framework", "sec:svar", text_paragraphs=18,
        equations=[eq_svar, eq_structural_shocks],
        subsections=[
            SectionSpec("Model Specification", "sec:svar-spec", level=2, text_paragraphs=11),
            SectionSpec("Estimation", "sec:svar-est", level=2, text_paragraphs=10),
        ],
    )

    narrative_id = SectionSpec(
        "Narrative Identification", "sec:narrative-id", text_paragraphs=18,
        equations=[eq_cholesky, eq_narrative, eq_forecast],
        tables=[forecast_errors],
        subsections=[
            SectionSpec("Construction of Narrative Shocks", "sec:narrative-construct", level=2, text_paragraphs=8),
            SectionSpec("Exogeneity of Narrative Shocks", "sec:narrative-exog", level=2, text_paragraphs=8),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-macro", text_paragraphs=10,
        subsections=[
            SectionSpec("Macroeconomic Time Series", "sec:data-ts", level=2, text_paragraphs=7),
            SectionSpec("Greenbook Forecast Data", "sec:data-gb", level=2, text_paragraphs=6),
        ],
    )

    results = SectionSpec(
        "Results", "sec:results-macro", text_paragraphs=13,
        tables=[var_estimates, irf_output, irf_prices, irf_interest, variance_decomp],
        equations=[eq_irf, eq_variance_decomp],
        subsections=[
            SectionSpec("Impulse Responses: Output", "sec:results-output", level=2, text_paragraphs=8),
            SectionSpec("Impulse Responses: Prices", "sec:results-prices", level=2, text_paragraphs=7),
            SectionSpec("Variance Decomposition", "sec:results-fevd", level=2, text_paragraphs=7),
        ],
    )

    robustness = SectionSpec(
        "Robustness", "sec:robust-macro", text_paragraphs=10,
        tables=[subperiod_1960, subperiod_1980, robust_lag, robust_order],
        subsections=[
            SectionSpec("Sub-Period Analysis", "sec:robust-subperiod", level=2, text_paragraphs=8),
            SectionSpec("Alternative Lag Lengths", "sec:robust-lags", level=2, text_paragraphs=7),
            SectionSpec("Alternative Orderings", "sec:robust-order", level=2, text_paragraphs=7),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-macro", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: SVAR Theory", "sec:appendix-a-macro", text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Narrative Classification", "sec:appendix-b-macro", text_paragraphs=5,
        tables=[narrative_dates],
    )

    appendix_c = SectionSpec(
        "Appendix C: Additional IRFs", "sec:appendix-c-macro", text_paragraphs=4,
    )

    return PaperSpec(
        paper_id="06",
        field_slug="macroeconomics",
        title="Monetary Policy Shocks and the Macroeconomy: Narrative Identification in a Structural VAR",
        authors="Valentina Cruz, Obinna Okafor, Lars Bergstrom",
        journal_style="jf",
        abstract=(
            "We identify monetary policy shocks using a narrative approach based on Federal Reserve records "
            "and Greenbook forecasts over 1960-2007. Embedding these shocks in a structural VAR, we find "
            "that a 100 basis point contractionary shock reduces output by a peak of 0.312 log points at "
            "eight quarters, with prices declining by 0.341 log points at twelve quarters. The monetary "
            "shock accounts for up to 24\\% of output forecast error variance. Results are robust to "
            "alternative lag lengths, Cholesky orderings, and sub-period analysis. SVAR identification "
            "conditions are formally verified."
        ),
        sections=[intro, historical_bg, svar_framework, narrative_id, data, results, robustness,
                  conclusion, appendix_a, appendix_b, appendix_c],
        bibliography_entries=[
            r"\bibitem{romer2004} Romer, C. D. and Romer, D. H. (2004). A New Measure of Monetary Shocks: Derivation and Implications. \textit{American Economic Review}, 94(4), 1055--1084.",
            r"\bibitem{sims1980} Sims, C. A. (1980). Macroeconomics and Reality. \textit{Econometrica}, 48(1), 1--48.",
            r"\bibitem{christiano1999} Christiano, L. J., Eichenbaum, M., and Evans, C. L. (1999). Monetary Policy Shocks: What Have We Learned and to What End? \textit{Handbook of Macroeconomics}, 1, 65--148.",
            r"\bibitem{stock2018} Stock, J. H. and Watson, M. W. (2018). Identification and Estimation of Dynamic Causal Effects in Macroeconomics Using External Instruments. \textit{Economic Journal}, 128(610), 917--948.",
            r"\bibitem{plagborg2021} Plagborg-Moller, M. and Wolf, C. K. (2021). Local Projections and VARs Estimate the Same Impulse Responses. \textit{Econometrica}, 89(2), 955--980.",
            r"\bibitem{lutkepohl2005} Lutkepohl, H. (2005). \textit{New Introduction to Multiple Time Series Analysis}. Springer.",
            r"\bibitem{gertler2015} Gertler, M. and Karadi, P. (2015). Monetary Policy Surprises, Credit Costs, and Economic Activity. \textit{American Economic Journal: Macroeconomics}, 7(1), 44--76.",
        ],
        target_pages=60,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "Narrative identification using Federal Reserve records and Greenbook forecasts to construct exogenous monetary policy shocks"},
            {"question": "What is the peak output response to a 100bp monetary shock?", "answer": "-0.312 log points at h=8 quarters"},
            {"question": "What is the price response at h=12?", "answer": "-0.341 log points"},
            {"question": "What share of output forecast error variance is explained by the monetary shock at h=8?", "answer": "24.1 percent"},
            {"question": "How many narrative monetary policy episodes are identified?", "answer": "24"},
        ],
    )


PAPER_BUILDERS["06"] = _paper_06_macro
