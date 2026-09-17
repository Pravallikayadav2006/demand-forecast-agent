import pandas as pd

# Load the full dataset
print("Loading data... this may take a minute for a 195MB file")
df = pd.read_csv("data/multi_product_sample.csv")

# --- INSPECTION ---
print("\nShape (rows, columns):", df.shape)
print("\nColumn names and types:\n", df.dtypes)
print("\nMissing values per column:\n", df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())
print("\nDate range:", df["date"].min(), "to", df["date"].max())
print("\nUnique stores:", df["store_id"].nunique())
print("\nUnique items:", df["item_id"].nunique())

# --- CREATE A MANAGEABLE SUBSET FOR THE HACKATHON ---
store_choice = "store_1"
item_choice = "item_1"

subset = df[(df["store_id"] == store_choice) & (df["item_id"] == item_choice)].copy()
subset = subset.sort_values("date")

print("\nSubset shape:", subset.shape)
subset.to_csv("data/single_series.csv", index=False)
print("\nSaved: data/single_series.csv")

# --- ALSO CREATE A SMALLER MULTI-PRODUCT SAMPLE ---
sample_stores = [f"store_{i}" for i in range(1, 6)]
sample_items = [f"item_{i}" for i in range(1, 6)]

multi_sample = df[df["store_id"].isin(sample_stores) & df["item_id"].isin(sample_items)].copy()
multi_sample = multi_sample.sort_values("date")

print("\nMulti-product sample shape:", multi_sample.shape)
multi_sample.to_csv("data/multi_product_sample.csv", index=False)
print("Saved: data/multi_product_sample.csv")