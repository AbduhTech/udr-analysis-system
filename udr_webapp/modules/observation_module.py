"""
================================================================
OBSERVATION MODULE — UDR Analysis System
================================================================
Processes Component 1: Participant-Observation data.
20 students, 7 sessions, 3 months (Dec 2025 - Mar 2026).
Applies F1 to compute all behavioral rates.
================================================================
"""

from modules.formula_engine import F1_relative_frequency


def analyze_observation(students, sessions, ai_first,
                        unable_explain, debug_weak,
                        reason_weak, passed_despite_deficits,
                        attendance_drop):
    """
    Analyze participant-observation data using Formula F1.

    Parameters:
        students (int):               total cohort size (20)
        sessions (int):               number of sessions (7)
        ai_first (int):               students using AI first
        unable_explain (int):         students unable to explain code
        debug_weak (int):             students with debugging weakness
        reason_weak (int):            students with reasoning weakness
        passed_despite_deficits (int):students who passed despite deficits
        attendance_drop (int):        students who declined/stopped

    Returns:
        dict: all computed rates and RQ mappings
    """
    ai_dep_rate   = F1_relative_frequency(ai_first, students)
    explain_rate  = F1_relative_frequency(unable_explain, students)
    debug_rate    = F1_relative_frequency(debug_weak, students)
    reason_rate   = F1_relative_frequency(reason_weak, students)
    inst_rate     = F1_relative_frequency(passed_despite_deficits, students)
    attend_rate   = F1_relative_frequency(attendance_drop, students)

    # Identify most affected UDR domain (RQ2)
    domain_rates = {
        'Understanding (explain failure)': explain_rate,
        'Debugging (weakness rate)':       debug_rate,
        'Reasoning (weakness rate)':       reason_rate,
    }
    most_affected = max(domain_rates, key=domain_rates.get)

    return {
        # Raw inputs
        'students': students,
        'sessions': sessions,
        # F1 outputs — RQ1
        'ai_dependency_rate':       ai_dep_rate,
        'explanation_failure_rate': explain_rate,
        'debugging_weakness_rate':  debug_rate,
        'reasoning_weakness_rate':  reason_rate,
        'institutional_gap_rate':   inst_rate,
        'attendance_decline_rate':  attend_rate,
        # RQ2 — most affected domain
        'most_affected_domain':     most_affected,
        'domain_rates':             domain_rates,
        # RQ answers
        'rq1_answer': f"AI dependency confirmed: {ai_dep_rate}% of students used AI as first resort",
        'rq2_answer': f"Most affected domain: {most_affected} ({domain_rates[most_affected]}%)",
        'rq3_answer': f"All {passed_despite_deficits}/{students} students passed despite documented UDR deficits",
        'rq4_answer': f"No guided-use behavior observed; {attend_rate}% showed motivational collapse",
    }


def analyze_observation_demo():
    """Demo using thesis-verified observation values."""
    return analyze_observation(
        students=20,
        sessions=7,
        ai_first=18,
        unable_explain=16,
        debug_weak=17,
        reason_weak=16,
        passed_despite_deficits=20,
        attendance_drop=12
    )
