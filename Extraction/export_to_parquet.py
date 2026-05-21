import os
import sys
import pandas as pd
from sqlalchemy import create_engine, inspect

# Dane połączenia z bazą PostgreSQL (Docker)
DB_USER = "admin"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Lista 8 operacyjnych baz danych zdefiniowanych w Twoim systemie
DATABASES = [
    "catalog-db",
    "claim-manager-db",
    "client-manager-db",
    "customer-manager-db",
    "delivery-account-manager-db",
    "delivery-manager-db",
    "planner-db",
    "wallet-db"
]

# Ścieżka docelowa dla wyekstrahowanych danych - folder 'data' wewnątrz bieżącego folderu 'Extraction'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(CURRENT_DIR, "data")

def export_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Rozpoczynanie eksportu baz danych do formatu Parquet w wydzielonym katalogu: {OUTPUT_DIR}")
    
    for db_name in DATABASES:
        print(f"\n========================================")
        print(f" Łączenie z bazą: {db_name}")
        print(f"========================================")
        
        # PostgreSQL connection string
        conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db_name}"
        
        try:
            engine = create_engine(conn_str)
            inspector = inspect(engine)
            
            # Pobierz nazwy wszystkich tabel w schemacie public
            tables = inspector.get_table_names(schema="public")
            
            if not tables:
                print(f" [INFO] Brak tabel w schemacie 'public' dla bazy: {db_name}")
                continue
                
            # Tabela wykluczeń ze względów bezpieczeństwa i braku przydatności analitycznej
            EXCLUDED_TABLES = {
                "DataProtectionKeys",
                "__EFMigrationsHistory",
                "CustomerAndroidToken",
                "DeliveryManAndroidToken"
            }
            
            # Stworzenie dedykowanego podfolderu dla konkretnej bazy danych
            db_dir = os.path.join(OUTPUT_DIR, db_name)
            os.makedirs(db_dir, exist_ok=True)
            
            for table in tables:
                if table in EXCLUDED_TABLES:
                    print(f"  -> Pomijanie tabeli (bezpieczeństwo/brak przydatności): {table}")
                    continue
                print(f"  -> Eksportowanie tabeli: {table} ... ", end="")
                try:
                    # Wczytanie tabeli do ramki danych Pandas
                    df = pd.read_sql_table(table, engine, schema="public")
                    
                    # Ścieżka docelowa dla pliku Parquet
                    parquet_file = os.path.join(db_dir, f"{table}.parquet")
                    
                    # Zapis do Parquet z użyciem silnika pyarrow
                    df.to_parquet(parquet_file, index=False, engine="pyarrow")
                    print(f"SUKCES ({len(df)} wierszy -> data/{db_name}/{table}.parquet)")
                except Exception as e:
                    print(f"BŁĄD (Szczegóły: {e})")
                    
        except Exception as e:
            print(f" [BŁĄD] Nie można połączyć się z bazą {db_name}. Szczegóły: {e}")
            
    print("\n========================================")
    print(" Eksport zakończony sukcesem!")
    print(f" Wyekstrahowane pliki danych znajdziesz w: {OUTPUT_DIR}")
    print("========================================")

if __name__ == "__main__":
    # Sprawdzenie zależności
    missing_deps = []
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    try:
        import sqlalchemy
    except ImportError:
        missing_deps.append("sqlalchemy")
    try:
        import pyarrow
    except ImportError:
        missing_deps.append("pyarrow")
    try:
        import psycopg2
    except ImportError:
        missing_deps.append("psycopg2-binary")
        
    if missing_deps:
        print(f"Brakujące biblioteki Pythona: {', '.join(missing_deps)}")
        print("Uruchom w konsoli (najlepiej w swoim venv):")
        print(f"  pip install {' '.join(missing_deps)}")
        sys.exit(1)
        
    export_all()
