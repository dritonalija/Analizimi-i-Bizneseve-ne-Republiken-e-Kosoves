import pandas as pd
import json
import os
from sklearn.preprocessing import LabelEncoder

# Funksioni për të ngarkuar të dhënat nga një skedar CSV në një DataFrame të Pandas
def load_data(file_path):
    """Ngarkon të dhënat nga një skedar CSV në një DataFrame të Pandas."""
    if not os.path.exists(file_path):  # Kontrollojmë nëse skedari ekziston
        raise FileNotFoundError(f"Skedari nuk u gjet: {file_path}")
    return pd.read_csv(file_path)  # Lexojmë të dhënat nga skedari CSV

# Funksioni për të ngarkuar hartën e aktiviteteve nga një skedar JSONL dhe e përmbys për dekodim
def load_activity_map(file_path):
    """Ngarkon hartën e aktiviteteve nga një skedar JSONL dhe e përmbys për dekodim."""
    if not os.path.exists(file_path):  # Kontrollojmë nëse skedari ekziston
        raise FileNotFoundError(f"Skedari nuk u gjet: {file_path}")
    
    activity_map = {}
    with open(file_path, 'r') as file:
        for line in file:
            activity = json.loads(line)  # Lexojmë çdo linjë JSON dhe e dekodojmë në një diktor
            activity_map.update(activity)  # Përditësojmë hartën e aktiviteteve
    
    # Kthejmë hartën për të marrë emrat e aktiviteteve nga etiketat
    reverse_map = {v: k for k, v in activity_map.items()}
    return reverse_map

# Funksioni për të numëruar bizneset për secilin aktivitet unik nga DataFrame-i i përpunuar
def count_activities_from_processed_file(df):
    """Numëron numrin e bizneseve për secilin aktivitet unik nga DataFrame-i i përpunuar."""
    
    # Sheshojmë të gjitha aktivitetet e koduara dhe numërojmë përsëritjet
    all_encoded_activities = [activity for sublist in df['Aktivitetet Encoded'].apply(eval) for activity in sublist]
    activity_counts = pd.Series(all_encoded_activities).value_counts().reset_index()
    activity_counts.columns = ['Aktiviteti i koduar', 'Numri i bizneseve']
    
    return activity_counts

# Funksioni për të aplikuar hartën e aktiviteteve dhe për të kthyer emrat origjinalë në raportin përfundimtar
def apply_activity_mapping(activity_counts, reverse_map):
    """Aplikon hartën e aktiviteteve për të kthyer vlerat e koduara në emra origjinalë në raportin e aktiviteteve."""
    # Kthejmë aktivitetet e koduara në emrat origjinalë
    activity_counts['Aktivitetet'] = activity_counts['Aktiviteti i koduar'].map(reverse_map)
    
    # Riorganizojmë kolonat dhe heqim kolonën 'Aktiviteti i koduar'
    activity_counts = activity_counts[['Aktivitetet', 'Numri i bizneseve']]
    return activity_counts

# Funksioni kryesor që ngarkon të dhënat dhe hartën, numëron bizneset sipas aktivitetit dhe shfaq rezultatin
def activity_report(df, activity_map_path):
    """Gjeneron raportin e aktiviteteve dhe aplikon hartën në fund për të kthyer emrat e aktiviteteve."""
    
    # Gjeneron raportin e aktiviteteve me vlera numerike
    activity_counts = count_activities_from_processed_file(df)
    
    # Ngarkojmë hartën e aktiviteteve
    reverse_map = load_activity_map(activity_map_path)
    
    # Aplikojmë hartën për të kthyer aktivitetet në emra
    activity_counts = apply_activity_mapping(activity_counts, reverse_map)
    
    # Shfaqim rezultatin
    print("Top 20 aktivitete sipas numrit të bizneseve:")
    print(activity_counts.head(20))

# Funksioni për të ngarkuar hartimet nga një skedar JSONL
def load_mapping(jsonl_file_path):
    """Ngarkon një hartë nga një skedar JSONL."""
    mapping = {}
    with open(jsonl_file_path, "r") as file:
        for line in file:
            entry = json.loads(line.strip())
            mapping.update(entry)
    # Sigurohemi që të gjitha çelësat janë të tipit int
    mapping = {int(k): v for k, v in mapping.items()}
    return mapping

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


# Funksioni për të aplikuar hartimet në raport
def apply_mapping_to_report(report, column, mapping):
    """Apliko hartimet në raport për të kthyer vlerat numerike në emra origjinalë."""
    # Konverton vlerat në int në rast se janë të tipit të ndryshëm
    report[column] = report[column].astype(int)
    report[column] = report[column].map(mapping)
    return report

# Ekzekutimi i skriptit
if __name__ == "__main__":
    # Përkufizojmë shtigjet e skedarëve
    input_file_path = "../data/processed/prepared_data.csv"  # Rregulloni këtë shteg sipas vendndodhjes së të dhënave tuaja
    activity_map_path = "../data/processed/activity_map.jsonl"  # Sigurohuni që përputhet me skedarin tuaj JSONL
    
    # Ngarkojmë të dhënat
    df = load_data(input_file_path)

    # Gjeneron raportin e aktiviteteve
    activity_report(df, activity_map_path)
    
    # Ngarkon hartimet nga skedarët JSONL për 'Statusi', 'Tipi i biznesit' dhe 'Komuna'
    mappings = {
        "Statusi": load_mapping("../data/processed/Statusi_mapping.jsonl"),
        "Tipi i biznesit": load_mapping("../data/processed/Tipi i biznesit_mapping.jsonl"),
        "Komuna": load_mapping("../data/processed/Komuna_mapping.jsonl"),
    }
    
    # Ngarkon hartimet nga skedarët JSONL për 'Statusi', 'Tipi i biznesit' dhe 'Komuna'
    mappings = {
        "Statusi": load_mapping("../data/processed/Statusi_mapping.jsonl"),
        "Tipi i biznesit": load_mapping("../data/processed/Tipi i biznesit_mapping.jsonl"),
        "Komuna": load_mapping("../data/processed/Komuna_mapping.jsonl"),
    }

    # Gjeneron raportet me vlera numerike
    business_type_report = generate_business_type_report(df)
    municipality_report = generate_municipality_report(df)
    status_report = generate_status_report(df)
    # Gjeneron raportin e ndarjes gjinore të pronarëve të bizneseve
    gender_counts = gender_report(df)

    # Aplikon hartimet për të kthyer vlerat numerike në emrat origjinalë
    business_type_report = apply_mapping_to_report(business_type_report, 'Tipi i biznesit', mappings["Tipi i biznesit"])
    municipality_report = apply_mapping_to_report(municipality_report, 'Komuna', mappings["Komuna"])
    status_report = apply_mapping_to_report(status_report, 'Statusi', mappings["Statusi"])

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
    
    # Afishon raportin e ndarjes gjinore
    print("Raporti i ndarjes gjinore të pronarëve të bizneseve:")
    print(gender_counts)
    print("\n")
