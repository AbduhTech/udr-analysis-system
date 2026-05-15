"""
================================================================
UDR ANALYSIS SYSTEM — GUI
================================================================
Title:   Analysing the Impact of AI-Assisted Coding Tools on
         Programming Skill Development
Author:  Abdelrahman Sabry Abdalla Ali Abada Belal
Univ:    Beykoz University — Computer Engineering MSc
Date:    May 2026
Advisor: Prof. Dr. Abdurazzag Ali A. Aburas

USAGE: python udr_gui.py
================================================================
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os

from modules.observation_module import analyze_observation
from modules.survey_module import analyze_survey, analyze_survey_demo
from modules.case_study_module import analyze_case_study, UDR_INDICATORS
from modules.triangulation_module import triangulate
from modules.report_generator import generate_text_report
from modules.visualization import generate_all_figures


class UDRGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UDR Research Analysis System — Beykoz University MSc")
        self.root.geometry("1100x750")

        self.observation_results = {}
        self.survey_results      = {}
        self.case_results        = {}

        # ── Title ─────────────────────────────────────────────
        tk.Label(root,
                 text="UDR Research Analysis System",
                 font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(root,
                 text="Analysing the Impact of AI-Assisted Coding Tools on Programming Skill Development",
                 font=("Arial", 10)).pack()
        tk.Label(root,
                 text="Abdelrahman Sabry Abdalla Ali Abada Belal  |  Beykoz University MSc  |  May 2026",
                 font=("Arial", 9), fg="gray").pack(pady=3)

        # ── Tabs ──────────────────────────────────────────────
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=8)

        self.obs_tab     = tk.Frame(self.tabs)
        self.survey_tab  = tk.Frame(self.tabs)
        self.case_tab    = tk.Frame(self.tabs)
        self.results_tab = tk.Frame(self.tabs)

        self.tabs.add(self.obs_tab,     text="Component 1 — Observation")
        self.tabs.add(self.survey_tab,  text="Component 2 — Survey")
        self.tabs.add(self.case_tab,    text="Component 3 — Case Study")
        self.tabs.add(self.results_tab, text="Integrated Results (RQ1-RQ4)")

        self.build_observation_tab()
        self.build_survey_tab()
        self.build_case_tab()
        self.build_results_tab()

    # ── Helper: labelled entry ─────────────────────────────────
    def labelled_entry(self, parent, label, row, default="", tooltip=""):
        tk.Label(parent, text=label, font=("Arial", 10),
                 anchor="w").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = ttk.Entry(parent, width=20)
        entry.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        entry.insert(0, default)
        if tooltip:
            tk.Label(parent, text=f"  ← {tooltip}",
                     font=("Arial", 8), fg="gray").grid(row=row, column=2, sticky="w")
        return entry

    def get_int(self, entry, name):
        try:
            return int(entry.get())
        except ValueError:
            messagebox.showerror("Input error", f"'{name}' must be a whole number.")
            raise

    # ══════════════════════════════════════════════════════════
    # COMPONENT 1 — OBSERVATION TAB
    # ══════════════════════════════════════════════════════════
    def build_observation_tab(self):
        tk.Label(self.obs_tab,
                 text="Component 1 — Participant Observation Input",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.obs_tab,
                 text="Enter the counts observed during the 3-month engagement.\n"
                      "Formula F1 (Relative Frequency) is applied to each value.",
                 font=("Arial", 9), fg="gray").pack()

        form = tk.Frame(self.obs_tab)
        form.pack(pady=8)

        self.obs_students  = self.labelled_entry(form, "Total students in cohort",          0, "20", "thesis value: 20")
        self.obs_sessions  = self.labelled_entry(form, "Number of sessions",                1, "7",  "thesis value: 7")
        self.obs_ai_first  = self.labelled_entry(form, "Students using AI as first resort", 2, "18", "observed in sessions")
        self.obs_unable    = self.labelled_entry(form, "Students unable to explain code",   3, "16", "verbal response check")
        self.obs_debug     = self.labelled_entry(form, "Students with Debugging weakness",  4, "17", "UDR domain — D")
        self.obs_reason    = self.labelled_entry(form, "Students with Reasoning weakness",  5, "16", "UDR domain — R")
        self.obs_passed    = self.labelled_entry(form, "Students passed despite deficits",  6, "20", "institutional gap")
        self.obs_drop      = self.labelled_entry(form, "Students with motivation decline",  7, "12", "abandoned take-home")

        ttk.Button(self.obs_tab, text="Analyze Observation Data (F1)",
                   command=self.analyze_observation).pack(pady=10)

        self.obs_box = ScrolledText(self.obs_tab, width=105, height=16,
                                    font=("Consolas", 10))
        self.obs_box.pack(padx=10, pady=5)

    def analyze_observation(self):
        try:
            s   = self.get_int(self.obs_students, "Total students")
            ses = self.get_int(self.obs_sessions,  "Sessions")
            ai  = self.get_int(self.obs_ai_first,  "AI first")
            un  = self.get_int(self.obs_unable,    "Unable to explain")
            db  = self.get_int(self.obs_debug,     "Debugging weak")
            re  = self.get_int(self.obs_reason,    "Reasoning weak")
            pa  = self.get_int(self.obs_passed,    "Passed despite")
            dr  = self.get_int(self.obs_drop,      "Motivation drop")
        except Exception:
            return

        self.observation_results = analyze_observation(s, ses, ai, un, db, re, pa, dr)
        r = self.observation_results

        self.obs_box.delete("1.0", tk.END)
        self.obs_box.insert(tk.END, "OBSERVATION MODULE RESULTS — Formula F1: P(i) = (f(i)/n) × 100\n")
        self.obs_box.insert(tk.END, "─" * 65 + "\n")
        self.obs_box.insert(tk.END, f"Students observed:          {r['students']}\n")
        self.obs_box.insert(tk.END, f"Sessions conducted:         {r['sessions']}\n\n")
        self.obs_box.insert(tk.END, f"UDR DOMAIN RATES (F1):\n")
        self.obs_box.insert(tk.END, f"  AI dependency rate:       {r['ai_dependency_rate']}%\n")
        self.obs_box.insert(tk.END, f"  Explanation failure rate: {r['explanation_failure_rate']}%  ← Understanding\n")
        self.obs_box.insert(tk.END, f"  Debugging weakness rate:  {r['debugging_weakness_rate']}%  ← Debugging (RQ2)\n")
        self.obs_box.insert(tk.END, f"  Reasoning weakness rate:  {r['reasoning_weakness_rate']}%  ← Reasoning\n\n")
        self.obs_box.insert(tk.END, f"INSTITUTIONAL GAP:\n")
        self.obs_box.insert(tk.END, f"  Institutional gap rate:   {r['institutional_gap_rate']}%\n")
        self.obs_box.insert(tk.END, f"  Motivation decline rate:  {r['attendance_decline_rate']}%\n\n")
        self.obs_box.insert(tk.END, f"RQ ANSWERS FROM COMPONENT 1:\n")
        self.obs_box.insert(tk.END, f"  {r['rq1_answer']}\n")
        self.obs_box.insert(tk.END, f"  {r['rq2_answer']}\n")
        self.obs_box.insert(tk.END, f"  {r['rq3_answer']}\n")
        self.obs_box.insert(tk.END, f"  {r['rq4_answer']}\n")

    # ══════════════════════════════════════════════════════════
    # COMPONENT 2 — SURVEY TAB
    # ══════════════════════════════════════════════════════════
    def build_survey_tab(self):
        tk.Label(self.survey_tab,
                 text="Component 2 — Survey Data Analysis",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.survey_tab,
                 text="Load your JotForm CSV export. Formulas F1, F2, F2b, F3, F4, F5 are applied automatically.",
                 font=("Arial", 9), fg="gray").pack()

        top = tk.Frame(self.survey_tab)
        top.pack(pady=10)

        self.csv_path = tk.StringVar()
        ttk.Entry(top, textvariable=self.csv_path, width=65).grid(row=0, column=0, padx=8)
        ttk.Button(top, text="Browse CSV", command=self.browse_csv).grid(row=0, column=1, padx=8)

        btn_frame = tk.Frame(self.survey_tab)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Run Survey Analysis (F1–F5)",
                   command=self.analyze_survey).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Generate Figures",
                   command=self.generate_figures).pack(side="left", padx=8)

        self.survey_box = ScrolledText(self.survey_tab, width=105, height=24,
                                       font=("Consolas", 10))
        self.survey_box.pack(padx=10, pady=5)

    def browse_csv(self):
        path = filedialog.askopenfilename(
            title="Select survey CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            self.csv_path.set(path)

    def analyze_survey(self):
        self.survey_box.delete("1.0", tk.END)
        path = self.csv_path.get()

        if path and os.path.exists(path):
            try:
                self.survey_results = analyze_survey(path)
                self.survey_box.insert(tk.END, f"CSV loaded: {os.path.basename(path)}\n")
            except Exception as e:
                messagebox.showerror("CSV error", str(e))
                return
        else:
            self.survey_results = analyze_survey_demo()
            self.survey_box.insert(tk.END, "No CSV selected — using verified thesis values.\n")

        r = self.survey_results
        n = r['n']

        self.survey_box.insert(tk.END, f"Responses: {n}\n\n")
        self.survey_box.insert(tk.END, "F1 — RELATIVE FREQUENCY:\n")
        self.survey_box.insert(tk.END, f"  Daily AI use:         {r['freq'].get('daily',0)}/{n} = {r['daily_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Weekly AI use:        {r['freq'].get('weekly',0)}/{n} = {r['weekly_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Daily+Weekly (RQ1):   {r['daily_weekly_pct']}%\n\n")
        self.survey_box.insert(tk.END, "F2 — LIKERT AGREEMENT SCORES:\n")
        self.survey_box.insert(tk.END, f"  Q10 Explain concepts (U):  {r['q10_n']}/{n} = {r['q10_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Q11 Write without AI (U):  {r['q11_n']}/{n} = {r['q11_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Q16 Debug without AI (D):  {r['q16_n']}/{n} = {r['q16_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Q17 AI-first Likert (D):   {r['q17_n']}/{n} = {r['q17_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Q18 Trace execution (R):   {r['q18_n']}/{n} = {r['q18_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Q19 Redo without AI (R):   {r['q19_n']}/{n} = {r['q19_pct']}%\n")
        self.survey_box.insert(tk.END, f"  Q24 Passing w/o learning:  {r['q24_n']}/{n} = {r['q24_pct']}%\n\n")
        self.survey_box.insert(tk.END, "F2b — LIKERT DISAGREEMENT SCORE:\n")
        self.survey_box.insert(tk.END, f"  Q32 No AI training:        {r['q32_n']}/{n} = {r['q32_pct']}%\n\n")
        self.survey_box.insert(tk.END, "F3 — COMPETENCE PERCEPTION GAP (RQ3):\n")
        self.survey_box.insert(tk.END, f"  G_competence = {r['q10_pct']}% - {r['q11_pct']}% = {r['g_competence']} pts\n\n")
        self.survey_box.insert(tk.END, "F4 — SOCIAL DESIRABILITY GAP (RQ2, RQ4):\n")
        self.survey_box.insert(tk.END, f"  Q14 AI-first (direct):     {r['q14_ai_n']}/{n} = {r['q14_ai_pct']}%\n")
        self.survey_box.insert(tk.END, f"  G_SDB = {r['q17_pct']}% - {r['q14_ai_pct']}% = {r['g_sdb']} pts\n\n")
        self.survey_box.insert(tk.END, "F5 — INSTITUTIONAL GAP (Gap 5):\n")
        self.survey_box.insert(tk.END, f"  Supply gap D(Q32):         {r['institutional_supply']}%\n")
        self.survey_box.insert(tk.END, f"  Demand A(Q34):             {r['institutional_demand']}%\n")

    def generate_figures(self):
        if not self.survey_results:
            self.analyze_survey()
        try:
            paths = generate_all_figures(self.survey_results)
            messagebox.showinfo("Figures saved",
                f"5 figures generated:\n" + "\n".join(paths))
        except Exception as e:
            messagebox.showerror("Figure error", str(e))

    # ══════════════════════════════════════════════════════════
    # COMPONENT 3 — CASE STUDY TAB
    # ══════════════════════════════════════════════════════════
    def build_case_tab(self):
        tk.Label(self.case_tab,
                 text="Component 3 — Case Study UDR Assessment (Student A)",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.case_tab,
                 text="Enter UDR indicator counts (0–4 per domain).\n"
                      "Formula F7: UDR_score(d) = (indicators_present / 4) × 100",
                 font=("Arial", 9), fg="gray").pack()

        frame = tk.Frame(self.case_tab)
        frame.pack(pady=8)

        tk.Label(frame, text="Interview — Claimed AI use behavior",
                 font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=3,
                                                  pady=6, sticky="w", padx=10)
        self.case_claimed = self.labelled_entry(frame,
            "Claimed self-reliance % (Student A stated 80% self, 20% AI)", 1, "80",
            "from interview 80/20 rule")

        tk.Label(frame, text="\nTask A — WITHOUT AI (isPrime program)",
                 font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=3,
                                                  pady=6, sticky="w", padx=10)
        self.ta_u = self.labelled_entry(frame, "Understanding indicators present (0–4)", 3, "0", "F7 — Task A")
        self.ta_d = self.labelled_entry(frame, "Debugging indicators present (0–4)",    4, "0", "F7 — Task A")
        self.ta_r = self.labelled_entry(frame, "Reasoning indicators present (0–4)",    5, "0", "F7 — Task A")

        tk.Label(frame, text="\nTask B — WITH AI (string-reversal bugfix)",
                 font=("Arial", 11, "bold")).grid(row=6, column=0, columnspan=3,
                                                  pady=6, sticky="w", padx=10)
        self.tb_u = self.labelled_entry(frame, "Understanding indicators present (0–4)", 7, "0", "F7 — Task B")
        self.tb_d = self.labelled_entry(frame, "Debugging indicators present (0–4)",    8, "0", "F7 — Task B")
        self.tb_r = self.labelled_entry(frame, "Reasoning indicators present (0–4)",    9, "1", "F7 — Task B (1 partial)")

        tk.Label(frame, text="\nBehavioral observations",
                 font=("Arial", 11, "bold")).grid(row=10, column=0, columnspan=3,
                                                  pady=6, sticky="w", padx=10)
        self.case_dep = self.labelled_entry(frame, "AI dependency level (1–10)",        11, "9",  "9 = very high")

        tk.Label(frame, text="Used AI before thinking independently?").grid(
            row=12, column=0, sticky="w", padx=10, pady=5)
        self.case_ai_before = ttk.Combobox(frame, values=["Yes", "No"], width=18)
        self.case_ai_before.grid(row=12, column=1, sticky="w", padx=10)
        self.case_ai_before.set("Yes")
        tk.Label(frame, text="  ← Task B: photographed task, sent to ChatGPT",
                 font=("Arial", 8), fg="gray").grid(row=12, column=2, sticky="w")

        tk.Label(frame, text="Could explain AI-generated code fixes?").grid(
            row=13, column=0, sticky="w", padx=10, pady=5)
        self.case_explain = ttk.Combobox(frame, values=["Yes", "No"], width=18)
        self.case_explain.grid(row=13, column=1, sticky="w", padx=10)
        self.case_explain.set("No")
        tk.Label(frame, text="  ← Task B debrief: could not explain bugs",
                 font=("Arial", 8), fg="gray").grid(row=13, column=2, sticky="w")

        ttk.Button(self.case_tab, text="Analyze Case Study (F7)",
                   command=self.analyze_case).pack(pady=10)

        self.case_box = ScrolledText(self.case_tab, width=105, height=14,
                                     font=("Consolas", 10))
        self.case_box.pack(padx=10, pady=5)

    def analyze_case(self):
        try:
            claimed = self.get_int(self.case_claimed, "Claimed confidence")
            ta_u    = self.get_int(self.ta_u, "Task A Understanding")
            ta_d    = self.get_int(self.ta_d, "Task A Debugging")
            ta_r    = self.get_int(self.ta_r, "Task A Reasoning")
            tb_u    = self.get_int(self.tb_u, "Task B Understanding")
            tb_d    = self.get_int(self.tb_d, "Task B Debugging")
            tb_r    = self.get_int(self.tb_r, "Task B Reasoning")
            dep     = self.get_int(self.case_dep, "Dependency level")
        except Exception:
            return

        ai_before  = self.case_ai_before.get() == "Yes"
        explain_ai = self.case_explain.get() == "Yes"

        # Validate ranges
        for val, name in [(ta_u,'Task A U'),(ta_d,'Task A D'),(ta_r,'Task A R'),
                          (tb_u,'Task B U'),(tb_d,'Task B D'),(tb_r,'Task B R')]:
            if not 0 <= val <= 4:
                messagebox.showerror("Range error", f"{name} must be 0-4.")
                return
        if not 1 <= dep <= 10:
            messagebox.showerror("Range error", "Dependency must be 1-10.")
            return

        self.case_results = analyze_case_study(
            claimed, ta_u, ta_d, ta_r, tb_u, tb_d, tb_r,
            dep, explain_ai, ai_before)
        r = self.case_results

        self.case_box.delete("1.0", tk.END)
        self.case_box.insert(tk.END, "CASE STUDY MODULE RESULTS — Formula F7: UDR_score = (indicators/4) × 100\n")
        self.case_box.insert(tk.END, "─" * 65 + "\n")
        self.case_box.insert(tk.END, f"Claimed self-reliance (interview): {claimed}%\n\n")
        self.case_box.insert(tk.END, f"TASK A (without AI):\n")
        self.case_box.insert(tk.END, f"  Understanding: {ta_u}/4 indicators = {r['task_a_understanding']}%\n")
        self.case_box.insert(tk.END, f"  Debugging:     {ta_d}/4 indicators = {r['task_a_debugging']}%\n")
        self.case_box.insert(tk.END, f"  Reasoning:     {ta_r}/4 indicators = {r['task_a_reasoning']}%\n")
        self.case_box.insert(tk.END, f"  Average UDR:   {r['task_a_average']}%\n\n")
        self.case_box.insert(tk.END, f"TASK B (with AI):\n")
        self.case_box.insert(tk.END, f"  Understanding: {tb_u}/4 indicators = {r['task_b_understanding']}%\n")
        self.case_box.insert(tk.END, f"  Debugging:     {tb_d}/4 indicators = {r['task_b_debugging']}%\n")
        self.case_box.insert(tk.END, f"  Reasoning:     {tb_r}/4 indicators = {r['task_b_reasoning']}%\n")
        self.case_box.insert(tk.END, f"  Average UDR:   {r['task_b_average']}%\n\n")
        self.case_box.insert(tk.END, f"ILLUSORY COMPETENCE GAP (F7 + F3):\n")
        self.case_box.insert(tk.END, f"  Claimed: {claimed}%  |  Observed (Task A avg): {r['task_a_average']}%\n")
        self.case_box.insert(tk.END, f"  Gap: {r['illusory_gap']} pts — {r['illusory_competence']}\n")
        self.case_box.insert(tk.END, f"  Classification: {r['classification']}\n\n")
        self.case_box.insert(tk.END, f"RQ ANSWERS FROM COMPONENT 3:\n")
        self.case_box.insert(tk.END, f"  {r['rq1_answer']}\n")
        self.case_box.insert(tk.END, f"  {r['rq2_answer']}\n")
        self.case_box.insert(tk.END, f"  {r['rq3_answer']}\n")
        self.case_box.insert(tk.END, f"  {r['rq4_answer']}\n")

    # ══════════════════════════════════════════════════════════
    # INTEGRATED RESULTS TAB
    # ══════════════════════════════════════════════════════════
    def build_results_tab(self):
        tk.Label(self.results_tab,
                 text="Integrated Findings — Formula F6 Triangulation (RQ1–RQ4)",
                 font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.results_tab,
                 text="Run all three components first, then click Generate to triangulate findings.",
                 font=("Arial", 9), fg="gray").pack()

        btn_frame = tk.Frame(self.results_tab)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Generate Integrated Results (F6)",
                   command=self.final_results).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Save Report to File",
                   command=self.save_report).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Generate All Figures",
                   command=self.save_figures).pack(side="left", padx=8)

        self.results_box = ScrolledText(self.results_tab, width=110, height=32,
                                        font=("Consolas", 10))
        self.results_box.pack(padx=10, pady=5)

    def final_results(self):
        self.results_box.delete("1.0", tk.END)

        # Use demo data for any missing component
        obs  = self.observation_results or __import__('modules.observation_module',
               fromlist=['analyze_observation_demo']).analyze_observation_demo()
        surv = self.survey_results or __import__('modules.survey_module',
               fromlist=['analyze_survey_demo']).analyze_survey_demo()
        case = self.case_results or __import__('modules.case_study_module',
               fromlist=['analyze_case_study_demo']).analyze_case_study_demo()

        final = triangulate(obs, surv, case)
        self._last_final = (obs, surv, case, final)

        self.results_box.insert(tk.END, "FINAL INTEGRATED UDR FINDINGS\n")
        self.results_box.insert(tk.END, "=" * 70 + "\n\n")

        # F6 triangulation status
        self.results_box.insert(tk.END, "FORMULA F6 — TRIANGULATION VALIDITY\n")
        self.results_box.insert(tk.END, "Finding is valid when: C1 AND C2 AND C3 all support it\n\n")
        findings = [
            ('Finding 1: AI dependency as default',    final['finding1_ai_dependency_valid']),
            ('Finding 2: Illusory competence gap',     final['finding2_illusory_competence_valid']),
            ('Finding 3: Debugging most affected',     final['finding3_debugging_affected_valid']),
            ('Finding 4: Dual institutional failure',  final['finding4_institutional_failure_valid']),
        ]
        for label, valid in findings:
            status = "VALID  ✓" if valid else "NOT VALID  ✗"
            self.results_box.insert(tk.END, f"  {label:<42} {status}\n")
        all_valid = final['all_findings_valid']
        self.results_box.insert(tk.END,
            f"\n  All findings valid: {'YES — thesis findings confirmed' if all_valid else 'NO — check component data'}\n")

        # RQ answers
        self.results_box.insert(tk.END, "\n" + "=" * 70 + "\n")
        self.results_box.insert(tk.END, "RESEARCH QUESTIONS — ANSWERS FROM SYSTEM OUTPUT\n")
        self.results_box.insert(tk.END, "=" * 70 + "\n\n")
        for key, label in [('rq1','RQ1'),('rq2','RQ2'),('rq3','RQ3'),('rq4','RQ4')]:
            self.results_box.insert(tk.END, f"{final[key]}\n\n")

        # Key metrics summary
        self.results_box.insert(tk.END, "=" * 70 + "\n")
        self.results_box.insert(tk.END, "KEY METRICS SUMMARY\n")
        self.results_box.insert(tk.END, "=" * 70 + "\n")
        self.results_box.insert(tk.END,
            f"  Survey responses (n):          {final['survey_n']}\n"
            f"  Cohort students:               {final['obs_students']}\n"
            f"  Daily+weekly AI use (F1):      {final['daily_weekly_pct']}%\n"
            f"  Competence gap (F3):           {final['g_competence']} pts\n"
            f"  Social desirability gap (F4):  {final['g_sdb']} pts\n"
            f"  Institutional supply gap (F5): {final['institutional_supply']}%\n"
            f"  Institutional demand (F5):     {final['institutional_demand']}%\n"
            f"  Case study illusory gap:       {final['illusory_gap']} pts\n"
        )

    def save_report(self):
        if not hasattr(self, '_last_final'):
            messagebox.showwarning("No data", "Generate results first.")
            return
        obs, surv, case, final = self._last_final
        generate_text_report(obs, surv, case, final)
        messagebox.showinfo("Saved", "Report saved to outputs/results_report.txt")

    def save_figures(self):
        if not self.survey_results:
            surv = __import__('modules.survey_module',
                              fromlist=['analyze_survey_demo']).analyze_survey_demo()
        else:
            surv = self.survey_results
        try:
            paths = generate_all_figures(surv)
            messagebox.showinfo("Figures saved",
                "5 figures generated:\n" + "\n".join(paths))
        except Exception as e:
            messagebox.showerror("Figure error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = UDRGUI(root)
    root.mainloop()
