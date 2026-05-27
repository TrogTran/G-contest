import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Product Performance",
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
def generate_product_data(n_products=50, seed=42):
    np.random.seed(seed)
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Sports"]
    product_names = {
        "Electronics": ["Wireless Headphones", "Bluetooth Speaker", "USB-C Hub", "Laptop Stand",
                        "Portable Charger", "Webcam HD", "Mechanical Keyboard", "Smartwatch Band",
                        "Tablet Case", "Noise Cancelling Earbuds"],
        "Clothing": ["Cotton T-Shirt", "Denim Jacket", "Running Shoes", "Wool Sweater",
                     "Canvas Sneakers", "Leather Belt", "Casual Blazer", "Athletic Shorts",
                     "Formal Shirt", "Winter Parka"],
        "Home & Kitchen": ["Coffee Maker", "Blender Pro", "Cast Iron Pan", "Kitchen Knife Set",
                           "Air Fryer", "Cutting Board Set", "Glass Food Containers", "Electric Kettle",
                           "Toaster Oven", "Measuring Cup Set"],
        "Books": ["Data Science Handbook", "Machine Learning Basics", "Python for Finance",
                  "Deep Learning Guide", "Statistics Essentials", "Algorithm Design",
                  "Business Analytics", "SQL Cookbook", "Cloud Architecture", "Cybersecurity 101"],
        "Sports": ["Yoga Mat Premium", "Resistance Bands", "Dumbbell Set 20lb", "Jump Rope Pro",
                   "Foam Roller", "Water Bottle 32oz", "Gym Towel Set", "Pull-Up Bar",
                   "Adjustable Bench", "Skipping Rope Speed"],
    }

    rows = []
    for cat in categories:
        names = product_names[cat]
        for name in names:
            price = round(np.random.uniform(9.99, 499.99), 2)
            cost = round(price * np.random.uniform(0.35, 0.65), 2)
            profit_margin = round((price - cost) / price * 100, 1)
            units_sold = int(np.random.negative_binomial(3, 0.08))
            revenue = round(price * units_sold, 2)
            profit = round((price - cost) * units_sold, 2)
            rating = round(np.clip(np.random.normal(4.0, 0.5), 1.0, 5.0), 1)
            stock = int(np.random.randint(0, 500))
            rows.append({
                "product_name": name,
                "category": cat,
                "price": price,
                "cost": cost,
                "profit_margin": profit_margin,
                "units_sold": units_sold,
                "revenue": revenue,
                "profit": profit,
                "rating": rating,
                "stock_remaining": stock,
            })
    df = pd.DataFrame(rows)
    return df

df_prod = generate_product_data()

categories = ["All"] + sorted(df_prod["category"].unique().tolist())
sel_cat = st.sidebar.multiselect("Category", categories[1:])

price_min = float(df_prod["price"].min())
price_max = float(df_prod["price"].max())
sel_price = st.sidebar.slider("Price Range ($)", price_min, price_max, (price_min, price_max), 5.0)

min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 1.0, 0.5)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="color: rgba(255,255,255,0.3); font-size: 11px; text-align: center; padding: 12px 0;">
        50 products across 5 categories
    </div>
""", unsafe_allow_html=True)

df_f = df_prod.copy()
if sel_cat:
    df_f = df_f[df_f["category"].isin(sel_cat)]
df_f = df_f[(df_f["price"] >= sel_price[0]) & (df_f["price"] <= sel_price[1])]
df_f = df_f[df_f["rating"] >= min_rating]

total_revenue = df_f["revenue"].sum()
total_units = df_f["units_sold"].sum()
avg_margin = round(df_f["profit_margin"].mean(), 1) if len(df_f) > 0 else 0
top_product = df_f.loc[df_f["revenue"].idxmax(), "product_name"] if len(df_f) > 0 else "N/A"
top_revenue = df_f["revenue"].max() if len(df_f) > 0 else 0

st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
        <div style="font-size: 22px; font-weight: 700; color: #212529;">Product Performance</div>
        <div style="font-size: 13px; color: #6C757D;">Sales, margins, and product profitability</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-grid" style="margin-top: 16px;">
    <div class="metric-card metric-blue">
        <div class="label">Total Revenue</div>
        <div class="value">${total_revenue:,.0f}</div>
        <div class="delta">Across {len(df_f)} products</div>
    </div>
    <div class="metric-card metric-green" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
        <div class="label">Units Sold</div>
        <div class="value">{total_units:,}</div>
        <div class="delta">{total_units / len(df_f):.0f} avg per product</div>
    </div>
    <div class="metric-card metric-orange">
        <div class="label">Avg Profit Margin</div>
        <div class="value">{avg_margin}%</div>
        <div class="delta">{avg_margin - 48.2:+.1f} pp vs target</div>
    </div>
    <div class="metric-card metric-red">
        <div class="label">Top Product</div>
        <div class="value" style="font-size: 18px;">{top_product}</div>
        <div class="delta">${top_revenue:,.0f} in revenue</div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Highest-grossing products in selected categories</div>', unsafe_allow_html=True)

    top10 = df_f.sort_values("revenue", ascending=False).head(10)
    top10 = top10.sort_values("revenue", ascending=True)

    cat_color_map = {
        "Electronics": "#0D6EFD",
        "Clothing": "#4facfe",
        "Home & Kitchen": "#6C9BCF",
        "Books": "#93C5FD",
        "Sports": "#B8D4FE",
    }
    bar_colors = [cat_color_map.get(c, "#6C757D") for c in top10["category"]]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=top10["revenue"],
        y=top10["product_name"],
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(color="white", width=2),
            opacity=0.9,
        ),
        text=top10["revenue"].apply(lambda x: f"${x:,.0f}"),
        textposition="outside",
        textfont=dict(size=12, weight=700, color="#212529"),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<br>Category: %{customdata}<extra></extra>",
        customdata=top10["category"],
        width=0.6,
    ))

    fig1.update_layout(
        height=420,
        xaxis=dict(title=dict(text="Revenue ($)", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=11, weight=600, color="#212529")),
        margin=dict(l=10, r=80, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig1, width='stretch', config={"displayModeBar": False})

with col2:
    st.markdown('<div class="section-title">Revenue Share by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Proportion of total revenue per category</div>', unsafe_allow_html=True)

    cat_rev = df_f.groupby("category")["revenue"].sum().reset_index()
    cat_rev = cat_rev.sort_values("revenue", ascending=False)

    fig2 = go.Figure()
    fig2.add_trace(go.Pie(
        labels=cat_rev["category"],
        values=cat_rev["revenue"],
        marker=dict(
            colors=["#0D6EFD", "#4facfe", "#6C9BCF", "#93C5FD", "#B8D4FE"],
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

    fig2.update_layout(
        height=420,
        margin=dict(l=10, r=180, t=10, b=10),
        template="plotly_white",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown('<div class="section-title">Profit vs Units Sold</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Scatter matrix: margin efficiency by product</div>', unsafe_allow_html=True)

    cat_color_map_scatter = {
        "Electronics": "#0D6EFD",
        "Clothing": "#4facfe",
        "Home & Kitchen": "#6C9BCF",
        "Books": "#93C5FD",
        "Sports": "#B8D4FE",
    }
    scatter_colors = [cat_color_map_scatter.get(c, "#6C757D") for c in df_f["category"]]

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_f["profit"],
        y=df_f["units_sold"],
        mode="markers",
        marker=dict(
            color=scatter_colors,
            size=df_f["profit_margin"] * 1.2,
            sizemode="area",
            sizeref=2.0 * max(df_f["profit_margin"]) / (20**2),
            sizemin=6,
            line=dict(color="white", width=1.5),
            opacity=0.8,
        ),
        text=df_f["product_name"],
        hovertemplate="<b>%{text}</b><br>Profit: $%{x:,.0f}<br>Units Sold: %{y:,}<br>Margin: %{customdata}%<extra></extra>",
        customdata=df_f["profit_margin"],
    ))

    fig3.add_hline(
        y=df_f["units_sold"].median(),
        line_dash="dash",
        line_color="#DC3545",
        line_width=1.5,
        opacity=0.5,
        annotation_text="Median Units",
        annotation_position="bottom right",
        annotation_font=dict(size=11, color="#DC3545", weight=500),
    )

    fig3.add_vline(
        x=df_f["profit"].median(),
        line_dash="dash",
        line_color="#DC3545",
        line_width=1.5,
        opacity=0.5,
        annotation_text="Median Profit",
        annotation_position="top left",
        annotation_font=dict(size=11, color="#DC3545", weight=500),
    )

    fig3.update_layout(
        height=400,
        xaxis=dict(title=dict(text="Profit ($)", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title=dict(text="Units Sold", font=dict(size=12, color="#212529")),
                   gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        margin=dict(l=10, r=20, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
        showlegend=False,
    )

    st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

with col4:
    st.markdown('<div class="section-title">Product Ratings Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Average rating breakdown by category</div>', unsafe_allow_html=True)

    rating_by_cat = df_f.groupby("category").agg(
        avg_rating=("rating", "mean"),
        count=("rating", "count")
    ).reset_index()
    rating_by_cat = rating_by_cat.sort_values("avg_rating", ascending=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=rating_by_cat["avg_rating"],
        y=rating_by_cat["category"],
        orientation="h",
        marker=dict(
            color=["#0D6EFD", "#4facfe", "#6C9BCF", "#93C5FD", "#B8D4FE"][:len(rating_by_cat)],
            line=dict(color="white", width=2),
            opacity=0.9,
        ),
        text=rating_by_cat["avg_rating"].apply(lambda x: f"{x:.1f}"),
        textposition="outside",
        textfont=dict(size=13, weight=700, color="#212529"),
        hovertemplate="<b>%{y}</b><br>Rating: %{x:.1f}<br>Products: %{customdata}<extra></extra>",
        customdata=rating_by_cat["count"],
        width=0.6,
        error_x=None,
    ))

    fig4.add_vline(
        x=4.0,
        line_dash="dash",
        line_color="#198754",
        line_width=2,
        annotation_text="Target 4.0",
        annotation_position="top right",
        annotation_font=dict(size=12, color="#198754", weight=600),
    )

    fig4.update_layout(
        height=400,
        xaxis=dict(title=dict(text="Avg Rating", font=dict(size=12, color="#212529")),
                   range=[0, 5], gridcolor="#F1F3F5", tickfont=dict(size=11, color="#212529")),
        yaxis=dict(title="", gridcolor="#F1F3F5", tickfont=dict(size=12, weight=600, color="#212529")),
        margin=dict(l=10, r=40, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig4, width='stretch', config={"displayModeBar": False})

st.markdown("""
    <div style="margin-top: 24px;">
        <div class="section-title">Product Catalog Summary</div>
    </div>
""", unsafe_allow_html=True)

summary = df_f.sort_values("revenue", ascending=False)[
    ["product_name", "category", "price", "units_sold", "revenue", "profit_margin", "rating"]
].copy()
summary["price"] = summary["price"].apply(lambda x: f"${x:.2f}")
summary["revenue"] = summary["revenue"].apply(lambda x: f"${x:,.0f}")
summary["profit_margin"] = summary["profit_margin"].apply(lambda x: f"{x}%")
summary.columns = ["Product Name", "Category", "Price", "Units Sold", "Revenue", "Profit Margin", "Rating"]
summary.index = range(1, len(summary) + 1)

st.dataframe(summary, width='stretch', height=360)

with st.expander("Detailed Product Data", expanded=False):
    st.dataframe(
        df_f.sort_values("revenue", ascending=False).reset_index(drop=True),
        width='stretch', height=300)

st.markdown("""
    <div style="margin-top: 32px; padding: 16px 0; text-align: center;">
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(13,110,253,0.3), transparent);
                    margin-bottom: 16px;"></div>
        <div style="font-size: 12px; color: #ADB5BD;">
            Data Source: Product Catalog System  &middot;  50 Products Across 5 Categories
        </div>
    </div>
""", unsafe_allow_html=True)
