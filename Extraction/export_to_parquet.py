import os
import sys
import pandas as pd
from sqlalchemy import create_engine, inspect

# PostgreSQL database connection credentials (Docker)
DB_USER = "admin"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# List of 8 operational databases defined in the system
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

# Dictionary specifying columns to drop for each table to ensure GDPR/RODO compliance and security.
# Key is formatted as "database_name.table_name" to be perfectly precise.
EXCLUDED_COLUMNS = {
    "delivery-account-manager-db.DeliveryMan": [
        "Pesel",
        "NumberOfIDCard",
        "NIP",
        "ContractOwner",
        "PictureFileName",
        "PhoneNumber",
        "Email",
        "DateOfBirth"
    ],
    "delivery-account-manager-db.BankAccount": [
        "BankAccountNumber"
    ],
    "delivery-account-manager-db.Address": [
        "StreetName",
        "HouseNumber",
        "ZipCode"
    ],
    "customer-manager-db.Customer": [
        "PhoneNumber",
        "Email",
        "Avatar",
        "CustomerIp"
    ],
    "customer-manager-db.CustomerAddress": [
        "EntryInformationAndCodes",
        "AdditionalInformation"
    ],
    "client-manager-db.Client": [
        "BankAccount",
        "Phone",
        "Email",
        "TpayMerchantId"
    ],
    "client-manager-db.Person": [
        "Phone",
        "Email"
    ],
    "wallet-db.PaymentMethods": [
        "EncryptedToken",
        "CardMask"
    ],
    "wallet-db.Payments": [
        "PaidByTransactionId"
    ],
    "wallet-db.RefundFinalizationError": [
        "PayURefundId",
        "ExtRefundId"
    ],
    "delivery-manager-db.Deliveries": [
        "EntryInformationAndCodes",
        "AdditionalInformation"
    ]
}

# Destination path for extracted data - 'data' folder inside the current 'Extraction' folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(CURRENT_DIR, "data")

def export_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Starting export of databases to Parquet format in the output directory: {OUTPUT_DIR}")
    
    for db_name in DATABASES:
        print(f"\n========================================")
        print(f" Connecting to database: {db_name}")
        print(f"========================================")
        
        # PostgreSQL connection string
        conn_str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{db_name}"
        
        try:
            engine = create_engine(conn_str)
            inspector = inspect(engine)
            
            # Get names of all tables in the public schema
            tables = inspector.get_table_names(schema="public")
            
            if not tables:
                print(f" [INFO] No tables in 'public' schema for database: {db_name}")
                continue
                
            # Excluded tables due to security reasons or lack of analytical usefulness
            EXCLUDED_TABLES = {
                "DataProtectionKeys",
                "__EFMigrationsHistory",
                "CustomerAndroidToken",
                "DeliveryManAndroidToken"
            }
            
            # Create a dedicated subdirectory for the specific database
            db_dir = os.path.join(OUTPUT_DIR, db_name)
            os.makedirs(db_dir, exist_ok=True)
            
            for table in tables:
                if table in EXCLUDED_TABLES:
                    print(f"  -> Skipping table (security/not analytically useful): {table}")
                    continue
                print(f"  -> Exporting table: {table} ... ", end="")
                try:
                    # Read table into a Pandas DataFrame
                    df = pd.read_sql_table(table, engine, schema="public")
                    
                    # Drop PII / sensitive columns if defined
                    db_table_key = f"{db_name}.{table}"
                    if db_table_key in EXCLUDED_COLUMNS:
                        cols_to_drop = [col for col in EXCLUDED_COLUMNS[db_table_key] if col in df.columns]
                        if cols_to_drop:
                            df = df.drop(columns=cols_to_drop)
                            print(f"(Dropped PII: {', '.join(cols_to_drop)}) ... ", end="")
                            
                    # Target path for the Parquet file
                    parquet_file = os.path.join(db_dir, f"{table}.parquet")
                    
                    # Write to Parquet using the pyarrow engine
                    df.to_parquet(parquet_file, index=False, engine="pyarrow")
                    print(f"SUCCESS ({len(df)} rows -> data/{db_name}/{table}.parquet)")
                except Exception as e:
                    print(f"ERROR (Details: {e})")
                    
        except Exception as e:
            print(f" [ERROR] Could not connect to database {db_name}. Details: {e}")
            
    print("\n========================================")
    print(" Export completed successfully!")
    print(f" You can find the extracted data files in: {OUTPUT_DIR}")
    print("========================================")

if __name__ == "__main__":
    # Verify dependencies
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
        print(f"Missing Python packages: {', '.join(missing_deps)}")
        print("Run in the console (preferably inside your venv):")
        print(f"  pip install {' '.join(missing_deps)}")
        sys.exit(1)
        
    export_all()
