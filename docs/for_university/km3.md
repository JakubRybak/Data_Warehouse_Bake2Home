### 0. Dashboardy z naszej hurtowni
Dashboardy z naszej hurtowni można obejrzeć pod poniższym linkiem:
https://datastudio.google.com/reporting/46e778d6-111d-4d84-b31a-bccd57b78bea

### 1. Rozszerzony opis wykorzystywanych zbiorów danych
Dane o punktach POI (Google Maps API) Dane o konkurencji i punktach użyteczności publicznej pozyskujemy z Google Maps API (New). Choć dane te są dostępne "na żądanie" w czasie rzeczywistym, nasza architektura stawia na rygorystyczną minimalizację liczby zapytań w celu optymalizacji kosztów. Wykorzystujemy zapytania zdefiniowane przestrzennie, na które nakładamy ścisłe filtry kategorii (np. tylko piekarnie i supermarkety) oraz maski pól (FieldMask), dzięki czemu pobieramy wyłącznie niezbędne atrybuty (nazwa, adres, współrzędne GPS). Należy mieć na uwadze ograniczenie samego API, które dla zapytania przestrzennego zwraca maksymalnie 20 wyników.

Dane pogodowe, dane odnośnie deszczu (open-meteo.com) Podczas rozmów z klientem, dotarliśmy do informacji, że proces sprzedażowy wykorzystuje mechanizm zawieszania zamówienia na płocie bądź pozostawienie go w innej formie na zewnątrz przed domem zamawiającego. W związku z powyższym podjęliśmy decyzję biznesową aby nasza hurtownia umożliwiała zestawienie danych sprzedażowych z opadami w godzinach dostarczania zamówień.

Na początku myśleliśmy o uwzględnieniu historycznych zapisów pogodowych dla konkretnych współrzędnych, natomiast po analizie doszliśmy do wniosku, że dużo lepszym predyktorem wpływu pogody na sprzedaż jest nie to jaka faktycznie była pogoda, ale jaka miała być pogoda. Dzięki temu uwzględniamy lepiej to czym się kierowała np. dzień wcześniej większość zamawiających klientów. Dlatego pobierając dane pobieramy informacje na temat prognoz w godzinach 6-10 rano. Zbieramy takie dane jak maksymalne prawdopodobieństwo opadów w tych godzinach, oraz sumę opadów z tych godzin w milimetrach.
  
### 2. Opis planowanego procesu ELT ze szczególnym uwzględnieniem sposobu transformacji i integracji danych
#### 2.1 Faza Ekstrakcji

Ekstrakcja następuje z trzech źródeł: baza bake2home, google maps api, oraz open-meteo. 

Najpierw sprawdzamy datę ostatniego eksportu i eksportujemy nowe rekordy z każdej tabeli z każdej bazy jako osobne csv.

Zauważmy, że dane z open-meteo oraz google maps api są ściśle powiązane z szerokością i długością geograficzną danych z bake2home. Dlatego w celu optymalnego wykorzystania api najpierw musimy wyeksportować w csv wynik zapytania do bazy bake2home, gdzie prosimy o wszystkie nowe szerokości i długości geograficzne oraz daty, tak żeby wiedzieć dla jakich parametrów ściągać dane z google maps api, oraz open meteo do późniejszej fazy transformacji. Aby to zrobić należy z bazy delivery-manager-db, z tabeli Deliveries należy wziąć int OrderId, i zrobić joina po OrderId z tabelą Bakery Orders z bazy planner-db, tak aby mieć listę deliveries z Date, oraz Latitude oraz Longitude odpowiadającą danym z tabeli FactOrderItem. Następnie na podstawie listy Latitude i Longitude ściągnąć dane z Google Maps API z współrzędnymi wszystkich punktów w okolicy oraz zapisać do pliku CSV:

| Kategoria | Nazwa | Adres | Szerokość (Lat) | Długość (Lon) | Typy Google |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Piekarnia/Cukiernia | Kołacz na Okrągło Auchan Okęcie | Aleja Krakowska 61, 02-285 Warszawa | 52.1711992 | 20.9346711 | bakery, food_store, food, point_of_interest, store, establishment |
| Supermarket | Biedronka | Sportowa 1, 05-090 Raszyn | 52.1536184 | 20.9217322 | discount_supermarket, supermarket, grocery_store, food_store, food, store, establishment |
| Supermarket | Delikatesy Centrum | Pruszkowska 52, 05-090 Raszyn | 52.1612933 | 20.9147626 | grocery_store, supermarket, deli, food_store, food, store, point_of_interest, establishment |

Jezeli chodzi o dane z open-meteo to zdecydowaliśmy się na ustawianie ich domyślnie na -1 -ki a następnie codziennie o północy przy użyciu Cloud Schedulera oraz Cloud run functions doładowywać brakujące dane w sposób automatyczny. Skrypt dla każdego zamówienia doładowuje pogodę.

#### 2.2 Faza Ładowania (Big Query)

Wrzucamy wszystkie pliki .csv do bucketu Google Cloud Storage, a następnie tworzymy tabele w bigquery odpowiadające wyeksportowanym wcześniej plikom .csv, oraz dwóm plikom z danymi z google maps, oraz z danymi opadowymi. Finalnie tabele uzupełniamy uploadem .csv z GCS.

#### 2.3 Proces ELT – Faza Transformacji (Google Cloud Dataform)

Transformacja danych surowych w docelowy model wielowymiarowy (Star Schema) odbywa się bezpośrednio w silniku BigQuery za pomocą narzędzia Google Cloud Dataform. Proces obejmuje trzy kluczowe operacje:

Generowanie Kluczy Zastępczych (Surrogate Keys): Dataform generuje unikalne klucze SK_ (typu INT64) dla każdego rekordu wymiaru, wykorzystując natywne funkcje hashujące BigQuery (np. FARM_FINGERPRINT). Uniezależnia to hurtownię od zmian identyfikatorów w systemach źródłowych i zapewnia integralność referencyjną między faktami a wymiarami.

Implementacja Historyzacji (SCD2): Dataform automatycznie zarządza wymiarami wolnozmiennymi Typu 2. W przypadku wykrycia zmiany w atrybutach wymiaru (np. zmiana adresu klienta), stary rekord zostaje "wygaszony" (aktualizacja IS_CURRENT i VALID_TO), a nowy wstawiany z aktualną datą VALID_FROM. Gwarantuje to pełną spójność danych historycznych bez konieczności pisania skomplikowanych zapytań MERGE.

Integracja Wieloźródłowa (Cross-Source Joins & Spatial Analytics): Wewnętrzne dane operacyjne (np. adresy klientów z bazy Bake2Home) są łączone za pomocą Spatial Joinów z zewnętrznymi danymi z Google Maps API (tabela DIM_COMPETITORS). Wykorzystując funkcje GIS (np. ST_DISTANCE), Dataform przelicza zdenormalizowane metryki odległościowe, które trafiają bezpośrednio jako atrybuty analityczne do tabeli DIM_CUSTOMER. Dzięki danym z meteo API dataform przelicza również informację czy zamówienie było dostarczane w deszczowy dzień, informacja ta trafia do tabeli FACT_ORDER_ITEM.

Harmonogram Odświeżania Danych (Data Refresh Strategy)

Procesy ładujące i transformujące są orkiestrowane z różną częstotliwością, aby zapewnić optymalny balans między świeżością danych a kosztami operacyjnymi:

Dane operacyjne (Bake2Home DB): Codziennie w nocy (Daily Nightly Batch). Klasyczny widok "T-1" na wczorajsze zamknięcie dnia, bez obciążania systemów produkcyjnych w godzinach szczytu.

Dane pogodowe: Codziennie około północy. Pobieramy prognozę D-1 - czyli to, co modele pogodowe prognozowały wczoraj na dzisiaj (Previous Runs API, parametr previous_model_run=1). Interesuje nas okno godzinowe 6:00–10:00 dla każdej lokalizacji dostawy.

Dane o konkurencji i POI (Google Maps API): Raz w miesiącu (Monthly). Cykl otwierania i zamykania fizycznych punktów sprzedaży charakteryzuje się niską dynamiką. Miesięczne odświeżanie gwarantuje miarodajny obraz otoczenia rynkowego przy minimalnych kosztach płatnych zapytań API.

### 3. Model fizyczny hurtowni danych przygotowany w dowolnym narzędziu do projektowania (uwzględniający tabele, kolumny, typy danych, wymagalność i relacje)

![Model fizyczny hurtowni danych Bake2Home](Constelation_main.svg)

  
### 4. Opis kluczowych miar i atrybutów w modelu
#### 4.1 Measures and Aggregation Methods

##### FACT_ORDER_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `PRICE` | Value/Price for a given product/offer | **SUM** (Revenue), **AVG** (Average price) |
| `QUANTITY` | Quantity of ordered items | **SUM** |
| `VAT` | VAT tax amount | **SUM** |
| `DISCOUNT_PERCENT` | Applied discount in percentage | **AVG**, **MAX** |
| `WEATHER_MORNING_WAS_RAINY` | (`PRECIP_PROB` >= 50 AND `PRECIP_SUM_MM` >= 1.0) OR (`PRECIP_SUM_MM` >= 2.5) | **CUSTOM** |

##### FACT_DELIVERY_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `PLANNED_QUANTITY` | Quantity planned for delivery | **SUM** |
| `PACKED_QUANTITY` | Quantity actually packed | **SUM** |
| `PRODUCT_PRICE` | Value of the product in delivery | **SUM** |

##### FACT_CLAIM_ITEM
Zrezygnowaliśmy z implementacji tej faktówki! :(

##### FACT_PAYMENT & FACT_REFUND_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `AMOUNT` (PAYMENT) | Booked payment amount | **SUM** |
| `AMOUNT` (REFUND) | Actual refund amount (net/gross) | **SUM** |
| `VAT_AMOUNT` | Refunded VAT amount | **SUM** |
| `MISSING_PRODUCT_QUANTITY` | Quantity of missing products forming the basis of the refund | **SUM** |

##### FACT_PLANNER_ITEM
| Measure | Business Description | Default Aggregation |
| :--- | :--- | :--- |
| `QUANTITY` | Number of items in the subscription plan | **SUM** |
| `DURATION_DAYS` | Duration of the plan / cycle | **AVG**, **MAX** |

---

#### 4.2 Key Attributes

##### Spatial and Logistics Attributes (GIS)
**Tables:** `DIM_SITE`, `DIM_CUSTOMER_ADDRESS`, `DIM_COMPETITORS`
* **Categorizing:** `CITY`, `ZIPCODE`, `STATE`, `COUNTRY`, `STREET`.
* **GIS (Coordinates):** `LATITUDE`, `LONGITUDE`, **`GEO_POINT`**.
* **Reach Indicators in `DIM_CUSTOMER`:** 
  * `DIST_TO_NEAREST_OWN_SITE_M`, `DIST_TO_NEAREST_COMP_BAKERY_M`
  * `COMP_BAKERY_COUNT_500M`, `OWN_SITE_COUNT_1000M`

##### Product and Marketing Attributes
**Tables:** `DIM_PRODUCT`, `DIM_OFFER`, `DIM_DISCOUNT`, `DIM_INGREDIENT`
* **Categorizing:** `PRODUCT_TYPE_NAME`, `TYPE` (in offer), `CATEGORY` (Competitors).
* **Technical/Nutritional:** `CALORIES`, `TOTAL_FATS`, `SUGAR`.
* **Promotional:** `DISCOUNT_CODE`, `ONLY_FOR_FIRST_PURCHASE`.

##### Status Attributes
* **In orders:** `ORDER_ITEM_STATE`, `ORDER_STATE`, `MODIFIED_BY_HAND`.
* **In payments:** `TYPE`, `CARD_BRAND`, `MOBILE`.
* **In claims:** `STATE`, `ISSUE_TYPE`.

---

#### 4.3 Analytical Hierarchies

##### A. Time Hierarchy (`DIM_DATE`)
1. `YEAR`
2. `QUARTER`
3. `MONTH_NAME` / `MONTH_NUMBER`
4. `WEEKDAY_NAME` / `WEEKDAY_NUMBER`
5. `SK_DATE`

##### B. Geographical Hierarchy
1. `COUNTRY`
2. `STATE`
3. `CITY`
4. `ZIPCODE`
5. `STREET` / `ADDRESS`

##### C. Operational-Management Hierarchy
1. `DIM_LOCATION`
2. `DIM_SITE`
*(Note: `DIM_DELIVERY_MAN` and `DIM_CUSTOMER` are independent dimensions. They are linked to a specific site dynamically per transaction via Fact tables, because a customer can order from multiple sites.)*

##### D. Product-Offer Hierarchy
1. `DIM_OFFER`
2. `DIM_PRODUCT`
3. `DIM_INGREDIENT` / `DIM_ALLERGEN`
*(Note: These relationships are Many-to-Many (N:M) resolved via Bridge tables like `BRIDGE_OFFER_PRODUCT`, meaning a single product can belong to multiple offers, and an ingredient to multiple products.)*


### 5. Opis planowanych raportów dla użytkowników
Podczas rozmowy z klientem o jego potrzebach doszliśmy do wniosku, że klient jest zainteresowany informacjami o rentowności obszarów, oraz o częstotliwościach zakupów przez klientów. Natomiast niestety klient zidentyfikował zdefniowanie rentowności jako problematyczne. Dlatego skorzystamy z prostszych rozwiązań i będziemy mierzyć rentowność wartościami zamówień.

#### 5.1 Raport pokazujący wpływ pogody na wartość zamówień
Dlaczego? Chcemy sprawdzić czy aktualna forma dostawy nie stanowi bariery zniechęcającej do zakupu.
Jak? 
Pokażemy wykres porównujący średnie przychody w deszczowe oraz niedeszczowe dni w kolejnych miesiącach, oraz dwa wykresy punktowe: wykres prognozowanej ilości opadów, oraz wykres punktowy połączonym linią wartości zamówień. Wykres z możliwością regulacji daty.

#### 5.2 Raport pokazujący wpływ ilości piekarni w okolicy na wartość zamówień
Dlaczego? Chcemy sprawdzić jak dużą konkurencją są stacjonarne piekarnie.
Jak?
Jest to dosyć trudne zadanie ponieważ dane mogą być skorelowane ale nie być ze sobą związane, np. licząc po łącznej wartości zamówień i odległości od piekarni może nam wyjść korelacja ale może ona być związana z tym, że na obrzeżach mieszka mniej ludzi więc jest mniej piekarni oraz mniej wartości. Natomiast nie ma tutaj zbyt dobrego wyjścia bo ciężko zmierzyć brak zamówień jakimikolwiek średnimi, więc mimo wszystko założymy jednostajną gęstość zaludnienia, co jest rozsądnym założeniem bo klient zaplanował obszary tak, żeby nie dowozić na odludzia. 

Dlatego pokażemy heat mapę sumy wartości zamówień w podziale na buckety, to jest w pierwszej kolumnie będziemy mieli `COMP_BAKERY_COUNT_300M` dla n = 1, 2, 3-4, 5+, w drugiej `COMP_BAKERY_COUNT_500M` dla tych samych n w trzeciej `COMP_BAKERY_COUNT_1000M` oraz czwartej `COMP_BAKERY_COUNT_2000M`. Dane powinny nieść uniwersalną informację niezależną od czasu i miejsca, więc w miarę napływu danych będziemy ją zawsze obliczać dla wszystkich danych. 

#### 5.3 Raport pokazujacy wpływ ilości supermarketów w okolicy na wartość zamówień
Dlaczego? Chcemy sprawdzić jak dużą konkurencją są supermarkety.
Jak?
Analogicznie do raportu wpływu ilości piekarni ale używając kolumn `COMP_SUPERMARKET_COUNT_500M`, `COMP_SUPERMARKET_COUNT_1000M`, `COMP_SUPERMARKET_COUNT_2000M` oraz `COMP_SUPERMARKET_COUNT_3000M` jako buckety w kolumnach heat mapy.


#### 5.4 Raport pokazujący charakteryzujący regularnych klientów
Dlaczego? Chcemy sprawdzić kto jest naszym klientem, oraz czy warto skupić się w 100% na klientach regularnych zaniedbując okazjonalnych.
Jak?
Pokażemy histogram wartości zamówień z każdej grupy klientów którzy zamawiają w n-dni w tygodniu (7 słupków, o tym jakiego rodzaju jest klient decyduje mediana z liczby dni w których klient zamawiał w tygodniach w których zamawiał). Wykres z możliwością regulacji daty.

---

### 6. Analiza jakości i spójności danych

#### 6.1 Raport Kompletności Danych
* **Cel:** Sprawdzenie jakości danych w systemach źródłowych i wykrycie ewentualnych anomalii w postaci braku wartości w kluczowych polach.
* **Kroki:** Uruchomienie skryptu w Jupyter Notebook łączącego się z `INFORMATION_SCHEMA` BigQuery. Skrypt iteruje po każdej tabeli we wszystkich warstwach (Bronze, Silver, Gold) i zlicza procentowy udział wartości NULL w poszczególnych kolumnach.
* **Oczekiwany wynik:** Otrzymanie czytelnego raportu w formie tabeli pokazującego odsetek braków dla każdej kolumny. Spodziewamy się wysokiej kompletności dla kluczy głównych oraz ewentualnych uzasadnionych biznesowo braków (np. data rozwiązania umowy).
* **Potwierdzenie:** 

  ![Raport Kompletności - Bronze](images/1_bronze.png)
  ![Raport Kompletności - Silver](images/1_silver.png)
  ![Raport Kompletności - Gold](images/1_gold.png)

#### 6.2 Audyt Spójności Ścieżek Danych
* **Cel:** Weryfikacja przepływu encji od surowego pliku na GCS (Bronze) do docelowej tabeli w hurtowni (Gold) pod kątem wycieków i duplikacji.
* **Kroki:** Skrypt zlicza liczbę wierszy dla 16 kluczowych encji kolejno w datasetach `bronze`, `silver` oraz `gold`.
* **Oczekiwany wynik:** Tabela faktów przenosi dokładnie 100% wolumenu na każdej warstwie. Tabele wymiarowe rosną o dokładnie 1 wiersz w warstwie Gold z powodu dodawania technicznego rekordu `-999999` do obsługi braków. Brak jakichkolwiek iloczynów kartezjańskich.
* **Potwierdzenie:** 

  ![Audyt Spójności Ścieżek Danych](images/2.png)

#### 6.3 Raport Odrzutów Biznesowych i Relacji
* **Cel:** Wykrycie braków w integralności referencyjnej oraz zbudowanie profilu biznesowego transakcji (np. jaki odsetek koszyków nie zawiera zniżki).
* **Kroki:** Skanowanie wszystkich tabel faktów oraz tabel pomostowych w warstwie Gold w celu zliczenia wystąpień technicznego klucza zastępczego `-999999` dla każdego klucza obcego.
* **Oczekiwany wynik:** Brak ukrytych sierot technicznych. Zidentyfikowanie naturalnych wyjątków biznesowych (np. płatności bez użycia zniżki) na oczekiwanym poziomie. Potwierdzenie, że hurtownia danych nie łamie zapytań analitycznych z powodu braku klucza w źródle.
* **Potwierdzenie:** 

  ![Raport Odrzutów Biznesowych (Sieroty)](images/3.png)

---

### 7. Testy Akceptacyjne, Funkcjonalne i End-to-End

#### 7.1 Weryfikacja Historyzacji Danych
* **Cel:** Potwierdzenie poprawnego działania mechanizmu Slowly Changing Dimensions Typu 2 w celu zachowania prawdy historycznej.
* **Kroki:** Symulacja zmiany nazwiska klienta w bazie operacyjnej, przetworzenie danych przez Dataform i odpytanie hurtowni zapytaniem SQL dla `id_customer = 1` sortując po dacie aktualizacji.
* **Oczekiwany wynik:** Dwa rekordy dla tego samego klienta: stary ze zgaszoną flagą `is_current = FALSE` (oraz zamkniętą datą `valid_to`) i nowy z flagą `is_current = TRUE` oraz zaktualizowanym nazwiskiem.
* **Potwierdzenie:** 

  ![Raport Odrzutów Biznesowych (Sieroty)](images/4.png)

#### 7.2 Test Filtrowania Przestrzennego
* **Cel:** Weryfikacja poprawności czyszczenia danych konkurencji o własne placówki. Zewnętrzne API (Google Maps) mogłoby zwracać własne piekarnie jako placówki w tej samej okolicy.
* **Kroki:** Skrypt sprawdzający analizuje kartezjańskie złączenie gotowych tabel `dim_site` oraz `dim_competitor` w warstwie Gold z nałożonym warunkiem dystansu GIS (`ST_DISTANCE < 30.0m`).
* **Oczekiwany wynik:** Zwrócona pusta tabela, co bezsprzecznie potwierdza poprawność odrzucenia z bazy konkurencji punktów nakładających się na nasze sklepy.
* **Potwierdzenie:** 

  ![Raport Odrzutów Biznesowych (Sieroty)](images/5.png)

#### 7.3 Potwierdzenie całościowego działania systemu
* **Cel:** Udowodnienie, że nowo pojawiające się zdarzenie biznesowe przepływa poprawnie przez całą architekturę aż do widoku dla użytkownika końcowego.
* **Kroki:** 
  1. Zanotowanie aktualnej wartości sprzedaży na raporcie Looker Studio.
  2. Wgranie do GCS pliku Parquet symulującego gigantyczną transakcję (np. wartość 500 PLN).
  3. Uruchomienie przeliczenia modelu (Dataform).
  4. Odświeżenie raportu końcowego.
* **Oczekiwany wynik:** Wskazania na wykresie/dashboardzie w Looker Studio powinny natychmiast uwzględnić nową transakcję, zwiększając łączną sumę o dokładnie 500 PLN.
* **Potwierdzenie:** 

  ![Raport Odrzutów Biznesowych (Sieroty)](images/6_1.png)

  ![Raport Odrzutów Biznesowych (Sieroty)](images/6_2.png)

---

### 8. Dokumentacja wykorzystania narzędzi AI

W trakcie realizacji projektu korzystaliśmy z narzędzia Claude Code (Anthropic) jako asystenta. Poniżej uczciwa ocena zakresu wykorzystania.

#### Co było własną pracą i koncepcją

- **Decyzja o integracji danych pogodowych** - wynikła bezpośrednio z rozmowy z klientem (mechanizm "zamówienia na płocie"); pomysł i uzasadnienie biznesowe są nasze
- **Wybór prognozy D-1 zamiast danych historycznych** - decyzja analityczna podjęta po zrozumieniu problemu: klient decyduje o zakupie na podstawie prognozy, nie rzeczywistości
- **Wybór okna 6–10 rano** - decyzja biznesowa
- **Decyzja o denormalizacji danych pogodowych do FACT_ORDER_ITEM** - po odrzuceniu przez nas propozycji DIM_SITE daily i BRIDGE_WEATHER_DAILY
- **Koncepcja i uzasadnienie wszystkich czterech raportów** (5.1–5.4), w tym pomysł heat mapy z bucketami i świadome zastrzeżenie metodologiczne dot. jednorodności zaludnienia
- **Architektura ELT** (GCS → BigQuery → Dataform) - decyzja projektowa, korekta z ETL na ELT
- **Tworzenie wykresów w Looker Studio oraz zapytań SQL będących ich źródłami** - implementacja i konfiguracja wizualizacji dla wszystkich raportów

#### Co wykonał Claude

- **Skrypty Python** do eksploracji API open-meteo (testy granulacji ICON-D2, skrypt prognozy porannej, skrypt D-1) oraz pierwsza wersja zwięzłego skryptu fetchującego pogodę zgodna z dokumentacją - kod pisany przez Claude, uruchamiany i weryfikowany przez nas
- **Research dokumentacji open-meteo** - odkrycie że `historical-forecast-api` to blend, nie D-1; znalezienie `previous-runs-api` i parametru `previous_model_run`
- **Naprawa bugów** w skryptach (błędne etykiety godzin w oknie 6–10)
- **Research progów klasyfikacji** `WEATHER_MORNING_WAS_RAINY` na podstawie literatury WMO/NWS (56 źródeł) - progi 50%/1.0mm/2.5mm zaproponowane przez Claude
- **Diagnoza i naprawa błędów SQL i BigQuery** - m.in. brakujące funkcje (`STR`, `INT`, `DATEPART`), obsługa STRUCT w porównaniach, format daty, ograniczenia `CREATE TEMP FUNCTION` w Looker Studio
- **Skrypt Cloud Function** pobierający dane z open-meteo dla rekordów bez pogody i aktualizujący `FACT_ORDER_ITEM` - kod, `requirements.txt`, konfiguracja klienta BigQuery, integracja z Cloud Scheduler
- **Wyjaśnienia konceptualne i architektoniczne** (Scheduled Queries vs Cloud Functions, hierarchie flat/snowflake/bridge, typy miar, SCD2, standardy branżowe przy decyzjach architektonicznych) - Claude tłumaczył, my podejmowaliśmy decyzje
- **Wsparcie implementacyjne** - przyspieszenie pisania kodu (podpowiedzi składni, gotowe fragmenty do adaptacji) oraz nawigacja po interfejsach GCP i Looker Studio (gdzie co kliknąć)
- **Looker Studio** - nauka obsługi narzędzia, podłączenie hurtowni BigQuery jako źródła danych (custom query, parametry `@DS_START_DATE`), pola kalkulowane `CASE WHEN` dla wartości binarnych, diagnoza date range control
- **Edycja i formatowanie tekstu** w `docs/km2.md` - formatowanie tabel CSV, poprawa sekcji 2.1 (urwane zdanie), korekta opisu harmonogramu, dodanie zdania o bucketach w 5.3
- **Wspólne redagowanie dokumentacji** - Claude współtworzył i edytował treść dokumentacji projektowej, w tym niniejszy dokument
- **Pomoc przy google cloud** - przy połapaniu się w moliwościach i UI oraz permisjach na google cloud


##### Co wykonał Jakub

- **Model fizyczny** (model.drawio) i iteracyjne dostosowywanie struktury Star/Constellation Schema
- **Skrypty Google Maps API** (testy, pobieranie danych POI z FieldMask i filtrami kategorii)
- **Cały pipeline Dataform** (bronze/silver/gold): surrogate keys, SCD2, spatial joiny z danymi konkurencji, metryki odległościowe w DIM_CUSTOMER
- **Wszystkie wymiary i tabele faktów** oraz bridge tables, widoki SQL analityczne, null rows
- **Struktura projektu** i organizacja plików, oraz drobna pomoc przy lookerze

#### Co wykonał Adam

- **Prace przygotowawcze i rozmowa z klientem** (wspólnie z Jakubem)
- **Moduł open-meteo**: skrypty Python pobierające prognozy D-1, Cloud Function doładowująca dane pogodowe do FACT_ORDER_ITEM, integracja z Cloud Scheduler
- **Kolumny pogodowe w modelu** i logika klasyfikacji WEATHER_MORNING_WAS_RAINY
- **Warstwa raportowa w Looker Studio**: wszystkie cztery raporty, podłączenie BigQuery, pola kalkulowane, heat mapy, wykresy punktowe, date range control