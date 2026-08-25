#!/usr/bin/env python3
"""Paper builder for paper 16 (Micro Theory)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table, render_math_table,
    PAPER_BUILDERS,
)


def _paper_16_micro_theory() -> PaperSpec:
    # Use render_math_table for ALL tables (theory paper, no regression tables)
    # Heavy math: 10 main equations, ~50 lines appendix proofs

    # --- Tables ---

    # Table 1: mechanism_comparison
    mechanism_comparison = render_math_table({
        "table_id": "mechanism-comparison",
        "caption": "Comparison of Standard Auction Formats",
        "label": "tab:mechanism-comparison",
        "col_headers": [
            {"text": "Format", "latex": r"\textbf{Format}"},
            {"text": "Revenue Formula", "latex": r"\textbf{Revenue Formula}"},
            {"text": "Bidder Surplus", "latex": r"\textbf{Bidder Surplus}"},
            {"text": "Efficient?", "latex": r"\textbf{Efficient?}"},
        ],
        "rows": [
            {
                "label": "First-price sealed-bid",
                "label_latex": r"\text{First-price sealed-bid}",
                "cells": [
                    {"text": "First-price sealed-bid", "latex": r"\text{First-price sealed-bid (FPA)}"},
                    {"text": "E[second-order stat]", "latex": r"E\!\left[v_{(1)}\left(1 - \frac{F(v_{(1)})}{f(v_{(1)})}\right)\right]"},
                    {"text": "Zero (shading)", "latex": r"0 \text{ (equilibrium bid shading)}"},
                    {"text": "Yes (symmetric IPV)", "latex": r"\checkmark \text{ (symmetric IPV)}"},
                ],
            },
            {
                "label": "Second-price sealed-bid",
                "label_latex": r"\text{Second-price sealed-bid}",
                "cells": [
                    {"text": "Second-price sealed-bid", "latex": r"\text{Second-price sealed-bid (SPA)}"},
                    {"text": "E[second-order stat]", "latex": r"E[v_{(2)}]"},
                    {"text": "E[v_(1) - v_(2)]", "latex": r"E[v_{(1)} - v_{(2)}]"},
                    {"text": "Yes (dominant strategy)", "latex": r"\checkmark \text{ (dominant strategy)}"},
                ],
            },
            {
                "label": "English ascending",
                "label_latex": r"\text{English ascending}",
                "cells": [
                    {"text": "English ascending (oral)", "latex": r"\text{English ascending (oral)}"},
                    {"text": "E[v_(2)]", "latex": r"E[v_{(2)}]"},
                    {"text": "E[v_(1) - v_(2)]", "latex": r"E[v_{(1)} - v_{(2)}]"},
                    {"text": "Yes", "latex": r"\checkmark"},
                ],
            },
            {
                "label": "Dutch descending",
                "label_latex": r"\text{Dutch descending}",
                "cells": [
                    {"text": "Dutch descending (oral)", "latex": r"\text{Dutch descending (oral)}"},
                    {"text": "Same as FPA", "latex": r"E\!\left[v_{(1)}\!\left(1 - \frac{F(v_{(1)})}{f(v_{(1)})}\right)\right]"},
                    {"text": "Zero (bid shading)", "latex": r"0 \text{ (bid shading)}"},
                    {"text": "Yes (symmetric IPV)", "latex": r"\checkmark \text{ (symmetric IPV)}"},
                ],
            },
            {
                "label": "All-pay",
                "label_latex": r"\text{All-pay}",
                "cells": [
                    {"text": "All-pay auction", "latex": r"\text{All-pay auction}"},
                    {"text": "N * E[b_i(v)]", "latex": r"n \cdot E[b_i(v_i)]"},
                    {"text": "E[v_(1)] - n*E[b]", "latex": r"E[v_{(1)}] - n \cdot E[b_i(v_i)]"},
                    {"text": "Yes (symmetric IPV)", "latex": r"\checkmark \text{ (symmetric IPV)}"},
                ],
            },
        ],
        "notes": r"IPV = Independent Private Values. $v_{(k)}$ denotes the $k$-th order statistic of valuations. Revenue Equivalence Theorem implies FPA, SPA, English, Dutch, and all-pay auctions yield the same expected revenue under symmetric IPV with risk-neutral bidders.",
        "qa": [
            {"question": "Which auction formats are strategically equivalent under symmetric IPV?", "answer": "First-price sealed-bid and Dutch descending auction are strategically equivalent (both involve bid shading)"},
            {"question": "Which formats are efficient under symmetric IPV?", "answer": "All five formats — FPA, SPA, English, Dutch, and all-pay — are allocatively efficient under symmetric IPV with risk-neutral bidders"},
            {"question": "What is the bidder surplus in a second-price auction?", "answer": r"E[v_{(1)} - v_{(2)}], the expected gap between highest and second-highest valuation"},
            {"question": "What does the Revenue Equivalence Theorem state?", "answer": "All standard auction formats yield the same expected seller revenue under symmetric IPV with risk-neutral bidders"},
        ],
    })

    # Table 2: numerical_uniform
    numerical_uniform = render_math_table({
        "table_id": "numerical-uniform",
        "caption": r"Optimal Reserve Price: Numerical Results for $F \sim \mathrm{Uniform}[0,1]$, $n=2$ Bidders",
        "label": "tab:numerical-uniform",
        "col_headers": [
            {"text": "Reserve Price r", "latex": r"r"},
            {"text": "Expected Revenue", "latex": r"E[\text{Rev}(r)]"},
            {"text": "Probability of Sale", "latex": r"\Pr(\text{sale})"},
        ],
        "rows": [
            {
                "label": "r = 0",
                "label_latex": r"r = 0",
                "cells": [
                    {"text": "r = 0", "latex": r"0"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "1", "latex": r"1.000"},
                ],
            },
            {
                "label": "r = 0.1",
                "label_latex": r"r = 0.1",
                "cells": [
                    {"text": "r = 0.1", "latex": r"0.1"},
                    {"text": "0.3484", "latex": r"0.3484"},
                    {"text": "0.9900", "latex": r"0.9900"},
                ],
            },
            {
                "label": "r = 0.25",
                "label_latex": r"r = 0.25",
                "cells": [
                    {"text": "r = 0.25", "latex": r"0.25"},
                    {"text": "0.3750", "latex": r"0.3750"},
                    {"text": "0.9375", "latex": r"0.9375"},
                ],
            },
            {
                "label": "r = 0.5 (optimal)",
                "label_latex": r"r = r^* = 0.5",
                "cells": [
                    {"text": "r = 0.5 (optimal)", "latex": r"r^* = 0.5"},
                    {"text": "5/12 = 0.4167", "latex": r"\tfrac{5}{12} \approx 0.4167"},
                    {"text": "0.7500", "latex": r"0.7500"},
                ],
            },
            {
                "label": "r = 0.75",
                "label_latex": r"r = 0.75",
                "cells": [
                    {"text": "r = 0.75", "latex": r"0.75"},
                    {"text": "0.3750", "latex": r"0.3750"},
                    {"text": "0.4375", "latex": r"0.4375"},
                ],
            },
            {
                "label": "r = 1.0",
                "label_latex": r"r = 1.0",
                "cells": [
                    {"text": "r = 1.0", "latex": r"1.0"},
                    {"text": "0", "latex": r"0.0000"},
                    {"text": "0", "latex": r"0.0000"},
                ],
            },
        ],
        "notes": r"Expected revenue computed as $E[\text{Rev}(r)] = 2\int_r^1 \int_r^{v_1} v_2 \,dv_2\,dv_1 + r \cdot \Pr(v_{(1)} \geq r > v_{(2)}) + r \cdot \Pr(v_{(1)} \geq r, v_{(2)} \geq r)$. Optimal reserve $r^* = 1/2$ from $\varphi(r^*) = 0$ where $\varphi(v) = 2v - 1$.",
        "qa": [
            {"question": "What is the optimal reserve price for Uniform[0,1] with 2 bidders?", "answer": "r* = 0.5"},
            {"question": "What is the expected revenue at the optimal reserve r*=0.5?", "answer": "5/12 ≈ 0.4167"},
            {"question": "What is the probability of sale at the optimal reserve r*=0.5?", "answer": "0.75"},
            {"question": "What is the expected revenue with no reserve (r=0)?", "answer": "1/3 ≈ 0.333"},
        ],
    })

    # Table 3: numerical_exponential
    numerical_exponential = render_math_table({
        "table_id": "numerical-exponential",
        "caption": r"Optimal Reserve Price: Numerical Results for $F \sim \mathrm{Exp}(1)$, $n=2$ Bidders",
        "label": "tab:numerical-exponential",
        "col_headers": [
            {"text": "Reserve Price r", "latex": r"r"},
            {"text": "Expected Revenue", "latex": r"E[\text{Rev}(r)]"},
            {"text": "Probability of Sale", "latex": r"\Pr(\text{sale})"},
        ],
        "rows": [
            {
                "label": "r = 0",
                "label_latex": r"r = 0",
                "cells": [
                    {"text": "r = 0", "latex": r"0"},
                    {"text": "1/2 = 0.500", "latex": r"\tfrac{1}{2} = 0.500"},
                    {"text": "1.000", "latex": r"1.000"},
                ],
            },
            {
                "label": "r = 0.5",
                "label_latex": r"r = 0.5",
                "cells": [
                    {"text": "r = 0.5", "latex": r"0.5"},
                    {"text": "0.5352", "latex": r"0.5352"},
                    {"text": "0.9394", "latex": r"0.9394"},
                ],
            },
            {
                "label": "r = 1.0 (optimal)",
                "label_latex": r"r = r^* = 1.0",
                "cells": [
                    {"text": "r = 1.0 (optimal)", "latex": r"r^* = 1.0"},
                    {"text": "0.5413", "latex": r"0.5413"},
                    {"text": "0.8647", "latex": r"0.8647"},
                ],
            },
            {
                "label": "r = 1.5",
                "label_latex": r"r = 1.5",
                "cells": [
                    {"text": "r = 1.5", "latex": r"1.5"},
                    {"text": "0.5165", "latex": r"0.5165"},
                    {"text": "0.7769", "latex": r"0.7769"},
                ],
            },
            {
                "label": "r = 2.0",
                "label_latex": r"r = 2.0",
                "cells": [
                    {"text": "r = 2.0", "latex": r"2.0"},
                    {"text": "0.4672", "latex": r"0.4672"},
                    {"text": "0.6767", "latex": r"0.6767"},
                ],
            },
            {
                "label": "r = 3.0",
                "label_latex": r"r = 3.0",
                "cells": [
                    {"text": "r = 3.0", "latex": r"3.0"},
                    {"text": "0.3233", "latex": r"0.3233"},
                    {"text": "0.5034", "latex": r"0.5034"},
                ],
            },
        ],
        "notes": r"For $F(v) = 1 - e^{-v}$ (Exp(1)), virtual valuation is $\varphi(v) = v - 1$. Optimal reserve satisfies $\varphi(r^*) = 0 \Rightarrow r^* = 1$. Expected revenue $E[\text{Rev}(r)] = 2\int_r^\infty \int_r^{v_1} v_2 e^{-v_2} e^{-v_1}\,dv_2\,dv_1 + r \cdot [e^{-r} - e^{-2r}] + r \cdot e^{-2r}$.",
        "qa": [
            {"question": "What is the optimal reserve price for Exp(1) with 2 bidders?", "answer": "r* = 1.0"},
            {"question": "What is the virtual valuation function for Exp(1)?", "answer": "phi(v) = v - 1"},
            {"question": "What is the expected revenue at the optimal reserve for Exp(1)?", "answer": "0.5413"},
            {"question": "What is the probability of sale at the optimal reserve for Exp(1)?", "answer": "0.8647"},
        ],
    })

    # Table 4: revenue_comparison
    revenue_comparison = render_math_table({
        "table_id": "revenue-comparison",
        "caption": r"Revenue Comparison Across Auction Formats: $F \sim \mathrm{Uniform}[0,1]$",
        "label": "tab:revenue-comparison",
        "col_headers": [
            {"text": "N bidders", "latex": r"n"},
            {"text": "FPA Revenue", "latex": r"E[\text{Rev}^{\text{FPA}}]"},
            {"text": "SPA Revenue", "latex": r"E[\text{Rev}^{\text{SPA}}]"},
            {"text": "All-pay Revenue", "latex": r"E[\text{Rev}^{\text{AP}}]"},
            {"text": "Optimal Revenue", "latex": r"E[\text{Rev}^{*}]"},
        ],
        "rows": [
            {
                "label": "N = 2",
                "label_latex": r"n = 2",
                "cells": [
                    {"text": "N = 2", "latex": r"2"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "5/12", "latex": r"\tfrac{5}{12} \approx 0.417"},
                ],
            },
            {
                "label": "N = 3",
                "label_latex": r"n = 3",
                "cells": [
                    {"text": "N = 3", "latex": r"3"},
                    {"text": "1/2", "latex": r"\tfrac{1}{2} = 0.500"},
                    {"text": "1/2", "latex": r"\tfrac{1}{2} = 0.500"},
                    {"text": "1/2", "latex": r"\tfrac{1}{2} = 0.500"},
                    {"text": "0.531", "latex": r"0.531"},
                ],
            },
            {
                "label": "N = 5",
                "label_latex": r"n = 5",
                "cells": [
                    {"text": "N = 5", "latex": r"5"},
                    {"text": "2/3", "latex": r"\tfrac{2}{3} \approx 0.667"},
                    {"text": "2/3", "latex": r"\tfrac{2}{3} \approx 0.667"},
                    {"text": "2/3", "latex": r"\tfrac{2}{3} \approx 0.667"},
                    {"text": "0.679", "latex": r"0.679"},
                ],
            },
            {
                "label": "N = 10",
                "label_latex": r"n = 10",
                "cells": [
                    {"text": "N = 10", "latex": r"10"},
                    {"text": "10/11", "latex": r"\tfrac{10}{11} \approx 0.833"},
                    {"text": "10/11", "latex": r"\tfrac{10}{11} \approx 0.833"},
                    {"text": "10/11", "latex": r"\tfrac{10}{11} \approx 0.833"},
                    {"text": "0.838", "latex": r"0.838"},
                ],
            },
            {
                "label": "N = 20",
                "label_latex": r"n = 20",
                "cells": [
                    {"text": "N = 20", "latex": r"20"},
                    {"text": "20/21", "latex": r"\tfrac{20}{21} \approx 0.905"},
                    {"text": "20/21", "latex": r"\tfrac{20}{21} \approx 0.905"},
                    {"text": "20/21", "latex": r"\tfrac{20}{21} \approx 0.905"},
                    {"text": "0.908", "latex": r"0.908"},
                ],
            },
        ],
        "notes": r"Under Revenue Equivalence, FPA, SPA, and all-pay yield identical expected revenue $E[\text{Rev}] = \tfrac{n-1}{n+1}$ for Uniform[0,1]. Optimal revenue computed with reserve $r^* = 1/2$; gain over no-reserve decreases as $n \to \infty$. Closed form: $E[\text{Rev}^{\text{SPA}}] = E[v_{(2)}] = \tfrac{n-1}{n+1}$.",
        "qa": [
            {"question": "What is the expected revenue for 2 bidders under FPA with Uniform[0,1]?", "answer": "1/3 ≈ 0.333"},
            {"question": "Does the Revenue Equivalence Theorem hold across FPA, SPA, and all-pay here?", "answer": "Yes, all three yield identical expected revenue 1/3 for n=2 bidders"},
            {"question": "What is the optimal revenue for n=2 bidders?", "answer": "5/12 ≈ 0.417"},
            {"question": "What happens to the gap between optimal and symmetric auction revenue as n grows?", "answer": "The gap shrinks toward zero as competition increases"},
        ],
    })

    # Table 5: optimal_vs_efficient
    optimal_vs_efficient = render_math_table({
        "table_id": "optimal-vs-efficient",
        "caption": "Optimal versus Efficient Mechanisms: Allocation, Payment, and Welfare",
        "label": "tab:optimal-vs-efficient",
        "col_headers": [
            {"text": "Mechanism", "latex": r"\textbf{Mechanism}"},
            {"text": "Allocation Rule", "latex": r"\textbf{Allocation Rule } q^*(v)"},
            {"text": "Payment Rule", "latex": r"\textbf{Payment Rule } t^*(v)"},
            {"text": "Revenue", "latex": r"\textbf{Revenue}"},
            {"text": "Efficiency Loss", "latex": r"\textbf{Efficiency Loss}"},
        ],
        "rows": [
            {
                "label": "Efficient (VCG)",
                "label_latex": r"\text{VCG}",
                "cells": [
                    {"text": "Efficient / VCG", "latex": r"\text{Efficient (VCG)}"},
                    {"text": "Award to highest v_i", "latex": r"q_i^{\text{VCG}}(v) = \mathbf{1}[v_i = \max_j v_j]"},
                    {"text": "max_{j != i} v_j", "latex": r"t_i^{\text{VCG}}(v) = \max_{j \neq i} v_j \cdot q_i^{\text{VCG}}(v)"},
                    {"text": "E[v_(2)]", "latex": r"E[v_{(2)}]"},
                    {"text": "0", "latex": r"0"},
                ],
            },
            {
                "label": "Optimal (Myerson)",
                "label_latex": r"\text{Myerson}",
                "cells": [
                    {"text": "Optimal (Myerson)", "latex": r"\text{Optimal (Myerson)}"},
                    {"text": "Award to highest phi(v_i) >= 0", "latex": r"q_i^*(v) = \mathbf{1}[\varphi(v_i) = \max_j \varphi(v_j) \geq 0]"},
                    {"text": "Myerson payment rule", "latex": r"t_i^*(v) = v_i q_i^*(v) - \int_{\underline{v}}^{v_i} q_i^*(s, v_{-i})\,ds"},
                    {"text": "E[phi(v_(1)) 1[phi>=0]]", "latex": r"E[\varphi(v_{(1)}) \cdot \mathbf{1}[\varphi(v_{(1)}) \geq 0]]"},
                    {"text": "DWL > 0 when r* > 0", "latex": r"\mathrm{DWL} > 0 \text{ iff } r^* > 0"},
                ],
            },
            {
                "label": "Posted Price",
                "label_latex": r"\text{Posted Price}",
                "cells": [
                    {"text": "Posted price p", "latex": r"\text{Posted price } p"},
                    {"text": "Award if v_i >= p", "latex": r"q_i^{pp}(v) = \mathbf{1}[v_i \geq p]"},
                    {"text": "p * 1[v_i >= p]", "latex": r"t_i^{pp}(v) = p \cdot \mathbf{1}[v_i \geq p]"},
                    {"text": "p * (1-F(p))", "latex": r"p \cdot [1 - F(p)]"},
                    {"text": "E[(v-p) 1[v in [r*,p]]]", "latex": r"E[(v - p) \cdot \mathbf{1}[v \in [r^*, p]]]"},
                ],
            },
        ],
        "notes": r"$\varphi(v) = v - \tfrac{1-F(v)}{f(v)}$ is the virtual valuation. VCG is allocatively efficient but may yield less revenue than Myerson's optimal mechanism. Posted price mechanism is optimal among posted-price mechanisms but generally dominated by Myerson auction.",
        "qa": [
            {"question": "What is the allocation rule in the Myerson optimal mechanism?", "answer": "Award the object to bidder i with the highest non-negative virtual valuation"},
            {"question": "What is the efficiency loss in the VCG mechanism?", "answer": "Zero — VCG is allocatively efficient"},
            {"question": "When does the Myerson mechanism have positive deadweight loss?", "answer": "Whenever the optimal reserve price r* > 0, because some high-valuation trades are excluded"},
            {"question": "What is the payment in a VCG mechanism for bidder i?", "answer": "The maximum valuation among all other bidders, paid only if i wins"},
        ],
    })

    # Table 6: welfare_decomposition
    welfare_decomposition = render_math_table({
        "table_id": "welfare-decomposition",
        "caption": "Welfare Decomposition: Total Surplus, Revenue, and Deadweight Loss",
        "label": "tab:welfare-decomposition",
        "col_headers": [
            {"text": "Component", "latex": r"\textbf{Component}"},
            {"text": "Formula", "latex": r"\textbf{Formula}"},
            {"text": "Value (Uniform[0,1])", "latex": r"\textbf{Uniform}[0,1]"},
            {"text": "Value (Exp(1))", "latex": r"\textbf{Exp}(1)"},
        ],
        "rows": [
            {
                "label": "Total surplus (efficient)",
                "label_latex": r"W^{\text{eff}}",
                "cells": [
                    {"text": "Total surplus (efficient)", "latex": r"W^{\text{eff}} = E[v_{(n)}]"},
                    {"text": "E[v_(n)] = n/(n+1)", "latex": r"E[v_{(n)}] = \tfrac{n}{n+1}"},
                    {"text": "2/3 (n=2)", "latex": r"\tfrac{2}{3} \approx 0.667 \;\; (n=2)"},
                    {"text": "3/2 (n=2)", "latex": r"\tfrac{3}{2} = 1.500 \;\; (n=2)"},
                ],
            },
            {
                "label": "Seller revenue (optimal)",
                "label_latex": r"R^*",
                "cells": [
                    {"text": "Seller revenue (Myerson)", "latex": r"R^* = E[\varphi(v_{(1)}) \cdot \mathbf{1}[\varphi(v_{(1)}) \geq 0]]"},
                    {"text": "E[phi(v_(1)) 1[phi>=0]]", "latex": r"R^* = \int_{r^*}^{\bar{v}} \varphi(v) \,n f(v) F(v)^{n-1}\,dv"},
                    {"text": "5/12 (n=2)", "latex": r"\tfrac{5}{12} \approx 0.417 \;\; (n=2)"},
                    {"text": "0.541 (n=2)", "latex": r"0.541 \;\; (n=2)"},
                ],
            },
            {
                "label": "Bidder surplus",
                "label_latex": r"CS",
                "cells": [
                    {"text": "Bidder (consumer) surplus", "latex": r"CS = W^{\text{opt}} - R^*"},
                    {"text": "W* - R*", "latex": r"CS = E\!\left[\sum_i (v_i - t_i^*) q_i^*(v)\right] - R^*"},
                    {"text": "0.125 (n=2)", "latex": r"0.125 \;\; (n=2)"},
                    {"text": "0.229 (n=2)", "latex": r"0.229 \;\; (n=2)"},
                ],
            },
            {
                "label": "Deadweight loss",
                "label_latex": r"\mathrm{DWL}",
                "cells": [
                    {"text": "Deadweight loss", "latex": r"\mathrm{DWL} = W^{\text{eff}} - W^{\text{opt}}"},
                    {"text": "W^eff - W^opt", "latex": r"\mathrm{DWL} = \int_{0}^{r^*} v \,n f(v) F(v)^{n-1}\,dv"},
                    {"text": "0.125 (n=2)", "latex": r"0.125 \;\; (n=2)"},
                    {"text": "0.730 (n=2)", "latex": r"0.730 \;\; (n=2)"},
                ],
            },
        ],
        "notes": r"$W^{\text{opt}} = R^* + CS$ is total surplus under the Myerson optimal mechanism. $\mathrm{DWL} = W^{\text{eff}} - W^{\text{opt}} \geq 0$ with equality iff $r^* = \underline{v}$. For Uniform[0,1] with $n=2$: $W^{\text{eff}} = 2/3$, $R^* = 5/12$, $CS = 1/8$, $\mathrm{DWL} = 1/8$. Identity: $W^{\text{eff}} = R^* + CS + \mathrm{DWL}$.",
        "qa": [
            {"question": "What is the total efficient surplus for Uniform[0,1] with n=2 bidders?", "answer": "2/3 ≈ 0.667"},
            {"question": "What is the deadweight loss for Uniform[0,1] with n=2 bidders under the Myerson mechanism?", "answer": "1/8 = 0.125"},
            {"question": "What is the identity relating welfare components?", "answer": "W^eff = R* + CS + DWL"},
            {"question": "When is deadweight loss zero in the optimal mechanism?", "answer": "When the optimal reserve r* equals the lowest possible valuation, so no trades are excluded"},
        ],
    })

    # Table 7: bidder_surplus_by_mechanism
    bidder_surplus_by_mechanism = render_math_table({
        "table_id": "bidder-surplus-by-mechanism",
        "caption": r"Bidder Surplus by Mechanism: $F \sim \mathrm{Uniform}[0,1]$, $n = 2$ Bidders",
        "label": "tab:bidder-surplus-by-mechanism",
        "col_headers": [
            {"text": "Mechanism", "latex": r"\textbf{Mechanism}"},
            {"text": "Winner Surplus", "latex": r"\textbf{Winner Surplus}"},
            {"text": "Loser Surplus", "latex": r"\textbf{Loser Surplus}"},
            {"text": "Total Bidder Surplus", "latex": r"\textbf{Total Bidder Surplus}"},
            {"text": "Seller Revenue", "latex": r"\textbf{Seller Revenue}"},
        ],
        "rows": [
            {
                "label": "Second-price (no reserve)",
                "label_latex": r"\text{SPA } (r=0)",
                "cells": [
                    {"text": "SPA (no reserve)", "latex": r"\text{SPA } (r=0)"},
                    {"text": "E[v_(1) - v_(2)] = 1/3", "latex": r"E[v_{(1)} - v_{(2)}] = \tfrac{1}{3}"},
                    {"text": "0", "latex": r"0"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                ],
            },
            {
                "label": "Second-price (r* = 0.5)",
                "label_latex": r"\text{SPA } (r^*=0.5)",
                "cells": [
                    {"text": "SPA (r* = 0.5)", "latex": r"\text{SPA } (r^*=\tfrac{1}{2})"},
                    {"text": "1/8", "latex": r"\tfrac{1}{8} = 0.125"},
                    {"text": "0", "latex": r"0"},
                    {"text": "1/8", "latex": r"\tfrac{1}{8} = 0.125"},
                    {"text": "5/12", "latex": r"\tfrac{5}{12} \approx 0.417"},
                ],
            },
            {
                "label": "First-price (no reserve)",
                "label_latex": r"\text{FPA } (r=0)",
                "cells": [
                    {"text": "FPA (no reserve)", "latex": r"\text{FPA } (r=0)"},
                    {"text": "E[v_(1) - b_(1)] = 1/3", "latex": r"E[v_{(1)} - b_{(1)}] = \tfrac{1}{3}"},
                    {"text": "0", "latex": r"0"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                ],
            },
            {
                "label": "All-pay (no reserve)",
                "label_latex": r"\text{All-pay } (r=0)",
                "cells": [
                    {"text": "All-pay (no reserve)", "latex": r"\text{All-pay } (r=0)"},
                    {"text": "v_(1) - b_(1)", "latex": r"E[v_{(1)} - b_{(1)}(v_{(1)})]"},
                    {"text": "-b_(2)", "latex": r"-E[b_{(2)}(v_{(2)})]"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                    {"text": "1/3", "latex": r"\tfrac{1}{3} \approx 0.333"},
                ],
            },
            {
                "label": "Posted price (p = 0.5)",
                "label_latex": r"\text{Posted } (p=0.5)",
                "cells": [
                    {"text": "Posted price (p = 0.5)", "latex": r"\text{Posted price } (p=0.5)"},
                    {"text": "E[v - 0.5 | v >= 0.5]", "latex": r"E[v - p \mid v \geq p] \cdot \Pr(v \geq p) = \tfrac{1}{8}"},
                    {"text": "0", "latex": r"0"},
                    {"text": "1/8", "latex": r"\tfrac{1}{8} = 0.125"},
                    {"text": "1/4", "latex": r"\tfrac{1}{4} = 0.250"},
                ],
            },
        ],
        "notes": r"Uniform[0,1] with $n=2$ independent bidders. Total surplus $= $ bidder surplus $+$ seller revenue. Under Revenue Equivalence, FPA, SPA, and all-pay yield identical total bidder surplus $\tfrac{1}{3}$ (no reserve). The optimal reserve $r^*=\tfrac{1}{2}$ transfers surplus from bidders to seller.",
        "qa": [
            {"question": "What is the total bidder surplus in a second-price auction with no reserve?", "answer": "1/3 ≈ 0.333"},
            {"question": "How does the optimal reserve affect bidder surplus?", "answer": "It reduces total bidder surplus from 1/3 to 1/8, transferring surplus to the seller"},
            {"question": "What is seller revenue under a posted price of p=0.5 with a single buyer?", "answer": "1/4 = 0.250"},
        ],
    })

    # Table 8: optimal_reserve_distributions
    optimal_reserve_distributions = render_math_table({
        "table_id": "optimal-reserve-distributions",
        "caption": "Optimal Reserve Price Under Different Valuation Distributions",
        "label": "tab:optimal-reserve-distributions",
        "col_headers": [
            {"text": "Distribution", "latex": r"\textbf{Distribution } F"},
            {"text": "Virtual Valuation", "latex": r"\boldsymbol{\varphi(v)}"},
            {"text": "Optimal Reserve r*", "latex": r"\boldsymbol{r^*}"},
            {"text": "Revenue (n=2)", "latex": r"\textbf{Rev}^*(n\!=\!2)"},
            {"text": "Regular?", "latex": r"\textbf{Regular?}"},
        ],
        "rows": [
            {
                "label": "Uniform[0,1]",
                "label_latex": r"\text{Uniform}[0,1]",
                "cells": [
                    {"text": "Uniform[0,1]", "latex": r"\text{Uniform}[0,1]"},
                    {"text": "2v - 1", "latex": r"2v - 1"},
                    {"text": "1/2", "latex": r"\tfrac{1}{2}"},
                    {"text": "5/12", "latex": r"\tfrac{5}{12} \approx 0.417"},
                    {"text": "Yes", "latex": r"\checkmark"},
                ],
            },
            {
                "label": "Exponential(1)",
                "label_latex": r"\text{Exp}(1)",
                "cells": [
                    {"text": "Exp(1)", "latex": r"\text{Exp}(1)"},
                    {"text": "v - 1", "latex": r"v - 1"},
                    {"text": "1", "latex": r"1"},
                    {"text": "0.541", "latex": r"0.541"},
                    {"text": "Yes", "latex": r"\checkmark"},
                ],
            },
            {
                "label": "Uniform[0, a]",
                "label_latex": r"\text{Uniform}[0,a]",
                "cells": [
                    {"text": "Uniform[0,a]", "latex": r"\text{Uniform}[0,a]"},
                    {"text": "2v - a", "latex": r"2v - a"},
                    {"text": "a/2", "latex": r"\tfrac{a}{2}"},
                    {"text": "5a/12", "latex": r"\tfrac{5a}{12}"},
                    {"text": "Yes", "latex": r"\checkmark"},
                ],
            },
            {
                "label": "Power law v^alpha, alpha > 0",
                "label_latex": r"F(v) = v^{\alpha}",
                "cells": [
                    {"text": "Power: F(v) = v^alpha", "latex": r"F(v) = v^{\alpha} \text{ on } [0,1]"},
                    {"text": "v - v/(alpha)", "latex": r"v\!\left(1 + \tfrac{1}{\alpha}\right) - \tfrac{1}{\alpha}"},
                    {"text": "1/(alpha + 1)", "latex": r"\tfrac{1}{\alpha + 1}"},
                    {"text": "(depends on alpha)", "latex": r"\text{(closed form)}"},
                    {"text": "Yes (alpha >= 1)", "latex": r"\checkmark \; (\alpha \geq 1)"},
                ],
            },
            {
                "label": "Log-normal(0, sigma^2)",
                "label_latex": r"\text{LogN}(0, \sigma^2)",
                "cells": [
                    {"text": "LogNormal(0, sigma^2)", "latex": r"\text{LogN}(0, \sigma^2)"},
                    {"text": "(no closed form)", "latex": r"v - \tfrac{1 - \Phi(\tfrac{\ln v}{\sigma})}{\tfrac{1}{\sigma v}\phi(\tfrac{\ln v}{\sigma})}"},
                    {"text": "(numerical)", "latex": r"\text{numerical}"},
                    {"text": "(numerical)", "latex": r"\text{numerical}"},
                    {"text": "Yes", "latex": r"\checkmark"},
                ],
            },
            {
                "label": "Pareto(1, alpha)",
                "label_latex": r"\text{Pareto}(1, \alpha)",
                "cells": [
                    {"text": "Pareto(1, alpha)", "latex": r"\text{Pareto}(1, \alpha),\; v \geq 1"},
                    {"text": "v - v/alpha", "latex": r"v\!\left(1 - \tfrac{1}{\alpha}\right)"},
                    {"text": "alpha/(alpha-1)", "latex": r"\tfrac{\alpha}{\alpha - 1}"},
                    {"text": "(depends on alpha)", "latex": r"\text{(closed form)}"},
                    {"text": "Yes (alpha > 1)", "latex": r"\checkmark \; (\alpha > 1)"},
                ],
            },
        ],
        "notes": r"$\varphi(v) = v - [1-F(v)]/f(v)$ is the Myerson virtual valuation. Optimal reserve $r^*$ solves $\varphi(r^*)=0$. A distribution is \emph{regular} if $\varphi(v)$ is non-decreasing. For irregular distributions, ironing is required. The Pareto distribution requires $\alpha > 1$ for finite mean; $r^* = \alpha/(\alpha-1) > 1$.",
        "qa": [
            {"question": "What is the virtual valuation for the Exponential(1) distribution?", "answer": "phi(v) = v - 1"},
            {"question": "What is the optimal reserve for Uniform[0,a]?", "answer": "r* = a/2"},
            {"question": "Is the power-law distribution F(v) = v^alpha regular for all alpha?", "answer": "It is regular for alpha >= 1; for alpha < 1 it may fail the monotonicity condition"},
            {"question": "What is the optimal reserve for Pareto(1, alpha)?", "answer": "r* = alpha/(alpha - 1)"},
        ],
    })

    # Table 9: correlated_vs_ipv_revenue
    correlated_vs_ipv_revenue = render_math_table({
        "table_id": "correlated-vs-ipv-revenue",
        "caption": "Revenue in Correlated vs. Independent Private Values: Numerical Comparison",
        "label": "tab:correlated-vs-ipv-revenue",
        "col_headers": [
            {"text": "Setting", "latex": r"\textbf{Setting}"},
            {"text": "N bidders", "latex": r"n"},
            {"text": "IPV Revenue", "latex": r"\textbf{IPV Revenue}"},
            {"text": "CPV Revenue (Cremer-McLean)", "latex": r"\textbf{CPV Revenue}"},
            {"text": "Full surplus extraction?", "latex": r"\textbf{Full Extraction?}"},
        ],
        "rows": [
            {
                "label": "Uniform, independent",
                "label_latex": r"\text{Uniform, indep.}",
                "cells": [
                    {"text": "Uniform, independent", "latex": r"\text{Uniform}[0,1],\;\text{indep.}"},
                    {"text": "2", "latex": r"2"},
                    {"text": "5/12", "latex": r"\tfrac{5}{12} \approx 0.417"},
                    {"text": "5/12", "latex": r"\tfrac{5}{12} \approx 0.417"},
                    {"text": "No (IPV = CPV here)", "latex": r"\text{No (indep.)}"},
                ],
            },
            {
                "label": "Uniform, rho = 0.3",
                "label_latex": r"\text{Uniform, } \rho\!=\!0.3",
                "cells": [
                    {"text": "Uniform, rho = 0.3", "latex": r"\text{Uniform}[0,1],\;\rho = 0.3"},
                    {"text": "2", "latex": r"2"},
                    {"text": "0.417 (benchmark)", "latex": r"0.417 \text{ (IPV benchmark)}"},
                    {"text": "0.528", "latex": r"0.528"},
                    {"text": "Partial", "latex": r"\text{Partial}"},
                ],
            },
            {
                "label": "Uniform, rho = 0.7",
                "label_latex": r"\text{Uniform, } \rho\!=\!0.7",
                "cells": [
                    {"text": "Uniform, rho = 0.7", "latex": r"\text{Uniform}[0,1],\;\rho = 0.7"},
                    {"text": "2", "latex": r"2"},
                    {"text": "0.417 (benchmark)", "latex": r"0.417 \text{ (IPV benchmark)}"},
                    {"text": "0.614", "latex": r"0.614"},
                    {"text": "Near-full", "latex": r"\text{Near-full}"},
                ],
            },
            {
                "label": "Uniform, rho = 1.0 (common value)",
                "label_latex": r"\text{Uniform, } \rho\!=\!1",
                "cells": [
                    {"text": "Uniform, rho = 1 (common value)", "latex": r"\text{Uniform}[0,1],\;\rho = 1"},
                    {"text": "2", "latex": r"2"},
                    {"text": "N/A", "latex": r"\text{N/A}"},
                    {"text": "2/3 = W^eff", "latex": r"\tfrac{2}{3} = W^{\text{eff}}"},
                    {"text": "Yes (full extraction)", "latex": r"\checkmark \text{ (full)}"},
                ],
            },
            {
                "label": "Uniform, independent, n=5",
                "label_latex": r"\text{Uniform, indep., } n\!=\!5",
                "cells": [
                    {"text": "Uniform, independent, n=5", "latex": r"\text{Uniform}[0,1],\;\text{indep.}"},
                    {"text": "5", "latex": r"5"},
                    {"text": "0.679", "latex": r"0.679"},
                    {"text": "0.679", "latex": r"0.679"},
                    {"text": "No (IPV = CPV here)", "latex": r"\text{No (indep.)}"},
                ],
            },
            {
                "label": "Uniform, rho = 0.5, n=5",
                "label_latex": r"\text{Uniform, } \rho\!=\!0.5,\; n\!=\!5",
                "cells": [
                    {"text": "Uniform, rho=0.5, n=5", "latex": r"\text{Uniform}[0,1],\;\rho = 0.5"},
                    {"text": "5", "latex": r"5"},
                    {"text": "0.679 (benchmark)", "latex": r"0.679 \text{ (IPV benchmark)}"},
                    {"text": "0.798", "latex": r"0.798"},
                    {"text": "Partial", "latex": r"\text{Partial}"},
                ],
            },
        ],
        "notes": r"IPV Revenue: Myerson optimal mechanism assuming independent private values. CPV Revenue: optimal mechanism under correlated private values following Cr\'{e}mer and McLean (1988). $\rho$ denotes the correlation coefficient between bidder valuations drawn from a joint distribution with Uniform$[0,1]$ marginals. Full surplus extraction is feasible when signals are sufficiently correlated and the seller can condition payments on all reports.",
        "qa": [
            {"question": "What is the CPV revenue with rho=0.7 and n=2 bidders?", "answer": "0.614"},
            {"question": "Can the seller extract full surplus under perfect correlation (rho=1)?", "answer": "Yes, the seller can extract the full efficient surplus of 2/3"},
            {"question": "Does correlation help the seller when valuations are independent?", "answer": "No, when rho=0 (independent), CPV and IPV revenues are identical"},
            {"question": "What is the CPV revenue gain over IPV for n=5 bidders with rho=0.5?", "answer": "0.798 - 0.679 = 0.119, an increase of about 17.5%"},
        ],
    })

    # --- Equations (10 main) ---

    eq_expected_utility = EquationSpec(
        "expected-utility",
        r"U_i(v_i, b_i) = v_i \cdot q_i(b_i, b_{-i}) - t_i(b_i, b_{-i})",
        "eq:expected-utility",
        r"Expected utility of bidder $i$ with valuation $v_i$: probability of winning $q_i$ times value, minus expected payment $t_i$.",
        [{"question": "What does the expected utility formula say about a bidder's payoff?", "answer": "Bidder i's payoff is the probability-weighted value of winning minus the expected payment"}],
    )

    eq_ic = EquationSpec(
        "ic-constraint",
        r"U_i(v_i, v_i) \geq U_i(v_i, v_i'), \quad \forall\, v_i, v_i' \in [\underline{v}, \bar{v}]",
        "eq:ic",
        r"Incentive Compatibility (IC): truthful reporting is a best response; misreporting $v_i'$ does not improve payoff.",
        [{"question": "What does the IC constraint require?", "answer": "Truthful reporting is weakly optimal — a bidder cannot improve payoff by misreporting their valuation"}],
    )

    eq_ir = EquationSpec(
        "ir-constraint",
        r"U_i(v_i, v_i) \geq 0, \quad \forall\, v_i \in [\underline{v}, \bar{v}]",
        "eq:ir",
        r"Individual Rationality (IR): every type weakly prefers participating. Binds at the lowest type: $U_i(\underline{v}, \underline{v}) = 0$.",
    )

    eq_revelation_principle = EquationSpec(
        "revelation-principle",
        r"\text{For any mechanism } \mathcal{M} \text{ with equilibrium } \sigma^*, \;\exists \text{ a direct mechanism } \mathcal{M}' \text{ that is IC, IR, and outcome-equivalent}",
        "eq:revelation-principle",
        r"Revelation Principle: without loss of generality, restrict attention to direct, incentive-compatible, individually rational mechanisms.",
    )

    eq_virtual_valuation = EquationSpec(
        "virtual-valuation",
        r"\varphi(v) = v - \frac{1 - F(v)}{f(v)}",
        "eq:virtual-valuation",
        r"Virtual valuation $\varphi(v)$: the marginal revenue to the seller from selling to type $v$. Equals $v$ minus the inverse hazard rate $[1-F(v)]/f(v)$.",
        [{"question": "What is the virtual valuation formula?", "answer": r"\varphi(v) = v - [1-F(v)]/f(v)"}],
    )

    eq_optimal_reserve = EquationSpec(
        "optimal-reserve",
        r"\varphi(r^*) = 0 \implies r^* - \frac{1 - F(r^*)}{f(r^*)} = 0",
        "eq:optimal-reserve",
        r"Myerson optimal reserve price $r^*$: the unique solution to $\varphi(r^*) = 0$. For Uniform[0,1], $r^* = 1/2$; for Exp(1), $r^* = 1$.",
        [{"question": "How is the Myerson optimal reserve price determined?", "answer": "It is the solution to phi(r*) = 0, i.e., the value where virtual valuation equals zero"}],
    )

    eq_revenue_equivalence = EquationSpec(
        "revenue-equivalence",
        r"E[\text{Rev}^A] = \int_{\underline{v}}^{\bar{v}} \bar{q}(v) \varphi(v) f(v)\,dv = E[\text{Rev}^B] \iff q^A = q^B \text{ and } U_i(\underline{v}) = 0",
        "eq:revenue-equivalence",
        r"Revenue Equivalence Theorem: any two symmetric auctions that allocate the object to the same winner and give the lowest type zero surplus yield identical expected revenue.",
    )

    eq_optimal_allocation = EquationSpec(
        "optimal-allocation",
        r"q_i^*(v) = \mathbf{1}\!\left[\varphi(v_i) \geq \max_{j \neq i} \varphi(v_j) \;\text{ and }\; \varphi(v_i) \geq 0\right], \quad \begin{bmatrix} q_1^*(v) \\ \vdots \\ q_n^*(v) \end{bmatrix} \in \{0,1\}^n, \; \sum_{i=1}^n q_i^* \leq 1",
        "eq:optimal-allocation",
        r"Myerson optimal allocation rule: allocate the object to the bidder with the highest non-negative virtual valuation.",
        [{"question": "What is the Myerson optimal allocation rule?", "answer": "Award the object to the bidder with the highest virtual valuation, provided it is non-negative"}],
    )

    eq_expected_revenue = EquationSpec(
        "expected-revenue",
        r"E[\text{Rev}^*] = \int_{r^*}^{\bar{v}} \varphi(v) \, n f(v) F(v)^{n-1}\,dv = E\!\left[\varphi(v_{(n)}) \cdot \mathbf{1}[\varphi(v_{(n)}) \geq 0]\right], \quad \hat{R}_n \xrightarrow{p} E[\text{Rev}^*]",
        "eq:expected-revenue",
        r"Expected revenue formula: the seller's expected revenue equals expected virtual surplus allocated, i.e., the virtual value of the winning bidder when winning is optimal.",
    )

    eq_hazard_regularity = EquationSpec(
        "hazard-regularity",
        r"\frac{d}{dv}\left[v - \frac{1-F(v)}{f(v)}\right] = \varphi'(v) \geq 0 \iff \frac{d}{dv}\!\left[\frac{1-F(v)}{f(v)}\right] \leq 1",
        "eq:hazard-regularity",
        r"Regularity condition: $\varphi(v)$ is non-decreasing. Equivalently, the hazard rate $f(v)/[1-F(v)]$ is non-decreasing (monotone hazard rate condition).",
        [{"question": "What does the regularity condition require?", "answer": "The virtual valuation function must be non-decreasing, equivalently the hazard rate f(v)/[1-F(v)] must be non-decreasing"}],
    )

    # --- Appendix proof block (~50 lines of heavy math) ---
    appendix_proof_text = r"""
\begin{theorem}[Revenue Equivalence Theorem]
\label{thm:rev-equiv}
Let $v_1, \ldots, v_n \overset{\mathrm{iid}}{\sim} F$ on $[\underline{v}, \bar{v}]$ with $F$ continuous and strictly increasing. Consider any two direct mechanisms $(q, t)$ and $(q', t')$ satisfying IC and IR. If $q(v) = q'(v)$ for all $v$ and $U_i(\underline{v}) = U_i'(\underline{v}) = 0$, then $E[t_i(v)] = E[t_i'(v)]$ for all $i$.
\end{theorem}

\begin{proof}
By the envelope theorem, the IC constraint implies $U'(v) = \bar{q}(v)$, where $\bar{q}(v) = E_{v_{-i}}[q(v, v_{-i})]$. Integrating from $\underline{v}$ with $U(\underline{v}) = 0$ gives $U(v) = \int_{\underline{v}}^{v} \bar{q}(s)\,ds$, hence:
\begin{align}
\bar{t}(v) &= v \cdot \bar{q}(v) - \int_{\underline{v}}^{v} \bar{q}(s)\,ds.
\end{align}
Taking expectations and applying Fubini's theorem:
\begin{align}
E[\bar{t}(v)] &= \int_{\underline{v}}^{\bar{v}} \bar{q}(v) \left[v - \frac{1-F(v)}{f(v)}\right] f(v)\,dv = E[\varphi(v) \cdot \bar{q}(v)].
\end{align}
Since both mechanisms share $\bar{q}$ and $U(\underline{v}) = 0$, summing over $i$ gives $E[\text{Rev}] = E[\text{Rev}']$.
\end{proof}

\begin{theorem}[Myerson Optimal Mechanism]
\label{thm:myerson}
Under the regularity condition $\varphi'(v) \geq 0$, the revenue-maximizing mechanism allocates the object to the bidder with the highest non-negative virtual valuation, with reserve price $r^* = \varphi^{-1}(0)$.
\end{theorem}

\begin{proof}
From Revenue Equivalence, $E[\text{Rev}] = \sum_{i} E[\varphi(v_i) q_i(v)]$. Pointwise maximization subject to $\sum_i q_i \leq 1$, $q_i \geq 0$ yields:
\begin{align}
q_i^*(v) &= \begin{cases} 1 & \text{if } \varphi(v_i) = \max_j \varphi(v_j) \geq 0, \\ 0 & \text{otherwise.} \end{cases}
\end{align}
Regularity ensures $\varphi$ is monotone, so $q_i^*$ is non-decreasing in $v_i$ (IC). IR holds since $U(\underline{v}) = 0$ and $U$ is increasing.
\end{proof}

\begin{theorem}[Dominant Strategy Incentive Compatibility of SPA]
\label{thm:spa-ic}
In the second-price auction, bidding $b_i = v_i$ is a weakly dominant strategy. The payoff is $\pi_i = (v_i - m_{-i})\mathbf{1}[b_i > m_{-i}]$ where $m_{-i} = \max_{j \neq i} b_j$. If $v_i > m_{-i}$, truthful bidding wins with positive surplus; if $v_i < m_{-i}$, truthful bidding loses avoiding negative surplus. No deviation strictly improves payoff.
\end{theorem}

\begin{lemma}[VCG Payment Formula]
\label{lem:vcg}
In the VCG mechanism, bidder $i$'s payment equals the externality imposed on others:
\begin{align}
t_i^{\mathrm{VCG}}(v) &= \sum_{j \neq i} v_j q_j^{\mathrm{eff}}(v_{-i}) - \sum_{j \neq i} v_j q_j^{\mathrm{eff}}(v).
\end{align}
In a single-item auction this simplifies to $t_i^{\mathrm{VCG}}(v) = \max_{j \neq i} v_j \cdot q_i^{\mathrm{eff}}(v)$, i.e., the winner pays the second-highest bid.
\end{lemma}

\begin{lemma}[Convergence of Empirical Revenue to Optimal Revenue]
Let $\hat{R}_n$ be the realized revenue with $n$ i.i.d. bidders from $F$. Then:
\begin{align}
\hat{R}_n \xrightarrow{p} E[\text{Rev}^*], \quad \sqrt{n}\bigl(\hat{R}_n - E[\text{Rev}^*]\bigr) \xrightarrow{d} \mathcal{N}\!\left(0, \int_{\underline{v}}^{\bar{v}} \varphi(v)^2 f(v)\,dv - \bigl(E[\text{Rev}^*]\bigr)^2 \right).
\end{align}
\end{lemma}

\begin{remark}[Matrix Representation of Multi-Unit Allocation]
In a $K$-unit auction, the allocation vector $\mathbf{q}^*(v) = (q_1^*, \ldots, q_n^*)' \in \{0,1\}^n$ with $\sum_i q_i^* \leq K$ satisfies:
\begin{align}
\begin{bmatrix} q_1^* \\ q_2^* \\ \vdots \\ q_n^* \end{bmatrix} = \begin{bmatrix} \mathbf{1}[\varphi(v_1) \geq \varphi(v_{(n-K+1)})] \\ \mathbf{1}[\varphi(v_2) \geq \varphi(v_{(n-K+1)})] \\ \vdots \\ \mathbf{1}[\varphi(v_n) \geq \varphi(v_{(n-K+1)})] \end{bmatrix} \cdot \mathbf{1}[\varphi(v_{(n-K+1)}) \geq 0].
\end{align}
\end{remark}
"""

    appendix_proof_table = TableSpec(
        table_id="appendix-proofs-micro",
        caption="",
        label="",
        latex=appendix_proof_text,
    )

    # --- Sections ---

    intro = SectionSpec(
        "Introduction",
        "sec:intro-micro",
        text_paragraphs=12,
        equations=[eq_revelation_principle],
    )

    auction_prelims = SectionSpec(
        "Auction Preliminaries",
        "sec:auction-prelims",
        text_paragraphs=6,
        tables=[mechanism_comparison, bidder_surplus_by_mechanism],
        subsections=[
            SectionSpec(
                "Auction Formats and Rules",
                "sec:auction-formats",
                level=2,
                text_paragraphs=10,
            ),
            SectionSpec(
                "Equilibrium Concepts in Auctions",
                "sec:auction-equilibrium",
                level=2,
                text_paragraphs=10,
            ),
        ],
    )

    ipv_model = SectionSpec(
        "The Independent Private Values Model",
        "sec:ipv",
        text_paragraphs=6,
        equations=[eq_expected_utility, eq_ic, eq_ir],
        subsections=[
            SectionSpec(
                "Model Setup and Assumptions",
                "sec:ipv-setup",
                level=2,
                text_paragraphs=10,
            ),
            SectionSpec(
                "Bidding Strategies and Equilibrium",
                "sec:ipv-bidding",
                level=2,
                text_paragraphs=10,
            ),
        ],
    )

    revenue_equivalence = SectionSpec(
        "Revenue Equivalence",
        "sec:rev-equiv",
        text_paragraphs=4,
        equations=[eq_revenue_equivalence],
        subsections=[
            SectionSpec(
                "Statement and Intuition",
                "sec:rev-equiv-statement",
                level=2,
                text_paragraphs=10,
            ),
            SectionSpec(
                "Applications and Limits of Revenue Equivalence",
                "sec:rev-equiv-apps",
                level=2,
                text_paragraphs=10,
                tables=[revenue_comparison],
            ),
        ],
    )

    optimal_auctions = SectionSpec(
        "Optimal Auctions",
        "sec:optimal-auctions",
        text_paragraphs=6,
        equations=[eq_virtual_valuation, eq_optimal_reserve, eq_optimal_allocation, eq_expected_revenue],
        tables=[numerical_uniform, numerical_exponential, optimal_vs_efficient, optimal_reserve_distributions],
        subsections=[
            SectionSpec(
                "Virtual Valuations and the Regularity Condition",
                "sec:virtual-val",
                level=2,
                text_paragraphs=8,
                equations=[eq_hazard_regularity],
            ),
            SectionSpec(
                "Characterization of the Optimal Mechanism",
                "sec:optimal-char",
                level=2,
                text_paragraphs=8,
            ),
            SectionSpec(
                "Welfare Analysis of Optimal Auctions",
                "sec:optimal-welfare",
                level=2,
                text_paragraphs=8,
                tables=[welfare_decomposition],
            ),
        ],
    )

    extensions = SectionSpec(
        "Extensions",
        "sec:extensions",
        text_paragraphs=6,
        tables=[correlated_vs_ipv_revenue],
        subsections=[
            SectionSpec(
                "Correlated Values and Cremer-McLean",
                "sec:correlated",
                level=2,
                text_paragraphs=9,
            ),
            SectionSpec(
                "Risk Aversion and Asymmetric Bidders",
                "sec:risk-aversion",
                level=2,
                text_paragraphs=9,
            ),
        ],
    )

    conclusion = SectionSpec(
        "Conclusion",
        "sec:conclusion-micro",
        text_paragraphs=8,
    )

    appendix_a = SectionSpec(
        "Appendix A: Proofs of Main Results",
        "sec:appendix-a-micro",
        text_paragraphs=8,
        tables=[appendix_proof_table],
    )

    appendix_b = SectionSpec(
        "Appendix B: Numerical Examples",
        "sec:appendix-b-micro",
        text_paragraphs=6,
    )

    return PaperSpec(
        paper_id="16",
        field_slug="micro-theory",
        title="Optimal Auction Design: Revenue Maximization and Mechanism Design",
        authors="Eleanor Voss, Kwame Asante, Isabela Fonseca",
        journal_style="econometrica",
        abstract=(
            "We present a self-contained treatment of Myerson's (1981) optimal auction theory, "
            "deriving the revenue-maximizing mechanism from first principles within the independent "
            "private values paradigm. The Revenue Equivalence Theorem is proven via the envelope "
            "condition and Fubini's theorem, establishing that all standard auction formats yield "
            "identical expected revenue under symmetric risk-neutral bidders. Departing from revenue "
            "equivalence, we characterize the Myerson optimal mechanism through the virtual valuation "
            r"$\varphi(v) = v - [1-F(v)]/f(v)$, showing that the optimal allocation awards the "
            "object to the highest non-negative virtual valuation bidder at a reserve price satisfying "
            r"$\varphi(r^*) = 0$. For the Uniform$[0,1]$ distribution with two bidders, the optimal "
            "reserve is $r^* = 1/2$, yielding revenue $5/12 \approx 0.417$ compared to $1/3$ without "
            "a reserve. We provide complete proofs of Revenue Equivalence, the Myerson mechanism "
            "characterization, dominant-strategy incentive compatibility of the second-price auction, "
            "and the VCG payment formula, with numerical comparisons across distribution families."
        ),
        sections=[
            intro,
            auction_prelims,
            ipv_model,
            revenue_equivalence,
            optimal_auctions,
            extensions,
            conclusion,
            appendix_a,
            appendix_b,
        ],
        bibliography_entries=[
            r"\bibitem{myerson1981} Myerson, R. B. (1981). Optimal Auction Design. \textit{Mathematics of Operations Research}, 6(1), 58--73.",
            r"\bibitem{riley1981} Riley, J. G. and Samuelson, W. F. (1981). Optimal Auctions. \textit{American Economic Review}, 71(3), 381--392.",
            r"\bibitem{vickrey1961} Vickrey, W. (1961). Counterspeculation, Auctions, and Competitive Sealed Tenders. \textit{Journal of Finance}, 16(1), 8--37.",
            r"\bibitem{bulow1989} Bulow, J. and Roberts, J. (1989). The Simple Economics of Optimal Auctions. \textit{Journal of Political Economy}, 97(5), 1060--1090.",
            r"\bibitem{milgrom2004} Milgrom, P. (2004). \textit{Putting Auction Theory to Work}. Cambridge University Press.",
            r"\bibitem{krishna2010} Krishna, V. (2010). \textit{Auction Theory}, 2nd ed. Academic Press.",
            r"\bibitem{klemperer1999} Klemperer, P. (1999). Auction Theory: A Guide to the Literature. \textit{Journal of Economic Surveys}, 13(3), 227--286.",
            r"\bibitem{milgrom2002} Milgrom, P. and Segal, I. (2002). Envelope Theorems for Arbitrary Choice Sets. \textit{Econometrica}, 70(2), 583--601.",
        ],
        target_pages=52,
        qa=[
            {"question": "What is the virtual valuation formula in Myerson's theory?", "answer": r"\varphi(v) = v - [1-F(v)]/f(v)"},
            {"question": "What is the optimal reserve price for Uniform[0,1] with 2 bidders?", "answer": "r* = 1/2, from solving phi(r*) = 0 with phi(v) = 2v - 1"},
            {"question": "What does the Revenue Equivalence Theorem state?", "answer": "Any two symmetric auctions satisfying IC and IR that allocate to the same winner and give the lowest type zero surplus yield identical expected seller revenue"},
            {"question": "What is the Myerson optimal allocation rule?", "answer": "Allocate to the bidder with the highest non-negative virtual valuation; withhold if all virtual valuations are negative"},
            {"question": "Why does the optimal mechanism generate deadweight loss?", "answer": "The optimal reserve r* > 0 excludes trades where v < r*, even when v > 0, creating deadweight loss equal to the foregone surplus from excluded high-value trades"},
        ],
    )


PAPER_BUILDERS["16"] = _paper_16_micro_theory
