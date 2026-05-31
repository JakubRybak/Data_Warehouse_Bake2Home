import csv
from shapely.geometry import Polygon
from shapely.ops import nearest_points
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def check_distances():
    islands = {}
    with open('merged_islands.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shp_id = int(row['IslandId'])
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            if shp_id not in islands:
                islands[shp_id] = []
            islands[shp_id].append((lng, lat))
            
    polys = {}
    for i_id, coords in islands.items():
        polys[i_id] = Polygon(coords)
        
    ids = list(polys.keys())
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            id1 = ids[i]
            id2 = ids[j]
            p1, p2 = nearest_points(polys[id1], polys[id2])
            dist_m = haversine(p1.y, p1.x, p2.y, p2.x)
            print(f"Najkrótsza odległość między Wyspą {id1} a Wyspą {id2} to około: {dist_m:.1f} metrów")

if __name__ == '__main__':
    check_distances()
