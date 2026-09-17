import pandas as pd

def load_and_clean(filepath):
    """
    Loads a sales CSV, converts date to datetime,
    sorts by date, and returns a clean DataFrame.
    """
    df = pd.read_csv(filepath)
    
    # Convert date column from text to actual datetime
    df["date"] = pd.to_datetime(df["date"])
    
    # Sort chronologically (should already be sorted, but just in case)
    df = df.sort_values("date").reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    # Quick test on our single series
    df = load_and_clean("data/single_series.csv")
    print("Loaded shape:", df.shape)
    print("\nData types after cleaning:\n", df.dtypes)
    print("\nFirst 5 rows:\n", df.head())
    print("\nLast 5 rows:\n", df.tail())