"""
refined_visualize.py - Rozbudowana wizualizacja wyników Refined (A4, A11, A12).
Generuje: summary_bar, grid_heatmap, time_comparison.
"""
import os
import sys
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_CSV = os.path.join(BASE_DIR, 'results', 'refined_results.csv')
PLOTS_DIR = os.path.join(BASE_DIR, 'plots')

SHORT_NAMES = {
    'A4_Standard': 'A4-Standard',
    'A4_Refined':  'A4-Refined',
    'A11_Refined': 'A11-Refined',
    'A12_Refined': 'A12-Refined',
}

def load_data():
    rows = []
    if not os.path.exists(RESULTS_CSV): return rows
    with open(RESULTS_CSV, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            n = None if r['n_circles'] in ['DNF', 'ERR'] else int(r['n_circles'])
            t = float(r['time_s'])
            rows.append({**r, 'n': n, 't': t})
    return rows

def build_matrices(rows):
    shapes = sorted(list(dict.fromkeys(r['shape_id'] for r in rows)))
    algos = sorted(list(dict.fromkeys(r['algorithm'] for r in rows)))
    mat_n = np.full((len(shapes), len(algos)), np.nan)
    mat_t = np.full((len(shapes), len(algos)), np.nan)
    names = {}
    for r in rows:
        si, ai = shapes.index(r['shape_id']), algos.index(r['algorithm'])
        mat_n[si, ai] = r['n']
        mat_t[si, ai] = r['t']
        names[r['shape_id']] = r['shape_name']
    return shapes, algos, mat_n, mat_t, names

def plot_heatmap(shapes, algos, mat_n, shape_names):
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(mat_n.T, cmap='RdYlGn_r', aspect='auto')
    ax.set_xticks(range(len(shapes)))
    ax.set_xticklabels([f"{s}\n{shape_names[s]}" for s in shapes], fontsize=8, rotation=35, ha='right')
    ax.set_yticks(range(len(algos)))
    ax.set_yticklabels([SHORT_NAMES.get(a, a) for a in algos])
    for i in range(len(shapes)):
        for j in range(len(algos)):
            ax.text(i, j, int(mat_n[i, j]), ha='center', va='center', fontweight='bold')
    plt.title('Refined Algorithms: Circles Count Heatmap')
    plt.colorbar(im, label='Count')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'refined_grid_heatmap.png'), dpi=150)
    plt.close()

def plot_summary(algos, mat_n, mat_t):
    avg_n = np.nanmean(mat_n, axis=0)
    avg_t = np.nanmean(mat_t, axis=0)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Ranking Bar
    axes[0].barh([SHORT_NAMES.get(a, a) for a in algos], avg_n, color='#5fb2ff')
    axes[0].set_title('Average Circles Count (Lower is Better)')
    axes[0].invert_yaxis()
    for i, v in enumerate(avg_n):
        axes[0].text(v + 0.1, i, f"{v:.1f}", va='center', fontweight='bold')
    
    # Scatter Time vs Quality
    for i, a in enumerate(algos):
        axes[1].scatter(avg_t[i], avg_n[i], s=150, label=SHORT_NAMES.get(a, a))
        axes[1].annotate(SHORT_NAMES.get(a, a), (avg_t[i], avg_n[i]), xytext=(5, 5), textcoords='offset points')
    axes[1].set_title('Tradeoff: Time vs Quality')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Circles')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'refined_summary_bar.png'), dpi=150)
    plt.close()

def plot_time_comparison(algos, mat_t, mat_n):
    avg_t = np.nanmean(mat_t, axis=0)
    avg_n = np.nanmean(mat_n, axis=0)
    order = np.argsort(avg_t)
    
    plt.figure(figsize=(10, 6))
    y_pos = np.arange(len(algos))
    plt.barh(y_pos, [avg_t[i] for i in order], color='#ff9f43', edgecolor='black')
    plt.yticks(y_pos, [SHORT_NAMES.get(algos[i], algos[i]) for i in order])
    plt.xlabel('Average Time (s)')
    plt.title('Refined Algorithms Time Comparison')
    for i, idx in enumerate(order):
        plt.text(avg_t[idx], i, f" {avg_t[idx]:.3f}s (Avg N: {avg_n[idx]:.1f})", va='center')
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'refined_time_comparison.png'), dpi=150)
    plt.close()

def main():
    rows = load_data()
    if not rows: return
    os.makedirs(PLOTS_DIR, exist_ok=True)
    shapes, algos, mat_n, mat_t, names = build_matrices(rows)
    plot_heatmap(shapes, algos, mat_n, names)
    plot_summary(algos, mat_n, mat_t)
    plot_time_comparison(algos, mat_t, mat_n)
    print(f"Wygenerowano komplet wykresów w {PLOTS_DIR}")

if __name__ == '__main__':
    main()
