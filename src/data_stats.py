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
def count_activities_from_processed_file(df, reverse_map):
    """Numëron numrin e bizneseve për secilin aktivitet unik nga DataFrame-i i përpunuar."""
    
    # Sheshojmë të gjitha aktivitetet e koduara dhe numërojmë përsëritjet
    all_encoded_activities = [activity for sublist in df['Aktivitetet Encoded'].apply(eval) for activity in sublist]
    activity_counts = pd.Series(all_encoded_activities).value_counts().reset_index()
    activity_counts.columns = ['Aktiviteti i koduar', 'Numri i bizneseve']
    
    # Kthejmë aktivitetet e koduara në emrat origjinalë
    activity_counts['Aktivitetet'] = activity_counts['Aktiviteti i koduar'].map(reverse_map)
    
    # Riorganizojmë kolonat dhe heqim kolonën 'Aktiviteti i koduar'
    activity_counts = activity_counts[['Aktivitetet', 'Numri i bizneseve']]
    
    return activity_counts

# Funksioni kryesor që ngarkon të dhënat dhe hartën, numëron bizneset sipas aktivitetit dhe shfaq rezultatin
def main(input_file_path, activity_map_path):
    # Ngarkojmë të dhënat
    df = load_data(input_file_path)
    
    # Ngarkojmë hartën e aktiviteteve
    reverse_map = load_activity_map(activity_map_path)
    
    # Numërojmë bizneset për secilin aktivitet
    activity_counts = count_activities_from_processed_file(df, reverse_map)
    
    # Shfaqim rezultatin
    print("Top 20 aktivitete sipas numrit të bizneseve:")
    print(activity_counts.head(20))

# Ekzekutimi i skriptit
if __name__ == "__main__":
    # Përkufizojmë shtigjet e skedarëve
    input_file_path = "../data/processed/prepared_data.csv"  # Rregulloni këtë shteg sipas vendndodhjes së të dhënave tuaja
    activity_map_path = "../data/processed/activity_map.jsonl"  # Sigurohuni që përputhet me skedarin tuaj JSONL

    main(input_file_path, activity_map_path)
