import pandas as pd
import numpy as np

# Funksioni për të zbuluar outliers duke përdorur metodën IQR
def detect_outliers_iqr(df, column):
    """
    Zbulon outliers në një kolonë duke përdorur metodën IQR.
    """
    Q1 = df[column].quantile(0.25)  # Kuartili i parë
    Q3 = df[column].quantile(0.75)  # Kuartili i tretë
    IQR = Q3 - Q1  # Diferenca midis kuartileve
    lower_bound = Q1 - 1.5 * IQR  # Kufiri i poshtëm
    upper_bound = Q3 + 1.5 * IQR  # Kufiri i sipërm
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]  # Filtron outliers

# Funksioni për të zbuluar outliers duke përdorur Z-Score
def detect_outliers_zscore(df, column, threshold=3):
    """
    Zbulon outliers në një kolonë duke përdorur metodën Z-Score.
    """
    mean = df[column].mean()  # Mesatarja
    std_dev = df[column].std()  # Devijimi standard
    z_scores = (df[column] - mean) / std_dev  # Llogarit Z-Score
    return df[np.abs(z_scores) > threshold]  # Filtron rreshtat me Z-Score më të madh se pragu

# Funksioni për të zbuluar outliers për të gjitha kolonat e përcaktuara
def detect_outliers(df, columns, method="IQR", z_threshold=3):
    """
    Zbulon outliers për kolonat e specifikuara duke përdorur metodën e përzgjedhur.
    """
    outliers = pd.DataFrame()  # DataFrame për të ruajtur outliers
    for column in columns:
        if column not in df:
            print(f"Kolona {column} nuk ekziston në dataset. Po e kalojmë.")
            continue
        if method == "IQR":
            outliers_in_column = detect_outliers_iqr(df, column)  # Metoda IQR
        elif method == "Z-Score":
            outliers_in_column = detect_outliers_zscore(df, column, z_threshold)  # Metoda Z-Score
        else:
            raise ValueError("Metoda e pavlefshme. Zgjidhni 'IQR' ose 'Z-Score'.")
        
        outliers_in_column["Kolona Outlier"] = column  # Shton informacion për kolonën
        outliers = pd.concat([outliers, outliers_in_column])  # Shton outliers në DataFrame

    return outliers.drop_duplicates()  # Kthen outliers pa dublikime

# Funksioni kryesor për të ngarkuar të dhënat dhe zbuluar outliers
def main(file_path, method="IQR", z_threshold=3, output_path="outliers_detected.csv"):
    """
    Ngarkon të dhënat dhe zbulon outliers duke ruajtur rezultatet në një skedar CSV.
    """
    # Ngarkon të dhënat e përgatitura
    df = pd.read_csv(file_path)

    # Përcakton kolonat numerike që do të kontrollohen për outliers
    numerical_columns = ["Kapitali", "Numri i punëtorëve"]

    # Zbulon outliers
    outliers = detect_outliers(df, numerical_columns, method=method, z_threshold=z_threshold)

    # Ruaj outliers në një skedar CSV
    if not outliers.empty:
        outliers.to_csv(output_path, index=False)
        print(f"Outliers u zbuluan dhe u ruajtën në {output_path}")
    else:
        print("Nuk u zbuluan outliers.")

if __name__ == "__main__":

    input_file_path = "../data/processed/prepared_data.csv"
    output_file_path = "../data/processed/detected_outliers.csv"

    #IQR
    #main(input_file_path, method="IQR", output_path=output_file_path)

    #Z-Score
    main(input_file_path, method="Z-Score", z_threshold=3, output_path=output_file_path)
