import csv
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import transform, unary_union
import pyproj

def main():
    print("Wczytywanie z merged_islands.csv...")
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
            
    polygons = []
    for coords in islands.values():
         if len(coords) >= 3:
             polygons.append(Polygon(coords))

    # Kluczowy moment: Zamiana Stopni na Metry.
    # Standardowy układ GPS (WGS84) ma stopnie. Używamy biblioteki 'pyproj' 
    # aby przeliczyć je na płaski system mapowy Web Mercator (EPSG:3857), 
    # gdzie operujemy wprost na metrach przed buforowaniem.
    project_to_meters = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True).transform
    project_to_latlng = pyproj.Transformer.from_crs("epsg:3857", "epsg:4326", always_xy=True).transform
    
    buffered_polygons = []
    for poly in polygons:
        # Transformacja na metry
        poly_m = transform(project_to_meters, poly)
        
        # DODANIE MARGINESU 500 METRÓW
        buffered_poly_m = poly_m.buffer(500)
        
        # Transformacja z powrotem na stopnie szerokości/długości gps
        buffered_poly = transform(project_to_latlng, buffered_poly_m)
        buffered_polygons.append(buffered_poly)
        
    print("Ponowne klejenie wysp, na wypadek gdyby szerzej napuchnięte bufory zetknęły się ze sobą...")
    final_geometry = unary_union(buffered_polygons)
    
    if isinstance(final_geometry, Polygon):
        final_islands = [final_geometry]
    elif isinstance(final_geometry, MultiPolygon):
        final_islands = list(final_geometry.geoms)
    else:
        final_islands = []

    print(f"Po dodaniu 500m marginesu mamy w sumie do zapisania {len(final_islands)} wysp(y).")

    with open('buffered_islands.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['IslandId', 'VertexOrder', 'Latitude', 'Longitude'])
        
        i_id = 1
        for island in final_islands:
            coords = list(island.exterior.coords)
            for i, (lng, lat) in enumerate(coords):
                writer.writerow([i_id, i+1, lat, lng])
            i_id += 1
            
    print("Wygenerowano i pomyślnie obłożono granice. Zapisano do: buffered_islands.csv")

if __name__ == "__main__":
    main()
