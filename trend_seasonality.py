import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from preprocessing import load_and_clean

def decompose_series(df, period=365):
    """
    Splits the sales series into trend, seasonal, and residual components.
    period=365 because we're checking yearly seasonality on daily data.
    """
    series = df.set_index("date")["sales"]
    result = seasonal_decompose(series, model="additive", period=period)
    return result

def detect_trend_direction(result):
    """
    Looks at the trend component's start vs end value to say whether
    demand is increasing, decreasing, or stable.
    """
    trend = result.trend.dropna()
    start_value = trend.iloc[0]
    end_value = trend.iloc[-1]
    change = end_value - start_value
    percent_change = (change / start_value) * 100

    if percent_change > 5:
        direction = "increasing"
    elif percent_change < -5:
        direction = "decreasing"
    else:
        direction = "stable"

    print(f"Trend start value: {round(start_value, 2)}")
    print(f"Trend end value: {round(end_value, 2)}")
    print(f"Percent change over period: {round(percent_change, 2)}%")
    print(f"Trend direction: {direction}")
    
    return direction, percent_change

def plot_decomposition(result):
    """
    Plots trend, seasonal, and residual components as separate charts
    saved into one HTML file.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result.trend.index, y=result.trend, name="Trend"))
    fig.update_layout(title="Trend Component Over Time")
    fig.write_html("trend_component.html")
    print("Saved: trend_component.html")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=result.seasonal.index[:730], y=result.seasonal[:730], name="Seasonal"))
    fig2.update_layout(title="Seasonal Component (first 2 years shown)")
    fig2.write_html("seasonal_component.html")
    print("Saved: seasonal_component.html")

if __name__ == "__main__":
    df = load_and_clean("data/single_series.csv")
    
    print("=== SEASONAL DECOMPOSITION ===")
    result = decompose_series(df, period=365)
    
    print("\n=== TREND DETECTION ===")
    direction, percent_change = detect_trend_direction(result)
    
    print("\n=== GENERATING CHARTS ===")
    plot_decomposition(result)