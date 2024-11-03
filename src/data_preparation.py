import pandas as pd
import numpy as np
import os
import re
import json
import gender_guesser.detector as gender
from nameparser import HumanName
from sklearn.preprocessing import LabelEncoder

# Inicializojmë detektuesin e gjinisë
d = gender.Detector()


# Funksioni për të ngarkuar të dhëna nga një skedar CSV në një DataFrame Pandas
def load_data(file_path):
    """Ngarkon të dhënat nga një skedar CSV në një DataFrame Pandas."""
    return pd.read_csv(file_path)


# Funksioni për të konvertuar kolonat në formatin e duhur të të dhënave
def datatype_format(df):
    """Kthen kolonat në formatin e duhur, duke definuar tipin e të dhënave."""
    df["Data e regjistrimit"] = pd.to_datetime(
        df["Data e regjistrimit"], errors="coerce"
    )
    df["Kapitali"] = pd.to_numeric(df["Kapitali"], errors="coerce")
    df["Numri i punëtorëve"] = pd.to_numeric(df["Numri i punëtorëve"], errors="coerce")
    return df


# Funksioni për të normalizuar 'Statusi' dhe për të nxjerrë datën në 'Data e mbylljes'
def normalize_status(df):
    """Normalizon vlerat specifike në kolonën 'Statusi' dhe nxjerr datat për kolonën 'Data e mbylljes'."""
    
    # Nxjerr datën nga vlerat si 'pasiv-DD/MM/YYYY' dhe e ruan në kolonën 'Data e mbylljes'
    df['Data e mbylljes'] = df['Statusi'].apply(
        lambda x: re.search(r"(?i)pasiv-(\d{2}/\d{2}/\d{4})", str(x)).group(1) if re.search(r"(?i)pasiv-\d{2}/\d{2}/\d{4}", str(x)) else None
    )
    
    # Konverton në formatin 'YYYY-MM-DD'
    df['Data e mbylljes'] = pd.to_datetime(df['Data e mbylljes'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Normalizon vlerat në kolonën 'Statusi'
    df["Statusi"] = df["Statusi"].replace(
        {r"(?i)pasiv.*": "Pasiv", r"(?i)anuluar nga sistemi": "Shuar"},
        regex=True
    )
    
    return df

# Funksioni për të përcaktuar gjininë bazuar në emrat duke përdorur gender_guesser
def detect_gender_gender_guesser(name):
    """Përcakton gjininë bazuar në emrin e parë."""
    first_name = HumanName(name).first
    guess = d.get_gender(first_name)
    if guess in ["male", "mostly_male"]:
        return "Mashkull"
    elif guess in ["female", "mostly_female"]:
        return "Femër"
    else:
        return "Panjohur"


# Funksioni për të përditësuar kolonën 'Gjinia e pronarit' duke deduktuar gjininë nga emrat
def update_gender_column(df):
    """Përditëson kolonën 'Gjinia e pronarit' për të ruajtur gjininë e deduktuar nga emrat."""

    def update_gender(row):
        if all(
            g.strip() == "Panjohur" for g in str(row["Gjinia e pronarit"]).split(",")
        ):
            return ", ".join(
                [
                    detect_gender_gender_guesser(name.strip())
                    for name in str(row["Pronarë"]).split(",")
                ]
            )
        return row["Gjinia e pronarit"]

    df["Gjinia e pronarit"] = df.apply(update_gender, axis=1)
    return df


# Funksioni për të numëruar përsëritjet e gjinive në kolonën 'Gjinia e pronarit'
def count_genders(df):
    """Krijon kolonat 'Pronarë Mashkull' dhe 'Pronarë Femër' për të numëruar përsëritjet në 'Gjinia e pronarit'."""
    df["Pronarë Mashkull"] = df["Gjinia e pronarit"].apply(
        lambda x: [g.strip() for g in str(x).split(",")].count("Mashkull")
    )
    df["Pronarë Femër"] = df["Gjinia e pronarit"].apply(
        lambda x: [g.strip() for g in str(x).split(",")].count("Femër")
    )
    return df


# Funksioni për të nxjerrë 'Uid' nga fundi i një lidhje për regjistrin
def extract_registry_number(df):
    """Krijon kolonën 'Uid' duke marrë pjesën e fundit të lidhjes dhe e kthen atë në numër të plotë."""
    df["Uid"] = df["Linku në ARBK"].apply(
        lambda x: (
            int(x.split(",")[-1])
            if pd.notnull(x) and x.split(",")[-1].isdigit()
            else None
        )
    )
    df["Uid"] = df["Uid"].astype("Int64")
    return df


# Funksioni për të mbushur vlerat e panjohura në kolonën 'Tipi i biznesit'
def fill_business_type(df):
    """Mbush vlerat që mungojnë në 'Tipi i biznesit' bazuar në prapashtesën e 'Emri i biznesit'."""

    def get_business_type(row):
        if pd.isna(row["Tipi i biznesit"]):
            if row["Emri i biznesit"].endswith("B.I."):
                return "Biznes individual"
            elif row["Emri i biznesit"].endswith(("SH.P.K.", "L.L.C.")):
                return "Shoqëri me përgjegjësi të kufizuara"
            elif row["Emri i biznesit"].endswith("K.B."):
                return "Kooperativa Bujqësore"
            elif row["Emri i biznesit"].endswith("N.SH."):
                return "Ndërmarrje shoqërore"
            elif row["Emri i biznesit"].endswith("O.K."):
                return "Ortakëri e kufizuar"
            elif row["Emri i biznesit"].endswith("O.P."):
                return "Ortakëri e përgjithshme"
            elif row["Emri i biznesit"].endswith("SH.A."):
                return "Shoqëri aksionare"
            elif row["Emri i biznesit"].endswith("Z.P.K."):
                return "Zyra e Përfaqësisë në Kosovë"
        return row["Tipi i biznesit"]

    df["Tipi i biznesit"] = df.apply(get_business_type, axis=1)
    return df


def encode_aktivitetet(df):
    """Encode the 'Aktivitetet' field by splitting by newline and applying label encoding."""

    # Split 'Aktivitetet' by newline and handle NaN values by converting them to empty lists
    df["Aktivitetet"] = df["Aktivitetet"].fillna("").str.split(r"\n")

    # Flatten all activities to get a list of unique activities, stripping extra spaces and any trailing commas
    all_activities = [
        activity.strip().rstrip(",")
        for sublist in df["Aktivitetet"]
        for activity in sublist
        if activity.strip()
    ]
    unique_activities = pd.Series(all_activities).unique()

    # Label encode unique activities
    label_encoder = LabelEncoder()
    label_encoder.fit(unique_activities)

    # Save mapping as newline-separated JSON
    activity_map = {
        activity: int(label)
        for activity, label in zip(
            unique_activities, label_encoder.transform(unique_activities)
        )
    }
    output_path = "../data/processed/activity_map.jsonl"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
        for activity, label in activity_map.items():
            json.dump({activity: label}, file)
            file.write("\n")

    # Encode each row's 'Aktivitetet' field and store as a list of integers
    def encode_activities(activity_list):
        # Ensure activity_list is a list before encoding
        return [
            activity_map[activity.strip().rstrip(",")]
            for activity in activity_list
            if activity.strip()
        ]

    # Apply encoding to each row
    df["Aktivitetet Encoded"] = df["Aktivitetet"].apply(encode_activities)

    return df

# Funksioni për të koduar kolona dhe për të ruajtur hartimet unike në një skedar JSONL
def encode_columns(df, columns, output_dir="../data/processed"):
    """Kodon kolonat e specifikuara me LabelEncoder dhe ruan hartimet unike në një skedar JSONL."""
    os.makedirs(output_dir, exist_ok=True)  # Siguro që ekziston direktoria e daljes

    for column in columns:
        # Kodo kolonën me LabelEncoder
        label_encoder = LabelEncoder()
        df[column] = label_encoder.fit_transform(df[column])

        # Përkufizo shtegun e skedarit JSONL për këtë kolonë
        jsonl_file_path = os.path.join(output_dir, f"{column}_mapping.jsonl")

        # Merr hartimet unike për kolonën aktuale
        unique_mappings = {int(label): class_name for label, class_name in zip(label_encoder.transform(label_encoder.classes_), label_encoder.classes_)}

        # Shkruaj të gjitha hartimet unike në skedarin JSONL
        with open(jsonl_file_path, "w") as file:
            for label, class_name in unique_mappings.items():
                json_line = json.dumps({label: class_name})
                file.write(json_line + "\n")
        print(f"Hartimet për '{column}' janë ruajtur në {jsonl_file_path}")

    return df

# Funksioni për të hequr rreshtat e dyfishtë bazuar në kolonën 'Uid'
def remove_duplicates(df):
    """Heq rreshtat e dyfishtë bazuar në kolonën 'Uid'."""
    return df.drop_duplicates(subset="Uid", keep="first")


def handle_missing_values(df):
    """Trajton vlerat që mungojnë me strategji të specifikuara."""
    df.fillna({"Numri i punëtorëve": 0, "Kapitali": 0}, inplace=True)
    return df


# Funksioni për të ruajtur të dhënat e përpunuara në një skedar CSV
def save_data(df, output_path):
    """Ruaj të dhënat e përpunuara në një skedar CSV."""
    df.to_csv(output_path, index=False)
    print(f"Të dhënat e përpunuara janë ruajtur në '{output_path}'")


# Funksioni kryesor për përpunimin e të dhënave
def preprocess_data(file_path, output_path):
    """Përpunim i plotë i të dhënave."""
    df = load_data(file_path)
    df = extract_registry_number(df)
    df = remove_duplicates(df)
    df = datatype_format(df)
    df = normalize_status(df)
    df = update_gender_column(df)
    df = count_genders(df)
    df = fill_business_type(df)
    df = handle_missing_values(df)
    df = encode_aktivitetet(df)
    df = encode_columns(df, ["Statusi", "Tipi i biznesit", "Komuna"])

    # Heq kolonat e panevojshme. Redukton dimensionin e të dhënave
    df = df[
        [
            "Emri i biznesit",
            "Statusi",
            "Tipi i biznesit",
            "Data e regjistrimit",
            "Data e mbylljes",
            "Komuna",
            "Kapitali",
            "Numri i punëtorëve",
            "Pronarë Mashkull",
            "Pronarë Femër",
            "Aktivitetet Encoded",
        ]
    ]

    save_data(df, output_path)


# Ekzekutimi kryesor i skriptit
if __name__ == "__main__":
    # Përkufizon shtegun e skedarëve
    input_file_path = "../data/raw/data.csv"
    output_file_path = "../data/processed/prepared_data.csv"

    # Sigurohet që direktoria 'processed' ekziston
    os.makedirs("../data/processed", exist_ok=True)

    # Ekzekuton përpunimin e të dhënave
    preprocess_data(input_file_path, output_file_path)
