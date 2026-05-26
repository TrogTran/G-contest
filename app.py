
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Customer Intelligence Dashboard", page_icon=":bar_chart:",
                   layout="wide", initial_sidebar_state="expanded")

# ──────────────────────────────────────────────────
#  CUSTOM CSS — Font, Shadows, Gradients, Dark Sidebar
# ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', 'Segoe UI', Roboto, sans-serif !important; }
    .stExpander details summary span[data-testid="stIconMaterial"] {
        display: none !important;
    }

    .stApp {
        background: #F0F2F6;
    }

    /* ─── SIDEBAR DARK MODE ─── */
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
    section[data-testid="stSidebar"] .stSlider > div > div {
        color: white;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1);
        margin: 16px 0;
    }

    /* ─── METRIC CARDS ─── */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 24px;
    }
    .metric-card {
        border-radius: 20px;
        padding: 22px 24px;
        color: white;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.14);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
        pointer-events: none;
    }
    .metric-card .label {
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        opacity: 0.85;
        margin-bottom: 4px;
    }
    .metric-card .value {
        font-size: 32px;
        font-weight: 800;
        line-height: 1.2;
    }
    .metric-card .delta {
        font-size: 13px;
        font-weight: 500;
        opacity: 0.9;
        margin-top: 2px;
    }
    .metric-blue   { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .metric-orange { background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
    .metric-purple { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }
    .metric-red    { background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%); }

    /* ─── SECTION TITLES ─── */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #1a1a2e;
        margin: 24px 0 16px 0;
        padding-left: 12px;
        border-left: 4px solid #4facfe;
    }
    .section-subtitle {
        font-size: 13px;
        color: #6C757D;
        margin-top: -8px;
        margin-bottom: 16px;
        padding-left: 16px;
    }

    /* ─── DIVIDER ─── */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(79,172,254,0.3), transparent);
        margin: 20px 0;
    }

    /* ─── CHART CARDS — Wrap each chart in a white card ─── */
    div[data-testid="column"] {
        background: white;
        border: 1px solid #E9ECEF;
        border-radius: 16px;
        padding: 16px 20px 12px 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    div[data-testid="column"]:hover {
        box-shadow: 0 8px 28px rgba(0,0,0,0.10);
    }
    div[data-testid="column"] .section-title {
        margin-top: 0;
    }
    div[data-testid="column"] .section-subtitle {
        margin-bottom: 8px;
    }
    div[data-testid="column"] .stPlotlyChart {
        padding-top: 4px;
    }
    div[data-testid="column"] .stCaption {
        padding: 4px 0 0 0;
        font-size: 12px;
        color: #6C757D;
    }

    /* ─── OTHER ─── */
    .stExpander {
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        overflow: visible;
    }
    .stExpander:hover { border-color: #4facfe; }
    .stExpander details {
        overflow: visible;
    }
    .stExpander details summary {
        padding: 12px 44px 12px 16px;
        overflow: visible;
    }
    .stDataFrame { border-radius: 12px; overflow: hidden; border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
    footer { display: none; }
    #MainMenu { visibility: hidden; }

    /* ─── RESPONSIVE FIT ─── */
    @media (max-width: 1200px) {
        .metric-grid { grid-template-columns: repeat(2, 1fr); }
        .metric-card .value { font-size: 26px; }
    }
    @media (max-width: 768px) {
        .metric-grid { grid-template-columns: 1fr; }
        .section-title { font-size: 16px; }
        div[data-testid="column"] { padding: 12px 14px 8px 14px; }
        .metric-card { padding: 16px 18px; }
        .metric-card .value { font-size: 22px; }
    }
    @media (max-width: 576px) {
        .stApp header { padding-top: 0; }
        .main .block-container { padding: 1rem 0.75rem; }
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────
#  SYNTHETIC DATA — 200 customers matching the spec
# ──────────────────────────────────────────────────
@st.cache_data
def generate_data(n=200, seed=42):
    np.random.seed(seed)

    ids = np.random.choice(range(100000, 1000000), n, replace=False)
    propensity = np.random.beta(1.8, 2.7, n)

    # ≈ 61/200 = 30.5% → use 0.305 to approximate the 61 target
    credit_hungry = np.random.binomial(1, 0.305, n)

    irq = np.random.negative_binomial(2, 0.045, n)
    topup = np.where(np.random.random(n) < 0.555, 0,
                     np.random.negative_binomial(2, 0.05, n)).astype(int)

    cluster = np.random.choice([0, 1, 2, 3], n, p=[0.485, 0.408, 0.024, 0.083])
    pm = {0: "Dormant / Churn-risk", 1: "Credit Seeker",
          2: "Wealth Accumulator", 3: "Digital Native"}
    persona = [pm[c] for c in cluster]

    total_trans = np.where(
        cluster == 3, np.random.randint(50, 400, n),
        np.where(cluster == 1, np.random.randint(5, 120, n),
                 np.where(cluster == 2, np.random.randint(2, 200, n),
                          np.random.randint(0, 50, n))))
    avg_amt = np.where(
        cluster == 2, np.random.uniform(50e6, 200e6, n),
        np.where(cluster == 3, np.random.uniform(2e5, 5e6, n),
                 np.random.uniform(5e4, 3e6, n)))
    login_cnt = np.where(
        cluster == 3, np.random.randint(80, 1000, n),
        np.where(cluster == 1, np.random.randint(10, 400, n),
                 np.where(cluster == 2, np.random.randint(10, 300, n),
                          np.random.randint(0, 150, n))))
    active_m = np.where(
        cluster == 3, np.random.randint(4, 12, n),
        np.where(cluster == 1, np.random.randint(1, 10, n),
                 np.where(cluster == 2, np.random.randint(1, 12, n),
                          np.random.randint(0, 8, n))))

    # ≈ 6/200 = 3% critical alerts
    priority = np.random.choice(["Alert", "Critical"], n, p=[0.97, 0.03])
    anomaly = np.where(priority == "Critical",
                       np.random.uniform(0.65, 0.78, n),
                       np.random.uniform(0.54, 0.72, n))
    rule_flags = np.random.choice([1, 2, 3, 4], n, p=[0.568, 0.396, 0.035, 0.001])
    rule_flags = np.where(priority == "Critical",
                          np.clip(rule_flags + 1, 2, 4), rule_flags)

    df = pd.DataFrame({
        "CUSTOMER_NUMBER": ids,
        "credit_propensity": np.round(propensity, 5),
        "credit_hungry": credit_hungry,
        "ir_query_count": irq,
        "topup_count": topup,
        "persona": persona,
        "total_trans": total_trans,
        "avg_amount": np.round(avg_amt, 0).astype(int),
        "login_count": login_cnt,
        "active_months": active_m,
        "anomaly_score": np.round(anomaly, 5),
        "priority": priority,
        "rule_flags": rule_flags,
    })
    df["credit_hungry_label"] = df["credit_hungry"].map(
        {1: "Credit Demand", 0: "No Demand"})
    return df

df = generate_data(200, 42)

# ──────────────────────────────────────────────────
#  SIDEBAR — Dark Mode
# ──────────────────────────────────────────────────
st.sidebar.markdown("""
    <div style="padding: 12px 0 20px 0; text-align: center;">
        <div style="font-size: 20px; font-weight: 800; color: white; letter-spacing: 0.5px;">Intelligence</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase;">Dashboard</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
    <div style="color: rgba(255,255,255,0.5); font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;">
        Filters
    </div>
""", unsafe_allow_html=True)

seg = ["All"] + sorted(df["persona"].unique().tolist())
sel_seg = st.sidebar.selectbox("Customer Profile", seg, label_visibility="collapsed")

sel_hungry = st.sidebar.selectbox(
    "Credit Demand",
    ["All", "Credit Demand", "No Demand"],
    label_visibility="collapsed")

sel_pri = st.sidebar.selectbox(
    "Alert Level",
    ["All"] + sorted(df["priority"].unique().tolist()),
    label_visibility="collapsed")

prop_r = st.sidebar.slider("Propensity Range", 0.0, 1.0, (0.0, 1.0), 0.05)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="color: rgba(255,255,255,0.3); font-size: 11px; text-align: center; padding: 12px 0;">
        200 sample customers &middot; 3 data sources
    </div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────
#  FILTER LOGIC
# ──────────────────────────────────────────────────
df_f = df.copy()
if sel_seg != "All":
    df_f = df_f[df_f["persona"] == sel_seg]
if sel_hungry != "All":
    df_f = df_f[df_f["credit_hungry_label"] == sel_hungry]
if sel_pri != "All":
    df_f = df_f[df_f["priority"] == sel_pri]
df_f = df_f[(df_f["credit_propensity"] >= prop_r[0]) &
            (df_f["credit_propensity"] <= prop_r[1])]

n = len(df_f)
hungry = int(df_f["credit_hungry"].sum())
hpct = round(hungry / n * 100, 1) if n > 0 else 0
ap = round(float(df_f["credit_propensity"].mean()), 3) if n > 0 else 0
crit = int(len(df_f[df_f["priority"] == "Critical"]))

# ──────────────────────────────────────────────────
#  METRIC CARDS — 4 Gradient Cards with HTML
# ──────────────────────────────────────────────────
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
        <div style="font-size: 22px; font-weight: 700; color: #1a1a2e;">Overview</div>
        <div style="font-size: 13px; color: #6C757D;">Financial Behavior Monitoring Dashboard</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="metric-grid" style="margin-top: 16px;">
    <div class="metric-card metric-blue">
        <div class="label">Total Customers</div>
        <div class="value">{n:,}</div>
        <div class="delta">Active customers in the system</div>
    </div>
    <div class="metric-card metric-orange">
        <div class="label">Credit Demand</div>
        <div class="value">{hungry:,} <span style="font-size:16px;font-weight:500;">({hpct}%)</span></div>
        <div class="delta">{hpct - 36.4:+.1f} pp vs baseline</div>
    </div>
    <div class="metric-card metric-purple">
        <div class="label">Avg Propensity Score</div>
        <div class="value">{ap:.3f}</div>
        <div class="delta">{ap - 0.402:+.3f} vs industry avg</div>
    </div>
    <div class="metric-card metric-red">
        <div class="label">Critical Alerts</div>
        <div class="value">{crit:,}</div>
        <div class="delta">{crit - 93:+d} vs baseline average</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────
#  COLOR MAP
# ──────────────────────────────────────────────────
color_map = {
    "Dormant / Churn-risk": "#FF6B6B",
    "Credit Seeker": "#4ECDC4",
    "Digital Native": "#45B7D1",
    "Wealth Accumulator": "#F7DC6F",
}

# ──────────────────────────────────────────────────
#  ROW 1 — Donut + Bar Chart
# ──────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">Customer Profile Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">High dormant ratio requires retention focus</div>', unsafe_allow_html=True)

    segs = df_f["persona"].value_counts().reset_index()
    segs.columns = ["persona", "count"]

    fig1 = go.Figure()

    fig1.add_trace(go.Pie(
        labels=segs["persona"],
        values=segs["count"],
        marker=dict(
            colors=[color_map.get(p, "#6C757D") for p in segs["persona"]],
            line=dict(color="white", width=3),
        ),
        textinfo="label+percent",
        textposition="outside",
        hole=0.55,
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Rate: %{percent}<extra></extra>",
        textfont=dict(size=12, color="#1a1a2e", weight=600),
        rotation=45,
    ))

    fig1.update_layout(
        height=400,
        margin=dict(l=10, r=180, t=10, b=10),
        template="plotly_white",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<div class="section-title">Propensity Score by Segment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Credit Seekers lead with significant gap</div>', unsafe_allow_html=True)

    pb = df_f.groupby("persona")["credit_propensity"].mean().reset_index()
    pb.columns = ["persona", "avg_prop"]
    pb = pb.sort_values("avg_prop")

    bar_colors = [color_map.get(p, "#6C757D") for p in pb["persona"]]

    fig2 = go.Figure()

    fig2.add_trace(go.Bar(
        x=pb["avg_prop"],
        y=pb["persona"],
        orientation="h",
        marker=dict(
            color=bar_colors,
            line=dict(color="white", width=2),
            opacity=0.9,
        ),
        text=pb["avg_prop"].apply(lambda x: f"{x:.3f}"),
        textposition="outside",
        textfont=dict(size=13, weight=700, color="#1a1a2e"),
        hovertemplate="<b>%{y}</b><br>Propensity: %{x:.3f}<extra></extra>",
        width=0.6,
    ))

    fig2.add_vline(
        x=0.5, line_dash="dash", line_color="#DC3545",
        line_width=2,
        annotation_text="Target 0.5",
        annotation_position="top left",
        annotation_font=dict(size=12, color="#DC3545", weight=600),
    )

    fig2.update_layout(
        height=400,
        xaxis=dict(
            title=dict(text="Avg Propensity Score", font=dict(size=12, color="#1a1a2e")),
            range=[0, 0.7],
            gridcolor="#F1F3F5",
            gridwidth=1,
            automargin=True,
            tickfont=dict(size=11, color="#1a1a2e"),
        ),
        yaxis=dict(
            title="",
            gridcolor="#F1F3F5",
            gridwidth=1,
            automargin=True,
            tickfont=dict(size=12, weight=600, color="#1a1a2e"),
        ),
        margin=dict(l=140, r=40, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ──────────────────────────────────────────────────
#  ROW 2 — Histogram + Flags
# ──────────────────────────────────────────────────
col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown('<div class="section-title">Propensity Score Distribution</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Mean: {ap} — Concentrated in 0.2–0.6 range</div>', unsafe_allow_html=True)

    fig3 = go.Figure()

    hist_counts, hist_edges = np.histogram(df_f["credit_propensity"], bins=20)
    hist_centers = (hist_edges[:-1] + hist_edges[1:]) / 2

    fig3.add_trace(go.Bar(
        x=hist_centers,
        y=hist_counts,
        width=hist_edges[1] - hist_edges[0] - 0.005,
        marker=dict(
            color=hist_counts,
            colorscale=[[0, "#DBEAFE"], [0.5, "#60A5FA"], [1, "#2563EB"]],
            line=dict(color="white", width=1),
            showscale=False,
        ),
        hovertemplate="Range: %{x:.3f}<br>Count: %{y:,}<extra></extra>",
    ))

    fig3.add_vline(
        x=ap, line_dash="dot", line_color="#DC3545",
        line_width=2,
        annotation_text=f"Mean: {ap}",
        annotation_position="top right",
        annotation_font=dict(size=12, color="#DC3545", weight=600),
    )

    fig3.update_layout(
        height=400,
        xaxis=dict(
            title=dict(text="Credit Propensity Score", font=dict(size=12, color="#1a1a2e")),
            gridcolor="#F1F3F5",
            automargin=True,
            tickfont=dict(size=11, color="#1a1a2e"),
        ),
        yaxis=dict(
            title=dict(text="Customers", font=dict(size=12, color="#1a1a2e")),
            gridcolor="#F1F3F5",
            automargin=True,
            tickfont=dict(size=11, color="#1a1a2e"),
        ),
        margin=dict(l=50, r=20, t=10, b=10),
        template="plotly_white",
        bargap=0.05,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

with col4:
    st.markdown('<div class="section-title">Alert Flag Distribution</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Critical: {crit} &middot; Regular: {n - crit}</div>', unsafe_allow_html=True)

    flags = df_f["rule_flags"].value_counts().sort_index().reset_index()
    flags.columns = ["rf", "count"]
    flag_labels = ["1 Flag - Low", "2 Flag - Medium", "3 Flag - High", "4 Flag - Critical"]

    flag_colors = ["#DBEAFE", "#93C5FD", "#3B82F6", "#1E3A5F"]

    fig4 = go.Figure()

    fig4.add_trace(go.Bar(
        x=[flag_labels[i - 1] if i <= 4 else f"{i} Flag" for i in flags["rf"]],
        y=flags["count"],
        marker=dict(
            color=[flag_colors[i - 1] if i <= 4 else "#6C757D" for i in flags["rf"]],
            line=dict(color="white", width=2),
        ),
        text=flags["count"],
        textposition="outside",
        textfont=dict(size=14, weight=700, color="#1a1a2e"),
        hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>",
        width=0.55,
    ))

    fig4.update_layout(
        height=400,
        xaxis=dict(
            title="",
            gridcolor="#F1F3F5",
            automargin=True,
            tickfont=dict(size=11, weight=500, color="#1a1a2e"),
        ),
        yaxis=dict(
            title=dict(text="Customers", font=dict(size=12, color="#1a1a2e")),
            gridcolor="#F1F3F5",
            automargin=True,
            tickfont=dict(size=11, color="#1a1a2e"),
        ),
        margin=dict(l=50, r=20, t=10, b=10),
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", font_size=13),
    )

    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ──────────────────────────────────────────────────
#  TABLE — Top 10 Priority Customers
# ──────────────────────────────────────────────────
st.markdown("""
    <div style="margin-top: 24px;">
        <div class="section-title">Top 10 Priority Customers</div>
    </div>
""", unsafe_allow_html=True)

top10 = (df_f
    .sort_values(["anomaly_score", "credit_propensity"], ascending=[False, False])
    .head(10)[["CUSTOMER_NUMBER", "credit_propensity", "priority",
               "rule_flags", "anomaly_score", "ir_query_count", "persona"]]
    .copy()
)
top10["credit_propensity"] = top10["credit_propensity"].apply(lambda x: f"{x:.1%}")
top10["anomaly_score"] = top10["anomaly_score"].apply(lambda x: f"{x:.3f}")
top10.columns = [
    "Customer ID", "Propensity", "Alert Level",
    "Rule Flags", "Anomaly Score", "Inquiries", "Profile"]
top10.index = range(1, len(top10) + 1)

styled = top10.style.map(
    lambda v: "color:#DC3545;font-weight:600;background:#FFF0F0" if v == "Critical"
    else ("color:#D97706;font-weight:600;background:#FFF8E8" if v == "Alert" else ""),
    subset=["Alert Level"])

st.dataframe(styled, use_container_width=True, height=280)

# ──────────────────────────────────────────────────
#  EXPANDER — Raw Data
# ──────────────────────────────────────────────────
with st.expander("Detailed Data", expanded=False):
    st.dataframe(
        df_f[["CUSTOMER_NUMBER", "persona", "credit_propensity",
              "credit_hungry_label", "ir_query_count", "priority",
              "anomaly_score", "rule_flags"]].reset_index(drop=True),
        use_container_width=True,
        height=300)

# ──────────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────────
st.markdown("""
    <div style="margin-top: 32px; padding: 16px 0; text-align: center;">
        <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(79,172,254,0.3), transparent); margin-bottom: 16px;"></div>
        <div style="font-size: 12px; color: #ADB5BD;">
            Data Sources: NBFO Target List  &middot;  CX Persona Segments  &middot;  Alert List Security
        </div>
    </div>
""", unsafe_allow_html=True)
