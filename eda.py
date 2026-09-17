import pandas as pd
import plotly.express as px
from preprocessing import load_and_clean

def basic_stats(df):
    """
    Prints simple overview stats: total sales, average daily demand,
    min/max, and how many days of data we have.
    """
    print("Total historical sales:", df["sales"].sum())
    print("Average daily demand:", round(df["sales"].mean(), 2))
    print("Minimum daily demand:", df["sales"].min())
    print("Maximum daily demand:", df["sales"].max())
    print("Number of days:", len(df))

def plot_sales_over_time(df):
    """
    Creates an interactive line chart of daily sales over time
    and saves it as an HTML file we can open in a browser.
    """
    fig = px.line(df, x="date", y="sales", title="Daily Sales Over Time (store_1, item_1)")
    fig.write_html("eda_sales_over_time.html")
    print("\nSaved chart: eda_sales_over_time.html")

def plot_monthly_average(df):
    """
    Groups sales by month number (1-12) and averages across all years,
    to give an early visual hint of yearly seasonality.
    """
    monthly_avg = df.groupby("month")["sales"].mean().reset_index()
    fig = px.bar(monthly_avg, x="month", y="sales", title="Average Sales by Month (across all years)")
    fig.write_html("eda_monthly_avg.html")
    print("Saved chart: eda_monthly_avg.html")

def plot_weekday_average(df):
    """
    Groups sales by weekday (0=Monday ... 6=Sunday) and averages,
    to give an early visual hint of weekly seasonality.
    """
    weekday_avg = df.groupby("weekday")["sales"].mean().reset_index()
    fig = px.bar(weekday_avg, x="weekday", y="sales", title="Average Sales by Weekday (0=Mon, 6=Sun)")
    fig.write_html("eda_weekday_avg.html")
    print("Saved chart: eda_weekday_avg.html")

if __name__ == "__main__":
    df = load_and_clean("data/single_series.csv")
    
    print("=== BASIC STATS ===")
    basic_stats(df)
    
    print("\n=== GENERATING CHARTS ===")
    plot_sales_over_time(df)
    plot_monthly_average(df)
    plot_weekday_average(df)