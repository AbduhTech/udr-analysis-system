"""
================================================================
FORMULA ENGINE — UDR Analysis System
================================================================
Author:  Abdelrahman Sabry Abdalla Ali Abada Belal
Thesis:  Analysing the Impact of AI-Assisted Coding Tools on
         Programming Skill Development
Univ:    Beykoz University — Computer Engineering MSc
Date:    May 2026

All 7 analytical formulas (F1-F7) as defined in
Section 3.10.5 of the thesis.
================================================================
"""


def F1_relative_frequency(count, total):
    """
    FORMULA F1 - Relative Frequency
    P(i) = (f(i) / n) x 100
    Converts a raw count into a percentage of total respondents.
    Applied to every percentage figure in the analysis.
    """
    if total == 0:
        return 0.0
    return round((count / total) * 100, 1)


def F2_likert_agreement(responses):
    """
    FORMULA F2 - Likert Agreement Score
    A(q) = (f_SA(q) + f_A(q)) / n x 100
    Combines Agree and Strongly Agree responses into one
    agreement percentage. Supports English, Turkish, Arabic.
    """
    agree_kw = [
        'strongly agree', 'agree',
        'kesinlikle katiliyorum', 'katiliyorum',
        'kesinlikle katılıyorum', 'katılıyorum',
        'موافق بشدة', 'موافق'
    ]
    n = len(responses)
    count = 0
    for r in responses:
        v = r.strip().lower()
        if any(k in v for k in agree_kw):
            if 'disagree' not in v and 'katılmıyorum' not in v and 'katilmiyorum' not in v and 'غير' not in v:
                count += 1
    return F1_relative_frequency(count, n), count


def F2b_likert_disagreement(responses):
    """
    FORMULA F2b - Likert Disagreement Score
    D(q) = (f_SD(q) + f_D(q)) / n x 100
    Combines Disagree and Strongly Disagree responses.
    Used specifically for Q32 (no institutional AI training).
    """
    disagree_kw = [
        'strongly disagree', 'disagree',
        'kesinlikle katilmiyorum', 'katilmiyorum',
        'kesinlikle katılmıyorum', 'katılmıyorum',
        'غير موافق بشدة', 'غير موافق'
    ]
    n = len(responses)
    count = sum(1 for r in responses if any(k in r.strip().lower() for k in disagree_kw))
    return F1_relative_frequency(count, n), count


def F3_competence_gap(a_q12, a_q13):
    """
    FORMULA F3 - Competence Perception Gap
    G_competence = A(Q12) - A(Q13)
    Measures the divergence between perceived understanding
    and actual independent coding ability. Answers RQ3.
    """
    return round(a_q12 - a_q13, 1)


def F4_social_desirability_gap(a_q17, p_ai_q14):
    """
    FORMULA F4 - Social Desirability Gap
    G_SDB = A(Q17) - P_AI(Q14)
    Detects discrepancy between stated and actual debugging
    behavior. Answers RQ2 and RQ4.
    """
    return round(a_q17 - p_ai_q14, 1)


def F5_institutional_gap(d_q32, a_q34):
    """
    FORMULA F5 - Institutional Supply-Demand Gap
    G_inst = D(Q32) vs A(Q34)
    Compares percentage who deny receiving AI training
    against those who demand a structured AI course.
    """
    return round(d_q32, 1), round(a_q34, 1)


def F6_triangulation_validity(c1, c2, c3):
    """
    FORMULA F6 - Convergent Triangulation Validity
    Finding is valid when: C1 AND C2 AND C3 all support it
    A finding is robust when all three data sources converge.
    """
    return bool(c1 and c2 and c3)


def F7_udr_coding_score(indicators_present, total_indicators=4):
    """
    FORMULA F7 - UDR Observation Coding Score
    UDR_score(d) = (indicators_present / 4) x 100
    Scores Student A's observed performance on each UDR domain.
    Each domain has 4 binary behavioral indicators (0 or 1).
    Answers RQ1 and RQ2.
    """
    if total_indicators == 0:
        return 0.0
    return round((indicators_present / total_indicators) * 100, 1)
