"""
================================================================
REPORT GENERATOR — UDR Analysis System
================================================================
Produces a structured results report that explicitly answers
RQ1-RQ4 and lists all formula outputs.
================================================================
"""

from datetime import datetime


def generate_text_report(observation, survey, case_study, final):
    """
    Generate a full structured results report.
    Explicitly answers RQ1-RQ4 using formula outputs.
    Returns report as string and saves to outputs/results_report.txt
    """
    import os
    os.makedirs('outputs', exist_ok=True)

    lines = []
    w = lines.append

    w('=' * 65)
    w('  UDR ANALYSIS SYSTEM — RESULTS REPORT')
    w(f'  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    w(f'  Thesis: Analysing the Impact of AI-Assisted Coding Tools')
    w(f'  Author: Abdelrahman Sabry Abdalla Ali Abada Belal')
    w(f'  Beykoz University — Computer Engineering MSc, May 2026')
    w('=' * 65)

    w('')
    w('── INPUT DATA SUMMARY ──────────────────────────────────────')
    w(f'  Component 1 — Observation:  {observation.get("students",0)} students, {observation.get("sessions",0)} sessions')
    w(f'  Component 2 — Survey:       {survey.get("n",0)} responses (JotForm, April 2026)')
    w(f'  Component 3 — Case Study:   Student A, 4h15m session, April 2026')

    w('')
    w('── FORMULA OUTPUTS ─────────────────────────────────────────')
    n = survey.get('n', 23)

    w(f'  F1 Relative Frequency:')
    w(f'    Daily AI use:            {survey.get("freq",{}).get("daily",0)}/{n} = {survey.get("daily_pct",0)}%')
    w(f'    Weekly AI use:           {survey.get("freq",{}).get("weekly",0)}/{n} = {survey.get("weekly_pct",0)}%')
    w(f'    Daily+Weekly combined:   {survey.get("daily_weekly_pct",0)}%')

    w(f'  F2 Likert Agreement Scores:')
    w(f'    Q10 (explain concepts):  {survey.get("q10_n",0)}/{n} = {survey.get("q10_pct",0)}%')
    w(f'    Q11 (write without AI):  {survey.get("q11_n",0)}/{n} = {survey.get("q11_pct",0)}%')
    w(f'    Q16 (debug without AI):  {survey.get("q16_n",0)}/{n} = {survey.get("q16_pct",0)}%')
    w(f'    Q17 (AI-first Likert):   {survey.get("q17_n",0)}/{n} = {survey.get("q17_pct",0)}%')
    w(f'    Q18 (trace execution):   {survey.get("q18_n",0)}/{n} = {survey.get("q18_pct",0)}%')
    w(f'    Q19 (redo without AI):   {survey.get("q19_n",0)}/{n} = {survey.get("q19_pct",0)}%')
    w(f'    Q23 (struggle without):  {survey.get("q23_n",0)}/{n} = {survey.get("q23_pct",0)}%')
    w(f'    Q24 (passing w/o learn): {survey.get("q24_n",0)}/{n} = {survey.get("q24_pct",0)}%')
    w(f'    Q34 (want AI course):    {survey.get("q34_n",0)}/{n} = {survey.get("q34_pct",0)}%')

    w(f'  F2b Disagreement Score:')
    w(f'    Q32 (no AI training):    {survey.get("q32_n",0)}/{n} = {survey.get("q32_pct",0)}%')

    w(f'  F3 Competence Perception Gap:')
    w(f'    G_competence = {survey.get("q10_pct",0)}% - {survey.get("q11_pct",0)}% = {survey.get("g_competence",0)} pts')

    w(f'  F4 Social Desirability Gap:')
    w(f'    Q14 AI-first (direct):   {survey.get("q14_ai_n",0)}/{n} = {survey.get("q14_ai_pct",0)}%')
    w(f'    G_SDB = {survey.get("q17_pct",0)}% - {survey.get("q14_ai_pct",0)}% = {survey.get("g_sdb",0)} pts')

    w(f'  F5 Institutional Gap:')
    w(f'    Supply (D(Q32)):         {survey.get("institutional_supply",0)}%')
    w(f'    Demand (A(Q34)):         {survey.get("institutional_demand",0)}%')

    w(f'  F6 Triangulation Validity:')
    w(f'    Finding 1 (AI dependency):      {"VALID" if final.get("finding1_ai_dependency_valid") else "NOT VALID"}')
    w(f'    Finding 2 (Illusory competence):{"VALID" if final.get("finding2_illusory_competence_valid") else "NOT VALID"}')
    w(f'    Finding 3 (Debugging affected): {"VALID" if final.get("finding3_debugging_affected_valid") else "NOT VALID"}')
    w(f'    Finding 4 (Institutional fail): {"VALID" if final.get("finding4_institutional_failure_valid") else "NOT VALID"}')

    w(f'  F7 UDR Coding Score — Student A:')
    w(f'    Task A (without AI):')
    w(f'      Understanding: {case_study.get("task_a_understanding",0)}%  Debugging: {case_study.get("task_a_debugging",0)}%  Reasoning: {case_study.get("task_a_reasoning",0)}%')
    w(f'      Average: {case_study.get("task_a_average",0)}%')
    w(f'    Task B (with AI):')
    w(f'      Understanding: {case_study.get("task_b_understanding",0)}%  Debugging: {case_study.get("task_b_debugging",0)}%  Reasoning: {case_study.get("task_b_reasoning",0)}%')
    w(f'      Average: {case_study.get("task_b_average",0)}%')
    w(f'    Illusory competence gap: {case_study.get("illusory_gap",0)} pts — {case_study.get("illusory_competence","N/A")}')
    w(f'    Classification: {case_study.get("classification","N/A")}')

    w('')
    w('=' * 65)
    w('  ANSWERS TO RESEARCH QUESTIONS (RQ1-RQ4)')
    w('=' * 65)
    w('')
    w(final.get('rq1', ''))
    w('')
    w(final.get('rq2', ''))
    w('')
    w(final.get('rq3', ''))
    w('')
    w(final.get('rq4', ''))
    w('')
    w('=' * 65)
    w('  OBSERVATION COMPONENT SUMMARY')
    w('=' * 65)
    w(f'  AI dependency rate:        {observation.get("ai_dependency_rate",0)}%')
    w(f'  Explanation failure rate:  {observation.get("explanation_failure_rate",0)}%')
    w(f'  Debugging weakness rate:   {observation.get("debugging_weakness_rate",0)}%')
    w(f'  Reasoning weakness rate:   {observation.get("reasoning_weakness_rate",0)}%')
    w(f'  Institutional gap rate:    {observation.get("institutional_gap_rate",0)}%')
    w(f'  Most affected domain:      {observation.get("most_affected_domain","N/A")}')
    w('')
    w('=' * 65)

    report_text = '\n'.join(lines)

    with open('outputs/results_report.txt', 'w', encoding='utf-8') as f:
        f.write(report_text)

    return report_text
