# Customer Intelligence Dashboard

Financial behavior monitoring dashboard built with **Streamlit** + **Plotly**.

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-APP-NAME.streamlit.app)

## Features

- **4 KPI metric cards** with gradient backgrounds (Total Customers, Credit Demand, Avg Propensity Score, Critical Alerts)
- **Donut chart** — customer profile distribution
- **Horizontal bar chart** — propensity score by segment (with target threshold)
- **Histogram** — propensity score distribution
- **Bar chart** — alert flag distribution
- **Top 10 priority customers** table with conditional formatting
- **Interactive filters** — sidebar with customer profile, credit demand, alert level, and propensity range selectors

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
streamlit run app.py
```

### Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **"New app"** → select this repo → branch `main` → file `app.py`
5. Click **Deploy**

Your dashboard will be live at `https://<app-name>.streamlit.app`.

### Deploy to Hugging Face Spaces

1. Create a Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose **Streamlit** as the SDK
3. Connect your GitHub repo or upload files manually
4. The Space will auto-detect `requirements.txt` and `app.py`

## Project Structure

```
├── app.py              # Main Streamlit application
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
