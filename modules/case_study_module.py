"""
================================================================
CASE STUDY MODULE — UDR Analysis System
================================================================
Processes Component 3: In-depth case study of Student A.
Applies Formula F7 (UDR Coding Score) to both coding tasks.
Session: 4h15m face-to-face, April 2026.
================================================================
"""

from modules.formula_engine import F7_udr_coding_score


# UDR indicator labels (4 per domain)
UDR_INDICATORS = {
    'Understanding': [
        'Can explain what the code does',
        'Can explain why specific constructs were used',
        'Can describe program behavior under different inputs',
        'Can relate code structure to the problem requirements',
    ],
    'Debugging': [
        'Reads error messages analytically',
        'Forms hypotheses about failure causes',
        'Traces execution to locate the error',
        'Applies fix and verifies correctness independently',
    ],
    'Reasoning': [
        'Plans logic before writing code',
        'Anticipates edge cases',
        'Verifies correctness through mental execution',
        'Can explain algorithmic approach before coding',
    ],
}


def analyze_case_study(claimed_confidence,
                       task_a_u, task_a_d, task_a_r,
                       task_b_u, task_b_d, task_b_r,
                       dependency_level,
                       explain_ai_code,
                       used_ai_before_thinking):
    """
    Analyze case study data using Formula F7.

    Parameters:
        claimed_confidence (int):      self-reported AI use % (from interview)
        task_a_u (int):               Task A Understanding indicators (0-4)
        task_a_d (int):               Task A Debugging indicators (0-4)
        task_a_r (int):               Task A Reasoning indicators (0-4)
        task_b_u (int):               Task B Understanding indicators (0-4)
        task_b_d (int):               Task B Debugging indicators (0-4)
        task_b_r (int):               Task B Reasoning indicators (0-4)
        dependency_level (int):        AI dependency level (1-10)
        explain_ai_code (bool):        could explain AI-generated code
        used_ai_before_thinking (bool):used AI before attempting independently

    Returns:
        dict: all F7 scores, gap analysis, and RQ answers
    """
    # F7 applied to Task A (without AI)
    a_u = F7_udr_coding_score(task_a_u)
    a_d = F7_udr_coding_score(task_a_d)
    a_r = F7_udr_coding_score(task_a_r)
    a_avg = round((a_u + a_d + a_r) / 3, 1)

    # F7 applied to Task B (with AI)
    b_u = F7_udr_coding_score(task_b_u)
    b_d = F7_udr_coding_score(task_b_d)
    b_r = F7_udr_coding_score(task_b_r)
    b_avg = round((b_u + b_d + b_r) / 3, 1)

    # Illusory competence gap
    # claimed_confidence = stated self-reliance % (80 = 80% self, 20% AI)
    # observed = actual UDR performance without AI
    illusory_gap = round(claimed_confidence - a_avg, 1)

    # Classification
    if dependency_level >= 7 or (used_ai_before_thinking and a_avg < 30):
        classification = "Unguided / dependent AI user"
    elif dependency_level >= 4:
        classification = "Mixed AI user"
    else:
        classification = "Guided AI user"

    # Most affected domain in Task A
    task_a_domains = {'Understanding': a_u, 'Debugging': a_d, 'Reasoning': a_r}
    most_affected = min(task_a_domains, key=task_a_domains.get)

    # Illusory competence detection
    illusory_detected = illusory_gap >= 30

    return {
        # Task A — without AI (F7)
        'task_a_understanding': a_u,
        'task_a_debugging':     a_d,
        'task_a_reasoning':     a_r,
        'task_a_average':       a_avg,
        # Task B — with AI (F7)
        'task_b_understanding': b_u,
        'task_b_debugging':     b_d,
        'task_b_reasoning':     b_r,
        'task_b_average':       b_avg,
        # Gap analysis
        'claimed_confidence':       claimed_confidence,
        'illusory_gap':             illusory_gap,
        'illusory_competence':      'Detected' if illusory_detected else 'Not strongly detected',
        'classification':           classification,
        'dependency_level':         dependency_level,
        'most_affected_domain':     most_affected,
        'explain_ai_code':          explain_ai_code,
        'used_ai_before_thinking':  used_ai_before_thinking,
        # RQ answers
        'rq1_answer': f"Task A UDR scores: U={a_u}%, D={a_d}%, R={a_r}% — all domains show AI dependency impact",
        'rq2_answer': f"Most affected domain (Task A): {most_affected} ({task_a_domains[most_affected]}%)",
        'rq3_answer': f"Illusory competence gap = {illusory_gap} pts ({claimed_confidence}% claimed vs {a_avg}% observed) — {('Detected' if illusory_detected else 'Not strongly detected')}",
        'rq4_answer': f"Classification: {classification}. Used AI before thinking: {used_ai_before_thinking}. Can explain AI code: {explain_ai_code}",
    }


def analyze_case_study_demo():
    """
    Demo using Student A's verified thesis values.
    Claimed confidence = 80 (Student A stated 80% self-reliance)
    Task A = 0 indicators in all domains (UDR score = 0%)
    Task B = 1 Reasoning indicator present (25%)
    Dependency level = 9/10
    """
    return analyze_case_study(
        claimed_confidence=80,
        task_a_u=0, task_a_d=0, task_a_r=0,
        task_b_u=0, task_b_d=0, task_b_r=1,
        dependency_level=9,
        explain_ai_code=False,
        used_ai_before_thinking=True
    )
