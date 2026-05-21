import os

# Konfiguracja Twojego projektu i kubełka GCP
PROJECT_ID = "bake2home-data-warehouse"
BUCKET_NAME = "bake2home-raw-data"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")
OUTPUT_SQL_FILE = os.path.join(CURRENT_DIR, "create_bronze_tables.sql")

def generate_ddl():
    if not os.path.exists(DATA_DIR):
        print(f"[BŁĄD] Katalog danych {DATA_DIR} nie istnieje! Uruchom najpierw eksport.")
        return
        
    sql_statements = []
    sql_statements.append(f"-- ================================================================================")
    sql_statements.append(f"-- Automatycznie wygenerowany skrypt DDL dla tabel Bronze w BigQuery")
    sql_statements.append(f"-- Projekt GCP: {PROJECT_ID}")
    sql_statements.append(f"-- Kubełek GCS: {BUCKET_NAME}")
    sql_statements.append(f"-- ================================================================================\n")
    
    # Przechodzimy po wszystkich podkatalogach baz danych w folderze 'data'
    for db_name in sorted(os.listdir(DATA_DIR)):
        db_path = os.path.join(DATA_DIR, db_name)
        if not os.path.isdir(db_path):
            continue
            
        sql_statements.append(f"\n-- --------------------------------------------------------------------------------")
        sql_statements.append(f"-- BAZA DANYCH: {db_name}")
        sql_statements.append(f"-- --------------------------------------------------------------------------------\n")
        
        # Przechodzimy po wszystkich plikach parquet w danej bazie
        for file_name in sorted(os.listdir(db_path)):
            # Interesują nas tylko pliki .parquet (ignorujemy np. ukryte pliki systemowe)
            if not file_name.endswith(".parquet"):
                continue
                
            # Wykluczamy pliki migracji Entity Framework lub specyficzne klucze systemowe, jeśli nie są potrzebne analitycznie
            # Ale zgodnie z filozofią ELT mapujemy je, dając użytkownikowi wybór
            table_name = file_name.replace(".parquet", "")
            
            # Czyszczenie i ujednolicanie nazw tabel w BigQuery
            # Np. "catalog-db" -> "catalog", "customer-manager-db" -> "customer_manager"
            clean_db_name = db_name.replace("-db", "").replace("-", "_")
            bq_table_name = f"raw_{clean_db_name}_{table_name}"
            
            # Pełna ścieżka do pliku w Google Cloud Storage
            gcs_uri = f"gs://{BUCKET_NAME}/data/{db_name}/{file_name}"
            
            # Szablon zapytania SQL do tabeli zewnętrznej
            sql = f"""CREATE OR REPLACE EXTERNAL TABLE `{PROJECT_ID}.bronze.{bq_table_name}`
OPTIONS (
  format = 'PARQUET',
  uris = ['{gcs_uri}']
);"""
            sql_statements.append(sql)
            
    # Zapisujemy wygenerowany skrypt SQL do pliku
    with open(OUTPUT_SQL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))
        
    print(f"\n[SUKCES] Wygenerowano plik SQL z DDL tabel Bronze!")
    print(f"Ścieżka do pliku: {OUTPUT_SQL_FILE}")
    print("-> Możesz teraz otworzyć ten plik, skopiować całą zawartość i wkleić ją do edytora SQL w BigQuery.")
    print("-> Po uruchomieniu wszystkie Twoje tabele z baz danych zostaną natychmiast zmapowane!")

if __name__ == "__main__":
    generate_ddl()
