# Analytical Formulas — UDR Analysis System

This document provides the full mathematical specification of all seven formulas (F1–F7) used in the UDR Analysis System. Each formula is defined in `modules/formula_engine.py` and corresponds to a section of the thesis (Section 3.10.5).

---

## F1 — Relative Frequency

**Expression:**
```
P(i) = (f(i) / n) × 100
```

**Variables:**
- `f(i)` — frequency count of respondents selecting response category *i*
- `n` — total number of respondents (23 for survey, 20 for observation)
- `P(i)` — percentage of respondents selecting category *i*

**Application:** Applied to every percentage figure in the analysis. The base calculation from which all other formulas derive their percentages.

**Thesis finding:** 82.6% = F1(19, 23) — combined daily and weekly AI users.

---

## F2 — Likert Agreement Score

**Expression:**
```
A(q) = (f_SA(q) + f_A(q)) / n × 100
```

**Variables:**
- `f_SA(q)` — count of Strongly Agree responses for item *q*
- `f_A(q)` — count of Agree responses for item *q*
- `n` — total respondents
- `A(q)` — combined agreement percentage for item *q*

**Application:** All Likert-scale items in Sections C–G of the survey. Supports English, Turkish, and Arabic response strings.

**Thesis finding:** A(Q10) = 73.9% — students who agree they can explain programming concepts.

---

## F2b — Likert Disagreement Score

**Expression:**
```
D(q) = (f_SD(q) + f_D(q)) / n × 100
```

**Variables:**
- `f_SD(q)` — count of Strongly Disagree responses for item *q*
- `f_D(q)` — count of Disagree responses for item *q*

**Application:** Used specifically for Q32 to measure students who *deny* having received formal AI training.

**Thesis finding:** D(Q32) = 60.9% — proportion who rejected the claim of institutional AI literacy provision.

---

## F3 — Competence Perception Gap

**Expression:**
```
G_competence = A(Q10) − A(Q11)
```

**Variables:**
- `A(Q10)` — agreement % on "I can explain concepts in my own words"
- `A(Q11)` — agreement % on "I can write code without AI"
- `G_competence` — the gap in percentage points

**Interpretation:** A positive gap indicates students perceive their understanding as higher than their demonstrated independent coding ability — the primary quantitative indicator of illusory competence.

**Thesis finding:** G_competence = 73.9% − 56.5% = **17.4 points** (answers RQ3).

---

## F4 — Social Desirability Gap

**Expression:**
```
G_SDB = A(Q17) − P_AI(Q14)
```

**Variables:**
- `A(Q17)` — Likert agreement % on "My first action when code fails is to copy the error to AI" (indirect question)
- `P_AI(Q14)` — percentage selecting "Use AI immediately" on direct multiple-choice Q14
- `G_SDB` — Social Desirability Bias gap in percentage points

**Interpretation:** Measures the discrepancy between how students describe their debugging behavior indirectly (Likert) versus directly (multiple choice). A large gap indicates social desirability bias — students under-report their AI-first behavior when asked directly.

**Thesis finding:** G_SDB = 52.2% − 21.7% = **30.4 points** (answers RQ2 and RQ4).

---

## F5 — Institutional Supply-Demand Gap

**Expression:**
```
Supply Gap = D(Q32)
Demand     = A(Q34)
```

**Variables:**
- `D(Q32)` — disagreement % on "My university has provided formal training on AI use" (computed via F2b)
- `A(Q34)` — agreement % on "I would benefit from a structured AI literacy course" (computed via F2)

**Interpretation:** Compares the proportion of students who report receiving no institutional AI training (supply failure) against the proportion who actively want such training (demand). Both values are stated separately rather than as a single arithmetic gap.

**Thesis finding:** Supply = 60.9%, Demand = 52.2% — confirms dual institutional failure (answers RQ4).

---

## F6 — Convergent Triangulation Validity

**Expression:**
```
Finding is VALID  iff  C1 ∧ C2 ∧ C3
Finding is INVALID if  ¬C1 ∨ ¬C2 ∨ ¬C3
```

**Variables:**
- `C1` — evidence from Component 1 (Participant-Observation) supports the finding
- `C2` — evidence from Component 2 (Anonymous Survey) supports the finding
- `C3` — evidence from Component 3 (Case Study) supports the finding
- `∧` — logical AND

**Interpretation:** A finding is considered empirically robust only when all three independent data sources converge on the same conclusion. Divergence in any one source invalidates the finding.

**Thesis finding:** All four integrated findings (AI dependency, illusory competence, debugging most affected, dual institutional failure) passed F6 — all are marked VALID.

---

## F7 — UDR Observation Coding Score

**Expression:**
```
UDR_score(d) = (indicators_present(d) / 4) × 100
```

**Variables:**
- `d` — domain index: U (Understanding), D (Debugging), or R (Reasoning)
- `indicators_present(d)` — number of behavioral indicators observed for domain *d* (integer 0–4)
- `4` — total number of binary indicators per domain
- `UDR_score(d)` — percentage score for domain *d*

**UDR Indicators per domain (4 each):**

*Understanding:*
1. Can explain what the code does
2. Can explain why specific constructs were used
3. Can describe program behavior under different inputs
4. Can relate code structure to the problem requirements

*Debugging:*
1. Reads error messages analytically
2. Forms hypotheses about failure causes
3. Traces execution to locate the error
4. Applies fix and verifies correctness independently

*Reasoning:*
1. Plans logic before writing code
2. Anticipates edge cases
3. Verifies correctness through mental execution
4. Can explain algorithmic approach before coding

**Application:** Applied to Student A's performance on Task A (no AI) and Task B (with AI) during the case study session.

**Thesis finding:** Student A scored 0% on all three UDR domains in Task A. Illusory gap = claimed 80% self-reliance − 0% observed = **80 points**.

---

## Formula Dependencies

```
F1  ──► F2 ──► F3
         │
         └──► F4
         │
F2b ──► F5

F3, F4, F6 (case study input) ──► F6 (triangulation)

F7 (case study scoring) ──────────► F6 (triangulation)
```

---

## Implementation

All formulas are implemented as pure functions in `modules/formula_engine.py`. Each function is self-contained, accepts only numeric inputs, and returns a rounded float. No external dependencies are required for the formula layer.
