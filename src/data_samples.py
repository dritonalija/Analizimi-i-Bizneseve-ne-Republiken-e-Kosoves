import pandas as pd

# Ngarkimi i të dhënave nga një skedar CSV
df = pd.read_csv("../data/processed/prepared_data.csv")

# Marrim një mostër prej 100 rreshtash nga të dhënat e pastruara
sample_data_100 = df.sample(n=100, random_state=42)
print("Mostra prej 100 rreshtash të zgjedhura rastësisht:")
print(sample_data_100)
print("\n" + "="*50 + "\n")

# Marrim një mostër prej 10% të të dhënave të pastruara
sample_data_10_percent = df.sample(frac=0.1, random_state=42)
print("Mostra prej 10% të të dhënave:")
print(sample_data_10_percent)
print("\n" + "="*50 + "\n")

# Marrim një mostër të rreshtave unikë të bazuar në kolonën 'Data e regjistrimit'
unique_dates_sample = df.drop_duplicates(subset=['Data e regjistrimit']).sample(n=50, random_state=42)
print("Mostra prej 50 rreshtash unikë bazuar në 'Data e regjistrimit':")
print(unique_dates_sample)
print("\n" + "="*50 + "\n")

# Marrim një mostër prej 50 rreshtash për datat nga viti 2020 e tutje
filtered_data = df[df['Data e regjistrimit'] >= '2020-01-01']
sample_data_filtered = filtered_data.sample(n=50, random_state=42)
print("Mostra prej 50 rreshtash nga të dhënat e filtruar për datat nga 2020 e tutje:")
print(sample_data_filtered)
print("\n" + "="*50 + "\n")
