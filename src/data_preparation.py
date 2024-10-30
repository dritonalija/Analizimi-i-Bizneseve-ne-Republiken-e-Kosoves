import pandas as pd
import numpy as np
import os


def load_data(file_path):
    """Load CSV data into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def normalize_status(df):
    """Standardize the Statusi column and add an encoded column without the Inactivity_Date."""
    
    # Define the mapping for the encoded status
    status_mapping = {"Active": 1, "Inactive": 2, "Closed": 3}
    
    def parse_status(value):
        if value.startswith("pasiv-"):
            # Mark any 'pasiv-' status as 'Inactive'
            return "Inactive"
        elif value == "anuluar nga sistemi":
            return "Inactive"
        elif value == "Aktiv":
            return "Active"
        elif value == "Shuar":
            return "Closed"
        else:
            return value

    # Apply the function to parse and standardize the status
    df["Statusi"] = df["Statusi"].apply(parse_status)
    
    # Create an encoded column based on the text column
    df["Statusi_Code"] = df["Statusi"].map(status_mapping)
    return df


    # Create an encoded column based on the text column
    df["Statusi_Code"] = df["Statusi"].map(status_mapping)
    return df


def format_dates(df):
    """Ensure 'Data e regjistrimit' is in datetime format."""
    df["Data e regjistrimit"] = pd.to_datetime(
        df["Data e regjistrimit"], errors="coerce"
    )
    return df


def split_activities(df):
    """Split 'Aktivitetet' column by commas into multiple rows."""
    df["Aktivitetet"] = df["Aktivitetet"].str.split(",")
    return df.explode("Aktivitetet").reset_index(drop=True)


def remove_duplicates(df):
    """Remove duplicate rows across all columns."""
    return df.drop_duplicates()


def calculate_business_age(df, current_year=2024):
    """Calculate the age of each business based on 'Data e regjistrimit'."""
    df["Business_Age"] = current_year - df["Data e regjistrimit"].dt.year
    return df


def binarize_gender(df):
    """Convert 'Gjinia e pronarit' to a binary column."""
    df["Gjinia_Binar"] = df["Gjinia e pronarit"].apply(
        lambda x: 1 if x == "Mashkull" else 0
    )
    return df


def bin_employee_count(df):
    """Categorize 'Numri i punëtorëve' into bins."""
    df["Employee_Bin"] = pd.cut(
        df["Numri i punëtorëve"],
        bins=[0, 5, 10, 50, 100, np.inf],
        labels=["1-5", "6-10", "11-50", "51-100", "100+"],
    )
    return df


def dimension_reduction(df, columns_to_drop):
    """Remove specified columns as part of dimensionality reduction."""
    return df.drop(columns=columns_to_drop, errors="ignore")


def save_data(df, output_path):
    """Save the processed DataFrame to a CSV file."""
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to '{output_path}'")


def preprocess_data(file_path, output_path):
    """Complete preprocessing pipeline."""
    df = load_data(file_path)

    # Drop the specified columns: 'Numri fiskal' and 'Personat e autorizuar'
    df = dimension_reduction(
        df,
        [
            "Numri fiskal",
            "Personat e autorizuar",
            "Numri i regjistrimit",
        ],
    )

    df = normalize_status(df)
    df = format_dates(df)
    # df = split_activities(df)
    df = remove_duplicates(df)
    df = calculate_business_age(df)
    df = binarize_gender(df)
    df = bin_employee_count(df)
    save_data(df, output_path)


# Main script execution
if __name__ == "__main__":
    # Define file paths
    input_file_path = "../data/raw/data-2023.csv"  # Adjusted path for input file
    output_file_path = (
        "../data/processed/preprocessed_data-2023.csv"  # Adjusted path for output file
    )

    # Ensure the 'processed' directory exists
    os.makedirs("../data/processed", exist_ok=True)

    # Run the preprocessing
    preprocess_data(input_file_path, output_file_path)
