import json
from pathlib import Path
from src.models.project import Project


PROJECTS_DIR = Path("projects")


# -----------------------------
# QUESTION SECTIONS
# -----------------------------

INPUT_SECTIONS = {
    "general_information": {
        "report_number": "EAS Report Number",
        "report_date": "Report Date",
        "property_type": "Enter property type",
        "property_address": "Enter property address",
        "city_name": "Enter city",
        "county_name": "Enter county name",
        "zip_code": "ZIP code",
        "parcel_number": "Parcel/Folio number",
        "site_visit_date": "Site visit date",
        "book_number": "OR Book number",
        "page_number": "Page number",
    },

    "site_information": {
        "property_size": "Property size (acres)",
        "property_description": "Current property use/description",
        "number_of_buildings": "Number of buildings",
        "stories": "Number of stories",
        "building_material": "Building construction type",
        "year_built": "Year built",
        "gross_sqft": "Gross square footage",
        "climate_sqft": "Climate-controlled square footage",
        "remainder_description": "Description of remaining parcel area",
        "ingress_egress": "Ingress/Egress description",
    },

    "utilities": {
        "power_company": "Power supply company",
        "number_transformers": "Number of transformers",
        "transformer_type": "Transformer type (pole/pad mounted)",
        "transformer_location": "Transformer location",
        "pcb_label": "Were transformers labeled non-PCB containing?",
        "natural_gas": "Natural gas connections present?",
        "stormwater": "Stormwater drainage description",
        "wells_present": "Monitor/irrigation/production wells present?",
    },

    "surrounding_properties": {
        "general_location": "General property location description",
        "north_street": "North adjacent street",
        "north_use": "North adjacent land use",
        "south_use": "South adjacent land use/roadway",
        "east_use": "East adjacent land use/roadway",
        "west_use": "West adjacent land use/roadway",
    },

    "historical_review": {
        "aerial_dates": "Aerial photo dates reviewed",
        "earliest_aerial": "Earliest aerial year",
        "topo_dates": "Topographic map dates",
        "sanborn_dates": "Sanborn map availability",
        "city_directories": "City directories reviewed?",
        "tenant_history": "Historic tenants",
    },

    "regulatory_database": {
        "facility_total_half_mile": "Total facilities within 0.5 mile",
        "tank_inclusion_status": "Is subject property listed? (yes/no)",
        "remediated_count": "No-action facilities count",
        "ongoing_remediation_count": "Ongoing remediation count",
        "no_action_count": "No further action count",
    },

    "hazardous_waste": {
        "sqg_count": "SQG count within 0.25 miles",
        "sqg_details": "SQG summary text",
        "sqg_facility_name": "SQG facility name",
        "distance_sqg_facility": "Distance to SQG facility",
        "cesqg_facility_name": "CESQG facility name",
        "distance_cesqg_facility": "Distance to CESQG facility",
    },
}


# -----------------------------
# BASIC HELPERS
# -----------------------------

def ask(prompt, current_value=None):
    """
    Ask a question.
    If a previous value exists, pressing Enter keeps it.
    If no value exists, pressing Enter saves Unknown.
    """

    if current_value and current_value != "Unknown":
        answer = input(f"{prompt} [{current_value}]: ").strip()
        return answer if answer else current_value

    answer = input(f"{prompt} (press Enter if unknown): ").strip()
    return answer if answer else "Unknown"


def make_project_name(address):
    """
    Converts an address into a safe folder name.
    Example: 107 West Waters Avenue -> 107_west_waters_avenue
    """

    if not address or address == "Unknown":
        return "unnamed_project"

    safe_name = (
        address.lower()
        .replace(",", "")
        .replace(".", "")
        .replace("#", "")
        .replace("/", "_")
        .replace(" ", "_")
    )

    return safe_name


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_json(path):
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)

    return {}


# -----------------------------
# PROJECT SELECTION
# -----------------------------

def list_existing_projects():
    PROJECTS_DIR.mkdir(exist_ok=True)

    projects = [
        folder for folder in PROJECTS_DIR.iterdir()
        if folder.is_dir()
    ]

    return projects


def select_existing_project():
    projects = list_existing_projects()

    if not projects:
        print("\nNo saved projects found.")
        return None

    print("\nSaved projects:")
    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project.name}")

    choice = input("\nSelect a project number, or press Enter to start new: ").strip()

    if choice == "":
        return None

    if choice.isdigit() and 1 <= int(choice) <= len(projects):
        return projects[int(choice) - 1]

    print("Invalid selection. Starting a new project.")
    return None


# -----------------------------
# INPUT COLLECTION
# -----------------------------

def collect_inputs(existing_inputs=None):
    """
    Collect all report inputs section by section.
    Saves values in a flat dictionary.
    """

    if existing_inputs is None:
        existing_inputs = {}

    inputs = existing_inputs.copy()

    for section_name, questions in INPUT_SECTIONS.items():
        print(f"\n--- {section_name.replace('_', ' ').title()} ---")

        for key, prompt in questions.items():
            current_value = inputs.get(key)
            inputs[key] = ask(prompt, current_value)

    return inputs


def edit_input_section(inputs):
    """
    Allows the user to edit only one section instead of retyping everything.
    """

    section_names = list(INPUT_SECTIONS.keys())

    print("\nWhich section do you want to edit?")
    for i, section in enumerate(section_names, start=1):
        print(f"{i}. {section.replace('_', ' ').title()}")

    choice = input("\nSelect a section number, or press Enter to skip editing: ").strip()

    if choice == "":
        return inputs

    if not choice.isdigit() or not (1 <= int(choice) <= len(section_names)):
        print("Invalid selection. No edits made.")
        return inputs

    selected_section = section_names[int(choice) - 1]
    questions = INPUT_SECTIONS[selected_section]

    print(f"\n--- Editing {selected_section.replace('_', ' ').title()} ---")

    for key, prompt in questions.items():
        current_value = inputs.get(key)
        inputs[key] = ask(prompt, current_value)

    return inputs


# -----------------------------
# MAIN FUNCTION USED BY main.py
# -----------------------------

def get_or_create_inputs():
    """
    Main function called by main.py.

    Returns:
        project_folder, inputs
    """

    PROJECTS_DIR.mkdir(exist_ok=True)

    existing_project = select_existing_project()

    if existing_project:
        project_folder = existing_project
        input_path = project_folder / "inputs.json"
        inputs = load_json(input_path)

        print(f"\nLoaded saved project: {project_folder.name}")

        edit_choice = input(
            "Press Enter to reuse saved inputs, type 'edit' to edit one section, "
            "or type 'all' to re-enter everything: "
        ).strip().lower()

        if edit_choice == "edit":
            inputs = edit_input_section(inputs)
            save_json(inputs, input_path)

        elif edit_choice == "all":
            inputs = collect_inputs(existing_inputs=inputs)
            save_json(inputs, input_path)

        return project_folder, inputs

    print("\nCreating a new project.")
    inputs = collect_inputs()

    project_name = make_project_name(inputs.get("property_address"))
    project_folder = PROJECTS_DIR / project_name
    project_folder.mkdir(parents=True, exist_ok=True)

    input_path = project_folder / "inputs.json"
    save_json(inputs, input_path)

    print(f"\nSaved project inputs to: {input_path}")

    project = Project(**inputs)

    return project_folder, project
