"""
visualize_maps.py - Wyciąga docelowe kształty (w tym z bazy, S11, S12) i nanosi koła algorytmów 100%.
"""
import os
import sys
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from shapes import get_all_shapes, get_radius
from algorithms import ALGORITHMS

out_dir = os.path.join(HERE, 'plots', 'maps')
os.makedirs(out_dir, exist_ok=True)

# S11, S12 to Twoje wyspy DB. Dodaję najciekawsze kształty ze zwykłych: S06 (Gwiazda) i S10 (Donut)
TARGET_SHAPES = ['S06', 'S10', 'S11', 'S12']

ALGOS_TO_PLOT = list(ALGORITHMS.keys())

SHORT_NAMES = {
    'A1_Square_Grid':       'A1 Sq.Grid',
    'A2_Hex_Grid':          'A2 Hex',
    'A3_Square_Shift':      'A3 Sq.Shift',
    'A4_Hex_Shift':         'A4 Hex+Shift',
    'A5_Greedy_Discrete':   'A5 Greedy-D',
    'A6_Greedy_Continuous': 'A6 Greedy-C',
    'A7_Voronoi_Relax':     'A7 Voronoi',
    'A8_Genetic':           'A8 Genetic',
    'A9_SA':                'A9 SA',
    'A10_Hybrid':           'A10 Hybrid',
    'A11_Adaptive_Hex':     'A11 Adapt Hex',
    'A12_PSO_Hex':          'A12 PSO Hex',
}

def plot_shape_maps():
    all_shapes = get_all_shapes()
    
    for shape_id, shape_name, polygon in all_shapes:
        if shape_id not in TARGET_SHAPES:
            continue
            
        radius = get_radius(polygon)
        
        # Plansza 3x4 dla wszystkich 12 algorytmów
        fig, axes = plt.subplots(3, 4, figsize=(22, 16))
        fig.suptitle(f'All Algorithms Overlay Maps: {shape_id} ({shape_name})', fontsize=20, fontweight='bold', y=0.98)
        
        axes = axes.flatten()
        
        minx, miny, maxx, maxy = polygon.bounds
        for i, algo_name in enumerate(ALGOS_TO_PLOT):
            ax = axes[i]
            algo_func = ALGORITHMS[algo_name]
            
            # Rekonstruujemy generowanie punktów prosto z algorytmów! (One są super-szybkie)
            centers = algo_func(polygon, radius, seed=42)
            n_c = len(centers)
            
            # Wypełniamy bryłę główną (kształt)
            try:
                x, y = polygon.exterior.xy
                ax.plot(x, y, color='#1c1c1c', linewidth=2.5, zorder=5)
                ax.fill(x, y, color='#9db2bf', alpha=0.7, zorder=1)
            except Exception:
                pass # w razie rozbitego multipolygonu
                
            # Wypełniamy dziury na biało (np. w Donucie)
            if hasattr(polygon, 'interiors'):
                for interior in polygon.interiors:
                    ix, iy = interior.xy
                    ax.plot(ix, iy, color='#1c1c1c', linewidth=2.5, zorder=5)
                    ax.fill(ix, iy, color='white', alpha=1.0, zorder=4)
                
            # Rysowanie kół wokół znalezionych Centrów
            for cx, cy in centers:
                circle = Circle((cx, cy), radius, color='#ee6c4d', alpha=0.35, zorder=2)
                ax.add_patch(circle)
                # Środek koła
                ax.scatter([cx], [cy], color='#982b1c', s=12, zorder=3)
                
            ax.set_aspect('equal')
            ax.set_xlim(minx - radius*1.5, maxx + radius*1.5)
            ax.set_ylim(miny - radius*1.5, maxy + radius*1.5)
            ax.set_title(f"{SHORT_NAMES[algo_name]}\nZajęto: {n_c} Kół", fontsize=13, fontweight='bold')
            ax.axis('off')
            
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        out_path = os.path.join(out_dir, f'full_map_{shape_id}.png')
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Wygenerowano z rzutem kół -> {out_path}")

if __name__ == '__main__':
    plot_shape_maps()
