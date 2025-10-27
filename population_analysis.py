<<<<<<< HEAD
import pandas as pd
import seaborn as sns
import os

# population_analysis.py
import matplotlib.pyplot as plt

# === 1. Locate and load dataset safely ===
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "population_data.csv")

try:
    df = pd.read_csv(csv_path)
    print("✅ File loaded successfully!")
except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit()

# === 2. Preview data ===
print("\n=== DATA PREVIEW ===")
print(df.head())

print("\n=== DATA INFO ===")
print(df.info())

print("\n=== SUMMARY STATISTICS ===")
print(df.describe(include='all'))

# === 3. Handle missing or misnamed columns ===
print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

# Optional: rename if needed (adjust to your dataset)
# df.rename(columns={"Population(in millions)": "Population", "Population density": "Density"}, inplace=True)

# === 4. Filter example: India ===
if "Country" in df.columns:
    india_data = df[df["Country"].str.lower() == "india"]
    print("\n=== INDIA DATA ===")
    print(india_data)
else:
    print("\n⚠️ 'Country' column not found!")

# === 5. Visualization: Top 10 Most Populous Countries ===
if "Population(in millions)" in df.columns and "Country" in df.columns:
    plt.figure(figsize=(10, 6))
    top10 = df.nlargest(10, "Population(in millions)")
    sns.barplot(data=top10, x="Country", y="Population(in millions)", palette="viridis")
    plt.title("Top 10 Most Populous Countries")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("\n⚠️ Required columns missing for population plot.")

# === 6. Visualization: Density vs Population ===
if "Population density" in df.columns and "Population(in millions)" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Population density", y="Population(in millions)")
    plt.title("Population Density vs Total Population")
    plt.xlabel("Population Density")
    plt.ylabel("Population (millions)")
    plt.show()
else:
    print("\n⚠️ Required columns missing for scatter plot.")
    
=======
import pandas as pd
import seaborn as sns
import os

# population_analysis.py
import matplotlib.pyplot as plt

# === 1. Locate and load dataset safely ===
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "population_data.csv")

try:
    df = pd.read_csv(csv_path)
    print("✅ File loaded successfully!")
except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit()

# === 2. Preview data ===
print("\n=== DATA PREVIEW ===")
print(df.head())

print("\n=== DATA INFO ===")
print(df.info())

print("\n=== SUMMARY STATISTICS ===")
print(df.describe(include='all'))

# === 3. Handle missing or misnamed columns ===
print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

# Optional: rename if needed (adjust to your dataset)
# df.rename(columns={"Population(in millions)": "Population", "Population density": "Density"}, inplace=True)

# === 4. Filter example: India ===
if "Country" in df.columns:
    india_data = df[df["Country"].str.lower() == "india"]
    print("\n=== INDIA DATA ===")
    print(india_data)
else:
    print("\n⚠️ 'Country' column not found!")

# === 5. Visualization: Top 10 Most Populous Countries ===
if "Population(in millions)" in df.columns and "Country" in df.columns:
    plt.figure(figsize=(10, 6))
    top10 = df.nlargest(10, "Population(in millions)")
    sns.barplot(data=top10, x="Country", y="Population(in millions)", palette="viridis")
    plt.title("Top 10 Most Populous Countries")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("\n⚠️ Required columns missing for population plot.")

# === 6. Visualization: Density vs Population ===
if "Population density" in df.columns and "Population(in millions)" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Population density", y="Population(in millions)")
    plt.title("Population Density vs Total Population")
    plt.xlabel("Population Density")
    plt.ylabel("Population (millions)")
    plt.show()
else:
    print("\n⚠️ Required columns missing for scatter plot.")
    
>>>>>>> 60bc944f62619a8fd865a6f4b03a11f0b1c38f44
    