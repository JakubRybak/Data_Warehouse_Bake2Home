"""
shapes.py – Generowanie i ładowanie kształtów testowych.

S01–S05: Losowe wielokąty wypukłe (convex)
S06–S08: Losowe wielokąty wklęsłe (gwiazdy)
S09:     Kształt L (union dwóch prostokątów)
S10:     Pierścień / donut (wielokąt z dziurą)
S11–S12: Wyspy z bazy danych (google_maps_test/data/merged_islands.csv)
"""
import os
import csv
import math
import numpy as np
from shapely.geometry import Polygon, MultiPoint
from shapely.affinity import translate, scale as affine_scale
from shapely.ops import transform, unary_union
import pyproj


# ── Kształty losowe ──────────────────────────────────────────────────────────

def _scale_to(poly, target: float = 4000.0):
    """Skaluje wielokąt tak, by jego największy wymiar = target."""
    minx, miny, maxx, maxy = poly.bounds
    w, h = maxx - minx, maxy - miny
    s = target / max(w, h, 1e-9)
    centered = translate(poly, -minx - w / 2, -miny - h / 2)
    return affine_scale(centered, xfact=s, yfact=s, origin=(0, 0))


def gen_convex(seed: int, n_pts: int = 12, scale: float = 4000.0) -> Polygon:
    rng = np.random.default_rng(seed)
    angles = np.sort(rng.uniform(0, 2 * math.pi, n_pts))
    rs = rng.uniform(0.55, 1.0, n_pts)
    pts = np.column_stack([rs * np.cos(angles), rs * np.sin(angles)])
    poly = MultiPoint(pts).convex_hull
    return _scale_to(poly, scale)


def gen_star(seed: int, n_points: int = 5, scale: float = 4000.0) -> Polygon:
    rng = np.random.default_rng(seed)
    inner_r = rng.uniform(0.30, 0.50)
    n = n_points * 2
    angles = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rs = np.array([1.0 if i % 2 == 0 else inner_r for i in range(n)])
    pts = list(zip(rs * np.cos(angles), rs * np.sin(angles)))
    return _scale_to(Polygon(pts), scale)


def gen_l_shape(seed: int, scale: float = 4000.0) -> Polygon:
    rng = np.random.default_rng(seed)
    w = rng.uniform(0.25, 0.55)
    h = rng.uniform(0.25, 0.55)
    rect1 = Polygon([(0, 0), (1, 0), (1, 1 + h), (w, 1 + h), (w, 1), (0, 1)])
    rect2 = Polygon([(0, 0), (1 + w, 0), (1 + w, h), (0, h)])
    return _scale_to(unary_union([rect1, rect2]), scale)


def gen_ring(seed: int, scale: float = 4000.0) -> Polygon:
    rng = np.random.default_rng(seed)
    n = 48
    angles = np.linspace(0, 2 * math.pi, n, endpoint=False)
    outer = list(zip(np.cos(angles), np.sin(angles)))
    inner_r = rng.uniform(0.35, 0.55)
    inner = list(zip(inner_r * np.cos(angles[::-1]), inner_r * np.sin(angles[::-1])))
    return _scale_to(Polygon(outer, [inner]), scale)


# ── Kształty z bazy ──────────────────────────────────────────────────────────

def load_db_shapes():
    """Ładuje merged_islands.csv i projektuje do EPSG:3857 (metry)."""
    proj = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)

    # Szukamy pliku względem lokalizacji tego skryptu
    base = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base, '..', 'google_maps_test', 'data', 'buffered_islands.csv')

    if not os.path.exists(csv_path):
        print(f"[shapes.py] UWAGA: Nie znaleziono {csv_path} – pomijam S11/S12")
        return []

    islands: dict = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sid = int(row['IslandId'])
            x, y = proj.transform(float(row['Longitude']), float(row['Latitude']))
            islands.setdefault(sid, []).append((x, y))

    polys = []
    for sid in sorted(islands):
        coords = islands[sid]
        if len(coords) >= 3:
            polys.append(Polygon(coords))
    return polys


# ── Zbiorczy rejestr ─────────────────────────────────────────────────────────

def get_all_shapes():
    """Zwraca listę (shape_id, shape_name, polygon)."""
    shapes = []

    # Convex (S01–S05)
    for i, seed in enumerate([10, 20, 30, 40, 50], start=1):
        shapes.append((f'S{i:02d}', f'Convex_{i}', gen_convex(seed)))

    # Concave stars (S06–S08)
    for i, (seed, npts) in enumerate([(60, 5), (70, 6), (80, 7)], start=6):
        shapes.append((f'S{i:02d}', f'Star_{i-5}', gen_star(seed, npts)))

    # L-shape (S09)
    shapes.append(('S09', 'L_Shape', gen_l_shape(90)))

    # Ring/Donut (S10)
    shapes.append(('S10', 'Ring_Donut', gen_ring(100)))

    # DB shapes (S11, S12)
    for i, poly in enumerate(load_db_shapes()[:2], start=11):
        shapes.append((f'S{i:02d}', f'DB_Island_{i - 10}', poly))

    return shapes


def get_radius(polygon) -> float:
    """Zmienione na sztywne 250m dla bezpieczeństwa danych w Google Maps API (limit 20 wyników)."""
    return 250.0
