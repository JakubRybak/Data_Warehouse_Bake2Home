"""
algo_logic.py - Samowystarczalna implementacja algorytmu A4_Standard (Hex Shift).
Skopiowane do google_maps_test, aby uniknąć problemów z importami w IDE.
"""
import math
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.affinity import rotate as shapely_rotate

def _rotate_centers(centers, cx, cy, angle):
    """Obraca listę punktów wokół zadanego centrum o zadany kąt."""
    if not centers or angle == 0:
        return centers
    rad = math.radians(-angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    new_pts = []
    for x, y in centers:
        tx, ty = x - cx, y - cy
        nx = tx * cos_a - ty * sin_a + cx
        ny = tx * sin_a + ty * cos_a + cy
        new_pts.append((nx, ny))
    return new_pts

def _hex_grid(region, radius, offset_x=0, offset_y=0):
    """Generuje siatkę heksagonalną wewnątrz zadanego regionu."""
    minx, miny, maxx, maxy = region.bounds
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    
    # Dodajemy margines, aby pokryć brzegi
    x_range = np.arange(minx - d, maxx + d, d)
    y_range = np.arange(miny - d, maxy + d, row_h)
    
    centers = []
    for i, y in enumerate(y_range):
        shift = (d / 2.0) if (i % 2 == 1) else 0
        for x in x_range:
            p = Point(x + shift + offset_x, y + offset_y)
            if region.contains(p):
                centers.append((p.x, p.y))
    return centers

def a4_standard(polygon, radius, seed=42):
    """Algorytm A4 - Przeszukiwanie siatki heksagonalnej (7 kątów x 16 przesunięć)."""
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y

    best_centers = []
    best_n = float('inf')

    # Sprawdzenie 7 kątów (0-60 stopni) i siatki przesunięć 4x4
    angles = np.linspace(0, 59, 7)
    shifts = np.linspace(0, 1, 4, endpoint=False)

    for angle in angles:
        rot_poly = shapely_rotate(polygon, angle, origin='centroid')
        # Buforujemy poligon promieniem, aby zapewnić 100% pokrycia krawędzi
        search_region = rot_poly.buffer(radius)
        
        for fx in shifts:
            for fy in shifts:
                centers = _hex_grid(search_region, radius, fx * d, fy * row_h)
                if len(centers) < best_n:
                    best_n = len(centers)
                    best_centers = _rotate_centers(centers, cx, cy, angle)
                    
    return best_centers
