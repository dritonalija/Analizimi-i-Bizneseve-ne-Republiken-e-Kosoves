import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Funksioni për të llogaritur Z-scores dhe filtruar outliers
def filtro_pa_outliers(data, kolona, z_threshold=3):
    """
    Filtron të dhënat duke hequr outliers duke përdorur Z-score.
    """
    z_scores = (data[kolona] - data[kolona].mean()) / data[kolona].std()
    return data[np.abs(z_scores) <= z_threshold]  # Kthen të dhënat pa outliers

# Funksioni për të vizualizuar kolonën numerike me dhe pa outliers (me Square Root Transform)
def vizualizo_square_root(data, kolona, z_threshold=3):
    """
    Vizualizon kolonën numerike me dhe pa outliers duke përdorur Square Root Transform.
    """
    # Filtrimi i të dhënave pa outliers
    data_pa_outliers = filtro_pa_outliers(data, kolona, z_threshold)

    # Transformimi Square Root
    data_square_root = np.sqrt(data[kolona])
    data_pa_outliers_square_root = np.sqrt(data_pa_outliers[kolona])

    plt.figure(figsize=(18, 8))

    # Vizualizimi origjinal me outliers
    plt.subplot(1, 2, 1)
    sns.histplot(data_square_root, kde=True, bins=20, color="skyblue")
    plt.axvline(data_square_root.mean(), color='red', linestyle='--', label='Mesatarja')
    plt.title(f"Me Outliers - {kolona} (Square Root)\nSkewness: {data_square_root.skew():.2f}")
    plt.xlabel(f"{kolona} (Square Root)")
    plt.ylabel("Frekuenca")
    plt.legend()

    # Vizualizimi pa outliers
    plt.subplot(1, 2, 2)
    sns.histplot(data_pa_outliers_square_root, kde=True, bins=20, color="lightgreen")
    plt.axvline(data_pa_outliers_square_root.mean(), color='red', linestyle='--', label='Mesatarja')
    plt.title(f"Pa Outliers - {kolona} (Square Root)\nSkewness: {data_pa_outliers_square_root.skew():.2f}")
    plt.xlabel(f"{kolona} (Square Root)")
    plt.ylabel("Frekuenca")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Funksioni kryesor
def main(shtegu_input, z_threshold=3):
    """
    Ngarkon dataset-in dhe krijon vizualizime për Square Root Transform me dhe pa outliers.
    """
    # Ngarkojmë dataset-in
    data = pd.read_csv(shtegu_input)

    # Kombino "Pronarë Mashkull" dhe "Pronarë Femër" në një kolonë të vetme
    data["Numri i Pronarëve"] = data["Pronarë Mashkull"] + data["Pronarë Femër"]

    # Përcakto kolonat numerike për analizë
    kolonat_numerike = ["Numri i punëtorëve", "Numri i Pronarëve"]

    # Vizualizo të dhënat me Square Root Transform
    for kolona in kolonat_numerike:
        print(f"\nVizualizime për kolonën: {kolona}")
        vizualizo_square_root(data, kolona, z_threshold)

if __name__ == "__main__":
    shtegu_input = "../data/processed/prepared_data.csv"  # Zëvendëso me shtegun e dataset-it tënd
    main(shtegu_input, z_threshold=3)  # Mund të ndryshoni pragun Z-score këtu
