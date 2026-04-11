import csv
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def main():
    print("Ładowanie danych...")
    # Ładowanie punktów klientów
    lats = []
    lngs = []
    try:
        with open('customers.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lats.append(float(row['Latitude']))
                lngs.append(float(row['Longitude']))
    except Exception as e:
        print(f"Błąd ładowania customers.csv: {e}")
        return

    # Ładowanie ulepionych wysp (kształtów stref)
    islands = {}
    try:
        with open('merged_islands.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                shp_id = int(row['IslandId'])
                lat = float(row['Latitude'])
                lng = float(row['Longitude'])
                if shp_id not in islands:
                    islands[shp_id] = []
                islands[shp_id].append((lng, lat))
    except Exception as e:
        print(f"Błąd ładowania merged_islands.csv: {e}")
        return

    print("Rysowanie połączonej mapy...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # KROK 1: Rysuj Poligony Wysp (Kładziemy plamy jako tło)
    for shp_id, coords in islands.items():
        if len(coords) < 3: continue
        poly = Polygon(coords)
        x, y = poly.exterior.xy
        
        # Gruby obrys i przezroczyste wypełnienie farbą czerwoną
        ax.plot(x, y, color='#d62728', alpha=0.8, linewidth=3, solid_capstyle='round', zorder=2)
        ax.fill(x, y, alpha=0.15, color='#d62728', zorder=1)

    # KROK 2: Rysuj Klientów (Rzucamy ich precyzyjnie na wierzch stref)
    # Rozświetlone fioletowe kropki
    ax.scatter(lngs, lats, color='#8a2be2', s=20, alpha=0.7, edgecolors='white', linewidths=0.5, zorder=3)
    
    ax.set_title('Mapa 4: Ścisły związek Klientów z ich Wyspami', fontsize=15, pad=20, fontweight='bold')
    ax.set_xlabel('Longitude (Długość Geograficzna)', fontsize=12)
    ax.set_ylabel('Latitude (Szerokość Geograficzna)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Skalowanie mapowe
    ax.set_aspect(1.6)
    
    plt.tight_layout()
    out_img = 'plot_combined.png'
    plt.savefig(out_img, dpi=150)
    plt.close()
    
    print(f"Pomyślnie nałożono i wygenerowano plik tła: {out_img}")

if __name__ == '__main__':
    main()
