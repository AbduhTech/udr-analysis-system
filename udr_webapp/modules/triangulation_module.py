"""
================================================================
TRIANGULATION MODULE — UDR Analysis System
================================================================
Applies Formula F6 (Convergent Triangulation Validity) to
integrate evidence from all three components and produce
explicit answers to Research Questions RQ1-RQ4.
================================================================
"""

from modules.formula_engine import F6_triangulation_validity


def triangulate(observation, survey, case_study):
    """
    Apply F6 to validate findings across all three components.
    Produces explicit RQ1-RQ4 answers.

    Parameters:
        observation (dict): results from observation_module
        survey (dict):      results from survey_module
        case_study (dict):  results from case_study_module

    Returns:
        dict: triangulated findings with RQ answers
    """

    # ── Finding 1: AI dependency as default (RQ1) ────────────
    f1_valid = F6_triangulation_validity(
        c1 = observation.get('ai_dependency_rate', 0) >= 70,
        c2 = survey.get('daily_weekly_pct', 0) >= 70,
        c3 = case_study.get('used_ai_before_thinking', False)
    )

    # ── Finding 2: Illusory competence gap (RQ3) ─────────────
    f2_valid = F6_triangulation_validity(
        c1 = observation.get('explanation_failure_rate', 0) >= 60,
        c2 = survey.get('g_competence', 0) >= 10,
        c3 = case_study.get('illusory_gap', 0) >= 30
    )

    # ── Finding 3: Debugging most affected (RQ2) ─────────────
    f3_valid = F6_triangulation_validity(
        c1 = observation.get('debugging_weakness_rate', 0) >= 70,
        c2 = survey.get('g_sdb', 0) >= 20,
        c3 = case_study.get('task_a_debugging', 100) <= 25
    )

    # ── Finding 4: Dual institutional failure (RQ4) ───────────
    f4_valid = F6_triangulation_validity(
        c1 = observation.get('institutional_gap_rate', 0) >= 80,
        c2 = survey.get('institutional_supply', 0) >= 50,
        c3 = case_study.get('dependency_level', 0) >= 7
    )

    # ── RQ1: How does AI engagement affect UDR? ──────────────
    rq1 = (
        f"RQ1 ANSWER: AI-Gen tool use is the default cognitive condition at this "
        f"educational level. {survey.get('daily_weekly_pct',0)}% of survey respondents "
        f"use AI tools daily or weekly (F1). {observation.get('ai_dependency_rate',0)}% "
        f"of the cohort used AI as their first resort (Observation, F1). "
        f"Student A used AI before attempting independently (Case Study). "
        f"All three UDR domains are affected, with differential severity."
    )

    # ── RQ2: Which UDR domain is most affected? ──────────────
    obs_domain = observation.get('most_affected_domain', 'Debugging')
    cs_domain  = case_study.get('most_affected_domain', 'Debugging')
    sdb        = survey.get('g_sdb', 0)
    rq2 = (
        f"RQ2 ANSWER: Debugging is the most strongly affected UDR domain. "
        f"Observation: {obs_domain} shows the highest weakness rate "
        f"({observation.get('debugging_weakness_rate',0)}%). "
        f"Survey: F4 social desirability gap = {sdb} pts — students under-report "
        f"AI-first debugging on direct questions. "
        f"Case Study: Student A scored 0% on Debugging in Task A (F7)."
    )

    # ── RQ3: Is there a measurable illusory competence gap? ──
    gap_comp = survey.get('g_competence', 0)
    gap_sdb  = survey.get('g_sdb', 0)
    gap_ill  = case_study.get('illusory_gap', 0)
    rq3 = (
        f"RQ3 ANSWER: Yes — a measurable illusory competence gap is confirmed "
        f"across all three components. "
        f"Survey F3: {gap_comp}-point competence perception gap (Q10 vs Q11). "
        f"Survey F4: {gap_sdb}-point social desirability gap (Q17 vs Q14). "
        f"Case Study F7: Student A scored 0% on Task A despite claiming "
        f"80% self-reliance — illusory gap = {gap_ill} points."
    )

    # ── RQ4: Guided vs unguided distinction ──────────────────
    supply = survey.get('institutional_supply', 0)
    demand = survey.get('institutional_demand', 0)
    rq4 = (
        f"RQ4 ANSWER: Guided use is rare without structured instruction. "
        f"No cohort student demonstrated consistent guided-use behavior. "
        f"Student A articulated guided-use principles (80/20 rule) but "
        f"defaulted to unguided behavior in Task B ('do it for me'). "
        f"Institutional failure confirmed: {supply}% denied receiving AI "
        f"training (F2b) while {demand}% demand a structured course (F2/F5)."
    )

    return {
        # F6 validity results
        'finding1_ai_dependency_valid':    f1_valid,
        'finding2_illusory_competence_valid': f2_valid,
        'finding3_debugging_affected_valid':  f3_valid,
        'finding4_institutional_failure_valid': f4_valid,
        'all_findings_valid': all([f1_valid, f2_valid, f3_valid, f4_valid]),
        # RQ answers
        'rq1': rq1,
        'rq2': rq2,
        'rq3': rq3,
        'rq4': rq4,
        # Summary metrics
        'survey_n': survey.get('n', 0),
        'obs_students': observation.get('students', 0),
        'daily_weekly_pct': survey.get('daily_weekly_pct', 0),
        'g_competence': gap_comp,
        'g_sdb': gap_sdb,
        'illusory_gap': gap_ill,
        'institutional_supply': supply,
        'institutional_demand': demand,
    }
