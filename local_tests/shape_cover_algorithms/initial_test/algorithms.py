"""
algorithms.py – 10 algorytmów pokrycia kształtu kołami.

Każda funkcja: (polygon: Shapely.Polygon, radius: float, seed: int) → list[[x, y]]
Funkcje muszą być importowalne z procesu potomnego (brak efektów ubocznych na poziomie modułu).
"""
import math
import numpy as np
from shapely.geometry import Point
from shapely.affinity import rotate as shapely_rotate
from scipy.spatial import cKDTree
from scipy.optimize import minimize

from coverage import sample_interior, is_covered, coverage_pct


# ═══════════════════════════════════════════════════════════════════════════════
# POMOCNIKI GENEROWANIA SIATEK
# ═══════════════════════════════════════════════════════════════════════════════

def _square_grid(polygon, radius: float, ox: float = 0.0, oy: float = 0.0):
    spacing = radius * math.sqrt(2)
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds
    centers = []
    y = miny + (oy % spacing) - spacing
    while y <= maxy + spacing:
        x = minx + (ox % spacing) - spacing
        while x <= maxx + spacing:
            if region.contains(Point(x, y)):
                centers.append([x, y])
            x += spacing
        y += spacing
    return centers


def _hex_grid(polygon, radius: float, ox: float = 0.0, oy: float = 0.0):
    d = radius * math.sqrt(3)          # odstęp między środkami
    row_h = d * math.sin(math.pi / 3)  # = d*√3/2 = 3r/2
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds
    centers = []
    row = 0
    y = miny + (oy % row_h) - row_h
    while y <= maxy + row_h:
        col_off = (d / 2) if (row % 2) else 0.0
        x = minx + (ox % d) - d + col_off
        while x <= maxx + d:
            if region.contains(Point(x, y)):
                centers.append([x, y])
            x += d
        y += row_h
        row += 1
    return centers


def _rotate_centers(centers, cx, cy, angle_deg: float):
    """Obraca listę środków o kąt (stopnie) relative do punktu (cx, cy)."""
    if not centers:
        return centers
    theta = math.radians(-angle_deg)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    arr = np.array(centers, dtype=float)
    arr -= [cx, cy]
    rotated = arr @ np.array([[cos_t, sin_t], [-sin_t, cos_t]])
    rotated += [cx, cy]
    return rotated.tolist()


# ═══════════════════════════════════════════════════════════════════════════════
# A1 – Naiwna Siatka Kwadratowa
# ═══════════════════════════════════════════════════════════════════════════════

def a1_square_grid(polygon, radius: float, seed: int = 42):
    return _square_grid(polygon, radius)


# ═══════════════════════════════════════════════════════════════════════════════
# A2 – Naiwna Siatka Heksagonalna
# ═══════════════════════════════════════════════════════════════════════════════

def a2_hex_grid(polygon, radius: float, seed: int = 42):
    return _hex_grid(polygon, radius)


# ═══════════════════════════════════════════════════════════════════════════════
# A3 – Kwadratowa + Przesunięcie / Rotacja
# ═══════════════════════════════════════════════════════════════════════════════

def a3_square_shift(polygon, radius: float, seed: int = 42):
    spacing = radius * math.sqrt(2)
    cx, cy = polygon.centroid.x, polygon.centroid.y

    best = _square_grid(polygon, radius)
    best_n = len(best)

    for angle in np.linspace(0, 44, 6):            # 6 kątów (symetria = 90°)
        rot_poly = shapely_rotate(polygon, angle, origin='centroid')
        for fx in np.linspace(0, 1, 5, endpoint=False):
            for fy in np.linspace(0, 1, 5, endpoint=False):
                centers = _square_grid(rot_poly, radius, fx * spacing, fy * spacing)
                if len(centers) < best_n:
                    best_n = len(centers)
                    best = _rotate_centers(centers, cx, cy, angle)

    return best


# ═══════════════════════════════════════════════════════════════════════════════
# A4 – Heksagonalna + Przesunięcie / Rotacja
# ═══════════════════════════════════════════════════════════════════════════════

def a4_hex_shift(polygon, radius: float, seed: int = 42):
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y

    best = _hex_grid(polygon, radius)
    best_n = len(best)

    for angle in np.linspace(0, 59, 7):            # symetria hex = 60°
        rot_poly = shapely_rotate(polygon, angle, origin='centroid')
        for fx in np.linspace(0, 1, 4, endpoint=False):
            for fy in np.linspace(0, 1, 4, endpoint=False):
                centers = _hex_grid(rot_poly, radius, fx * d, fy * row_h)
                if len(centers) < best_n:
                    best_n = len(centers)
                    best = _rotate_centers(centers, cx, cy, angle)

    return best


# ═══════════════════════════════════════════════════════════════════════════════
# A5 – Zachłanny Dyskretny (Greedy Set Cover)
# ═══════════════════════════════════════════════════════════════════════════════

def a5_greedy_discrete(polygon, radius: float, seed: int = 42):
    test_pts = sample_interior(polygon, n=2000, seed=seed)

    # Kandydaci = gęsta siatka w obrębie polygon.buffer(radius)
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds
    step = radius / 2.0
    cands = []
    y = miny
    while y <= maxy:
        x = minx
        while x <= maxx:
            if region.contains(Point(x, y)):
                cands.append([x, y])
            x += step
        y += step

    if not cands:
        return []

    cands = np.array(cands, dtype=float)

    # Precompute: które kandydaci pokrywają który punkt testowy
    cand_tree = cKDTree(cands)
    assignments = cand_tree.query_ball_point(test_pts, radius)

    cand_covers = [[] for _ in range(len(cands))]
    for pt_i, cand_idxs in enumerate(assignments):
        for c_i in cand_idxs:
            cand_covers[c_i].append(pt_i)

    covered = np.zeros(len(test_pts), dtype=bool)
    selected = []

    while not np.all(covered):
        counts = np.array([sum(1 for i in cs if not covered[i]) for cs in cand_covers])
        best_i = int(np.argmax(counts))
        if counts[best_i] == 0:
            break
        selected.append(cands[best_i].tolist())
        for pt_i in cand_covers[best_i]:
            covered[pt_i] = True

    return selected


# ═══════════════════════════════════════════════════════════════════════════════
# A6 – Zachłanny Ciągły (Greedy + Nelder-Mead refinement)
# ═══════════════════════════════════════════════════════════════════════════════

def a6_greedy_continuous(polygon, radius: float, seed: int = 42):
    test_pts = sample_interior(polygon, n=1000, seed=seed)
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds

    # Coarse candidate grid
    step = radius * 0.8
    cands = []
    y = miny
    while y <= maxy:
        x = minx
        while x <= maxx:
            if region.contains(Point(x, y)):
                cands.append([x, y])
            x += step
        y += step

    if not cands:
        return []

    cands = np.array(cands, dtype=float)
    covered = np.zeros(len(test_pts), dtype=bool)
    selected = []

    def neg_cover_count(center, uncov):
        d = np.linalg.norm(uncov - center, axis=1)
        return -float(np.sum(d <= radius))

    while not np.all(covered):
        uncov_pts = test_pts[~covered]

        # Najlepszy kandydat dyskretny
        counts = np.array([
            np.sum(np.linalg.norm(uncov_pts - c, axis=1) <= radius) for c in cands
        ])
        best_i = int(np.argmax(counts))
        if counts[best_i] == 0:
            break

        x0 = cands[best_i]
        res = minimize(neg_cover_count, x0, args=(uncov_pts,),
                       method='Nelder-Mead',
                       options={'maxiter': 300, 'xatol': radius * 0.01, 'fatol': 0.5})
        best_center = res.x if (res.success or -res.fun > counts[best_i]) else x0

        selected.append(best_center.tolist())
        d = np.linalg.norm(test_pts - best_center, axis=1)
        covered |= (d <= radius)

    return selected


# ═══════════════════════════════════════════════════════════════════════════════
# A7 – Relaksacja Voronoia (Lloyd's Algorithm)
# ═══════════════════════════════════════════════════════════════════════════════

def a7_voronoi_relax(polygon, radius: float, seed: int = 42):
    test_pts = sample_interior(polygon, n=2000, seed=seed)

    # Start: siatka heksagonalna
    centers = np.array(_hex_grid(polygon, radius), dtype=float)
    if len(centers) == 0:
        return []

    # Lloyd's: iteracyjne przesuwanie środków do centroidu ich klastra
    for _ in range(40):
        tree = cKDTree(centers)
        _, labels = tree.query(test_pts)

        new_centers = np.empty_like(centers)
        for i in range(len(centers)):
            cluster = test_pts[labels == i]
            new_centers[i] = cluster.mean(axis=0) if len(cluster) > 0 else centers[i]

        movement = np.max(np.linalg.norm(new_centers - centers, axis=1))
        centers = new_centers
        if movement < radius * 0.001:
            break

    # Usuń redundantne koła
    centers_list = centers.tolist()
    improved = True
    while improved:
        improved = False
        for i in range(len(centers_list) - 1, -1, -1):
            without = centers_list[:i] + centers_list[i + 1:]
            if without and is_covered(test_pts, without, radius, threshold=100.0):
                centers_list = without
                improved = True
                break

    return centers_list


# ═══════════════════════════════════════════════════════════════════════════════
# A8 – Algorytm Genetyczny
# ═══════════════════════════════════════════════════════════════════════════════

def a8_genetic(polygon, radius: float, seed: int = 42):
    rng = np.random.default_rng(seed)
    test_pts = sample_interior(polygon, n=1000, seed=seed)
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds

    baseline_n = len(_hex_grid(polygon, radius))
    POP = 24
    GENS = 100
    MUTATION_SIGMA = radius * 0.5

    def fitness(ind):
        cov = coverage_pct(test_pts, ind, radius)
        return len(ind) + max(0.0, 100.0 - cov) * 200.0

    def rand_valid_centers(n):
        pts = []
        attempts = 0
        while len(pts) < n and attempts < n * 20:
            x = rng.uniform(minx, maxx)
            y = rng.uniform(miny, maxy)
            if region.contains(Point(x, y)):
                pts.append([x, y])
            attempts += 1
        return pts

    def clip_to_region(centers):
        return [c for c in centers if region.contains(Point(c[0], c[1]))]

    # Inicjalizacja populacji
    pop = [_hex_grid(polygon, radius), _square_grid(polygon, radius)]
    for _ in range(POP - 2):
        n = rng.integers(max(2, baseline_n // 2), baseline_n + 4)
        pop.append(rand_valid_centers(int(n)))

    for _gen in range(GENS):
        scores = [fitness(ind) for ind in pop]
        sorted_pop = [x for _, x in sorted(zip(scores, pop), key=lambda t: t[0])]
        survivors = sorted_pop[: POP // 2]
        new_pop = survivors.copy()

        while len(new_pop) < POP:
            i1, i2 = rng.integers(0, len(survivors), 2)
            p1 = np.array(survivors[i1], dtype=float)
            p2 = np.array(survivors[i2], dtype=float)

            # Krzyżowanie: weź losowy podzbiór z każdego rodzica
            n1 = max(1, rng.integers(1, len(p1) + 1))
            n2 = max(1, rng.integers(1, len(p2) + 1))
            idx1 = rng.choice(len(p1), min(n1, len(p1)), replace=False)
            idx2 = rng.choice(len(p2), min(n2, len(p2)), replace=False)
            child = np.vstack([p1[idx1], p2[idx2]])

            # Mutacja
            if rng.random() < 0.2:
                m_idx = rng.integers(0, len(child))
                child[m_idx] += rng.normal(0, MUTATION_SIGMA, 2)

            # Usunięcie losowego koła (eksploracja mniejszych zbiorów)
            if rng.random() < 0.15 and len(child) > 1:
                child = np.delete(child, rng.integers(0, len(child)), axis=0)

            child_list = clip_to_region(child.tolist())
            if child_list:
                new_pop.append(child_list)

        pop = new_pop

    scores = [fitness(ind) for ind in pop]
    return pop[int(np.argmin(scores))]


# ═══════════════════════════════════════════════════════════════════════════════
# A9 – Symulowane Wyżarzanie (SA)
# ═══════════════════════════════════════════════════════════════════════════════

def a9_sa(polygon, radius: float, seed: int = 42):
    rng = np.random.default_rng(seed)
    test_pts = sample_interior(polygon, n=1500, seed=seed)
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds

    def energy(centers):
        cov = coverage_pct(test_pts, centers, radius)
        # Mnożnik *10000.0 (zamiast 100.0) karze odrzucenie kola, gubiąc ułamek pokrycia.
        return float(len(centers)) + max(0.0, 100.0 - cov) * 10000.0

    def rand_pt():
        for _ in range(200):
            x = rng.uniform(minx, maxx)
            y = rng.uniform(miny, maxy)
            if region.contains(Point(x, y)):
                return [x, y]
        return None

    current = [list(c) for c in _hex_grid(polygon, radius)]
    cur_e = energy(current)
    best, best_e = current.copy(), cur_e

    T = 2.0
    alpha = 0.9975
    T_min = 0.005
    max_iter = 12000
    MOVES = ['remove', 'move', 'add']
    WEIGHTS = [0.45, 0.45, 0.10]

    for _ in range(max_iter):
        T = max(T * alpha, T_min)
        move = rng.choice(MOVES, p=WEIGHTS)
        cand = [list(c) for c in current]

        if move == 'remove' and len(cand) > 1:
            cand.pop(int(rng.integers(0, len(cand))))
        elif move == 'move' and cand:
            idx = int(rng.integers(0, len(cand)))
            sigma = radius * (0.5 + T)
            new_pt = [cand[idx][0] + rng.normal(0, sigma),
                      cand[idx][1] + rng.normal(0, sigma)]
            if region.contains(Point(*new_pt)):
                cand[idx] = new_pt
        elif move == 'add':
            pt = rand_pt()
            if pt:
                cand.append(pt)

        new_e = energy(cand)
        delta = new_e - cur_e
        if delta < 0 or rng.random() < math.exp(-delta / T):
            current, cur_e = cand, new_e
            if cur_e < best_e:
                best, best_e = current.copy(), cur_e

    return best


# ═══════════════════════════════════════════════════════════════════════════════
# A10 – Hybryda: Hex Shift → SA
# ═══════════════════════════════════════════════════════════════════════════════

def a10_hybrid(polygon, radius: float, seed: int = 42):
    rng = np.random.default_rng(seed)
    test_pts = sample_interior(polygon, n=1500, seed=seed)
    region = polygon.buffer(radius)
    minx, miny, maxx, maxy = region.bounds

    # Dobry punkt startowy z A4
    current = [list(c) for c in a4_hex_shift(polygon, radius, seed)]

    def energy(centers):
        cov = coverage_pct(test_pts, centers, radius)
        # Mnożnik *10000.0 (zamiast 100.0) wymusza 100% pokrycia.
        return float(len(centers)) + max(0.0, 100.0 - cov) * 10000.0

    def rand_pt():
        for _ in range(200):
            x = rng.uniform(minx, maxx)
            y = rng.uniform(miny, maxy)
            if region.contains(Point(x, y)):
                return [x, y]
        return None

    cur_e = energy(current)
    best, best_e = current.copy(), cur_e

    # SA z mniejszymi parametrami (startujemy z dobrego miejsca, chcemy drobne korekty)
    T = 1.0
    alpha = 0.9980
    T_min = 0.003
    max_iter = 10000
    MOVES = ['remove', 'move']
    WEIGHTS = [0.5, 0.5]

    for _ in range(max_iter):
        T = max(T * alpha, T_min)
        move = rng.choice(MOVES, p=WEIGHTS)
        cand = [list(c) for c in current]

        if move == 'remove' and len(cand) > 1:
            cand.pop(int(rng.integers(0, len(cand))))
        elif move == 'move' and cand:
            idx = int(rng.integers(0, len(cand)))
            sigma = radius * (0.3 + T * 0.5)
            new_pt = [cand[idx][0] + rng.normal(0, sigma),
                      cand[idx][1] + rng.normal(0, sigma)]
            if region.contains(Point(*new_pt)):
                cand[idx] = new_pt

        new_e = energy(cand)
        delta = new_e - cur_e
        if delta < 0 or rng.random() < math.exp(-delta / T):
            current, cur_e = cand, new_e
            if cur_e < best_e:
                best, best_e = current.copy(), cur_e

    return best


# ═══════════════════════════════════════════════════════════════════════════════
# A11 – Adaptive Hex Shift (Zgrubne + Dokładne)
# ═══════════════════════════════════════════════════════════════════════════════

def a11_adaptive_hex(polygon, radius: float, seed: int = 42):
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y

    best = _hex_grid(polygon, radius)
    best_n = len(best)
    best_params = [(0, 0, 0)]
    
    coarse_angles = np.linspace(0, 59, 5) 
    for angle in coarse_angles:
        rot_poly = shapely_rotate(polygon, angle, origin='centroid')
        for fx in np.linspace(0, 1, 3, endpoint=False):
            for fy in np.linspace(0, 1, 3, endpoint=False):
                centers = _hex_grid(rot_poly, radius, fx * d, fy * row_h)
                n_c = len(centers)
                if n_c < best_n:
                    best_n = n_c
                    best = _rotate_centers(centers, cx, cy, angle)
                    best_params = [(angle, fx, fy)]
                elif n_c == best_n:
                    best_params.append((angle, fx, fy))

    fine_best = best
    fine_best_n = best_n
    
    for (ang, fx, fy) in best_params[:3]:
        for d_ang in [-3.0, -1.0, 1.0, 3.0]:
            fin_a = (ang + d_ang) % 60
            rot_poly = shapely_rotate(polygon, fin_a, origin='centroid')
            for dfx in [-0.15, 0.15]:
                for dfy in [-0.15, 0.15]:
                    nx = (fx + dfx) % 1.0
                    ny = (fy + dfy) % 1.0
                    centers = _hex_grid(rot_poly, radius, nx * d, ny * row_h)
                    n_c = len(centers)
                    if n_c < fine_best_n:
                        fine_best_n = n_c
                        fine_best = _rotate_centers(centers, cx, cy, fin_a)
    return fine_best

# ═══════════════════════════════════════════════════════════════════════════════
# A12 – PSO Hex (Particle Swarm Optimization)
# ═══════════════════════════════════════════════════════════════════════════════

def a12_pso_hex(polygon, radius: float, seed: int = 42):
    rng = np.random.default_rng(seed)
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y
    
    def evaluate(state):
        ang, fx, fy = state
        rot_poly = shapely_rotate(polygon, ang, origin='centroid')
        centers = _hex_grid(rot_poly, radius, fx * d, fy * row_h)
        return len(centers)
        
    pop_size = 15
    iters = 12
    
    pos = np.zeros((pop_size, 3))
    pos[:, 0] = rng.uniform(0, 60, pop_size)
    pos[:, 1] = rng.uniform(0, 1, pop_size)
    pos[:, 2] = rng.uniform(0, 1, pop_size)
    vel = np.zeros((pop_size, 3))
    
    pbest_pos = pos.copy()
    pbest_val = np.array([evaluate(p) for p in pos])
    
    gbest_idx = int(np.argmin(pbest_val))
    gbest_pos = pbest_pos[gbest_idx].copy()
    gbest_val = pbest_val[gbest_idx]
    
    w, c1, c2 = 0.5, 1.5, 1.5
    
    for _ in range(iters):
        r1 = rng.random((pop_size, 3))
        r2 = rng.random((pop_size, 3))
        vel = w * vel + c1 * r1 * (pbest_pos - pos) + c2 * r2 * (gbest_pos - pos)
        pos = pos + vel

        pos[:, 0] %= 60.0
        pos[:, 1] %= 1.0
        pos[:, 2] %= 1.0
        
        for i in range(pop_size):
            val = evaluate(pos[i])
            if val < pbest_val[i]:
                pbest_val[i] = val
                pbest_pos[i] = pos[i].copy()
                if val < gbest_val:
                    gbest_val = val
                    gbest_pos = pos[i].copy()
                    
    ang, fx, fy = gbest_pos
    rot_poly = shapely_rotate(polygon, ang, origin='centroid')
    centers = _hex_grid(rot_poly, radius, fx * d, fy * row_h)
    return _rotate_centers(centers, cx, cy, ang)

# ═══════════════════════════════════════════════════════════════════════════════
# REJESTR
# ═══════════════════════════════════════════════════════════════════════════════

ALGORITHMS = {
    'A1_Square_Grid':       a1_square_grid,
    'A2_Hex_Grid':          a2_hex_grid,
    'A3_Square_Shift':      a3_square_shift,
    'A4_Hex_Shift':         a4_hex_shift,
    'A5_Greedy_Discrete':   a5_greedy_discrete,
    'A6_Greedy_Continuous': a6_greedy_continuous,
    'A7_Voronoi_Relax':     a7_voronoi_relax,
    'A8_Genetic':           a8_genetic,
    'A9_SA':                a9_sa,
    'A10_Hybrid':           a10_hybrid,
    'A11_Adaptive_Hex':     a11_adaptive_hex,
    'A12_PSO_Hex':          a12_pso_hex,
}
