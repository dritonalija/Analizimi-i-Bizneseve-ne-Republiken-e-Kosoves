import pandas as pd
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Funksioni për të ngarkuar të dhënat nga një skedar CSV në një DataFrame të Pandas
def load_data(file_path):
    """Ngarkon të dhënat nga një skedar CSV në një DataFrame të Pandas."""
    if not os.path.exists(file_path):  # Kontrollojmë nëse skedari ekziston
        raise FileNotFoundError(f"Skedari nuk u gjet: {file_path}")
    return pd.read_csv(file_path)  # Lexojmë të dhënat nga skedari CSV

# Funksioni për të ngarkuar hartimet nga një skedar JSONL
def load_mapping(jsonl_file_path):
    """Ngarkon një hartë nga një skedar JSONL."""
    mapping = {}
    with open(jsonl_file_path, "r", encoding="utf-8") as file:
        for line in file:
            entry = json.loads(line.strip())
            mapping.update(entry)
    # Kthejmë çelësat në int nëse është e nevojshme
    mapping = {int(k): v for k, v in mapping.items()}
    return mapping

# Funksioni për të aplikuar hartimet në raport
def apply_mapping_to_column(df, column, mapping):
    """Apliko hartimet në një kolonë për të kthyer vlerat numerike në emra origjinalë."""
    if column in df.columns:
        df[column] = df[column].astype(int).map(mapping).fillna("I panjohur")
    return df

# Raportet bazë
def generate_business_type_report(df):
    """Gjeneron raportin për 'Tipi i biznesit'."""
    tipi_biznesit_report = df['Tipi i biznesit'].value_counts().reset_index()
    tipi_biznesit_report.columns = ['Tipi i biznesit', 'Numri i Bizneseve']
    return tipi_biznesit_report

def generate_municipality_report(df):
    """Gjeneron raportin për 'Komuna'."""
    komuna_report = df['Komuna'].value_counts().reset_index()
    komuna_report.columns = ['Komuna', 'Numri i Bizneseve']
    return komuna_report

def generate_status_report(df):
    """Gjeneron raportin për 'Statusi'."""
    statusi_report = df['Statusi'].value_counts().reset_index()
    statusi_report.columns = ['Statusi', 'Numri i Bizneseve']
    return statusi_report

def generate_activity_report(df):
    """Gjeneron raportin për 'Aktiviteti Primar'."""
    aktiviteti_report = df['Aktiviteti Primar'].value_counts().reset_index()
    aktiviteti_report.columns = ['Aktiviteti', 'Numri i Bizneseve']
    return aktiviteti_report

def gender_report(df):
    """Gjeneron raportin e ndarjes gjinore të pronarëve të bizneseve."""
    # Llogarit numrin total të pronarëve meshkuj dhe femra
    total_male_owners = df['Pronarë Mashkull'].sum()
    total_female_owners = df['Pronarë Femër'].sum()
    # Krijojmë një DataFrame për raportin
    gender_counts = pd.DataFrame({
        'Gjinia': ['Mashkull', 'Femër'],
        'Numri i Pronarëve': [total_male_owners, total_female_owners]
    })
    return gender_counts

# ===============================
# Statistika Avancuara
# ===============================

def advanced_analysis(df):
    # Filtrimi i bizneseve aktive (nëse 'Statusi' ka vlera si 'Aktiv')
    aktive = df[df['Statusi'] == 'Aktiv'].copy()

    # Sigurohuni që kolona 'Pronarë Femër' dhe 'Pronarë Mashkull' janë numerike
    aktive['Pronarë Femër'] = pd.to_numeric(aktive['Pronarë Femër'], errors='coerce').fillna(0)
    aktive['Pronarë Mashkull'] = pd.to_numeric(aktive['Pronarë Mashkull'], errors='coerce').fillna(0)

    # Analiza e Ndikimit Rajonal
    zhvillimi_komuna = aktive.groupby('Komuna').agg({
        'Emri i biznesit': 'count',
        'Numri i punëtorëve': 'mean'
    }).rename(columns={
        'Emri i biznesit': 'Numri i bizneseve aktive',
        'Numri i punëtorëve': 'Mesatarja e punëtorëve'
    })

    # Identifikimi i komunave me përqindje të lartë të bizneseve me pronare femra
    aktive['Femra Pronare'] = aktive['Pronarë Femër'] > 0
    femra_komuna = aktive.groupby('Komuna')['Femra Pronare'].mean() * 100

    # Raportet e Gjinive në Biznes:
    aktive['Femra Dominon'] = aktive['Pronarë Femër'] > aktive['Pronarë Mashkull']
    femra_dominon_per_sektor = aktive.groupby('Aktiviteti Primar')['Femra Dominon'].mean() * 100

    # Produktiviteti i bizneseve sipas pronësisë gjinore
    produktivitet = aktive.groupby('Femra Dominon')['Numri i punëtorëve'].mean()

    # Analiza e Diversifikimit të Bizneseve:
    sekondar_present = aktive['Aktiviteti Sekondar'].notna() & (aktive['Aktiviteti Sekondar'] != 0)
    perqindja_sekondar = sekondar_present.mean() * 100

    diversifikim = aktive.groupby(['Komuna', 'Aktiviteti Primar']).size().unstack(fill_value=0)

    # Përqendrimi i Punësimit
    punetore_primar = aktive.groupby('Aktiviteti Primar')['Numri i punëtorëve'].sum().sort_values(ascending=False)

    # Printime të statistikave
    print("\n--- Zhvillimi ekonomik i komunave ---")
    print(zhvillimi_komuna.head())

    print("\n--- Përqindja e bizneseve me pronare femra sipas komunës ---")
    print(femra_komuna.sort_values(ascending=False).head())

    print("\n--- Përqindja e sektorëve ku femra dominon ---")
    print(femra_dominon_per_sektor.sort_values(ascending=False).head())

    print("\n--- Produktiviteti mesatar i punëtorëve në bazë të dominimit gjinor ---")
    print(produktivitet)

    print(f"\nPërqindja e bizneseve me aktivitet sekondar: {perqindja_sekondar:.2f}%")

    print("\n--- Shpërndarja e punëtorëve sipas Aktivitetit Primar ---")
    print(punetore_primar.head())

    # Vizualizime shtesë:

    # Histogramë për Tipin e Biznesit (biznese aktive)
    plt.figure(figsize=(8,5))
    sns.countplot(y='Tipi i biznesit', data=aktive, order=aktive['Tipi i biznesit'].value_counts().index)
    plt.title("Numri i Bizneseve Aktive sipas Tipit")
    plt.xlabel("Frekuenca")
    plt.ylabel("Tipi i biznesit")
    plt.tight_layout()
    plt.show()

    # Grafikë Pie për Pronësinë Gjinore (biznese aktive)
    femra_count = (aktive['Pronarë Femër'] > 0).sum()
    mashkull_count = (aktive['Pronarë Mashkull'] > 0).sum()
    if femra_count == 0 and mashkull_count == 0:
        print("Nuk ka të dhëna për grafinë pie të pronësisë gjinore.")
    else:
        plt.figure(figsize=(6,6))
        plt.pie([femra_count, mashkull_count], labels=['Femra', 'Mashkull'], autopct='%1.1f%%')
        plt.title("Përqindja e Bizneseve Aktive sipas Pronësisë Gjinore")
        plt.show()

    

    # Bubble Chart për Komuna:
    data_komuna = aktive.groupby('Komuna').agg({
        'Emri i biznesit': 'count',
        'Numri i punëtorëve': 'sum'
    }).rename(columns={'Emri i biznesit':'Biznese','Numri i punëtorëve': 'Punetore'})

    plt.figure(figsize=(10,6))
    plt.scatter(data_komuna['Biznese'], data_komuna['Punetore'], s=data_komuna['Punetore']/5, alpha=0.6)
    for k,v in data_komuna.iterrows():
        plt.text(v['Biznese'], v['Punetore'], k, fontsize=8)
    plt.title('Përqendrimi i Punësimit dhe Bizneseve Aktive sipas Komunës')
    plt.xlabel("Numri i Bizneseve")
    plt.ylabel("Numri i Punëtorëve")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Konfiguroni opsionet e Pandas për të shfaqur emrat e plotë
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None) 

    input_file_path = "../data/processed/prepared_data.csv" 
    
    # Përcaktojmë shtigjet e skedarëve për hartimet
    mappings_files = {
        "Statusi": "../data/processed/Statusi_mapping.jsonl",
        "Tipi i biznesit": "../data/processed/Tipi i biznesit_mapping.jsonl",
        "Komuna": "../data/processed/Komuna_mapping.jsonl",
        "Aktivitetet": "../data/processed/activity_map.jsonl"
    }
    df = load_data(input_file_path)

    # Ngarkon hartimet nga skedarët JSONL
    mappings = {key: load_mapping(path) for key, path in mappings_files.items()}

    # Aplikon hartimet në kolonat për të kthyer vlerat numerike në emra origjinalë
    df = apply_mapping_to_column(df, 'Statusi', mappings['Statusi'])
    df = apply_mapping_to_column(df, 'Tipi i biznesit', mappings['Tipi i biznesit'])
    df = apply_mapping_to_column(df, 'Komuna', mappings['Komuna'])
    df = apply_mapping_to_column(df, 'Aktiviteti Primar', mappings['Aktivitetet'])

    # Gjeneron raportet bazë
    business_type_report = generate_business_type_report(df)
    municipality_report = generate_municipality_report(df)
    status_report = generate_status_report(df)
    activity_report = generate_activity_report(df)
    gender_counts = gender_report(df)

    # Afishon raportet përfundimtare me emra origjinalë
    print("Raporti mbi Tipet e Bizneseve:")
    print(business_type_report)
    print("\n")
    
    print("Raporti mbi Komunat:")
    print(municipality_report)
    print("\n")
    
    print("Raporti mbi Statusin e Bizneseve:")
    print(status_report)
    print("\n")
    
    print("Raporti mbi Aktivitetet Primare:")
    print(activity_report.head(20))
    print("\n")
    
    print("Raporti mbi ndarjen gjinore të pronarëve të bizneseve:")
    print(gender_counts)
    print("\n")

    # Thirrja e analizave avanacuara
    advanced_analysis(df)
