import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Funksioni për të ngarkuar të dhënat nga një skedar CSV në një DataFrame të Pandas
def load_data(file_path):
    """Ngarkon të dhënat nga një skedar CSV në një DataFrame të Pandas."""
    if not os.path.exists(file_path):  # Kontrollojmë nëse skedari ekziston
        raise FileNotFoundError(f"Skedari nuk u gjet: {file_path}")
    return pd.read_csv(file_path)  # Lexojmë të dhënat nga skedari CSV

# Funksioni për të krijuar matricën e korrelacionit për kolona të zgjedhura
def create_correlation_matrix(df, selected_columns=None):
    """Krijon matricën e korrelacionit për kolonat e zgjedhura në DataFrame."""
    if selected_columns is not None:
        df = df[selected_columns]  # Përdorim vetëm kolonat e specifikuara
    return df.corr()  # Llogarit matricën e korrelacionit për kolonat e përzgjedhura

# Funksioni për të vizualizuar matricën e korrelacionit
def plot_correlation_matrix(correlation_matrix):
    """Vizualizon matricën e korrelacionit."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Matrica e Korrelacionit")
    plt.show()

# Ekzekutimi i skriptit për shembull
if __name__ == "__main__":
    # Përkufizoni shtigjin e skedarit tuaj CSV
    input_file_path = "../data/processed/prepared_data.csv"  # Ndryshoni këtë me shtigjin e skedarit tuaj CSV
    
    # Ngarkojmë të dhënat
    df = load_data(input_file_path)
    
    # Specifikoni kolonat që dëshironi të përfshini në analizën e korrelacionit
    selected_columns = ['Statusi','Tipi i biznesit','Komuna','Kapitali','Numri i punëtorëve'] 
    
    # Krijojmë matricën e korrelacionit për kolonat e zgjedhura dhe e vizualizojmë
    correlation_matrix = create_correlation_matrix(df, selected_columns)
    plot_correlation_matrix(correlation_matrix)
