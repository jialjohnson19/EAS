# -----------------------------
# IMPORTS
# -----------------------------

import os
import webbrowser
from pathlib import Path

# Services
from src.input_manager import get_or_create_inputs
from src.setup import geocode_address
from src.map_setup import create_leaflet_subject_map
from src.eris_setup import load_eris_csv
from src.report_writer import create_word_report

# Models
from src.models.project import Project


# -----------------------------
# CONFIGURATION
# -----------------------------

# Toggle development testing
TEST_MODE = True

# Test property used during development
TEST_PROJECT = Project(
    entity="Test Client",
    property_type="Commercial",
    property_address="107 West Waters Avenue, Tampa, FL 33604",
    city_name="Tampa",
    county_name="Hillsborough",
    parcel_number="TEST-12345"
)

# Test ERIS CSV filename
TEST_ERIS_CSV = "107_w_waters_ERIS"


# -----------------------------
# MAIN FUNCTION
# -----------------------------

def main():

    print("\n===================================")
    print("PHASE I ESA REPORT GENERATOR")
    print("===================================\n")

    # ---------------------------------
    # LOAD PROJECT
    # ---------------------------------

    if TEST_MODE:

        print("Running in TEST MODE...\n")

        project = TEST_PROJECT

        project_folder = Path("projects/test_project")
        project_folder.mkdir(parents=True, exist_ok=True)

    else:

        print("Loading project inputs...\n")

        project_folder, project = get_or_create_inputs()

    print(f"Property Address: {project.property_address}")

    # ---------------------------------
    # GEOCODE PROPERTY
    # ---------------------------------

    print("\nGeocoding property...")

    result = geocode_address(project.property_address)

    if not result:
        print("ERROR: Failed to geocode property.")
        return

    print("Geocoding successful.")

    # ---------------------------------
    # LOAD ERIS DATA
    # ---------------------------------

    print("\nLoading ERIS data...")

    if TEST_MODE:
        eris_csv_name = TEST_ERIS_CSV

    else:
        eris_csv_name = (
            project.property_address.lower()
            .replace(",", "")
            .replace(".", "")
            .replace(" ", "_")
            + "_ERIS"
        )

    try:

        eris_df = load_eris_csv(eris_csv_name)

        print("ERIS data loaded successfully.")

    except Exception as e:

        print(f"ERROR loading ERIS CSV:\n{e}")
        return

    # ---------------------------------
    # GENERATE MAP
    # ---------------------------------

    print("\nGenerating subject property map...")

    try:

        map_path = create_leaflet_subject_map(
            result=result,
            eris_df=eris_df
        )

        print(f"Map created:\n{map_path}")

    except Exception as e:

        print(f"ERROR generating map:\n{e}")
        return

    # ---------------------------------
    # OPEN MAP
    # ---------------------------------

    try:

        webbrowser.open(
            "file://" + os.path.abspath(map_path)
        )

        print("Opened map in browser.")

    except Exception as e:

        print(f"WARNING: Could not open browser:\n{e}")

    # ---------------------------------
    # GENERATE WORD REPORT
    # ---------------------------------

    print("\nGenerating Phase I report...")

    report_path = project_folder / "phase1_report.docx"

    try:

        create_word_report(
            project=project,
            output_path=report_path
        )

        print(f"Report created:\n{report_path}")

    except Exception as e:

        print(f"ERROR generating report:\n{e}")
        return

    # ---------------------------------
    # FINISHED
    # ---------------------------------

    print("\n===================================")
    print("PROCESS COMPLETE")
    print("===================================\n")


# -----------------------------
# RUN APPLICATION
# -----------------------------

if __name__ == "__main__":
    main()


# # import libraries 
# from src.setup import geocode_address
# from src.map_setup import create_leaflet_subject_map
# from src.eris_setup import load_eris_csv

# import webbrowser
# import os

# ######### beginning of code ########
# # address = input("Enter the address of the subject property: ")

# # standing address for testing 
# address = "107 West Waters Avenue, Tampa, FL 33604"

# # ERIS CSV name for this property
# eris_csv_name = "107_w_waters_ERIS"

# # PRINT ADDRESS TO BE GEOCODED
# result = geocode_address(address)

# # LOAD ERIS CSV
# eris_df = load_eris_csv(eris_csv_name)

# # PATH TO MAP 
# map_path = create_leaflet_subject_map(
#     result=result,
#     eris_df=eris_df
# )

# # OPEN BROWSER TO VIEW MAP
# webbrowser.open(
#     "file://" + os.path.abspath(map_path)
# )