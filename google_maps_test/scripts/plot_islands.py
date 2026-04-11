import csv
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def plot_polygons(csv_in, out_image, title, is_island=False):
    shapes = {}
    id_col = 'IslandId' if is_island else 'LocationId'
    
    with open(csv_in, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shp_id = int(row[id_col])
            lat = float(row['Latitude'])
            lng = float(row['Longitude'])
            if shp_id not in shapes:
                shapes[shp_id] = []
            shapes[shp_id].append((lng, lat))
            
    fig, ax = plt.subplots(figsize=(10, 8))
    
    for shp_id, coords in shapes.items():
        if len(coords) < 3: continue
        poly = Polygon(coords)
        x, y = poly.exterior.xy
        
        # Style
        if is_island:
            ax.plot(x, y, color='#d62728', alpha=0.7, linewidth=3, solid_capstyle='round')
            ax.fill(x, y, alpha=0.3, color='#d62728')
        else:
            ax.plot(x, y, color='#1f77b4', alpha=0.8, linewidth=1.5)
            ax.fill(x, y, alpha=0.3, color='#add8e6')

    ax.set_title(title, fontsize=15, pad=20, fontweight='bold')
    ax.set_xlabel('Longitude (Długość Geograficzna)', fontsize=12)
    ax.set_ylabel('Latitude (Szerokość Geograficzna)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Zachowanie proporcji mapy Europy
    ax.set_aspect(1.6) 
    
    plt.tight_layout()
    plt.savefig(out_image, dpi=150)
    plt.close()

if __name__ == '__main__':
    print("Rysowanie mapy nr 1...")
    plot_polygons('active_locations.csv', 'plot_locations.png', 'Mapa 1: Pojedyncze 20 stref (Locations)', is_island=False)
    
    print("Rysowanie mapy nr 2...")
    plot_polygons('merged_islands.csv', 'plot_islands.png', 'Mapa 2: Zmergowane 3 Wielkie Wyspy', is_island=True)
    
    print("Zakończono renderowanie!")
