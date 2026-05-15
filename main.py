"""
================================================================
UDR ANALYSIS SYSTEM — MAIN CONSOLE RUNNER
================================================================
Title:   Analysing the Impact of AI-Assisted Coding Tools on
         Programming Skill Development
Author:  Abdelrahman Sabry Abdalla Ali Abada Belal
Univ:    Beykoz University — Computer Engineering MSc
Date:    May 2026
Advisor: Prof. Dr. Abdurazzag Ali A. Aburas

USAGE:
    python main.py                       # uses data/survey_data.csv
    python main.py data/my_survey.csv    # custom CSV path

OUTPUT:
    outputs/fig1_ai_frequency.png
    outputs/fig2_udr_profile.png
    outputs/fig3_debugging_gap.png
    outputs/fig4_illusory_competence.png
    outputs/fig5_institutional_gap.png
    outputs/results_report.txt
================================================================
"""

import sys
import os
from modules.observation_module import analyze_observation_demo
from modules.survey_module import analyze_survey, analyze_survey_demo
from modules.case_study_module import analyze_case_study_demo
from modules.triangulation_module import triangulate
from modules.visualization import generate_all_figures
from modules.report_generator import generate_text_report

DEFAULT_CSV = os.path.join('data', 'survey_data.csv')


def main():
    print()
    print('=' * 65)
    print('  UDR ANALYSIS SYSTEM')
    print('  Beykoz University — Computer Engineering MSc')
    print('  Thesis: AI-Assisted Coding & Programming Skill Development')
    print('=' * 65)
    print()

    # ── Load survey data ──────────────────────────────────────
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    print(f'STEP 1 — Loading survey data from: {csv_path}')
    if os.path.exists(csv_path):
        survey = analyze_survey(csv_path)
        print(f'  [OK] {survey["n"]} responses loaded successfully')
    else:
        print(f'  [WARN] CSV not found — using demo values')
        survey = analyze_survey_demo()
        print(f'  [OK] Demo survey data loaded ({survey["n"]} responses)')

    # ── Observation component ─────────────────────────────────
    print('\nSTEP 2 — Processing Component 1 (Observation)...')
    observation = analyze_observation_demo()
    print(f'  [OK] {observation["students"]} students, {observation["sessions"]} sessions')
    print(f'  AI dependency rate:       {observation["ai_dependency_rate"]}%')
    print(f'  Debugging weakness rate:  {observation["debugging_weakness_rate"]}%')
    print(f'  Institutional gap rate:   {observation["institutional_gap_rate"]}%')

    # ── Survey component ──────────────────────────────────────
    print('\nSTEP 3 — Applying Formulas F1-F5 to Survey Data...')
    print(f'  F1 Daily+weekly AI use:   {survey["daily_weekly_pct"]}%')
    print(f'  F2 Q10 (explain):         {survey["q10_pct"]}%')
    print(f'  F2 Q11 (write w/o AI):    {survey["q11_pct"]}%')
    print(f'  F2 Q16 (debug w/o AI):    {survey["q16_pct"]}%')
    print(f'  F2 Q17 (AI-first Likert): {survey["q17_pct"]}%')
    print(f'  F2b Q32 (no training):    {survey["q32_pct"]}%')
    print(f'  F3 Competence gap:        {survey["g_competence"]} pts')
    print(f'  F4 Social desirability:   {survey["g_sdb"]} pts')
    print(f'  F5 Institutional supply:  {survey["institutional_supply"]}%')
    print(f'  F5 Institutional demand:  {survey["institutional_demand"]}%')

    # ── Case study component ──────────────────────────────────
    print('\nSTEP 4 — Processing Component 3 (Case Study, F7)...')
    case_study = analyze_case_study_demo()
    print(f'  Task A (no AI): U={case_study["task_a_understanding"]}% D={case_study["task_a_debugging"]}% R={case_study["task_a_reasoning"]}%')
    print(f'  Task B (AI):    U={case_study["task_b_understanding"]}% D={case_study["task_b_debugging"]}% R={case_study["task_b_reasoning"]}%')
    print(f'  Illusory gap:   {case_study["illusory_gap"]} pts — {case_study["illusory_competence"]}')
    print(f'  Classification: {case_study["classification"]}')

    # ── Triangulation ─────────────────────────────────────────
    print('\nSTEP 5 — Applying Formula F6 (Triangulation Validity)...')
    final = triangulate(observation, survey, case_study)
    for key in ['finding1_ai_dependency_valid',
                'finding2_illusory_competence_valid',
                'finding3_debugging_affected_valid',
                'finding4_institutional_failure_valid']:
        label = key.replace('_valid','').replace('_',' ').title()
        status = 'VALID  ✓' if final[key] else 'NOT VALID  ✗'
        print(f'  {label:<40} {status}')
    print(f'  All findings valid: {final["all_findings_valid"]}')

    # ── Generate figures ──────────────────────────────────────
    print('\nSTEP 6 — Generating output figures...')
    try:
        paths = generate_all_figures(survey)
        for p in paths:
            print(f'  Saved: {p}')
    except Exception as e:
        print(f'  [WARN] Figure generation error: {e}')
        paths = []

    # ── Generate report ───────────────────────────────────────
    print('\nSTEP 7 — Saving results report...')
    generate_text_report(observation, survey, case_study, final)
    print('  Saved: outputs/results_report.txt')

    # ── RQ Summary ────────────────────────────────────────────
    print()
    print('=' * 65)
    print('  RESEARCH QUESTIONS — ANSWERS FROM SYSTEM OUTPUT')
    print('=' * 65)
    for rq in ['rq1','rq2','rq3','rq4']:
        print()
        for line in final[rq].split('. '):
            if line.strip():
                print(f'  {line.strip()}.')
    print()
    print('=' * 65)
    print('  ANALYSIS COMPLETE — All outputs saved to: outputs/')
    print('=' * 65)
    print()


if __name__ == '__main__':
    main()
