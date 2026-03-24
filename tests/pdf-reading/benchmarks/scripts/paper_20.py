#!/usr/bin/env python3
"""Paper builder for paper 20 (Market Design -- Abdulkadiroglu et al school choice / DA style)."""

from __future__ import annotations

from generate_long_form import (
    EquationSpec, PaperSpec, SectionSpec, TableSpec,
    render_regression_table, render_math_table,
    PAPER_BUILDERS,
)


def _paper_20_market_design() -> PaperSpec:
    """Paper 20: Market Design -- school choice, deferred acceptance, RDD."""

    # ── Tables ──

    tab_student_summary = render_regression_table({
        "table_id": "student-summary-stats",
        "caption": "Student Summary Statistics",
        "label": "tab:student-summary-stats",
        "model_labels": ["All students", "DA assigned", "Not DA assigned", "Difference"],
        "panels": [
            {
                "variables": [
                    {"label": "Female (\\%)",
                     "coefficients": ["49.8", "50.2", "49.4", "0.8"]},
                    {"label": "Free/reduced lunch (\\%)",
                     "coefficients": ["62.4", "64.1", "60.8", "3.3"]},
                    {"label": "Special education (\\%)",
                     "coefficients": ["14.2", "13.8", "14.6", "-0.8"]},
                    {"label": "English language learner (\\%)",
                     "coefficients": ["18.7", "19.4", "18.1", "1.3"]},
                    {"label": "4th grade math score (std. dev.)",
                     "coefficients": ["0.00", "0.04", "-0.04", "0.08"]},
                    {"label": "4th grade reading score (std. dev.)",
                     "coefficients": ["0.00", "0.02", "-0.02", "0.04"]},
                    {"label": "Age at application (months)",
                     "coefficients": ["131.4", "131.6", "131.2", "0.4"]},
                ],
            },
        ],
        "notes": "Sample: all applicants to the centralized school choice system, 2005-2018 cohorts. DA assigned = student was assigned to their first-choice school via DA. Differences are raw means differences; none are statistically significant at the 5\\% level after Bonferroni correction.",
        "qa": [
            {"question": "What fraction of students receive free or reduced lunch?", "answer": "62.4%"},
            {"question": "Are DA-assigned and non-DA-assigned students different in 4th grade math scores?", "answer": "Slightly: 0.04 vs -0.04 standard deviations, difference of 0.08, but not statistically significant"},
            {"question": "What fraction of students are English language learners?", "answer": "18.7%"},
        ],
    })

    tab_school_chars = render_regression_table({
        "table_id": "school-characteristics",
        "caption": "School Characteristics",
        "label": "tab:school-characteristics",
        "model_labels": ["All schools", "Oversubscribed", "Undersubscribed", "Difference"],
        "panels": [
            {
                "variables": [
                    {"label": "Total enrollment",
                     "coefficients": ["482", "641", "384", "257***"]},
                    {"label": "Free/reduced lunch (\\%)",
                     "coefficients": ["59.4", "52.1", "63.8", "-11.7***"]},
                    {"label": "4th-8th grade test score (std. dev.)",
                     "coefficients": ["0.00", "0.41", "-0.24", "0.65***"]},
                    {"label": "Pupil-teacher ratio",
                     "coefficients": ["16.4", "15.8", "16.8", "-1.0**"]},
                    {"label": "Share of teachers with > 5 years experience (\\%)",
                     "coefficients": ["61.4", "68.4", "57.1", "11.3***"]},
                    {"label": "Distance from median applicant (km)",
                     "coefficients": ["2.84", "3.12", "2.68", "0.44"]},
                ],
            },
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Oversubscribed = more applicants than seats in at least one year. School-level means, weighted by enrollment.",
        "qa": [
            {"question": "Are oversubscribed schools higher or lower in average test scores?", "answer": "Higher: 0.41 vs -0.24 standard deviations"},
            {"question": "Do oversubscribed schools have fewer free/reduced lunch students?", "answer": "Yes: 52.1% vs 63.8%"},
            {"question": "What is the average school enrollment?", "answer": "482 students"},
        ],
    })

    tab_pref = render_regression_table({
        "table_id": "preference-distributions",
        "caption": "Distribution of Student Preferences",
        "label": "tab:preference-distributions",
        "model_labels": ["1 school", "2 schools", "3-5 schools", "6-10 schools", "11+ schools"],
        "panels": [
            {
                "variables": [
                    {"label": "Fraction of applicants (\\%)",
                     "coefficients": ["12.4", "18.7", "31.4", "28.8", "8.7"]},
                    {"label": "Mean test score of 1st choice (std. dev.)",
                     "coefficients": ["0.12", "0.18", "0.24", "0.31", "0.28"]},
                    {"label": "Fraction assigned to 1st choice (\\%)",
                     "coefficients": ["84.1", "72.4", "61.8", "54.2", "49.8"]},
                    {"label": "Fraction assigned to any listed school (\\%)",
                     "coefficients": ["84.1", "88.3", "91.4", "93.8", "95.2"]},
                    {"label": "Distance from 1st choice school (km)",
                     "coefficients": ["1.84", "2.14", "2.74", "3.12", "3.84"]},
                ],
            },
        ],
        "notes": "Students who list more schools are more likely to be assigned to any listed school. Maximum list length is 12 schools. About 8.7\\% of applicants list 11+ schools and are nearly always assigned to a listed school.",
        "qa": [
            {"question": "What fraction of students list only one school?", "answer": "12.4%"},
            {"question": "Does listing more schools increase the chance of assignment to some listed school?", "answer": "Yes: from 84.1% (1 school) to 95.2% (11+ schools)"},
            {"question": "What is the maximum list length allowed?", "answer": "12 schools"},
        ],
    })

    tab_da_results = render_regression_table({
        "table_id": "da-assignment-results",
        "caption": "DA Algorithm Assignment Outcomes",
        "label": "tab:da-assignment-results",
        "model_labels": ["2005-2008", "2009-2012", "2013-2016", "2017-2018"],
        "panels": [
            {
                "variables": [
                    {"label": "Assigned to 1st choice (\\%)",
                     "coefficients": ["61.4", "63.8", "66.2", "68.4"]},
                    {"label": "Assigned to 2nd choice (\\%)",
                     "coefficients": ["14.2", "13.8", "12.4", "11.8"]},
                    {"label": "Assigned to 3rd+ choice (\\%)",
                     "coefficients": ["11.8", "10.4", "9.8", "9.1"]},
                    {"label": "Unassigned (\\%)",
                     "coefficients": ["12.6", "12.0", "11.6", "10.7"]},
                    {"label": "Justified envy rate (\\%)",
                     "coefficients": ["0.0", "0.0", "0.0", "0.0"]},
                    {"label": "Avg. rank of assigned school",
                     "coefficients": ["1.74", "1.71", "1.68", "1.63"]},
                ],
            },
        ],
        "notes": "Cohorts split into 4-year periods. Justified envy rate = fraction of student-school pairs where student $i$ prefers school $s$ and has higher priority than an assigned student. DA produces stable matchings so this is exactly zero by construction.",
        "qa": [
            {"question": "What fraction of students are assigned to their first choice in 2017-2018?", "answer": "68.4%"},
            {"question": "What is the justified envy rate under DA?", "answer": "0.0% -- DA produces stable matchings which eliminate justified envy"},
            {"question": "Has the fraction assigned to first choice been increasing over time?", "answer": "Yes: from 61.4% in 2005-2008 to 68.4% in 2017-2018"},
        ],
    })

    tab_rdd_cutoff = render_regression_table({
        "table_id": "rdd-cutoff-effects",
        "caption": "RDD First Stage: Probability of Attending School at Admission Cutoff",
        "label": "tab:rdd-cutoff-effects",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "dep_var": "Dep. var.: Attending school $s$ in grade 6",
                "variables": [
                    {"label": "Above cutoff (sharp RD)",
                     "coefficients": ["0.61***", "0.61***", "0.62***", "0.62***"],
                     "std_errors": ["(0.02)", "(0.02)", "(0.02)", "(0.02)"]},
                    {"label": "Running variable (score - cutoff)",
                     "coefficients": ["0.04***", "0.04***", "0.03***", "0.03***"],
                     "std_errors": ["(0.01)", "(0.01)", "(0.01)", "(0.01)"]},
                    {"label": "Above x Running",
                     "coefficients": ["-0.02*", "-0.02*", "-0.01", "-0.01"],
                     "std_errors": ["(0.01)", "(0.01)", "(0.01)", "(0.01)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Baseline covariates", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "School-year FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Bandwidth (points)", "values": ["10", "10", "10", "8"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["24,841", "24,841", "24,841", "21,382"]},
            {"label": "Mean dep. var. (below cutoff)", "values": ["0.12", "0.12", "0.12", "0.12"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Running variable is the normalized priority score minus cutoff. Sharp RD: above cutoff indicator. Bandwidth selected by Calonico-Cattaneo-Titiunik (2014) MSE-optimal procedure. Standard errors clustered by school-cohort.",
        "qa": [
            {"question": "What is the first-stage jump at the cutoff?", "answer": "0.61 -- students just above the cutoff are 61 percentage points more likely to attend the school"},
            {"question": "What is the mean attendance rate just below the cutoff?", "answer": "0.12 (12%)"},
            {"question": "What bandwidth is used in the baseline specification?", "answer": "10 points (Calonico-Cattaneo-Titiunik MSE-optimal)"},
        ],
    })

    tab_rdd_test = render_regression_table({
        "table_id": "rdd-test-score-outcomes",
        "caption": "RDD Estimates: Effect of Attending Oversubscribed School on 8th Grade Test Scores",
        "label": "tab:rdd-test-score-outcomes",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "label": "Panel A: Math scores (standard deviations)",
                "variables": [
                    {"label": "ITT (above cutoff)",
                     "coefficients": ["0.18***", "0.19***", "0.19***", "0.18***"],
                     "std_errors": ["(0.05)", "(0.05)", "(0.05)", "(0.06)"]},
                    {"label": "IV (2SLS: attend = 1)",
                     "coefficients": ["0.30***", "0.31***", "0.31***", "0.29***"],
                     "std_errors": ["(0.09)", "(0.09)", "(0.08)", "(0.10)"]},
                ],
            },
            {
                "label": "Panel B: Reading scores (standard deviations)",
                "variables": [
                    {"label": "ITT (above cutoff)",
                     "coefficients": ["0.12**", "0.13**", "0.13**", "0.12**"],
                     "std_errors": ["(0.05)", "(0.05)", "(0.05)", "(0.06)"]},
                    {"label": "IV (2SLS: attend = 1)",
                     "coefficients": ["0.20**", "0.21**", "0.21**", "0.19**"],
                     "std_errors": ["(0.09)", "(0.09)", "(0.08)", "(0.10)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Baseline covariates", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "School-year FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Bandwidth (points)", "values": ["10", "10", "10", "8"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["22,184", "22,184", "22,184", "19,013"]},
            {"label": "First-stage F", "values": ["841", "841", "847", "798"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. ITT = intent-to-treat. IV uses above-cutoff indicator as instrument for school attendance. Standard errors clustered by school-cohort. Scores normalized to mean 0, std. dev. 1 within grade-year.",
        "qa": [
            {"question": "What is the IV estimate of attending an oversubscribed school on math scores?", "answer": "0.30 standard deviations in the baseline specification"},
            {"question": "Is the effect larger for math or reading?", "answer": "Math (0.30 sd) is larger than reading (0.20 sd)"},
            {"question": "What is the first-stage F-statistic?", "answer": "841, far above conventional weak-instrument thresholds"},
        ],
    })

    tab_rdd_grad = render_regression_table({
        "table_id": "rdd-graduation",
        "caption": "RDD Estimates: Effect of Attending Oversubscribed School on High School Outcomes",
        "label": "tab:rdd-graduation",
        "model_labels": ["(1)", "(2)", "(3)", "(4)"],
        "panels": [
            {
                "label": "Panel A: High school graduation (pp)",
                "variables": [
                    {"label": "ITT (above cutoff)",
                     "coefficients": ["4.2***", "4.4***", "4.3***", "4.1***"],
                     "std_errors": ["(1.4)", "(1.4)", "(1.4)", "(1.5)"]},
                    {"label": "IV (2SLS)",
                     "coefficients": ["6.9***", "7.2***", "6.9***", "6.6***"],
                     "std_errors": ["(2.3)", "(2.3)", "(2.3)", "(2.5)"]},
                ],
            },
            {
                "label": "Panel B: 4-year college enrollment (pp)",
                "variables": [
                    {"label": "ITT (above cutoff)",
                     "coefficients": ["3.1**", "3.4**", "3.3**", "3.0**"],
                     "std_errors": ["(1.4)", "(1.4)", "(1.4)", "(1.5)"]},
                    {"label": "IV (2SLS)",
                     "coefficients": ["5.1**", "5.6**", "5.3**", "4.8**"],
                     "std_errors": ["(2.3)", "(2.3)", "(2.3)", "(2.5)"]},
                ],
            },
        ],
        "controls": [
            {"label": "Baseline covariates", "values": ["No", "Yes", "Yes", "Yes"]},
            {"label": "School-year FE", "values": ["No", "No", "Yes", "Yes"]},
            {"label": "Bandwidth (points)", "values": ["10", "10", "10", "8"]},
        ],
        "summary": [
            {"label": "Observations", "values": ["18,421", "18,421", "18,421", "15,847"]},
            {"label": "Mean dep. var. (below cutoff, \\%)", "values": ["74.2", "74.2", "74.2", "74.2"]},
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Outcome is an indicator for the event. IV uses above-cutoff indicator as instrument.",
        "qa": [
            {"question": "What is the IV estimate of attending an oversubscribed school on graduation rate?", "answer": "6.9 percentage points in the baseline"},
            {"question": "What is the baseline graduation rate for students just below the cutoff?", "answer": "74.2%"},
            {"question": "Does attending the oversubscribed school increase college enrollment?", "answer": "Yes: 5.1 percentage point increase in 4-year college enrollment (IV estimate)"},
        ],
    })

    tab_welfare = render_math_table({
        "table_id": "welfare-comparison-mechanisms",
        "caption": "Welfare Comparison of School Assignment Mechanisms",
        "label": "tab:welfare-comparison-mechanisms",
        "col_headers": [
            {"text": "Stable?", "latex": "Stable?"},
            {"text": "Strategy-proof?", "latex": "Strategy-proof?"},
            {"text": "Avg Welfare", "latex": "Avg Welfare"},
            {"text": "Worst-case Welfare", "latex": "Worst-case Welfare"},
        ],
        "rows": [
            {"label": "Student-proposing DA", "label_latex": "Student-proposing DA",
             "cells": [{"text": "Yes", "latex": "Yes"},
                       {"text": "Yes", "latex": "Yes"},
                       {"text": "0.742", "latex": "0.742"},
                       {"text": "0.484", "latex": "0.484"}]},
            {"label": "School-proposing DA", "label_latex": "School-proposing DA",
             "cells": [{"text": "Yes", "latex": "Yes"},
                       {"text": "No", "latex": "No"},
                       {"text": "0.731", "latex": "0.731"},
                       {"text": "0.412", "latex": "0.412"}]},
            {"label": "Boston mechanism", "label_latex": "Boston mechanism",
             "cells": [{"text": "No", "latex": "No"},
                       {"text": "No", "latex": "No"},
                       {"text": "0.718", "latex": "0.718"},
                       {"text": "0.314", "latex": "0.314"}]},
            {"label": "Top Trading Cycles (TTC)", "label_latex": "Top Trading Cycles (TTC)",
             "cells": [{"text": "No", "latex": "No"},
                       {"text": "Yes", "latex": "Yes"},
                       {"text": "0.761", "latex": "0.761"},
                       {"text": "0.498", "latex": "0.498"}]},
            {"label": "Random serial dictatorship", "label_latex": "Random serial dictatorship",
             "cells": [{"text": "No", "latex": "No"},
                       {"text": "Yes", "latex": "Yes"},
                       {"text": "0.724", "latex": "0.724"},
                       {"text": "0.441", "latex": "0.441"}]},
            {"label": "Immediate acceptance (IA)", "label_latex": "Immediate acceptance (IA)",
             "cells": [{"text": "No", "latex": "No"},
                       {"text": "No", "latex": "No"},
                       {"text": "0.706", "latex": "0.706"},
                       {"text": "0.287", "latex": "0.287"}]},
        ],
        "qa": [
            {"question": "Which mechanism is both stable and strategy-proof?", "answer": "Student-proposing DA"},
            {"question": "Which mechanism achieves the highest average welfare?", "answer": "Top Trading Cycles (TTC) with 0.761"},
            {"question": "Is the Boston mechanism stable?", "answer": "No"},
        ],
    })

    tab_boston_da = render_regression_table({
        "table_id": "boston-vs-da",
        "caption": "Boston Mechanism vs. Deferred Acceptance: Outcomes Under Misreported Preferences",
        "label": "tab:boston-vs-da",
        "model_labels": ["Truthful", "Strategize top choice", "Strategize full list", "Nash equilibrium"],
        "panels": [
            {
                "label": "Panel A: Boston mechanism",
                "variables": [
                    {"label": "Assigned to 1st true preference (\\%)",
                     "coefficients": ["71.4", "68.4", "61.8", "58.4"]},
                    {"label": "Avg welfare (0-1 scale)",
                     "coefficients": ["0.718", "0.694", "0.672", "0.651"]},
                    {"label": "Welfare loss from manipulation (pp)",
                     "coefficients": ["0.0", "2.4", "4.6", "6.7"]},
                ],
            },
            {
                "label": "Panel B: Student-proposing DA",
                "variables": [
                    {"label": "Assigned to 1st true preference (\\%)",
                     "coefficients": ["66.2", "66.2", "66.2", "66.2"]},
                    {"label": "Avg welfare (0-1 scale)",
                     "coefficients": ["0.742", "0.742", "0.742", "0.742"]},
                    {"label": "Welfare loss from manipulation (pp)",
                     "coefficients": ["0.0", "0.0", "0.0", "0.0"]},
                ],
            },
        ],
        "notes": "Welfare measured as fraction of first-choice school expected value captured. Boston mechanism exhibits welfare-reducing manipulation in equilibrium (6.7 pp loss). DA is strategy-proof so manipulation has no effect.",
        "qa": [
            {"question": "Does manipulation under the Boston mechanism reduce welfare?", "answer": "Yes, by 6.7 percentage points in Nash equilibrium relative to truthful play"},
            {"question": "Does manipulation under DA reduce welfare?", "answer": "No, welfare loss is 0.0 pp at all manipulation levels -- DA is strategy-proof"},
            {"question": "Which mechanism assigns more students to their true first choice under truthful play?", "answer": "Boston mechanism (71.4% vs 66.2% for DA)"},
        ],
    })

    tab_ttc_da = render_regression_table({
        "table_id": "ttc-vs-da",
        "caption": "TTC vs. DA: Assignment Differences and Welfare",
        "label": "tab:ttc-vs-da",
        "model_labels": ["TTC", "DA", "TTC-DA", "p-value"],
        "panels": [
            {
                "variables": [
                    {"label": "Assigned to 1st choice (\\%)",
                     "coefficients": ["68.4", "66.2", "2.2", "0.01"]},
                    {"label": "Assigned to any listed school (\\%)",
                     "coefficients": ["94.1", "91.8", "2.3", "0.00"]},
                    {"label": "Average rank of assigned school",
                     "coefficients": ["1.61", "1.68", "-0.07", "0.00"]},
                    {"label": "Utilitarian welfare",
                     "coefficients": ["0.761", "0.742", "0.019", "0.00"]},
                    {"label": "Rawlsian welfare (min utility)",
                     "coefficients": ["0.498", "0.484", "0.014", "0.04"]},
                    {"label": "Stable matchings achieved (\\%)",
                     "coefficients": ["N/A", "100", "--", "--"]},
                    {"label": "Justified envy (\\% of pairs)",
                     "coefficients": ["1.84", "0.00", "1.84", "0.00"]},
                ],
            },
        ],
        "notes": "TTC uses current assignment as endowment. DA = student-proposing DA. Welfare calculated from estimated preference parameters. Justified envy under TTC: 1.84\\% of student-school pairs where a student prefers a school over their TTC assignment and has higher priority than an assigned student.",
        "qa": [
            {"question": "Does TTC achieve higher average welfare than DA?", "answer": "Yes: 0.761 vs 0.742"},
            {"question": "Is TTC stable?", "answer": "No, TTC has 1.84% of student-school pairs with justified envy"},
            {"question": "What fraction of DA matchings are stable?", "answer": "100%"},
        ],
    })

    tab_subgroup = render_regression_table({
        "table_id": "subgroup-effects",
        "caption": "Heterogeneous Effects of Attending Oversubscribed School by Student Subgroup",
        "label": "tab:subgroup-effects",
        "model_labels": ["Math (sd)", "Reading (sd)", "Graduation (pp)", "College (pp)"],
        "panels": [
            {
                "variables": [
                    {"label": "All students (IV baseline)",
                     "coefficients": ["0.30***", "0.20**", "6.9***", "5.1**"],
                     "std_errors": ["(0.09)", "(0.09)", "(2.3)", "(2.3)"]},
                    {"label": "Free/reduced lunch",
                     "coefficients": ["0.34***", "0.23**", "8.1***", "6.2**"],
                     "std_errors": ["(0.11)", "(0.11)", "(2.8)", "(2.8)"]},
                    {"label": "Not free/reduced lunch",
                     "coefficients": ["0.24**", "0.14", "5.2*", "3.4"],
                     "std_errors": ["(0.12)", "(0.13)", "(3.0)", "(3.1)"]},
                    {"label": "English language learner",
                     "coefficients": ["0.41***", "0.28**", "9.4***", "7.1**"],
                     "std_errors": ["(0.14)", "(0.14)", "(3.4)", "(3.4)"]},
                    {"label": "Special education",
                     "coefficients": ["0.22", "0.18", "4.1", "2.8"],
                     "std_errors": ["(0.18)", "(0.18)", "(4.2)", "(4.3)"]},
                    {"label": "Female",
                     "coefficients": ["0.28***", "0.22**", "6.4**", "6.2**"],
                     "std_errors": ["(0.10)", "(0.10)", "(2.6)", "(2.6)"]},
                    {"label": "Male",
                     "coefficients": ["0.32***", "0.18*", "7.4***", "4.1*"],
                     "std_errors": ["(0.10)", "(0.10)", "(2.7)", "(2.5)"]},
                ],
            },
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. IV estimates using RDD at admission cutoffs. Each row estimated separately with baseline covariates and school-year FE. Standard errors clustered by school-cohort.",
        "qa": [
            {"question": "Which subgroup benefits most in math from attending an oversubscribed school?", "answer": "English language learners (0.41 sd)"},
            {"question": "Are effects larger for free/reduced lunch students than non-FRL students?", "answer": "Yes, 0.34 vs 0.24 sd for math"},
        ],
    })

    tab_app_pref = render_regression_table({
        "table_id": "appendix-preference-elicitation",
        "caption": "Appendix: Estimated Preference Parameters from Structural Demand Model",
        "label": "tab:appendix-preference-elicitation",
        "model_labels": ["Coeff.", "Std. Error", "95\\% CI Low", "95\\% CI High"],
        "panels": [
            {
                "variables": [
                    {"label": "School test score (1 sd increase)",
                     "coefficients": ["1.84***", "0.21", "1.43", "2.25"]},
                    {"label": "Distance (1 km increase)",
                     "coefficients": ["-0.42***", "0.08", "-0.58", "-0.26"]},
                    {"label": "Peer free lunch share (10 pp increase)",
                     "coefficients": ["-0.18**", "0.09", "-0.36", "-0.00"]},
                    {"label": "School size (100 students)",
                     "coefficients": ["0.08*", "0.04", "-0.00", "0.16"]},
                    {"label": "Teacher experience share (10 pp)",
                     "coefficients": ["0.24***", "0.07", "0.10", "0.38"]},
                    {"label": "Fraction same race as student",
                     "coefficients": ["0.31***", "0.08", "0.15", "0.47"]},
                ],
            },
        ],
        "notes": "*** p<0.01, ** p<0.05, * p<0.1. Preference parameters estimated by BLP (1995) method using variation in school availability as instruments. Standard errors from 200 bootstrap replications.",
        "qa": [
            {"question": "What is the most important positive factor in school preferences?", "answer": "School test score (coefficient 1.84 per sd)"},
            {"question": "Does distance deter school choice?", "answer": "Yes, coefficient -0.42 per km is negative and significant"},
        ],
    })

    # ── Main Equations ──
    eqs_20 = [
        EquationSpec("da-step",
                     r"\text{Step } t: \text{ each unmatched student } i \text{ proposes to best unrejected school } s; \text{ school } s \text{ tentatively holds top-}q_s \text{ and rejects others}",
                     "eq:da-step",
                     "Deferred Acceptance algorithm: student proposes, school tentatively holds",
                     [{"question": "What happens in each step of the DA algorithm?",
                       "answer": "Each unmatched student proposes to their most-preferred unrejected school; each school tentatively holds its top-q_s applicants by priority and rejects the rest"}]),
        EquationSpec("stability",
                     r"(i, s) \text{ is a blocking pair if } s \succ_i \mu(i) \text{ and } i \succ_s j \text{ for some } j \in \mu(s), \quad |\mathcal{S}| \leq \binom{n}{2} \cdot \lfloor K/2 \rfloor",
                     "eq:stability",
                     "Stability: no student-school pair prefers each other to their current match",
                     [{"question": "What is a blocking pair?",
                       "answer": "A student i and school s such that s is preferred by i over their current match mu(i), and i is preferred by s over some currently matched student j"}]),
        EquationSpec("strategy-proof",
                     r"\mu_D(\succ_i, \succ_{-i}) \succsim_i \mu_D(\succ_i', \succ_{-i}) \quad \forall \succ_i', \succ_{-i}, i",
                     "eq:strategy-proof",
                     "Strategy-proofness: truthful preference revelation is a dominant strategy under DA",
                     [{"question": "What does strategy-proofness mean?",
                       "answer": "A student cannot improve their assignment by misreporting their preferences: mu_D(true) is weakly preferred to mu_D(misreport) for all misreports and all others' reports"}]),
        EquationSpec("welfare-utilitarian",
                     r"W_U(\mu) = \sum_{i=1}^n u_i(\mu(i)), \quad u_i(s) = \beta_1 q_s + \beta_2 d_{is} + \varepsilon_{is}, \quad \#\{\text{matchings}\} = \binom{n + K - 1}{K} \cdot \prod_{s=1}^{K} \lfloor q_s \rfloor !",
                     "eq:welfare-util",
                     "Utilitarian social welfare: sum of student utilities under matching mu",
                     [{"question": "How is utilitarian welfare calculated?",
                       "answer": "Sum of individual utilities u_i(mu(i)) where utility is a function of school quality q_s and distance d_is"}]),
        EquationSpec("welfare-rawlsian",
                     r"W_R(\mu) = \min_{i=1,\ldots,n} u_i(\mu(i))",
                     "eq:welfare-rawls",
                     "Rawlsian social welfare: minimum utility across all students",
                     [{"question": "What does Rawlsian welfare capture?",
                       "answer": "The welfare of the worst-off student -- the minimum utility across all students in the matching"}]),
        EquationSpec("match-prob",
                     r"P_{is} = \Pr(\mu(i) = s) = \Pr\!\left(\text{priority}_{is} \geq \text{priority}_{\lceil q_s \rceil\text{-th}}\right), \quad \begin{bmatrix} P_{i1} \\ P_{i2} \\ \vdots \\ P_{iK} \end{bmatrix} \in [0,1]^K, \; \sum_{s=1}^K P_{is} \leq 1",
                     "eq:match-prob",
                     "Matching probability: likelihood student i is matched to school s under DA",
                     [{"question": "What determines a student's probability of being matched to a school?",
                       "answer": "Whether the student's priority score at the school is above the cutoff (q_s-th highest applicant priority)"}]),
        EquationSpec("rdd-cutoff",
                     r"Y_i = \alpha + \tau D_i + f(R_i - c) + \varepsilon_i, \quad D_i = \mathbf{1}[R_i \geq c]",
                     "eq:rdd",
                     "RDD at school admission cutoff c; D_i = 1 if student admitted above cutoff",
                     [{"question": "What is the identifying variation in the RDD?",
                       "answer": "Whether student priority score R_i is above or below the school's admission cutoff c; tau is the local average treatment effect for marginal applicants"}]),
        EquationSpec("justified-envy",
                     r"(i, s) \text{ has justified envy if } s \succ_i \mu(i) \text{ and } \text{priority}_{is} > \text{priority}_{js} \text{ for some } j \in \mu(s)",
                     "eq:justified-envy",
                     "Justified envy: student i has higher priority than an assigned student at a school s they prefer",
                     [{"question": "What is justified envy?",
                       "answer": "Student i has justified envy if they prefer school s to their current assignment AND have higher priority than some student who was assigned to s"}]),
        EquationSpec("boston-manipulation",
                     r"\\exists \\succ_i' \\neq \\succ_i : \\mu_{Boston}(\\succ_i', \\succ_{-i}) \\succ_i \\mu_{Boston}(\\succ_i, \\succ_{-i})",
                     "eq:boston-manip",
                     "Boston mechanism is manipulable: misreporting can strictly improve a student's outcome",
                     [{"question": "Is the Boston mechanism strategy-proof?",
                       "answer": "No -- there exist preference reports succ_i' such that the student strictly prefers their assignment under misreporting to truthful play"}]),
    ]

    # ── Appendix proofs ──
    appendix_proofs_20 = r"""
\subsection*{A.1 Proof that DA Produces a Stable Matching}

\begin{proposition}[Stability of DA]
\label{prop:da-stable}
The student-proposing Deferred Acceptance algorithm produces a stable matching.
\end{proposition}

\begin{proof}
Suppose for contradiction that $(i, s)$ is a blocking pair in the DA outcome $\mu_D$. Then $s \succ_i \mu_D(i)$, so student $i$ proposed to school $s$ at some step $t$ before proposing to $\mu_D(i)$. Since $i \notin \mu_D(s)$, school $s$ must have rejected $i$ at some step $t' \geq t$ in favor of students with higher priority. Let $j$ be a student in $\mu_D(s)$; then $\text{priority}_{js} > \text{priority}_{is}$ (since $s$ rejected $i$ for $j$). This contradicts the assumption that $i \succ_s j$, so no blocking pair exists and $\mu_D$ is stable.
\end{proof}

\subsection*{A.2 Proof of Strategy-Proofness of Student-Proposing DA}

\begin{proposition}[Strategy-Proofness]
\label{prop:sp}
Under student-proposing DA, truthful preference reporting is a dominant strategy for every student.
\end{proposition}

\begin{proof}
Fix the reports of all other students $\succ_{-i}$. We show that for any misreport $\succ_i'$, $\mu_D(\succ_i, \succ_{-i}) \succsim_i \mu_D(\succ_i', \succ_{-i})$.

Case 1: $\mu_D(\succ_i, \succ_{-i}) = \mu_D(\succ_i', \succ_{-i})$. Then the student is indifferent.

Case 2: $\mu_D(\succ_i', \succ_{-i}) \succ_i \mu_D(\succ_i, \succ_{-i})$. Let $s^* = \mu_D(\succ_i', \succ_{-i})$ and $s = \mu_D(\succ_i, \succ_{-i})$. Under truthful play, $i$ proposed to $s^*$ before $s$. School $s^*$ rejected $i$. Under the misreport, $i$ is matched to $s^*$; but this requires $s^*$ to hold $i$ throughout. Since the set of other students' proposals is the same in both runs (they report $\succ_{-i}$ in both), the students competing for $s^*$ are identical. Therefore $s^*$ holds $i$ under the misreport iff it holds $i$ under truthful play -- a contradiction. So Case 2 is impossible.
\end{proof}

\subsection*{A.3 Proof that Boston Mechanism is Manipulable}

\begin{proposition}[Boston Manipulability]
\label{prop:boston-manip}
The Boston mechanism is not strategy-proof: there exist preference profiles $(\succ_i, \succ_{-i})$ and misreports $\succ_i'$ such that $\mu_B(\succ_i', \succ_{-i}) \succ_i \mu_B(\succ_i, \succ_{-i})$.
\end{proposition}

\begin{proof}[Proof by example]
Consider two students $\{i, j\}$ and two schools $\{s, t\}$ each with capacity 1. True preferences: $i: s \succ t$, $j: s \succ t$. Priorities: $s$ ranks $j$ above $i$. Under truthful play, both apply to $s$ first; $s$ accepts $j$ and rejects $i$; $i$ applies to $t$ and is accepted. Under misreport $\succ_i': t \succ s$, student $i$ applies to $t$ first (no competition), gets $t$; student $j$ gets $s$. The outcomes are identical. Now consider: true preferences $i: s \succ t$, $j: t \succ s$. Under truthful play: $i$ gets $s$ (no competition), $j$ gets $t$. Under misreport $i': t \succ s$: both $i$ and $j$ apply to $t$; $t$ accepts $j$ (higher priority); $i$ applies to $s$, gets $s$. Again the same.

For a case where manipulation strictly helps: let true preferences be $i: s \succ t$, $j: s \succ t$, priority of $s$: $j > i$. Under truthful play $i$ ends up at $t$. Now if $i$ knows $j$ will apply to $s$ first-round, $i$ can safely report $\succ_i': s \succ t$ truncated to only $s$ -- but this is the same as truthful play. Alternatively, if there are three schools and $i$ can misreport to avoid competing at $s$, obtain their second choice at a school with no competition first-round, and $j$ does not fill it. This straightforward construction establishes that reporting preferences strategically can yield a weakly better assignment, with strict improvement possible.
\end{proof}

\subsection*{A.4 Rural Hospitals Theorem}

\begin{theorem}[Rural Hospitals Theorem]
\label{thm:rural-hospitals}
In any market with two-sided preferences, the set of agents matched and the number of positions filled at each hospital (school) are the same across all stable matchings.
\end{theorem}

\begin{proof}
Let $\mu$ and $\mu'$ be two stable matchings. For any school $s$, suppose $|\mu(s)| > |\mu'(s)|$. Then there exists a student $i \in \mu(s) \setminus \mu'(s)$. Under $\mu'$, $i$ is either unmatched or matched to $\mu'(i) \prec_i s$. In either case, $(i,s)$ is a blocking pair for $\mu'$ (since $s$ prefers $i$ to some student in $\mu'(s)$ by priority consistency), contradicting the stability of $\mu'$. Hence $|\mu(s)| = |\mu'(s)|$ for all $s$.
\end{proof}

\subsection*{A.5 Combinatorial Bounds on the Number of Stable Matchings}

\begin{lemma}[Counting Stable Matchings]
\label{lem:count-stable}
The number of distinct stable matchings satisfies:
\begin{align}
|\mathcal{M}_{\text{stable}}| \leq \binom{n + K - 1}{K} \cdot \prod_{s=1}^{K} \binom{n_s}{\lfloor q_s \rfloor},
\end{align}
where $n_s$ is the number of students who rank school $s$ and $q_s = \lceil c_s \rceil$ is the school capacity. The matching probability matrix is:
\begin{align}
\mathbf{P} = \begin{bmatrix} P_{11} & P_{12} & \cdots & P_{1K} \\ P_{21} & P_{22} & \cdots & P_{2K} \\ \vdots & \vdots & \ddots & \vdots \\ P_{n1} & P_{n2} & \cdots & P_{nK} \end{bmatrix}, \quad \sum_{s=1}^{K} P_{is} \leq 1,\; \sum_{i=1}^{n} P_{is} \leq \lfloor q_s \rfloor.
\end{align}
\end{lemma}
"""

    proof_block_20 = TableSpec(
        table_id="proofs-block",
        caption="",
        label="",
        latex=appendix_proofs_20,
    )

    # ── Sections ──
    sections_20 = [
        SectionSpec("Introduction", "sec:intro-20", text_paragraphs=14),
        SectionSpec("Institutional Background", "sec:background-20", text_paragraphs=12,
                    subsections=[
                        SectionSpec("The Centralized School Choice System", "sec:system-20", level=2,
                                    text_paragraphs=10),
                        SectionSpec("History of Mechanism Design", "sec:history-mech-20", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Data Sources and Sample Construction", "sec:data-mech-20", level=2,
                                    text_paragraphs=8, tables=[tab_student_summary, tab_school_chars]),
                    ]),
        SectionSpec("Matching Theory", "sec:theory-20", text_paragraphs=14,
                    equations=[eqs_20[0], eqs_20[1], eqs_20[2]],
                    subsections=[
                        SectionSpec("The Deferred Acceptance Algorithm", "sec:da-theory-20", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Stability and Strategy-Proofness", "sec:stability-sp-20", level=2,
                                    text_paragraphs=10, equations=[eqs_20[7], eqs_20[8]]),
                        SectionSpec("Welfare Criteria and Mechanism Comparison", "sec:welfare-theory-20", level=2,
                                    text_paragraphs=10, equations=[eqs_20[3], eqs_20[4], eqs_20[5]],
                                    tables=[tab_welfare]),
                    ]),
        SectionSpec("Data", "sec:data-20", text_paragraphs=12,
                    tables=[tab_pref, tab_da_results],
                    subsections=[
                        SectionSpec("Student and School Characteristics", "sec:chars-20", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Preference Distributions", "sec:pref-20", level=2,
                                    text_paragraphs=8),
                        SectionSpec("Matching Outcomes", "sec:outcomes-20", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Empirical Strategy", "sec:empirical-20", text_paragraphs=12,
                    equations=[eqs_20[6]],
                    subsections=[
                        SectionSpec("Regression Discontinuity at Admission Cutoffs", "sec:rdd-20", level=2,
                                    text_paragraphs=10, tables=[tab_rdd_cutoff]),
                        SectionSpec("Identification and Validity Checks", "sec:validity-20", level=2,
                                    text_paragraphs=10),
                    ]),
        SectionSpec("Results", "sec:results-20", text_paragraphs=12,
                    tables=[tab_rdd_test, tab_rdd_grad, tab_subgroup],
                    subsections=[
                        SectionSpec("Test Score Outcomes", "sec:test-scores-20", level=2,
                                    text_paragraphs=10),
                        SectionSpec("High School Graduation and College Enrollment", "sec:grad-college-20", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Heterogeneous Effects by Student Subgroup", "sec:subgroup-20", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Welfare Analysis", "sec:welfare-20", text_paragraphs=12,
                    tables=[tab_boston_da, tab_ttc_da],
                    subsections=[
                        SectionSpec("Counterfactual Mechanism Comparison", "sec:counterfactual-20", level=2,
                                    text_paragraphs=10),
                        SectionSpec("Distributional Welfare Effects", "sec:distrib-20", level=2,
                                    text_paragraphs=8),
                    ]),
        SectionSpec("Conclusion", "sec:conclusion-20", text_paragraphs=10),
        SectionSpec("Appendix A: Matching Theory Proofs", "sec:appendix-a-20", text_paragraphs=8),
        SectionSpec("Appendix B: DA Algorithm Details", "sec:appendix-b-20", text_paragraphs=6),
        SectionSpec("Appendix C: Additional Results", "sec:appendix-c-20", text_paragraphs=6,
                    tables=[tab_app_pref]),
    ]

    # inject proof block
    sections_20[8].tables.append(proof_block_20)

    bib_20 = [
        r"\bibitem{abdulkadiroglu2003} Abdulkadiroglu, A. and T. Sonmez (2003). ``School Choice: A Mechanism Design Approach.'' \textit{American Economic Review}, 93(3), 729--747.",
        r"\bibitem{gale1962} Gale, D. and L.S. Shapley (1962). ``College Admissions and the Stability of Marriage.'' \textit{American Mathematical Monthly}, 69(1), 9--15.",
        r"\bibitem{abdulkadiroglu2009} Abdulkadiroglu, A., P. Pathak, and A. Roth (2009). ``Strategy-Proofness versus Efficiency in Matching with Indifferences: Redesigning the NYC High School Match.'' \textit{American Economic Review}, 99(5), 1954--1978.",
        r"\bibitem{pathak2010} Pathak, P.A. and T. Sonmez (2008). ``Leveling the Playing Field: Sincere and Sophisticated Players in the Boston Mechanism.'' \textit{American Economic Review}, 98(4), 1636--1652.",
        r"\bibitem{calonico2014} Calonico, S., M.D. Cattaneo, and R. Titiunik (2014). ``Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs.'' \textit{Econometrica}, 82(6), 2295--2326.",
        r"\bibitem{roth1984} Roth, A.E. (1984). ``The Evolution of the Labor Market for Medical Interns and Residents: A Case Study in Game Theory.'' \textit{Journal of Political Economy}, 92(6), 991--1016.",
        r"\bibitem{hoxby2000} Hoxby, C.M. (2000). ``Does Competition Among Public Schools Benefit Students and Taxpayers?'' \textit{American Economic Review}, 90(5), 1209--1238.",
        r"\bibitem{shapley1974} Shapley, L. and H. Scarf (1974). ``On Cores and Indivisibility.'' \textit{Journal of Mathematical Economics}, 1(1), 23--37.",
    ]

    return PaperSpec(
        paper_id="20",
        field_slug="market-design",
        title="School Choice, Deferred Acceptance, and Student Outcomes: Evidence from a Centralized Admissions System",
        authors="Amara Diallo \\and Henrik Eriksson \\and Priya Nair",
        journal_style="restud",
        abstract=(
            "We study the welfare effects of switching from the Boston Immediate Acceptance mechanism "
            "to the Deferred Acceptance (DA) algorithm for school assignment in a large urban district. "
            "Using administrative data on 155,000 applicants across fourteen cohorts, we document "
            "that DA assigns 66 percent of students to their first-choice school -- 5 percentage "
            "points below the Boston mechanism under truthful play, but 7 percentage points above "
            "the Boston mechanism in Nash equilibrium with strategic behavior. Using regression "
            "discontinuity designs at school admission cutoffs, we estimate that attending an "
            "oversubscribed school improves 8th grade math scores by 0.30 standard deviations, "
            "reading by 0.20 standard deviations, high school graduation by 6.9 percentage points, "
            "and four-year college enrollment by 5.1 percentage points. Effects are largest for "
            "low-income students and English language learners. Counterfactual welfare analysis "
            "shows that DA achieves Pareto improvements over Boston for 12 percent of students, "
            "and that Top Trading Cycles achieves higher average welfare but at the cost of "
            "stability and justified envy."
        ),
        sections=sections_20,
        bibliography_entries=bib_20,
        target_pages=60,
        qa=[
            {"question": "What mechanisms are compared in this paper?",
             "answer": "Boston (Immediate Acceptance), student-proposing DA, and Top Trading Cycles (TTC)"},
            {"question": "What is the IV estimate of attending an oversubscribed school on math scores?",
             "answer": "0.30 standard deviations"},
            {"question": "Is student-proposing DA strategy-proof?",
             "answer": "Yes -- truthful preference reporting is a dominant strategy under DA"},
            {"question": "Which mechanism achieves higher average welfare, TTC or DA?",
             "answer": "TTC achieves higher average welfare (0.761 vs 0.742), but TTC is not stable"},
            {"question": "What is the graduation rate for students just below the admission cutoff?",
             "answer": "74.2%"},
        ],
    )


PAPER_BUILDERS["20"] = _paper_20_market_design
