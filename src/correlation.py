import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, pearsonr

# Funksioni për të ngarkuar të dhënat
def load_data(file_path):
    return pd.read_csv(file_path)

# Funksioni për të përpunuar kolonën "Aktivitetet Encoded"
def preprocess_activity_column(df, activity_column):
    """Përpunon kolonën 'Aktivitetet Encoded' duke kthyer listat dhe shtuar statistika."""
    def parse_activity(activity_str):
        try:
            return eval(activity_str) if isinstance(activity_str, str) else []
        except:
            return []
    
    # Konvertojnë dhe llogarisin statistika bazë për aktivitete
    df[activity_column] = df[activity_column].apply(parse_activity)
    df['Numri i Aktiviteteve'] = df[activity_column].apply(len)  # Numri i aktiviteteve
    df['Aktiviteti_Primar'] = df[activity_column].apply(lambda x: x[0] if len(x) > 0 else None)  # Aktiviteti i parë
    df['Aktiviteti_Sekondar'] = df[activity_column].apply(lambda x: x[1] if len(x) > 1 else None)  # Aktiviteti i dytë
    return df

# Funksioni për të analizuar Chi-Square për të gjitha çiftet e kolonave nominale
def analyze_chi_square_all(df, categorical_columns):
    """Teston pavarësinë mes të gjitha kombinimeve të kolonave nominale."""
    results = []
    for i, col1 in enumerate(categorical_columns):
        for col2 in categorical_columns[i + 1:]:
            contingency_table = pd.crosstab(df[col1], df[col2])
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            results.append({
                'Atributi 1': col1,
                'Atributi 2': col2,
                'Chi2': chi2,
                'p-value': p
            })
    return pd.DataFrame(results).sort_values(by='p-value')

# Funksioni për të analizuar korrelacionin (Pearson dhe Covariance) për kolonat numerike
def analyze_numerical_relationships(df, numerical_columns):
    """Llogarit korrelacionin dhe kovariancën për kolona numerike."""
    correlations = []
    for i, col1 in enumerate(numerical_columns):
        for col2 in numerical_columns[i + 1:]:
            # Pearson Correlation
            pearson_corr, _ = pearsonr(df[col1], df[col2])
            # Covariance
            covariance = df[[col1, col2]].cov().iloc[0, 1]
            correlations.append({
                'Atributi 1': col1,
                'Atributi 2': col2,
                'Pearson Correlation': pearson_corr,
                'Covariance': covariance
            })
    return pd.DataFrame(correlations)

# Vizualizimi i matricës së korrelacionit numerik
def plot_correlation_matrix(df, numerical_columns):
    correlation_matrix = df[numerical_columns].corr(method='pearson')
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Matrica e Korrelacionit (Pearson)")
    plt.show()

# Ekzekutimi i skriptit
if __name__ == "__main__":
    input_file_path = "../data/processed/prepared_data.csv"
    df = load_data(input_file_path)
    
    # Përpunojmë kolonën "Aktivitetet Encoded"
    df = preprocess_activity_column(df, 'Aktivitetet Encoded')
    
    # Specifikimi i kolonave nominale dhe numerike
    categorical_columns = ['Tipi i biznesit', 'Komuna', 'Aktiviteti_Primar', 'Aktiviteti_Sekondar']
    numerical_columns = ['Kapitali', 'Numri i punëtorëve', 'Pronarë Mashkull', 'Pronarë Femër', 'Numri i Aktiviteteve']
    
    # Analiza Chi-Square për kolonat nominale (përfshirë aktivitetet)
    chi_square_results = analyze_chi_square_all(df, categorical_columns)
    print("Rezultatet e Chi-Square Test për kolonat nominale (përfshirë aktivitetet):")
    print(chi_square_results)
    
    # Analiza e marrëdhënieve numerike (Pearson dhe Covariance)
    numerical_relationships = analyze_numerical_relationships(df, numerical_columns)
    print("\nKorrelacioni dhe Kovarianca për kolona numerike:")
    print(numerical_relationships)
    
    # Vizualizojmë matricën e korrelacionit numerik
    plot_correlation_matrix(df, numerical_columns)
