import pandas as pd

input_path = r"c:\Projekty\Bake2Home\docker_db_to_gcs_export\data\customer-manager-db\Customer.parquet"
output_path = r"c:\Projekty\Bake2Home\docker_db_to_gcs_export\data\customer-manager-db\next_Customer.parquet"

# Wczytujemy plik
df = pd.read_parquet(input_path)

print("--- PRZED ZMIANĄ ---")
print(df.head(1)[['Id', 'Name', 'Updated']])

# Symulujemy, że pierwszy klient zmienił nazwisko w systemie
df.at[0, 'Name'] = df.at[0, 'Name'] + " - ZMIENIONE DO TESTU"
# Ważne: Aktualizujemy datę modyfikacji, bo bez tego mechanizm SCD2 w hurtowni mógłby zignorować zmianę
df.at[0, 'Updated'] = pd.Timestamp.now()

print("\n--- PO ZMIANIE ---")
print(df.head(1)[['Id', 'Name', 'Updated']])

# Zapisujemy nowy plik, pozostawiając resztę klientów nienaruszoną (symulacja nowego pełnego zrzutu z bazy)
df.to_parquet(output_path)
print(f"\nGotowe! Nowy plik zapisany jako: {output_path}")
