import pandas as pd
import json
import os

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

# Funksioni për të krijuar raportin për 'Tipi i biznesit' me vlera numerike
def generate_business_type_report(df):
    """Gjeneron raportin për 'Tipi i biznesit' me vlera numerike."""
    tipi_biznesit_report = df['Tipi i biznesit'].value_counts().reset_index()
    tipi_biznesit_report.columns = ['Tipi i biznesit', 'Numri i Bizneseve']
    return tipi_biznesit_report

# Funksioni për të krijuar raportin për 'Komuna' me vlera numerike
def generate_municipality_report(df):
    """Gjeneron raportin për 'Komuna' me vlera numerike."""
    komuna_report = df['Komuna'].value_counts().reset_index()
    komuna_report.columns = ['Komuna', 'Numri i Bizneseve']
    return komuna_report

# Funksioni për të krijuar raportin për 'Statusi' me vlera numerike
def generate_status_report(df):
    """Gjeneron raportin për 'Statusi' me vlera numerike."""
    statusi_report = df['Statusi'].value_counts().reset_index()
    statusi_report.columns = ['Statusi', 'Numri i Bizneseve']
    return statusi_report

# Funksioni për të krijuar raportin për 'Aktiviteti Primar' me vlera numerike
def generate_activity_report(df):
    """Gjeneron raportin për 'Aktiviteti Primar' me vlera numerike."""
    aktiviteti_report = df['Aktiviteti Primar'].value_counts().reset_index()
    aktiviteti_report.columns = ['Aktiviteti', 'Numri i Bizneseve']
    return aktiviteti_report

# Funksioni për të gjeneruar raportin e ndarjes gjinore të pronarëve të bizneseve
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

# Ekzekutimi i skriptit
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

    # Gjeneron raportet me vlera të përpunuara
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
