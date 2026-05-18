import pandas as pd 
from ipyleaflet import Map, Marker, Circle, LayersControl, basemaps


import os
import folium


def create_leaflet_subject_map(result, output_folder="outputs", output_filename="subject_property_map.html"):
    """
    Creates an interactive Leaflet map using Folium and saves it as an HTML file.

    Parameters:
        result (dict): Geocoding result from geocode_address().
        output_folder (str): Folder where the map HTML file will be saved.
        output_filename (str): Name of the saved HTML map file.

    Returns:
        str: Path to the saved map file.
    """

    if result is None:
        print("No geocoded result available to map.")
        return None

    lat = result["latitude"]
    lon = result["longitude"]
    matched_address = result["matched_address"]

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, output_filename)

    m = folium.Map(
        location=[lat, lon],
        zoom_start=16,
        tiles="OpenStreetMap"
    )

    folium.Marker(
        location=[lat, lon],
        popup=matched_address,
        tooltip="Subject Property",
        icon=folium.Icon(color="red", icon="home")
    ).add_to(m)

    folium.Circle(
        location=[lat, lon],
        radius=161,  # 0.10 miles in meters
        popup="0.10 mile radius",
        color="blue",
        fill=False
    ).add_to(m)

    folium.Circle(
        location=[lat, lon],
        radius=402,  # 0.25 miles in meters
        popup="0.25 mile radius",
        color="green",
        fill=False
    ).add_to(m)

    folium.Circle(
        location=[lat, lon],
        radius=805,  # 0.50 miles in meters
        popup="0.50 mile radius",
        color="orange",
        fill=False
    ).add_to(m)

    folium.Circle(
        location=[lat, lon],
        radius=1609,  # 1.00 mile in meters
        popup="1.00 mile radius",
        color="purple",
        fill=False
    ).add_to(m)

    folium.LayerControl().add_to(m)

    m.save(output_path)

    print(f"Leaflet map saved to: {output_path}")

    return output_path

