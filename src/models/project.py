from dataclasses import dataclass

@dataclass
class Project:

    # General Information
    report_number: str = "Unknown"

    entity: str = "Unknown"
    property_type: str = "Unknown"
    property_address: str = "Unknown"
    city_name: str = "Unknown"
    county_name: str = "Unknown"
    parcel_number: str = "Unknown"
    site_visit_date: str = "Unknown"
    book_number: str = "Unknown"
    page_number: str = "Unknown"

    # Site Information
    property_size: str = "Unknown"
    property_description: str = "Unknown"
    number_of_buildings: str = "Unknown"
    stories: str = "Unknown"
    building_material: str = "Unknown"
    year_built: str = "Unknown"
    gross_sqft: str = "Unknown"
    climate_sqft: str = "Unknown"
    remainder_description: str = "Unknown"
    ingress_egress: str = "Unknown"

    # Utilities
    power_company: str = "Unknown"
    number_transformers: str = "Unknown"
    transformer_type: str = "Unknown"
    transformer_location: str = "Unknown"
    pcb_label: str = "Unknown"
    natural_gas: str = "Unknown"
    stormwater: str = "Unknown"
    wells_present: str = "Unknown"