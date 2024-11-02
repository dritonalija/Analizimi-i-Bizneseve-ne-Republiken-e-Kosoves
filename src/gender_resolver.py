import pandas as pd
import glob
from IPython.display import display

# Shtegu drejt dosjes që përmban skedarët CSV
file_path = '../data/raw'

# Përdorim glob për të marrë vetëm skedarët CSV që përmbajnë 'data-2' në emrat e tyre
selected_files = glob.glob(file_path + "/*data-2*.csv")

# Krijojmë një listë të DataFrames për të ruajtur të dhënat nga secili skedar
dataframes = []

# Kalojmë nëpër secilin skedar, e lexojmë dhe shfaqim informacionin e tij
for file in selected_files:
    df = pd.read_csv(file)  # Lexojmë skedarin CSV në një DataFrame
    dataframes.append(df)  # Shtojmë DataFrame-in në listë
    print(f"Informacion për skedarin {file}:")
    display(df.info())  # Shfaqim informacionin e DataFrame-it
    print("\n" + "-"*50 + "\n")  # Shtojmë një vijë ndarëse për pamjen

# Bashkojmë të gjitha DataFrames në një të vetme
merged_df = pd.concat(dataframes, ignore_index=True)

# Shfaqim informacionin për DataFrame-in e bashkuar
print("Informacion për DataFrame-in e bashkuar:")
display(merged_df.info())

# Ruajmë DataFrame-in e bashkuar në një skedar CSV
merged_df.to_csv('../data/raw/data.csv', index=False)
print("Skedari i bashkuar u ruajt si 'data.csv'")
