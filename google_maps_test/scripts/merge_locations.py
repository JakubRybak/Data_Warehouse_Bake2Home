import csv
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

def load_polygons_from_csv(filename):
    locations = {}
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            loc_id = int(row['LocationId'])
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            
            if loc_id not in locations:
                locations[loc_id] = []
            locations[loc_id].append((lng, lat))
            
    polygons = []
    for loc_id, coords in locations.items():
        if len(coords) >= 3:
            polygons.append(Polygon(coords))
            
    return polygons

def save_islands_to_csv(geometry, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['IslandId', 'VertexOrder', 'Latitude', 'Longitude'])
        
        # Geometria po sklejeniu może być jednym wielkim poligonem (Polygon)
        # albo zbiorem kilku odizolowanych wysp (MultiPolygon)
        if isinstance(geometry, Polygon):
            islands = [geometry]
        elif isinstance(geometry, MultiPolygon):
            islands = list(geometry.geoms)
        else:
            islands = []
            
        island_id = 1
        for island in islands:
            # Chcemy zewnętrzny kontur obrysu wyspy (exterior.coords z Shapely)
            coords = list(island.exterior.coords)
            for i, (lng, lat) in enumerate(coords):
                writer.writerow([island_id, i+1, lat, lng])
            island_id += 1

def main():
    print("1/3 Wczytywanie z active_locations.csv...")
    try:
        polygons = load_polygons_from_csv('active_locations.csv')
        print(f"Pomyślnie wczytano {len(polygons)} stref (Locations) do połączenia.")
    except Exception as e:
        print(f"Błąd podczas wczytywania: {e}")
        return
    
    print("2/3 Klejenie sąsiadujących stref (Unary Union z Shapely)...")
    # To jest to jedno potężne słowo w Pythonie, które z zębatych małych kawałków
    # łączy wszystko co do siebie przylega w gigantyczne obrysy!
    merged_geometry = unary_union(polygons)
    
    if isinstance(merged_geometry, Polygon):
        print("=> Geometria obwieszcza: Utworzono 1 wielką połączoną wyspę!")
    elif isinstance(merged_geometry, MultiPolygon):
        print(f"=> Geometria obwieszcza: Utworzono {len(merged_geometry.geoms)} wysp(y). Niektóre strefy są od siebie oderwane (nie dotykają się).")
    else:
        print("=> Nieoczekiwany kształt.")
         
    print("3/3 Zapisywanie geometrycznego kształtu obrysu wysp do merged_islands.csv...")
    save_islands_to_csv(merged_geometry, 'merged_islands.csv')
    print("Zakończono sukcesem! Sprawdź wygenerowany plik.")

if __name__ == "__main__":
    main()
