import os
import folium
import pandas as pd


SOURCE_STYLES = {
    "UST": {"color": "red", "icon": "tint"},
    "LST": {"color": "red", "icon": "tint"},
    "TANK": {"color": "red", "icon": "tint"},
    "AST": {"color": "red", "icon": "tint"},
    "DEL STORAGE TANK": {"color": "lightred", "icon": "tint"},

    "SQG": {"color": "orange", "icon": "trash"},
    "RCRA NON GEN": {"color": "orange", "icon": "trash"},
    "RCRA VSQG": {"color": "orange", "icon": "trash"},
    "TIER 2": {"color": "orange", "icon": "trash"},
    "HMIRS": {"color": "orange", "icon": "warning-sign"},

    "DWM CONTAM": {"color": "darkred", "icon": "remove-sign"},
    "CLEANUP DEP": {"color": "darkred", "icon": "remove-sign"},
    "PRIORITYCLEAN": {"color": "darkred", "icon": "remove-sign"},
    "DEL CONTAM SITE": {"color": "pink", "icon": "remove-sign"},

    "CERCLIS": {"color": "black", "icon": "fire"},
    "CERCLIS NFRAP": {"color": "black", "icon": "fire"},
    "SEMS ARCHIVE": {"color": "black", "icon": "fire"},
    "OSC RESPONSE": {"color": "black", "icon": "fire"},
    "PRP": {"color": "black", "icon": "fire"},

    "SPILLS": {"color": "blue", "icon": "tint"},
    "ERNS": {"color": "blue", "icon": "tint"},
    "ERNS 1987 TO 1989": {"color": "blue", "icon": "tint"},

    "WELL SURVEILLANCE": {"color": "cadetblue", "icon": "cloud"},
    "WCRPS": {"color": "cadetblue", "icon": "cloud"},

    "AFS": {"color": "green", "icon": "cloud"},
    "HIST RISK": {"color": "gray", "icon": "info-sign"},
    "SWF/LF": {"color": "darkgreen", "icon": "trash"},
    "MINES": {"color": "beige", "icon": "cog"},
    "PFAS AFFF": {"color": "purple", "icon": "warning-sign"},

    "DEFAULT": {"color": "lightgray", "icon": "info-sign"}
}


def create_leaflet_subject_map(
    result,
    eris_df=None,
    output_folder="outputs",
    output_filename="subject_property_map.html"
):
    """
    Creates an interactive Leaflet map using Folium and saves it as an HTML file.
    Adds subject property marker, search radius circles, and ERIS site markers.
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

    radius_layers = [
        (161, "0.10 mile radius", "blue"),
        (402, "0.25 mile radius", "green"),
        (805, "0.50 mile radius", "orange"),
        (1609, "1.00 mile radius", "purple"),
    ]

    for radius, label, color in radius_layers:
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            popup=label,
            color=color,
            fill=False
        ).add_to(m)

    if eris_df is not None:
        eris_df = eris_df.copy()

        eris_df["x_nad_83"] = pd.to_numeric(eris_df["x_nad_83"], errors="coerce")
        eris_df["y_nad_83"] = pd.to_numeric(eris_df["y_nad_83"], errors="coerce")

        eris_df = eris_df.dropna(subset=["x_nad_83", "y_nad_83"])

        eris_layer = folium.FeatureGroup(name="ERIS Sites")

        for _, row in eris_df.iterrows():
            site_lat = row["y_nad_83"]
            site_lon = row["x_nad_83"]

            company = row.get("company_name", "Unknown Site")
            source = str(row.get("source", "Unknown Source")).strip().upper()
            address = row.get("address1", "")
            city = row.get("city", "")
            distance = row.get("distance_miles", "")

            style = SOURCE_STYLES.get(source, SOURCE_STYLES["DEFAULT"])

            popup_html = f"""
            <b>{company}</b><br>
            Source: {source}<br>
            Address: {address}<br>
            City: {city}<br>
            Distance: {distance} miles
            """

            folium.Marker(
                location=[site_lat, site_lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=str(company),
                icon=folium.Icon(
                    color=style["color"],
                    icon=style["icon"],
                    prefix="glyphicon"
                )
            ).add_to(eris_layer)

        eris_layer.add_to(m)

    folium.LayerControl().add_to(m)
    m.save(output_path)

    print(f"Leaflet map saved to: {output_path}")

    return output_path