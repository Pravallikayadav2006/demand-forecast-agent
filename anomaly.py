import pandas as pd
import plotly.graph_objects as go
from preprocessing import load_and_clean

def detect_anomalies(df, window=30, threshold=2.5):
    """
    Flags days where sales are unusually far from the recent rolling average.
    Uses a rolling z-score: how many standard deviations away from the
    recent local average a point is.
    
    window: how many recent days define "normal" for comparison
    threshold: how many standard deviations away counts as an anomaly
               (2.5 is a common, reasonably strict cutoff)
    """
    df = df.copy()
    
    rolling_mean = df["sales"].rolling(window=window, center=True, min_periods=1).mean()
    rolling_std = df["sales"].rolling(window=window, center=True, min_periods=1).std()
    
    df["z_score"] = (df["sales"] - rolling_mean) / rolling_std
    df["is_anomaly"] = df["z_score"].abs() > threshold
    
    return df

def summarize_anomalies(df):
    """
    Prints how many anomalies were found and lists them with dates.
    """
    anomalies = df[df["is_anomaly"]]
    print(f"Total anomalies detected: {len(anomalies)}")
    print(f"Out of {len(df)} total days ({round(len(anomalies)/len(df)*100, 2)}%)")
    
    if len(anomalies) > 0:
        print("\nAnomaly dates and values:")
        print(anomalies[["date", "sales", "z_score", "promo"]].to_string(index=False))
    
    return anomalies

def plot_anomalies(df):
    """
    Plots the full sales series with anomalies highlighted as red markers.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["sales"],
        mode="lines", name="Sales",
        line=dict(color="blue")
    ))
    
    anomalies = df[df["is_anomaly"]]
    fig.add_trace(go.Scatter(
        x=anomalies["date"], y=anomalies["sales"],
        mode="markers", name="Anomaly",
        marker=dict(color="red", size=8, symbol="x")
    ))
    
    fig.update_layout(title="Sales with Detected Anomalies Highlighted")
    fig.write_html("anomaly_detection.html")
    print("\nSaved: anomaly_detection.html")

if __name__ == "__main__":
    df = load_and_clean("data/single_series.csv")
    
    print("=== ANOMALY DETECTION ===")
    df = detect_anomalies(df, window=30, threshold=2.5)
    anomalies = summarize_anomalies(df)
    
    print("\n=== GENERATING CHART ===")
    plot_anomalies(df)