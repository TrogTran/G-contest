# Customer Intelligence Dashboard

Financial behavior monitoring dashboard built with **Streamlit** + **Plotly**.

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-APP-NAME.streamlit.app)

## Pages

### Overview (app.py)
- **4 KPI metric cards** with gradient backgrounds (Total Customers, Credit Demand, Avg Propensity Score, Critical Alerts)
- **Donut chart** — customer profile distribution
- **Horizontal bar chart** — propensity score by segment (with target threshold)
- **Histogram** — propensity score distribution
- **Bar chart** — alert flag distribution
- **Top 10 priority customers** table with conditional formatting
- **Interactive filters** — sidebar with customer profile, credit demand, alert level, and propensity range selectors

### Sales Analysis (pages/1_Sales_Analysis.py)
- Revenue & orders KPIs with period-over-period growth
- Revenue trend over time with 7-day rolling average
- Revenue breakdown by category and channel
- Top selling categories by order volume
- Filters: date range, category, channel

### Customer Insights (pages/2_Customer_Insights.py)
- Customer count, retention rate, LTV, and churn KPIs
- Geographic distribution by region
- Segment composition and value analysis
- Lifetime value distribution by segment
- Customer acquisition trend over time
- Filters: region, segment, activity status

### Product Performance (pages/3_Product_Performance.py)
- Revenue, units sold, margin, and top product KPIs
- Top 10 products by revenue (horizontal bar)
- Revenue share by category (donut chart)
- Profit vs units sold scatter matrix
- Product ratings by category
- Filters: category, price range, minimum rating

## Tech Stack

| Component | Library |
|-----------|---------|
| Framework | Streamlit |
| Charts | Plotly (go + express) |
| Data | Pandas + NumPy |
| Styling | Custom CSS (Inter font, gradients, dark sidebar) |

## Quick Start

### Local

```bash
pip install -r requirements.txt
streamlit run app.py   # app.py is the multi-page router
```

### Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **"New app"** → select this repo → branch `main` → file `app.py` (app.py is the multi-page router)
5. Click **Deploy**

Your dashboard will be live at `https://<app-name>.streamlit.app`.

### Deploy to Hugging Face Spaces

1. Create a Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose **Streamlit** as the SDK
3. Connect your GitHub repo or upload files manually
4. The Space will auto-detect `requirements.txt` and `app.py`

## Project Structure

```
├── app.py              # Multi-page router (st.navigation)
├── overview.py         # Overview dashboard (original content)
├── pages/
│   ├── 1_Sales_Analysis.py        # Sales performance page
│   ├── 2_Customer_Insights.py     # Customer behavior page
│   └── 3_Product_Performance.py   # Product profitability page
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── .streamlit/
│   └── config.toml     # Streamlit theme configuration
└── data/               # (optional) sample data directory
```

## Data

The app uses **synthetic data** generated on-the-fly with NumPy, modeling:
- 200 customers across 4 personas (Dormant, Credit Seeker, Wealth Accumulator, Digital Native)
- Credit propensity scores (beta distribution)
- Alert flags with anomaly scores
- Transaction behavior metrics

No external data files required.
