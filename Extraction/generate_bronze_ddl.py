import os

# Configuration of your GCP project and bucket
PROJECT_ID = "bake2home-data-warehouse"
BUCKET_NAME = "bake2home-raw-data"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")
OUTPUT_SQL_FILE = os.path.join(CURRENT_DIR, "create_bronze_tables.sql")

def generate_ddl():
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Data directory {DATA_DIR} does not exist! Please run the export first.")
        return
        
    sql_statements = []
    sql_statements.append(f"-- ================================================================================")
    sql_statements.append(f"-- Automatically generated DDL script for Bronze tables in BigQuery")
    sql_statements.append(f"-- GCP Project: {PROJECT_ID}")
    sql_statements.append(f"-- GCS Bucket: {BUCKET_NAME}")
    sql_statements.append(f"-- ================================================================================\n")
    
    # Iterate through all database subdirectories in the 'data' folder
    for db_name in sorted(os.listdir(DATA_DIR)):
        db_path = os.path.join(DATA_DIR, db_name)
        if not os.path.isdir(db_path):
            continue
            
        sql_statements.append(f"\n-- --------------------------------------------------------------------------------")
        sql_statements.append(f"-- DATABASE: {db_name}")
        sql_statements.append(f"\n-- --------------------------------------------------------------------------------\n")
        
        # Iterate through all parquet files in the database
        for file_name in sorted(os.listdir(db_path)):
            # We only care about .parquet files (ignoring hidden system files, etc.)
            if not file_name.endswith(".parquet"):
                continue
                
            # Exclude EF migrations or system keys if they are not analytically useful
            # Following ELT patterns, we map them if they exist in the folder, giving the user control
            table_name = file_name.replace(".parquet", "")
            
            # Cleaning and normalizing table names in BigQuery
            # E.g., "catalog-db" -> "catalog", "customer-manager-db" -> "customer_manager"
            clean_db_name = db_name.replace("-db", "").replace("-", "_")
            bq_table_name = f"raw_{clean_db_name}_{table_name}"
            
            # Full file path in Google Cloud Storage
            gcs_uri = f"gs://{BUCKET_NAME}/data/{db_name}/{file_name}"
            
            # SQL template for creating the external table
            sql = f"""CREATE OR REPLACE EXTERNAL TABLE `{PROJECT_ID}.bronze.{bq_table_name}`
OPTIONS (
  format = 'PARQUET',
  uris = ['{gcs_uri}']
);"""
            sql_statements.append(sql)
            
    # Save the generated SQL script to a file
    with open(OUTPUT_SQL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))
        
    print(f"\n[SUCCESS] Generated SQL file with DDL for Bronze tables!")
    print(f"File path: {OUTPUT_SQL_FILE}")
    print("-> You can now open this file, copy all its content, and paste it into the BigQuery SQL Editor.")
    print("-> Once executed, all your database tables will be mapped instantly!")

if __name__ == "__main__":
    generate_ddl()
