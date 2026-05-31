"""
generate_api_points.py - Generuje listę współrzędnych (Lat, Lon) dla wywołań Google Maps API.
Cel: Wyspa nr 1 (S11), Algorytm: A4_Standard, Promień: 250m.
"""
import os
import csv
from shapely.geometry import Polygon
import pyproj

# Importujemy naszą lokalną logikę (brak żółtego podświetlania!)
from algo_logic import a4_standard

# Konfiguracja projekcji
to_meters = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
to_gps = pyproj.Transformer.from_crs("epsg:3857", "epsg:4326", always_xy=True)

def load_target_island():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'data', 'buffered_islands.csv')
    coords = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['IslandId'] == '2': # ZMIANA NA WYSPĘ 2
                x, y = to_meters.transform(float(row['Longitude']), float(row['Latitude']))
                coords.append((x, y))
    
    if not coords:
        raise ValueError("Nie znaleziono danych dla IslandId: 2 w pliku buffered_islands.csv")
    
    return Polygon(coords)

def main():
    print("--- PRZYGOTOWANIE PUNKTY API (Island 2 - LARGE) ---")
    
    island_poly = load_target_island()
    radius = 700.0  
    
    print(f"Szerokość obszaru: {island_poly.bounds[2] - island_poly.bounds[0]:.2f}m")
    
    # 2. Generowanie środków kół (Lokalny algorytm A4)
    centers_meters = a4_standard(island_poly, radius)
    
    print(f"Wygenerowano {len(centers_meters)} kół dla pełnego pokrycia.")
    
    # 3. Konwersja na GPS (Lat, Lon)
    api_points = []
    for x, y in centers_meters:
        lon, lat = to_gps.transform(x, y)
        api_points.append({
            'lat': lat,
            'lon': lon
        })
    
    print("\nLista 26 współrzędnych gotowych do zapytań API:")
    print("-" * 45)
    for i, pt in enumerate(api_points, 1):
        print(f"Punkt {i:02d}: {pt['lat']:.6f}, {pt['lon']:.6f}")
    print("-" * 45)
    
    return api_points

if __name__ == "__main__":
    points = main()
