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

Oraz dla każdej listy unikalnych Latitude, Longitude oraz Date, ściągnąć dane z open-meteo do pliku CSV:

| Latitude | Longitude | Date | WeatherMorningPrecipProb | WeatherMorningPrecipSumMm |
| :--- | :--- | :--- | :--- | :--- |
| 52.1656 | 20.9326 | 2026-04-06 | 72 | 3.30 |
| 52.1656 | 20.9326 | 2026-03-26 | 86 | 2.90 |
| 52.1656 | 20.9326 | 2026-03-20 | 93 | 0.90 |

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

Dane pogodowe: Codziennie nad ranem. Pobieramy prognozę D-1 — czyli to, co modele pogodowe prognozowały wczoraj na dzisiaj (Previous Runs API, parametr previous_model_run=1). Interesuje nas okno godzinowe 6:00–10:00 dla każdej lokalizacji dostawy.

Dane o konkurencji i POI (Google Maps API): Raz w miesiącu (Monthly). Cykl otwierania i zamykania fizycznych punktów sprzedaży charakteryzuje się niską dynamiką. Miesięczne odświeżanie gwarantuje miarodajny obraz otoczenia rynkowego przy minimalnych kosztach płatnych zapytań API.

### 3. Model fizyczny hurtowni danych przygotowany w dowolnym narzędziu do projektowania (uwzględniający tabele, kolumny, typy danych, wymagalność i relacje)
TODO przekleić
  
### 4. Opis kluczowych miar i atrybutów w modelu
TODO przekleić

### 5. Opis planowanych raportów dla użytkowników
Podczas rozmowy z klientem o jego potrzebach doszliśmy do wniosku, że klient jest zainteresowany informacjami o rentowności obszarów, oraz o częstotliwościach zakupów przez klientów. Natomiast niestety klient zidentyfikował zdefniowanie rentowności jako problematyczne. Dlatego skorzystamy z prostszych rozwiązań i będziemy mierzyć rentowność wartościami zamówień.

#### 5.1 Raport pokazujący wpływ pogody na wartość zamówień
Dlaczego? Chcemy sprawdzić czy aktualna forma dostawy nie stanowi bariery zniechęcającej do zakupu.
Jak? 
Pokażemy wykresy porównujące średnie przychody w deszczowe oraz niedeszczowe dni w kolejnych miesiącach.
Słupkowy wykres prognozowanej ilości opadów, z naniesionym wykresem punktowym połączonym linią wartości zamówień z oznaczeniem dni deszczowych. Wykres w ujęciu miesięcznym.

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
Pokażemy histogram ilu jest klientów którzy zamawiają w n-dni w tygodniu (7 słupków) oraz histogram wartości zamówień z każdej grupy, dla różnych miesięcy. Dwa histogramy co miesiąc.