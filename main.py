import pandas as pd
import numpy as np

# Uploading our DataSet as cvs
df = pd.read_csv("assets/movies.csv")


print("First 5 rows from our data:")
print(df.head())
print("\nInfo about our data: Like columns in the data")
print(df.info())
print("\nStatistics about number columns:")
print(df.describe())

# 1. Cleaning column YEAR
print("\n### Cleaning column 'YEAR' ###")
df['YEAR'] = df['YEAR'].astype(str).str.extract(r'(\d{4})')[0]  # we have to leave only 4 digits
df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')  # Converting to Number
print(f"Found {df['YEAR'].isna().sum()} incorrect year value")

# 2. Cleaning column VOTES
print("\n### CLEANING 'VOTES' column ###")
df['VOTES'] = df['VOTES'].astype(str).str.replace('[^\\d]', '', regex=True)
df['VOTES'] = pd.to_numeric(df['VOTES'], errors='coerce')
print(f"Found {df['VOTES'].isna().sum()} incorrect 'VOTES' values")

# 3. Cleaning column Gross
print("\n### CLEANING COLUMN 'GROSS' ###")
def clean_gross(value):
    if pd.isna(value):
        return np.nan
    value = str(value).replace('$', '').replace('M', '')
    try:
        return float(value) * 1_000_000  # Convert to USD
    except:
        return np.nan

df['Gross'] = df['Gross'].apply(clean_gross)
print(f"Found {df['Gross'].isna().sum()} incorrect 'GROSS'  values")

# 4. Filling Gaps
print("\n### FILLING GAPS ###")
numeric_cols = ['RATING', 'VOTES', 'RunTime', 'Gross']
for col in numeric_cols:
    if col in df.columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"Found {df[col].isna().sum()} GAPS in {col}")

if 'GENRE' in df.columns:
    mode_val = df['GENRE'].mode()[0] if not df['GENRE'].mode().empty else 'unknown'
    df['GENRE'] = df['GENRE'].fillna(mode_val)
    print(f"FOUND {df['GENRE'].isna().sum()} GAPS in 'GENRE'")

# 5. Emission filtering
print("\n### Emission filtering ###")
initial_count = len(df)
df = df[(df['YEAR'] >= 1880) & (df['YEAR'] <= 2023)]
df = df[(df['RATING'] >= 1) & (df['RATING'] <= 10)]
df = df[(df['RunTime'] >= 15) & (df['RunTime'] <= 240)]
print(f"DELETED {initial_count - len(df)} records with outliers")

# 6. Text Cleaning
print("\n### TEXT CLEANING ###")
text_cols = ['MOVIES', 'GENRE', 'ONE-LINE', 'STARS']
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

df['GENRE'] = df['GENRE'].str.lower()

# 7. DELETING DUPLICATES
print("\n=== DELETING DUPLICATES ===")
initial_count = len(df)
df = df.drop_duplicates(subset=['MOVIES', 'YEAR'])
print(f"Deleted {initial_count - len(df)} duplicates")

# 8. Processing Gross column
if 'Gross' in df.columns:
    if df['Gross'].isna().mean() > 0.9:
        df = df.drop(columns=['Gross'])
        print("Column Gross was deleted (too many gaps)")
    else:
        df['Gross'] = df['Gross'].fillna(0)
        print("Gaps in Gross were filled by zeros")

# Final Checking
print("\n### Cleaning Result ###")
print(f"Source Recorded Data: {initial_count}")
print(f"Left after Cleaning: {len(df)}")
print("\nInfo about the Cleaned Data:")
print(df.info())

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 30)

print("\nFirst 10 Cleaned rows:")
print(df.head(10))

# Analyzing Numeric Columns
print("\nStatistics on Numeric Columns:")
print(df.describe())

# Saving the Results
df.to_csv('cleaned_movies.csv', index=False)
print("\nThe Cleaned Data were saved in cleaned_movies.csv")