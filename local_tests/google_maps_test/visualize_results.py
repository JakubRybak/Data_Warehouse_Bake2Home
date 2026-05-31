import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import os
import csv
import pyproj

# Transformatory współrzędnych
to_meters = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)

def load_island_polygon(island_id):
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'buffered_islands.csv')
    coords = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['IslandId'] == str(island_id):
                coords.append((float(row['Longitude']), float(row['Latitude'])))
    return Polygon(coords)

def visualize_pois_on_island(island_id=2):
    base_dir = os.path.dirname(__file__)
    poi_csv_path = os.path.join(base_dir, 'api_results', 'formatted_poi_results.csv')
    output_img = os.path.join(base_dir, 'api_results', 'coverage_map.png')
    
    # 1. Wczytaj dane
    island_poly = load_island_polygon(island_id)
    pois_df = pd.read_csv(poi_csv_path)

    # 2. Przygotuj wykres
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Rysuj wyspę (kontur i półprzezroczyste wypełnienie)
    x, y = island_poly.exterior.xy
    ax.fill(x, y, alpha=0.1, color='green', label=f'Strefa Dostaw (Island {island_id})')
    ax.plot(x, y, color='green', linewidth=2, linestyle='--')

    # 3. Rysuj punkty POI z podziałem na kategorie
    categories = {
        'Piekarnia/Cukiernia': {'color': 'orange', 'marker': 'o', 'size': 60, 'label': 'Piekarnia/Cukiernia'},
        'Supermarkets': {'color': 'blue', 'marker': 's', 'size': 80, 'label': 'Supermarket'}
    }

    for cat_name, style in categories.items():
        subset = pois_df[pois_df['Kategoria'] == cat_name]
        if not subset.empty:
            ax.scatter(
                subset['Długość (Lon)'], 
                subset['Szerokość (Lat)'], 
                c=style['color'], 
                marker=style['marker'], 
                s=style['size'], 
                label=style['label'],
                zorder=5,
                alpha=0.8
            )

    # 4. Kosmetyka wykresu
    ax.set_title(f"Wizualizacja POI na Wyspie nr {island_id} (Raszyn)", fontsize=15)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(loc='upper right', frameon=True)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Ustaw aspekt geograficzny (żeby mapa nie była rozciągnięta)
    ax.set_aspect('equal', adjustable='datalim')

    # 5. Zapisz i zamknij
    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"SYKCES: Mapa została wygenerowana i zapisana w: {output_img}")

if __name__ == "__main__":
    visualize_pois_on_island(2)
