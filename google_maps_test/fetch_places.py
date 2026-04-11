"""
fetch_places.py - Pobiera dane z Google Places API (New) dla wyznaczonych punktów.
"""
import os
import json
import requests
from dotenv import load_dotenv

# Importujemy mapowanie punktów z poprzedniego skryptu
from generate_api_points import main as get_points

# Załadowanie klucza API z pliku .env (szukamy go w tym samym folderze co skrypt)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '').strip()

if API_KEY:
    print(f"DEBUG: Klucz wczytany poprawnie (początek: {API_KEY[:4]}...)")
else:
    print("DEBUG: Klucz jest pustY!")

def fetch_nearby_places(lat, lon, radius=700.0):
    endpoint = "https://places.googleapis.com/v1/places:searchNearby"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        # FieldMask decyduje za co płacimy i co dostajemy
        "X-Goog-FieldMask": "places.id,places.displayName,places.primaryType,places.types,places.location,places.formattedAddress"
    }
    
    body = {
        "includedTypes": ["bakery", "pastry_shop", "supermarket"],
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": radius
            }
        }
    }
    
    response = requests.post(endpoint, headers=headers, json=body)
    if response.status_code != 200:
        print(f"Błąd API ({response.status_code}): {response.text}")
        return []
    
    return response.json().get('places', [])

def main():
    if not API_KEY:
        print("BŁĄD: Nie znaleziono GOOGLE_MAPS_API_KEY w pliku .env")
        return

    # 1. Pobierz punkty wygenerowane przez A4_Standard
    points = get_points()
    
    all_found_places = {} # Używamy słownika z place_id jako kluczem (automatyczna deduplikacja)
    
    print(f"\nRozpoczynam pobieranie danych dla {len(points)} punktów...")
    
    for i, pt in enumerate(points, 1):
        print(f"[{i}/{len(points)}] Szukam w okolicy {pt['lat']:.5f}, {pt['lon']:.5f}...", end=" ")
        places = fetch_nearby_places(pt['lat'], pt['lon'])
        
        new_count = 0
        for p in places:
            pid = p['id']
            if pid not in all_found_places:
                all_found_places[pid] = p
                new_count += 1
        
        print(f"Znaleziono {len(places)} miejsc (w tym {new_count} nowych).")

    # 2. Podział na koszyki
    bakeries = []
    supermarkets = []
    others = []
    
    for p in all_found_places.values():
        types = p.get('types', [])
        
        if 'bakery' in types or 'pastry_shop' in types:
            bakeries.append(p)
        elif 'supermarket' in types:
            supermarkets.append(p)
        else:
            others.append(p)

    # 3. Przygotowanie i zapisanie wyników do pliku
    output = {
        "summary": {
            "total_unique_places": len(all_found_places),
            "bakeries_count": len(bakeries),
            "supermarkets_count": len(supermarkets),
            "others_count": len(others)
        },
        "results": {
            "bakeries": bakeries,
            "supermarkets": supermarkets,
            "others": others,
            "all_unique_data": list(all_found_places.values())
        }
    }

    result_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_results')
    os.makedirs(result_dir, exist_ok=True)
    json_path = os.path.join(result_dir, 'raw_api_results.json')
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        
    print("\n" + "="*40)
    print(f"FINAŁ: Znaleziono łącznie {len(all_found_places)} unikalnych miejsc.")
    print(f" - Piekarnie/Cukiernie: {len(bakeries)}")
    print(f" - Supermarkety: {len(supermarkets)}")
    print("="*40)
    print(f"Szczegółowe dane zapisano w: {json_path}")

if __name__ == "__main__":
    main()
