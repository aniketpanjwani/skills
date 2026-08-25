#!/usr/bin/env python3
"""Paper builder for paper 10 (Political Economy)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table,
    PAPER_BUILDERS,
)


# ═══════════════════════════════════════════════════════════════════════════
# Paper 10: Political Economy — Media, Accountability, and Corruption
# ═══════════════════════════════════════════════════════════════════════════

def _paper_10_political_economy() -> PaperSpec:
    """Paper 10: Political Economy — media exposure, government accountability."""

    # ── Tables ──
    summary_stats = render_regression_table({
        "table_id": "summary-stats",
        "caption": "Summary Statistics",
        "label": "tab:summary-stats",
        "model_labels": ["Mean", "SD", "Min", "Max", "N"],
        "panels": [{
            "dep_var": "Panel A: Municipality Characteristics",
            "variables": [
                {"label": "Population (thousands)", "coefficients": ["31.4", "98.2", "0.8", "1,024.3", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Log per capita income", "coefficients": ["7.82", "0.64", "5.91", "9.84", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Literacy rate", "coefficients": ["0.74", "0.14", "0.31", "0.97", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Urbanization rate", "coefficients": ["0.58", "0.24", "0.04", "1.00", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }, {
            "dep_var": "Panel B: Media and Corruption Variables",
            "variables": [
                {"label": "Number of local radio stations", "coefficients": ["2.41", "2.18", "0", "14", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Has local newspaper", "coefficients": ["0.34", "0.47", "0", "1", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Audit irregularities (share of resources)", "coefficients": ["0.082", "0.104", "0.000", "0.891", "1,891"],
                 "std_errors": ["", "", "", "", ""]},
                {"label": "Re-election rate", "coefficients": ["0.42", "0.49", "0", "1", "1,456"],
                 "std_errors": ["", "", "", "", ""]},
            ],
        }],
        "notes": "Audit irregularities measured as share of federal transfers with detected misuse. Re-election rate conditional on incumbents running. Sample: Brazilian municipalities audited 2003--2008.",
        "qa": [
            {"question": "What is the mean share of resources with audit irregularities?", "answer": "0.082 (8.2 percent)"},
            {"question": "How many municipalities are in the sample?", "answer": "1,891"},
            {"question": "What fraction of municipalities have a local newspaper?", "answer": "0.34 (34 percent)"},
            {"question": "What is the mean number of local radio stations?", "answer": "2.41"},
        ],
    })

    main_results = render_regression_table({
        "table_id": "main-results",
        "caption": "Effect of Audit Disclosure on Electoral Accountability",
        "label": "tab:main-results",
        "model_labels": ["(1)", "(2)", "(3)", "(4)", "(5)"],
        "panels": [{
            "dep_var": "Dep. var.: Incumbent Vote Share",
            "variables": [
                {"label": "Audit disclosed before election", "coefficients": ["-0.041***", "-0.038***", "-0.036***", "-0.034***", "-0.032***"],
                 "std_errors": ["(0.008)", "(0.008)", "(0.008)", "(0.008)", "(0.009)"]},
                {"label": "Irregularity share", "coefficients": ["", "-0.112***", "-0.108***", "-0.094***", "-0.091***"],
                 "std_errors": ["", "(0.024)", "(0.024)", "(0.028)", "(0.028)"]},
                {"label": "Disclosed $\\times$ Irregularity", "coefficients": ["", "", "-0.084***", "-0.078***", "-0.074***"],
                 "std_errors": ["", "", "(0.028)", "(0.028)", "(0.029)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["No", "No", "No", "Yes", "Yes"]},
            {"label": "State fixed effects", "values": ["No", "No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1,456", "1,456", "1,456", "1,456", "1,456"]},
            {"label": "R-squared", "values": ["0.014", "0.028", "0.034", "0.118", "0.184"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors clustered at state level in parentheses. Sample: municipalities where incumbents sought re-election. Disclosure timing determined by random audit lottery.",
        "qa": [
            {"question": "What is the main effect of audit disclosure on incumbent vote share?", "answer": "-0.041 (4.1 percentage point decrease) in column 1"},
            {"question": "What is the interaction effect of disclosure and irregularity share?", "answer": "-0.084 in column 3, indicating larger electoral penalties in more corrupt municipalities"},
            {"question": "What controls are included in column 5?", "answer": "Municipality controls and state fixed effects"},
            {"question": "How are standard errors clustered?", "answer": "At the state level"},
        ],
    })

    media_interaction = render_regression_table({
        "table_id": "media-interaction",
        "caption": "Media Exposure and the Electoral Effect of Audits",
        "label": "tab:media-interaction",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Incumbent Vote Share",
            "variables": [
                {"label": "Disclosed $\\times$ Irregularity", "coefficients": ["-0.024", "-0.028", "-0.018", "-0.022"],
                 "std_errors": ["(0.032)", "(0.031)", "(0.034)", "(0.033)"]},
                {"label": "Disclosed $\\times$ Irr. $\\times$ Local radio", "coefficients": ["-0.058***", "", "-0.042**", ""],
                 "std_errors": ["(0.018)", "", "(0.019)", ""]},
                {"label": "Disclosed $\\times$ Irr. $\\times$ Newspaper", "coefficients": ["", "-0.071***", "", "-0.054***"],
                 "std_errors": ["", "(0.022)", "", "(0.024)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State fixed effects", "values": ["No", "No", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1,456", "1,456", "1,456", "1,456"]},
            {"label": "R-squared", "values": ["0.138", "0.141", "0.198", "0.201"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors clustered at state level. Local radio: indicator for above-median radio stations. The electoral penalty from audit disclosure operates primarily through media dissemination.",
        "qa": [
            {"question": "Is the electoral penalty from audits larger in municipalities with local radio?", "answer": "Yes, the triple interaction is -0.058 (significant at 1% level)"},
            {"question": "Is the electoral penalty from audits larger in municipalities with newspapers?", "answer": "Yes, the triple interaction is -0.071 (significant at 1% level)"},
            {"question": "Is there an electoral penalty in municipalities without media?", "answer": "The base interaction is -0.024, small and insignificant, suggesting minimal penalty without media"},
        ],
    })

    corruption_outcomes = render_regression_table({
        "table_id": "corruption-outcomes",
        "caption": "Effect of Audit Disclosure on Subsequent Corruption",
        "label": "tab:corruption-outcomes",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Irregularity Share in Next Audit",
            "variables": [
                {"label": "Prior audit disclosed", "coefficients": ["-0.028***", "-0.024***", "-0.022**", "-0.018**"],
                 "std_errors": ["(0.008)", "(0.008)", "(0.009)", "(0.009)"]},
                {"label": "Prior irregularity share", "coefficients": ["", "0.384***", "0.371***", "0.362***"],
                 "std_errors": ["", "(0.041)", "(0.042)", "(0.044)"]},
                {"label": "Disclosed $\\times$ Prior irr.", "coefficients": ["", "", "-0.148***", "-0.134***"],
                 "std_errors": ["", "", "(0.048)", "(0.049)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["No", "No", "No", "Yes"]},
            {"label": "State fixed effects", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["842", "842", "842", "842"]},
            {"label": "R-squared", "values": ["0.012", "0.158", "0.172", "0.248"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors clustered at state level. Sample restricted to municipalities audited in both periods. Audit disclosure reduces subsequent corruption by 2.8 percentage points.",
        "qa": [
            {"question": "Does audit disclosure reduce subsequent corruption?", "answer": "Yes, by 2.8 percentage points of federal transfers (column 1)"},
            {"question": "Is the persistence of corruption significant?", "answer": "Yes, prior irregularity share coefficient is 0.384 (highly persistent)"},
            {"question": "Is the deterrence effect larger for more corrupt municipalities?", "answer": "Yes, the interaction is -0.148, indicating stronger deterrence where prior corruption was higher"},
        ],
    })

    reelection = render_regression_table({
        "table_id": "reelection",
        "caption": "Effect of Audit Disclosure on Re-Election Probability",
        "label": "tab:reelection",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [{
            "dep_var": "Dep. var.: Re-Election Indicator",
            "variables": [
                {"label": "Disclosed $\\times$ High irr.", "coefficients": ["-0.098***", "-0.091***", "-0.084***", "-0.078***"],
                 "std_errors": ["(0.024)", "(0.024)", "(0.025)", "(0.026)"]},
                {"label": "Disclosed $\\times$ Low irr.", "coefficients": ["-0.012", "-0.008", "-0.004", "-0.002"],
                 "std_errors": ["(0.018)", "(0.018)", "(0.018)", "(0.019)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "State fixed effects", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Party fixed effects", "values": ["No", "No", "No", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1,456", "1,456", "1,456", "1,456"]},
            {"label": "Control mean (high irr.)", "values": ["0.38", "0.38", "0.38", "0.38"]},
            {"label": "Control mean (low irr.)", "values": ["0.48", "0.48", "0.48", "0.48"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors clustered at state level. High irregularity: above-median irregularity share. Voters punish corruption only when informed by audit disclosure.",
        "qa": [
            {"question": "Does audit disclosure reduce re-election of corrupt mayors?", "answer": "Yes, by 9.8 percentage points for high-irregularity mayors (column 1)"},
            {"question": "Does audit disclosure affect re-election of non-corrupt mayors?", "answer": "No, the effect for low-irregularity mayors is -0.012 and insignificant"},
            {"question": "What is the control mean re-election rate for high-irregularity mayors?", "answer": "0.38 (38 percent)"},
        ],
    })

    rd_results = render_regression_table({
        "table_id": "rd-results",
        "caption": "Regression Discontinuity: Audit Disclosure Timing",
        "label": "tab:rd-results",
        "model_labels": ["Vote Share", "Re-Election", "Turnout", "Challenger Entry"],
        "panels": [{
            "dep_var": "Panel A: Local Linear (h=60 days)",
            "variables": [
                {"label": "Disclosed before election", "coefficients": ["-0.038***", "-0.084**", "0.024**", "0.218***"],
                 "std_errors": ["(0.012)", "(0.038)", "(0.011)", "(0.062)"]},
            ],
        }, {
            "dep_var": "Panel B: Local Quadratic (h=90 days)",
            "variables": [
                {"label": "Disclosed before election", "coefficients": ["-0.041***", "-0.091**", "0.028**", "0.241***"],
                 "std_errors": ["(0.014)", "(0.042)", "(0.013)", "(0.068)"]},
            ],
        }],
        "summary": [
            {"label": "Observations (h=60)", "values": ["512", "512", "512", "512"]},
            {"label": "Observations (h=90)", "values": ["684", "684", "684", "684"]},
            {"label": "Bandwidth (days)", "values": ["60", "60", "60", "60"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors. Running variable: days between audit release and election. Cutoff: election date. Positive values indicate disclosure before election.",
        "qa": [
            {"question": "What is the RD estimate of audit disclosure on vote share?", "answer": "-0.038 with the local linear estimator"},
            {"question": "Does audit disclosure increase voter turnout?", "answer": "Yes, by 2.4 percentage points (local linear)"},
            {"question": "Does audit disclosure increase challenger entry?", "answer": "Yes, by 21.8 percentage points"},
        ],
    })

    mechanisms = render_regression_table({
        "table_id": "mechanisms",
        "caption": "Mechanisms: How Information Reaches Voters",
        "label": "tab:mechanisms",
        "model_labels": ["Radio Mentions", "Print Coverage", "Campaign Topic", "Voter Awareness"],
        "panels": [{
            "dep_var": "Dep. var.: Information Channel Indicator",
            "variables": [
                {"label": "Audit disclosed", "coefficients": ["0.412***", "0.284***", "0.168***", "0.342***"],
                 "std_errors": ["(0.048)", "(0.042)", "(0.038)", "(0.044)"]},
                {"label": "Disclosed $\\times$ Irr. share", "coefficients": ["0.184***", "0.142***", "0.098**", "0.218***"],
                 "std_errors": ["(0.052)", "(0.048)", "(0.042)", "(0.058)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["Yes", "Yes", "Yes", "Yes"]},
            {"label": "State fixed effects", "values": ["Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1,891", "1,891", "1,456", "4,812"]},
            {"label": "Control mean", "values": ["0.12", "0.08", "0.14", "0.18"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors clustered at state level. Radio mentions: indicator for local radio coverage of audit. Voter awareness from post-election survey.",
        "qa": [
            {"question": "Does audit disclosure increase radio coverage?", "answer": "Yes, by 41.2 percentage points"},
            {"question": "Does disclosure increase voter awareness of corruption?", "answer": "Yes, by 34.2 percentage points"},
            {"question": "What is the control mean of voter awareness?", "answer": "0.18 (18 percent)"},
        ],
    })

    placebo = render_regression_table({
        "table_id": "placebo",
        "caption": "Placebo Tests: Pre-Audit Electoral Outcomes",
        "label": "tab:placebo",
        "model_labels": ["Prior Vote Share", "Prior Re-Election", "Prior Turnout"],
        "panels": [{
            "dep_var": "Dep. var.: Electoral Outcome in Election Before Audit",
            "variables": [
                {"label": "Will be disclosed", "coefficients": ["0.004", "-0.008", "0.002"],
                 "std_errors": ["(0.009)", "(0.021)", "(0.008)"]},
                {"label": "Will be disclosed $\\times$ Irr.", "coefficients": ["0.012", "-0.018", "0.008"],
                 "std_errors": ["(0.028)", "(0.042)", "(0.024)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["Yes", "Yes", "Yes"]},
            {"label": "State fixed effects", "values": ["Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1,224", "1,224", "1,224"]},
        ],
        "notes": "Placebo test: regressing prior election outcomes on future audit disclosure. All coefficients are small and insignificant, confirming that disclosure timing is orthogonal to pre-existing electoral trends.",
        "qa": [
            {"question": "Do placebo tests reject the null?", "answer": "No, all coefficients are small and insignificant, supporting the identification strategy"},
        ],
    })

    robustness = render_regression_table({
        "table_id": "robustness",
        "caption": "Robustness: Alternative Specifications",
        "label": "tab:robustness",
        "model_labels": ["Baseline", "Ordered Probit", "Drop Top 5\\%", "Alternative Irr.", "Weighted"],
        "panels": [{
            "dep_var": "Dep. var.: Incumbent Vote Share",
            "variables": [
                {"label": "Disclosed $\\times$ Irr.", "coefficients": ["-0.074***", "-0.068***", "-0.081***", "-0.064***", "-0.078***"],
                 "std_errors": ["(0.029)", "(0.024)", "(0.031)", "(0.028)", "(0.030)"]},
            ],
        }],
        "controls": [
            {"label": "Municipality controls", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
            {"label": "State fixed effects", "values": ["Yes", "Yes", "Yes", "Yes", "Yes"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["1,456", "1,456", "1,384", "1,456", "1,456"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Robust standard errors clustered at state level. Column 3 drops top 5\\% of irregularity share. Column 4 uses count of irregularities instead of share. Column 5 weights by inverse population.",
        "qa": [
            {"question": "Are results robust to dropping top 5% outliers?", "answer": "Yes, the coefficient is -0.081 (slightly larger), significant at 1%"},
            {"question": "Are results robust to ordered probit?", "answer": "Yes, the coefficient is -0.068, significant at 1%"},
        ],
    })

    appendix_audit = render_regression_table({
        "table_id": "appendix-audit-process",
        "caption": "Appendix: Audit Lottery Selection and Balance",
        "label": "tab:appendix-audit",
        "model_labels": ["Audited", "Not Audited", "Difference", "p-value"],
        "panels": [{
            "dep_var": "Municipal Characteristics",
            "variables": [
                {"label": "Log population", "coefficients": ["9.84", "9.81", "0.03", "0.62"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Log per capita income", "coefficients": ["7.81", "7.84", "-0.03", "0.54"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Urbanization", "coefficients": ["0.57", "0.58", "-0.01", "0.68"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Literacy rate", "coefficients": ["0.73", "0.74", "-0.01", "0.41"],
                 "std_errors": ["", "", "", ""]},
                {"label": "Mayor party alignment", "coefficients": ["0.31", "0.32", "-0.01", "0.72"],
                 "std_errors": ["", "", "", ""]},
            ],
        }],
        "summary": [
            {"label": "Joint F-test p-value", "values": ["", "", "", "0.78"]},
            {"label": "N municipalities", "values": ["1,891", "3,648", "", ""]},
        ],
        "notes": "Balance test: audited vs. non-audited municipalities. Random lottery selection ensures balance. Joint F-test p-value of 0.78 confirms randomization.",
        "qa": [
            {"question": "Is the audit lottery random?", "answer": "Yes, the joint F-test p-value is 0.78, confirming balance"},
        ],
    })

    # --- Equations ---
    eq_voting = EquationSpec(
        "voting-model",
        r"v_i^* = \mu + \beta D_i + \gamma C_i + \delta (D_i \times C_i) + X_i'\theta + \varepsilon_i",
        "eq:voting",
        "Voting model: $v_i^*$ is incumbent vote share, $D_i$ is disclosure indicator, $C_i$ is corruption measure, and the interaction $D_i \\times C_i$ captures information-dependent accountability.",
        [{"question": "What does the interaction term D_i x C_i capture?", "answer": "The additional electoral penalty for corruption that occurs when voters are informed by audit disclosure"}],
    )

    eq_accountability = EquationSpec(
        "accountability-condition",
        r"\frac{\partial v}{\partial C} \bigg|_{D=1} = \gamma + \delta < 0 \quad \text{(informed accountability)}",
        "eq:accountability",
        "Accountability condition: when audits are disclosed ($D=1$), the electoral penalty for corruption is $\\gamma + \\delta$. The key prediction is $\\delta < 0$.",
    )

    eq_media_channel = EquationSpec(
        "media-channel",
        r"v_i^* = \mu + \beta D_i + \gamma C_i + \delta_1 (D_i \times C_i \times M_i) + \delta_0 (D_i \times C_i \times (1-M_i)) + X_i'\theta + \varepsilon_i",
        "eq:media-channel",
        "Extended model decomposing accountability by media presence $M_i$. Tests whether electoral punishment requires media to inform voters.",
    )

    eq_bayesian = EquationSpec(
        "bayesian-updating",
        r"\dot{\pi}_i = \frac{\int_0^1 \Pr(s_i | \pi_H, \omega)\, d\omega}{\int_0^1 \Pr(s_i | \pi_H, \omega)\, d\omega + \int_0^1 \Pr(s_i | \pi_L, \omega)\, d\omega} \cdot \frac{\Pr(\pi_H)}{\Pr(\pi_H) + \Pr(\pi_L)}",
        "eq:bayesian",
        "Bayesian updating: voter posterior belief about incumbent type ($\\pi_H$ = honest) given audit signal $s_i$.",
    )

    eq_optimal_vote = EquationSpec(
        "optimal-vote",
        r"\text{Vote}_i = \mathbf{1}\left\{\hat{\pi}_i > \bar{\pi}(b_C)\right\}, \quad \bar{\pi}(b_C) = \frac{u(b_C)}{u(b_H) - u(b_D)}",
        "eq:optimal-vote",
        "Optimal voting rule: re-elect the incumbent iff the posterior probability of honesty exceeds a threshold determined by the relative payoffs.",
    )

    eq_deterrence = EquationSpec(
        "deterrence",
        r"\dot{C}_t^* = \arg\max_{C} \left\{\int_0^\infty R(C, \omega)\, d\omega - p \cdot L(C) - (1-p) \cdot \begin{bmatrix} \Pr(\text{audit}) \\ \Delta \dot{v}(C) \\ V \end{bmatrix}' \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix}\right\}",
        "eq:deterrence",
        "Official's optimal corruption $C^*$: balances rent extraction $R(C)$, legal penalty $L(C)$, and electoral sanction $\\Delta v(C)$ weighted by audit probability and value of office $V$.",
        [{"question": "What determines the optimal level of corruption?", "answer": "The tradeoff between rents from corruption, legal penalties, and electoral sanctions conditional on audit probability"}],
    )

    eq_rd = EquationSpec(
        "rd-specification",
        r"v_i = \alpha + \tau \cdot \mathbf{1}(d_i > 0) + f(d_i) + X_i'\gamma + \varepsilon_i, \quad d_i = \text{election date} - \text{audit release date}",
        "eq:rd",
        "Regression discontinuity: $d_i$ is days between audit release and election. Treatment: audit disclosed before election ($d_i > 0$). $f(d_i)$ is local polynomial.",
    )

    eq_welfare = EquationSpec(
        "welfare-selection",
        r"\Delta W = \underbrace{\Pr(\text{high type elected} | D=1) - \Pr(\text{high type elected} | D=0)}_{\text{selection effect}} \times (V_H - V_L)",
        "eq:welfare",
        "Welfare gain from audit disclosure: improved selection of honest politicians times the value difference between high and low types.",
    )

    eq_information_value = EquationSpec(
        "information-value",
        r"\text{VOI} = E_s\left[\max_a u(a, \theta) | s\right] - \max_a E_\theta\left[u(a, \theta)\right]",
        "eq:voi",
        "Value of information (VOI): expected gain from making informed decisions (conditional on signal $s$) minus the value of the best uninformed decision.",
    )

    eq_persistence = EquationSpec(
        "persistence-model",
        r"\dot{C}_{i,t+1} = \rho \ddot{C}_{i,t} + \phi D_{i,t} \times \dot{C}_{i,t} + X_{i,t}'\begin{bmatrix}\psi_1 \\ \psi_2 \\ \vdots \\ \psi_K\end{bmatrix} + \eta_{i,t}",
        "eq:persistence",
        "Persistence of corruption: $\\rho$ captures baseline persistence; $\\phi$ measures the deterrence effect of disclosure on future corruption.",
    )

    # --- Appendix proof block ---
    appendix_proof_text = r"""
\begin{proposition}[Equilibrium Electoral Accountability]
Consider a two-period model with an incumbent of unknown type $\theta \in \{\theta_H, \theta_L\}$ and a voter who observes signal $s \in \{0, 1\}$ (audit disclosure). Let $\Pr(\theta_H) = \mu_0$ be the prior.

Under Bayesian updating, the voter's posterior after observing signal $s$ is:
\begin{align}
\mu_1(s) = \frac{\Pr(s | \theta_H) \mu_0}{\Pr(s | \theta_H) \mu_0 + \Pr(s | \theta_L)(1 - \mu_0)}.
\end{align}

The voter re-elects iff $\mu_1(s) \geq \bar{\mu}$, where $\bar{\mu} = u_L / (u_H - u_L + u_L)$ is the re-election threshold. In equilibrium:
\begin{itemize}
\item If $\Pr(s=\text{corrupt} | \theta_L) > \Pr(s=\text{corrupt} | \theta_H)$ (informativeness), disclosure of corruption reduces re-election probability for $\theta_L$ types.
\item The magnitude of the electoral penalty is:
\begin{align}
\Delta v = \Pr(\text{re-elect} | s=\text{clean}) - \Pr(\text{re-elect} | s=\text{corrupt}) = \Phi\left(\frac{\mu_1(\text{clean}) - \bar{\mu}}{\sigma}\right) - \Phi\left(\frac{\mu_1(\text{corrupt}) - \bar{\mu}}{\sigma}\right).
\end{align}
\end{itemize}
\end{proposition}

\begin{proof}
Under the assumed signal structure, $\Pr(s=\text{corrupt} | \theta_L) = q_L > q_H = \Pr(s=\text{corrupt} | \theta_H)$ with $q_L > q_H$ (informativeness). Then:
\begin{align}
\mu_1(\text{corrupt}) = \frac{q_H \mu_0}{q_H \mu_0 + q_L(1-\mu_0)} < \mu_0 < \frac{(1-q_H)\mu_0}{(1-q_H)\mu_0 + (1-q_L)(1-\mu_0)} = \mu_1(\text{clean}).
\end{align}
Since $\mu_1(\text{corrupt}) < \mu_0 < \mu_1(\text{clean})$, the re-election probability conditional on a corrupt signal is strictly lower than conditional on a clean signal, establishing the accountability mechanism.
\end{proof}

\begin{proposition}[Deterrence Effect of Audits]
In the official's optimization problem, the first-order condition for optimal corruption is:
\begin{align}
R'(C^*) = p \cdot L'(C^*) + (1-p) \cdot \Pr(\text{audit}) \cdot \Delta v'(C^*) \cdot V.
\end{align}
An increase in audit probability $\Pr(\text{audit})$ unambiguously reduces $C^*$ if $\Delta v'(C) > 0$ (greater corruption increases electoral penalty) and $R''(C) < 0$ (diminishing returns to corruption).

The deterrence effect is larger when:
\begin{enumerate}
\item The value of office $V$ is higher (higher-stakes elections)
\item Media coverage amplifies $\Delta v$ (information dissemination)
\item Voters have lower prior beliefs $\mu_0$ about politician honesty (already suspicious)
\end{enumerate}
\end{proposition}

\begin{proposition}[Identification via Audit Lottery]
Let $Z_i$ be the lottery indicator (audit selected = 1). Under random lottery selection:
\begin{align}
E[C_i(0) | Z_i = 1] &= E[C_i(0) | Z_i = 0] \quad \text{(balance)}, \\
E[v_i(0) | Z_i = 1] &= E[v_i(0) | Z_i = 0] \quad \text{(no pre-trends)}.
\end{align}
The treatment effect is identified as:
\begin{align}
\tau = E[v_i | Z_i = 1, D_i = 1] - E[v_i | Z_i = 1, D_i = 0],
\end{align}
where $D_i = 1$ if the audit is disclosed before the election (timing variation). The RD design exploits the sharp discontinuity at $d_i = 0$ (election date).
\end{proposition}

\noindent\textbf{Welfare integral.} The expected welfare gain from the audit program integrates over the distribution of corruption types:
\begin{align}
\Delta \dot{W} &= \int_0^1 \left[\dot{v}(\theta_H) - \dot{v}(\theta_L)\right] \cdot \begin{bmatrix} \ddot{\mu}_1(s) \\ 1 - \ddot{\mu}_1(s) \end{bmatrix}' \begin{bmatrix} u_H \\ u_L \end{bmatrix} \, dF(\theta).
\end{align}
The matrix representation of the selection and deterrence channels is
\begin{align}
\begin{bmatrix} \Delta \dot{v} \\ \Delta \dot{C} \end{bmatrix} &= \begin{bmatrix} \gamma + \delta & 0 \\ \phi & \rho \end{bmatrix} \begin{bmatrix} D_i \cdot \ddot{C}_i \\ \dot{C}_{i,t-1} \end{bmatrix} + \begin{bmatrix} \varepsilon_i \\ \eta_i \end{bmatrix}.
\end{align}
"""

    appendix_proof_table = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---
    intro = SectionSpec("Introduction", "sec:intro-pe", text_paragraphs=14,
                        equations=[eq_voting])

    institutional_bg = SectionSpec(
        "Institutional Background", "sec:background-pe", text_paragraphs=10,
        subsections=[
            SectionSpec("The Brazilian Anti-Corruption Program", "sec:anti-corruption", level=2, text_paragraphs=8),
            SectionSpec("Audit Lottery and Disclosure Process", "sec:audit-lottery", level=2, text_paragraphs=7),
            SectionSpec("Local Media Landscape", "sec:media-landscape", level=2, text_paragraphs=6),
        ],
    )

    theory = SectionSpec(
        "Theoretical Framework", "sec:theory-pe", text_paragraphs=12,
        equations=[eq_bayesian, eq_optimal_vote, eq_accountability, eq_deterrence],
        subsections=[
            SectionSpec("A Model of Electoral Accountability", "sec:model-accountability", level=2, text_paragraphs=8),
            SectionSpec("The Role of Information", "sec:model-information", level=2, text_paragraphs=7),
            SectionSpec("Testable Predictions", "sec:model-predictions", level=2, text_paragraphs=6),
        ],
    )

    data = SectionSpec(
        "Data", "sec:data-pe", text_paragraphs=10,
        tables=[summary_stats],
        subsections=[
            SectionSpec("Audit Data", "sec:data-audit", level=2, text_paragraphs=7),
            SectionSpec("Electoral Data", "sec:data-electoral", level=2, text_paragraphs=6),
            SectionSpec("Media Data", "sec:data-media", level=2, text_paragraphs=6),
        ],
    )

    empirical_strategy = SectionSpec(
        "Empirical Strategy", "sec:empirical-pe", text_paragraphs=10,
        equations=[eq_rd, eq_media_channel],
        subsections=[
            SectionSpec("Identification", "sec:identification", level=2, text_paragraphs=8),
            SectionSpec("Regression Discontinuity Design", "sec:rd-design", level=2, text_paragraphs=7),
        ],
    )

    results = SectionSpec(
        "Results", "sec:results-pe", text_paragraphs=10,
        tables=[main_results, reelection, media_interaction],
        subsections=[
            SectionSpec("Electoral Accountability", "sec:results-electoral", level=2, text_paragraphs=8),
            SectionSpec("The Role of Media", "sec:results-media", level=2, text_paragraphs=7),
            SectionSpec("RD Estimates", "sec:results-rd", level=2, text_paragraphs=7,
                        tables=[rd_results]),
        ],
    )

    mechanisms_section = SectionSpec(
        "Mechanisms", "sec:mechanisms-pe", text_paragraphs=10,
        tables=[mechanisms],
        equations=[eq_information_value],
        subsections=[
            SectionSpec("Information Channels", "sec:info-channels", level=2, text_paragraphs=7),
            SectionSpec("Voter Learning", "sec:voter-learning", level=2, text_paragraphs=7),
        ],
    )

    deterrence_section = SectionSpec(
        "Deterrence Effects", "sec:deterrence", text_paragraphs=10,
        tables=[corruption_outcomes],
        equations=[eq_persistence],
    )

    robustness_section = SectionSpec(
        "Robustness and Placebo Tests", "sec:robustness-pe", text_paragraphs=10,
        tables=[robustness, placebo],
        equations=[eq_welfare],
    )

    conclusion = SectionSpec("Conclusion", "sec:conclusion-pe", text_paragraphs=10)

    appendix_a = SectionSpec(
        "Appendix A: Proofs", "sec:appendix-a-pe", text_paragraphs=3,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Balance and Sample", "sec:appendix-b-pe", text_paragraphs=5,
        tables=[appendix_audit],
    )

    return PaperSpec(
        paper_id="10",
        field_slug="political-economy",
        title="Information, Accountability, and Corruption: Evidence from Random Audits in Brazil",
        authors="Claudio Ferraz, Frederico Finan, Miriam Costa",
        journal_style="rfs",
        abstract=(
            "We study how information about government corruption affects electoral accountability using "
            "Brazil's random municipal audit program. Municipalities randomly selected for audits that are "
            "disclosed before elections see a 4.1 percentage point decline in incumbent vote share. This "
            "penalty is concentrated among mayors with high detected irregularities and is amplified by "
            "local media: the interaction of disclosure, corruption, and radio presence yields an additional "
            "5.8 percentage point vote decline. Using a regression discontinuity design based on audit "
            "disclosure timing, we confirm the causal effect. Disclosed audits also deter future corruption, "
            "reducing irregularities by 2.8 percentage points in subsequent audits. A Bayesian model of "
            "voter learning rationalizes these findings: voters update beliefs about incumbent quality upon "
            "receiving audit signals, but only when media disseminates the information."
        ),
        sections=[intro, institutional_bg, theory, data, empirical_strategy, results,
                  mechanisms_section, deterrence_section, robustness_section,
                  conclusion, appendix_a, appendix_b],
        bibliography_entries=[
            r"\bibitem{ferraz2008} Ferraz, C. and Finan, F. (2008). Exposing Corrupt Politicians: The Effects of Brazil's Publicly Released Audits on Electoral Outcomes. \textit{Quarterly Journal of Economics}, 123(2), 703--745.",
            r"\bibitem{ferraz2011} Ferraz, C. and Finan, F. (2011). Electoral Accountability and Corruption: Evidence from the Audits of Local Governments. \textit{American Economic Review}, 101(4), 1274--1311.",
            r"\bibitem{besley2002} Besley, T. and Burgess, R. (2002). The Political Economy of Government Responsiveness: Theory and Evidence from India. \textit{Quarterly Journal of Economics}, 117(4), 1415--1451.",
            r"\bibitem{stromberg2004} Stromberg, D. (2004). Radio's Impact on Public Spending. \textit{Quarterly Journal of Economics}, 119(1), 189--221.",
            r"\bibitem{gentzkow2011} Gentzkow, M., Shapiro, J. M., and Sinkinson, M. (2011). The Effect of Newspaper Entry and Exit on Electoral Politics. \textit{American Economic Review}, 101(7), 2980--3018.",
            r"\bibitem{olken2007} Olken, B. A. (2007). Monitoring Corruption: Evidence from a Field Experiment in Indonesia. \textit{Journal of Political Economy}, 115(2), 200--249.",
            r"\bibitem{banerjee2011} Banerjee, A. V., Kumar, S., Pande, R., and Su, F. (2011). Do Informed Voters Make Better Choices? Experimental Evidence from Urban India. Unpublished manuscript.",
        ],
        target_pages=55,
        qa=[
            {"question": "What is the main identification strategy?", "answer": "Random audit lottery combined with quasi-random timing of audit disclosure relative to elections"},
            {"question": "What is the main effect of audit disclosure on incumbent vote share?", "answer": "-4.1 percentage points (ITT)"},
            {"question": "How does media amplify the accountability effect?", "answer": "The triple interaction of disclosure, corruption, and radio presence adds -5.8 percentage points"},
            {"question": "Does disclosure reduce future corruption?", "answer": "Yes, by 2.8 percentage points in subsequent audits"},
            {"question": "How many municipalities are in the sample?", "answer": "1,891 audited municipalities, 1,456 with incumbent re-election data"},
        ],
    )


PAPER_BUILDERS["10"] = _paper_10_political_economy
