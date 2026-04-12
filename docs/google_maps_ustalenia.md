## Założenia problemu
- `Google Maps Api (NEW)` ma opcje `Nearby Search` która po tagach filtruje, przyjmuje współrzędne i promień i sprawdza okręg-
- Limit miejsc na zapytanie: **20**
- Założenie jest że wszyscy klienci znajdują się w jakims `Locations` 
## Cel:
- Znalezienie wszystkich piekarni we wszystkich `Locations` + `bufor`
## Proponowany algorytm
#### 1. Bierzemy locations (potencjalnie tylko te gdzie sa jacys klienci, trzeba sie jakos uchronić przed sztucznymi locations)
#### 2. Lączymy sąsiadujące locations żeby powstały rozlączne wyspy. 
#### 3. Do wysp dodajemy buffor umowny np. 500m
#### 4. Po dodaniu bufora łączymy zazębiające się wyspy co tworzy ostateczne rozłączne wyspy które trzeba pokryć
#### 5. Każdą z wysp pokrywamy okręgami (o umownej maksymalnej średnicy np. 700m) algorytmem A4_Standard (tak wyszło z testów)
#### 6. Dla każdego z tych okręgów robimy zapytanie do Google Maps API i zapisujemy wyniki do pliku po usunięciu duplikatów 
#### 7. (Optional) Wyfiltrowywanie sztywne Żabek, Cerfourów Express itp.

----------------

#### **Algorytm A4_Standard**

**Zasada działania:**
1. **Siatka Heksagonalna:** Układa koła w strukturę plastra miodu – jest to matematycznie najefektywniejszy sposób na pokrycie terenu (minimalizuje nakładanie się kół i puste miejsca).
2. **Optymalizacja Przestrzenna:** Algorytm nie nakłada siatki statycznie. Testuje on dziesiątki wariantów ułożenia poprzez:
   * **Rotację:** Obracanie siatki o kąty od 0° do 60°.
   * **Translację:** Przesuwanie siatki o niewielkie przesunięcia (offsety) X i Y.
3. **Wybór Najlepszego Wariantu:** System wybiera tę konfigurację, która generuje **najmniejszą liczbę punktów okręgów** przy jednoczesnym zachowaniu 100% pokrycia obszaru.
