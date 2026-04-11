"""
coverage.py – Narzędzia do sprawdzania pokrycia kształtu przez koła.
"""
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point


def sample_interior(polygon, n: int = 2000, seed: int = 42) -> np.ndarray:
    """Losuje n punktów równomiernie z wnętrza wielokąta (rejection sampling)."""
    rng = np.random.default_rng(seed)
    minx, miny, maxx, maxy = polygon.bounds
    result = []
    while len(result) < n:
        batch_n = max((n - len(result)) * 4, 500)
        xs = rng.uniform(minx, maxx, batch_n)
        ys = rng.uniform(miny, maxy, batch_n)
        for x, y in zip(xs, ys):
            if polygon.contains(Point(x, y)):
                result.append([x, y])
                if len(result) >= n:
                    break
    return np.array(result[:n], dtype=float)


def coverage_pct(test_pts: np.ndarray, centers, radius: float) -> float:
    """Procent punktów testowych pokrytych przez koła (center ± radius)."""
    if len(centers) == 0:
        return 0.0
    tree = cKDTree(np.array(centers, dtype=float))
    dists, _ = tree.query(test_pts)
    return float(np.mean(dists <= radius)) * 100.0


def is_covered(test_pts: np.ndarray, centers, radius: float,
               threshold: float = 99.95) -> bool:
    """Sprawdza czy pokrycie przekracza próg (domyślnie 99.95%)."""
    return coverage_pct(test_pts, centers, radius) >= threshold
