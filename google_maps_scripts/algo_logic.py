"""
algo_logic.py - Optimized hex-grid coverage algorithm implementation (A4_Standard).
Responsible for dividing irregular delivery zone polygons into a minimal set
of search circles for the Google Places API to minimize cloud query costs.
"""
import math
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.affinity import rotate as shapely_rotate

def _rotate_centers(centers: list, cx: float, cy: float, angle: float) -> list:
    """Rotates the list of generated circle centers back by the given angle around the polygon centroid."""
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

def _hex_grid(region: Polygon, radius: float, offset_x: float = 0.0, offset_y: float = 0.0) -> list:
    """Generates a regular hexagonal grid (honeycomb pattern) inside and on the boundaries of the search region."""
    minx, miny, maxx, maxy = region.bounds
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    
    # Add a safety margin (buffer) to ensure full coverage of the polygon boundaries
    x_range = np.arange(minx - d, maxx + d, d)
    y_range = np.arange(miny - d, maxy + d, row_h)
    
    centers = []
    for i, y in enumerate(y_range):
        # Shift every second row to create the honeycomb grid layout
        shift = (d / 2.0) if (i % 2 == 1) else 0.0
        for x in x_range:
            p = Point(x + shift + offset_x, y + offset_y)
            if region.contains(p):
                centers.append((p.x, p.y))
    return centers

def a4_standard(polygon: Polygon, radius: float, buffer_distance: float = None) -> list:
    """
    A4_Standard Algorithm - Calculates the optimal hexagonal coverage of a polygon with circles.
    Scans 7 rotation angles and 16 translation shifts (4x4 offset grid), selecting the configuration
    that yields the absolute minimum number of search circles while guaranteeing 100% spatial coverage.
    """
    d = radius * math.sqrt(3)
    row_h = d * math.sin(math.pi / 3)
    cx, cy = polygon.centroid.x, polygon.centroid.y
    actual_buffer = buffer_distance if buffer_distance is not None else radius

    best_centers = []
    best_n = float('inf')

    # Optimization grid: 7 rotation angles (0 to 60 degrees) and 4x4 translation shifts
    angles = np.linspace(0, 59, 7)
    shifts = np.linspace(0, 1, 4, endpoint=False)

    for angle in angles:
        # Rotate the polygon to test alternative grid alignments
        rot_poly = shapely_rotate(polygon, angle, origin='centroid')
        # Buffer the polygon to ensure circle centers can cover outer margins
        search_region = rot_poly.buffer(actual_buffer)
        
        for fx in shifts:
            for fy in shifts:
                centers = _hex_grid(search_region, radius, fx * d, fy * row_h)
                if len(centers) < best_n:
                    best_n = len(centers)
                    best_centers = _rotate_centers(centers, cx, cy, angle)
                    
    return best_centers
