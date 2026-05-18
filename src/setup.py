# geocode addresses 
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd 
import plotly.express as px

def geocode_address(address):
    """
    Geocodes an address and returns
    the matched address, latitude,
    and longitude.
    """

    # create geocoder
    geolocator = Nominatim(
        user_agent="environmental_site_geocoder"
    )

    # prevent sending requests too quickly
    geocode = RateLimiter(
        geolocator.geocode,
        min_delay_seconds=1
    )

    # geocode address
    location = geocode(address)

    # if no result found
    if location is None:
        print("No matching address found.")
        return None

    # organize results
    result = {
        "matched_address": location.address,
        "latitude": location.latitude,
        "longitude": location.longitude
    }

    if result:

        print("Matched Address:")
        print(result["matched_address"])

        print("\nLatitude:")
        print(result["latitude"])

        print("\nLongitude:")
        print(result["longitude"])

    return result


def create_subject_property_map(result):
    """
    Creates an interactive map for the matched subject property address.
    """

    if result is None:
        print("No geocoded result available to map.")
        return None

    map_df = pd.DataFrame([{
        "matched_address": result["matched_address"],
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }])

    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        hover_name="matched_address",
        zoom=15,
        height=600
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        title="Matched Subject Property Location",
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    return fig