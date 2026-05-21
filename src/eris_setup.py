# This file will contain the setup for the ERIS CSV

from pathlib import Path
import pandas as pd


def load_eris_csv(file_name):
    """
    Loads the ERIS CSV file and returns a cleaned DataFrame.
    """

    ERIS_DATA_PATH = Path("data/eris_data")

    file_path = ERIS_DATA_PATH / f"{file_name}.csv"

    # check if file exists
    if not Path(file_path).is_file():
        print(f"File not found: {file_path}")
        return None

    # load CSV into DataFrame
    try:
        df = pd.read_csv(file_path)

        # -----------------------------
        # CLEAN COLUMN NAMES
        # -----------------------------
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        print("Successfully loaded ERIS CSV:")
        print(file_path)

        print("\nDetected Columns:")
        print(df.columns.tolist())

        return df

    except Exception as e:
        print(f"Error loading ERIS CSV: {e}")
        return None