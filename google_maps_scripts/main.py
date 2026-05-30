"""
main.py - Main orchestrator for the competitor data pipeline (Cloud Functions / Cloud Run Entrypoint).
Integrates BigQuery active zones retrieval, A4 hex-grid optimization,
Google Places API queries, business filtering, Parquet serialization, and GCS upload.
"""
import os
import io
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyproj
from shapely.geometry import Polygon

# Imports from helper modules (Modular Architecture)
from algo_logic import a4_standard
from gcp_utils import get_active_locations, upload_parquet_to_gcs
from google_maps_client import fetch_nearby_competitors

# GCP Environment variables loaded from cloud environment
PROJECT_ID = os.environ.get("GCP_PROJECT", "bake2home-data-warehouse")
BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "bake2home-raw-data")
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()

# Projections configuration (GPS EPSG:4326 <-> Metric EPSG:3857)
to_meters = pyproj.Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
to_gps = pyproj.Transformer.from_crs("epsg:3857", "epsg:4326", always_xy=True)

def parse_zone_to_polygon(vertexes: list) -> Polygon:
    """Converts a list of GPS vertices from JSON into a Shapely Polygon object in meters."""
    coords_meters = []
    for v in vertexes:
        x, y = to_meters.transform(v["longitude"], v["latitude"])
        coords_meters.append((x, y))
    return Polygon(coords_meters)

def serialize_to_parquet(competitors: dict) -> io.BytesIO:
    """Converts the competitors dictionary to a Pandas DataFrame and serializes it to binary Parquet in RAM."""
    df = pd.DataFrame(list(competitors.values()))

    # Strict PyArrow schema declaration (guarantees schema integrity inside BigQuery)
    arrow_schema = pa.schema([
        ("place_id", pa.string()),
        ("name", pa.string()),
        ("address", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("competitor_type", pa.string()),
        ("types", pa.list_(pa.string())),
        ("extracted_at", pa.timestamp("us", tz="UTC"))
    ])

    table = pa.Table.from_pandas(df, schema=arrow_schema, preserve_index=False)
    
    parquet_buffer = io.BytesIO()
    pq.write_table(table, parquet_buffer, compression="SNAPPY")
    parquet_buffer.seek(0)
    return parquet_buffer

def run_competitors_pipeline(request=None):
    """Main pipeline execution trigger (Entrypoint for Google Cloud Functions)."""
    print("=== STARTING MODULAR COMPETITOR DATA PIPELINE ===")
    
    if not API_KEY:
        error_msg = "CRITICAL ERROR: GOOGLE_MAPS_API_KEY is not set in environment variables."
        print(error_msg)
        return error_msg, 500
        
    try:
        active_zones = get_active_locations(PROJECT_ID)
    except Exception as e:
        error_msg = f"Failed to retrieve active zones from BigQuery: {e}"
        print(error_msg)
        return error_msg, 500

    if not active_zones:
        msg = "No active delivery zones found. Pipeline execution completed."
        print(msg)
        return msg, 200

    all_unique_competitors = {}
    total_api_calls = 0

    for zone in active_zones:
        print(f"\nAnalyzing delivery zone: {zone['name']} (ID: {zone['id_location']})...")
        
        try:
            poly = parse_zone_to_polygon(zone["vertexes"])
        except Exception as e:
            print(f"Skipping zone {zone['name']} due to geometry parsing error: {e}")
            continue

        # Generate optimal honeycomb search grid (700m radius)
        radius_meters = 700.0
        centers_meters = a4_standard(poly, radius_meters)
        print(f"Hexagonal grid coverage generated {len(centers_meters)} search circles.")

        # Query Places API for each circle center
        for idx, (x, y) in enumerate(centers_meters, 1):
            lon, lat = to_gps.transform(x, y)
            print(f" -> Querying API {idx}/{len(centers_meters)} at coords: {lat:.6f}, {lon:.6f}...")
            places = fetch_nearby_competitors(lat, lon, API_KEY, radius_meters)
            total_api_calls += 1

            if len(places) == 20:
                print(f"WARNING: Search circle at {lat:.6f}, {lon:.6f} (Zone: {zone['name']}) "
                      f"returned exactly 20 places. Some competitors might have been truncated due to "
                      f"Google Places API limit of 20 results per call. Consider reducing search radius.")

            for p in places:
                place_id = p.get("id")
                if not place_id or place_id in all_unique_competitors:
                    continue

                types = p.get("types", [])
                is_bakery = "bakery" in types or "pastry_shop" in types
                is_supermarket = "supermarket" in types

                # Business Filtering: Strictly discard 'others' (cafes, restaurants, gas stations, etc.)
                if not (is_bakery or is_supermarket):
                    continue

                # Categorize competitor type (bakery vs supermarket)
                competitor_type = "bakery" if is_bakery else "supermarket"
                
                all_unique_competitors[place_id] = {
                    "place_id": place_id,
                    "name": p.get("displayName", {}).get("text", "Unknown"),
                    "address": p.get("formattedAddress", "Unknown"),
                    "latitude": float(p.get("location", {}).get("latitude", 0.0)),
                    "longitude": float(p.get("location", {}).get("longitude", 0.0)),
                    "competitor_type": competitor_type,
                    "types": types,
                    "extracted_at": datetime.datetime.now(datetime.timezone.utc)
                }

    print(f"\nAPI search completed. Total API calls executed: {total_api_calls}.")
    print(f"Found {len(all_unique_competitors)} unique competitors after filtering.")

    if not all_unique_competitors:
        msg = "No competitor locations found in active zones. End of pipeline."
        print(msg)
        return msg, 200

    # Convert to Pandas and PyArrow binary Parquet format
    try:
        parquet_buffer = serialize_to_parquet(all_unique_competitors)
        upload_parquet_to_gcs(PROJECT_ID, BUCKET_NAME, parquet_buffer)
    except Exception as e:
        error_msg = f"Failed to serialize or upload Parquet dataset: {e}"
        print(error_msg)
        return error_msg, 500

    success_msg = f"Pipeline successfully completed. Uploaded {len(all_unique_competitors)} records to gs://{BUCKET_NAME}/competitors/competitors_raw.parquet."
    print(success_msg)
    return success_msg, 200

if __name__ == "__main__":
    run_competitors_pipeline()
