"""
================================================================
UDR ANALYSIS SYSTEM — Streamlit Web App
================================================================
Title:   Analysing the Impact of AI-Assisted Coding Tools on
         Programming Skill Development
Author:  Abdelrahman Sabry Abdalla Ali Abada Belal
Univ:    Beykoz University — Computer Engineering MSc
Date:    May 2026
Advisor: Prof. Dr. Abdurazzag Ali A. Aburas

USAGE (local):  streamlit run app.py
DEPLOY:         Streamlit Cloud → point at udr_webapp/app.py
================================================================
"""

import os
import sys
import tempfile

import streamlit as st

# Ensure modules/ is importable regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.observation_module  import analyze_observation, analyze_observation_demo
from modules.survey_module       import analyze_survey, analyze_survey_demo
from modules.case_study_module   import analyze_case_study, analyze_case_study_demo
from modules.triangulation_module import triangulate
from modules.report_generator    import generate_text_report
from modules.visualization       import (
    plot_ai_frequency, plot_udr_profile, plot_debugging_gap,
    plot_illusory_competence, plot_institutional_gap,
)

# ── Page configuration ─────────────────────────────────────────
st.set_page_config(
    page_title="UDR Analysis System — Beykoz University",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state initialisation ──────────────────────────────
for _k in ('obs_results', 'surv_results', 'case_results',
           'final', '_last_obs', '_last_surv', '_last_case', 'fig_paths'):
    if _k not in st.session_state:
        st.session_state[_k] = {} if _k not in ('fig_paths',) else []

# ── Header ─────────────────────────────────────────────────────
st.title("UDR Research Analysis System")
st.markdown(
    "**Analysing the Impact of AI-Assisted Coding Tools on "
    "Programming Skill Development**"
)
st.caption(
    "Abdelrahman Sabry Abdalla Ali Abada Belal  ·  "
    "Beykoz University — Computer Engineering MSc  ·  May 2026"
)
st.divider()

# ── Tabs ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Component 1 — Observation",
    "📊  Component 2 — Survey",
    "🔬  Component 3 — Case Study",
    "📈  Integrated Results (RQ1–RQ4)",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — OBSERVATION
# ══════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Component 1 — Participant Observation Input")
    st.caption(
        "Enter the counts observed during the 3-month engagement.  "
        "Formula F1: P(i) = (f(i) / n) × 100"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        o_students = st.number_input("Total students in cohort",          1, 200, 20, key="o_stu")
        o_sessions = st.number_input("Number of sessions",                1, 100,  7, key="o_ses")
        o_ai_first = st.number_input("Students using AI as first resort", 0, 200, 18, key="o_ai")
        o_unable   = st.number_input("Students unable to explain code",   0, 200, 16, key="o_un")
    with col_b:
        o_debug    = st.number_input("Students with debugging weakness",  0, 200, 17, key="o_db")
        o_reason   = st.number_input("Students with reasoning weakness",  0, 200, 16, key="o_re")
        o_passed   = st.number_input("Students passed despite deficits",  0, 200, 20, key="o_pa")
        o_drop     = st.number_input("Students with motivation decline",  0, 200, 12, key="o_dr")

    if st.button("Analyze Observation Data (F1)", type="primary", key="btn_obs"):
        st.session_state['obs_results'] = analyze_observation(
            int(o_students), int(o_sessions), int(o_ai_first), int(o_unable),
            int(o_debug),    int(o_reason),   int(o_passed),   int(o_drop),
        )

    r = st.session_state['obs_results']
    if r:
        st.success("✓  Observation analysis complete")

        st.markdown("#### UDR Domain Rates (F1)")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("AI dependency rate",       f"{r['ai_dependency_rate']}%")
        m2.metric("Explanation failure rate", f"{r['explanation_failure_rate']}%",
                  help="Understanding domain")
        m3.metric("Debugging weakness rate",  f"{r['debugging_weakness_rate']}%",
                  help="Debugging domain — RQ2")
        m4.metric("Reasoning weakness rate",  f"{r['reasoning_weakness_rate']}%",
                  help="Reasoning domain")

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("Students observed",       str(r['students']))
        m6.metric("Sessions conducted",      str(r['sessions']))
        m7.metric("Institutional gap rate",  f"{r['institutional_gap_rate']}%")
        m8.metric("Motivation decline rate", f"{r['attendance_decline_rate']}%")

        st.markdown("#### RQ Answers from Component 1")
        for k in ('rq1_answer', 'rq2_answer', 'rq3_answer', 'rq4_answer'):
            st.info(r[k])


# ══════════════════════════════════════════════════════════════
# TAB 2 — SURVEY
# ══════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Component 2 — Survey Data Analysis")
    st.caption(
        "Load your JotForm CSV export or use demo data.  "
        "Formulas F1, F2, F2b, F3, F4, F5 are applied automatically."
    )

    use_demo     = st.checkbox("Use demo data (thesis-verified values, n = 23)", value=True)
    uploaded_csv = None
    if not use_demo:
        uploaded_csv = st.file_uploader("Upload JotForm CSV export", type=["csv"])

    if st.button("Run Survey Analysis (F1–F5)", type="primary", key="btn_surv"):
        if use_demo or uploaded_csv is None:
            st.session_state['surv_results'] = analyze_survey_demo()
            if not use_demo:
                st.warning("No CSV uploaded — using demo data.")
        else:
            with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="wb") as tmp:
                tmp.write(uploaded_csv.read())
                tmp_path = tmp.name
            try:
                st.session_state['surv_results'] = analyze_survey(tmp_path)
                st.success(f"CSV loaded: {uploaded_csv.name}")
            except Exception as exc:
                st.error(f"CSV error: {exc}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    r = st.session_state['surv_results']
    if r:
        st.success("✓  Survey analysis complete")
        n = r['n']

        st.markdown(f"**Responses: n = {n}**")

        st.markdown("#### F1 — Relative Frequency")
        c1, c2, c3 = st.columns(3)
        c1.metric("Daily AI use",         f"{r['daily_pct']}%",
                  f"{r['freq'].get('daily',0)}/{n} respondents")
        c2.metric("Weekly AI use",        f"{r['weekly_pct']}%",
                  f"{r['freq'].get('weekly',0)}/{n} respondents")
        c3.metric("Daily + Weekly (RQ1)", f"{r['daily_weekly_pct']}%",
                  help="Combined F1 result — answers RQ1")

        st.markdown("#### F2 — Likert Agreement Scores")
        f2_items = [
            ("Q10 — Explain concepts (U)", r['q10_pct'], r['q10_n']),
            ("Q11 — Write without AI (U)", r['q11_pct'], r['q11_n']),
            ("Q16 — Debug without AI (D)", r['q16_pct'], r['q16_n']),
            ("Q17 — AI-first Likert (D)",  r['q17_pct'], r['q17_n']),
            ("Q18 — Trace execution (R)",  r['q18_pct'], r['q18_n']),
            ("Q19 — Redo without AI (R)",  r['q19_pct'], r['q19_n']),
            ("Q24 — Passing w/o learning", r['q24_pct'], r['q24_n']),
        ]
        cols = st.columns(len(f2_items))
        for col, (label, pct, count) in zip(cols, f2_items):
            col.metric(label, f"{pct}%", f"{count}/{n}")

        st.markdown("#### F2b — Likert Disagreement  |  F3, F4, F5 — Gaps")
        g1, g2, g3, g4, g5 = st.columns(5)
        g1.metric("F2b — Q32 No AI training",     f"{r['q32_pct']}%",
                  f"{r['q32_n']}/{n}",
                  help="D(Q32) — used for F5 supply gap")
        g2.metric("F3 — Competence gap",           f"{r['g_competence']} pts",
                  help="G = A(Q10) − A(Q11)")
        g3.metric("F4 — Social desirability gap",  f"{r['g_sdb']} pts",
                  help="G_SDB = A(Q17) − P_AI(Q14)")
        g4.metric("F5 — Institutional supply",     f"{r['institutional_supply']}%",
                  help="D(Q32)")
        g5.metric("F5 — Institutional demand",     f"{r['institutional_demand']}%",
                  help="A(Q34)")

        st.markdown("#### Figures")
        if st.button("Generate All 5 Figures", key="btn_figs"):
            with st.spinner("Rendering figures…"):
                st.session_state['fig_paths'] = [
                    plot_ai_frequency(r),
                    plot_udr_profile(r),
                    plot_debugging_gap(r),
                    plot_illusory_competence(r),
                    plot_institutional_gap(r),
                ]

        if st.session_state['fig_paths']:
            paths = st.session_state['fig_paths']
            captions = [
                "Figure 1 — AI Tool Use Frequency (F1)",
                "Figure 2 — UDR Self-Assessment Profile (F2, F3)",
                "Figure 3 — Debugging Behavior Contradiction (F4)",
                "Figure 4 — Illusory Competence Cluster (F3)",
                "Figure 5 — Institutional Supply-Demand Gap (F5)",
            ]
            fc1, fc2 = st.columns(2)
            for i, (path, cap) in enumerate(zip(paths, captions)):
                col = fc1 if i % 2 == 0 else fc2
                with col:
                    st.image(path, caption=cap, use_container_width=True)
                    with open(path, 'rb') as fh:
                        st.download_button(
                            f"Download {cap[:8]}…",
                            data=fh,
                            file_name=os.path.basename(path),
                            mime="image/png",
                            key=f"dl_fig_{i}",
                        )


# ══════════════════════════════════════════════════════════════
# TAB 3 — CASE STUDY
# ══════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Component 3 — Case Study UDR Assessment (Student A)")
    st.caption(
        "Enter UDR indicator counts (0–4 per domain).  "
        "Formula F7: UDR_score(d) = (indicators_present / 4) × 100"
    )

    st.markdown("##### Interview — Claimed AI use behavior")
    claimed = st.number_input(
        "Claimed self-reliance % (Student A stated 80% self, 20% AI)",
        0, 100, 80, key="c_claimed",
    )

    st.markdown("##### Task A — WITHOUT AI (isPrime program)")
    ca1, ca2, ca3 = st.columns(3)
    ta_u = ca1.number_input("Understanding indicators (0–4)", 0, 4, 0, key="ta_u")
    ta_d = ca2.number_input("Debugging indicators (0–4)",     0, 4, 0, key="ta_d")
    ta_r = ca3.number_input("Reasoning indicators (0–4)",     0, 4, 0, key="ta_r")

    st.markdown("##### Task B — WITH AI (string-reversal bugfix)")
    cb1, cb2, cb3 = st.columns(3)
    tb_u = cb1.number_input("Understanding indicators (0–4)", 0, 4, 0, key="tb_u")
    tb_d = cb2.number_input("Debugging indicators (0–4)",     0, 4, 0, key="tb_d")
    tb_r = cb3.number_input(
        "Reasoning indicators (0–4)", 0, 4, 1, key="tb_r",
        help="Task B: 1 partial indicator present",
    )

    st.markdown("##### Behavioral Observations")
    dep = st.slider("AI dependency level (1–10)", 1, 10, 9, key="c_dep")
    bc1, bc2 = st.columns(2)
    ai_before  = bc1.radio(
        "Used AI before thinking independently?", ["Yes", "No"], index=0, key="c_aib",
        help="Task B: photographed task, sent to ChatGPT",
    )
    explain_ai = bc2.radio(
        "Could explain AI-generated code fixes?", ["Yes", "No"], index=1, key="c_exp",
        help="Task B debrief: could not explain bugs",
    )

    if st.button("Analyze Case Study (F7)", type="primary", key="btn_case"):
        st.session_state['case_results'] = analyze_case_study(
            int(claimed),
            int(ta_u), int(ta_d), int(ta_r),
            int(tb_u), int(tb_d), int(tb_r),
            int(dep),
            explain_ai == "Yes",
            ai_before  == "Yes",
        )

    r = st.session_state['case_results']
    if r:
        st.success("✓  Case study analysis complete")

        st.markdown("#### Task A (without AI) — F7 Scores")
        ma1, ma2, ma3, ma4 = st.columns(4)
        ma1.metric("Understanding", f"{r['task_a_understanding']}%")
        ma2.metric("Debugging",     f"{r['task_a_debugging']}%")
        ma3.metric("Reasoning",     f"{r['task_a_reasoning']}%")
        ma4.metric("Average UDR",   f"{r['task_a_average']}%")

        st.markdown("#### Task B (with AI) — F7 Scores")
        mb1, mb2, mb3, mb4 = st.columns(4)
        mb1.metric("Understanding", f"{r['task_b_understanding']}%")
        mb2.metric("Debugging",     f"{r['task_b_debugging']}%")
        mb3.metric("Reasoning",     f"{r['task_b_reasoning']}%")
        mb4.metric("Average UDR",   f"{r['task_b_average']}%")

        st.markdown("#### Illusory Competence Gap (F7 + F3)")
        mg1, mg2, mg3, mg4 = st.columns(4)
        mg1.metric("Claimed confidence",    f"{r['claimed_confidence']}%")
        mg2.metric("Observed (Task A avg)", f"{r['task_a_average']}%")
        mg3.metric("Illusory gap",          f"{r['illusory_gap']} pts")
        mg4.metric("Classification",         r['classification'])

        st.markdown("#### RQ Answers from Component 3")
        for k in ('rq1_answer', 'rq2_answer', 'rq3_answer', 'rq4_answer'):
            st.info(r[k])


# ══════════════════════════════════════════════════════════════
# TAB 4 — INTEGRATED RESULTS
# ══════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Integrated Findings — Formula F6 Triangulation (RQ1–RQ4)")
    st.caption(
        "Run all three components first (or use demo data), "
        "then click Generate to triangulate findings."
    )

    missing = []
    if not st.session_state['obs_results']:
        missing.append("Component 1 (Observation)")
    if not st.session_state['surv_results']:
        missing.append("Component 2 (Survey)")
    if not st.session_state['case_results']:
        missing.append("Component 3 (Case Study)")
    if missing:
        st.info(
            f"Not yet run: **{', '.join(missing)}** — "
            "demo values will be used for any missing component."
        )

    if st.button("Generate Integrated Results (F6)", type="primary", key="btn_final"):
        obs  = st.session_state['obs_results']  or analyze_observation_demo()
        surv = st.session_state['surv_results'] or analyze_survey_demo()
        case = st.session_state['case_results'] or analyze_case_study_demo()

        st.session_state['final']      = triangulate(obs, surv, case)
        st.session_state['_last_obs']  = obs
        st.session_state['_last_surv'] = surv
        st.session_state['_last_case'] = case

    final = st.session_state.get('final')
    if final:
        st.success("✓  Triangulation complete")

        # ── F6 validity ───────────────────────────────────────
        st.markdown("#### Formula F6 — Triangulation Validity")
        st.caption("Finding is valid when C1 ∧ C2 ∧ C3 — all three components confirm it")

        findings = [
            ("Finding 1\nAI dependency as default",   final['finding1_ai_dependency_valid']),
            ("Finding 2\nIllusory competence gap",    final['finding2_illusory_competence_valid']),
            ("Finding 3\nDebugging most affected",    final['finding3_debugging_affected_valid']),
            ("Finding 4\nDual institutional failure", final['finding4_institutional_failure_valid']),
        ]
        f_cols = st.columns(4)
        for col, (label, valid) in zip(f_cols, findings):
            col.metric(label, "VALID ✓" if valid else "NOT VALID ✗")

        if final['all_findings_valid']:
            st.success("All 4 findings valid — thesis findings confirmed via F6")
        else:
            st.warning("Not all findings valid — check component data")

        # ── RQ answers ────────────────────────────────────────
        st.markdown("#### Research Questions — Answers from System Output")
        for key, label in (('rq1','RQ1'), ('rq2','RQ2'), ('rq3','RQ3'), ('rq4','RQ4')):
            with st.expander(label, expanded=True):
                st.write(final[key])

        # ── Key metrics ───────────────────────────────────────
        st.markdown("#### Key Metrics Summary")
        km1, km2, km3, km4 = st.columns(4)
        km1.metric("Survey responses (n)",         str(final['survey_n']))
        km2.metric("Daily+weekly AI use (F1)",     f"{final['daily_weekly_pct']}%")
        km3.metric("Competence gap (F3)",          f"{final['g_competence']} pts")
        km4.metric("Social desirability gap (F4)", f"{final['g_sdb']} pts")

        km5, km6, km7, km8 = st.columns(4)
        km5.metric("Cohort students",              str(final['obs_students']))
        km6.metric("Institutional supply gap (F5)",f"{final['institutional_supply']}%")
        km7.metric("Institutional demand (F5)",    f"{final['institutional_demand']}%")
        km8.metric("Case study illusory gap",      f"{final['illusory_gap']} pts")

        # ── Export ────────────────────────────────────────────
        st.markdown("#### Export")
        report_text = generate_text_report(
            st.session_state['_last_obs'],
            st.session_state['_last_surv'],
            st.session_state['_last_case'],
            final,
        )
        st.download_button(
            label="📥  Download Full Results Report (.txt)",
            data=report_text,
            file_name="udr_results_report.txt",
            mime="text/plain",
            key="dl_report",
        )
