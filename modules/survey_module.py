"""
================================================================
SURVEY MODULE — UDR Analysis System
================================================================
Reads real survey CSV data and applies Formulas F1-F5.
Column indices verified against actual JotForm export.
================================================================
"""

import csv
from modules.formula_engine import (
    F1_relative_frequency, F2_likert_agreement,
    F2b_likert_disagreement, F3_competence_gap,
    F4_debugging_displacement_gap, F5_institutional_gap
)

# ── Verified column indices from JotForm CSV export ──────────
COL_AI_FREQUENCY  = 7   # Q5: How often do you use AI tools?
COL_Q10_EXPLAIN   = 12  # Q10: explain concepts in own words (U)
COL_Q11_WRITECODE = 13  # Q11: write program without AI (U)
COL_Q14_FIRSTSTEP = 14  # Q14: first step when error (direct MC)
COL_Q15_CONFIDENT = 15  # Q15: confident in debugging ability
COL_Q16_DEBUG     = 16  # Q16: fix bugs without AI (D)
COL_Q17_COPYERROR = 17  # Q17: copy error to AI first (Likert D)
COL_Q18_TRACE     = 18  # Q18: trace execution mentally (R)
COL_Q19_REDO      = 19  # Q19: redo assignment without AI (R)
COL_Q20_TEACH     = 20  # Q20: understand well enough to teach
COL_Q21_COMPETENT = 21  # Q21: consider self competent
COL_Q22_GRADES    = 22  # Q22: grades reflect real ability
COL_Q23_STRUGGLE  = 23  # Q23: struggle without AI
COL_Q24_PASSING   = 24  # Q24: passing without truly learning
COL_Q27_MOTIVAT   = 27  # Q21e: motivation decreased
COL_Q28_INTEREST  = 28  # Q22e: less interested independently
COL_Q29_CONCERN   = 29  # Q23e: concerned about future
COL_Q32_TRAINING  = 32  # Q24f: received formal AI training
COL_Q33_PROMPTS   = 33  # Q25f: know how to write prompts
COL_Q34_BENEFIT   = 34  # Q26f: would benefit from AI course


def _col(row, idx):
    """Safely get column value."""
    return row[idx].strip() if idx < len(row) else ''


def _count_mc(rows, col_idx, keywords):
    """Count rows where column matches any keyword (case-insensitive)."""
    count = sum(
        1 for row in rows
        if any(k.lower() in _col(row, col_idx).lower() for k in keywords)
    )
    return count, F1_relative_frequency(count, len(rows))


def analyze_survey(csv_path):
    """
    Load survey CSV and apply all survey formulas.
    Returns a dictionary of all computed results.
    """
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = [r for r in reader if any(c.strip() for c in r)]

    n = len(rows)

    # ── F1: AI use frequency ──────────────────────────────────
    freq = {'daily': 0, 'weekly': 0, 'monthly': 0, 'rarely': 0, 'never': 0}
    for row in rows:
        val = _col(row, COL_AI_FREQUENCY).lower()
        if   'daily'   in val or 'günlük'   in val or 'يومياً'   in val: freq['daily']   += 1
        elif 'weekly'  in val or 'haftalık'  in val or 'أسبوعياً' in val: freq['weekly']  += 1
        elif 'monthly' in val or 'aylık'    in val or 'شهرياً'   in val: freq['monthly'] += 1
        elif 'rarely'  in val or 'nadiren'  in val or 'نادراً'   in val: freq['rarely']  += 1
        elif 'never'   in val or 'hiç'      in val or 'لا أ'     in val: freq['never']   += 1

    daily_pct   = F1_relative_frequency(freq['daily'], n)
    weekly_pct  = F1_relative_frequency(freq['weekly'], n)
    combined    = F1_relative_frequency(freq['daily'] + freq['weekly'], n)

    # ── F2: Likert agreement scores ───────────────────────────
    def ag(col): return F2_likert_agreement([_col(r, col) for r in rows])

    q10_pct, q10_n = ag(COL_Q10_EXPLAIN)
    q11_pct, q11_n = ag(COL_Q11_WRITECODE)
    q16_pct, q16_n = ag(COL_Q16_DEBUG)
    q17_pct, q17_n = ag(COL_Q17_COPYERROR)
    q18_pct, q18_n = ag(COL_Q18_TRACE)
    q19_pct, q19_n = ag(COL_Q19_REDO)
    q20_pct, q20_n = ag(COL_Q20_TEACH)
    q21_pct, q21_n = ag(COL_Q21_COMPETENT)
    q22_pct, q22_n = ag(COL_Q22_GRADES)
    q23_pct, q23_n = ag(COL_Q23_STRUGGLE)
    q24_pct, q24_n = ag(COL_Q24_PASSING)
    q27_pct, q27_n = ag(COL_Q27_MOTIVAT)
    q28_pct, q28_n = ag(COL_Q28_INTEREST)
    q29_pct, q29_n = ag(COL_Q29_CONCERN)
    q34_pct, q34_n = ag(COL_Q34_BENEFIT)

    # ── F2b: Disagreement score for Q32 ──────────────────────
    q32_pct, q32_n = F2b_likert_disagreement([_col(r, COL_Q32_TRAINING) for r in rows])

    # ── Q14: Direct first-step question (MC) ─────────────────
    ai_n, ai_pct = _count_mc(rows, COL_Q14_FIRSTSTEP,
        ['use an ai', 'ask an ai', 'copy', 'yapay zeka', 'أسأل', 'انسخ', 'ai tool'])
    read_n, read_pct = _count_mc(rows, COL_Q14_FIRSTSTEP,
        ['read the error', 'understand', 'oku', 'اقرأ', 'anlamaya', 'hata mesaj'])

    # ── F3: Competence perception gap ────────────────────────
    g_competence = F3_competence_gap(q10_pct, q11_pct)

    # ── F4: Debugging displacement gap ───────────────────────
    g_sdb = F4_debugging_displacement_gap(q17_pct, ai_pct)

    # ── F5: Institutional gap ─────────────────────────────────
    supply, demand = F5_institutional_gap(q32_pct, q34_pct)

    return {
        # Meta
        'n': n,
        'headers_count': len(headers),
        # F1 — frequency
        'freq': freq,
        'daily_pct': daily_pct,
        'weekly_pct': weekly_pct,
        'daily_weekly_pct': combined,
        # F2 — UDR agreement scores
        'q10_pct': q10_pct,   'q10_n': q10_n,   # Understanding: explain
        'q11_pct': q11_pct,   'q11_n': q11_n,   # Understanding: write without AI
        'q16_pct': q16_pct,   'q16_n': q16_n,   # Debugging: fix without AI
        'q17_pct': q17_pct,   'q17_n': q17_n,   # Debugging: AI-first Likert (thesis Q13)
        'q13_pct': q17_pct,   'q13_n': q17_n,   # Thesis Q13 alias (col 17)
        'q18_pct': q18_pct,   'q18_n': q18_n,   # Reasoning: trace execution
        'q19_pct': q19_pct,   'q19_n': q19_n,   # Reasoning: redo without AI
        'q20_pct': q20_pct,   'q20_n': q20_n,   # Understanding: teach others
        'q21_pct': q21_pct,   'q21_n': q21_n,   # Perceived competence
        'q22_pct': q22_pct,   'q22_n': q22_n,   # Grades reflect ability
        'q23_pct': q23_pct,   'q23_n': q23_n,   # Would struggle without AI
        'q24_pct': q24_pct,   'q24_n': q24_n,   # Passing without learning
        'q27_pct': q27_pct,   'q27_n': q27_n,   # Motivation decreased
        'q28_pct': q28_pct,   'q28_n': q28_n,   # Less independent interest
        'q29_pct': q29_pct,   'q29_n': q29_n,   # Career concern
        'q34_pct': q34_pct,   'q34_n': q34_n,   # Want AI course
        # F2b
        'q32_pct': q32_pct,   'q32_n': q32_n,   # No AI training received
        # Q14 direct (thesis Q14 = AI-first MC)
        'q14_ai_pct': ai_pct, 'q14_ai_n': ai_n,
        'q14_pct': ai_pct,    'q14_n': ai_n,
        'q14_read_pct': read_pct, 'q14_read_n': read_n,
        # F3
        'g_competence': g_competence,
        # F4
        'g_sdb': g_sdb,
        # F5
        'institutional_supply': supply,
        'institutional_demand': demand,
    }


def analyze_survey_demo():
    """Demo mode using sample data — for testing without CSV."""
    return {
        'n': 23, 'headers_count': 38,
        'freq': {'daily':12,'weekly':7,'monthly':1,'rarely':2,'never':1},
        'daily_pct': 52.2, 'weekly_pct': 30.4, 'daily_weekly_pct': 82.6,
        'q10_pct': 73.9, 'q10_n': 17,
        'q11_pct': 56.5, 'q11_n': 13,
        'q16_pct': 47.8, 'q16_n': 11,
        'q17_pct': 52.2, 'q17_n': 12,
        'q13_pct': 52.2, 'q13_n': 12,
        'q18_pct': 65.2, 'q18_n': 15,
        'q19_pct': 56.5, 'q19_n': 13,
        'q20_pct': 60.9, 'q20_n': 14,
        'q21_pct': 56.5, 'q21_n': 13,
        'q22_pct': 43.5, 'q22_n': 10,
        'q23_pct': 56.5, 'q23_n': 13,
        'q24_pct': 39.1, 'q24_n': 9,
        'q27_pct': 26.1, 'q27_n': 6,
        'q28_pct': 43.5, 'q28_n': 10,
        'q29_pct': 30.4, 'q29_n': 7,
        'q34_pct': 52.2, 'q34_n': 12,
        'q32_pct': 60.9, 'q32_n': 14,
        'q14_ai_pct': 21.7, 'q14_ai_n': 5,
        'q14_pct': 21.7,    'q14_n': 5,
        'q14_read_pct': 65.2, 'q14_read_n': 15,
        'g_competence': 17.4,
        'g_sdb': 30.4,
        'institutional_supply': 60.9,
        'institutional_demand': 52.2,
    }
