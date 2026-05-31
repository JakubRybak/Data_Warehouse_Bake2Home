import json
import csv
import os

def export_json_to_pretty_csv():
    # Ścieżki relatywne do folderu ze skryptem
    base_dir = os.path.dirname(os.path.abspath(__file__))
    result_dir = os.path.join(base_dir, 'api_results')
    
    json_path = os.path.join(result_dir, 'raw_api_results.json')
    csv_path = os.path.join(result_dir, 'formatted_poi_results.csv')
    
    if not os.path.exists(json_path):
        print(f"BŁĄD: Nie znaleziono pliku {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Przygotowanie listy wierszy
    rows = []
    
    # Przetwarzamy wyniki z podziałem na kategorie
    for category_name, places in data.get('results', {}).items():
        if category_name == 'all_unique_data':
            continue
            
        for p in places:
            name = p.get('displayName', {}).get('text', 'N/A')
            address = p.get('formattedAddress', 'N/A')
            lat = p.get('location', {}).get('latitude', '')
            lon = p.get('location', {}).get('longitude', '')
            types = ", ".join(p.get('types', []))
            
            # Sub-kategoria dla jasności
            if category_name == 'bakeries':
                row_category = 'Piekarnia/Cukiernia'
            elif category_name == 'supermarkets':
                row_category = 'Supermarkets'
            else:
                continue # Nie eksportujemy innych do tego raportu

            rows.append({
                'Kategoria': row_category,
                'Nazwa': name,
                'Adres': address,
                'Szerokość (Lat)': lat,
                'Długość (Lon)': lon,
                'Typy Google': types
            })

    # Sortowanie: najpierw Piekarnie, potem Supermarkety
    rows.sort(key=lambda x: x['Kategoria'])

    # Zapis do CSV
    headers = ['Kategoria', 'Nazwa', 'Adres', 'Szerokość (Lat)', 'Długość (Lon)', 'Typy Google']
    
    try:
        with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"SUKCES: Utworzono plik {csv_path}")
        print(f"Eksportowano {len(rows)} unikalnych punktów POI.")
    except Exception as e:
        print(f"BŁĄD przy zapisie CSV: {e}")

if __name__ == "__main__":
    export_json_to_pretty_csv()
