import pandas as pd
import numpy as np
import os


def load_data(file_path):
    """Load CSV data into a Pandas DataFrame."""
    return pd.read_csv(file_path)


def normalize_status(df):
    """Standardize the Statusi column and extract inactivity date if available."""
    df["Inactivity_Date"] = pd.NaT

    def parse_status(value):
        if value.startswith("pasiv-"):
            date_str = value.split("-")[1]
            inactivity_date = pd.to_datetime(
                date_str, format="%d/%m/%Y", errors="coerce"
            )
            return "Inactive", inactivity_date
        elif value == "Aktiv":
            return "Active", pd.NaT
        elif value == "Shuar":
            return "Closed", pd.NaT
        else:
            return value, pd.NaT

    df[["Statusi", "Inactivity_Date"]] = df["Statusi"].apply(
        lambda x: pd.Series(parse_status(x))
    )
    return df


def format_dates(df):
    df["Data e regjistrimit"] = pd.to_datetime(
        df["Data e regjistrimit"], errors="coerce"
    )
    return df


def split_activities(df):
    df["Aktivitetet"] = df["Aktivitetet"].str.split(",")
    return df.explode("Aktivitetet").reset_index(drop=True)


def remove_duplicates(df):
    return df.drop_duplicates()


def calculate_business_age(df, current_year=2024):
    df["Business_Age"] = current_year - df["Data e regjistrimit"].dt.year
    return df


def binarize_gender(df):
    df["Gjinia_Binar"] = df["Gjinia e pronarit"].apply(
        lambda x: 1 if x == "Mashkull" else 0
    )
    return df


def bin_employee_count(df):
    df["Employee_Bin"] = pd.cut(
        df["Numri i punëtorëve"],
        bins=[0, 5, 10, 50, 100, np.inf],
        labels=["1-5", "6-10", "11-50", "51-100", "100+"],
    )
    return df


def save_data(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to '{output_path}'")


def preprocess_data(file_path, output_path):
    """Complete preprocessing pipeline."""
    df = load_data(file_path)
    df = normalize_status(df)
    df = format_dates(df)
    df = split_activities(df)
    # df = remove_duplicates(df)
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
