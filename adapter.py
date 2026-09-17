"""
Adapter layer: makes our real backend match the function contract
that the frontend (app.py) expects.
"""
import pandas as pd
from preprocessing import load_and_clean
from trend_seasonality import decompose_series, detect_trend_direction
from forecasting import train_forecast_model, generate_forecast
from anomaly import detect_anomalies as _detect_anomalies
from inventory import calculate_inventory_recommendation


def load_data(filepath):
    return load_and_clean(filepath)


def get_series(df, store_id, item_id):
    sub = df[(df["store_id"] == store_id) & (df["item_id"] == item_id)].copy()
    sub = sub.sort_values("date").set_index("date")
    return sub[["sales"]]


def summary_stats(series):
    s = series["sales"]
    return {
        "total_sales": int(s.sum()),
        "avg_daily": float(s.mean()),
        "min": float(s.min()),
        "max": float(s.max()),
        "std": float(s.std())
    }


def detect_trend(series):
    df_reset = series.reset_index()
    decomposition = decompose_series(df_reset, period=365)
    direction, pct_change = detect_trend_direction(decomposition)
    trend_clean = decomposition.trend.dropna()
    slope = (trend_clean.iloc[-1] - trend_clean.iloc[0]) / len(trend_clean)
    return {"direction": direction, "slope": float(slope), "pct_change": float(pct_change)}


def detect_seasonality(series):
    s = series.copy()
    s["weekday"] = s.index.dayofweek
    s["month"] = s.index.month
    return {
        "has_weekly": True,
        "has_yearly": True,
        "weekday_avg": s.groupby("weekday")["sales"].mean().to_dict(),
        "monthly_avg": s.groupby("month")["sales"].mean().to_dict(),
    }


def detect_anomalies(series):
    df_reset = series.reset_index()
    result = _detect_anomalies(df_reset, window=30, threshold=2.5)
    return result.set_index("date")


def forecast(series, horizon, confidence):
    df_reset = series.reset_index()
    fitted_model, _ = train_forecast_model(df_reset, seasonal_period=7)
    forecast_df = generate_forecast(fitted_model, horizon_days=horizon)
    return forecast_df.rename(columns={"lower_bound": "lower", "upper_bound": "upper"})


def recommend(series, forecast_df, lead_time_days, service_level_z, current_inventory=0):
    df_reset = series.reset_index()
    results = calculate_inventory_recommendation(
        df_reset, current_inventory=current_inventory,
        lead_time_days=lead_time_days, service_level_z=service_level_z,
        forecast_horizon_days=len(forecast_df)
    )
    return {
        "safety_stock": results["safety_stock"],
        "reorder_point": results["reorder_point"],
        "reorder_qty": results["suggested_reorder_qty"],
        "recommended_inventory": results["recommended_inventory"],
        "avg_daily_demand": results["avg_daily_demand"],
        "current_inventory": results["current_inventory"],
        "shortage_risk": results["shortage_risk"],
        "overstock_risk": results["overstock_risk"],
    }


def generate_insights(stats, trend, seasonality, anomalies, inventory):
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    top_weekday = max(seasonality["weekday_avg"], key=seasonality["weekday_avg"].get)
    n_anom = int(anomalies["is_anomaly"].sum())
    return [
        f"Demand is **{trend['direction']}**, changing by {trend['pct_change']:.1f}% over the historical period.",
        f"Average daily demand is **{stats['avg_daily']:.1f} units**, with variability (std dev) of {stats['std']:.1f}.",
        f"**{weekday_names[top_weekday]}** is consistently the strongest day of the week for sales.",
        f"**{n_anom} anomalies** were flagged out of {len(anomalies)} days ({n_anom/len(anomalies)*100:.1f}%).",
        f"Reorder point is **{inventory['reorder_point']:.0f} units** with recommended safety stock of {inventory['safety_stock']:.0f} units.",
    ]