import subprocess
import csv
from shapely.geometry import Point, Polygon

def run_db_query(db_name, query):
    """Pomocnicza funkcja do uruchamiania poleceń SQL w kontenerze Dockera"""
    escaped_query = query.replace('"', '\\"')
    cmd = f'docker exec -i postgres_db psql -U admin -d {db_name} -t -A -c "{escaped_query}"'
    try:
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        return [line.strip() for line in output.split('\n') if line.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas uruchamiania zapytania w {db_name}: {e}")
        return []

def main():
    print("1/3 Pobieranie adresów Klientów z bazy...")
    customer_lines = run_db_query(
        "customer-manager-db",
        'SELECT "Latitude", "Longitude" FROM "CustomerAddress" WHERE "Latitude" > 0 AND "Longitude" > 0;'
    )
    
    customers = []
    for line in customer_lines:
        parts = line.split('|')
        if len(parts) == 2:
            try:
                lat = float(parts[0])
                lng = float(parts[1])
                # W Shapely konwencją jest rzutowanie (X, Y) w tym układzie (Longitude, Latitude)
                customers.append(Point(lng, lat))
            except ValueError:
                pass
    print(f"   => Pomyślnie przetworzono {len(customers)} punktów z bazy klientów.\n")

    print("2/3 Pobieranie Siatki Stref (Locations) z bazy...")
    polygon_lines = run_db_query(
        "client-manager-db",
        'SELECT "LocationId", "Latitude", "Longitude" FROM "PolygonVertex" ORDER BY "LocationId", "Id";'
    )
    
    locations = {}
    for line in polygon_lines:
        parts = line.split('|')
        if len(parts) == 3:
            loc_id = int(parts[0])
            lat = float(parts[1])
            lng = float(parts[2])
            if loc_id not in locations:
                locations[loc_id] = []
            locations[loc_id].append((lng, lat))
            
    print(f"   => Odnaleziono {len(locations)} zdefiniowanych Stref.\n")

    print("3/3 Rozpoczęcie analizy przestrzennej: Szukanie Miejsc Aktywnych (zawierających klientów)...")
    active_locations = []
    
    for loc_id, coords in locations.items():
        if len(coords) >= 3:
            poly = Polygon(coords)
            count_inside = 0
            
            for pt in customers:
                if poly.contains(pt):
                    count_inside += 1
                    
            if count_inside > 0:
                active_locations.append({
                    'loc_id': loc_id, 
                    'customer_count': count_inside, 
                    'vertices': coords
                })

    print("-" * 50)
    print(f"MAMY TO! Znaleziono {len(active_locations)} AKTYWNYCH stref.")
    print("Zapisywanie punktów do pliku CSV (active_locations.csv)...")

    # Zapis do pliku CSV
    csv_file = "active_locations.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['LocationId', 'CustomerCount', 'VertexOrder', 'Latitude', 'Longitude'])
        
        for al in sorted(active_locations, key=lambda x: x['customer_count'], reverse=True):
            for i, (lng, lat) in enumerate(al['vertices']):
                writer.writerow([al['loc_id'], al['customer_count'], i+1, lat, lng])
                
    print(f"Dane odcedzone ze śmieci! Pomyślnie zapisano do: {csv_file}")
            
if __name__ == "__main__":
    main()
