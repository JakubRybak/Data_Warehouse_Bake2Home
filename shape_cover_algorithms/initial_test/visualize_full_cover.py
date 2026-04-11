"""
visualize_full_cover.py - Benchmark summary plots, filtered ONLY for algorithms with 100% coverage.

Generates:
  plots/full_cover/grid_heatmap.png
  plots/full_cover/summary_bar.png
  plots/full_cover/per_shape/<shape>.png
  plots/full_cover/time_comparison.png
"""
import os
import sys
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

RESULTS_CSV = os.path.join(HERE, 'results', 'results.csv')
PLOTS_DIR   = os.path.join(HERE, 'plots', 'full_cover')
PER_SHAPE   = os.path.join(PLOTS_DIR, 'per_shape')

# Mapping for nicer labels in plots
SHORT_NAMES = {
    'A1_Square_Grid':       'A1\nSq.Grid',
    'A2_Hex_Grid':          'A2\nHex',
    'A3_Square_Shift':      'A3\nSq.Shift',
    'A4_Hex_Shift':         'A4\nHex+Shift',
    'A5_Greedy_Discrete':   'A5\nGreedy-D',
    'A6_Greedy_Continuous': 'A6\nGreedy-C',
    'A7_Voronoi_Relax':     'A7\nVoronoi',
    'A8_Genetic':           'A8\nGenetic',
    'A9_SA':                'A9\nSA',
    'A10_Hybrid':           'A10\nHybrid',
    'A11_Adaptive_Hex':     'A11\nAdapt Hex',
    'A12_PSO_Hex':          'A12\nPSO Hex',
}

def load(csv_path=RESULTS_CSV):
    rows = []
    algo_covs = {}
    with open(csv_path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            n = None if r['n_circles'] == 'DNF' else int(r['n_circles'])
            t = float(r['time_s']) if r['time_s'] else 0.0
            cov = float(r['coverage_pct']) if r['coverage_pct'] and r['coverage_pct'] != 'DNF' else 0.0
            
            algo = r['algorithm']
            if algo not in algo_covs:
                algo_covs[algo] = []
            algo_covs[algo].append(cov)
                
            rows.append({**r, 'n': n, 't': t, 'cov': cov})
            
    # Filtrujemy WYŁĄCZNIE te algorytmy, które matematycznie GWARANTUJĄ 100% krycia siatką.
    # Odrzucamy wszystkie heurystyczne, które jedynie "zdają test" z wynikiem 100.0%.
    guaranteed_algos = {
        'A1_Square_Grid', 'A2_Hex_Grid', 'A3_Square_Shift', 
        'A4_Hex_Shift', 'A11_Adaptive_Hex', 'A12_PSO_Hex'
    }
    
    full_cover_algos = {a for a in algo_covs.keys() if a in guaranteed_algos}
    
    print(f"Znalezione algorytmy z idealnym kryciem: {sorted(list(full_cover_algos))}")
    
    filtered_rows = [r for r in rows if r['algorithm'] in full_cover_algos]
    return filtered_rows

def build_matrices(rows):
    shapes = list(dict.fromkeys(r['shape_id']   for r in rows))
    algos  = list(dict.fromkeys(r['algorithm']  for r in rows))
    mat_n  = np.full((len(shapes), len(algos)), np.nan)
    mat_t  = np.full((len(shapes), len(algos)), np.nan)
    shape_names = {}
    for r in rows:
        si = shapes.index(r['shape_id'])
        ai = algos.index(r['algorithm'])
        if r['n'] is not None:
            mat_n[si, ai] = r['n']
        mat_t[si, ai] = r['t']
        shape_names[r['shape_id']] = r['shape_name']
    return shapes, algos, mat_n, mat_t, shape_names

def plot_heatmap(shapes, algos, mat_n, shape_names):
    fig, ax = plt.subplots(figsize=(max(12, len(shapes) * 1.1),
                                    max(7, len(algos) * 0.9)))

    display = mat_n.copy()
    nan_mask = np.isnan(display)
    vmax = np.nanmax(display) if not np.all(nan_mask) else 1
    display[nan_mask] = vmax * 1.2   # DNF as worst color

    im = ax.imshow(display.T, aspect='auto', cmap='RdYlGn_r',
                   vmin=np.nanmin(mat_n), vmax=vmax)

    ax.set_xticks(range(len(shapes)))
    ax.set_xticklabels([f"{s}\n{shape_names[s]}" for s in shapes],
                       fontsize=8, rotation=30, ha='right')
    ax.set_yticks(range(len(algos)))
    ax.set_yticklabels([SHORT_NAMES.get(a, a) for a in algos], fontsize=8)

    for i, s in enumerate(shapes):
        for j, a in enumerate(algos):
            val = mat_n[i, j]
            txt = 'DNF' if np.isnan(val) else str(int(val))
            color = 'white' if np.isnan(val) else 'black'
            ax.text(i, j, txt, ha='center', va='center',
                    fontsize=8, color=color, fontweight='bold')

    plt.colorbar(im, ax=ax, label='Circles count (lower is better)', shrink=0.8)
    ax.set_xlabel('Shape')
    ax.set_ylabel('Algorithm')
    ax.set_title('100% COVERAGE GUARANTEED - Heatmap: Shapes x Algorithms\n(color = circle count)',
                 fontsize=13, pad=12)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, 'full_cover_grid_heatmap.png')
    plt.savefig(out, dpi=150)
    plt.close()

def plot_summary(algos, mat_n, mat_t):
    avg_n = [np.nanmean(mat_n[:, j]) for j in range(len(algos))]
    avg_t = [np.nanmean(mat_t[:, j]) for j in range(len(algos))]
    dnf_counts = [int(np.sum(np.isnan(mat_n[:, j]))) for j in range(len(algos))]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    cmap = plt.cm.RdYlGn_r
    norm = mcolors.Normalize(vmin=min(avg_n), vmax=max(avg_n))
    colors = [cmap(norm(v)) for v in avg_n]

    # Bar chart: ranking based on average circle count
    order = np.argsort(avg_n)
    bars = axes[0].barh(
        [SHORT_NAMES.get(algos[i], algos[i]).replace('\n', ' ') for i in order],
        [avg_n[i] for i in order],
        color=[colors[i] for i in order],
        edgecolor='white', linewidth=0.5,
    )
    for bar, i in zip(bars, order):
        dnf = dnf_counts[i]
        label = f"{avg_n[i]:.1f}" + (f"  (DNF:{dnf})" if dnf else "")
        axes[0].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                     label, va='center', fontsize=8)
    axes[0].set_xlabel('Avg. circle count (completed tests)')
    axes[0].set_title('Ranking: Average Circle Count (Only 100% Covers)')
    axes[0].grid(True, axis='x', alpha=0.3)

    # Scatter: time vs quality
    ax2 = axes[1]
    for j, algo in enumerate(algos):
        n_val = avg_n[j]
        t_val = avg_t[j]
        ax2.scatter(t_val, n_val, s=90, color=colors[j], zorder=3,
                    edgecolors='black', linewidths=0.5)
        ax2.annotate(SHORT_NAMES.get(algo, algo).replace('\n', ' '),
                     (t_val, n_val),
                     textcoords='offset points', xytext=(6, 4), fontsize=7)
    ax2.set_xlabel('Avg. time (s)')
    ax2.set_ylabel('Avg. circle count')
    ax2.set_title('Tradeoff: Time vs Quality\n(bottom-left is ideal)')
    ax2.grid(True, alpha=0.3)

    plt.suptitle('Aggregate Benchmark Results (Filtered strictly to 100% Coverage algorithms)',
                 fontsize=13, y=1.01)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, 'full_cover_summary_bar.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()

def plot_per_shape(shapes, algos, mat_n, mat_t, shape_names):
    os.makedirs(PER_SHAPE, exist_ok=True)
    cmap = plt.cm.tab10
    colors = [cmap(i / len(algos)) for i in range(len(algos))]
    short = [SHORT_NAMES.get(a, a).replace('\n', ' ') for a in algos]

    for i, sid in enumerate(shapes):
        ns = mat_n[i]
        ts = mat_t[i]

        fig, ax = plt.subplots(figsize=(12, 5))
        x = np.arange(len(algos))

        for j in range(len(algos)):
            val = ns[j]
            height = float(val) if not np.isnan(val) else 0
            bar = ax.bar(x[j], height, color=colors[j], width=0.65,
                         edgecolor='white', linewidth=0.5)
            label = 'DNF' if np.isnan(val) else f"{int(val)}\n{ts[j]:.1f}s"
            ax.text(x[j], height + 0.2, label, ha='center', va='bottom',
                    fontsize=7.5, color='#333333')

        ax.set_xticks(x)
        ax.set_xticklabels(short, fontsize=9, rotation=20, ha='right')
        ax.set_ylabel('Circles count')
        ax.set_title(f'{sid}: {shape_names.get(sid, "")} - [Tylko 100%]',
                     fontsize=11)
        ax.grid(True, axis='y', alpha=0.3)
        ax.set_ylim(bottom=0)

        plt.tight_layout()
        out = os.path.join(PER_SHAPE, f'full_cover_{sid}.png')
        plt.savefig(out, dpi=150)
        plt.close()

def plot_time_comparison(algos, mat_t, mat_n):
    avg_t = [np.nanmean(mat_t[:, j]) for j in range(len(algos))]
    avg_n = [np.nanmean(mat_n[:, j]) for j in range(len(algos))]
    
    order = np.argsort(avg_t)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    y_pos = np.arange(len(algos))
    sorted_avg_t = np.array([avg_t[i] for i in order])
    sorted_avg_n = np.array([avg_n[i] for i in order])
    sorted_labels = [SHORT_NAMES.get(algos[i], algos[i]).replace('\n', ' ') for i in order]
    
    valid_t = sorted_avg_t[sorted_avg_t > 0]
    if len(valid_t) > 0:
        use_log = max(valid_t) / min(valid_t) > 50
    else:
        use_log = False
    
    cmap = plt.cm.RdYlGn_r
    norm = mcolors.Normalize(vmin=min(avg_n), vmax=max(avg_n))
    colors = [cmap(norm(val)) for val in sorted_avg_n]
    
    bars = ax.barh(y_pos, sorted_avg_t, align='center', color=colors, edgecolor='black', height=0.7)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('Average Execution Time (s)' + (' [Log Scale]' if use_log else ''), fontsize=11)
    ax.set_title('Time Comparison: 100% Coverage Algorithms\nColor = Quality (Green is fewer circles)', fontsize=13)
    
    if use_log:
        ax.set_xscale('log')
        
    for i, bar in enumerate(bars):
        t_val = sorted_avg_t[i]
        n_val = sorted_avg_n[i]
        label = f"{t_val:.3f} s (Circles: {n_val:.1f})"
        
        offset = t_val * 1.1 if use_log else t_val + (max(avg_t)*0.01)
        ax.text(max(offset, 1e-5), bar.get_y() + bar.get_height()/2, label, 
                va='center', fontsize=9, fontweight='bold')
            
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.7, pad=0.1)
    cbar.set_label('Average Circles Count')

    plt.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, 'full_cover_time_comparison.png')
    plt.savefig(out, dpi=150)
    plt.close()

def print_table(shapes, algos, mat_n):
    header = f"{'Shape':<8}" + "".join(f"{SHORT_NAMES.get(a, a).split(chr(10))[0]:>10}" for a in algos)
    print("\n" + "=" * len(header))
    print(header)
    print("-" * len(header))
    for i, sid in enumerate(shapes):
        row = f"{sid:<8}"
        for j in range(len(algos)):
            val = mat_n[i, j]
            row += f"{'DNF':>10}" if np.isnan(val) else f"{int(val):>10}"
        print(row)
    print("=" * len(header))

def main():
    if not os.path.exists(RESULTS_CSV):
        print(f"Results file not found: {RESULTS_CSV}")
        print("Run benchmark first: python benchmark.py")
        return

    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(PER_SHAPE, exist_ok=True)

    rows = load()
    if not rows:
        print("Brak algorytmów z wynikiem 100% pokrycia we wszystkich testach!")
        return

    shapes, algos, mat_n, mat_t, shape_names = build_matrices(rows)

    print_table(shapes, algos, mat_n)
    plot_heatmap(shapes, algos, mat_n, shape_names)
    plot_summary(algos, mat_n, mat_t)
    plot_per_shape(shapes, algos, mat_n, mat_t, shape_names)
    plot_time_comparison(algos, mat_t, mat_n)

    print(f"\nDone! Zapisano wyfiltrowane wykresy pełnego pokrycia (tylko 100%) w katalogu: {PLOTS_DIR}")

if __name__ == '__main__':
    main()
