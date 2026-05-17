# UDR Analysis System

**Analysing the Impact of AI-Assisted Coding Tools on Programming Skill Development**

> MSc Thesis — Computer Engineering | Beykoz University, Istanbul | May 2026  
> Author: Abdelrahman Sabry Abdalla Ali Abada Belal  
> Supervisor: Prof. Dr. Abdurazzag Ali A. Aburas

---

## Overview

The **UDR Analysis System** is a Python-based research instrument that operationalises a three-component mixed-methods study into the effect of AI-assisted coding tools on student programming competence. It processes empirical data from three sources, applies seven analytical formulas (F1–F7), and produces validated answers to four research questions through convergent triangulation.

The system is the engineering deliverable of the MSc thesis and can be run either as a **console pipeline** (`main.py`) or through a **four-tab graphical interface** (`udr_gui.py`).

---

## Research Questions

| ID | Question |
|----|----------|
| RQ1 | How do students engage with AI tools during programming learning, and how does this affect UDR skills? |
| RQ2 | Which UDR domain — Understanding, Debugging, or Reasoning — is most strongly affected? |
| RQ3 | Is there a measurable illusory competence gap between perceived and actual ability? |
| RQ4 | What distinguishes guided from unguided AI use, and under what conditions is guided use possible? |

---

## The UDR Framework

The system measures three cognitive skill domains required for programming competence:

- **U — Understanding**: the ability to explain what code does and why
- **D — Debugging**: the ability to read errors, trace execution, and fix faults independently
- **R — Reasoning**: the ability to plan logic, anticipate edge cases, and verify correctness mentally

---

## System Architecture

```
udr-analysis-system/
│
├── main.py                    # Console pipeline — runs all 7 steps
├── udr_gui.py                 # Four-tab Tkinter GUI
│
├── modules/
│   ├── formula_engine.py      # All 7 analytical formulas (F1–F7)
│   ├── survey_module.py       # Reads JotForm CSV, applies F1–F5
│   ├── observation_module.py  # Processes cohort behavioral data via F1
│   ├── case_study_module.py   # Scores Student A UDR domains via F7
│   ├── triangulation_module.py # Validates findings via F6
│   ├── visualization.py       # Generates 5 output figures (Figs 4.1–4.5)
│   └── report_generator.py    # Saves structured results_report.txt
│
├── data/
│   └── survey_data.csv        # JotForm export — 23 responses, 38 columns
│
├── outputs/                   # Generated automatically on first run
│   ├── fig1_ai_frequency.png
│   ├── fig2_udr_profile.png
│   ├── fig3_debugging_gap.png
│   ├── fig4_illusory_competence.png
│   ├── fig5_institutional_gap.png
│   └── results_report.txt
│
├── tests/
│   └── test_formulas.py       # Unit tests for all 7 formulas
│
├── docs/
│   └── formulas.md            # Mathematical documentation of F1–F7
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## The 7 Analytical Formulas

| Formula | Name | Expression | Purpose |
|---------|------|------------|---------|
| F1 | Relative Frequency | `P(i) = (f(i) / n) × 100` | Convert any count to percentage |
| F2 | Likert Agreement Score | `A(q) = (SA + A) / n × 100` | Agreement % for Likert items |
| F2b | Likert Disagreement Score | `D(q) = (SD + D) / n × 100` | Disagreement % (used for Q32) |
| F3 | Competence Perception Gap | `G = A(Q10) − A(Q11)` | Illusory competence measure |
| F4 | Social Desirability Gap | `G_SDB = A(Q17) − P_AI(Q14)` | Self-report bias in debugging |
| F5 | Institutional Supply-Demand Gap | `Supply = D(Q32)` vs `Demand = A(Q34)` | AI training provision gap |
| F6 | Convergent Triangulation Validity | `Valid iff C1 ∧ C2 ∧ C3` | Cross-source finding validation |
| F7 | UDR Observation Coding Score | `UDR(d) = (indicators / 4) × 100` | Case study domain scoring |

---

## Quick Start

### Requirements

```bash
pip install -r requirements.txt
```

### Console run (full pipeline)

```bash
python main.py
```

Uses `data/survey_data.csv` by default. To specify a different file:

```bash
python main.py path/to/your_survey.csv
```

### Graphical interface

```bash
python udr_gui.py
```

Four tabs: Observation input → Survey CSV upload → Case Study scoring → Integrated Results

---

## Outputs

After running `main.py`, the `outputs/` folder contains:

| File | Thesis Figure | Content |
|------|--------------|---------|
| `fig1_ai_frequency.png` | Figure 4.1 | AI tool use frequency distribution (F1) |
| `fig2_udr_profile.png` | Figure 4.2 | UDR self-assessment profile across survey items (F2, F3) |
| `fig3_debugging_gap.png` | Figure 4.3 | Q14 vs Q17 — 30.4-point social desirability gap (F4) |
| `fig4_illusory_competence.png` | Figure 4.4 | Illusory competence cluster — 17.4-point gap (F3) |
| `fig5_institutional_gap.png` | Figure 4.5 | Institutional supply-demand gap (F5) |
| `results_report.txt` | — | Full formula outputs and RQ1–RQ4 answers |

---

## Key Findings (System Output)

| Metric | Value | Formula |
|--------|-------|---------|
| Daily + weekly AI use | 82.6% | F1 |
| Can explain concepts (Q10) | 73.9% | F2 |
| Can write without AI (Q11) | 56.5% | F2 |
| Competence perception gap | **17.4 pts** | F3 |
| Social desirability gap (debugging) | **30.4 pts** | F4 |
| Received no AI training (Q32) | 60.9% | F2b |
| Student A — Task A UDR score | **0% (all domains)** | F7 |
| All 4 findings validated | ✓ VALID | F6 |

---

## Three-Component Design

The system processes data from three methodological components simultaneously:

**Component 1 — Participant Observation** (20 students, 7 sessions, Dec 2025–Mar 2026)  
Processed by `observation_module.py` using F1.

**Component 2 — Anonymous Survey** (23 responses, JotForm, April 2026)  (See The Survey Here:  )
Processed by `survey_module.py` using F1, F2, F2b, F3, F4, F5.

**Component 3 — Case Study** (Student A, 4h 15m session, April 2026)  
Processed by `case_study_module.py` using F7.

All three converge in `triangulation_module.py` via Formula F6.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests cover all 7 formulas with known-value assertions, edge cases, and boundary conditions.

---

## Survey CSV Format

The system expects the JotForm export format with 38 columns. Key column indices:

| Column | Index | Question |
|--------|-------|---------|
| AI frequency | 7 | Q5: How often do you use AI tools? |
| Q10 explain | 12 | Can you explain concepts in your own words |
| Q11 write | 13 | Can write program without AI |
| Q14 first step | 14 | First step when code fails (direct MC) |
| Q16 debug | 16 | Can fix bugs without AI |
| Q17 copy error | 17 | Copy error to AI first (Likert) |
| Q32 training | 32 | Received formal AI training |
| Q34 benefit | 34 | Would benefit from AI course |

The survey module handles trilingual responses (English, Turkish, Arabic) on all Likert items.
See the survey here:  
( https://www.jotform.com/tables/261112389940053 )

---

## Citation

```
Belal, A. S. A. A. A. (2026). Analysing the Impact of AI-Assisted Coding Tools on 
Programming Skill Development: An Experimental Study in Computer Engineering Education.
MSc Thesis, Beykoz University, Istanbul.
```

---

## License

This repository is part of an academic thesis submission. The source code is made available for academic review and reproducibility purposes.

© 2026 Abdelrahman Sabry Abdalla Ali Abada Belal — Beykoz University
