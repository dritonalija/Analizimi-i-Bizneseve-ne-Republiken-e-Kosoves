import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Funksioni për të bashkuar kolonat Pronarë Mashkull dhe Femër
def merge_pronare_columns(df):
    """
    Bashkon kolonat 'Pronarë Mashkull' dhe 'Pronarë Femër' në një kolonë të vetme 'Pronarë',
    duke llogaritur numrin total të pronarëve.
    """
    if "Pronarë Mashkull" in df.columns and "Pronarë Femër" in df.columns:
        # Krijo një kolonë të re 'Pronarë' duke mbledhur dy kolonat
        df["Pronarë"] = df["Pronarë Mashkull"] + df["Pronarë Femër"]
        # Fshin kolonat ekzistuese
        df = df.drop(columns=["Pronarë Mashkull", "Pronarë Femër"])
    else:
        print("Kolonat 'Pronarë Mashkull' dhe/ose 'Pronarë Femër' nuk u gjetën.")
    return df

# Funksioni për të vizualizuar të dhënat
def visualize_data(df):
    """
    Vizualizon të dhënat numerike me grafika të ndryshme, duke përfshirë boxplot, histogram dhe scatterplot.
    """
    numerical_columns = ["Kapitali", "Numri i punëtorëve", "Pronarë"]
    for column in numerical_columns:
        if column not in df.columns:
            print(f"Kolona '{column}' nuk u gjet në dataset.")
            continue
        
        # Boxplot për të identifikuar outliers
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df[column])
        plt.title(f"Boxplot për {column}")
        plt.xlabel(column)
        plt.show()
        
        # Histogram për shpërndarjen e të dhënave
        plt.figure(figsize=(8, 6))
        sns.histplot(df[column], bins=30, kde=True)
        plt.title(f"Histogram për {column}")
        plt.xlabel(column)
        plt.ylabel("Frekuenca")
        plt.show()

    # Scatterplot për Kapitali vs Numri i punëtorëve
    if "Kapitali" in df.columns and "Numri i punëtorëve" in df.columns:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df["Kapitali"], y=df["Numri i punëtorëve"])
        plt.title("Scatterplot: Kapitali vs Numri i punëtorëve")
        plt.xlabel("Kapitali")
        plt.ylabel("Numri i punëtorëve")
        plt.show()

if __name__ == "__main__":
    file_path = "../data/processed/prepared_data.csv"
    df = pd.read_csv(file_path)

    df = merge_pronare_columns(df)

    visualize_data(df)
