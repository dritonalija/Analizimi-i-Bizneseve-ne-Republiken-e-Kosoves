import pandas as pd

# Ngarkimi i të dhënave nga një skedar CSV
df = pd.read_csv("../data/processed/prepared_data.csv")

# Përkufizojmë një funksion ndihmës për shfaqjen e të dhënave
def display_sample(description, sample_df):
    print(description)
    print(sample_df)
    print("\n" + "=" * 50 + "\n")

# Marrim një mostër prej 100 rreshtash nga të dhënat e pastruara
sample_100 = df.sample(n=100, random_state=42)
display_sample("Sample of 100 randomly selected rows:", sample_100)

# Marrim një mostër prej 10% të të dhënave të pastruara
sample_10_percent = df.sample(frac=0.1, random_state=42)
display_sample("Sample of 10% of the data:", sample_10_percent)

# Marrim një mostër të rreshtave unikë të bazuar në kolonën 'Data e regjistrimit'
unique_dates_sample = df.drop_duplicates(subset=['Data e regjistrimit']).sample(n=50, random_state=42)
display_sample("Sample of 50 unique rows based on 'Data e regjistrimit':", unique_dates_sample)


# Marrim një mostër prej 50 rreshtash për datat nga viti 2020 e tutje
filtered_sample = df[df['Data e regjistrimit'] >= '2020-01-01'].sample(n=50, random_state=42)
display_sample("Sample of 50 rows from 2020 onwards:", filtered_sample)
