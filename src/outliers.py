import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Funksioni për të llogaritur Z-scores
def calculate_z_scores(column, z_threshold=3):
    """
    Llogarit Z-scores për një kolonë numerike dhe detekton outliers bazuar në pragun Z-score.
    """
    mean = column.mean()
    std = column.std()
    z_scores = (column - mean) / std
    return z_scores[np.abs(z_scores) > z_threshold]  # Kthen vetëm vlerat që tejkalojnë pragun

# Funksioni për të detektuar outliers me IQR (opsional)
def detect_outliers_iqr(column):
    """
    Detekton outliers duke përdorur metodën IQR (Interquartile Range).
    """
    q1 = column.quantile(0.25)
    q3 = column.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return column[(column < lower_bound) | (column > upper_bound)]

# Funksioni për të detektuar vlera me frekuencë të ulët
def detect_low_frequency_categorical(data, categorical_columns):
    """
    Detekton vlerat me frekuencë të ulët në kolonat kategorike.
    """
    anomalies = pd.DataFrame()
    print("\nKontroll për vlerat me frekuencë të ulët:")
    for col in categorical_columns:
        freq_counts = data[col].value_counts()
        low_freq_values = freq_counts[freq_counts < 2].index
        low_freq_data = data[data[col].isin(low_freq_values)]
        if not low_freq_data.empty:
            print(f"Frekuencë e ulët e gjetur në kolonën: {col}")
            for idx in low_freq_data.index:
                data.loc[idx, "Anomaly Details"] += f"Low frequency value in {col}: {data.loc[idx, col]}. "
                anomalies = pd.concat([anomalies, data.loc[[idx]]])
        else:
            print(f"Nuk u gjetën vlera me frekuencë të ulët në kolonën: {col}")
    return anomalies

# Funksioni për të vizualizuar kolonat numerike me dhe pa outliers
def visualize_outliers(data_before, data_after, numeric_columns):
    """
    Vizualizon kolonat numerike me dhe pa outliers duke shfaqur Boxplot, Violin Plot dhe Histogram.
    """
    for col in numeric_columns:
        print(f"\nVizualizime për kolonën: {col}")

        plt.figure(figsize=(18, 10))

        # Vizualizimi me outliers - Boxplot
        plt.subplot(2, 3, 1)
        sns.boxplot(data_before[col], orient="h", color="skyblue")
        plt.title(f"Boxplot me outliers për {col}")

        # Vizualizimi me outliers - Violin Plot
        plt.subplot(2, 3, 2)
        sns.violinplot(data_before[col], orient="h", color="lightgreen")
        plt.title(f"Violin Plot me outliers për {col}")

        # Vizualizimi me outliers - Histogram
        plt.subplot(2, 3, 3)
        sns.histplot(data_before[col], kde=True, bins=20, color="salmon")
        plt.title(f"Histogram me outliers për {col}")

        # Vizualizimi pa outliers - Boxplot
        plt.subplot(2, 3, 4)
        sns.boxplot(data_after[col], orient="h", color="skyblue")
        plt.title(f"Boxplot pa outliers për {col}")

        # Vizualizimi pa outliers - Violin Plot
        plt.subplot(2, 3, 5)
        sns.violinplot(data_after[col], orient="h", color="lightgreen")
        plt.title(f"Violin Plot pa outliers për {col}")

        # Vizualizimi pa outliers - Histogram
        plt.subplot(2, 3, 6)
        sns.histplot(data_after[col], kde=True, bins=20, color="salmon")
        plt.title(f"Histogram pa outliers për {col}")

        plt.tight_layout()
        plt.show()

# Funksioni për të detektuar datat e pavlefshme
def detect_invalid_dates(data, registration_col, closure_col):
    """
    Kontrollon për datat e pavlefshme (të ardhshme ose mungesa).
    """
    print("\nKontroll për datat e pavlefshme...")
    data[registration_col] = pd.to_datetime(data[registration_col], errors='coerce')
    data[closure_col] = pd.to_datetime(data[closure_col], errors='coerce')

    future_dates = data[
        (data[registration_col] > pd.Timestamp.now()) | 
        (data[closure_col] > pd.Timestamp.now())
    ]
    if not future_dates.empty:
        print(f"Numri i datave të ardhshme: {len(future_dates)}")
        print(f"Rreshtat me data të ardhshme:\n{future_dates[[registration_col, closure_col]]}")
        for idx in future_dates.index:
            if pd.notnull(future_dates.loc[idx, registration_col]):
                data.loc[idx, "Anomaly Details"] += "Future registration date. "
            if pd.notnull(future_dates.loc[idx, closure_col]):
                data.loc[idx, "Anomaly Details"] += "Future closure date. "
    else:
        print("Nuk ka data të pavlefshme.")
    return future_dates

# Funksioni për të detektuar anomalitë dhe ruajtur rezultatet
def detect_anomalies(data, numeric_columns, categorical_columns, z_threshold=3):
    """
    Detekton anomalitë në kolonat numerike dhe kategorike.
    """
    data["Anomaly Details"] = ""  # Kolona për të mbajtur detajet e anomalive
    anomalies = pd.DataFrame()

    # Detektojmë outliers në kolonat numerike me Z-score
    for col in numeric_columns:
        z_scores = calculate_z_scores(data[col].dropna(), z_threshold)
        if not z_scores.empty:
            for idx, zscore in z_scores.items():
                data.loc[idx, "Anomaly Details"] += f"Z-score outlier in {col} (Z={zscore:.2f}). "
                anomalies = pd.concat([anomalies, data.loc[[idx]]])

    # Detektojmë datat e pavlefshme
    detect_invalid_dates(data, "Data e regjistrimit", "Data e mbylljes")

    # Detektojmë vlera me frekuencë të ulët
    low_freq_anomalies = detect_low_frequency_categorical(data, categorical_columns)
    anomalies = pd.concat([anomalies, low_freq_anomalies])

    return anomalies

# Funksioni për të ruajtur anomalitë në file
def save_anomalies_to_file(anomalies, output_file_path):
    """
    Ruaj anomalitë e zbuluara në një file CSV.
    """
    if not anomalies.empty:
        anomalies.to_csv(output_file_path, index=False)
        print(f"\nAnomalitë u ruajtën në: {output_file_path}")
    else:
        print("\nNuk u gjetën anomalitë për t'u ruajtur.")

# Funksioni kryesor
def main(input_file_path, output_file_path, z_threshold=3):
    """
    Ngarkon dataset-in, kontrollon anomalitë dhe ruan rezultatet.
    """
    # Ngarkojmë dataset-in
    data = pd.read_csv(input_file_path)

    # Kolonat numerike dhe kategorike për analizë
    numeric_columns = ["Numri i punëtorëve", "Pronarë Mashkull", "Pronarë Femër"]
    categorical_columns = ["Statusi", "Tipi i biznesit", "Komuna"]

    # Ruaj dataset-in origjinal për krahasim
    original_data = data.copy()

    # Detektojmë anomalitë
    anomalies = detect_anomalies(data, numeric_columns, categorical_columns, z_threshold)

    # Heqim outliers nga të dhënat
    for col in numeric_columns:
        z_scores = (data[col] - data[col].mean()) / data[col].std()
        data = data[np.abs(z_scores) <= z_threshold]

    # Vizualizojmë të dhënat me dhe pa outliers
    visualize_outliers(original_data, data, numeric_columns)

    # Ruaj anomalitë në file
    save_anomalies_to_file(anomalies, output_file_path)


if __name__ == "__main__":
    input_file_path = "../data/processed/prepared_data.csv"
    output_file_path = "../data/processed/detected_outliers.csv"
    main(input_file_path, output_file_path, z_threshold=3)
