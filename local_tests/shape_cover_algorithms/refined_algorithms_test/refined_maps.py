"""
refined_maps.py - Mapy pokrycia dla algorytmów Refined (A4, A11, A12).
"""
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_DIR = os.path.join(BASE_DIR, '..', 'initial_test')
sys.path.append(ORIGINAL_DIR)

from shapes import get_all_shapes, get_radius
from refined_algorithms import ALGORITHMS_REFINED

MAPS_DIR = os.path.join(BASE_DIR, 'plots', 'maps')
os.makedirs(MAPS_DIR, exist_ok=True)

TARGET_SHAPES = ['S06', 'S10', 'S11', 'S12']
ALGOS = ['A4_Standard', 'A4_Refined', 'A11_Refined', 'A12_Refined']

def main():
    shapes = [s for s in get_all_shapes() if s[0] in TARGET_SHAPES]
    
    for sid, sname, poly in shapes:
        radius = get_radius(poly)
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'Refined Coverage Overlay: {sid} ({sname})', fontsize=18, fontweight='bold')
        
        axes = axes.flatten()
        minx, miny, maxx, maxy = poly.bounds
        for i, algo in enumerate(ALGOS):
            ax = axes[i]
            centers = ALGORITHMS_REFINED[algo](poly, radius)
            
            # Draw Shape
            def draw_poly(p, axis):
                axis.plot(*p.exterior.xy, color='black', lw=2, zorder=5)
                axis.fill(*p.exterior.xy, color='#9db2bf', alpha=0.5, zorder=1)
                for interior in p.interiors:
                    axis.plot(*interior.xy, color='black', lw=1.5, zorder=5)
                    axis.fill(*interior.xy, color='white', alpha=1.0, zorder=4)

            if hasattr(poly, 'geoms'): # MultiPolygon
                for part in poly.geoms:
                    draw_poly(part, ax)
            else:
                draw_poly(poly, ax)
                
            # Draw Circles
            for cx, cy in centers:
                c = Circle((cx, cy), radius, color='#ee6c4d', alpha=0.3)
                ax.add_patch(c)
                ax.scatter(cx, cy, s=10, color='red', alpha=0.5)
                
            ax.set_title(f"{algo}\nCircles: {len(centers)}")
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_xlim(minx - radius, maxx + radius)
            ax.set_ylim(miny - radius, maxy + radius)
            
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(os.path.join(MAPS_DIR, f'refined_map_{sid}.png'), dpi=150)
        plt.close()
        print(f"Zapisano mapę dla {sid}")

if __name__ == '__main__':
    main()
