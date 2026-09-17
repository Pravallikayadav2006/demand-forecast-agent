📦 Demand Forecast Agent
An explainable demand forecasting and inventory recommendation system, built for the Microsoft Codeathon.
Turns raw historical retail sales data into a concrete, justified inventory recommendation — with every number traceable back to a real calculation, not a black-box prediction.
DATA → ANALYSIS → FORECAST → REASONING → RECOMMENDATION
---
🚀 Live Demo
Deployed app: https://demand-forecast-agent-czrb8ofsirckfdiavckamy.streamlit.app/
GitHub repo:https://github.com/Pravallikayadav2006/demand-forecast-agent.git
---
🧩 Problem Statement
Retail businesses often make stocking decisions based on gut feel or simple historical averages, leading to two costly failure modes:
Stockouts — lost sales when demand spikes unexpectedly
Overstock — tied-up capital and waste when demand is overestimated
Most existing forecasting tools are either too simplistic (flat averages) or too opaque (black-box ML with no explanation) to be trusted by an actual business owner.
💡 Our Solution
An end-to-end, explainable pipeline that:
Loads and cleans raw daily sales data per store/item
Runs exploratory analysis — total sales, average daily demand, min/max, variability
Detects trend — increasing, decreasing, or stable, with a quantified slope and % change
Detects seasonality — weekly and yearly demand patterns
Flags anomalies — statistical outliers using a rolling z-score, likely promotions or stockouts
Forecasts future demand over a configurable horizon (7–90 days) with a confidence interval
Recommends inventory actions — safety stock, reorder point, and reorder quantity, compared against current inventory to flag shortage or overstock risk
Generates plain-English insights — grounded entirely in the numbers computed above, never hallucinated
Every tab in the dashboard answers a "why," not just a "what."
📊 Dataset
Store Item Demand Forecasting Dataset (Kaggle) — 5 years of daily synthetic-but-realistic retail sales data (2019–2023) across 50 stores × 50 items, with genuine trend, weekly/yearly seasonality, pricing, and promotional effects.
Columns: `date`, `store_id`, `item_id`, `sales`, `price`, `promo`, `weekday`, `month`
🏗️ Architecture
```
demand-forecast-agent/
│
├── app.py                    → Streamlit UI, orchestrates everything
├── adapter.py                → Wraps backend modules to match the frontend's contract
├── data_loader.py            → Loads and validates raw CSV data
├── preprocessing.py          → Cleans, filters, resamples per store/item
├── eda.py                    → Summary statistics
├── trend_seasonality.py      → Trend detection & seasonal decomposition
├── anomaly.py                → Rolling z-score anomaly detection
├── forecasting.py            → Model fitting + forecast + confidence interval
├── inventory.py              → Safety stock / reorder point / reorder quantity logic
├── insights.py                → Converts computed numbers into plain-English insights
├── prepare_data.py           → One-time script to inspect & subset the raw dataset
├── requirements.txt
└── data/
    ├── single_series.csv         → One store, one item (demo dataset)
    └── multi_product_sample.csv  → 5 stores × 5 items sample
```
Each backend module is independently built and testable, and connects to the frontend through a single adapter layer — so the UI and backend could be developed in parallel.
🛠️ Tech Stack
Backend: Python, pandas, NumPy, statsmodels (seasonal decomposition & forecasting), scikit-learn
Frontend: Streamlit, Plotly (interactive visualizations)
Deployment: Streamlit Community Cloud
⚙️ Running Locally
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/demand-forecast-agent.git
cd demand-forecast-agent

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
The app opens automatically at `http://localhost:8501`.
🖥️ Using the Dashboard
Pick a store and item from the sidebar
Adjust forecast horizon, confidence level, current inventory, lead time, and service level
Click 🚀 Run analysis
Explore the six tabs:
📊 Overview — historical sales trend and summary stats
📈 Trend & Seasonality — weekly/yearly patterns and trend classification
🚨 Anomalies — flagged unusual sales days
🔮 Forecast — future demand with confidence interval (downloadable as CSV)
📦 Inventory — reorder point, safety stock, and shortage/overstock risk
💡 AI Insights — auto-generated, numbers-grounded summary
🔮 Future Work
Multi-product / multi-store comparison views
What-if scenario sliders (e.g. simulating a promotion's demand impact)
LLM-polished narrative layer on top of the existing rule-based insights
👥 Team
Baddula Pravallika — Frontend & UI (Streamlit dashboard, integration)
Boda Bhargavi — Backend (data pipeline, forecasting, inventory logic)
Karanam Naga Srija — Backend (data pipeline, forecasting, inventory logic)
---
