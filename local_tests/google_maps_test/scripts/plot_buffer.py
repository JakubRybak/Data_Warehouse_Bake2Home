import csv
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def load_islands(csv_file):
    islands = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shp_id = int(row['IslandId'])
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            if shp_id not in islands:
                islands[shp_id] = []
            islands[shp_id].append((lng, lat))
    polys = []
    for coords in islands.values():
        if len(coords) >= 3:
            polys.append(Polygon(coords))
    return polys

def main():
    original = load_islands('merged_islands.csv')
    buffered = load_islands('buffered_islands.csv')

    fig, ax = plt.subplots(figsize=(10, 8))

    # KROK 1: Rysuj nowe, szersze wyspy jako podłoże (Kolor zielony)
    for poly in buffered:
        x, y = poly.exterior.xy
        ax.fill(x, y, alpha=0.4, color='#2ca02c', label='Margines 500m (Nowy rozmiar)')
        ax.plot(x, y, color='#2ca02c', linewidth=2, linestyle='--')

    # KROK 2: Rysuj stare wyspy nakładając je jako mniejszy element wgłębny
    for poly in original:
        x, y = poly.exterior.xy
        ax.fill(x, y, alpha=0.8, color='#d62728', label='Oryginalne Wyspy (Rdzewiejące)')
        ax.plot(x, y, color='#9e0000', linewidth=1.5)

    # Optymalizacja dublujących się wierszy w legendzie matplotlib
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    ax.set_title('Mapa 5: Testowe nałożenie 500m Marginesu (Bufora)', fontsize=15, pad=20, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect(1.6)

    plt.tight_layout()
    plt.savefig('plot_buffer.png', dpi=150)
    plt.close()
    print("Mapa wygenerowana i zapisana jako plot_buffer.png")

if __name__ == "__main__":
    main()
