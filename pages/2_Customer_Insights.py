import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Customer Insights",
                   layout="wide", initial_sidebar_state="expanded")

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', 'Segoe UI', Roboto, sans-serif !important; }
    .material-icons, .material-symbols-outlined,
    span[data-testid="stIconMaterial"] {
        font-family: 'Material Icons', 'Material Icons Outlined', 'Material Symbols Outlined' !important;
        font-size: inherit !important;
    }
    .stExpander details summary span[data-testid="stIconMaterial"] { display: none !important; }
    .stApp { background: #F0F2F6; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(195deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        color: rgba(255,255,255,0.85) !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        color: white;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: rgba(255,255,255,0.3);
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.08) !important;
    }
    section[data-testid="stSidebar"] .stSlider > div > div { color: white; }
    section[data-testid="stSidebar"] nav a {
        color: rgba(255,255,255,0.85) !important;
        font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] nav a:hover {
        color: #4facfe !important;
    }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1); margin: 16px 0; }
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 24px; }
    .metric-card {
        border-radius: 20px; padding: 22px 24px; color: white;
        position: relative; overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 16px 40px rgba(0,0,0,0.14); }
    .metric-card::after {
        content: ''; position: absolute; top: -50%; right: -50%;
        width: 100%; height: 100%;
        background: rgba(255,255,255,0.06);
        border-radius: 50%; pointer-events: none;
    }
    .metric-card .label { font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; opacity: 0.85; margin-bottom: 4px; }
    .metric-card .value { font-size: 32px; font-weight: 800; line-height: 1.2; }
    .metric-card .delta { font-size: 13px; font-weight: 500; opacity: 0.9; margin-top: 2px; }
    .metric-blue   { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .metric-orange { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
    .metric-purple { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }
    .metric-red    { background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); }
    .section-title {
        font-size: 18px; font-weight: 700; color: #212529;
        margin: 24px 0 16px 0; padding-left: 12px;
        border-left: 4px solid #0D6EFD;
    }
    .section-subtitle {
        font-size: 13px; color: #6C757D;
        margin-top: -8px; margin-bottom: 16px; padding-left: 16px;
    }
    div[data-testid="column"] {
        background: white; border: 1px solid #E9ECEF; border-radius: 16px;
        padding: 16px 20px 12px 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    div[data-testid="column"]:hover { box-shadow: 0 8px 28px rgba(0,0,0,0.10); }
    div[data-testid="column"] .section-title { margin-top: 0; }
    div[data-testid="column"] .section-subtitle { margin-bottom: 8px; }
    footer { display: none; }
    #MainMenu { visibility: hidden; }
    @media (max-width: 1200px) { .metric-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 768px) { .metric-grid { grid-template-columns: 1fr; } }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_data
def generate_customer_data(n=500, seed=42):
    np.random.seed(seed)
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East / Africa"]
    segments = ["Premium", "Standard", "Budget"]
    acquisition_dates = [datetime(2023, 1, 1) + timedelta(days=int(d)) for d in np.random.randint(0, 731, n)]

    data = []
    for i in range(n):
        region = np.random.choice(regions, p=[0.30, 0.25, 0.20, 0.15, 0.10])
        seg_probs = {"Premium": 0.20, "Standard": 0.50, "Budget": 0.30}
        segment = np.random.choice(segments, p=[seg_probs[s] for s in segments])
        base_value = {"Premium": 5000, "Standard": 1500, "Budget": 400}[segment]
        lifetime_value = round(base_value + np.random.exponential(base_value * 0.6), 2)
        total_purchases = max(1, int(np.random.poisson({"Premium": 25, "Standard": 12, "Budget": 5}[segment])))
        avg_rating = round(np.clip(np.random.normal(3.8, 0.6), 1, 5), 2)
        is_active = np.random.random() > 0.15
        churned = not is_active and np.random.random() > 0.5
        support_tickets = int(np.random.poisson(1.5 + (0 if segment == "Premium" else 0.5)))
        data.append({
            "customer_id": f"CUST-{10000 + i:05d}",
            "region": region,
            "segment": segment,
            "acquisition_date": acquisition_dates[i],
            "lifetime_value": lifetime_value,
            "total_purchases": total_purchases,
            "avg_rating": avg_rating,
            "is_active": is_active,
            "churned": churned,
            "support_tickets": support_tickets,
        })
    df = pd.DataFrame(data)
    df["acquisition_month"] = df["acquisition_date"].dt.to_period("M").astype(str)
    return df

df_cust = generate_customer_data()

regions = ["All"] + sorted(df_cust["region"].unique().tolist())
sel_region = st.sidebar.multiselect("Region", regions[1:])

segments = ["All"] + sorted(df_cust["segment"].unique().tolist())
sel_segment = st.sidebar.selectbox("Segment", segments)

active_filter = st.sidebar.selectbox("Status", ["All", "Active Only", "Inactive Only"])

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="color: rgba(255,255,255,0.3); font-size: 11px; text-align: center; padding: 12px 0;">
        Customer base since Jan 2023
    </div>
""", unsafe_allow_html=True)

df_f = df_cust.copy()
if sel_region:
    df_f = df_f[df_f["region"].isin(sel_region)]
if sel_segment != "All":
    df_f = df_f[df_f["segment"] == sel_segment]
if active_filter == "Active Only":
    df_f = df_f[df_f["is_active"] == True]
elif active_filter == "Inactive Only":
    df_f = df_f[df_f["is_active"] == False]

total_customers = len(df_f)
active_cust = df_f["is_active"].sum()
retention_rate = round(active_cust / total_customers * 100, 1) if total_customers > 0 else 0
avg_ltv = round(df_f["lifetime_value"].mean(), 2) if total_customers > 0 else 0
churned_cust = df_f["churned"].sum()

today = datetime.today()
thirty_days_ago = today - timedelta(days=30)
new_customers = (df_f["acquisition_date"] >= thirty_days_ago).sum()

st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
        <div style="font-size: 22px; font-weight: 700; color: #212529;">Customer Insights</div>
        <div style="font-size: 13px; color: #6C757D;">Segmentation, retention, and value analysis</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-grid" style="margin-top: 16px;">
    <div class="metric-card metric-blue">
        <div class="label">Total Customers</div>
        <div class="value">{total_customers:,}</div>
        <div class="delta">{new_customers:,} new this month</div>
    </div>
    <div class="metric-card metric-green" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
        <div class="label">Retention Rate</div>
        <div class="value">{retention_rate}%</div>
        <div class="delta">{retention_rate - 82.5:+.1f} pp vs target</div>
    </div>
    <div class="metric-card metric-orange">
        <div class="label">Avg Lifetime Value</div>
        <div class="value">${avg_ltv:,.2f}</div>
        <div class="delta">Per customer</div>
    </div>
    <div class="metric-card metric-red">
        <div class="label">Churned</div>
        <div class="value">{churned_cust:,}</div>
        <div class="delta">{churned_cust / total_customers * 100:.1f}% of total</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">Customer Distribution by Region</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Geographic breakdown of customer base</div>', unsafe_allow_html=True)

    region_dist = df_f["region"].value_counts().reset_index()
    region_dist.columns = ["region", "count"]
    region_dist = region_dist.sort_values("count", ascending=True)

    region_colors = ["#0D6EFD", "#4facfe", "#6C9BCF", "#93C5FD", "#B8D4FE"]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=region_dist["count"],
        y=region_dist["region"],
        orientation="h",
        marker=dict(color=region_colors[:len(region_dist)], line=dict(color="white", width=2), opacity=0.9),
        text=region_dist["count"],
        textposition="outside",
        textfont=dict(size=13, weight=700, color="#212529"),
        hovertemplate="<b>%{y}</b><br>Customers: %{x:,}<extra></extra>",
        width=0.6,
    ))

    fig1.update_layout(
        height=400,
        xaxis=dict(title=dict(text="Customers", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=12, weight=600, color="#212529")),
        margin=dict(l=10, r=40, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig1, width='stretch', config={"displayModeBar": False})

with col2:
    st.markdown('<div class="section-title">Customer Segment Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Segmentation by customer value tier</div>', unsafe_allow_html=True)

    seg_dist = df_f["segment"].value_counts().reset_index()
    seg_dist.columns = ["segment", "count"]

    seg_colors = {"Premium": "#0D6EFD", "Standard": "#4facfe", "Budget": "#93C5FD"}

    fig2 = go.Figure()
    fig2.add_trace(go.Pie(
        labels=seg_dist["segment"],
        values=seg_dist["count"],
        marker=dict(
            colors=[seg_colors.get(s, "#6C757D") for s in seg_dist["segment"]],
            line=dict(color="white", width=3),
        ),
        textinfo="label+percent",
        textposition="outside",
        hole=0.55,
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
        textfont=dict(size=12, color="#212529", weight=600),
        rotation=45,
    ))

    fig2.update_layout(
        height=400,
        margin=dict(l=10, r=180, t=10, b=10),
        template="plotly_white",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown('<div class="section-title">Lifetime Value by Segment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Distribution of customer value across segments</div>', unsafe_allow_html=True)

    fig3 = go.Figure()
    segments_list = ["Premium", "Standard", "Budget"]
    for seg in segments_list:
        subset = df_f[df_f["segment"] == seg]["lifetime_value"]
        if len(subset) == 0:
            continue
        fig3.add_trace(go.Box(
            y=subset,
            name=seg,
            marker=dict(color=seg_colors.get(seg, "#6C757D")),
            boxmean="sd",
            hovertemplate="<b>%{x}</b><br>Value: $%{y:,.2f}<extra></extra>",
        ))

    fig3.update_layout(
        height=400,
        yaxis=dict(title=dict(text="Lifetime Value ($)", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        xaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=12, weight=600, color="#212529")),
        margin=dict(l=10, r=20, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
        showlegend=False,
    )

    st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

with col4:
    st.markdown('<div class="section-title">Customer Acquisition Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Monthly new customer additions</div>', unsafe_allow_html=True)

    acq_trend = df_f.groupby("acquisition_month").size().reset_index(name="count")
    acq_trend = acq_trend.sort_values("acquisition_month")

    fig4 = go.Figure()

    fig4.add_trace(go.Bar(
        x=acq_trend["acquisition_month"],
        y=acq_trend["count"],
        marker=dict(
            color="#0D6EFD",
            line=dict(color="rgba(255,255,255,0.6)", width=1),
            opacity=0.95
        ),
        hovertemplate="<b>%{x}</b><br>New Customers: %{y:,}<extra></extra>",
        width=0.65,
    ))

    fig4.update_layout(
        height=400,
        xaxis=dict(
            title="",
            gridcolor="#E9ECEF",
            tickfont=dict(size=11, color="#495057"),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="New Customers", font=dict(size=12, color="#212529")),
            gridcolor="#E9ECEF",
            tickfont=dict(size=11, color="#495057"),
            zerolinecolor="#DEE2E6"
        ),
        margin=dict(l=10, r=20, t=10, b=40),
        template="plotly_white",
        plot_bgcolor="rgba(255,255,255,0.95)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.15,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_color="#212529",
            bordercolor="#E9ECEF"
        ),
    )

    st.plotly_chart(fig4, width='stretch', config={"displayModeBar": False})

st.markdown("""
    <div style="margin-top: 24px;">
        <div class="section-title">Top Customers by Lifetime Value</div>
    </div>
""", unsafe_allow_html=True)

top_cust = (df_f
    .sort_values("lifetime_value", ascending=False)
    .head(10)[["customer_id", "region", "segment", "lifetime_value",
               "total_purchases", "avg_rating", "is_active"]]
    .copy()
)
top_cust["lifetime_value"] = top_cust["lifetime_value"].apply(lambda x: f"${x:,.2f}")
top_cust["is_active"] = top_cust["is_active"].map({True: "Active", False: "Inactive"})
top_cust.columns = ["Customer ID", "Region", "Segment", "LTV", "Purchases", "Rating", "Status"]
top_cust.index = range(1, len(top_cust) + 1)

st.dataframe(top_cust, width='stretch', height=280)

with st.expander("Detailed Customer Data", expanded=False):
    display_cols = ["customer_id", "region", "segment", "acquisition_date",
                    "lifetime_value", "total_purchases", "avg_rating",
                    "is_active", "churned", "support_tickets"]
    st.dataframe(
        df_f[display_cols].sort_values("acquisition_date", ascending=False).reset_index(drop=True),
        width='stretch', height=300)

st.markdown("""
    <div style="margin-top: 32px; padding: 16px 0; text-align: center;">
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(13,110,253,0.3), transparent);
                    margin-bottom: 16px;"></div>
        <div style="font-size: 12px; color: #ADB5BD;">
            Data Source: CRM System  &middot;  Updated Monthly
        </div>
    </div>
""", unsafe_allow_html=True)
