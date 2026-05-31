"""
refined_algorithms.py - Ulepszone wersje A4, A11, A12.
Wprowadza: 
- Multi-component optimization (osobne gridy dla osobnych wysp).
- Higher precision search.
- Local search refinement.
"""
import math
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.affinity import rotate as shapely_rotate
from scipy.spatial import cKDTree

# Importujemy bazowe funkcje z poprzedniego folderu, aby nie dublować kodu
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'initial_test'))
from coverage import sample_interior, is_covered, coverage_pct
from algorithms import _hex_grid, _rotate_centers, a4_hex_shift as a4_standard

# ═══════════════════════════════════════════════════════════════════════════════
# REFINED ENGINE: Multi-component wrapper
# ═══════════════════════════════════════════════════════════════════════════════

def multi_component_optimize(polygon, radius, optimizer_func):
    """
    Rozbija MultiPolygon na osobne części i optymalizuje każdą z nich niezależnie.
    """
    if polygon.is_empty:
        return []
        
    if isinstance(polygon, MultiPolygon):
        parts = list(polygon.geoms)
    else:
        parts = [polygon]
        
    all_centers = []
    for part in parts:
        centers = optimizer_func(part, radius)
        all_centers.extend(centers)
    return all_centers

# ═══════════════════════════════════════════════════════════════════════════════
# A4_Refined - Bruteforce z wyższą rozdzielczością
# ═══════════════════════════════════════════════════════════════════════════════

def _a4_refined_logic(polygon, radius):
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y

    best = _hex_grid(polygon, radius)
    best_n = len(best)

    # 15 kątów (co 4 stopnie) i gęstsze przesunięcia (siatka 6x6)
    for angle in np.linspace(0, 59, 15):
        rot_poly = shapely_rotate(polygon, angle, origin='centroid')
        for fx in np.linspace(0, 1, 6, endpoint=False):
            for fy in np.linspace(0, 1, 6, endpoint=False):
                centers = _hex_grid(rot_poly, radius, fx * d, fy * row_h)
                if len(centers) < best_n:
                    best_n = len(centers)
                    best = _rotate_centers(centers, cx, cy, angle)
    return best

def a4_refined(polygon, radius, seed=42):
    return multi_component_optimize(polygon, radius, _a4_refined_logic)

# ═══════════════════════════════════════════════════════════════════════════════
# A11_Refined - Successive Zoom Search (4-etapowe przybliżanie)
# ═══════════════════════════════════════════════════════════════════════════════

def _a11_refined_logic(polygon, radius):
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y

    best_n = 10**9
    best_params = (0, 0, 0)
    
    # KROK 1: Bardzo zgrubny skan (globalny)
    for ang in np.linspace(0, 56, 8):
        rot_poly = shapely_rotate(polygon, ang, origin='centroid')
        for fx in [0.0, 0.33, 0.66]:
            for fy in [0.0, 0.33, 0.66]:
                n = len(_hex_grid(rot_poly, radius, fx*d, fy*row_h))
                if n < best_n:
                    best_n, best_params = n, (ang, fx, fy)

    # KROK 2-4: Zooming (zawężanie zakresu o połowę w każdej turze)
    ang_range, f_range = 10.0, 0.2
    for _ in range(3):
        curr_ang, curr_fx, curr_fy = best_params
        for a in np.linspace(curr_ang - ang_range, curr_ang + ang_range, 5):
            rot_poly = shapely_rotate(polygon, a % 60, origin='centroid')
            for x in np.linspace(curr_fx - f_range, curr_fx + f_range, 4):
                for y in np.linspace(curr_fy - f_range, curr_fy + f_range, 4):
                    nx, ny = x % 1.0, y % 1.0
                    n = len(_hex_grid(rot_poly, radius, nx*d, ny*row_h))
                    if n < best_n:
                        best_n, best_params = n, (a % 60, nx, ny)
        ang_range /= 2.5
        f_range /= 2.5

    ang, fx, fy = best_params
    centers = _hex_grid(shapely_rotate(polygon, ang, origin='centroid'), radius, fx*d, fy*row_h)
    return _rotate_centers(centers, cx, cy, ang)

def a11_refined(polygon, radius, seed=42):
    return multi_component_optimize(polygon, radius, _a11_refined_logic)

# ═══════════════════════════════════════════════════════════════════════════════
# A12_Refined - Turbo PSO + Local Hill Climb
# ═══════════════════════════════════════════════════════════════════════════════

def _a12_refined_logic(polygon, radius):
    rng = np.random.default_rng(42)
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y
    
    def eval_fn(state):
        a, x, y = state[0]%60, state[1]%1.0, state[2]%1.0
        rp = shapely_rotate(polygon, a, origin='centroid')
        return len(_hex_grid(rp, radius, x*d, y*row_h))
        
    pop, iters = 40, 30
    pos = rng.uniform(0, 1, (pop, 3))
    pos[:, 0] *= 60.0
    vel = np.zeros((pop, 3))
    pbest_pos = pos.copy()
    pbest_val = np.array([eval_fn(p) for p in pos])
    gbest_idx = np.argmin(pbest_val)
    gbest_pos, gbest_val = pbest_pos[gbest_idx].copy(), pbest_val[gbest_idx]
    
    # PSO Loop
    for _ in range(iters):
        r1, r2 = rng.random((pop, 3)), rng.random((pop, 3))
        vel = 0.5*vel + 1.5*r1*(pbest_pos-pos) + 1.5*r2*(gbest_pos-pos)
        pos += vel
        for i in range(pop):
            v = eval_fn(pos[i])
            if v < pbest_val[i]:
                pbest_val[i], pbest_pos[i] = v, pos[i].copy()
                if v < gbest_val:
                    gbest_val, gbest_pos = v, pos[i].copy()

    # Local Hill Climb - spróbuj małych przesunięć wokół gbest
    final_ang, final_fx, final_fy = gbest_pos[0]%60, gbest_pos[1]%1.0, gbest_pos[2]%1.0
    for _ in range(20):
        # Mała losowa perturbacja
        p_ang = (final_ang + rng.normal(0, 0.5)) % 60
        p_fx = (final_fx + rng.normal(0, 0.02)) % 1.0
        p_fy = (final_fy + rng.normal(0, 0.02)) % 1.0
        v = eval_fn([p_ang, p_fx, p_fy])
        if v <= gbest_val: # nawet jeśli równe, bierzemy nowe (może być stabilniejsze)
            gbest_val = v
            final_ang, final_fx, final_fy = p_ang, p_fx, p_fy

    rp = shapely_rotate(polygon, final_ang, origin='centroid')
    centers = _hex_grid(rp, radius, final_fx*d, final_fy*row_h)
    return _rotate_centers(centers, cx, cy, final_ang)

def a12_refined(polygon, radius, seed=42):
    return multi_component_optimize(polygon, radius, _a12_refined_logic)

# ═══════════════════════════════════════════════════════════════════════════════
# REJESTR REFINED
# ═══════════════════════════════════════════════════════════════════════════════

ALGORITHMS_REFINED = {
    'A4_Standard': a4_standard,
    'A4_Refined':  a4_refined,
    'A11_Refined': a11_refined,
    'A12_Refined': a12_refined,
}
