# Customer Intelligence Dashboard

Financial behavior monitoring and credit targeting dashboard built with **Streamlit** + **Plotly**, styled with a McKinsey/BCG consulting design system.

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://YOUR-APP-NAME.streamlit.app)

## Pages

### 0 · Overview

Portfolio-level snapshot combining all three data sources.

- **KPIs:** Total Customers, Critical Alerts, Alert Count, Avg Anomaly Score, Avg Burst Ratio, Credit Hungry
- **Charts:** Priority distribution (pie), Customer persona breakdown (bar), Anomaly score histogram, Burst ratio vs anomaly scatter, Credit propensity by persona
- **Filters:** Alert Level, Rule Flags, Anomaly Score range, Persona
- Top 25 flagged customers table + raw data expander

### 1 · Customer Segments

Deep-dive into behavioural clustering and persona analysis.

- **KPIs:** Customer Count, Avg Transactions, Avg Active Months, Avg Annual Outflow, Avg Credit Propensity, Credit Hungry %
- **Charts:** Customers by persona, Avg annual outflow, Login count distribution, Transaction histogram, Alert rate by persona, Credit propensity by persona
- **Filters:** Persona multiselect, Cluster multiselect, Active Months slider
- Cluster summary table + raw data expander

### 2 · NBFO & Credit Targeting

Next-best-financial-offer prioritisation and credit propensity scoring.

- **KPIs:** Targeted Customers, Credit Hungry, Avg Propensity, High Propensity ≥ 0.8, Avg IR Queries, Avg Outflow
- **Charts:** Propensity score histogram (0.8 threshold line), Product mix pie, NBFO targets by persona (stacked bar), Outflow slope vs propensity scatter
- **Filters:** Credit Hungry toggle, Propensity range, Product Type (Credit Card / Consumer Loan / Other), Persona
- Top 30 targets table + CSV download

### 3 · Security Alerts

Transaction anomaly and fraud-risk investigation.

- **KPIs:** Total Flagged, Critical, Alert, Avg Score, Max Score, Avg Burst Ratio
- **Charts:** Priority breakdown (pie), Rule flag frequency, Anomaly score distribution, Burst ratio scatter, Max transaction amount boxplot, Alert rate by persona
- **Filters:** Priority, Rule Flags, Anomaly Score range, Persona, Show Normal toggle
- Detail table with sort selector + CSV download
- Critical customer deep-dive: individual metric cards + radar chart

## Tech Stack

| Component | Library                                            |
| --------- | -------------------------------------------------- |
| Framework | Streamlit 1.49+                                    |
| Charts    | Plotly (graph_objects + express)                   |
| Data      | Pandas                                             |
| Design    | Custom McKinsey/BCG inline CSS (`utils/styles.py`) |

## Quick Start

### Local

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub → **New app** → select repo → branch `main` → file `app.py`
4. Click **Deploy**

### Deploy to Hugging Face Spaces

1. Create a Space on [huggingface.co/spaces](https://huggingface.co/spaces) with **Streamlit** SDK
2. Connect your GitHub repo or upload files manually
3. The Space auto-detects `requirements.txt` and `app.py`

## Project Structure

```
├── app.py                          # Entry point — set_page_config, styles, st.navigation
├── pages/
│   ├── 0_Overview.py               # Portfolio overview
│   ├── 1_Customer_Segments.py      # Persona & cluster analysis
│   ├── 2_NBFO_Credit.py            # Credit targeting
│   └── 3_Security_Alerts.py        # Fraud & anomaly investigation
├── utils/
│   ├── __init__.py
│   └── styles.py                   # Shared design system (CSS + layout helpers)
├── data/
│   ├── alert_list_security.csv     # 52,488 customers — anomaly scores, rule flags
│   ├── cx_persona_segments.csv     # Behavioural clusters & persona labels
│   └── nbfo_target_list.csv        # Credit propensity scores & NBFO messages
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── config.toml                 # Streamlit theme
```

## Data

All pages use **real data** from the `data/` directory (joined on `CUSTOMER_NUMBER`):

| File                      | Rows   | Key Columns                                                        |
| ------------------------- | ------ | ------------------------------------------------------------------ |
| `alert_list_security.csv` | 52,488 | anomaly_score, priority, rule_flags, burst_ratio                   |
| `cx_persona_segments.csv` | 52,488 | persona, cluster, total_trans, active_months, total_annual_outflow |
| `nbfo_target_list.csv`    | 52,488 | credit_propensity, credit_hungry, ir_query_count, nbfo_message     |

Priority breakdown: Normal = 49,916 · Alert = 2,479 · Critical = 93
