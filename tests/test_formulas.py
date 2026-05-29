"""
================================================================
UNIT TESTS — UDR Analysis System
================================================================
Tests all 7 analytical formulas (F1–F7) with:
  - Known-value assertions from the thesis
  - Edge cases (zero, full, boundary)
  - Type and return value checks

Run with:
    python -m pytest tests/ -v
================================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.formula_engine import (
    F1_relative_frequency,
    F2_likert_agreement,
    F2b_likert_disagreement,
    F3_competence_gap,
    F4_debugging_displacement_gap,
    F5_institutional_gap,
    F6_triangulation_validity,
    F7_udr_coding_score,
)


# ══════════════════════════════════════════════════════════════
# F1 — Relative Frequency
# ══════════════════════════════════════════════════════════════

class TestF1RelativeFrequency:

    def test_thesis_daily_use(self):
        """12 daily users out of 23 = 52.2%"""
        assert F1_relative_frequency(12, 23) == 52.2

    def test_thesis_daily_plus_weekly(self):
        """19 daily+weekly users out of 23 = 82.6%"""
        assert F1_relative_frequency(19, 23) == 82.6

    def test_zero_count(self):
        """0 respondents = 0%"""
        assert F1_relative_frequency(0, 23) == 0.0

    def test_full_count(self):
        """All respondents = 100%"""
        assert F1_relative_frequency(23, 23) == 100.0

    def test_zero_total_safe(self):
        """Division by zero should return 0.0 not raise"""
        assert F1_relative_frequency(5, 0) == 0.0

    def test_returns_float(self):
        result = F1_relative_frequency(10, 20)
        assert isinstance(result, float)

    def test_rounding_one_decimal(self):
        """Result should be rounded to 1 decimal place"""
        result = F1_relative_frequency(1, 3)
        assert result == 33.3

    def test_single_respondent(self):
        assert F1_relative_frequency(1, 23) == 4.3


# ══════════════════════════════════════════════════════════════
# F2 — Likert Agreement Score
# ══════════════════════════════════════════════════════════════

class TestF2LikertAgreement:

    def test_thesis_q10_english(self):
        """17 of 23 agree = 73.9%"""
        responses = ['Agree'] * 10 + ['Strongly Agree'] * 7 + ['Neutral'] * 4 + ['Disagree'] * 2
        pct, count = F2_likert_agreement(responses)
        assert pct == 73.9
        assert count == 17

    def test_thesis_q11_english(self):
        """13 of 23 agree = 56.5%"""
        responses = ['Agree'] * 8 + ['Strongly Agree'] * 5 + ['Neutral'] * 5 + ['Disagree'] * 5
        pct, count = F2_likert_agreement(responses)
        assert pct == 56.5
        assert count == 13

    def test_turkish_responses(self):
        """Turkish 'Katılıyorum' should be counted as Agree"""
        responses = ['Katılıyorum'] * 10 + ['Kesinlikle Katılıyorum'] * 5 + ['Kararsızım'] * 8
        pct, count = F2_likert_agreement(responses)
        assert count == 15

    def test_arabic_responses(self):
        """Arabic 'موافق' should be counted as Agree"""
        responses = ['موافق'] * 8 + ['موافق بشدة'] * 4 + ['محايد'] * 11
        pct, count = F2_likert_agreement(responses)
        assert count == 12

    def test_all_disagree(self):
        responses = ['Disagree'] * 10 + ['Strongly Disagree'] * 13
        pct, count = F2_likert_agreement(responses)
        assert pct == 0.0
        assert count == 0

    def test_all_agree(self):
        responses = ['Agree'] * 23
        pct, count = F2_likert_agreement(responses)
        assert pct == 100.0
        assert count == 23

    def test_empty_responses(self):
        pct, count = F2_likert_agreement([])
        assert pct == 0.0
        assert count == 0

    def test_strongly_disagree_not_counted(self):
        """'Strongly Disagree' must not be counted as agreement"""
        responses = ['Strongly Disagree'] * 23
        pct, count = F2_likert_agreement(responses)
        assert count == 0

    def test_disagree_not_counted(self):
        """'Disagree' must not be counted as agreement"""
        responses = ['Disagree'] * 23
        pct, count = F2_likert_agreement(responses)
        assert count == 0


# ══════════════════════════════════════════════════════════════
# F2b — Likert Disagreement Score
# ══════════════════════════════════════════════════════════════

class TestF2bLikertDisagreement:

    def test_thesis_q32(self):
        """14 of 23 disagree = 60.9%"""
        responses = (
            ['Strongly Disagree'] * 5 + ['Disagree'] * 9 +
            ['Neutral'] * 4 + ['Agree'] * 3 + ['Strongly Agree'] * 2
        )
        pct, count = F2b_likert_disagreement(responses)
        assert pct == 60.9
        assert count == 14

    def test_all_agree_gives_zero_disagreement(self):
        responses = ['Agree'] * 23
        pct, count = F2b_likert_disagreement(responses)
        assert pct == 0.0
        assert count == 0

    def test_turkish_disagree(self):
        responses = ['Katılmıyorum'] * 10 + ['Kesinlikle Katılmıyorum'] * 5 + ['Kararsızım'] * 8
        pct, count = F2b_likert_disagreement(responses)
        assert count == 15

    def test_arabic_disagree(self):
        responses = ['غير موافق'] * 8 + ['غير موافق بشدة'] * 4 + ['محايد'] * 11
        pct, count = F2b_likert_disagreement(responses)
        assert count == 12


# ══════════════════════════════════════════════════════════════
# F3 — Competence Perception Gap
# ══════════════════════════════════════════════════════════════

class TestF3CompetenceGap:

    def test_thesis_value(self):
        """73.9% - 56.5% = 17.4 points"""
        assert F3_competence_gap(73.9, 56.5) == 17.4

    def test_no_gap(self):
        assert F3_competence_gap(60.0, 60.0) == 0.0

    def test_negative_gap(self):
        """Lower perceived understanding than ability — unusual but possible"""
        result = F3_competence_gap(40.0, 60.0)
        assert result == -20.0

    def test_returns_float(self):
        assert isinstance(F3_competence_gap(73.9, 56.5), float)

    def test_large_gap(self):
        assert F3_competence_gap(100.0, 0.0) == 100.0


# ══════════════════════════════════════════════════════════════
# F4 — Social Desirability Gap
# ══════════════════════════════════════════════════════════════

class TestF4SocialDesirabilityGap:

    def test_thesis_value(self):
        """52.2% - 21.7% = 30.4 (rounding may give 30.5)"""
        result = F4_debugging_displacement_gap(52.2, 21.7)
        assert abs(result - 30.5) < 0.2  # allow rounding tolerance

    def test_no_gap(self):
        assert F4_debugging_displacement_gap(50.0, 50.0) == 0.0

    def test_negative_gap(self):
        """Direct > Indirect would indicate reverse desirability bias"""
        result = F4_debugging_displacement_gap(20.0, 50.0)
        assert result == -30.0

    def test_returns_float(self):
        assert isinstance(F4_debugging_displacement_gap(52.2, 21.7), float)


# ══════════════════════════════════════════════════════════════
# F5 — Institutional Supply-Demand Gap
# ══════════════════════════════════════════════════════════════

class TestF5InstitutionalGap:

    def test_thesis_values(self):
        supply, demand = F5_institutional_gap(60.9, 52.2)
        assert supply == 60.9
        assert demand == 52.2

    def test_returns_tuple(self):
        result = F5_institutional_gap(60.9, 52.2)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_zero_values(self):
        supply, demand = F5_institutional_gap(0.0, 0.0)
        assert supply == 0.0
        assert demand == 0.0

    def test_full_values(self):
        supply, demand = F5_institutional_gap(100.0, 100.0)
        assert supply == 100.0
        assert demand == 100.0


# ══════════════════════════════════════════════════════════════
# F6 — Convergent Triangulation Validity
# ══════════════════════════════════════════════════════════════

class TestF6TriangulationValidity:

    def test_all_true_is_valid(self):
        """All three components support the finding → VALID"""
        assert F6_triangulation_validity(True, True, True) is True

    def test_c1_false_is_invalid(self):
        assert F6_triangulation_validity(False, True, True) is False

    def test_c2_false_is_invalid(self):
        assert F6_triangulation_validity(True, False, True) is False

    def test_c3_false_is_invalid(self):
        assert F6_triangulation_validity(True, True, False) is False

    def test_all_false_is_invalid(self):
        assert F6_triangulation_validity(False, False, False) is False

    def test_returns_bool(self):
        result = F6_triangulation_validity(True, True, True)
        assert isinstance(result, bool)

    def test_thesis_finding1(self):
        """Finding 1 — AI dependency confirmed across all three components"""
        assert F6_triangulation_validity(
            c1=True,   # 90% observation dependency rate ≥ 70%
            c2=True,   # 82.6% survey daily+weekly ≥ 70%
            c3=True,   # Student A used AI before attempting
        ) is True

    def test_thesis_finding2(self):
        """Finding 2 — Illusory competence confirmed"""
        assert F6_triangulation_validity(
            c1=True,   # 80% explanation failure rate ≥ 60%
            c2=True,   # F3 gap = 17.4 pts ≥ 10 pts
            c3=True,   # F7 illusory gap = 80 pts ≥ 30 pts
        ) is True

    def test_thesis_finding3(self):
        """Finding 3 — Debugging most affected"""
        assert F6_triangulation_validity(
            c1=True,   # 85% debugging weakness ≥ 70%
            c2=True,   # F4 SDB gap = 30.4 pts ≥ 20 pts
            c3=True,   # Student A debugging = 0% ≤ 25%
        ) is True

    def test_thesis_finding4(self):
        """Finding 4 — Dual institutional failure"""
        assert F6_triangulation_validity(
            c1=True,   # 100% passed despite deficits ≥ 80%
            c2=True,   # 60.9% no training ≥ 50%
            c3=True,   # dependency level 9 ≥ 7
        ) is True


# ══════════════════════════════════════════════════════════════
# F7 — UDR Observation Coding Score
# ══════════════════════════════════════════════════════════════

class TestF7UDRCodingScore:

    def test_thesis_task_a_all_zero(self):
        """Student A scored 0 indicators in all Task A domains"""
        assert F7_udr_coding_score(0) == 0.0

    def test_thesis_task_b_reasoning(self):
        """Student A scored 1 Reasoning indicator in Task B"""
        assert F7_udr_coding_score(1) == 25.0

    def test_two_indicators(self):
        assert F7_udr_coding_score(2) == 50.0

    def test_three_indicators(self):
        assert F7_udr_coding_score(3) == 75.0

    def test_full_score(self):
        """All 4 indicators present = 100%"""
        assert F7_udr_coding_score(4) == 100.0

    def test_returns_float(self):
        assert isinstance(F7_udr_coding_score(2), float)

    def test_zero_total_safe(self):
        """total_indicators=0 should return 0.0 not raise"""
        assert F7_udr_coding_score(0, total_indicators=0) == 0.0

    def test_illusory_gap_calculation(self):
        """
        Student A claimed 80% self-reliance.
        Task A average = (0 + 0 + 0) / 3 = 0.0%
        Illusory gap = 80 - 0 = 80 points
        """
        a_u = F7_udr_coding_score(0)
        a_d = F7_udr_coding_score(0)
        a_r = F7_udr_coding_score(0)
        task_a_avg = round((a_u + a_d + a_r) / 3, 1)
        claimed = 80
        gap = round(claimed - task_a_avg, 1)
        assert task_a_avg == 0.0
        assert gap == 80.0
