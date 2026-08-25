#!/usr/bin/env python3
"""Generate 20 synthetic long-form economics paper benchmarks.

Each paper is a full-length LaTeX document (~30-100 pages) mimicking the
style and structure of a famous top-5 economics journal paper. Ground truth
for tables, equations, and sections is extracted from the LaTeX source.

Usage:
    python generate_long_form.py                         # all 20 papers
    python generate_long_form.py --paper-id 01           # single paper
    python generate_long_form.py --output-dir ./cases    # custom output
    python generate_long_form.py --no-compile            # LaTeX only, skip PDF

Output per paper:
    cases/paper-XX-field/
        source.tex          LaTeX source
        source.pdf          Compiled PDF
        gold/
            sections.json   Section headings with labels
            tables.json     Gold table cell data
            equations.json  Gold equation LaTeX
            qa.json         Question-answer pairs
        manifest.json       Paper metadata
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════
# Data classes
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TableSpec:
    """Specification for a single table in a paper."""
    table_id: str
    caption: str
    label: str  # LaTeX label, e.g. "tab:main-results"
    latex: str  # Complete LaTeX for the table environment
    gold_cells: list[dict] = field(default_factory=list)
    notes: str = ""
    qa: list[dict] = field(default_factory=list)


@dataclass
class EquationSpec:
    """Specification for a displayed equation."""
    eq_id: str
    latex: str        # LaTeX inside equation environment (no \begin{equation})
    label: str        # LaTeX label
    description: str  # Plain-text description of what the equation represents
    qa: list[dict] = field(default_factory=list)


@dataclass
class SectionSpec:
    """Specification for a paper section."""
    title: str
    label: str          # LaTeX label
    level: int = 1      # 1=section, 2=subsection, 3=subsubsection
    text_paragraphs: int = 6  # how many filler paragraphs
    tables: list[TableSpec] = field(default_factory=list)
    equations: list[EquationSpec] = field(default_factory=list)
    subsections: list[SectionSpec] = field(default_factory=list)


@dataclass
class PaperSpec:
    """Full specification for a synthetic paper."""
    paper_id: str       # e.g. "01"
    field_slug: str     # e.g. "development"
    title: str
    authors: str
    abstract: str
    journal_style: str  # e.g. "aer", "econometrica", "qje"
    sections: list[SectionSpec]
    bibliography_entries: list[str]  # BibTeX entries
    qa: list[dict] = field(default_factory=list)  # paper-level QA
    target_pages: int = 50
    packages: list[str] = field(default_factory=list)
    table_style: str = ""  # TABLE_STYLES preset name; empty = default formatting


# ═══════════════════════════════════════════════════════════════════════════
# Filler text generator
# ═══════════════════════════════════════════════════════════════════════════

# Template paragraphs by section type. Variables: {x}, {y}, {method},
# {data_source}, {n_obs}, {period}, {unit}, {field}, {result_direction},
# {instrument}, {dep_var}, {indep_var}, {outcome}

INTRO_TEMPLATES = [
    "This paper investigates the causal relationship between {indep_var} and {dep_var}. Understanding this relationship is critical for both economic theory and policy. Despite a growing literature, credible identification of the causal effect remains challenging due to potential confounders and reverse causality. We contribute to this literature by proposing a new identification strategy based on {method}. Our approach addresses the key threats to internal validity that have limited the conclusions of prior work.",
    "We contribute to the literature on {field} by exploiting a novel source of variation in {indep_var}. Our identification strategy relies on {method}, which allows us to isolate the causal effect of {indep_var} on {dep_var} from confounding factors that have plagued earlier studies. The identifying assumption underlying our approach is that {instrument} affects {dep_var} only through its effect on {indep_var}, conditional on observable characteristics. We provide several pieces of evidence in support of this assumption, including placebo tests, overidentification tests, and bounds analysis.",
    "The existing literature on the relationship between {indep_var} and {dep_var} has produced mixed results. Some studies find a {result_direction} association, while others find no statistically significant effect. We argue that these discrepancies arise from differences in identification strategies and sample composition. Studies relying on cross-sectional variation tend to overstate the relationship due to omitted variable bias, while panel data approaches that rely on within-unit variation may attenuate the true effect by absorbing long-run changes in {indep_var}. Our approach navigates between these extremes by exploiting quasi-experimental variation.",
    "A central question in {field} is whether changes in {indep_var} lead to changes in {dep_var}, or whether the observed correlation reflects reverse causality or omitted variable bias. We address this question using {method} applied to data from {data_source}. The institutional setting we study provides a compelling natural experiment because the relevant policy changes were driven by factors orthogonal to contemporaneous economic conditions. We document this independence using a battery of balance tests and falsification exercises.",
    "Our main finding is that {indep_var} has a statistically significant and economically meaningful effect on {dep_var}. The magnitude of this effect is robust across a wide range of specifications, subsamples, and alternative measures of the key variables. A one standard deviation increase in {indep_var} is associated with a change of approximately 0.3 to 0.5 standard deviations in {dep_var}, depending on the specification. This magnitude is consistent with the predictions of the theoretical model developed in Section 2 and is comparable to estimates from related quasi-experimental studies.",
    "The remainder of this paper proceeds as follows. Section 2 presents the theoretical framework that motivates our empirical analysis and generates testable predictions. Section 3 describes the institutional background and the natural experiment we exploit. Section 4 describes the data sources and sample construction. Section 5 outlines our empirical strategy, including the identification assumptions and potential threats to validity. Section 6 presents the main results. Section 7 discusses robustness checks and extensions. Section 8 concludes with a discussion of policy implications.",
    "Our paper relates to several strands of the economics literature. First, we contribute to the extensive body of work on the determinants of {dep_var}, which has been a central topic in {field} since the seminal contributions of the 1990s and 2000s. Second, we contribute to the methodological literature on {method} by demonstrating its applicability to a new empirical context. Third, our findings speak to an ongoing policy debate about the effectiveness of interventions targeting {indep_var}.",
    "The economic significance of our findings warrants emphasis. Back-of-the-envelope calculations suggest that the estimated effect implies substantial welfare gains from policies that improve {indep_var}. Using the framework of Chetty (2009) for translating reduced-form estimates into welfare statements, we estimate that a policy intervention that increases {indep_var} by one standard deviation would generate welfare gains equivalent to approximately 2-4 percent of annual income. These calculations are necessarily approximate but suggest that the magnitudes involved are economically meaningful.",
    "A distinctive feature of our analysis is the richness of the data. Unlike many previous studies that rely on aggregate proxies, our dataset contains individual-level information on both {dep_var} and {indep_var}, measured with high frequency over an extended time period. This granularity allows us to investigate heterogeneity in treatment effects across {unit}, to construct precise event study estimates, and to conduct a range of placebo and falsification tests that would not be feasible with more aggregated data.",
    "Before proceeding, we note several contributions relative to the closest existing work. While prior studies have documented a correlation between {indep_var} and {dep_var} in various contexts, our paper is among the first to provide credibly causal estimates using {method}. Moreover, our analysis of mechanisms goes beyond what has been possible in earlier studies, shedding light on the channels through which {indep_var} affects {dep_var}.",
]

MODEL_TEMPLATES = [
    "Consider an economy populated by a continuum of agents indexed by $i \\in [0,1]$. Each agent chooses {dep_var} to maximize lifetime utility subject to a budget constraint. The key source of heterogeneity across agents is their exposure to {indep_var}. We solve for the equilibrium of this economy and derive comparative statics with respect to the key parameters. The model generates a clear testable prediction: an exogenous increase in {indep_var} should lead to a {result_direction} change in {dep_var}, with the magnitude depending on structural parameters that we estimate in the empirical analysis.",
    "Let $Y_i$ denote the outcome of interest for unit $i$. We model $Y_i$ as a function of treatment status $D_i$, observed covariates $X_i$, and unobserved heterogeneity $\\varepsilon_i$. Under standard regularity conditions, the conditional expectation function takes the form presented in Equation~\\ref{{eq:main}}. The parameter of interest is the coefficient on treatment status, which captures the causal effect of {indep_var} on {dep_var} holding constant observed and unobserved confounders. Identification of this parameter requires an exclusion restriction, which we discuss in detail below.",
    "The theoretical framework builds on the canonical model of {field}. Agents face a discrete choice between $J$ alternatives, each yielding utility $U_{ij} = V_{ij} + \\epsilon_{ij}$, where $V_{ij}$ is the deterministic component and $\\epsilon_{ij}$ captures idiosyncratic preferences. Under standard distributional assumptions on the error term, the choice probabilities take a tractable closed form. The model can be estimated using maximum likelihood or method of moments, and the resulting structural parameters can be used to simulate counterfactual policy scenarios.",
    "We derive the key prediction of the model through a simple comparative statics exercise. An exogenous increase in {indep_var} shifts the equilibrium allocation of {dep_var} through two channels: a direct effect operating through prices, and an indirect effect operating through the reallocation of factors across sectors. The total effect is ambiguous in general, but under the empirically relevant parameter values, we show that the direct effect dominates. Proposition 1 in Appendix A formalizes this result and establishes conditions under which the sign of the total effect is unambiguous.",
    "Under the assumption that {instrument} satisfies the exclusion restriction, the model implies that the reduced-form relationship between {instrument} and {dep_var} is proportional to the structural parameter of interest. This motivates our instrumental variables strategy described in Section~\\ref{{sec:empirical}}. A key advantage of the IV approach is that it does not require functional form assumptions on the relationship between {indep_var} and the unobserved confounders. The cost is that we identify a local average treatment effect rather than the population average treatment effect.",
    "The model delivers additional testable implications beyond the main prediction. First, the treatment effect should be larger for {unit} with lower baseline levels of {dep_var}, reflecting diminishing marginal returns. Second, the effect should be persistent over time rather than transitory, because the mechanism operates through permanent changes in the level of {indep_var}. Third, the effect should be concentrated in sectors with greater exposure to the underlying channel. We test each of these auxiliary predictions in Section 6.",
    "We make several simplifying assumptions to maintain tractability. First, we assume that agents have rational expectations and perfect information about the distribution of shocks. Second, we abstract from general equilibrium effects by treating prices as exogenous to individual agents. Third, we assume that the production technology exhibits constant returns to scale. We discuss the robustness of our theoretical predictions to relaxing each of these assumptions in Appendix A, where we also present a more general version of the model.",
    "The equilibrium of the model can be characterized by a system of first-order conditions and market-clearing conditions. In the interior solution, the marginal benefit of increasing {indep_var} equals the marginal cost, yielding an implicit equation for the optimal level of {indep_var} as a function of exogenous parameters and state variables. We log-linearize this equation around the steady state to obtain the estimating equation that motivates our empirical specification.",
]

DATA_TEMPLATES = [
    "Our primary data source is {data_source}, which covers {n_obs} {unit} over the period {period}. This dataset provides detailed information on {dep_var}, {indep_var}, and a rich set of control variables that we use to address potential confounders. The data are available at the individual level and include both repeated cross-sections and a longitudinal component that allows us to track {unit} over time. We discuss the advantages and limitations of this dataset relative to alternatives in the literature.",
    "Table~\\ref{{tab:summary-stats}} presents summary statistics for the key variables used in our analysis. The mean of {dep_var} is consistent with values reported in prior studies, providing confidence that our sample is representative of the population of interest. The standard deviation suggests substantial variation across {unit}, which is essential for our identification strategy. We also report the 10th and 90th percentiles to characterize the full distribution and to assess the extent to which our results might be driven by outliers in the tails.",
    "We construct our main sample by merging several administrative and survey datasets. After applying standard sample restrictions and dropping observations with missing values on key variables, our final estimation sample contains {n_obs} observations covering {period}. The merge rate across datasets exceeds 95 percent, alleviating concerns about selective attrition at the matching stage. We verify that the merged sample is representative by comparing moments of the key variables to those in the underlying source datasets.",
    "The key independent variable, {indep_var}, exhibits substantial cross-sectional variation. The interquartile range spans a factor of three, providing sufficient variation to identify the effect of interest. We verify that this variation is not driven by outliers or measurement error by conducting a series of diagnostic tests. In particular, we show that the results are robust to winsorizing {indep_var} at the 1st and 99th percentiles, to using alternative measures from different data sources, and to correcting for measurement error using an errors-in-variables estimator.",
    "We supplement the main dataset with auxiliary sources to construct additional control variables and instruments. Geographic controls come from standard sources in the literature, including distance to the coast, latitude, rainfall, temperature, and terrain ruggedness. Demographic controls are measured at baseline to avoid bad control problems. Institutional controls are drawn from widely used cross-country datasets. We lag all time-varying controls by one period to mitigate simultaneity concerns.",
    "The measurement of {dep_var} deserves discussion. Following the standard approach in the literature, we use the logarithm of {dep_var} as our primary outcome variable. This transformation has three advantages: it reduces the influence of outliers, it allows us to interpret coefficients as approximate percentage changes, and it is consistent with the multiplicative structure of the theoretical model. We verify that our results are qualitatively robust to using {dep_var} in levels or in ranks.",
    "Panel A of Table~\\ref{{tab:summary-stats}} reports summary statistics for the full sample, while Panels B and C restrict attention to subsamples that will be used in the heterogeneity analysis. The key variables are well-balanced across subsamples, with the exception of {indep_var}, which exhibits the expected variation driven by the quasi-experimental design. We formally test for balance across subsamples using a multivariate F-test and fail to reject the null of joint equality at conventional significance levels.",
    "Data quality is a potential concern in studies of this type. We address this concern in several ways. First, we cross-validate our primary measure of {dep_var} against alternative sources and find high concordance rates. Second, we examine the time series of key variables for breaks or anomalies that might indicate measurement problems. Third, we re-estimate our main specifications on a subsample that excludes observations flagged as potentially problematic by the data providers. All results are robust to these checks.",
]

RESULTS_TEMPLATES = [
    "Table~\\ref{{tab:main-results}} presents our main estimates. Column (1) reports the baseline specification without controls. Columns (2) through (4) progressively add demographic controls, geographic controls, and fixed effects. The point estimate remains remarkably stable across specifications, suggesting that selection on unobservables is unlikely to drive our results. Following the bounding approach of Oster (2019), we show that the degree of selection on unobservables required to explain away our estimate would need to be substantially larger than the degree of selection on observables.",
    "The estimated coefficient on {indep_var} is statistically significant at the one percent level in all specifications. The magnitude implies that a one standard deviation increase in {indep_var} is associated with a {result_direction} of approximately 0.3 standard deviations in {dep_var}. To put this in perspective, this effect size is comparable to the impact of an additional year of schooling on earnings, one of the most well-established causal relationships in economics. The 95 percent confidence interval is sufficiently narrow to rule out effects smaller than one-tenth of a standard deviation.",
    "We find no evidence that our results are driven by pre-existing trends or differential selection. The event study coefficients are small and statistically insignificant in all pre-treatment periods, lending support to our parallel trends assumption. Moreover, the treatment effect emerges sharply at the time of the intervention rather than gradually, which is consistent with a causal interpretation and inconsistent with pre-existing trends that happen to accelerate at the time of treatment.",
    "The first-stage relationship between {instrument} and {indep_var} is strong, with an F-statistic well above conventional thresholds for weak instruments. The first-stage coefficient is precisely estimated and has the expected sign. Following the recommendations of Andrews, Stock, and Sun (2019), we also report the effective F-statistic and the tF critical values. Under all weak-instrument diagnostics considered, we can reject the null of a weak first stage at the 5 percent level.",
    "Heterogeneity analysis reveals that the treatment effect is concentrated among {unit} with below-median baseline levels of {dep_var}. This pattern is consistent with the theoretical prediction that the marginal return to {indep_var} is decreasing. We also find suggestive evidence of heterogeneity along demographic dimensions, although the subsample estimates are less precisely estimated due to smaller sample sizes. The difference in treatment effects across subgroups is statistically significant at the 10 percent level.",
    "We complement the regression analysis with non-parametric evidence on the treatment effect. Kernel density estimates of the distribution of {dep_var} show a clear rightward shift for treated {unit} relative to untreated {unit}. Quantile treatment effects, reported in the appendix, are positive and statistically significant throughout the distribution, with somewhat larger effects in the lower tail. This pattern suggests that the treatment reduces inequality in {dep_var} by disproportionately benefiting those at the bottom of the distribution.",
    "The magnitude of our estimates is informative about the relative importance of {indep_var} as a determinant of {dep_var}. A variance decomposition exercise reveals that variation in {indep_var} can account for approximately 15 to 25 percent of the cross-sectional variance in {dep_var}, depending on the specification. While this leaves substantial residual variation unexplained, it establishes {indep_var} as one of the most quantitatively important determinants identified in the literature.",
    "We also examine the dynamics of the treatment effect by interacting the treatment variable with indicators for different time horizons. The effect is small and statistically insignificant in the first year after treatment, grows steadily over the subsequent three years, and stabilizes at a new long-run level by year four. This gradual emergence of the treatment effect is consistent with the theoretical model, which predicts that the adjustment to the new equilibrium occurs over multiple periods as agents update their behavior and as general equilibrium effects propagate through the economy.",
]

ROBUSTNESS_TEMPLATES = [
    "We conduct a battery of robustness checks to assess the sensitivity of our main findings. Table~\\ref{{tab:robustness}} reports results from alternative specifications that vary the set of controls, the sample definition, the functional form, and the estimation method. Across all specifications, the point estimate on {indep_var} remains within the 95 percent confidence interval of the baseline estimate, and the qualitative conclusions are unchanged.",
    "Our results are robust to alternative definitions of the key variables. Using log transformations instead of levels, measuring {indep_var} at different points in time, and winsorizing outliers at the first and ninety-ninth percentiles all yield qualitatively similar estimates. We also consider alternative measures of {dep_var} from different data sources and find highly consistent results. The correlation between alternative measures exceeds 0.9, suggesting that measurement error is not a first-order concern.",
    "Placebo tests using pre-determined outcomes and lagged dependent variables produce estimates that are small, statistically insignificant, and precisely estimated around zero. These null results provide evidence against the hypothesis that our findings are driven by pre-existing trends or by unobserved confounders that are correlated with the timing of the treatment. We also conduct a randomization inference exercise that permutes the treatment assignment across {unit} and find that the true estimate lies in the extreme tail of the placebo distribution.",
    "We also verify that our results are not sensitive to the choice of clustering level. Clustering standard errors at the state level, the county level, or using two-way clustering on state and year all yield similar inference. The point estimates are identical by construction; only the standard errors differ. Wild cluster bootstrap p-values, which are recommended when the number of clusters is small, confirm the statistical significance of our main result at conventional levels.",
    "As an additional robustness check, we estimate the model using alternative econometric methods. Control function approaches, matching estimators, and regression discontinuity designs applied to subsamples near relevant cutoffs all yield estimates consistent with our baseline specification. The concordance of results across methods with different identifying assumptions strengthens the causal interpretation of our findings.",
    "We address the possibility of spillover effects by examining whether the treatment of neighboring {unit} affects outcomes for untreated {unit}. Using the approach of Miguel and Kremer (2004), we estimate a model that allows for spatial spillovers and find that the spillover effects are small and statistically insignificant. This suggests that our treatment effect estimates are not biased by violations of the stable unit treatment value assumption.",
    "Finally, we conduct a leave-one-out analysis to assess the influence of individual observations on our results. Sequentially dropping each {unit} from the sample and re-estimating the main specification reveals that no single observation has a disproportionate influence on the point estimate. The coefficient on {indep_var} varies by less than 10 percent across leave-one-out samples, and the statistical significance is maintained in all cases.",
]

CONCLUSION_TEMPLATES = [
    "This paper provides new evidence on the causal effect of {indep_var} on {dep_var}. Using {method} applied to {data_source}, we find a {result_direction} and statistically significant effect that is robust across a wide range of specifications. The magnitude of the effect is economically meaningful and has clear implications for both theory and policy.",
    "Our findings have several implications for economic theory. First, the results support models in which {indep_var} plays a central role in determining {dep_var}, as opposed to alternative theories that emphasize other factors. Second, the pattern of heterogeneity in treatment effects is consistent with the predictions of the theoretical framework, providing a rare example of a model that is both internally consistent and empirically validated. Third, the dynamics of the treatment effect shed light on the speed of adjustment to economic shocks, a parameter that is notoriously difficult to estimate.",
    "From a policy perspective, the estimates suggest that interventions targeting {indep_var} could have meaningful effects on {dep_var}. However, several caveats are in order. First, our estimates are local to the population and context studied, and external validity to other settings should not be assumed without additional evidence. Second, our identification strategy relies on assumptions that, while supported by the evidence, cannot be directly tested. Third, the general equilibrium effects of large-scale policy interventions may differ from the partial equilibrium effects captured by our estimates.",
    "Future work should investigate the mechanisms through which {indep_var} affects {dep_var} in greater detail. Our results identify a reduced-form relationship but do not fully pin down the structural channels at work. Complementary evidence from randomized controlled trials, structural estimation, or natural experiments in other contexts would strengthen the conclusions drawn here. Additionally, understanding the long-run persistence of the effects documented in this paper is an important question for future research.",
    "In conclusion, this paper demonstrates that {indep_var} is a quantitatively important determinant of {dep_var}. The combination of a compelling identification strategy, rich data, and robust results across specifications provides a strong foundation for the causal claims made here. We hope that these findings will stimulate further research on the economic consequences of variation in {indep_var} and will inform the design of policies aimed at improving {dep_var}.",
]

APPENDIX_TEMPLATES = [
    "This appendix provides additional results referenced in the main text. We organize the supplementary material into three parts. Appendix A presents proofs of the theoretical propositions stated in Section~\\ref{{sec:model}}. Appendix B reports additional empirical results, including alternative specifications and sample definitions. Appendix C describes the construction of key variables in detail.",
    "We present detailed derivations of the key theoretical results stated in Section~\\ref{{sec:model}}. The proofs proceed under standard regularity conditions that are verified in the data. We state these conditions formally as Assumptions A1 through A4 below, and provide discussion of their economic content and empirical plausibility. Throughout, we maintain the notation introduced in the main text.",
    "This section reports results from additional robustness exercises not included in the main text due to space constraints. All estimates are qualitatively similar to the baseline results reported in Table~\\ref{{tab:main-results}}. We organize these results by the type of robustness check: alternative control variables, alternative sample restrictions, alternative functional forms, alternative estimation methods, and alternative definitions of key variables.",
    "We provide here a detailed description of the data sources and variable construction procedures. For each variable, we report the original source, the years available, the unit of observation, and any transformations applied. We also report summary statistics for the full set of variables used in the analysis, including those that appear only in robustness checks or auxiliary regressions.",
    "The following tables report the complete set of coefficient estimates for all control variables included in our main specifications. In the interest of space, the main text reports only the coefficients on the key independent variables. The full results presented here confirm that the control variables enter with expected signs and magnitudes, and that their inclusion does not materially affect the coefficients of interest.",
]


def generate_filler(
    section_type: str,
    variables: dict[str, str],
    n_paragraphs: int,
) -> str:
    """Generate filler text for a section."""
    templates = {
        "intro": INTRO_TEMPLATES,
        "model": MODEL_TEMPLATES,
        "data": DATA_TEMPLATES,
        "results": RESULTS_TEMPLATES,
        "robustness": ROBUSTNESS_TEMPLATES,
        "conclusion": CONCLUSION_TEMPLATES,
        "appendix": APPENDIX_TEMPLATES,
    }.get(section_type, INTRO_TEMPLATES)

    paragraphs = []
    for i in range(n_paragraphs):
        tmpl = templates[i % len(templates)]
        try:
            text = tmpl.format(**variables)
        except (KeyError, IndexError):
            text = tmpl  # fallback: use template as-is
        paragraphs.append(text)
    return "\n\n".join(paragraphs)


# ═══════════════════════════════════════════════════════════════════════════
# Table renderers
# ═══════════════════════════════════════════════════════════════════════════

def _stars_latex(val: str) -> str:
    """Convert 0.94*** to 0.94$^{***}$."""
    m = re.match(r'^(.+?)(\*{1,3})$', val.strip())
    if m:
        return f"{m.group(1)}$^{{{m.group(2)}}}$"
    return val


def _ensure_math(s: str) -> str:
    """Wrap in $...$ if the string has LaTeX math commands but isn't already in math mode."""
    if not s or s.startswith("$") or s.startswith(r"\text"):
        return s
    if "\\" in s:
        return f"${s}$"
    return s


# ── Table style presets ──
# Each preset is a table_format dict reflecting a real-world software/convention.
TABLE_STYLES: dict[str, dict] = {
    "stata_esttab":       {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "threeparttable"},
    "stata_outreg2":      {"rules": "hline",    "se_wrap": "()", "star_pos": "coeff", "notes": "text"},
    "stata_wide":         {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "threeparttable", "col_sep": r"\setlength{\tabcolsep}{3pt}"},
    "r_stargazer":        {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "text"},
    "r_modelsummary":     {"rules": "booktabs", "se_wrap": "[]", "star_pos": "coeff", "notes": "threeparttable"},
    "r_texreg":           {"rules": "booktabs", "se_wrap": "()", "star_pos": "se",    "notes": "text", "font_size": "small"},
    "python_statsmodels":  {"rules": "hline",   "se_wrap": "",   "star_pos": "none",  "notes": "text"},
    "sas_proc":           {"rules": "hline",    "se_wrap": "()", "star_pos": "none",  "notes": "text", "font_size": "footnotesize"},
    "excel_grid":         {"rules": "hline",    "se_wrap": "()", "star_pos": "coeff", "notes": "none"},
    "manual_hline":       {"rules": "hline",    "se_wrap": "()", "star_pos": "coeff", "notes": "text"},
    "old_school":         {"rules": "hline",    "se_wrap": "()", "star_pos": "coeff", "notes": "none", "font_size": "small"},
    "aer_published":      {"rules": "booktabs", "se_wrap": "()", "star_pos": "none",  "notes": "threeparttable"},
    "econometrica_pub":   {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "threeparttable", "font_size": "small"},
    "qje_published":      {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "threeparttable"},
    "nber_wp":            {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "text", "font_size": "footnotesize"},
    "jf_endnotes":        {"rules": "booktabs", "se_wrap": "[]", "star_pos": "coeff", "notes": "text"},
    "compact_conf":       {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "none", "font_size": "scriptsize", "col_sep": r"\setlength{\tabcolsep}{2pt}"},
    "landscape_wide":     {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "threeparttable"},
    "minimal_clean":      {"rules": "none",     "se_wrap": "()", "star_pos": "coeff", "notes": "text"},
    "verbose_notes":      {"rules": "booktabs", "se_wrap": "()", "star_pos": "coeff", "notes": "threeparttable"},
}


# Module-level default table style — set by build_paper() before calling builders.
# Builders can override per-table via spec["table_format"].
_default_table_style: str = ""


def render_regression_table(spec: dict) -> TableSpec:
    """Render a regression table from a high-level spec dict.

    Expected keys: table_id, caption, label, model_labels, panels,
    controls (optional), summary (optional), notes (optional), qa (optional).
    Optional: table_format (dict or preset name string).
    """
    # ── Table formatting options ──
    raw_fmt = spec.get("table_format", None)
    if raw_fmt is None and _default_table_style:
        raw_fmt = _default_table_style
    if raw_fmt is None:
        raw_fmt = {}
    # Allow passing a preset name string
    if isinstance(raw_fmt, str):
        fmt = TABLE_STYLES.get(raw_fmt, {})
    else:
        fmt = raw_fmt
    rules = fmt.get("rules", "booktabs")
    se_wrap = fmt.get("se_wrap", "()")
    star_pos = fmt.get("star_pos", "coeff")
    notes_style = fmt.get("notes", "threeparttable")
    font_size = fmt.get("font_size", "")
    col_sep = fmt.get("col_sep", "")

    # Rule helpers
    def _toprule() -> str:
        if rules == "booktabs":
            return r"\toprule"
        elif rules == "hline":
            return r"\hline"
        return ""

    def _midrule() -> str:
        if rules == "booktabs":
            return r"\midrule"
        elif rules == "hline":
            return r"\hline"
        return ""

    def _bottomrule() -> str:
        if rules == "booktabs":
            return r"\bottomrule"
        elif rules == "hline":
            return r"\hline"
        return ""

    def _wrap_se(s: str) -> str:
        """Wrap a standard-error value according to *se_wrap*."""
        if not s:
            return s
        if se_wrap == "()":
            return f"({s})"
        elif se_wrap == "[]":
            return f"[{s}]"
        return s

    ml = spec["model_labels"]
    ncols = len(ml) + 1
    colspec = "l" + "c" * len(ml)

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    if spec.get("notes") and notes_style == "threeparttable":
        lines.append(r"\begin{threeparttable}")
    lines.append(f"\\caption{{{spec['caption']}}}")
    lines.append(f"\\label{{{spec['label']}}}")
    if font_size:
        lines.append(f"\\{font_size}")
    if col_sep:
        lines.append(col_sep)
    lines.append(f"\\begin{{tabular}}{{{colspec}}}")
    top = _toprule()
    if top:
        lines.append(top)

    # Column headers
    headers = " & ".join([""] + ml) + r" \\"
    lines.append(headers)
    mid = _midrule()
    if mid:
        lines.append(mid)

    gold_cells = []
    row_idx = 0  # track for gold

    for panel in spec["panels"]:
        if panel.get("label"):
            lines.append(
                f"\\multicolumn{{{ncols}}}{{l}}{{\\textit{{{panel['label']}}}}}"
                + r" \\"
            )
            row_idx += 1

        if panel.get("dep_var"):
            lines.append(
                f"\\multicolumn{{{ncols}}}{{l}}{{{panel['dep_var']}}}"
                + r" \\"
            )
            row_idx += 1

        for var in panel["variables"]:
            # Coefficient row
            if star_pos == "coeff":
                coeffs = [_stars_latex(c) if c else "" for c in var["coefficients"]]
            elif star_pos == "none":
                # Strip stars for display but keep raw value in gold
                coeffs = [re.sub(r'\*+$', '', c).strip() if c else "" for c in var["coefficients"]]
            else:
                # star_pos == "se": no stars on coefficient row
                coeffs = [re.sub(r'\*+$', '', c).strip() if c else "" for c in var["coefficients"]]
            lines.append(f"{var['label']} & " + " & ".join(coeffs) + r" \\")
            for ci, c in enumerate(var["coefficients"]):
                gold_cells.append({
                    "row": row_idx, "col": ci + 1,
                    "text": c, "role": "data",
                    "variable": var["label"], "is_coefficient": True,
                })
            row_idx += 1

            # SE row
            if var.get("std_errors"):
                if star_pos == "se":
                    # Move stars from coefficients to SEs
                    raw_ses = []
                    for ci_se, s in enumerate(var["std_errors"]):
                        if s:
                            coeff_raw = var["coefficients"][ci_se] if ci_se < len(var["coefficients"]) else ""
                            star_match = re.search(r'(\*{1,3})$', coeff_raw.strip()) if coeff_raw else None
                            se_val = _wrap_se(s)
                            if star_match:
                                se_val = _stars_latex(se_val + star_match.group(1))
                            raw_ses.append(se_val)
                        else:
                            raw_ses.append("")
                    ses = raw_ses
                else:
                    ses = [_wrap_se(s) if s else "" for s in var["std_errors"]]
                lines.append(" & " + " & ".join(ses) + r" \\")
                for ci, s in enumerate(var["std_errors"]):
                    gold_cells.append({
                        "row": row_idx, "col": ci + 1,
                        "text": s, "role": "data",
                        "variable": var["label"], "is_stderr": True,
                    })
                row_idx += 1

    # Controls
    if spec.get("controls"):
        mid = _midrule()
        if mid:
            lines.append(mid)
        for ctrl in spec["controls"]:
            vals = ctrl["values"]
            lines.append(f"{ctrl['label']} & " + " & ".join(vals) + r" \\")
            row_idx += 1

    # Summary stats
    if spec.get("summary"):
        mid = _midrule()
        if mid:
            lines.append(mid)
        for stat in spec["summary"]:
            vals = stat["values"]
            lines.append(f"{stat['label']} & " + " & ".join(vals) + r" \\")
            for ci, v in enumerate(vals):
                gold_cells.append({
                    "row": row_idx, "col": ci + 1,
                    "text": v, "role": "summary",
                    "label": stat["label"],
                })
            row_idx += 1

    bot = _bottomrule()
    if bot:
        lines.append(bot)
    lines.append(r"\end{tabular}")

    if spec.get("notes"):
        notes_text = spec["notes"] if isinstance(spec["notes"], str) else spec["notes"][0]
        if notes_style == "threeparttable":
            lines.append(r"\begin{tablenotes}")
            lines.append(f"\\small\\item \\textit{{Notes:}} {notes_text}")
            lines.append(r"\end{tablenotes}")
            lines.append(r"\end{threeparttable}")
        elif notes_style == "text":
            lines.append(f"\\\\\\small\\textit{{Notes:}} {notes_text}")
        # notes_style == "none": omit notes entirely

    lines.append(r"\end{table}")

    return TableSpec(
        table_id=spec["table_id"],
        caption=spec["caption"],
        label=spec["label"],
        latex="\n".join(lines),
        gold_cells=gold_cells,
        notes=spec.get("notes", ""),
        qa=spec.get("qa", []),
    )


def render_math_table(spec: dict) -> TableSpec:
    """Render a math/formula table from a high-level spec dict.

    Expected keys: table_id, caption, label, col_headers, rows.
    """
    headers = spec["col_headers"]
    colspec = "l" + "l" * len(headers)

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(f"\\caption{{{spec['caption']}}}")
    lines.append(f"\\label{{{spec['label']}}}")
    lines.append(f"\\begin{{tabular}}{{{colspec}}}")
    lines.append(r"\toprule")

    # Headers
    hdr_texts = []
    for h in headers:
        hdr_texts.append(h.get("latex") or h["text"])
    lines.append(" & " + " & ".join(hdr_texts) + r" \\")
    lines.append(r"\midrule")

    gold_cells = []
    for ri, row in enumerate(spec["rows"]):
        label_tex = row.get("label_latex") or row["label"]
        cell_texts = []
        for ci, cell in enumerate(row["cells"]):
            tex = cell.get("latex") or cell["text"]
            tex = _ensure_math(tex)
            cell_texts.append(tex)
            gold_cells.append({
                "row": ri, "col": ci + 1,
                "text": cell["text"],
                "latex": cell.get("latex", ""),
                "role": "data",
            })
        lines.append(f"{label_tex} & " + " & ".join(cell_texts) + r" \\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    if spec.get("notes"):
        notes_text = spec["notes"] if isinstance(spec["notes"], str) else spec["notes"][0]
        lines.append(f"\\\\\\small\\textit{{Notes:}} {notes_text}")
    lines.append(r"\end{table}")

    return TableSpec(
        table_id=spec["table_id"],
        caption=spec["caption"],
        label=spec["label"],
        latex="\n".join(lines),
        gold_cells=gold_cells,
        qa=spec.get("qa", []),
    )


# ═══════════════════════════════════════════════════════════════════════════
# Document assembly
# ═══════════════════════════════════════════════════════════════════════════

# ── Journal-specific preambles ──
# Each mimics the typographic style of a real journal using only standard CTAN
# packages, giving the benchmark suite visual diversity across papers.

_JOURNAL_PREAMBLES: dict[str, str] = {
    # ── Top-5 Economics ──
    "aer": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{mathptmx}                       % Times Roman (AER house font)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\onehalfspacing
\usepackage{natbib}\bibliographystyle{aer}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\renewcommand{\thesection}{\Roman{section}}  % AER: Roman numeral sections
\renewcommand{\thesubsection}{\Alph{subsection}}
""",
    "econometrica": r"""\documentclass[11pt]{article}
\usepackage[margin=1.25in]{geometry}
\usepackage{fourier}                        % Utopia (Econometrica house font)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{econometrica}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\renewcommand{\thesection}{\Roman{section}}  % Roman numeral sections
\renewcommand{\thesubsection}{\thesection.\Alph{subsection}}
""",
    "qje": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{palatino}                       % Palatino (QJE/Oxford house font)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\renewcommand{\thesection}{\Roman{section}}  % QJE: Roman numeral sections
\renewcommand{\thesubsection}{\Alph{subsection}}
\renewcommand{\thetable}{\Roman{table}}      % QJE: Roman numeral tables/figures
\renewcommand{\thefigure}{\Roman{figure}}
""",
    "jpe": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{charter}                        % Charter (JPE / U Chicago style)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\renewcommand{\thesection}{\Roman{section}}  % JPE: Roman numeral sections
\renewcommand{\thesubsection}{\Alph{subsection}}
""",
    "restud": r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{newpxtext,newpxmath}             % New PX (Palatino clone, REStud style)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\renewcommand{\thesection}{\arabic{section}.}
""",
    # ── Top-3 Finance ──
    "jf": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{lmodern}                        % Latin Modern (JF clean style)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\usepackage{titlesec}
\renewcommand{\thesection}{\Roman{section}}  % JF: Roman sections, centered headings
\renewcommand{\thesubsection}{\Alph{subsection}}
\titleformat{\section}{\large\bfseries\centering}{\thesection.}{1em}{}
""",
    "rfs": r"""\documentclass[11pt]{article}
\usepackage[margin=1.1in]{geometry}
\usepackage{mathptmx}                       % Times (RFS / Oxford style)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
""",
    "jfe": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{newtxtext,newtxmath}             % New TX (Times clone, JFE/Elsevier)
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
""",
    # ── Non-journal document formats ──
    "working_paper": r"""\documentclass[11pt]{article}
\usepackage[margin=0.8in]{geometry}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\onehalfspacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\usepackage{titlesec}
\titleformat{\section}{\large\sffamily\bfseries}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalsize\sffamily\bfseries}{\thesubsection.}{0.5em}{}
""",
    "typewriter": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{courier}
\renewcommand{\familydefault}{\ttdefault}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
""",
    "nber_wp": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{mathptmx}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\onehalfspacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{\small NBER WORKING PAPER SERIES}
\fancyhead[R]{\small\thepage}
\fancyfoot{}
""",
    "word_like": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{times}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\onehalfspacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
\renewcommand{\thesection}{\arabic{section}.}
\renewcommand{\thesubsection}{\thesection\arabic{subsection}.}
\usepackage{indentfirst}
""",
    "two_column": r"""\documentclass[11pt,twocolumn]{article}
\usepackage[margin=0.75in]{geometry}
\usepackage{mathptmx}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{booktabs,threeparttable,multirow,siunitx}
\usepackage{setspace}\onehalfspacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
""",
    "old_school": r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,mathtools,amsthm}
\usepackage{multirow,siunitx}
\usepackage{setspace}\doublespacing
\usepackage{natbib}\bibliographystyle{plain}
\usepackage{hyperref,graphicx,enumitem,caption}
\usepackage[T1]{fontenc}
""",
}

# Shared theorem environments appended to every preamble
_THEOREM_DEFS = r"""
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{assumption}{Assumption}
"""


def assemble_document(paper: PaperSpec) -> str:
    """Assemble a complete LaTeX document from a PaperSpec."""
    preamble = _JOURNAL_PREAMBLES.get(paper.journal_style, _JOURNAL_PREAMBLES["aer"])
    parts = [preamble + _THEOREM_DEFS]

    # Extra packages
    for pkg in paper.packages:
        parts.append(f"\\usepackage{{{pkg}}}")

    parts.append(f"\\title{{{paper.title}}}")
    parts.append(f"\\author{{{paper.authors}}}")
    parts.append(r"\date{\today}")
    parts.append(r"\begin{document}")
    parts.append(r"\maketitle")
    parts.append(r"\begin{abstract}")
    parts.append(paper.abstract)
    parts.append(r"\end{abstract}")
    parts.append(r"\newpage")
    parts.append(r"\tableofcontents")
    parts.append(r"\newpage")

    # Sections
    variables = _paper_variables(paper)

    for sec in paper.sections:
        parts.append(_render_section(sec, variables))

    # Bibliography
    parts.append(r"\newpage")
    parts.append(r"\begin{thebibliography}{99}")
    for entry in paper.bibliography_entries:
        parts.append(entry)
    parts.append(r"\end{thebibliography}")

    parts.append(r"\end{document}")
    return "\n\n".join(parts)


def _render_section(sec: SectionSpec, variables: dict) -> str:
    """Render a section and its subsections."""
    cmd = {1: r"\section", 2: r"\subsection", 3: r"\subsubsection"}[sec.level]
    parts = [f"{cmd}{{{sec.title}}}"]
    parts.append(f"\\label{{{sec.label}}}")

    # Determine section type for filler
    stype = _infer_section_type(sec.title)

    # Interleave filler text, equations, and tables
    n_para = sec.text_paragraphs
    filler = generate_filler(stype, variables, n_para)
    paras = filler.split("\n\n")

    # Place equations after first few paragraphs
    eq_insert_after = max(1, len(paras) // 3) if sec.equations else len(paras)
    # Place tables after the middle
    tab_insert_after = max(2, len(paras) * 2 // 3) if sec.tables else len(paras)

    eq_idx = 0
    tab_idx = 0
    for pi, para in enumerate(paras):
        parts.append(para)
        if pi == eq_insert_after and eq_idx < len(sec.equations):
            for eq in sec.equations:
                parts.append(_render_equation(eq))
                eq_idx += 1
        if pi == tab_insert_after and tab_idx < len(sec.tables):
            for tab in sec.tables:
                parts.append(tab.latex)
                tab_idx += 1

    # Any remaining equations/tables
    for eq in sec.equations[eq_idx:]:
        parts.append(_render_equation(eq))
    for tab in sec.tables[tab_idx:]:
        parts.append(tab.latex)

    # Subsections
    for sub in sec.subsections:
        parts.append(_render_section(sub, variables))

    return "\n\n".join(parts)


def _render_equation(eq: EquationSpec) -> str:
    """Render a displayed equation."""
    return (
        f"\\begin{{equation}}\n"
        f"\\label{{{eq.label}}}\n"
        f"{eq.latex}\n"
        f"\\end{{equation}}"
    )


def _infer_section_type(title: str) -> str:
    """Map section title to filler template type."""
    title_lower = title.lower()
    if any(w in title_lower for w in ["intro", "motivation", "background"]):
        return "intro"
    if any(w in title_lower for w in ["model", "theory", "framework", "setup"]):
        return "model"
    if any(w in title_lower for w in ["data", "sample", "measurement", "variable"]):
        return "data"
    if any(w in title_lower for w in ["result", "finding", "estimate", "main"]):
        return "results"
    if any(w in title_lower for w in ["robust", "sensitiv", "placebo", "alternative"]):
        return "robustness"
    if any(w in title_lower for w in ["conclu", "discussion", "summary"]):
        return "conclusion"
    if any(w in title_lower for w in ["appendix", "additional", "supplement"]):
        return "appendix"
    return "intro"


def _paper_variables(paper: PaperSpec) -> dict[str, str]:
    """Extract template variables from paper spec."""
    # Default variables; papers override via their specs
    defaults = {
        "field": paper.field_slug.replace("-", " "),
        "indep_var": "the treatment variable",
        "dep_var": "the outcome variable",
        "method": "an instrumental variables strategy",
        "data_source": "administrative records",
        "n_obs": "50,000",
        "period": "1990--2010",
        "unit": "individuals",
        "result_direction": "positive and significant",
        "instrument": "the proposed instrument",
        "outcome": "economic outcomes",
    }
    return defaults


# ═══════════════════════════════════════════════════════════════════════════
# Gold artifact extraction
# ═══════════════════════════════════════════════════════════════════════════

def extract_gold(paper: PaperSpec) -> dict:
    """Extract gold-standard artifacts from the paper spec."""

    def _walk_sections(secs: list[SectionSpec], out_sec, out_tab, out_eq):
        for sec in secs:
            out_sec.append({"title": sec.title, "label": sec.label, "level": sec.level})
            for tab in sec.tables:
                out_tab.append({
                    "table_id": tab.table_id, "caption": tab.caption,
                    "label": tab.label, "gold_cells": tab.gold_cells, "qa": tab.qa,
                })
            for eq in sec.equations:
                out_eq.append({
                    "eq_id": eq.eq_id, "label": eq.label, "latex": eq.latex,
                    "description": eq.description, "qa": eq.qa,
                })
            _walk_sections(sec.subsections, out_sec, out_tab, out_eq)

    sections, tables, equations = [], [], []
    _walk_sections(paper.sections, sections, tables, equations)

    # QA: combine paper-level + table-level + equation-level
    all_qa = list(paper.qa)
    for t in tables:
        all_qa.extend(t.get("qa", []))
    for e in equations:
        all_qa.extend(e.get("qa", []))

    return {
        "sections": sections,
        "tables": tables,
        "equations": equations,
        "qa": all_qa,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Compilation
# ═══════════════════════════════════════════════════════════════════════════

def compile_latex(tex_path: Path) -> Path | None:
    """Compile LaTeX to PDF. Returns PDF path or None on failure."""
    out_dir = tex_path.parent
    for compiler in ["latexmk", "tectonic", "pdflatex"]:
        try:
            if compiler == "latexmk":
                cmd = [
                    "latexmk", "-pdf", "-interaction=nonstopmode",
                    "-output-directory=" + str(out_dir),
                    str(tex_path),
                ]
            elif compiler == "tectonic":
                cmd = ["tectonic", "--outdir", str(out_dir), str(tex_path)]
            else:
                cmd = [
                    "pdflatex", "-interaction=nonstopmode",
                    f"-output-directory={out_dir}",
                    str(tex_path),
                ]

            subprocess.run(
                cmd, capture_output=True, timeout=120,
            )
            pdf_path = tex_path.with_suffix(".pdf")
            if pdf_path.exists():
                print(f"  Compiled with {compiler}: {pdf_path.name}")
                return pdf_path
            else:
                print(f"  {compiler} ran but no PDF produced")
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            print(f"  {compiler} timed out")
            continue

    print(f"  WARNING: Could not compile {tex_path.name}")
    return None


# ═══════════════════════════════════════════════════════════════════════════
# Paper registry
# ═══════════════════════════════════════════════════════════════════════════

PAPER_BUILDERS: dict[str, Callable[[], PaperSpec]] = {}

# Ensure builder modules import from this module instance (not a duplicate)
# when the script is run directly as __main__.
if __name__ == "__main__":
    sys.modules.setdefault("generate_long_form", sys.modules[__name__])

# Import builder modules — each registers itself in PAPER_BUILDERS on import
import paper_01  # noqa: F401,E402
import paper_02  # noqa: F401,E402
import paper_03  # noqa: F401,E402
import paper_04  # noqa: F401,E402
import paper_05  # noqa: F401,E402
import paper_06  # noqa: F401,E402
import paper_07  # noqa: F401,E402
import paper_08  # noqa: F401,E402
import paper_09  # noqa: F401,E402
import paper_10  # noqa: F401,E402
import paper_11  # noqa: F401,E402
import paper_12  # noqa: F401,E402
import paper_13  # noqa: F401,E402
import paper_14  # noqa: F401,E402
import paper_15  # noqa: F401,E402
import paper_16  # noqa: F401,E402
import paper_17  # noqa: F401,E402
import paper_18  # noqa: F401,E402
import paper_19  # noqa: F401,E402
import paper_20  # noqa: F401,E402


# Map paper IDs to table style presets
_PAPER_TABLE_STYLES: dict[str, str] = {
    "01": "aer_published",     "02": "stata_esttab",      "03": "r_stargazer",
    "04": "stata_outreg2",     "05": "econometrica_pub",  "06": "jf_endnotes",
    "07": "python_statsmodels", "08": "r_modelsummary",   "09": "nber_wp",
    "10": "old_school",        "11": "r_texreg",          "12": "manual_hline",
    "13": "sas_proc",          "14": "compact_conf",      "15": "excel_grid",
    "16": "minimal_clean",     "17": "stata_wide",        "18": "verbose_notes",
    "19": "landscape_wide",    "20": "qje_published",
}


def build_paper(paper_id: str) -> PaperSpec:
    """Build a paper spec by ID, setting the default table style."""
    global _default_table_style
    _default_table_style = _PAPER_TABLE_STYLES.get(paper_id, "")
    builder = PAPER_BUILDERS.get(paper_id)
    if not builder:
        raise ValueError(f"Unknown paper ID: {paper_id}. Available: {sorted(PAPER_BUILDERS)}")
    spec = builder()
    spec.table_style = _default_table_style
    _default_table_style = ""
    return spec


# ═══════════════════════════════════════════════════════════════════════════
# File I/O
# ═══════════════════════════════════════════════════════════════════════════

def write_paper(paper: PaperSpec, output_dir: Path, compile_pdf: bool = True) -> None:
    """Generate all artifacts for a paper."""
    slug = f"paper-{paper.paper_id}-{paper.field_slug}"
    case_dir = output_dir / slug
    case_dir.mkdir(parents=True, exist_ok=True)

    # Generate LaTeX
    tex_content = assemble_document(paper)
    tex_path = case_dir / "source.tex"
    tex_path.write_text(tex_content, encoding="utf-8")
    print(f"[{slug}] Wrote {tex_path.name} ({len(tex_content):,} chars)")

    # Compile
    if compile_pdf:
        pdf_path = compile_latex(tex_path)
        if pdf_path:
            print(f"[{slug}] PDF: {pdf_path}")

    # Extract gold — single file with metadata + all gold artifacts
    gold = extract_gold(paper)
    gold_combined = {
        "paper_id": paper.paper_id,
        "field": paper.field_slug,
        "title": paper.title,
        "journal_style": paper.journal_style,
        "target_pages": paper.target_pages,
        "sections": gold["sections"],
        "tables": gold["tables"],
        "equations": gold["equations"],
        "qa": gold["qa"],
    }
    (case_dir / "gold.json").write_text(
        json.dumps(gold_combined, indent=2), encoding="utf-8")

    print(f"[{slug}] Gold: {len(gold['tables'])} tables, "
          f"{len(gold['equations'])} equations, {len(gold['qa'])} QA pairs")


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent.parent / "cases",
                        help="Output directory for generated papers")
    parser.add_argument("--paper-id", action="append", dest="paper_ids",
                        help="Generate specific paper(s) by ID (repeatable)")
    parser.add_argument("--no-compile", action="store_true",
                        help="Skip PDF compilation (LaTeX + gold only)")
    parser.add_argument("--list", action="store_true",
                        help="List available papers and exit")
    args = parser.parse_args()

    if args.list:
        for pid in sorted(PAPER_BUILDERS):
            spec = PAPER_BUILDERS[pid]()
            print(f"  {pid}: [{spec.field_slug}] {spec.title}")
        return

    ids = args.paper_ids or sorted(PAPER_BUILDERS)
    print(f"Generating {len(ids)} paper(s)...")

    built_specs: dict[str, PaperSpec] = {}
    for pid in ids:
        print(f"\n{'='*60}")
        paper = build_paper(pid)
        built_specs[pid] = paper
        write_paper(paper, args.output_dir, compile_pdf=not args.no_compile)

    # Write master manifest (reuse already-built specs; only build missing ones)
    manifest_entries = []
    for pid in sorted(PAPER_BUILDERS):
        spec = built_specs.get(pid) or PAPER_BUILDERS[pid]()
        slug = f"paper-{spec.paper_id}-{spec.field_slug}"
        manifest_entries.append({
            "paper_id": spec.paper_id,
            "field": spec.field_slug,
            "title": spec.title,
            "case_dir": slug,
        })
    manifest_path = args.output_dir.parent / "manifest.long-form.json"
    manifest_path.write_text(json.dumps(manifest_entries, indent=2), encoding="utf-8")
    print(f"\nWrote manifest: {manifest_path}")
    print("Done.")


if __name__ == "__main__":
    main()
