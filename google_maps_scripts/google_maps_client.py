"""
google_maps_client.py - Integration module for the Google Places API (New).
Handles retrieving POI listings (competitors) based on geographic coordinates.
"""
import requests

def fetch_nearby_competitors(lat: float, lon: float, api_key: str, radius: float = 700.0) -> list:
    """
    Executes a NearbySearch query against the Google Places API (New) for bakeries and supermarkets.
    Returns the raw list of places returned by Google.
    """
    endpoint = "https://places.googleapis.com/v1/places:searchNearby"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        # FieldMask strictly determines what attributes are returned and dictates API pricing per call
        "X-Goog-FieldMask": "places.id,places.displayName,places.primaryType,places.types,places.location,places.formattedAddress"
    }
    
    body = {
        "includedTypes": ["bakery", "pastry_shop", "supermarket"],
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": radius
            }
        }
    }
    
    response = requests.post(endpoint, headers=headers, json=body)
    if response.status_code != 200:
        print(f"Google Places API Error ({response.status_code}): {response.text}")
        return []
    
    return response.json().get("places", [])
