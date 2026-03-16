#!/usr/bin/env python3
"""Paper builder for paper 01 (Development Economics)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)


def _paper_01_development() -> PaperSpec:
    """Paper 1: Development economics — IV with institutions."""

    # ── Tables ──
    tab_summary = render_regression_table({
        "table_id": "summary-stats",
        "caption": "Summary Statistics",
        "label": "tab:summary-stats",
        "model_labels": ["N", "Mean", "Std. Dev.", "Min", "Max"],
        "panels": [{
            "variables": [
                {"label": "Log GDP per capita (PPP), 1995",
                 "coefficients": ["64", "8.05", "1.07", "5.63", "10.22"]},
                {"label": "Average protection against expropriation",
                 "coefficients": ["64", "6.52", "1.75", "3.50", "10.00"]},
                {"label": "Log settler mortality",
                 "coefficients": ["64", "4.68", "1.22", "2.15", "7.99"]},
                {"label": "Latitude (absolute value)",
                 "coefficients": ["64", "0.16", "0.13", "0.00", "0.67"]},
                {"label": "Africa dummy",
                 "coefficients": ["64", "0.44", "0.50", "0.00", "1.00"]},
                {"label": "Asia dummy",
                 "coefficients": ["64", "0.16", "0.37", "0.00", "1.00"]},
            ],
        }],
        "notes": "Sample includes 64 former European colonies with available data on settler mortality.",
        "qa": [
            {"question": "How many observations are in the sample?", "answer": "64"},
            {"question": "What is the mean log GDP per capita?", "answer": "8.05"},
        ],
    })

    tab_ols = render_regression_table({
        "table_id": "ols-results",
        "caption": "OLS Estimates: Institutions and Economic Development",
        "label": "tab:ols-results",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita (PPP), 1995",
            "variables": [
                {"label": "Average protection against expropriation",
                 "coefficients": ["0.52***", "0.47***", "0.43***", "0.39***"],
                 "std_errors": ["(0.06)", "(0.06)", "(0.07)", "(0.07)"]},
                {"label": "Latitude",
                 "coefficients": ["", "0.89**", "0.72*", "0.61"],
                 "std_errors": ["", "(0.41)", "(0.43)", "(0.42)"]},
            ],
        }],
        "controls": [
            {"label": "Continent dummies", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Legal origin controls", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["64", "64", "64", "64"]},
            {"label": "$R^2$", "values": ["0.54", "0.57", "0.62", "0.64"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors in parentheses.",
        "qa": [
            {"question": "What is the OLS coefficient on institutions in column 1?", "answer": "0.52"},
            {"question": "What is the R-squared in the most saturated specification (column 4)?", "answer": "0.64"},
        ],
    })

    tab_iv = render_regression_table({
        "table_id": "iv-results",
        "caption": "IV Estimates: Effect of Institutions on Income",
        "label": "tab:iv-results",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "label": "Panel A: Second Stage",
                "dep_var": "Dep. var.: Log GDP per capita",
                "variables": [
                    {"label": "Average protection against expropriation",
                     "coefficients": ["0.94***", "1.01***", "0.98***", "0.87***"],
                     "std_errors": ["(0.16)", "(0.19)", "(0.21)", "(0.15)"]},
                    {"label": "Latitude",
                     "coefficients": ["", "0.41", "0.38", "0.29"],
                     "std_errors": ["", "(0.31)", "(0.33)", "(0.28)"]},
                ],
            },
            {
                "label": "Panel B: First Stage",
                "dep_var": "Dep. var.: Avg. protection against expropriation",
                "variables": [
                    {"label": "Log settler mortality",
                     "coefficients": ["-0.61***", "-0.54***", "-0.49***", "-0.58***"],
                     "std_errors": ["(0.13)", "(0.12)", "(0.14)", "(0.13)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Geographic controls", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "Continent dummies", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["64", "64", "64", "64"]},
            {"label": "First-stage F", "values": ["22.1", "20.3", "12.2", "19.7"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors in parentheses. The instrument is log European settler mortality.",
        "qa": [
            {"question": "What is the IV coefficient on institutions in column 1?", "answer": "0.94"},
            {"question": "What is the first-stage F-statistic in column 3?", "answer": "12.2"},
            {"question": "Is the first-stage F above 10 in all columns?", "answer": "Yes"},
            {"question": "What is the first-stage coefficient on log settler mortality in column 1?", "answer": "-0.61"},
        ],
    })

    tab_balance = render_regression_table({
        "table_id": "balance",
        "caption": "Balance of Covariates Across High and Low Settler Mortality Countries",
        "label": "tab:balance",
        "model_labels": ["Low Mortality", "High Mortality", "Difference", "p-value"],
        "panels": [{
            "variables": [
                {"label": "Latitude", "coefficients": ["0.22", "0.11", "0.11", "0.03"]},
                {"label": "Africa dummy", "coefficients": ["0.19", "0.69", "-0.50", "0.00"]},
                {"label": "Asia dummy", "coefficients": ["0.22", "0.09", "0.13", "0.11"]},
                {"label": "Population density, 1500", "coefficients": ["4.51", "6.20", "-1.69", "0.38"]},
                {"label": "British legal origin", "coefficients": ["0.53", "0.47", "0.06", "0.64"]},
            ],
        }],
        "notes": "Countries split at median settler mortality. p-values from two-sample t-tests.",
        "qa": [
            {"question": "Is the Africa dummy balanced across groups?", "answer": "No, p-value is 0.00"},
        ],
    })

    tab_reduced = render_regression_table({
        "table_id": "reduced-form",
        "caption": "Reduced-Form Estimates: Settler Mortality and Income",
        "label": "tab:reduced-form",
        "model_labels": ["(1)", "(2)", "(3)"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita",
            "variables": [
                {"label": "Log settler mortality",
                 "coefficients": ["-0.57***", "-0.54***", "-0.48***"],
                 "std_errors": ["(0.10)", "(0.10)", "(0.11)"]},
            ],
        }],
        "controls": [
            {"label": "Geographic controls", "values": ["No", "Yes", "Yes"]},
            {"label": "Continent dummies", "values": ["No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["64", "64", "64"]},
            {"label": "$R^2$", "values": ["0.31", "0.35", "0.42"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors in parentheses.",
        "qa": [
            {"question": "What is the reduced-form effect of settler mortality on income?", "answer": "-0.57 in the baseline specification"},
        ],
    })

    tab_robust = render_regression_table({
        "table_id": "robustness",
        "caption": "Robustness of IV Estimates to Alternative Specifications",
        "label": "tab:robustness",
        "model_labels": ["Baseline", "No Africa", "No neo-Europes", "Campaign dummy", "Constraint on exec."],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita",
            "variables": [
                {"label": "Institutions",
                 "coefficients": ["0.94***", "0.99***", "1.10***", "0.81***", "0.76***"],
                 "std_errors": ["(0.16)", "(0.22)", "(0.25)", "(0.17)", "(0.19)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["64", "36", "60", "64", "64"]},
            {"label": "First-stage F", "values": ["22.1", "11.4", "15.8", "18.3", "16.9"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Each column reports IV estimates from a different specification.",
        "qa": [
            {"question": "Does excluding Africa weaken the result?", "answer": "No, coefficient increases to 0.99"},
            {"question": "What is the smallest first-stage F across robustness checks?", "answer": "11.4 (No Africa)"},
        ],
    })

    tab_mechanisms = render_regression_table({
        "table_id": "mechanisms",
        "caption": "Mechanisms: Institutions and Intermediate Outcomes",
        "label": "tab:mechanisms",
        "model_labels": ["Investment rate", "Human capital", "Trade openness"],
        "panels": [{
            "variables": [
                {"label": "Avg. protection against expropriation",
                 "coefficients": ["2.31**", "0.78***", "0.42"],
                 "std_errors": ["(1.04)", "(0.28)", "(0.31)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["64", "64", "64"]},
            {"label": "First-stage F", "values": ["22.1", "22.1", "22.1"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. IV estimates using log settler mortality as instrument.",
        "qa": [
            {"question": "Is the effect of institutions on trade openness statistically significant?", "answer": "No, the coefficient is 0.42 with a standard error of 0.31"},
            {"question": "Which mechanism channel has the largest coefficient?", "answer": "Investment rate (2.31)"},
        ],
    })

    tab_heterogeneity = render_regression_table({
        "table_id": "heterogeneity",
        "caption": "Heterogeneity: Effect of Institutions by Region",
        "label": "tab:heterogeneity",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "label": "Panel A: Africa",
                "variables": [
                    {"label": "Institutions",
                     "coefficients": ["0.82***", "0.91***", "", ""],
                     "std_errors": ["(0.22)", "(0.25)", "", ""]},
                ],
            },
            {
                "label": "Panel B: Non-Africa",
                "variables": [
                    {"label": "Institutions",
                     "coefficients": ["", "", "1.12***", "1.05***"],
                     "std_errors": ["", "", "(0.23)", "(0.20)"]},
                ],
            },
        ],
        "summary": [
            {"label": "Observations", "values": ["28", "28", "36", "36"]},
            {"label": "First-stage F", "values": ["9.8", "8.5", "14.3", "13.1"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Samples split by continent.",
        "qa": [
            {"question": "Is the first-stage F above 10 for all African sub-samples?", "answer": "No, columns 1-2 have F-statistics of 9.8 and 8.5, both below 10"},
            {"question": "Is the effect of institutions larger in Africa or non-Africa?", "answer": "Larger in non-Africa (1.12 vs 0.82 in the baseline specifications)"},
        ],
    })

    tab_appendix = render_regression_table({
        "table_id": "appendix-alt-mortality",
        "caption": "IV Estimates Using Alternative Mortality Data Sources",
        "label": "tab:appendix-a",
        "model_labels": ["Curtin (1989)", "Acemoglu et al.", "Gutierrez"],
        "panels": [{
            "dep_var": "Dep. var.: Log GDP per capita",
            "variables": [
                {"label": "Institutions",
                 "coefficients": ["0.88***", "0.94***", "0.91***"],
                 "std_errors": ["(0.19)", "(0.16)", "(0.18)"]},
            ],
        }],
        "summary": [
            {"label": "Observations", "values": ["51", "64", "58"]},
            {"label": "First-stage F", "values": ["14.2", "22.1", "17.6"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Each column uses settler mortality data from a different source.",
    })

    # ── Equations ──
    eqs = [
        EquationSpec("main", r"\log y_i = \hat{\mu} + \hat{\alpha} R_i + X_i'\bar{\gamma} + \tilde{\varepsilon}_i, \quad \frac{\partial^2 \mathcal{L}}{\partial \alpha \partial \gamma} = \mathbb{E}\left[\frac{\partial \hat{\varepsilon}_i}{\partial \alpha} \cdot X_i'\right]",
                     "eq:main", "Main estimating equation (second stage)",
                     [{"question": "What is the main estimating equation?",
                       "answer": "log(y_i) = mu + alpha*R_i + X_i'*gamma + epsilon_i"}]),
        EquationSpec("first-stage", r"R_i = \zeta + \pi M_i + X_i'\delta + \nu_i",
                     "eq:first-stage", "First-stage equation",
                     [{"question": "What is the instrument in the first stage?",
                       "answer": "M_i (log settler mortality)"}]),
        EquationSpec("exclusion", r"\text{Cov}(M_i, \varepsilon_i \mid X_i) = 0",
                     "eq:exclusion", "Exclusion restriction"),
        EquationSpec("wald", r"\hat{\alpha}_{IV} = \frac{\text{Cov}(y_i, M_i)}{\text{Cov}(R_i, M_i)}, \quad \mathbb{E}\left[\hat{\alpha}_{IV}\right] = \alpha + \frac{\mathbb{E}\left[\bar{Z}'\tilde{\varepsilon}\right]}{\mathbb{E}\left[\bar{Z}' X\right]}",
                     "eq:wald", "Wald estimator for just-identified IV"),
        EquationSpec("reduced-form", r"\log y_i = \kappa + \beta M_i + X_i'\lambda + u_i",
                     "eq:reduced-form", "Reduced-form equation"),
        EquationSpec("production", r"Y_i = A_i K_i^{\alpha} H_i^{1-\alpha}",
                     "eq:production", "Aggregate production function"),
        EquationSpec("institutions-channel",
                     r"A_i = A(R_i, G_i) = \bar{A} \cdot R_i^{\hat{\theta}} \cdot G_i^{\hat{\phi}}, \quad \frac{\partial^2 A_i}{\partial R_i \partial G_i} = \hat{\theta}\hat{\phi}\,\bar{A}\, R_i^{\hat{\theta}-1} G_i^{\hat{\phi}-1}",
                     "eq:institutions", "Institutions as determinant of TFP"),
        EquationSpec("settler-model",
                     r"R_i = \begin{cases} R^{extractive} & \text{if } M_i > \bar{M} \\ R^{inclusive} & \text{if } M_i \leq \bar{M} \end{cases}",
                     "eq:settler", "Settler mortality determines institutional type"),
    ]

    # ── Appendix proof blocks (raw LaTeX) ──
    appendix_proofs = r"""
\begin{proposition}[Consistency of the IV Estimator]
\label{prop:consistency}
Under Assumptions A1--A4, the IV estimator $\hat{\alpha}_{IV}$ is consistent for $\alpha$.
\end{proposition}

\begin{proof}
The IV estimator can be written as
\begin{align}
\hat{\alpha}_{IV} &= (Z'X)^{-1}Z'y \nonumber \\
    &= (Z'X)^{-1}Z'(X\alpha + \varepsilon) \nonumber \\
    &= \alpha + (Z'X)^{-1}Z'\varepsilon \label{eq:iv-expand}
\end{align}
Dividing numerator and denominator by $n$ and applying the law of large numbers:
\begin{equation}
\text{plim}\, \hat{\alpha}_{IV} = \alpha + \underbrace{\text{plim}\left(\frac{Z'X}{n}\right)^{-1}}_{= Q_{ZX}^{-1}} \cdot \underbrace{\text{plim}\left(\frac{Z'\varepsilon}{n}\right)}_{= 0} = \alpha
\end{equation}
where the last equality uses the exclusion restriction $E[Z_i \varepsilon_i] = 0$ (Assumption A3) and the relevance condition $\text{rank}(Q_{ZX}) = \text{rank}(E[Z_i X_i']) = p$ (Assumption A2).
\end{proof}

\begin{proposition}[Asymptotic Normality]
\label{prop:normality}
Under Assumptions A1--A4, the IV estimator is asymptotically normal:
\begin{equation}
\sqrt{n}(\hat{\alpha}_{IV} - \alpha) \xrightarrow{d} \mathcal{N}\left(0, \sigma^2 Q_{ZX}^{-1} Q_{ZZ} (Q_{ZX}')^{-1}\right)
\end{equation}
The result follows from applying the CLT to $\frac{1}{\sqrt{n}} Z'\varepsilon$ and Slutsky's theorem.
\end{proposition}

\begin{proposition}[Weak Instrument Asymptotics]
\label{prop:weak}
Under the weak instrument sequence $\pi_n = C/\sqrt{n}$ for fixed $C$, the conventional first-stage F-statistic converges in distribution to a noncentral $\chi^2$ divided by its degrees of freedom:
\begin{equation}
F \xrightarrow{d} \frac{\chi^2_k(\lambda)}{k}, \quad \text{where } \lambda = C' Q_{ZZ} C / \sigma^2_\nu
\end{equation}
The IV estimator is inconsistent in this case, with a limiting distribution that depends on the concentration parameter $\lambda$.
\end{proposition}

\noindent\textbf{Additional derivation.} The bias of the 2SLS estimator under weak instruments involves the mixed partial of the concentrated likelihood:
\begin{align}
\frac{\partial^2 \mathcal{L}}{\partial \hat{\alpha} \partial \hat{\gamma}} &= -\mathbb{E}\left[\bar{X}_i \bar{Z}_i' \hat{\Sigma}^{-1}\right], \quad \hat{\Sigma} = \frac{1}{n}\sum_{i=1}^{n} \hat{\varepsilon}_i \hat{\varepsilon}_i'.
\end{align}
Under the maintained assumptions, the asymptotic variance of the IV estimator satisfies
\begin{align}
\mathbb{E}\left[\sqrt{n}(\hat{\alpha}_{IV} - \alpha)\right] &\xrightarrow{d} \mathcal{N}\!\left(0,\; \sigma^2 \left(\bar{Q}_{ZX}^{-1}\right) Q_{ZZ} \left(\bar{Q}_{ZX}^{-1}\right)'\right).
\end{align}
"""

    # ── Sections ──
    sections = [
        SectionSpec("Introduction", "sec:intro", text_paragraphs=19),
        SectionSpec("Historical Background", "sec:history", text_paragraphs=15,
                    subsections=[
                        SectionSpec("European Colonization and Institutional Origins",
                                    "sec:colonization", level=2, text_paragraphs=11),
                        SectionSpec("Settler Mortality and Colony Type",
                                    "sec:mortality", level=2, text_paragraphs=8),
                    ]),
        SectionSpec("Theoretical Framework", "sec:model", text_paragraphs=12,
                    equations=eqs[:4],
                    subsections=[
                        SectionSpec("Production and Institutions",
                                    "sec:production", level=2, text_paragraphs=6),
                        SectionSpec("Settlement Patterns and Institutional Choice",
                                    "sec:settlement", level=2, text_paragraphs=6),
                    ]),
        SectionSpec("Data and Measurement", "sec:data", text_paragraphs=14,
                    tables=[tab_summary, tab_balance],
                    subsections=[
                        SectionSpec("Data Sources", "sec:data-sources", level=2,
                                    text_paragraphs=6),
                        SectionSpec("Variable Definitions", "sec:variables", level=2,
                                    text_paragraphs=6),
                        SectionSpec("Sample Construction", "sec:sample", level=2,
                                    text_paragraphs=5),
                    ]),
        SectionSpec("Empirical Strategy", "sec:empirical", text_paragraphs=12,
                    equations=eqs[4:],
                    subsections=[
                        SectionSpec("Identification", "sec:identification", level=2,
                                    text_paragraphs=6),
                        SectionSpec("Threats to Validity", "sec:threats", level=2,
                                    text_paragraphs=6),
                    ]),
        SectionSpec("Results", "sec:results", text_paragraphs=10,
                    tables=[tab_ols, tab_iv, tab_reduced],
                    subsections=[
                        SectionSpec("OLS Estimates", "sec:ols", level=2, text_paragraphs=8),
                        SectionSpec("IV Estimates", "sec:iv", level=2, text_paragraphs=10),
                        SectionSpec("Reduced-Form Evidence", "sec:reduced", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Robustness and Extensions", "sec:robustness", text_paragraphs=10,
                    tables=[tab_robust, tab_mechanisms, tab_heterogeneity],
                    subsections=[
                        SectionSpec("Alternative Specifications", "sec:alt-specs", level=2,
                                    text_paragraphs=6),
                        SectionSpec("Mechanisms", "sec:mechanisms", level=2,
                                    text_paragraphs=6),
                        SectionSpec("Heterogeneity", "sec:heterogeneity", level=2,
                                    text_paragraphs=6),
                    ]),
        SectionSpec("Conclusion", "sec:conclusion", text_paragraphs=8),
    ]

    # ── Appendix ──
    appendix_sections = [
        SectionSpec("Appendix A: Proofs of Theoretical Results", "sec:appendix-proofs",
                    text_paragraphs=6),
        SectionSpec("Appendix B: Additional Empirical Results", "sec:appendix-empirical",
                    text_paragraphs=8, tables=[tab_appendix]),
        SectionSpec("Appendix C: Data Construction Details", "sec:appendix-data",
                    text_paragraphs=10),
    ]

    proof_block = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proofs,
    )
    appendix_sections[0].tables.append(proof_block)

    sections.extend(appendix_sections)

    # ── Bibliography ──
    bib = [
        r"\bibitem{acemoglu2001} Acemoglu, D., S. Johnson, and J.A. Robinson (2001). ``The Colonial Origins of Comparative Development: An Empirical Investigation.'' \textit{American Economic Review}, 91(5), 1369--1401.",
        r"\bibitem{north1990} North, D.C. (1990). \textit{Institutions, Institutional Change and Economic Performance}. Cambridge University Press.",
        r"\bibitem{la2008} La Porta, R., F. Lopez-de-Silanes, and A. Shleifer (2008). ``The Economic Consequences of Legal Origins.'' \textit{Journal of Economic Literature}, 46(2), 285--332.",
        r"\bibitem{engerman2000} Engerman, S.L. and K.L. Sokoloff (2000). ``History Lessons: Institutions, Factor Endowments, and Paths of Development.'' \textit{Journal of Economic Perspectives}, 14(3), 217--232.",
        r"\bibitem{glaeser2004} Glaeser, E.L., R. La Porta, F. Lopez-de-Silanes, and A. Shleifer (2004). ``Do Institutions Cause Growth?'' \textit{Journal of Economic Growth}, 9(3), 271--303.",
        r"\bibitem{curtin1989} Curtin, P.D. (1989). \textit{Death by Migration: Europe's Encounter with the Tropical World in the Nineteenth Century}. Cambridge University Press.",
        r"\bibitem{rodrik2004} Rodrik, D., A. Subramanian, and F. Trebbi (2004). ``Institutions Rule: The Primacy of Institutions Over Geography and Integration in Economic Development.'' \textit{Journal of Economic Growth}, 9(2), 131--165.",
        r"\bibitem{sachs2003} Sachs, J.D. (2003). ``Institutions Don't Rule: Direct Effects of Geography on Per Capita Income.'' NBER Working Paper No. 9490.",
    ]

    return PaperSpec(
        paper_id="01",
        field_slug="development",
        title="Institutions and Economic Development: Evidence from Colonial Settlement Patterns",
        authors="Elena Vasquez \\and Marcus Okafor \\and Sarah Chen",
        journal_style="aer",
        abstract=(
            "We examine the causal effect of institutional quality on long-run economic "
            "development using data from 64 former European colonies. Exploiting variation "
            "in European settler mortality rates as an instrument for contemporary institutional "
            "quality, we find that institutions have a large and statistically significant "
            "effect on income per capita. A one-standard-deviation improvement in institutional "
            "quality raises log GDP per capita by approximately 0.94 log points. This result "
            "is robust to controlling for geographic characteristics, continent fixed effects, "
            "legal origin, and alternative measures of institutional quality. We provide evidence "
            "that the effect operates primarily through the investment channel rather than "
            "human capital accumulation or trade openness. These findings support theories "
            "emphasizing the primacy of institutions in economic development."
        ),
        sections=sections,
        bibliography_entries=bib,
        target_pages=45,
        qa=[
            {"question": "What is the main identification strategy?",
             "answer": "IV using log European settler mortality as instrument for institutional quality"},
            {"question": "How many former colonies are in the sample?",
             "answer": "64"},
            {"question": "What is the main finding?",
             "answer": "Institutions have a large causal effect on income; IV coefficient is 0.94"},
        ],
    )


PAPER_BUILDERS["01"] = _paper_01_development
