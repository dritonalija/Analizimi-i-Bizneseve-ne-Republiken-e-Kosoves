import pandas as pd
import glob
from IPython.display import display

# Path to the folder containing your CSV files
file_path = '../data/raw'

# Use glob to get only CSV files containing 'data-2' in their names
selected_files = glob.glob(file_path + "/*data-2*.csv")

dataframes = []

# Loop through each file, read it, and display its info
for file in selected_files:
    df = pd.read_csv(file)
    dataframes.append(df)
    print(f"Info for file {file}:")
    display(df.info())
    print("\n" + "-"*50 + "\n")

# Concatenate all DataFrames into one
merged_df = pd.concat(dataframes, ignore_index=True)

# Display info for the final merged DataFrame
print("Info for merged DataFrame:")
display(merged_df.info())

# Save the merged DataFrame to a CSV file
merged_df.to_csv('../data/raw/data.csv', index=False)
print("Merged file saved as 'data.csv'")
