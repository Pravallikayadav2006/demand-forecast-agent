import pandas as pd
import numpy as np
from preprocessing import load_and_clean

def calculate_inventory_recommendation(
    df,
    current_inventory,
    lead_time_days=7,
    service_level_z=1.65,  # 95% service level
    forecast_horizon_days=30
):
    """
    Calculates inventory recommendations based on historical demand.
    
    current_inventory: units currently in stock (business provides this)
    lead_time_days: how many days it takes for a reorder to arrive
    service_level_z: z-score for desired service level 
                      (1.65 = 95%, 1.28 = 90%, 2.33 = 99%)
    forecast_horizon_days: how many days ahead we're planning for
    
    Returns a dictionary with all the key inventory metrics.
    """
    avg_daily_demand = df["sales"].mean()
    std_daily_demand = df["sales"].std()
    
    # Expected demand during the lead time (while waiting for reorder)
    expected_demand_during_lead_time = avg_daily_demand * lead_time_days
    
    # Safety stock: extra buffer to protect against demand variability
    # Formula: z * std_dev * sqrt(lead_time)
    safety_stock = service_level_z * std_daily_demand * np.sqrt(lead_time_days)
    
    # Reorder point: inventory level at which we should reorder
    reorder_point = expected_demand_during_lead_time + safety_stock
    
    # Expected demand over the full forecast horizon (e.g. next 30 days)
    expected_demand_horizon = avg_daily_demand * forecast_horizon_days
    
    # Recommended inventory to hold to cover the forecast horizon + safety stock
    recommended_inventory = expected_demand_horizon + safety_stock
    
    # Suggested reorder quantity if we're currently below reorder point
    if current_inventory < reorder_point:
        shortage_risk = True
        suggested_reorder_qty = recommended_inventory - current_inventory
    else:
        shortage_risk = False
        suggested_reorder_qty = 0
    
    # Overstock check: do we have way more than we need?
    overstock_risk = current_inventory > (recommended_inventory * 1.5)
    
    results = {
        "avg_daily_demand": round(avg_daily_demand, 2),
        "std_daily_demand": round(std_daily_demand, 2),
        "expected_demand_during_lead_time": round(expected_demand_during_lead_time, 2),
        "safety_stock": round(safety_stock, 2),
        "reorder_point": round(reorder_point, 2),
        "expected_demand_horizon": round(expected_demand_horizon, 2),
        "recommended_inventory": round(recommended_inventory, 2),
        "current_inventory": current_inventory,
        "shortage_risk": shortage_risk,
        "overstock_risk": overstock_risk,
        "suggested_reorder_qty": round(suggested_reorder_qty, 2),
    }
    
    return results

def print_recommendation(results):
    """
    Prints the inventory recommendation in a readable format.
    """
    print("=== INVENTORY RECOMMENDATION ===")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    df = load_and_clean("data/single_series.csv")
    
    # Assumption: business currently has 200 units in stock
    # (In the real dashboard, this will be a user input)
    current_inventory = 1500
    
    results = calculate_inventory_recommendation(
        df,
        current_inventory=current_inventory,
        lead_time_days=7,
        service_level_z=1.65,
        forecast_horizon_days=30
    )
    
    print_recommendation(results)