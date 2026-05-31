# Historia promptów — Claude Code

Dokumentacja wykorzystania narzędzia AI (Claude Code) w projekcie Bake2Home Data Warehouse.
Każdy wpis zawiera treść prompta oraz timestamp (czas lokalny, Europe/Warsaw).

---

## 2026-05-10

### 10:xx — Test granulacji ICON-D2 nad Raszynem

**Prompt:**
```
execute this

#!/usr/bin/env python3
"""Test granulacji ICON-D2 nad Raszynem - 25 punktów w kwadracie ~1.2 x 1.3 km."""
...
[skrypt testujący 25 punktów siatki 5x5 nad Raszynem, pobierający dane z open-meteo API]
```

**Cel:** Sprawdzenie efektywnej rozdzielczości przestrzennej modelu ICON-D2 — ile unikalnych komórek siatki pokrywa kwadrat ~1.2×1.3 km nad Raszynem.

**Wynik:** 2 unikalne komórki siatki z 25 zapytań. Cały obszar Raszyna pokryty przez jedną komórkę (~6.25 km rozdzielczość efektywna).

---

### 10:xx — Zmiana daty na wtorek

**Prompt:** `ok can we change date to tuesday`

**Cel:** Powtórzenie testu granulacji dla wtorku 2026-05-12.

**Wynik:** Identyczna struktura siatki, 0.00 mm (model ICON-D2 nie sięga tak daleko — poza horyzontem prognozy).

---

### 10:xx — Znalezienie dnia z opadem w ostatnim miesiącu

**Prompt:** `nah its okay lets find from the last month for one point at least one with more than 0 and for that day run 25 points test`

**Cel:** Weryfikacja granulacji na realnym dniu deszczowym — znalezienie dnia z opadem >0 i uruchomienie testu 25-punktowego.

**Wynik:**
- Najbardziej deszczowy dzień w ostatnim miesiącu: 2026-05-07 (5.9 mm wg archive-api)
- Test 25 punktów: 2 unikalne komórki siatki, wartości 2.00 mm i 5.90 mm
- Kluczowe odkrycie: historical-forecast-api zwrócił 0.00 mm dla tego dnia — model D-1 nie przewidział opadu

---

### 11:xx — Weryfikacja historical-forecast-api vs archive-api

**Prompt:** `ok so theres no interpolation from openmeteo based on lat lan`

**Kontekst:** Pytanie o mechanizm działania open-meteo — czy API interpoluje wartości między węzłami siatki.

**Wynik (badanie):** Open-meteo stosuje nearest-neighbor snapping — brak interpolacji przestrzennej.

---

### 11:xx — Prognoza poranna kwiecień 2026

**Prompt:**
```
sprawdz dla calego kwietnia to [skrypt pobierający prognozę 6:00-10:00 z historical-forecast-api]
```

**Cel:** Uruchomienie skryptu prognozy porannej okno 6-10 dla całego kwietnia 2026, model icon_d2.

**Wynik:** icon_d2 zwraca wszystkie zera — brak archiwalnych biegów dla tego okresu. Przełączono na `best_match`.

---

### 11:xx — Porównanie best_match vs default

**Prompt:** `a jak zamienimy na best_match / default`

**Wynik:** Identyczne wartości we wszystkich 30 dniach — `best_match` i brak parametru `models` to alias.

---

### 11:xx — Test dnia kolejnego (D+1)

**Prompt:** `wgat about day later?` *(typo: what about day later)*

**Cel:** Sprawdzenie czy D-1 prognoza myliła się nie tylko dla 2026-05-07, ale też dla 2026-05-08.

**Wynik:** Ten sam pattern — 2026-05-08 archive-api: 0.30 mm, historical-forecast-api: 0.00 mm. Dwa kolejne dni z zerem prognozy vs rzeczywistym opadem. Kluczowe odkrycie: ICON-D2 D-1 rano systematycznie przegapił epizod opadowy 07-08 maja.

---

### 11:xx — Czy jakikolwiek forecast zwraca niezerowe wartości dla kwietnia

**Prompt:** `do we have any forecast that actually doesnt return 0? check april for 1c point`

**Cel:** Weryfikacja czy historical-forecast-api (ICON-D2) w ogóle zwraca niezerowe wartości dla Raszyna w całym kwietniu.

**Wynik:** Pusta tabela — icon_d2 zwraca wszystkie zera dla kwietnia 2026 (brak archiwalnych biegów modelu). To zmotywowało przełączenie na best_match i skrypt przeglądu całego miesiąca.

---

### 11:xx — Marzec 2026

**Prompt:** `a marzec?`

**Wynik:** 2 dni deszczowe rano w marcu: 2026-03-20 (93% prob, 0.90 mm) i 2026-03-26 (86% prob, 2.90 mm). Wykryto bug w etykietach godzin — naprawiono.

---

### 11:xx — Weryfikacja etykiet godzin

**Prompt:** `czekaj czyli godziny na pewno sie zgadzaja?`

**Cel:** Sprawdzenie czy wyświetlane godziny (06-10) faktycznie odpowiadają wartościom z okna porannego.

**Wynik:** Bug potwierdzony — `times[i]` brało indeksy 0–4 z oryginalnej tablicy (godziny 00–04), zamiast godzin z okna 6–10. Wartości mm i % były poprawne, etykiety fałszywe. Naprawiono przez śledzenie oddzielnej listy `wt` (window times).

---

### 11:xx — Wstępna propozycja: prognoza do fact_order_item

**Prompt:** `ok i taka prognoze w sumie najlepiej byloby dodawac do fact_order_item?`

**Cel:** Pytanie o właściwe miejsce w modelu dla danych pogodowych.

**Wynik:** Odpowiedź wstępna — nie bezpośrednio do fact_order_item. Zaproponowane dwa warianty: (1) extend DIM_DATE — dla jednego Raszyna, (2) osobna DIM_WEATHER_FORECAST — dla wielu lokalizacji. Rekomendacja: DIM_DATE jako najprostsze.

---

## 2026-05-11

### 09:xx — Orientacja w projekcie po git clone

**Prompt:**
```
trochę porobilem

https://github.com/JakubRybak/Data_Warehouse_Bake2Home

możesz podać swojego maila to ci dam contributora

w diagrams sa diagramy z pgadmina
w docs sa notatki @ustalenia.md to to jest ważne do przeczytania
w docs @full_schema_dump.txt to elegancki schema
i w models jest cały model hurtowni — jest praktycznie skonczony

nowy update — dodałem nowe rzeczy do modelu, ogarnalem dokładnie jak sie obchodzić z google maps api,
rozkminilem algorytm, zrobiłem testy i elegancko dziala

Przeanalizuj projekt i commity i powiedz co zrobil Jakub i co mi zostalo do zrobienia
```

**Cel:** Orientacja w projekcie po klonowaniu repo Jakuba. Przekazanie kontekstu o stanie projektu i podziale pracy.

**Wynik:**
- Jakub zbudował: model konstelacyjny (drawio), diagramy pgAdmin (8 baz), full_schema_dump.txt, pipeline Google Maps API (algo A4_Standard, hexagonalne pokrycie), docker-compose
- Google Maps wyniki wkomponowane w DIM_CUSTOMER jako pre-zagregowane atrybuty (COMP_BAKERY_COUNT_*, DIST_TO_NEAREST_*)
- Do zrobienia dla Adama: moduł pogody, deployment pipeline ELT, Docker z danymi, decyzje biznesowe z Krzyśkiem

---

### 09:xx — Weryfikacja integracji Google Maps w modelu drawio

**Prompt:** `czy jakub wkomponowal ten google maps api i jego wyniki w Models/Constelation_main.drawio?`

**Cel:** Sprawdzenie czy wyniki pipeline'u Google Maps (liczba konkurentów, odległości) są już w modelu hurtowni.

**Wynik:** Tak — wkomponowane bezpośrednio w DIM_CUSTOMER jako atrybuty wyliczone podczas ETL:
- `COMP_BAKERY_COUNT_300M/500M/1000M/2000M`
- `COMP_SUPERMARKET_COUNT_500M/1000M/2000M/3000M`
- `OWN_SITE_COUNT_300M/500M/1000M/2000M/3000M`
- `DIST_TO_NEAREST_OWN_SITE_M`, `DIST_TO_NEAREST_COMP_BAKERY_M`, `DIST_TO_NEAREST_COMP_SUPERMARKET_M`
- DIM_COMPETITORS jako osobna tabela wymiarów z SCD Type 2 (VALID_FROM/TO/IS_CURRENT)

---

### 09:xx — Wyjaśnienie hierarchii w modelu hurtowni

**Prompt:** `o co chodzi z hierarchiami? Projektowanie modelu hurtowni danych uwzględniającego tabele faktowe (dedykowane typy), wymiary i ich zmienność, hierarchie, miary, agregaty, itp.`

**Cel:** Wyjaśnienie konceptu hierarchii w kontekście wymagań projektowych (KM2).

**Wynik:**
- Hierarchia = naturalne poziomy agregacji (drill-down/roll-up) w wymiarze
- 3 podejścia: **Flat** (Kimball, spłaszczone kolumny — najczęstsze), **Snowflake** (znormalizowane osobne tabele), **Bridge** (dla hierarchii nieregularnych o zmiennej głębokości)
- Przykłady w Bake2Home: DIM_DATE (Rok→Kwartał→Miesiąc→Tydzień→Dzień), DIM_LOCATION (Kraj→Województwo→Miasto→Lokalizacja), DIM_PRODUCT (Typ→Produkt→Oferta)
- Jakub zastosował podejście Kimball flat + bridge tables dla M:N (BRIDGE_OFFER_PRODUCT, BRIDGE_PRODUCT_ALLERGEN) + SCD2 dla zmienności
- Miary: addytywne (QUANTITY — SUM), póładdytywne (STOCK_LEVEL), nieaddytywne (DISCOUNT_PERCENT — tylko AVG/MIN/MAX)

---

### 09:xx — Sprawdzenie czy model ma tabele agregacyjne

**Prompt:** `ale to mamy agregacje czy nie?`

**Cel:** Weryfikacja czy w modelu Jakuba są dedykowane tabele agregacyjne (AGG_*).

**Wynik:** Brak dedykowanych tabel agregacyjnych — wszystkie fakty na poziomie transakcyjnym. Atrybuty Google Maps w DIM_CUSTOMER to pre-zagregowane atrybuty wymiaru (obliczone raz podczas ETL), nie tabele agregacyjne w sensie hurtowniowym. Tabele AGG nie są potrzebne na tym etapie projektu — BI tools (Power BI, Looker Studio) robią agregacje samodzielnie.

---

### 09:xx — Opis procesu ETL

**Prompt:** `a co tutaj moga chciec? Opis planowanego procesu ETL ze szczególnym uwzlędnieniem sposobu transformacji i integracji danych`

*(przerwane — Claude chciał czytać schema)*

**Prompt:** `nie no ogolnie odpowiedz`

**Cel:** Ogólna odpowiedź bez czytania plików — czego oczekuje egzaminator w opisie ETL.

**Wynik:** Trzy elementy ETL dla Bake2Home:
- **Extract**: 6 baz źródłowych, full load vs. incremental (po kolumnie Updated), nocny batch
- **Transform** (serce odpowiedzi): surrogate keys, SCD Type 2, łączenie danych z różnych baz (planner-db + customer-manager + wallet-db → FACT_ORDER_ITEM), miary pochodne (DISCOUNT_PERCENT), denormalizacja (DIM_SITE = Site + Client + SiteCoordinates), atrybuty zewnętrzne (Google Maps → DIM_CUSTOMER)
- **Load**: kolejność ładowania (wymiary → fakty), insert vs. upsert dla SCD2, obsługa błędów

---

### 09:xx — Estymacja pozostałej pracy i podział zadań

**Prompt:**
```
ocen ile tu jeszcze pracy zeby to zrobic na odwal sie TODO:
- Rozszerzony opis zbiorów danych (Adam pogoda, Jakub maps)
- KM2 Projektowanie modelu (hierarchie, miary, agregaty, harmonogram odświeżania, SCD2)
- Model fizyczny (tabele, kolumny, typy danych, wymagalność, relacje)
- Opis kluczowych miar i atrybutów
- Opis planowanych raportów
- Opis planowanego procesu ETL
i zaproponuj podzial biorac pod uwage ze Jakub zrobil wczesniej ten model
```

**Cel:** Realistyczna ocena nakładu pracy i podział zadań między Adama i Jakuba.

**Wynik (estymacja):**
| Deliverable | Stan | Praca |
|---|---|---|
| Opis zbiorów danych — Maps | Jakub ma google_maps_ustalenia.md | ~1h |
| Opis zbiorów danych — Pogoda | Nic nie ma | ~2-3h |
| Model KM2 | Drawio gotowy, brak hierarchii/harmonogramu | ~2h |
| Model fizyczny (typy danych) | Drawio bez typów kolumn | ~3-4h |
| Opis miar i atrybutów | Nic nie ma | ~2h |
| Opis planowanych raportów | Nic nie ma | ~1-2h |
| Opis ETL | Nic nie ma | ~2-3h |

**Łącznie: ~13-15h**

**Podział:** Jakub (model fizyczny, miary, Maps, transformacje ETL) / Adam (pogoda, raporty, hierarchie + harmonogram odświeżania do KM2)

---

### 09:xx — Korekta: robimy ELT nie ETL

**Prompt:** `ale my robimy jednak ELT [zdjęcie architektury GCS → BigQuery → Dataform]`

**Cel:** Korekta — stack to GCS + BigQuery + Dataform, czyli ELT a nie ETL.

**Wynik:** Zaktualizowany opis procesu:
- **E** — zrzut danych do GCS (Parquet/JSON/CSV)
- **L** — załadowanie surowych danych do staging tables w BigQuery z GCS
- **T** — Dataform robi transformacje SQL wewnątrz BigQuery (surrogate keys, SCD2, joiny)

Harmonogram odświeżania: Bake2Home 3×/tydzień (Scheduled), Open-Meteo 3×/tydzień (Scheduled), Google Maps tylko przy nowym obszarze dostawy (Event-driven)

---

### 09:xx — Zaktualizowany podział zadań (po korekcie ELT)

**Prompt:** `ok to wrocmy do podzialu`

**Cel:** Finalny podział zadań z uwzględnieniem stosu ELT (BigQuery + Dataform).

**Wynik:**
- **Jakub**: model fizyczny (typy w drawio), opis miar i atrybutów, opis zbiorów danych Maps, opis procesu ELT — część T (transformacje Dataform: SCD2, surrogate keys, joiny)
- **Adam**: opis zbiorów danych Open-Meteo, opis procesu ELT — część E i L (GCS, staging, scheduling), opis planowanych raportów (Looker Studio), hierarchie + harmonogram odświeżania do KM2

---

### 09:xx — Propozycja DIM_SITE daily

**Prompt:** `ok de facto potrzebujemy dwoch wartosci rainyMorningMaxProb oraz rainyMorningPrecipSum czy cos takiego no i mysle zeby je dodac do DIM_SITE i po prostu zrobic tak zeby on byl daily czy to m sens?`

**Wynik:** DIM_SITE daily — nie. Problem: DIM_SITE jest SCD Type 2 — miesza wolnozmienną (adres, współrzędne, raz na kilka miesięcy) z szybkozmienną (pogoda codziennie). Poprawne opcje: extend DIM_DATE lub FACT_WEATHER_DAILY.

---

### 09:xx — Pytanie o BRIDGE_WEATHER_DAILY

**Prompt:** `a to nie bedzie BRIDGE_WEATHER_DAILY?`

**Wynik:** Nie — bridge table rozwiązuje relację M:N. Data × site = jeden rekord pogody = relacja 1:1. Poprawna nazwa to `FACT_WEATHER_DAILY` (ma miary: mm, %) lub `DIM_WEATHER_DAILY` (czysto opisowa). FACT_WEATHER_DAILY poprawniejsze Kimballa, ale przy jednym Raszyniu dwie kolumny w DIM_DATE wystarczą.

---

### 09:xx — Argument za fact_order_item

**Prompt:** `a czemu nie mozemy dac tego po prostu do fact order item`

**Wynik:** Technicznie można — BigQuery columnar compression kompresuje powtarzające się wartości. Jedyny argument przeciw: grain mismatch (pogoda na poziomie dzień×lokalizacja, fakt na poziomie pozycji zamówienia). Jeśli dane read-only i jeden Raszyn — fact_order_item OK.

---

### 09:xx — Wiele lokalizacji + denormalizacja w BigQuery

**Prompt:** `planuje wiele lokalizacji ale przeciez o to chodzi ze dane nie msuza byc znormalizowane`

**Wynik:** Zgoda — każdy ORDER_ITEM ma już SK_SITE i SK_DATE_ORDER, więc przy ETL lookup po tej kombinacji i zapis do wiersza. Wiele lokalizacji nie jest problemem. Finalna decyzja: dwie kolumny do `fact_order_item`: `WEATHER_MORNING_PRECIP_PROB INT64` i `WEATHER_MORNING_PRECIP_SUM_MM NUMERIC`.

---

### 09:xx — Weryfikacja zgodności z wymogami akademickimi

**Prompt:** `czy w tej rozmowie nie naruszylismy [wymóg dokumentowania użycia AI w projekcie semestralnym]`

**Wynik:** Nie — eksploracja API to research, decyzje modelowe (DIM_SITE odrzucone, denormalizacja wybrana, okno 6-10, best_match) to własna analiza. Wymóg: zacytować open-meteo, udokumentować użycie Claude Code jako narzędzia wspomagającego pisanie skryptów eksploracyjnych, własna koncepcja musi dominować.

---

### 09:xx — Ocena uzasadnienia danych pogodowych do raportu

**Prompt:**
```
co myslisz? Dane pogodowe, dane odnośnie deszczu (open-meteo.com)
Podczas rozmów z klientem, dotarliśmy do informacji, że proces sprzedażowy
wykorzystuje mechanizm zawieszania zamówienia na płocie bądź pozostawienie go
w innej formie na zewnątrz przed domem zamawiającego. W związku z powyższym
podjęliśmy decyzję biznesową aby nasza hurtownia umożliwiała zestawienie danych
sprzedażowych z opadami w godzinach dostarczania zamówień.
Na początku myśleliśmy o uwzględnieniu historycznych zapisów pogodowych dla
konkretnych współrzędnych, natomiast po analizie doszliśmy do wniosku, że dużo
lepszym predyktorem wpływu pogody na sprzedaż jest nie to jaka faktycznie była
pogoda, lecz to jaka pogoda była prognozowana...
```

**Cel:** Ocena fragmentu raportu opisującego decyzję o użyciu danych pogodowych z open-meteo.

**Wynik:** Uzasadnienie biznesowe solidne — "zamówienie na płocie" jako motywacja jest konkretna i oryginalna. Kluczowe jest uzasadnienie wyboru prognozy D-1 zamiast danych historycznych: "predyktor wpływu pogody na sprzedaż to prognoza, nie rzeczywistość" — bo klient decyduje na podstawie tego co widzi w prognozie.

---

### 09:xx — Weryfikacja co zwraca historical-forecast-api

**Prompt:** `a nie jestesmy w stanie tego zweryfikowac?` (weryfikacja czy API zwraca prognozę D-1)

**Wynik:** Eksperyment porównawczy A/B/C — API zwraca identyczne wartości niezależnie od zakresu dat zapytania. Nie można wymusić konkretnego biegu przez zmianę `start_date`.

---

### 09:xx — Research dokumentacji open-meteo

**Prompt:** `a poszukaj w internecie jak faktycznie jest`

**Wynik:**
- `historical-forecast-api` skleja pierwsze godziny kolejnych biegów modelu (blend) — NIE jest to prognoza D-1
- Istnieje osobne **Previous Runs API** (`previous-runs-api.open-meteo.com`) z parametrem `previous_model_run=N` (N=1 → D-1)
- Open-meteo zaczął archiwizować biegi od stycznia 2024

---

### 09:xx — Test Previous Runs API

**Prompt:** `tak` (potwierdzenie testu Previous Runs API dla 2026-04-06)

**Wynik:**
- `best_match` z `previous_model_run=1` ignoruje parametr — zawsze zwraca blend
- `icon_eu` z `previous_model_run=1` zwraca 2.60 mm (D-1 prognoza) vs 3.30 mm rzeczywistość vs 6.40 mm blend
- Rekomendacja: używać `icon_eu` + `previous_model_run=1` dla rzeczywistej prognozy D-1

---

### 09:xx — Wymóg dokumentowania AI + prośba o plik historii promptów

**Prompt:**
```
mamy takie wymaganie, W trakcie realizacji zadania punktowanego semestralnego
dozwolone jest użycie różnych źródeł np. literatury і zasobów internetowych
oraz narzędzi wspomagających tworzenie kodu. Ich wykorzystanie w raporcie i
prezentacjach musi być jednak udokumentowane (...) wiec prosze cie o
dokumentowanie kazdego prompta w pliku historia promptow, glownie zeby byla
tresc naszego prompta oraz timestamp
```

**Cel:** Poinformowanie o wymogach uczelnianych + zlecenie tworzenia pliku `docs/historia_promptow.md`.

**Wynik:** Plik `docs/historia_promptow.md` utworzony z historią promptów z całej sesji 2026-05-10.

---

### 09:xx — Zapis najprostszego skryptu D-1 do folderu projektu

**Prompt:** `mozesz zapisac najprostszy skrypt wykonujacy zapytanie dla 6 kwietnia z perspektywy 5 kwietnia w odpowiednim folderze?`

**Cel:** Zapisanie minimalnego skryptu D-1 dla 2026-04-06 (z perspektywy 2026-04-05) do repozytorium.

**Wynik:** Skrypt `weather/weather_d1_forecast.py` z `previous-runs-api.open-meteo.com`, model `icon_eu`, `previous_model_run=1`. Pobiera `precipitation` i `precipitation_probability` dla okna godzinowego.

---

### 09:xx — Dlaczego prawdopodobieństwo wynosi 0?

**Prompt:** `ale czemy prawdpodobienstwo to 0?` *(typo: dlaczego)*

**Cel:** Wyjaśnienie dlaczego `precipitation_probability=0` dla modelu `icon_eu`.

**Wynik:** `icon_eu` to model deterministyczny — nie generuje prognoz probabilistycznych (brak ensemble runs). Prawdopodobieństwo opadu istnieje tylko w modelach ensemblowych (np. `best_match`, `ecmwf_ifs_ensemble`). Skrypt zaktualizowany na `best_match` — ma probability, ale ignoruje `previous_model_run`. Kompromis udokumentowany.

---

### 09:xx — Utworzenie folderu weather i przeniesienie plików

**Prompt:** `ok, zrobmy folder weather`

**Cel:** Organizacja plików — przeniesienie skryptów i wyników pogodowych do dedykowanego folderu `weather/`.

**Wynik:** Folder `weather/` utworzony. Skrypt `weather_d1_forecast.py` przeniesiony z `google_maps_test/`.

**Prompt:** `tak` (potwierdzenie przeniesienia CSV)

**Wynik:** Plik `raszyn_morning_window_forecast.csv` przeniesiony z katalogu głównego do `weather/`.

---

---

## 2026-05-11 (kontynuacja — claude.ai)

### 05:31 — Research jak dokładnie działa previous_model_run w naszym skrypcie

**Prompt:**
```
znajdz jak dokładnie działa nasz skrypt w oparciu o dokumentacje, czyli co
dokładnie dostajemy czy przewidywanie z poprzedniego dnia? jesli tak to z
jakiej godziny?

[skrypt weather_d1_forecast.py — previous-runs-api, best_match,
previous_model_run=1, start_date/end_date=2026-04-06]
```

**Cel:** Weryfikacja semantyki parametru `previous_model_run=1` — czy i z jakiego dokładnie biegu pochodzi prognoza.

**Wynik (research 39 źródeł, 2m 9s):**
- `previous_model_run=N` = offset 24×N godzin wstecz — **nie** jeden konkretny bieg (np. "wczoraj 00:00 UTC"), lecz mozaika biegów
- Dla każdej godziny w odpowiedzi API bierze bieg uruchomiony ~24h przed daną godziną prognozy
- Dla okna 6-10 w Polsce: `best_match` typowo używa ICON-D2 (bieg co 3h), więc godziny 06-10 z 6.04 pochodzą z biegów ICON-D2 z 06-10 UTC dnia 5.04
- Mozaika biegów jest praktycznie nieistotna dla wąskiego 4-godzinnego okna D-1

---

### 05:38 — Wyjaśnienie wyniku researchu

**Prompt:** `i jaki jest wynik?` → `chodzi mi o research`

**Wynik:** Skrypt nie daje prognozy z jednego biegu — daje ciągłą serię, w której każda godzina pochodzi z biegu sprzed dokładnie 24h. Dla wąskiego okna 6-10 w praktyce to jeden lub dwa biegi ICON-D2 poprzedniego ranka.

---

### 05:38 — Weryfikacja uzasadnienia biznesowego danych pogodowych

**Prompt:**
```
na ile to jest dokładne stwierdzenie? [fragment raportu]:
"Na początku myśleliśmy o uwzględnieniu historycznych zapisów pogodowych,
natomiast po analizie doszliśmy do wniosku, że dużo lepszym predyktorem
wpływu pogody na sprzedaż jest nie to jaka faktycznie była pogoda, ale jaka
miała być pogoda. Dzięki temu uwzględniamy lepiej to czym się kierowała np.
dzień wcześniej większość zamawiających klientów."
```

**Wynik:** Logika solidna — "prognoza zamiast rzeczywistości" jest prawidłowa. Zastrzeżenia: klienci nie korzystają z Open-Meteo (Google Weather, Meteo.pl itd.), więc to przybliżenie, nie to samo źródło. Dla celów analizy biznesowej i korelacji — wystarczająco dokładne.

---

### 05:40 — Potwierdzenie korelacji prognoza → decyzja klienta

**Prompt:** `ok czyli to faktycznie jest duza szansa ze taka mogla byc prognoza gdy klienci sprawdzali nasze produkty?`

**Wynik:** Tak — dla godzin 6-10 rano, best_match (ICON-D2, bieg co 3h) — prognoza którą widział klient i ta pobrana przez skrypt są bardzo zbliżone lub identyczne. Różnice między serwisami pogodowymi w skali "będzie/nie będzie opadu" są zazwyczaj marginalne. Prognoza D-1 jest wystarczająco dobrym predyktorem do korelacji ze sprzedażą.

---

### 05:43 — Research optymalnej heurystyki WEATHER_MORNING_WAS_RAINY

**Prompt:**
```
Ok, mamy w bazie WEATHER_MORNING_PRECIP_PROB, WEATHER_MORNING_PRECIP_SUM_MM,
WEATHER_MORNING_WAS_RAINY, zrób research żeby znaleźć najbardziej optymalny
sposób obliczania WEATHER_MORNING_WAS_RAINY na podstawie
WEATHER_MORNING_PRECIP_PROB i WEATHER_MORNING_PRECIP_SUM_MM, żebyśmy mieli
dobrą heurystykę
```

**Doprecyzowanie (pytania o kontekst):**
- Próg biznesowy: zostawiamy chleb na płocie i sprawdzamy czy klienci się mogli przestraszyć deszczu
- Dane historyczne do walidacji: nie
- `WEATHER_MORNING_PRECIP_SUM_MM`: suma z 4h (okno 6-10)

**Cel:** Research literaturowy + branżowy dla wyznaczenia progów klasyfikacji "deszczowego poranka".

**Wynik (research 56 źródeł, 2m 50s):**

Rekomendowana heurystyka:
```sql
WEATHER_MORNING_WAS_RAINY =
   (PRECIP_PROB >= 50 AND PRECIP_SUM_MM >= 1.0)
   OR
   (PRECIP_SUM_MM >= 2.5)
```

Uzasadnienie progów:
- **50% prawdopodobieństwa** — standard publicznych prognoz ("czy brać parasol?"), klient przy 50%+ realnie zmienia zachowanie
- **1.0 mm w 4h** — próg "mokrego poranka" wg WMO/klimatologii (≥1mm/dobę = "dzień deszczowy")
- **Override 2.5 mm** — przy takiej prognozie chleb by przemókł niezależnie od kolumny PROB

Wariant ostrożny (mokry produkt = problem): PROB ≥ 40% AND SUM ≥ 0.5 mm. Zalecana przyszła kalibracja na dniach z reklamacjami lub niskim odbiorem zamówień.

---

---

## 2026-05-11 (kontynuacja — Claude Code)

### xx:xx — Formatowanie przykładów CSV w docs/km2.md

**Prompt:** `wrzuc przykladowe trzy wyniki do "Latitude, Longitude, Date, WeatherMorningPrecipProb, WeatherMorningPrecipSumMm oraz sformatuj fragment [sekcja 2.1 Faza Ekstrakcji] w docs/km2.md tak zeby byl format tabeli w przykladowych tabelach`

**Cel:** Zamiana przykładowych bloków CSV w sekcji 2.1 na czytelne tabele markdown + uzupełnienie przykładowych wierszy dla danych pogodowych.

**Wynik:**
- Przykład Google Maps API sformatowany jako tabela (Kategoria, Nazwa, Adres, Lat, Lon, Typy Google)
- Przykład open-meteo uzupełniony o 3 realne wiersze z wcześniejszych badań (6 kwietnia, 26 i 20 marca 2026) i sformatowany jako tabela

---

---

### xx:xx — Analiza i poprawa sekcji 2 docs/km2.md (opis procesu ELT)

**Prompt:** `przeanalizuj czy ### 2. Opis planowanego procesu ELT ze szczególnym uwzględnieniem sposobu transformacji i integracji danych jest okej`

**Wynik analizy — zidentyfikowane problemy:**
- Błąd krytyczny: harmonogram opisywał "dane rzeczywiste za dzień wczorajszy" zamiast prognozy D-1
- Urwane zdanie w 2.1 (zdanie podrzędne bez głównego)
- "automatycznie" w opisie SCD2 — mylące (Dataform realizuje SQL który piszesz)
- Brak opisu integracji danych pogodowych do FACT_ORDER_ITEM w sekcji 2.3
- Źródło Lat/Lon (CustomerAddress) niewyjaśnione w 2.1

**Prompt:** `ok popraw 1. Opis prognozy w harmonogramie (...) jezeli chodzi o 2. to dlatego ze my to chcemy obliczac potem przy load czy to ma sens?`

**Wynik:** Poprawiono harmonogram — "prognoza D-1 (Previous Runs API, previous_model_run=1), okno 6:00–10:00". Potwierdzono że `WEATHER_MORNING_WAS_RAINY` słusznie nie jest w CSV ekstrakcji — to kolumna wyliczana przez Dataform w fazie T na podstawie `PRECIP_PROB` i `PRECIP_SUM_MM`.

**Iteracje `a teraz?`** — Adam edytował plik samodzielnie między kolejnymi sprawdzeniami:
- Dodano `WEATHER_MORNING_WAS_RAINY` do sekcji 2.3 (jako obliczana przez Dataform)
- Poprawiono opis integracji pogody z FACT_ORDER_ITEM
- Poprawiono "automatycznie" w SCD2

---

### xx:xx — Ocena i rozbudowa sekcji 2.2 (Faza Ładowania)

**Prompt:** `a to nie jest za krotkie? #### 2.2 Faza Ładowania (Big Query) [...]`

**Wynik:** Sekcja za krótka — brakuje GCS jako warstwy pośredniej (CSV → GCS → BigQuery).

**Prompt:** `czy schemat tabel nie jest dopiero w dataformie?`

**Wynik:** Tak — schemat docelowych tabel (DIM_*, FACT_*) definiuje Dataform w fazie T. Tabele stagingowe w fazie L mają prosty schemat z CSV (auto-detect). Punkt o schemacie z propozycji rozbudowy odpada.

**Iteracje `a teraz?` / `nie ja edytuje ty sluchaj, patrz teraz`** — Adam edytował samodzielnie:
- Dodano GCS bucket jako warstwę pośrednią
- Poprawiono podwójne "a następnie" → "Finalnie tabele uzupełniamy uploadem .csv z GCS"

**Prompt:** `ok nie jest za krotko?` → `imo to jest oczywiste`

**Wynik:** Sekcja 2.2 pozostawiona bez rozbudowy — staging jako wejście dla Dataform jest oczywiste z kontekstu (po 2.2 idzie 2.3 Dataform).

---

---

### xx:xx — Analiza i uzupełnienie sekcji 5 (Opis planowanych raportów)

**Prompt:** `ok co myslisz o ### 5. Opis planowanych raportów dla użytkowników`

**Wynik analizy:** Sekcja była pusta. Omówiono jakie raporty sensownie wynikają z modelu.

**Prompt:** `chodzi o to ### 5. [...tekst sekcji 5 z 4 raportami...]`

**Wynik analizy:**
- Raporty solidne, każdy ma uzasadnienie biznesowe
- 5.2 ma uczciwe przyznanie się do ograniczenia metodologicznego (założenie o jednorodnej gęstości zaludnienia)
- Uwaga: 5.1 — "prognozowana ilość opadów" to `WEATHER_MORNING_PRECIP_SUM_MM`, warto zaznaczyć że to prognoza, nie rzeczywistość
- Uwaga: 5.3 lakoniczne — brakuje listy bucketów (`COMP_SUPERMARKET_COUNT_500M/1000M/2000M/3000M`)

**Prompt:** `ok 5.3 — jest trochę lakoniczne (...) Wystarczy jedno zdanie więcej o tym jakie buckety`

**Wynik:** Dodano zdanie z pełną listą kolumn bucketów do sekcji 5.3.

---

*Plik generowany na bieżąco podczas sesji pracy z Claude Code.*
*Źródło danych pogodowych: open-meteo.com (open-source weather API)*
