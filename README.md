# Bake2Home Data Warehouse

This repository contains the Google Cloud Dataform project and related tools for the Bake2Home analytical data warehouse. The core logic transforms raw transactional and planner data into a clean, dimensional model optimized for BI reporting (e.g., Looker Studio).

## Directory Structure

*   **`definitions/`**: The core Dataform project containing all SQLX transformations.
    *   **`definitions/silver/`**: The Staging layer. Cleans, standardizes, and casts raw data from the operational databases into uniform views.
    *   **`definitions/gold/`**: The Dimensional layer (Kimball methodology). Contains Facts, Dimensions, Bridge tables (for many-to-many relationships), and flat, denormalized Reporting Views designed directly for BI tools.
*   **`Docs/`**: Project documentation, including business definitions of measures, attributes, and column data types.
*   **`docker_db_to_gcs_export/`**: Utilities and Docker configurations for extracting raw operational databases and loading them into Google Cloud Storage (GCS).
*   **`google_maps_scripts/`**: Python scripts for enriching location data, geocoding customer addresses, and calculating POI buffers (e.g., distances to competitors and own sites).
*   **`model.drawio`**: The visual Entity-Relationship Diagram (ERD) mapping the entire Data Warehouse architecture.

## Development

To compile the Dataform project locally and verify there are no syntax or dependency errors:

```bash
npx dataform compile
```
