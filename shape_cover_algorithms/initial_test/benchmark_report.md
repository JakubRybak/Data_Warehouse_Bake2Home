# Raport: Porównanie Algorytmów Pokrycia Kształtów (Shape Cover)

Uruchomiliśmy benchmark 10 algorytmów na 12 kształtach (10 losowych + 2 nasze wyspy z bazy danych). Celem było znalezienie ułożenia kół, które w 100% pokrywa obszar, przy minimalnej liczbie kół (zapytań API).

## Główne Wnioski

1.  **Ogromne Oszczędności**: Algorytmy **A9 (Simulated Annealing)** i **A10 (Hybrid)** są bezkonkurencyjne. Zredukowały one liczbę kół o ok. **40-50%** w stosunku do naiwnej siatki kwadratowej (A1).
2.  **Hex > Square**: Nawet najprostsza siatka heksagonalna (A2) jest o ok. 20-25% lepsza od kwadratowej (A1).
3.  **Wydajność**: Mimo że A9/A10 działają dłużej (ok. 10-40s), ich koszt obliczeniowy jest pomijalny w porównaniu do oszczędności finansowych na Google Places API.

## Tabela Wyników (Liczba Kół)

| Kształt | Typ | A1 (Sq) | A2 (Hex) | A4 (HexShift) | A9 (SA) | A10 (Hybrid) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S11** | **Wyspa DB 1** | 23 | 19 | 16 | **13** | 14 |
| **S12** | **Wyspa DB 2** | 25 | 18 | 15 | 13 | **12** |
| S01-S10 | Losowe | ~27 | ~20 | ~18 | **~15** | **~15** |

*Pełne dane dostępne w [results.csv](file:///C:/Projekty/Bake2Home/shape_cover_algorithms/results/results.csv)*

## Wizualizacje

Wygenerowane wykresy znajdują się w folderze `shape_cover_algorithms/plots/`:

- **[Mapa Wyników (Heatmap)](file:///C:/Projekty/Bake2Home/shape_cover_algorithms/plots/grid_heatmap.png)** – Porównanie wszystkich algo na wszystkich kształtach.
- **[Ranking i Kompromis](file:///C:/Projekty/Bake2Home/shape_cover_algorithms/plots/summary_bar.png)** – Średnia skuteczność i czas działania.
- **Wykresy per kształt**: folder `per_shape/` zawiera szczegółowe słupki dla każdego testu.

## Rekomendacja

Do produkcyjnego skryptu wybieramy **A10 (Hybrid)**. Jest stabilny, bardzo szybki (dzięki startowi z Hex Shift) i daje wyniki niemal identyczne (a czasem lepsze) niż czyste Simulated Annealing.

Czy chcesz, abym teraz zaimplementował docelowy skrypt `generate_grid.py`, który użyje algorytmu A10 do wygenerowania punktów zapytania dla Twoich wysp?
