import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from preprocessing import load_and_clean

def train_forecast_model(df, seasonal_period=7):
    """
    Trains a Holt-Winters Exponential Smoothing model on the sales data.
    seasonal_period=7 because we confirmed strong WEEKLY seasonality earlier.
    (Yearly seasonality also exists, but with daily data, period=365 needs
    much more data per cycle to estimate reliably within our time limit —
    weekly is the safer, well-supported choice for this hackathon model.)
    """
    series = df.set_index("date")["sales"]

    model = ExponentialSmoothing(
        series,
        trend="add",           # additive trend (matches our confirmed increasing trend)
        seasonal="add",        # additive seasonality (weekly pattern)
        seasonal_periods=seasonal_period
    )

    fitted_model = model.fit()
    return fitted_model, series

def generate_forecast(fitted_model, horizon_days=30):
    """
    Generates a forecast for the next `horizon_days` days,
    along with a simple confidence interval based on residual variability.
    """
    forecast = fitted_model.forecast(horizon_days)

    # Estimate a simple confidence interval using residual standard deviation
    residuals = fitted_model.resid
    resid_std = residuals.std()

    lower_bound = forecast - (1.96 * resid_std)  # ~95% interval
    upper_bound = forecast + (1.96 * resid_std)

    forecast_df = pd.DataFrame({
        "date": forecast.index,
        "forecast": forecast.values,
        "lower_bound": lower_bound.values,
        "upper_bound": upper_bound.values
    })

    return forecast_df

def plot_forecast(series, forecast_df):
    """
    Plots historical sales plus the forecast with confidence interval.
    """
    fig = go.Figure()

    # Historical data (last 90 days for a cleaner view)
    recent_history = series[-90:]
    fig.add_trace(go.Scatter(
        x=recent_history.index, y=recent_history.values,
        mode="lines", name="Historical Sales", line=dict(color="blue")
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["forecast"],
        mode="lines", name="Forecast", line=dict(color="orange")
    ))

    # Confidence interval band
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["upper_bound"],
        mode="lines", name="Upper Bound", line=dict(width=0), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=forecast_df["date"], y=forecast_df["lower_bound"],
        mode="lines", name="Confidence Interval",
        line=dict(width=0), fill="tonexty", fillcolor="rgba(255,165,0,0.2)"
    ))

    fig.update_layout(title="Demand Forecast with Confidence Interval")
    fig.write_html("forecast.html")
    print("Saved: forecast.html")

if __name__ == "__main__":
    df = load_and_clean("data/single_series.csv")

    print("=== TRAINING FORECAST MODEL ===")
    fitted_model, series = train_forecast_model(df, seasonal_period=7)
    print("Model trained successfully.")

    print("\n=== GENERATING 30-DAY FORECAST ===")
    forecast_df = generate_forecast(fitted_model, horizon_days=30)
    print(forecast_df.to_string(index=False))

    print("\n=== GENERATING CHART ===")
    plot_forecast(series, forecast_df)