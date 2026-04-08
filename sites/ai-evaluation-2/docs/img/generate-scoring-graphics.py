#!/usr/bin/env python3
"""Generate 4 scoring visualization SVGs for the AI Toolchain Evaluation."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

# --- DATA ---
factors = [
    ("EF-01", "Total Cost of Ownership", "Economics", 0.15),
    ("EF-02", "Cost Predictability", "Economics", 0.08),
    ("EF-03", "Cost Scaling", "Economics", 0.06),
    ("EF-04", "Output Quality", "Quality & Capability", 0.18),
    ("EF-05", "Domain Context Awareness", "Quality & Capability", 0.08),
    ("EF-06", "Tool Integration Breadth", "Quality & Capability", 0.03),
    ("EF-07", "Multi-Model Flexibility", "Quality & Capability", 0.03),
    ("EF-13", "Content Retrieval Quality", "Quality & Capability", 0.05),
    ("EF-08", "Time to Value", "Operational Fitness", 0.08),
    ("EF-09", "Operational Complexity", "Operational Fitness", 0.07),
    ("EF-10", "Workflow Integration", "Operational Fitness", 0.05),
    ("EF-11", "Vendor Lock-in Risk", "Strategic & Risk", 0.08),
    ("EF-12", "Governance & Compliance", "Strategic & Risk", 0.06),
]

scores_a = [5, 5, 5, 5, 5, 4, 4, 4, 5, 5, 5, 4, 5]
scores_b = [2, 2, 3, 3, 4, 4, 5, 4, 3, 2, 4, 4, 3]
scores_c = [2, 1, 2, 2, 3, 3, 3, 2, 1, 1, 2, 1, 4]

weighted_a = sum(s * f[3] for s, f in zip(scores_a, factors))
weighted_b = sum(s * f[3] for s, f in zip(scores_b, factors))
weighted_c = sum(s * f[3] for s, f in zip(scores_c, factors))

categories = ["Economics\n(29%)", "Quality &\nCapability (37%)", "Operational\nFitness (20%)", "Strategic &\nRisk (14%)"]
cat_indices = [
    [0, 1, 2],       # Economics
    [3, 4, 5, 6, 7], # Quality
    [8, 9, 10],       # Operational
    [11, 12],         # Strategic
]

# --- COLORS ---
SCORE_COLORS = {
    5: '#1b5e20',  # dark green
    4: '#4caf50',  # green
    3: '#fdd835',  # yellow
    2: '#ff9800',  # orange
    1: '#d32f2f',  # red
}
SCORE_TEXT_COLORS = {
    5: 'white',
    4: 'white',
    3: '#333333',
    2: '#333333',
    1: 'white',
}
SCORE_LABELS = {
    5: 'Excellent',
    4: 'Good',
    3: 'Adequate',
    2: 'Weak',
    1: 'Critical Failure',
}

OPT_A_COLOR = '#1565c0'  # blue
OPT_B_COLOR = '#00897b'  # teal
OPT_C_COLOR = '#78909c'  # blue-grey

CAT_BG_COLORS = ['#e3f2fd', '#e8f5e9', '#fff3e0', '#fce4ec']

FIGURE_WIDTH = 14  # ~1200px at 86dpi
DPI = 100


def add_score_legend(ax, x=0.0, y=-0.12, fontsize=9):
    """Add color-coded score legend below a chart."""
    patches = []
    for score in [5, 4, 3, 2, 1]:
        patches.append(mpatches.Patch(
            facecolor=SCORE_COLORS[score],
            edgecolor='#999999',
            label=f'{score} — {SCORE_LABELS[score]}'
        ))
    ax.legend(
        handles=patches, loc='upper center',
        bbox_to_anchor=(0.5, y), ncol=5, fontsize=fontsize,
        frameon=True, fancybox=True, shadow=False,
        edgecolor='#cccccc', facecolor='white',
        handlelength=1.5, handleheight=1.2,
        title='Score Legend', title_fontsize=fontsize + 1,
    )


def add_option_legend(ax, x=0.5, y=-0.10, fontsize=10, include_totals=False):
    """Add option color legend."""
    labels = [
        f'Option A — GitHub Copilot' + (f'  ({weighted_a:.2f})' if include_totals else ''),
        f'Option B — Roo Code + Kong' + (f'  ({weighted_b:.2f})' if include_totals else ''),
        f'Option C — Bespoke Agent' + (f'  ({weighted_c:.2f})' if include_totals else ''),
    ]
    patches = [
        mpatches.Patch(facecolor=OPT_A_COLOR, label=labels[0]),
        mpatches.Patch(facecolor=OPT_B_COLOR, label=labels[1]),
        mpatches.Patch(facecolor=OPT_C_COLOR, label=labels[2]),
    ]
    ax.legend(
        handles=patches, loc='upper center',
        bbox_to_anchor=(x, y), ncol=3, fontsize=fontsize,
        frameon=True, fancybox=True, shadow=False,
        edgecolor='#cccccc', facecolor='white',
        handlelength=1.5, handleheight=1.2,
    )


# ============================================================================
# GRAPHIC 1: HEAT MAP SCORECARD
# ============================================================================
def create_heatmap():
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 8.5), dpi=DPI)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-1.5, len(factors) + 2.5)
    ax.axis('off')

    # Title
    ax.text(1.5, len(factors) + 2.0, 'AI Toolchain Evaluation — Scoring Heat Map',
            ha='center', va='center', fontsize=18, fontweight='bold', color='#212121')
    ax.text(1.5, len(factors) + 1.3, 'Each cell scored 1–5. Color reveals the pattern: green = strong, red = critical failure.',
            ha='center', va='center', fontsize=11, color='#616161')

    # Column headers
    col_labels = ['Option A\nGitHub Copilot', 'Option B\nRoo Code + Kong', 'Option C\nBespoke Agent']
    for j, label in enumerate(col_labels):
        colors = [OPT_A_COLOR, OPT_B_COLOR, OPT_C_COLOR]
        ax.add_patch(plt.Rectangle((j + 0.52, len(factors) + 0.05), 0.96, 0.7,
                                    facecolor=colors[j], edgecolor='white', linewidth=1, zorder=3))
        ax.text(j + 1.0, len(factors) + 0.4, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=4)

    # Factor label column header
    ax.add_patch(plt.Rectangle((-0.48, len(factors) + 0.05), 1.0, 0.7,
                                facecolor='#37474f', edgecolor='white', linewidth=1, zorder=3))
    ax.text(0.02, len(factors) + 0.4, 'Evaluation Factor', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white', zorder=4)

    # Draw category separators and cells
    current_cat = None
    cat_start = None
    cat_idx = 0

    for i, (fid, fname, fcat, fweight) in enumerate(factors):
        row_y = len(factors) - 1 - i

        # Category grouping background
        if fcat != current_cat:
            if current_cat is not None:
                # Draw category background
                h = cat_start - row_y
                ax.add_patch(plt.Rectangle((-0.48, row_y + 0.98), 4.0, h + 0.04,
                                            facecolor=CAT_BG_COLORS[cat_idx], edgecolor='none',
                                            alpha=0.3, zorder=0))
                cat_idx += 1
            current_cat = fcat
            cat_start = row_y

        # Factor label
        weight_pct = int(fweight * 100)
        ax.text(-0.45, row_y + 0.5, f'{fid}: {fname} ({weight_pct}%)',
                ha='left', va='center', fontsize=9.5, color='#212121', zorder=5)

        # Score cells
        for j, score in enumerate([scores_a[i], scores_b[i], scores_c[i]]):
            color = SCORE_COLORS[score]
            text_color = SCORE_TEXT_COLORS[score]
            ax.add_patch(plt.Rectangle((j + 0.52, row_y + 0.02), 0.96, 0.96,
                                        facecolor=color, edgecolor='white', linewidth=2, zorder=3))
            ax.text(j + 1.0, row_y + 0.5, str(score), ha='center', va='center',
                    fontsize=14, fontweight='bold', color=text_color, zorder=4)

    # Last category background
    row_y_last = len(factors) - 1 - (len(factors) - 1)
    h = cat_start - row_y_last
    ax.add_patch(plt.Rectangle((-0.48, row_y_last - 0.02), 4.0, h + 1.04,
                                facecolor=CAT_BG_COLORS[cat_idx], edgecolor='none',
                                alpha=0.3, zorder=0))

    # Weighted totals row
    total_y = -1.0
    ax.add_patch(plt.Rectangle((-0.48, total_y + 0.02), 1.0, 0.76,
                                facecolor='#37474f', edgecolor='white', linewidth=1, zorder=3))
    ax.text(0.02, total_y + 0.4, 'WEIGHTED TOTAL', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white', zorder=4)

    for j, (total, color) in enumerate([(weighted_a, OPT_A_COLOR), (weighted_b, OPT_B_COLOR), (weighted_c, OPT_C_COLOR)]):
        ax.add_patch(plt.Rectangle((j + 0.52, total_y + 0.02), 0.96, 0.76,
                                    facecolor=color, edgecolor='white', linewidth=2, zorder=3))
        ax.text(j + 1.0, total_y + 0.4, f'{total:.2f}', ha='center', va='center',
                fontsize=14, fontweight='bold', color='white', zorder=4)

    # Score legend
    add_score_legend(ax, y=-0.08, fontsize=9)

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-heatmap.svg'),
                format='svg', bbox_inches='tight', dpi=DPI)
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-heatmap.png'),
                format='png', bbox_inches='tight', dpi=200, facecolor='white')
    plt.close(fig)
    print('Created: scoring-heatmap.svg + .png')


# ============================================================================
# GRAPHIC 2: HORIZONTAL BAR CHART (WEIGHTED TOTALS)
# ============================================================================
def create_bar_chart():
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 4.5), dpi=DPI)

    options = ['Option C\nBespoke Agent', 'Option B\nRoo Code + Kong', 'Option A\nGitHub Copilot']
    totals = [weighted_c, weighted_b, weighted_a]
    colors = [OPT_C_COLOR, OPT_B_COLOR, OPT_A_COLOR]

    bars = ax.barh(options, totals, color=colors, height=0.55, edgecolor='white', linewidth=1.5)

    # Score labels on bars
    for bar, total in zip(bars, totals):
        ax.text(bar.get_width() - 0.15, bar.get_y() + bar.get_height() / 2,
                f'{total:.2f}', ha='right', va='center',
                fontsize=16, fontweight='bold', color='white')

    # Max line
    ax.axvline(x=5.0, color='#bdbdbd', linestyle='--', linewidth=1, alpha=0.7)
    ax.text(5.0, 2.35, 'Max: 5.00', ha='center', va='bottom', fontsize=9, color='#9e9e9e')

    ax.set_xlim(0, 5.5)
    ax.set_xlabel('Weighted Score (1–5 scale)', fontsize=11, color='#424242')
    ax.set_title('AI Toolchain Evaluation — Weighted Score Comparison',
                 fontsize=16, fontweight='bold', color='#212121', pad=15)
    ax.tick_params(axis='y', labelsize=11)
    ax.tick_params(axis='x', labelsize=10)

    # Margin annotation
    ax.annotate(f'Margin: {weighted_a - weighted_b:.2f} pts',
                xy=(weighted_a, 2), xytext=(weighted_a + 0.3, 1.5),
                fontsize=10, color=OPT_A_COLOR, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=OPT_A_COLOR, lw=1.5))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e0e0e0')
    ax.spines['bottom'].set_color('#e0e0e0')

    plt.tight_layout()
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-bar-chart.svg'),
                format='svg', bbox_inches='tight', dpi=DPI)
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-bar-chart.png'),
                format='png', bbox_inches='tight', dpi=200, facecolor='white')
    plt.close(fig)
    print('Created: scoring-bar-chart.svg + .png')


# ============================================================================
# GRAPHIC 3: RADAR / SPIDER CHART
# ============================================================================
def create_radar():
    # Use short labels for radar
    labels = [f[0] for f in factors]
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    sa = scores_a + scores_a[:1]
    sb = scores_b + scores_b[:1]
    sc = scores_c + scores_c[:1]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 9), dpi=DPI,
                            subplot_kw=dict(polar=True))

    # Radar-specific colors — higher contrast than shared palette
    RADAR_A = '#1565c0'  # blue
    RADAR_B = '#f57c00'  # warm orange (complementary to blue)
    RADAR_C = '#6a1b9a'  # deep purple

    # Draw the polygons
    ax.fill(angles, sa, alpha=0.15, color=RADAR_A)
    ax.plot(angles, sa, color=RADAR_A, linewidth=2.5, label=f'Option A — GitHub Copilot ({weighted_a:.2f})')
    ax.scatter(angles[:-1], scores_a, color=RADAR_A, s=50, zorder=5)

    ax.fill(angles, sb, alpha=0.10, color=RADAR_B)
    ax.plot(angles, sb, color=RADAR_B, linewidth=2.0, linestyle='--', label=f'Option B — Roo Code + Kong ({weighted_b:.2f})')
    ax.scatter(angles[:-1], scores_b, color=RADAR_B, s=40, zorder=5)

    ax.fill(angles, sc, alpha=0.10, color=RADAR_C)
    ax.plot(angles, sc, color=RADAR_C, linewidth=2.0, linestyle=':', label=f'Option C — Bespoke Agent ({weighted_c:.2f})')
    ax.scatter(angles[:-1], scores_c, color=RADAR_C, s=40, zorder=5)

    ax.set_xticks(angles[:-1])
    # Build rich labels with factor name
    rich_labels = [f'{f[0]}\n{f[1]}' for f in factors]
    ax.set_xticklabels(rich_labels, fontsize=8.5)
    ax.set_ylim(0, 5.5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8, color='#757575')
    ax.set_rlabel_position(30)

    # Highlight critical failure zone
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.fill_between(theta, 0, 1.5, alpha=0.05, color='red')

    ax.set_title('AI Toolchain Evaluation — Factor Profile Comparison',
                 fontsize=16, fontweight='bold', color='#212121', pad=30, y=1.05)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              ncol=3, fontsize=10, frameon=True, fancybox=True,
              edgecolor='#cccccc', facecolor='white')

    plt.tight_layout(rect=[0, 0.05, 1, 0.98])
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-radar.svg'),
                format='svg', bbox_inches='tight', dpi=DPI)
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-radar.png'),
                format='png', bbox_inches='tight', dpi=200, facecolor='white')
    plt.close(fig)
    print('Created: scoring-radar.svg + .png')


# ============================================================================
# GRAPHIC 4: STACKED BAR CHART BY CATEGORY
# ============================================================================
def create_stacked_bars():
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, 6), dpi=DPI)

    # Calculate category subtotals (weighted contribution to final score)
    cat_names_short = ['Economics\n(29%)', 'Quality &\nCapability (37%)', 'Operational\nFitness (20%)', 'Strategic &\nRisk (14%)']

    cat_weighted = {'A': [], 'B': [], 'C': []}
    for indices in cat_indices:
        wa = sum(factors[i][3] * scores_a[i] for i in indices)
        wb = sum(factors[i][3] * scores_b[i] for i in indices)
        wc = sum(factors[i][3] * scores_c[i] for i in indices)
        cat_weighted['A'].append(wa)
        cat_weighted['B'].append(wb)
        cat_weighted['C'].append(wc)

    x = np.arange(len(cat_names_short))
    width = 0.25

    bars_a = ax.bar(x - width, cat_weighted['A'], width, color=OPT_A_COLOR, edgecolor='white', linewidth=1.2, label=f'Option A ({weighted_a:.2f})')
    bars_b = ax.bar(x, cat_weighted['B'], width, color=OPT_B_COLOR, edgecolor='white', linewidth=1.2, label=f'Option B ({weighted_b:.2f})')
    bars_c = ax.bar(x + width, cat_weighted['C'], width, color=OPT_C_COLOR, edgecolor='white', linewidth=1.2, label=f'Option C ({weighted_c:.2f})')

    # Value labels on bars
    for bars in [bars_a, bars_b, bars_c]:
        for bar in bars:
            height = bar.get_height()
            if height >= 0.15:
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.02,
                        f'{height:.2f}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='#424242')

    ax.set_xticks(x)
    ax.set_xticklabels(cat_names_short, fontsize=11)
    ax.set_ylabel('Weighted Score Contribution', fontsize=11, color='#424242')
    ax.set_title('AI Toolchain Evaluation — Score Breakdown by Category',
                 fontsize=16, fontweight='bold', color='#212121', pad=15)
    ax.set_ylim(0, max(cat_weighted['A']) * 1.25)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e0e0e0')
    ax.spines['bottom'].set_color('#e0e0e0')
    ax.tick_params(axis='y', labelsize=10)

    # Max possible contribution line per category
    cat_max = []
    for indices in cat_indices:
        cat_max.append(sum(factors[i][3] * 5 for i in indices))

    for i, m in enumerate(cat_max):
        ax.plot([i - width * 1.5, i + width * 1.5], [m, m],
                color='#bdbdbd', linestyle='--', linewidth=1, alpha=0.7)
        ax.text(i + width * 1.6, m, f'Max: {m:.2f}', fontsize=8, color='#9e9e9e', va='center')

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
              ncol=3, fontsize=11, frameon=True, fancybox=True,
              edgecolor='#cccccc', facecolor='white',
              handlelength=1.5, handleheight=1.2)

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-stacked-bars.svg'),
                format='svg', bbox_inches='tight', dpi=DPI)
    fig.savefig(os.path.join(os.path.dirname(__file__), 'scoring-stacked-bars.png'),
                format='png', bbox_inches='tight', dpi=200, facecolor='white')
    plt.close(fig)
    print('Created: scoring-stacked-bars.svg + .png')


if __name__ == '__main__':
    create_heatmap()
    create_bar_chart()
    create_radar()
    create_stacked_bars()
    print('\nAll 4 graphics generated successfully.')
