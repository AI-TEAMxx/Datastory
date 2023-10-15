import pandas as pd
import os


def process_and_normalize_data(
    file_path,
    y_columns,
    output_folder="data/processed",
    value_vars=None,
    var_name=None,
    value_mapping=None,
):
    """
    Process, optionally melt, and normalize dataset, and save it as a JSON file.

    Parameters:
    - file_path (str): The path to the input CSV file.
    - y_columns (list of str): List of column names to be normalized.
    - output_folder (str, optional): The path to the folder where the output JSON file will be saved. Defaults to "data/processed".
    - value_vars (list of str, optional): List of column names that will be melted. Defaults to None.
    - var_name (str, optional): The name to assign to the 'variable' column after melting. Defaults to None.
    - value_mapping (dict, optional): A mapping from original values to desired values in the melted column. Defaults to None.

    Returns:
    - output_path (str): The path where the output JSON file is saved.
    """

    # Load the data
    data = pd.read_csv(file_path)

    # Select data for Norway
    norway_data = data[data["Entity"] == "Norway"].copy()

    # Drop unwanted columns
    norway_data = norway_data.drop(columns=["Entity", "Code"])

    # Melt the data if value_vars and var_name are provided
    if value_vars is not None and var_name is not None:
        norway_data = pd.melt(
            norway_data,
            id_vars=["Year"],
            value_vars=value_vars,
            var_name=var_name,
            value_name="Value",
        )
        # Replace long type names with shorter ones if value_mapping is provided
        if value_mapping is not None:
            norway_data[var_name] = norway_data[var_name].replace(value_mapping)

    # Normalize specified columns using Value/Max Value
    for col in y_columns:
        max_val = norway_data[col].max()
        norway_data[col] = norway_data[col] / max_val

        # testing
        # print(f"Normalizing column: {col}")
        # print(f"Max value before normalization: {max_val}")
        # print("Sample of data after normalization:", norway_data.head())

    # Create a new filename and save as JSON
    file_name = "pd_" + os.path.basename(file_path).replace(".csv", ".json")
    output_path = os.path.join(output_folder, file_name)
    norway_data.to_json(output_path, orient="records")

    return output_path


# Preprocessing data
pd_1 = process_and_normalize_data("data/raw/forest-area-km.csv", ["Forest area"])

# -------------pd_2 set up-------------#

value_vars = [
    "Other renewables (including geothermal and biomass) electricity generation - TWh",
    "Solar generation - TWh",
    "Wind generation - TWh",
    "Hydro generation - TWh",
]

var_name = "Energy Type"
value_names = ["Value"]

value_mapping = {
    "Other renewables (including geothermal and biomass) electricity generation - TWh": "Other Renewables",
    "Solar generation - TWh": "Solar",
    "Wind generation - TWh": "Wind",
    "Hydro generation - TWh": "Hydro",
}

pd_2 = process_and_normalize_data(
    "data/raw/modern-renewable-energy-consumption.csv",
    value_names,
    value_vars=value_vars,
    var_name=var_name,
    value_mapping=value_mapping,
)
