#!/usr/bin/env python3
"""Paper builder for paper 05 (IO)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)

def _paper_05_io() -> PaperSpec:
    # --- Tables ---
    market_summary = render_regression_table({
        "table_id": "market-summary-stats",
        "caption": "Market-Level Summary Statistics",
        "label": "tab:market-summary",
        "model_labels": ["Mean", "SD", "p10", "p90"],
        "panels": [{
            "dep_var": "Panel A: Market Characteristics",
            "variables": [
                {"label": "Number of Products", "coefficients": ["24.3", "8.1", "14", "35"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Market Share (leader)", "coefficients": ["0.312", "0.142", "0.148", "0.491"],
                 "std_errors": ["", "", "", ""]},
                {"label": "HHI", "coefficients": ["0.218", "0.091", "0.118", "0.341"],
                 "std_errors": ["", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Pricing",
            "variables": [
                {"label": "Price (\\$)", "coefficients": ["24.81", "12.41", "10.50", "41.20"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Price-Cost Margin (\\%)", "coefficients": ["34.2", "18.1", "14.1", "58.4"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Markets", "values": ["342", "342", "342", "342"]},
            {"label": "Products", "values": ["8,321", "8,321", "8,321", "8,321"]},
        ],
        "notes": "Sample covers 342 geographic markets across 18 quarters. Price in constant 2010 dollars.",
        "qa": [
            {"question": "What is the mean number of products per market?", "answer": "24.3"},
            {"question": "How many markets are in the sample?", "answer": "342"},
            {"question": "What is the mean market HHI?", "answer": "0.218"},
        ],
    })

    product_chars = render_regression_table({
        "table_id": "product-characteristics",
        "caption": "Product Characteristics Summary",
        "label": "tab:product-chars",
        "model_labels": ["Mean", "SD", "Min", "Max"],
        "panels": [{
            "dep_var": "Continuous Characteristics",
            "variables": [
                {"label": "Quality Index (0-10)", "coefficients": ["6.42", "1.84", "1.20", "9.91"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Space (cu ft)", "coefficients": ["18.4", "6.2", "6.1", "34.8"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Energy Star Rating", "coefficients": ["3.21", "1.14", "1.00", "5.00"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Products", "values": ["8,321", "8,321", "8,321", "8,321"]},
        ],
        "notes": "Product characteristics from manufacturer spec sheets matched to retail scanner data.",
        "qa": [
            {"question": "What is the mean quality index?", "answer": "6.42"},
            {"question": "What is the mean space (cu ft) of a product?", "answer": "18.4"},
        ],
    })

    demand_logit = render_regression_table({
        "table_id": "demand-estimates-logit",
        "caption": "Demand Estimates: Simple Logit",
        "label": "tab:demand-logit",
        "model_labels": ["OLS", "IV", "IV", "IV"],
        "panels": [{
            "dep_var": "Dep. var.: Log Market Share Ratio",
            "variables": [
                {"label": "Price", "coefficients": ["-0.041***", "-0.182***", "-0.171***", "-0.164***"],
                 "std_errors": ["(0.006)", "(0.031)", "(0.029)", "(0.027)"]},
                {"label": "Quality", "coefficients": ["0.318***", "0.341***", "0.328***", "0.319***"],
                 "std_errors": ["(0.028)", "(0.031)", "(0.029)", "(0.027)"]},
                {"label": "Space", "coefficients": ["0.024***", "0.027***", "0.025***", "0.024***"],
                 "std_errors": ["(0.004)", "(0.005)", "(0.004)", "(0.004)"]},
                {"label": "Energy Star", "coefficients": ["0.112***", "0.118***", "0.114***", "0.111***"],
                 "std_errors": ["(0.019)", "(0.021)", "(0.020)", "(0.018)"]},
            ],
        }],
        "controls": [
            {"label": "Market FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Quarter FE", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "Brand FE", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["149,778", "149,778", "149,778", "149,778"]},
            {"label": "R-squared", "values": ["0.741", "", "", ""]},
        ],
        "notes": "*** p<0.01. Instruments: BLP instruments (sum of other products' characteristics). Market-clustered SEs.",
        "qa": [
            {"question": "What is the OLS price coefficient in the logit model?", "answer": "-0.041"},
            {"question": "What is the IV price coefficient in column 2?", "answer": "-0.182"},
            {"question": "What is the quality coefficient in column 1 OLS?", "answer": "0.318"},
        ],
    })

    demand_rc = render_regression_table({
        "table_id": "demand-estimates-rc-logit",
        "caption": "Demand Estimates: Random Coefficients Logit (BLP)",
        "label": "tab:demand-rc",
        "model_labels": ["Mean $\\bar{\\beta}$", "SD $\\sigma$", "t-stat ($\\bar{\\beta}$)", "t-stat ($\\sigma$)"],
        "panels": [{
            "dep_var": "Random Coefficients Logit Estimates",
            "variables": [
                {"label": "Price", "coefficients": ["-0.241", "0.118", "-7.82", "4.21"],
                 "std_errors": ["(0.031)", "(0.028)", "", ""]},
                {"label": "Quality", "coefficients": ["0.384", "0.142", "12.41", "5.81"],
                 "std_errors": ["(0.031)", "(0.024)", "", ""]},
                {"label": "Space", "coefficients": ["0.031", "0.014", "7.41", "3.62"],
                 "std_errors": ["(0.004)", "(0.004)", "", ""]},
                {"label": "Energy Star", "coefficients": ["0.128", "0.041", "6.12", "2.91"],
                 "std_errors": ["(0.021)", "(0.014)", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["149,778", "149,778", "149,778", "149,778"]},
            {"label": "GMM Objective", "values": ["18.42", "18.42", "18.42", "18.42"]},
            {"label": "Overid. p-value", "values": ["0.318", "0.318", "0.318", "0.318"]},
        ],
        "notes": "BLP random coefficients logit. Instruments: BLP + Hausman price instruments. Markets pooled.",
        "qa": [
            {"question": "What is the mean price coefficient in the RC logit?", "answer": "-0.241"},
            {"question": "What is the standard deviation of the price coefficient?", "answer": "0.118"},
            {"question": "What is the overidentification test p-value?", "answer": "0.318"},
        ],
    })

    own_elas = render_regression_table({
        "table_id": "own-price-elasticities",
        "caption": "Own-Price Elasticities by Segment",
        "label": "tab:own-elas",
        "model_labels": ["Logit", "RC Logit", "Nested Logit", "RC Nested"],
        "panels": [{
            "dep_var": "Mean Own-Price Elasticity by Segment",
            "variables": [
                {"label": "Budget Segment", "coefficients": ["-3.21", "-4.18", "-3.84", "-4.41"],
                 "std_errors": ["(0.18)", "(0.31)", "(0.24)", "(0.38)"]},
                {"label": "Mid Segment", "coefficients": ["-2.84", "-3.61", "-3.42", "-3.88"],
                 "std_errors": ["(0.16)", "(0.27)", "(0.21)", "(0.34)"]},
                {"label": "Premium Segment", "coefficients": ["-2.41", "-3.14", "-2.98", "-3.31"],
                 "std_errors": ["(0.14)", "(0.24)", "(0.19)", "(0.31)"]},
                {"label": "All Products", "coefficients": ["-2.91", "-3.71", "-3.42", "-3.94"],
                 "std_errors": ["(0.17)", "(0.28)", "(0.22)", "(0.35)"]},
            ],
        }],
        "notes": "Elasticities evaluated at sample means. Bootstrap standard errors in parentheses.",
        "qa": [
            {"question": "What is the mean own-price elasticity for all products in the RC logit?", "answer": "-3.71"},
            {"question": "What is the own-price elasticity for the budget segment in the RC logit?", "answer": "-4.18"},
        ],
    })

    cross_elas = render_regression_table({
        "table_id": "cross-price-elasticities",
        "caption": "Cross-Price Elasticities: Selected Products",
        "label": "tab:cross-elas",
        "model_labels": ["Product A", "Product B", "Product C", "Product D"],
        "panels": [{
            "dep_var": "Cross-price elasticity matrix (RC Logit)",
            "variables": [
                {"label": "Product A price", "coefficients": ["-3.84", "0.028", "0.019", "0.011"],
                 "std_errors": ["(0.31)", "(0.004)", "(0.003)", "(0.002)"]},
                {"label": "Product B price", "coefficients": ["0.031", "-3.61", "0.024", "0.014"],
                 "std_errors": ["(0.004)", "(0.27)", "(0.003)", "(0.002)"]},
                {"label": "Product C price", "coefficients": ["0.021", "0.026", "-3.42", "0.018"],
                 "std_errors": ["(0.003)", "(0.004)", "(0.28)", "(0.003)"]},
                {"label": "Product D price", "coefficients": ["0.012", "0.015", "0.019", "-3.14"],
                 "std_errors": ["(0.002)", "(0.002)", "(0.003)", "(0.28)"]},
            ],
        }],
        "notes": "RC Logit estimates. Own-price elasticities on diagonal; cross-price elasticities off diagonal.",
        "qa": [
            {"question": "What is the cross-price elasticity of Product A demand with respect to Product B price?", "answer": "0.031"},
            {"question": "What is the own-price elasticity of Product C?", "answer": "-3.42"},
        ],
    })

    mc_bias = render_regression_table({
        "table_id": "monte-carlo-bias",
        "caption": "Monte Carlo: Bias of Estimators",
        "label": "tab:mc-bias",
        "model_labels": ["N=200", "N=500", "N=1000", "N=5000"],
        "panels": [{
            "dep_var": "Bias in Price Coefficient ($\\times 100$)",
            "variables": [
                {"label": "OLS", "coefficients": ["41.2", "40.8", "41.1", "40.9"],
                 "std_errors": ["(2.1)", "(1.4)", "(1.0)", "(0.4)"]},
                {"label": "BLP (BLP Instruments)", "coefficients": ["1.8", "1.2", "0.8", "0.3"],
                 "std_errors": ["(1.9)", "(1.3)", "(0.9)", "(0.4)"]},
                {"label": "BLP (Optimal Instruments)", "coefficients": ["0.9", "0.6", "0.4", "0.1"],
                 "std_errors": ["(1.8)", "(1.2)", "(0.8)", "(0.3)"]},
            ],
        }],
        "notes": "1000 Monte Carlo replications. True $\\bar{\\beta}_p = -0.241$, $\\sigma_p = 0.118$.",
        "qa": [
            {"question": "What is the OLS bias in the price coefficient at N=1000?", "answer": "41.1"},
            {"question": "What is the BLP bias with optimal instruments at N=5000?", "answer": "0.1"},
        ],
    })

    mc_coverage = render_regression_table({
        "table_id": "monte-carlo-coverage",
        "caption": "Monte Carlo: Coverage Rates of 95\\% Confidence Intervals",
        "label": "tab:mc-coverage",
        "model_labels": ["N=200", "N=500", "N=1000", "N=5000"],
        "panels": [{
            "dep_var": "Coverage Rate (\\%)",
            "variables": [
                {"label": "BLP (BLP Instruments)", "coefficients": ["88.4", "91.2", "93.1", "94.8"],
                 "std_errors": ["(1.0)", "(0.9)", "(0.8)", "(0.7)"]},
                {"label": "BLP (Optimal Instruments)", "coefficients": ["91.2", "93.4", "94.2", "94.9"],
                 "std_errors": ["(0.9)", "(0.8)", "(0.7)", "(0.7)"]},
            ],
        }],
        "notes": "Nominal coverage rate: 95\\%. BLP instruments achieve near-nominal coverage at $N \\geq 1000$.",
        "qa": [
            {"question": "What is the coverage rate for BLP with BLP instruments at N=1000?", "answer": "93.1"},
            {"question": "What is the coverage rate for BLP with optimal instruments at N=5000?", "answer": "94.9"},
        ],
    })

    counterfactual = render_regression_table({
        "table_id": "counterfactual-merger",
        "caption": "Merger Simulation: Price Effects",
        "label": "tab:merger",
        "model_labels": ["Logit", "RC Logit", "Nested", "RC Nested"],
        "panels": [{
            "dep_var": "Predicted Price Change from Merger (\\%)",
            "variables": [
                {"label": "Merging Firm A Products", "coefficients": ["4.12", "6.84", "5.91", "7.21"],
                 "std_errors": ["(0.38)", "(0.71)", "(0.54)", "(0.82)"]},
                {"label": "Merging Firm B Products", "coefficients": ["3.84", "6.41", "5.48", "6.78"],
                 "std_errors": ["(0.34)", "(0.64)", "(0.49)", "(0.74)"]},
                {"label": "Rival Products", "coefficients": ["1.21", "1.94", "1.68", "2.11"],
                 "std_errors": ["(0.14)", "(0.24)", "(0.19)", "(0.28)"]},
            ],
        }],
        "notes": "Bertrand-Nash merger simulation. RC Logit predicts larger price increases than simple logit.",
        "qa": [
            {"question": "What is the predicted price increase for Firm A products under RC Logit?", "answer": "6.84"},
            {"question": "What is the predicted price increase for rival products under logit?", "answer": "1.21"},
        ],
    })

    markups = render_regression_table({
        "table_id": "markups",
        "caption": "Estimated Markups",
        "label": "tab:markups",
        "model_labels": ["Logit", "RC Logit", "Nested", "Data (Acctg)"],
        "panels": [{
            "dep_var": "Price-Cost Markup (\\%)",
            "variables": [
                {"label": "Budget Segment", "coefficients": ["21.4", "28.1", "24.8", "25.2"],
                 "std_errors": ["(1.2)", "(2.1)", "(1.8)", "(3.1)"]},
                {"label": "Mid Segment", "coefficients": ["26.8", "33.4", "29.8", "30.4"],
                 "std_errors": ["(1.4)", "(2.4)", "(2.0)", "(3.4)"]},
                {"label": "Premium Segment", "coefficients": ["31.2", "38.4", "34.1", "36.8"],
                 "std_errors": ["(1.8)", "(2.8)", "(2.4)", "(3.8)"]},
            ],
        }],
        "notes": "RC Logit markups closest to accounting-based estimates. Bootstrap SEs in parentheses.",
        "qa": [
            {"question": "What is the RC Logit markup for the premium segment?", "answer": "38.4"},
            {"question": "What is the accounting-based markup for the mid segment?", "answer": "30.4"},
        ],
    })

    welfare = render_regression_table({
        "table_id": "welfare-effects",
        "caption": "Welfare Effects of Proposed Merger",
        "label": "tab:welfare",
        "model_labels": ["Logit", "RC Logit", "Nested", "RC Nested"],
        "panels": [{
            "dep_var": "Welfare Change (\\$ per consumer per quarter)",
            "variables": [
                {"label": "Consumer Surplus Change", "coefficients": ["-1.84", "-3.12", "-2.68", "-3.41"],
                 "std_errors": ["(0.21)", "(0.38)", "(0.31)", "(0.44)"]},
                {"label": "Producer Surplus Change", "coefficients": ["2.41", "3.84", "3.21", "4.12"],
                 "std_errors": ["(0.28)", "(0.44)", "(0.38)", "(0.51)"]},
                {"label": "Total Welfare Change", "coefficients": ["0.57", "0.72", "0.53", "0.71"],
                 "std_errors": ["(0.14)", "(0.22)", "(0.18)", "(0.26)"]},
            ],
        }],
        "notes": "Compensating variation consumer surplus measure. RC Logit suggests larger welfare effects.",
        "qa": [
            {"question": "What is the consumer surplus change under RC Logit?", "answer": "-3.12"},
            {"question": "What is the total welfare change under RC Logit?", "answer": "0.72"},
        ],
    })

    appendix_instruments = render_regression_table({
        "table_id": "appendix-instruments",
        "caption": "Appendix: Instrument Relevance and Validity",
        "label": "tab:appendix-instruments",
        "model_labels": ["F-stat", "Partial R2", "Hansen J", "p-value"],
        "panels": [{
            "dep_var": "Instrument Diagnostics",
            "variables": [
                {"label": "BLP Instruments (own chars)", "coefficients": ["84.2", "0.182", "12.41", "0.412"],
                 "std_errors": ["", "", "", ""]},
                {"label": "BLP Instruments (rival chars)", "coefficients": ["91.4", "0.201", "11.84", "0.458"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Hausman Instruments", "coefficients": ["72.1", "0.161", "13.12", "0.361"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Optimal Instruments", "coefficients": ["142.8", "0.318", "8.41", "0.681"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "notes": "Optimal instruments constructed from nonparametric estimates of $E[\\partial s / \\partial \\theta]$.",
        "qa": [
            {"question": "What is the F-statistic for the optimal instruments?", "answer": "142.8"},
            {"question": "What is the Hansen J p-value for BLP own characteristics instruments?", "answer": "0.412"},
        ],
    })

    # --- Equations ---
    eq_utility = EquationSpec(
        "indirect-utility",
        r"u_{ijt} = \alpha_i p_{jt} + x_{jt}'\beta_i + \xi_{jt} + \varepsilon_{ijt}, \quad \alpha_i \sim \mathcal{N}\!\left(\bar{\alpha},\; \begin{bmatrix}\sigma_\alpha^2 & 0 \\ 0 & \sigma_\beta^2\end{bmatrix}\right), \quad \binom{J}{2} \text{ cross-elasticities}",
        "eq:utility",
        "Indirect utility of consumer $i$ for product $j$ in market $t$.",
        [{"question": "What does xi_jt capture?", "answer": "Unobserved product quality (demand-side unobservable)"}],
    )

    eq_shares = EquationSpec(
        "market-shares",
        r"s_{jt}(\delta, \Sigma) = \int \frac{\exp(\delta_{jt} + \mu_{ijt})}{1 + \sum_k \exp(\delta_{kt} + \mu_{ikt})} dP_\nu(\nu), \quad \Sigma = \begin{bmatrix} \sigma_p^2 & \rho_{pq}\sigma_p\sigma_q \\ \rho_{pq}\sigma_p\sigma_q & \sigma_q^2 \end{bmatrix}",
        "eq:shares",
        "Market shares as integral over consumer heterogeneity $\\nu$ with normal mixing distribution.",
    )

    eq_contraction = EquationSpec(
        "blp-contraction",
        r"\delta^{(r+1)} = \delta^{(r)} + \ln s^{obs} - \ln s(\delta^{(r)}, \Sigma), \quad \|\delta^{(r+1)} - \delta^*\| \leq \sqrt[3]{\binom{J}{2} \kappa^r \|\delta^{(0)} - \delta^*\|^3}",
        "eq:contraction",
        "BLP contraction mapping to invert market shares and recover mean utilities $\\delta$.",
    )

    eq_gmm = EquationSpec(
        "gmm-objective",
        r"\hat{\\theta} = \\arg\\min_{\\theta} \\xi(\\theta)' Z W Z' \\xi(\\theta)",
        "eq:gmm",
        "GMM objective function minimized over structural parameters $\\theta = (\\bar{\\beta}, \\Sigma)$.",
    )

    eq_opt_instruments = EquationSpec(
        "optimal-instruments",
        r"Z^*_{jt} = E\\left[\\frac{\\partial \\xi_{jt}}{\\partial \\theta} \\mid Z\\right] = -E\\left[\\frac{\\partial s_{jt}}{\\partial \\theta} / \\frac{\\partial s_{jt}}{\\partial \\xi_{jt}} \\mid Z\\right]",
        "eq:opt-instruments",
        "Optimal instruments (Chamberlain 1987): expected Jacobian of moments.",
    )

    eq_own_elas = EquationSpec(
        "own-elas",
        r"\\varepsilon_{jjt} = \\frac{\\partial s_{jt}}{\\partial p_{jt}} \\cdot \\frac{p_{jt}}{s_{jt}} = \\frac{p_{jt}}{s_{jt}} \\int \\alpha_i s_{ijt}(1 - s_{ijt}) dP_\\nu",
        "eq:own-elas",
        "Own-price elasticity formula for the random coefficients logit.",
    )

    eq_markup = EquationSpec(
        "markup-formula",
        r"p - mc = -\\left(\\frac{\\partial s}{\\partial p}'\\Omega\\right)^{-1} s",
        "eq:markup",
        "Markup formula (Lerner index) from Bertrand-Nash pricing conditions, where $\\Omega$ is the ownership matrix.",
    )

    eq_merger = EquationSpec(
        "merger-simulation",
        r"p^m = mc + \\left(\\frac{\\partial s}{\\partial p}'\\Omega^m\\right)^{-1} s(p^m)",
        "eq:merger",
        "Post-merger equilibrium prices from modified Bertrand-Nash conditions with new ownership matrix $\\Omega^m$.",
    )

    eq_welfare = EquationSpec(
        "welfare-measure",
        r"CV_i = -\\frac{1}{\\alpha_i} \\ln\\left(\\sum_j \\exp(u_{ij}^{post})\\right) + \\frac{1}{\\alpha_i} \\ln\\left(\\sum_j \\exp(u_{ij}^{pre})\\right)",
        "eq:welfare",
        "Compensating variation welfare measure for consumer $i$.",
    )


    # --- Appendix math ---
    appendix_proof_text = r"""
\begin{proposition}[Contraction Mapping: Berry 1994]
Define the operator $T: \mathbb{R}^J \to \mathbb{R}^J$ by
\begin{align}
T(\delta)_j &= \delta_j + \ln s_j^{obs} - \ln s_j(\delta, \Sigma).
\end{align}
$T$ is a contraction mapping with modulus $\kappa < 1$, so the iteration $\delta^{(r+1)} = T(\delta^{(r)})$ converges to the unique fixed point $\delta^* = \sigma^{-1}(s^{obs}, \Sigma)$.
\end{proposition}

\begin{proof}
The Jacobian satisfies
\begin{align}
\frac{\partial T_j}{\partial \delta_k} &= \begin{cases} 1 - s_j & k = j \\ s_k & k \neq j. \end{cases}
\end{align}
Since $\sum_k \partial s_j / \partial \delta_k = s_j(1 - s_j) - \sum_{k\neq j} s_j s_k = 0$, the operator norm $\|I - \partial T / \partial \delta\|_\infty < 1$. For mixed logit, dominated convergence extends this bound uniformly over $\nu$.
\end{proof}

\begin{proposition}[GMM Consistency]
Under compactness of $\Theta$, identification, and $E[\xi_{jt} z_{jt}] = 0$, the BLP GMM estimator
\begin{align}
\hat{\theta} &= \arg\min_\theta \xi(\theta)' Z W Z' \xi(\theta)
\end{align}
satisfies $\hat{\theta} \xrightarrow{p} \theta_0$ as $T \to \infty$.
\end{proposition}

\begin{proposition}[Optimal Instruments]
By the Chamberlain (1987) efficiency bound, the optimal instrument for $\theta_k$ is
\begin{align}
Z^*_k &= E\left[\frac{\partial \xi}{\partial \theta_k} \mid p, x, Z_{\text{exog}}\right] = E\left[\left(\frac{\partial s}{\partial \delta}\right)^{-1} \frac{\partial s}{\partial \theta_k} \mid Z_{\text{exog}}\right].
\end{align}
\end{proposition}

\begin{proposition}[Bertrand-Nash Equilibrium Prices]
Under demand $s(p)$ with $\partial s_j / \partial p_j < 0$, $|\partial s_j / \partial p_j| > |\partial s_k / \partial p_j|$ for $k \neq j$, and convex costs, there exists a unique equilibrium price vector $p^*$ satisfying
\begin{align}
p_j^* - mc_j &= -\frac{s_j(p^*)}{\partial s_j / \partial p_j(p^*)}, \quad \forall j \in \mathcal{F}_f,
\end{align}
for each firm $f$'s product portfolio $\mathcal{F}_f$.
\end{proposition}

\begin{proof}
Define $\phi(p) = mc - (\partial s / \partial p)^{-1} \Omega^{-1} s(p)$. Existence follows from Brouwer's fixed point theorem on $[mc, \bar{p}]^J$. Uniqueness follows from the $P$-matrix property of $\partial s / \partial p$ under logit demand.
\end{proof}

\noindent\textbf{Combinatorial structure of instruments.} There are $\binom{J}{2}$ distinct product-pair interactions in the BLP instrument set. The optimal instrument matrix has the block structure
\begin{align}
Z^* &= \begin{bmatrix} z_{11}^* & z_{12}^* & \cdots \\ z_{21}^* & z_{22}^* & \cdots \\ \vdots & \vdots & \ddots \end{bmatrix}, \quad \sqrt[3]{\det(Z^{*\prime} Z^*)} \leq \prod_{k=1}^{K} \|z_k^*\|^{2/K}.
\end{align}
The convergence rate of the contraction mapping satisfies $\|\delta^{(r)} - \delta^*\| \leq \sqrt[3]{\kappa^r} \cdot \|\delta^{(0)} - \delta^*\|$.
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-io",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-io", text_paragraphs=14, equations=[eq_utility])

    industry_bg = SectionSpec("Industry Background", "sec:industry-bg", text_paragraphs=10, tables=[market_summary, product_chars])

    demand_model = SectionSpec(
        "Demand Model", "sec:demand", text_paragraphs=12,
        equations=[eq_shares, eq_contraction],
        subsections=[
            SectionSpec("Consumer Heterogeneity", "sec:demand-het", level=2, text_paragraphs=8),
            SectionSpec("Market Share Inversion", "sec:demand-inv", level=2, text_paragraphs=8),
            SectionSpec("Identification of Demand Parameters", "sec:demand-id", level=2, text_paragraphs=8),
        ],
    )

    supply = SectionSpec(
        "Supply Side", "sec:supply", text_paragraphs=10,
        equations=[eq_markup, eq_merger],
        subsections=[
            SectionSpec("Firm Pricing", "sec:supply-pricing", level=2, text_paragraphs=8),
            SectionSpec("Cost Estimation", "sec:supply-cost", level=2, text_paragraphs=7),
        ],
    )

    estimation = SectionSpec(
        "Estimation", "sec:estimation-io", text_paragraphs=12,
        equations=[eq_gmm, eq_opt_instruments],
        subsections=[
            SectionSpec("GMM Procedure", "sec:estimation-gmm", level=2, text_paragraphs=9),
            SectionSpec("Instruments", "sec:estimation-iv", level=2, text_paragraphs=8),
            SectionSpec("Standard Errors", "sec:estimation-se", level=2, text_paragraphs=7),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-io", text_paragraphs=10,
        tables=[market_summary, product_chars],
        subsections=[
            SectionSpec("Scanner Data", "sec:data-scanner", level=2, text_paragraphs=7),
            SectionSpec("Product Characteristics", "sec:data-chars", level=2, text_paragraphs=7),
        ],
    )

    results = SectionSpec(
        "Results", "sec:results-io", text_paragraphs=10,
        tables=[demand_logit, demand_rc, own_elas, cross_elas],
        equations=[eq_own_elas],
        subsections=[
            SectionSpec("Demand Estimates", "sec:results-demand", level=2, text_paragraphs=8),
            SectionSpec("Elasticities", "sec:results-elas", level=2, text_paragraphs=8),
            SectionSpec("Markups", "sec:results-markups", level=2, text_paragraphs=7, tables=[markups]),
        ],
    )

    counterfactuals = SectionSpec(
        "Counterfactuals", "sec:counter-io", text_paragraphs=10,
        tables=[counterfactual, welfare],
        equations=[eq_welfare],
        subsections=[
            SectionSpec("Merger Simulation", "sec:counter-merger", level=2, text_paragraphs=8),
            SectionSpec("Welfare Analysis", "sec:counter-welfare", level=2, text_paragraphs=8),
        ],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-io", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Proofs", "sec:appendix-a-io", text_paragraphs=4,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Computational Details", "sec:appendix-b-io", text_paragraphs=6,
        tables=[appendix_instruments],
    )

    appendix_c = SectionSpec(
        "Appendix C: Monte Carlo Design", "sec:appendix-c-io", text_paragraphs=5,
        tables=[mc_bias, mc_coverage],
    )

    return PaperSpec(
        paper_id="05",
        field_slug="industrial-organization",
        title="Demand Estimation with Market-Level Data: A BLP Approach with Optimal Instruments",
        authors="Kenji Watanabe, Aisha Mensah, Dmitri Sokolov",
        journal_style="econometrica",
        abstract=(
            "We estimate a random coefficients logit demand model (BLP) using market-level scanner data from "
            "342 geographic markets. Exploiting optimal instruments constructed from the expected Jacobian of "
            "market shares, we obtain price coefficients with mean $-0.241$ and standard deviation $0.118$, "
            "implying mean own-price elasticities of $-3.71$. The implied Lerner markups closely match "
            "accounting-based estimates. Merger simulation predicts price increases of 6.8\\% for merging "
            "parties and 1.9\\% for rivals, with consumer surplus declining by \\$3.12 per consumer per quarter. "
            "Monte Carlo results confirm that BLP with optimal instruments achieves near-nominal coverage at "
            "moderate sample sizes."
        ),
        sections=[intro, industry_bg, demand_model, supply, estimation, data, results, counterfactuals,
                  conclusion, appendix_a, appendix_b, appendix_c],
        bibliography_entries=[
            r"\bibitem{blp1995} Berry, S., Levinsohn, J., and Pakes, A. (1995). Automobile Prices in Market Equilibrium. \textit{Econometrica}, 63(4), 841--890.",
            r"\bibitem{berry1994} Berry, S. T. (1994). Estimating Discrete-Choice Models of Product Differentiation. \textit{RAND Journal of Economics}, 25(2), 242--262.",
            r"\bibitem{nevo2001} Nevo, A. (2001). Measuring Market Power in the Ready-to-Eat Cereal Industry. \textit{Econometrica}, 69(2), 307--342.",
            r"\bibitem{armstrong2016} Armstrong, T. B. (2016). Large Market Asymptotics for Differentiated Product Demand Estimators with Economic Models of Supply. \textit{Econometrica}, 84(5), 1961--2002.",
            r"\bibitem{conlon2020} Conlon, C. and Gortmaker, J. (2020). Best Practices for Differentiated Products Demand Estimation with PyBLP. \textit{RAND Journal of Economics}, 51(4), 1108--1161.",
            r"\bibitem{chamberlain1987} Chamberlain, G. (1987). Asymptotic Efficiency in Estimation with Conditional Moment Restrictions. \textit{Journal of Econometrics}, 34(3), 305--334.",
            r"\bibitem{hausman1994} Hausman, J. A. (1994). Valuation of New Goods Under Perfect and Imperfect Competition. NBER Working Paper No. 4970.",
        ],
        target_pages=70,
        qa=[
            {"question": "What is the main estimation method?", "answer": "BLP GMM with random coefficients logit demand model"},
            {"question": "What is the mean own-price elasticity from the RC logit?", "answer": "-3.71"},
            {"question": "What is the mean price coefficient in the RC logit?", "answer": "-0.241"},
            {"question": "What price increase does the merger simulation predict for merging firm products under RC logit?", "answer": "6.84 percent"},
            {"question": "What is the overidentification test p-value for the RC logit?", "answer": "0.318"},
        ],
    )


PAPER_BUILDERS["05"] = _paper_05_io
