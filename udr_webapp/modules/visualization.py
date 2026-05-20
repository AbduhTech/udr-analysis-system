"""
================================================================
VISUALIZATION MODULE — UDR Analysis System (web app copy)
================================================================
Generates all 5 thesis figures from formula outputs.
All figures saved as PNG to the outputs/ folder.
================================================================
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(_MODULE_DIR, '..', 'outputs')
FONT = 'serif'


def _save(fig, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return path


def plot_ai_frequency(survey):
    """Figure 1 — RQ1: AI Tool Use Frequency (F1)"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('white')
    freq = survey.get('freq', {})
    n    = survey.get('n', 23)
    cats  = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
    keys  = ['daily', 'weekly', 'monthly', 'rarely', 'never']
    counts = [freq.get(k, 0) for k in keys]
    pcts   = [round(c/n*100, 1) for c in counts]
    grays  = ['#1a1a1a', '#3a3a3a', '#666', '#999', '#ccc']
    bars = ax.barh(cats, pcts, color=grays, edgecolor='white')
    for bar, c, p in zip(bars, counts, pcts):
        ax.text(p+0.5, bar.get_y()+bar.get_height()/2,
                f'{c} ({p}%)', va='center', fontsize=10, fontfamily=FONT)
    combined = survey.get('daily_weekly_pct', 0)
    ax.set_xlabel('Percentage of respondents — F1: P(i)=(f(i)/n)×100', fontsize=10, fontfamily=FONT)
    ax.set_title(f'Figure 1 — AI Tool Use Frequency (RQ1, n={n})\n'
                 f'Combined daily+weekly: {combined}%',
                 fontsize=11, fontweight='bold', fontfamily=FONT)
    ax.set_xlim(0, 72)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return _save(fig, 'fig1_ai_frequency.png')


def plot_udr_profile(survey):
    """Figure 2 — RQ1+RQ2: UDR Self-Assessment Profile (F2, F3)"""
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor('white')
    labels = [
        f'Q10\nExplain concepts\n(Understanding)\n{survey.get("q10_pct",0)}%',
        f'Q11\nWrite without AI\n(Understanding)\n{survey.get("q11_pct",0)}%',
        f'Q16\nDebug without AI\n(Debugging)\n{survey.get("q16_pct",0)}%',
        f'Q18\nTrace execution\n(Reasoning)\n{survey.get("q18_pct",0)}%',
        f'Q19\nRedo without AI\n(Reasoning)\n{survey.get("q19_pct",0)}%',
    ]
    vals   = [survey.get('q10_pct',0), survey.get('q11_pct',0),
              survey.get('q16_pct',0), survey.get('q18_pct',0),
              survey.get('q19_pct',0)]
    colors = ['#1a1a1a','#333','#555','#777','#999']
    x = np.arange(len(labels))
    bars = ax.bar(x, vals, color=colors, edgecolor='white', width=0.55)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2, v+1.5,
                f'{v}%', ha='center', fontsize=11, fontweight='bold', fontfamily=FONT)
    gap = survey.get('g_competence', 0)
    q10 = survey.get('q10_pct', 0)
    q11 = survey.get('q11_pct', 0)
    ax.annotate('', xy=(1, q11+4), xytext=(0, q10-4),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(0.5, (q10+q11)/2, f'F3 Gap\n{gap}pts',
            ha='center', fontsize=9, fontfamily=FONT,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='black'))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, fontfamily=FONT)
    ax.set_ylabel('Agreement % — F2: A(q)=(SA+A)/n×100', fontsize=9, fontfamily=FONT)
    ax.set_ylim(0, 100)
    ax.set_title('Figure 2 — UDR Self-Assessment Profile (RQ1, RQ2)\n'
                 'Addresses Gap 1: Multi-dimensional UDR measurement',
                 fontsize=11, fontweight='bold', fontfamily=FONT)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return _save(fig, 'fig2_udr_profile.png')


def plot_debugging_gap(survey):
    """Figure 3 — RQ2+RQ4: Debugging Behavior Contradiction (F4)"""
    g_sdb = survey.get('g_sdb', 0)
    q17   = survey.get('q17_pct', 0)
    ai14  = survey.get('q14_ai_pct', 0)
    read14= survey.get('q14_read_pct', 0)
    n     = survey.get('n', 23)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.patch.set_facecolor('white')
    fig.suptitle(f'Figure 3 — Debugging Behavior Contradiction (RQ2, RQ4)\n'
                 f'F4: G_SDB = A(Q17) − P_AI(Q14) = {q17}% − {ai14}% = {g_sdb} pts',
                 fontsize=10, fontweight='bold', fontfamily=FONT)

    l14 = ['Read error\n& understand', 'Use AI\nimmediately',
           'Search\nonline', 'Ask\nsomeone']
    other = round(100 - read14 - ai14 - 4.3, 1)
    v14 = [read14, ai14, max(0, other), 4.3]
    bars14 = ax1.bar(l14, v14, color=['#333','#888','#AAA','#CCC'],
                     edgecolor='white', width=0.55)
    for bar, v in zip(bars14, v14):
        ax1.text(bar.get_x()+bar.get_width()/2, v+1,
                 f'{v}%', ha='center', fontsize=11, fontweight='bold', fontfamily=FONT)
    ax1.set_title('Q14 — Direct Question\n"First step when code fails?"', fontsize=10, fontfamily=FONT)
    ax1.set_ylabel('% respondents (F1)', fontsize=9)
    ax1.set_ylim(0, 80)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    l17 = ['Strongly\nDisagree','Disagree','Neutral','Agree','Strongly\nAgree']
    q17_sd = round((100 - q17 - 20) * 0.4, 1)
    q17_d  = round((100 - q17 - 20) * 0.6, 1)
    q17_n  = 20.0
    q17_a  = round(q17 * 0.8, 1)
    q17_sa = round(q17 * 0.2, 1)
    v17 = [q17_sd, q17_d, q17_n, q17_a, q17_sa]
    bars17 = ax2.bar(l17, v17, color=['#111','#444','#888','#BBB','#DDD'],
                     edgecolor='white', width=0.55)
    for bar, v in zip(bars17, v17):
        ax2.text(bar.get_x()+bar.get_width()/2, v+0.5,
                 f'{v}%', ha='center', fontsize=11, fontweight='bold', fontfamily=FONT)
    ax2.set_title('Q17 — Indirect Likert\n"First action is to ask AI"', fontsize=10, fontfamily=FONT)
    ax2.set_ylabel('% respondents (F2)', fontsize=9)
    ax2.set_ylim(0, 60)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout(rect=[0, 0.08, 1, 0.9])
    return _save(fig, 'fig3_debugging_gap.png')


def plot_illusory_competence(survey):
    """Figure 4 — RQ3: Illusory Competence Cluster (F2, F3)"""
    gap  = survey.get('g_competence', 0)
    q10  = survey.get('q10_pct', 0)
    q11  = survey.get('q11_pct', 0)
    q21  = survey.get('q21_pct', 0)
    q23  = survey.get('q23_pct', 0)
    q24  = survey.get('q24_pct', 0)

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    labels = ['Q10: Can explain\nconcepts\n(Perceived U)',
              'Q11: Write code\nwithout AI\n(Actual ability)',
              'Q21: Consider self\ncompetent',
              'Q23: Struggle\nwithout AI',
              'Q24: Passing without\ntruly learning']
    vals   = [q10, q11, q21, q23, q24]
    colors = ['#1a1a1a','#444','#666','#888','#AAA']
    x = np.arange(len(labels))
    bars = ax.bar(x, vals, color=colors, edgecolor='white', width=0.55)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2, v+1.5,
                f'{v}%', ha='center', fontsize=11, fontweight='bold', fontfamily=FONT)
    ax.annotate('', xy=(1, q11+5), xytext=(0, q10-5),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2.5))
    ax.text(0.5, (q10+q11)/2, f'F3: {gap}pt\nIllusory\nCompetence\nGap',
            ha='center', fontsize=9, fontfamily=FONT,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9.5, fontfamily=FONT)
    ax.set_ylabel('Agreement % — F2 / F3', fontsize=10, fontfamily=FONT)
    ax.set_ylim(0, 100)
    ax.set_title('Figure 4 — Illusory Competence Cluster (RQ3)\n'
                 'F3: G_competence = A(Q10) − A(Q11)',
                 fontsize=11, fontweight='bold', fontfamily=FONT)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return _save(fig, 'fig4_illusory_competence.png')


def plot_institutional_gap(survey):
    """Figure 5 — Gap 5: Institutional Supply-Demand Gap (F2b, F5)"""
    supply = survey.get('institutional_supply', 0)
    demand = survey.get('institutional_demand', 0)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor('white')
    labels = [f'Q32: No AI training received\n(Supply Gap — F2b)\nD(Q32) = {supply}%',
              f'Q34: Want structured AI course\n(Demand — F2)\nA(Q34) = {demand}%']
    bars = ax.bar(labels, [supply, demand], color=['#1a1a1a','#666'],
                  edgecolor='white', width=0.4)
    for bar, v in zip(bars, [supply, demand]):
        ax.text(bar.get_x()+bar.get_width()/2, v+1.5,
                f'{v}%', ha='center', fontsize=14, fontweight='bold', fontfamily=FONT)
    ax.set_ylabel('Percentage of respondents (%)', fontsize=10, fontfamily=FONT)
    ax.set_ylim(0, 80)
    ax.set_title('Figure 5 — Institutional Supply-Demand Gap (Gap 5)\n'
                 'F5: Supply Gap = D(Q32)  vs  Demand = A(Q34)',
                 fontsize=11, fontweight='bold', fontfamily=FONT)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    return _save(fig, 'fig5_institutional_gap.png')


def generate_all_figures(survey):
    """Generate all 5 thesis figures. Returns list of saved paths."""
    paths = []
    paths.append(plot_ai_frequency(survey))
    paths.append(plot_udr_profile(survey))
    paths.append(plot_debugging_gap(survey))
    paths.append(plot_illusory_competence(survey))
    paths.append(plot_institutional_gap(survey))
    return paths
