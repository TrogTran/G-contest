import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Analysis",
                   layout="wide", initial_sidebar_state="expanded")

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', 'Segoe UI', Roboto, sans-serif !important; }
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
def generate_sales_data(n_days=365, seed=42):
    np.random.seed(seed)
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"]
    channels = ["Online", "In-Store", "Mobile App", "Wholesale"]

    rows = []
    for d in dates:
        for cat in categories:
            daily_revenue = np.random.gamma(shape=2.5, scale=2000)
            daily_orders = max(1, int(np.random.poisson(18)))
            aov = daily_revenue / daily_orders
            channel = np.random.choice(channels)
            profit = daily_revenue * np.random.uniform(0.15, 0.40)
            rows.append({
                "date": d,
                "category": cat,
                "channel": channel,
                "revenue": round(daily_revenue, 2),
                "orders": daily_orders,
                "aov": round(aov, 2),
                "profit": round(profit, 2),
            })
    df = pd.DataFrame(rows)
    return df

df_sales = generate_sales_data()

st.sidebar.markdown("""
    <div style="padding: 12px 0 20px 0; text-align: center;">
        <div style="font-size: 20px; font-weight: 800; color: white; letter-spacing: 0.5px;">Sales Analysis</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase;">Performance Overview</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
    <div style="color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase;
                letter-spacing: 1.5px; margin-bottom: 10px;">Filters</div>
""", unsafe_allow_html=True)

date_min = df_sales["date"].min()
date_max = df_sales["date"].max()
sel_dates = st.sidebar.date_input("Date Range",
    [date_min, date_max],
    min_value=date_min, max_value=date_max)

categories = ["All"] + sorted(df_sales["category"].unique().tolist())
sel_cat = st.sidebar.selectbox("Category", categories)

channels = ["All"] + sorted(df_sales["channel"].unique().tolist())
sel_chan = st.sidebar.selectbox("Channel", channels)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="color: rgba(255,255,255,0.3); font-size: 11px; text-align: center; padding: 12px 0;">
        Transaction data since Jan 2024
    </div>
""", unsafe_allow_html=True)

df_f = df_sales.copy()
if len(sel_dates) == 2:
    mask = (df_f["date"] >= pd.Timestamp(sel_dates[0])) & (df_f["date"] <= pd.Timestamp(sel_dates[1]))
    df_f = df_f[mask]
if sel_cat != "All":
    df_f = df_f[df_f["category"] == sel_cat]
if sel_chan != "All":
    df_f = df_f[df_f["channel"] == sel_chan]

total_revenue = df_f["revenue"].sum()
total_orders = df_f["orders"].sum()
aov = round(total_revenue / total_orders, 2) if total_orders > 0 else 0

df_prev = df_sales.copy()
if len(sel_dates) == 2:
    span = (pd.Timestamp(sel_dates[1]) - pd.Timestamp(sel_dates[0])).days
    prev_end = pd.Timestamp(sel_dates[0]) - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=span)
    mask_p = (df_prev["date"] >= prev_start) & (df_prev["date"] <= prev_end)
    df_prev = df_prev[mask_p]
    if sel_cat != "All":
        df_prev = df_prev[df_prev["category"] == sel_cat]
    if sel_chan != "All":
        df_prev = df_prev[df_prev["channel"] == sel_chan]
else:
    df_prev = df_prev[df_prev["date"] < df_prev["date"].min() + pd.Timedelta(days=30)]

prev_revenue = df_prev["revenue"].sum()
growth = round((total_revenue - prev_revenue) / prev_revenue * 100, 1) if prev_revenue > 0 else 0

prev_orders = df_prev["orders"].sum()
order_growth = round((total_orders - prev_orders) / prev_orders * 100, 1) if prev_orders > 0 else 0

st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
        <div style="font-size: 22px; font-weight: 700; color: #212529;">Sales Analysis</div>
        <div style="font-size: 13px; color: #6C757D;">Revenue, orders, and channel performance</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-grid" style="margin-top: 16px;">
    <div class="metric-card metric-blue">
        <div class="label">Total Revenue</div>
        <div class="value">${total_revenue:,.0f}</div>
        <div class="delta">{growth:+.1f}% vs prior period</div>
    </div>
    <div class="metric-card metric-orange">
        <div class="label">Total Orders</div>
        <div class="value">{total_orders:,}</div>
        <div class="delta">{order_growth:+.1f}% vs prior period</div>
    </div>
    <div class="metric-card metric-purple">
        <div class="label">Avg Order Value</div>
        <div class="value">${aov:,.2f}</div>
        <div class="delta">Across all channels</div>
    </div>
    <div class="metric-card metric-red">
        <div class="label">Revenue Growth</div>
        <div class="value">{growth:+.1f}%</div>
        <div class="delta">{'Above target' if growth > 0 else 'Below target'}</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">Revenue Trend Over Time</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Daily revenue with 7-day rolling average</div>', unsafe_allow_html=True)

    trend = df_f.groupby("date")["revenue"].sum().reset_index()
    trend["rolling_avg"] = trend["revenue"].rolling(7, min_periods=1).mean()

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=trend["date"], y=trend["revenue"],
        mode="lines", name="Daily Revenue",
        line=dict(color="#4facfe", width=1.5),
        hovertemplate="<b>%{x|%b %d}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        opacity=0.6,
    ))
    fig1.add_trace(go.Scatter(
        x=trend["date"], y=trend["rolling_avg"],
        mode="lines", name="7-Day Avg",
        line=dict(color="#0D6EFD", width=3),
        hovertemplate="<b>%{x|%b %d}</b><br>Avg: $%{y:,.0f}<extra></extra>",
    ))

    fig1.update_layout(
        height=400, margin=dict(l=10, r=10, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, font=dict(size=11, color="#212529")),
        xaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title=dict(text="Revenue ($)", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
    )

    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<div class="section-title">Revenue by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Total revenue broken down by segment</div>', unsafe_allow_html=True)

    cat_rev = df_f.groupby("category")["revenue"].sum().reset_index()
    cat_rev = cat_rev.sort_values("revenue", ascending=True)

    cat_colors = ["#0D6EFD", "#4facfe", "#6C9BCF", "#93C5FD", "#B8D4FE"]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=cat_rev["revenue"],
        y=cat_rev["category"],
        orientation="h",
        marker=dict(color=cat_colors[:len(cat_rev)], line=dict(color="white", width=2), opacity=0.9),
        text=cat_rev["revenue"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        textfont=dict(size=13, weight=700, color="#212529"),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
        width=0.6,
    ))

    fig2.update_layout(
        height=400,
        xaxis=dict(title=dict(text="Revenue ($)", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=12, weight=600, color="#212529")),
        margin=dict(l=10, r=60, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown('<div class="section-title">Channel Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Revenue share by sales channel</div>', unsafe_allow_html=True)

    chan_rev = df_f.groupby("channel")["revenue"].sum().reset_index()
    chan_rev = chan_rev.sort_values("revenue", ascending=False)

    fig3 = go.Figure()
    fig3.add_trace(go.Pie(
        labels=chan_rev["channel"],
        values=chan_rev["revenue"],
        marker=dict(
            colors=["#0D6EFD", "#4facfe", "#6C9BCF", "#93C5FD"],
            line=dict(color="white", width=3),
        ),
        textinfo="label+percent",
        textposition="outside",
        hole=0.55,
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        textfont=dict(size=12, color="#212529", weight=600),
        rotation=45,
    ))

    fig3.update_layout(
        height=400,
        margin=dict(l=10, r=180, t=10, b=10),
        template="plotly_white",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with col4:
    st.markdown('<div class="section-title">Top Selling Categories</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Breakdown of orders by product category</div>', unsafe_allow_html=True)

    cat_orders = df_f.groupby("category")["orders"].sum().reset_index()
    cat_orders = cat_orders.sort_values("orders", ascending=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=cat_orders["orders"],
        y=cat_orders["category"],
        orientation="h",
        marker=dict(
            color=cat_orders["orders"],
            colorscale=[[0, "#DBEAFE"], [0.5, "#60A5FA"], [1, "#0D6EFD"]],
            line=dict(color="white", width=2),
            showscale=False,
        ),
        text=cat_orders["orders"],
        textposition="outside",
        textfont=dict(size=14, weight=700, color="#212529"),
        hovertemplate="<b>%{y}</b><br>Orders: %{x:,}<extra></extra>",
        width=0.55,
    ))

    fig4.update_layout(
        height=400,
        xaxis=dict(title=dict(text="Orders", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=12, weight=600, color="#212529")),
        margin=dict(l=10, r=40, t=10, b=10),
        template="plotly_white",
        bargap=0.3,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

st.markdown("""
    <div style="margin-top: 24px;">
        <div class="section-title">Daily Sales Summary</div>
    </div>
""", unsafe_allow_html=True)

summary = df_f.groupby("date").agg(
    Revenue=("revenue", "sum"),
    Orders=("orders", "sum"),
    AOV=("aov", "mean")
).reset_index()
summary["Revenue"] = summary["Revenue"].apply(lambda x: f"${x:,.2f}")
summary["AOV"] = summary["AOV"].apply(lambda x: f"${x:,.2f}")
summary.columns = ["Date", "Revenue", "Orders", "Avg Order Value"]
summary["Date"] = summary["Date"].dt.strftime("%b %d, %Y")
summary.index = range(1, len(summary) + 1)

st.dataframe(summary.tail(15), use_container_width=True, height=320)

with st.expander("Detailed Transaction Data", expanded=False):
    st.dataframe(
        df_f.sort_values("date", ascending=False).reset_index(drop=True),
        use_container_width=True, height=300)

st.markdown("""
    <div style="margin-top: 32px; padding: 16px 0; text-align: center;">
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(13,110,253,0.3), transparent);
                    margin-bottom: 16px;"></div>
        <div style="font-size: 12px; color: #ADB5BD;">
            Data Source: Sales Transactions  &middot;  Updated Daily
        </div>
    </div>
""", unsafe_allow_html=True)
