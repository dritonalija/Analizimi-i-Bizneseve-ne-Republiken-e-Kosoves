import pandas as pd

# Funksioni për të analizuar një skedar CSV dhe kthimin e statistikave të ndryshme
def analyze_csv(file_path, unique_columns=None):
    # Ngarkoni skedarin CSV në një DataFrame
    df = pd.read_csv(file_path)

    # Numri i rreshtave dhe kolonave
    row_count, column_count = df.shape

    # Llojet e të dhënave për secilën kolonë
    data_types = df.dtypes

    # Vlerat unike për kolona specifike
    unique_values = {}
    if unique_columns:
        for column in unique_columns:
            if column in df.columns:
                unique_values[column] = df[column].unique()
            else:
                print(f"Paralajmërim: Kolona '{column}' nuk u gjet në dataset.")

    # Vlerat Null për kolonë (përfshirë kolonat me zero vlera null)
    null_values = df.isnull().sum()
    null_percentage = (df.isnull().mean() * 100).round(2)

    # Krijo një DataFrame përmbledhës për të gjitha kolonat me vlera null dhe përqindjet
    null_summary = pd.DataFrame({
        'Numri Null': null_values,
        'Përqindja Null (%)': null_percentage
    })

    # Numri i rreshtave të kopjuar (duplicated)
    duplicate_count = df.duplicated().sum()

    # Zgjidh rreshtat që përmbajnë vlera null
    rows_with_nulls = df[df.isnull().any(axis=1)]

    # Shfaq rezultatet
    print(f"Numri i rreshtave: {row_count}")
    print(f"Numri i kolonave: {column_count}")
    print("\nLlojet e të dhënave:\n", data_types)
    
    if unique_values:
        print("\nVlerat Unike:")
        for column, values in unique_values.items():
            print(f"Kolona '{column}': {values}")
    
    print("\nVlerat Null për Kolonë (përfshirë kolonat me zero vlera null):")
    print(null_summary)
    
    print(f"\nNumri i Rreshtave të Kopjuar: {duplicate_count}")
    print("\nRreshtat me Vlera Null (duke shfaqur 10 rreshtat e parë me vlera null):")
    print(rows_with_nulls.head(10))  # Shfaq 10 rreshtat e parë me vlera null për një përmbledhje

    return rows_with_nulls  # Opsionale: kthen rreshtat me vlera null për analizë të mëtejshme

# Përdorimi
file_path = '../data/processed/prepared_data.csv'  # Zëvendësoni me rrugën tuaj të skedarit
unique_columns = ['Statusi', 'Tipi i biznesit', 'Komuna']  # Zëvendësoni me kolonat tuaja të interesit
rows_with_nulls = analyze_csv(file_path, unique_columns)

file_path = '../data/raw/data.csv'  # Zëvendësoni me rrugën tuaj të skedarit
rows_with_nulls = analyze_csv(file_path, unique_columns)
