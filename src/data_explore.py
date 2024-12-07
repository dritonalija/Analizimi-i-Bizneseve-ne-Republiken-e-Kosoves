import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Funksioni për të ngarkuar JSONL si fjalor
def load_jsonl_to_dict(file_path):
    """
    Ngarkon një skedar JSONL dhe e konverton në fjalor.
    """
    data_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            entry = json.loads(line.strip())
            data_dict.update(entry)
    return data_dict

# Funksioni për të aplikuar mappings në dataset
def map_codes(data, column, mapping_dict):
    """
    Apliko hartimet në një kolonë të dataset-it për të kthyer kodet në emra.
    """
    data[column] = data[column].map(mapping_dict)
    return data

# Funksioni për të eksploruar të dhënat me emrat e mapped
def explore_data(data, mappings):
    """
    Bën eksplorimin e të dhënave duke përdorur emrat e mapped.
    """
    
    print("Statistika permbledhese:")
    print(data.describe())
   
    # Konverto kolonat në string për të përputhur me JSONL mappings
    for col in mappings.keys():
        data[col] = data[col].astype(str)

    # Aplikimi i mappings
    data = map_codes(data, "Komuna", mappings["Komuna"])
    data = map_codes(data, "Tipi i biznesit", mappings["Tipi i biznesit"])
    data = map_codes(data, "Statusi", mappings["Statusi"])

    # Tregojmë numërimet për çdo kategori
    print("\nNumërimet për kategori:")
    for col in ["Komuna", "Tipi i biznesit", "Statusi"]:
        print(f"{data[col].value_counts()}\n")

    # Vizualizime për kategoritë
    print("\nVizualizime për kategoritë:")
    nominal_columns = ["Komuna", "Tipi i biznesit", "Statusi"]
    for col in nominal_columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(y=data[col], order=data[col].value_counts().index)
        plt.title(f"Shpërndarja e {col}")
        plt.xlabel("Frekuenca")
        plt.ylabel(col)
        plt.show()

    # Kombino "Pronarë Mashkull" dhe "Pronarë Femër"
    data["Total Pronarë"] = data["Pronarë Mashkull"] + data["Pronarë Femër"]

    # Vizualizime për kolonat numerike
    print("\nVizualizime për kolonat numerike:")
    numeric_columns = ["Numri i punëtorëve", "Pronarë Mashkull", "Pronarë Femër", "Total Pronarë"]
    for col in numeric_columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(data[col], kde=True, bins=20)
        plt.title(f"Shpërndarja e {col}")
        plt.xlabel(col)
        plt.ylabel("Frekuenca")
        plt.show()

# Funksioni kryesor
def main(input_file_path, mapping_paths):
    """
    Ngarkon dataset-in dhe mappings, dhe bën eksplorimin e të dhënave.
    """
    # Ngarkojmë dataset-in
    data = pd.read_csv(input_file_path)

    # Ngarkojmë mappings
    mappings = {key: load_jsonl_to_dict(path) for key, path in mapping_paths.items()}

    # Eksplorojmë të dhënat
    explore_data(data, mappings)

if __name__ == "__main__":
    input_file_path = "../data/processed/prepared_data.csv"
    mapping_paths = {
        "Komuna": "../data/processed/Komuna_mapping.jsonl",
        "Tipi i biznesit": "../data/processed/Tipi i biznesit_mapping.jsonl",
        "Statusi": "../data/processed/Statusi_mapping.jsonl",
    }

    main(input_file_path, mapping_paths)
