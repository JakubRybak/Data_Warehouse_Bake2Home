"""
gcp_utils.py - Helper utilities for communicating with Google Cloud Platform (GCP) services.
Handles fetching geographic delivery zone vertices from BigQuery and uploading Parquet blobs to GCS.
"""
import json
import io
from google.cloud import bigquery
from google.cloud import storage

def get_active_locations(project_id: str) -> list:
    """
    Fetches only active delivery zones (locations containing current customer addresses) from BigQuery.
    Returns a list of dictionaries with id_location, location_name, and parsed GPS vertices list.
    """
    print("Initializing Google BigQuery client...")
    bq_client = bigquery.Client(project=project_id)
    
    # Query only 'live' zones that have current customers mapped to them
    sql_query = f"""
        SELECT 
          l.id_location,
          l.name AS location_name,
          l.vertexes
        FROM `{project_id}.gold.dim_location` l
        WHERE l.is_current = TRUE
          AND l.status = 'EXISTING'
          AND l.id_location IN (
            SELECT DISTINCT id_location 
            FROM `{project_id}.gold.dim_customer_address`
            WHERE id_location != -999999 AND state = 'CURRENT'
          )
    """
    
    query_job = bq_client.query(sql_query)
    results = query_job.result()
    
    active_zones = []
    for row in results:
        active_zones.append({
            "id_location": row.id_location,
            "name": row.location_name,
            "vertexes": json.loads(row.vertexes)
        })
        
    print(f"Successfully retrieved {len(active_zones)} active delivery zones from BigQuery.")
    return active_zones

def upload_parquet_to_gcs(project_id: str, bucket_name: str, buffer: io.BytesIO) -> None:
    """Uploads a binary memory buffer containing a Parquet file directly to the specified GCS bucket."""
    print(f"Initializing Google Cloud Storage client for bucket: {bucket_name}...")
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("competitors/competitors_raw.parquet")
    
    # Upload streaming directly from RAM buffer without writing local temporary files to container storage
    blob.upload_from_file(buffer, content_type="application/octet-stream")
    print("SUCCESS: competitors_raw.parquet file uploaded successfully to GCS!")
