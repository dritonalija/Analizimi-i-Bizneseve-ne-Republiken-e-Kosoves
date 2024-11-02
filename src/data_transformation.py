import pandas as pd
import numpy as np

# Ngarkon të dhënat nga një skedar CSV në një DataFrame të Pandas
def load_data(file_path):
    """Ngarkon të dhënat nga një skedar CSV në një DataFrame të Pandas."""
    return pd.read_csv(file_path)

# Kategorizon 'Kapitali' në intervale të caktuara
def bin_kapitali(df):
    """Kategorizon 'Kapitali' në intervale të caktuara."""
    df["Kapitali_Bin"] = pd.cut(
        df["Kapitali"],
        bins=[0, 500, 1000, 5000, 10000, 20000, 30000, np.inf],
        labels=[
            "0-500",
            "500-1000",
            "1000-5000",
            "5000-10000",
            "10000-20000",
            "20000-30000",
            "30000+",
        ],
        include_lowest=True  # Përfshin vlerën 0 në intervalin e parë
    )
    return df

# Kategorizon 'Numri i punëtorëve' në intervale të caktuara
def bin_employee(df):
    """Kategorizon 'Numri i punëtorëve' në intervale të caktuara."""
    df["Numri i punëtorëve Bin"] = pd.cut(
        df["Numri i punëtorëve"],
        bins=[0, 5, 20, 50, 100, 500, 1000, 2500, np.inf],
        labels=[
            "0-5",
            "6-20",
            "21-50",
            "51-100",
            "101-500",
            "501-1000",
            "1001-2500",
            "2500+",
        ],
    )
    return df

# Llogarit moshën e secilit biznes bazuar në datën e regjistrimit
def calculate_business_age(df, current_year=2024):
    """Llogarit moshën e secilit biznes bazuar në 'Data e regjistrimit'."""
    df["Data e regjistrimit"] = pd.to_datetime(df["Data e regjistrimit"], errors="coerce")
    df["Business_Age"] = current_year - df["Data e regjistrimit"].dt.year
    return df

# Funksioni kryesor për të ngarkuar, përpunuar dhe shfaqur të dhënat
if __name__ == "__main__":
    # Përkufizon shtegun e skedarit CSV
    file_path = "../data/processed/prepared_data.csv"  # Përditësoni këtë shteg sipas vendndodhjes së skedarit tuaj
    
    # Ngarkon të dhënat
    df = load_data(file_path)
    
    # Aplikon funksionet e kategorizimit dhe llogaritjes së moshës
    df = bin_kapitali(df)
    df = bin_employee(df)
    df = calculate_business_age(df)
    
    # Shfaq rezultatin
    print(df[["Kapitali", "Kapitali_Bin", "Numri i punëtorëve", "Numri i punëtorëve Bin", "Business_Age"]].head(30))
