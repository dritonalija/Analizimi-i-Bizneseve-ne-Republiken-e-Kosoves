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
    df["Numri i punëtorëve"] = pd.to_numeric(df["Numri i punëtorëve"], errors="coerce")
    return df


# Funksioni për të normalizuar 'Statusi' dhe për të nxjerrë datën në 'Data e mbylljes'
def normalize_status(df):
    """Normalizon vlerat specifike në kolonën 'Statusi' dhe nxjerr datat për kolonën 'Data e mbylljes'."""
    df["Data e mbylljes"] = pd.to_datetime(
        df["Statusi"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0],
        format="%d/%m/%Y",
        errors="coerce",
    )
    df["Statusi"] = df["Statusi"].replace(
        {r"(?i)pasiv.*": "Pasiv", r"(?i)anuluar nga sistemi": "Shuar"}, regex=True
    )
    return df


# Funksioni për të përcaktuar gjininë bazuar në emrat duke përdorur gender_guesser me strategji rezervë
def gender_guesser(name):
    """Përcakton gjininë bazuar në emrin e parë duke përdorur gender_guesser dhe heuristikë për fundoret e emrave."""
    # Marrim vetëm emrin e parë
    first_name = name.strip().split()[0] if name.strip() else ""

    # Përdorim librarinë gender_guesser fillimisht
    guess = d.get_gender(HumanName(first_name).first)
    if guess in ["male", "mostly_male"]:
        return "Mashkull"
    elif guess in ["female", "mostly_female"]:
        return "Femër"
    else:
        # Strategjia rezervë bazuar në fundoret e emrave shqiptarë
        first_name = first_name.lower()
        if first_name.endswith(('a', 'e', 'ë', 'ja')):
            return "Femër"
        else:
            return "Mashkull"


# Funksioni për të përditësuar kolonën 'Gjinia e pronarit' duke deduktuar gjininë nga emrat
def update_gender_column(df):
    """Përditëson kolonën 'Gjinia e pronarit' për të ruajtur gjininë e deduktuar nga emrat."""
    df["Gjinia e pronarit"] = df.apply(
        lambda row: (
            ", ".join(
                gender_guesser(name.strip())
                for name in str(row["Pronarë"]).split(",")
            )
            if "Panjohur" in str(row["Gjinia e pronarit"])
            else row["Gjinia e pronarit"]
        ),
        axis=1,
    )
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
    df["Uid"] = (
        df["Linku në ARBK"]
        .str.split(",")
        .str[-1]
        .apply(lambda x: int(x) if pd.notnull(x) and x.isdigit() else None)
        .astype("Int64")
    )
    return df


# Funksioni për të mbushur vlerat e panjohura në kolonën 'Tipi i biznesit'
def fill_business_type(df):
    """Mbush 'Tipi i biznesit' bazuar në emrin e biznesit."""
    type_map = {
        "B.I.": "Biznes individual",
        "SH.P.K.": "Shoqëri me përgjegjësi të kufizuara",
        "L.L.C.": "Shoqëri me përgjegjësi të kufizuara",
        "K.B.": "Kooperativa Bujqësore",
        "N.SH.": "Ndërmarrje shoqërore",
        "O.K.": "Ortakëri e kufizuar",
        "O.P.": "Ortakëri e përgjithshme",
        "SH.A.": "Shoqëri aksionare",
        "Z.P.K.": "Zyra e Përfaqësisë në Kosovë",
    }
    df["Tipi i biznesit"] = df.apply(
        lambda row: next(
            (v for k, v in type_map.items() if row["Emri i biznesit"].endswith(k)),
            row["Tipi i biznesit"],
        ),
        axis=1,
    )
    return df

def split_aktivitetet(df):
    """Krijon kolonat 'Aktiviteti Primar' dhe 'Aktiviteti Sekondar' nga kolona 'Aktivitetet' dhe heq presjet në fund."""
    # Sigurojmë që 'Aktivitetet' është një listë
    df["Aktivitetet"] = df["Aktivitetet"].fillna("").str.split(r"\n")

    # Nxjerrim aktivitetin primar dhe sekondar, duke hequr presjet nga fundi
    df["Aktiviteti Primar"] = df["Aktivitetet"].apply(
        lambda x: x[0].strip().rstrip(",") if len(x) > 0 and x[0].strip() else None
    )
    df["Aktiviteti Sekondar"] = df["Aktivitetet"].apply(
        lambda x: x[1].strip().rstrip(",") if len(x) > 1 and x[1].strip() else None
    )

    return df

def encode_aktivitetet_categories(df):
    """Encodes 'Aktiviteti Primar' and 'Aktiviteti Sekondar' into categories and saves in JSONL format."""
    # Use LabelEncoder for each column
    le_primar = LabelEncoder()

    # Combine values from both columns to ensure consistent encoding
    all_activities = pd.concat([df["Aktiviteti Primar"], df["Aktiviteti Sekondar"]]).fillna("Unknown").unique()

    # Fit the LabelEncoder with all unique activities
    le_primar.fit(all_activities)

    # Fill missing values with "Unknown" before encoding
    df["Aktiviteti Primar"] = le_primar.transform(df["Aktiviteti Primar"].fillna("Unknown"))
    df["Aktiviteti Sekondar"] = le_primar.transform(df["Aktiviteti Sekondar"].fillna("Unknown"))

    # Save mappings in JSONL format
    jsonl_path = "../data/processed/activity_map.jsonl"
    os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)

    with open(jsonl_path, "w", encoding="utf-8") as file:
        for index, label in enumerate(le_primar.classes_):
            json_line = json.dumps({index: label}, ensure_ascii=False)
            file.write(json_line + "\n")

    print(f"Activities have been encoded and mappings saved in '{jsonl_path}'.")
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

# Funksion për të zëvendësuar 'Komuna' në datasetin kryesor
def fill_komuna(main_df, secondary_csv_path):
    """Përditëson kolonën 'Komuna' kur është 'I panjohur' duke përdorur të dhënat nga një CSV tjetër."""
    arbk_df = pd.read_csv(secondary_csv_path)

    # Konvertojmë kolonat për krahasim
    main_df["Uid"] = main_df["Uid"].astype(str)
    arbk_df["nRegjistriID"] = arbk_df["nRegjistriID"].astype(str)

    # Për të gjitha rreshtat ku `Komuna` është "I panjohur"
    for index, row in main_df.iterrows():
        if row["Komuna"] == "I panjohur":
            # Kontrollojmë në datasetin tjetër nëse ekziston `nRegjistriID` i njëjtë me `Uid`
            matching_row = arbk_df[arbk_df["nRegjistriID"] == row["Uid"]]
            if not matching_row.empty:
                # Marrim vlerën `Komuna` nga dataset-i tjetër
                new_komuna = matching_row.iloc[0]["Komuna"]
                # Përditësojmë kolonën `Komuna` në datasetin fillestar
                main_df.at[index, "Komuna"] = new_komuna
    return main_df


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
        unique_mappings = {
            int(label): class_name
            for label, class_name in zip(
                label_encoder.transform(label_encoder.classes_), label_encoder.classes_
            )
        }

        # Shkruaj të gjitha hartimet unike në skedarin JSONL
        with open(jsonl_file_path, "w") as file:
            for label, class_name in unique_mappings.items():
                json_line = json.dumps({label: class_name})
                file.write(json_line + "\n")
        print(f"Hartimet për '{column}' janë ruajtur në {jsonl_file_path}")

    return df


def preprocess_data(file_path,arbk_csv_path, output_path):
    """Përpunimi i të dhënave për finalizim."""
    df = (
        load_data(file_path)
        .pipe(extract_registry_number)
        .drop_duplicates("Uid")
        .pipe(datatype_format)
        .pipe(normalize_status)
        .pipe(update_gender_column)
        .pipe(count_genders)
        .pipe(fill_business_type)
        .fillna({"Numri i punëtorëve": 0})
        .pipe(split_aktivitetet)
        #.pipe(encode_aktivitetet_categories)
        #.pipe(fill_komuna, arbk_csv_path) # perdoret atehere kur marrim te dhena nga Crawleri
       # .pipe(encode_columns, ["Statusi", "Tipi i biznesit", "Komuna"])
       [
            [   'Uid',
                "Emri i biznesit",
                "Statusi",
                "Tipi i biznesit",
                "Data e regjistrimit",
                "Data e mbylljes",
                "Komuna",
                "Numri i punëtorëve",
                "Pronarë Mashkull",
                "Pronarë Femër",
                "Aktiviteti Primar",
            ]
        ]
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Të dhënat e përpunuara janë ruajtur në '{output_path}'")


# Ekzekutimi kryesor i skriptit
if __name__ == "__main__":
    # Përkufizon shtegun e skedarëve
    input_file_path = "../data/raw/data.csv"
    arbk_csv_path = "../data/raw/arbk_crawler_data.csv"  # Dataseti i ARBK me detajet e biznesit nga crawler-i
    output_file_path = "../data/processed/prepared_data_tableau.csv"

    # Sigurohet që direktoria 'processed' ekziston
    os.makedirs("../data/processed", exist_ok=True)

    # Ekzekuton përpunimin e të dhënave
    preprocess_data(input_file_path,arbk_csv_path, output_file_path)
