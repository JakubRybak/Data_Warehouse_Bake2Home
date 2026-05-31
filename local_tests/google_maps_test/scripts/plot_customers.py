import csv
import matplotlib.pyplot as plt

def main():
    print("Wyświetlanie mapy z klientami z pliku customers.csv...")
    lats = []
    lngs = []
    
    try:
        with open('customers.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lats.append(float(row['Latitude']))
                lngs.append(float(row['Longitude']))
    except FileNotFoundError:
        print("Nie znaleziono pliku customers.csv. Uruchom najpierw export_customers.py")
        return
            
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Rysowanie kropek punkt po punkcie
    # Kolor niebieski z lekką przezroczystością (alpha), żeby widzieć skupiska
    ax.scatter(lngs, lats, color='#8a2be2', s=15, alpha=0.5, edgecolors='none', zorder=3)
    
    ax.set_title('Mapa 3: Indywidualne lokalizacje klientów', fontsize=15, pad=20, fontweight='bold')
    ax.set_xlabel('Longitude (Długość)', fontsize=12)
    ax.set_ylabel('Latitude (Szerokość)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Zachowanie proporcji typowych dla mapy świata w tych współrzędnych
    ax.set_aspect(1.6)
    
    plt.tight_layout()
    out_img = 'plot_customers.png'
    plt.savefig(out_img, dpi=150)
    plt.close()
    print(f"Mapa pomyślnie wygenerowana: {out_img}")

if __name__ == '__main__':
    main()
