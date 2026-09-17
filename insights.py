def generate_insight(trend_direction, percent_change, forecast_df, inventory_results, anomaly_count, total_days):
    """
    Combines all our calculated results into a plain-English business
    recommendation. Every sentence here is generated FROM actual numbers
    we calculated earlier — nothing is invented.
    """
    lines = []

    # --- Trend statement ---
    if trend_direction == "increasing":
        lines.append(f"Demand has been increasing over the historical period, up {percent_change:.1f}% from start to end.")
    elif trend_direction == "decreasing":
        lines.append(f"Demand has been decreasing over the historical period, down {abs(percent_change):.1f}% from start to end.")
    else:
        lines.append("Demand has remained relatively stable over the historical period.")

    # --- Forecast statement ---
    avg_forecast = forecast_df["forecast"].mean()
    lines.append(f"Over the next {len(forecast_df)} days, average expected demand is {avg_forecast:.1f} units per day.")

    # --- Anomaly statement ---
    anomaly_pct = (anomaly_count / total_days) * 100
    lines.append(f"{anomaly_count} unusual demand spikes or drops were detected in the historical data ({anomaly_pct:.1f}% of days).")

    # --- Inventory statement ---
    if inventory_results["shortage_risk"]:
        lines.append(
            f"Current inventory ({inventory_results['current_inventory']} units) is below the recommended "
            f"reorder point ({inventory_results['reorder_point']} units). Replenishment is recommended: "
            f"order approximately {inventory_results['suggested_reorder_qty']} units."
        )
    elif inventory_results["overstock_risk"]:
        lines.append(
            f"Current inventory ({inventory_results['current_inventory']} units) is significantly higher than "
            f"recommended ({inventory_results['recommended_inventory']} units). Consider slowing reorders to avoid overstocking."
        )
    else:
        lines.append(
            f"Current inventory ({inventory_results['current_inventory']} units) is within a healthy range "
            f"relative to the recommended level ({inventory_results['recommended_inventory']} units)."
        )

    return " ".join(lines)


if __name__ == "__main__":
    from preprocessing import load_and_clean
    from trend_seasonality import decompose_series, detect_trend_direction
    from forecasting import train_forecast_model, generate_forecast
    from anomaly import detect_anomalies
    from inventory import calculate_inventory_recommendation

    df = load_and_clean("data/single_series.csv")

    # Trend
    decomposition = decompose_series(df, period=365)
    trend_direction, percent_change = detect_trend_direction(decomposition)

    # Forecast
    fitted_model, series = train_forecast_model(df, seasonal_period=7)
    forecast_df = generate_forecast(fitted_model, horizon_days=30)

    # Anomalies
    df_with_anomalies = detect_anomalies(df, window=30, threshold=2.5)
    anomaly_count = df_with_anomalies["is_anomaly"].sum()

    # Inventory
    inventory_results = calculate_inventory_recommendation(
        df, current_inventory=200, lead_time_days=7,
        service_level_z=1.65, forecast_horizon_days=30
    )

    print("=== AI-GENERATED BUSINESS INSIGHT ===\n")
    insight = generate_insight(
        trend_direction, percent_change, forecast_df,
        inventory_results, anomaly_count, len(df)
    )
    print(insight)