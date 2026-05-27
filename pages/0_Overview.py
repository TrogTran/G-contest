import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import (
    PERSONA_COLORS,
    PLOTLY_LAYOUT,
    PRIORITY_COLORS,
    C_AMBER,
    C_GREEN,
    C_NAVY,
    C_RED,
    C_TEAL,
    chart_wrap,
    insight,
    kpi_row,
    page_header,
    section_title,
    warn,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "alert_list_security.csv"))
    p = os.path.join(DATA_DIR, "cx_persona_segments.csv")
    if os.path.exists(p) and os.path.getsize(p) > 10:
        df = df.merge(
            pd.read_csv(p), on="CUSTOMER_NUMBER", how="left", suffixes=("", "_p")
        )
    n = os.path.join(DATA_DIR, "nbfo_target_list.csv")
    if os.path.exists(n) and os.path.getsize(n) > 10:
        df = df.merge(
            pd.read_csv(n)[["CUSTOMER_NUMBER", "credit_propensity", "credit_hungry"]],
            on="CUSTOMER_NUMBER",
            how="left",
        )
    return df


df = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────────────────
st.sidebar.markdown("### Filters")
priority_opts = ["All"] + sorted(df["priority"].dropna().unique().tolist())
sel_priority = st.sidebar.selectbox("Alert Level", priority_opts)
flag_opts = sorted(df["rule_flags"].dropna().unique().tolist())
sel_flags = st.sidebar.multiselect("Rule Flags", flag_opts, default=flag_opts)
score_min, score_max = (
    float(df["anomaly_score"].min()),
    float(df["anomaly_score"].max()),
)
sel_score = st.sidebar.slider(
    "Anomaly Score", score_min, score_max, (score_min, score_max), step=0.01
)
persona_opts = ["All"] + (
    sorted(df["persona"].dropna().unique().tolist()) if "persona" in df.columns else []
)
sel_persona = (
    st.sidebar.selectbox("Persona", persona_opts) if "persona" in df.columns else "All"
)

# ── FILTER ─────────────────────────────────────────────────────────────────
f = df.copy()
if sel_priority != "All":
    f = f[f["priority"] == sel_priority]
if sel_flags:
    f = f[f["rule_flags"].isin(sel_flags)]
f = f[(f["anomaly_score"] >= sel_score[0]) & (f["anomaly_score"] <= sel_score[1])]
if sel_persona != "All" and "persona" in f.columns:
    f = f[f["persona"] == sel_persona]

# ── HEADER ─────────────────────────────────────────────────────────────────
page_nav = st.columns(4)
with page_nav[0]:
    st.page_link("pages/0_Overview.py", label="Overview", icon="📊", disabled=True)
with page_nav[1]:
    st.page_link("pages/1_Customer_Segments.py", label="Segments", icon="👥")
with page_nav[2]:
    st.page_link("pages/2_NBFO_Credit.py", label="NBFO & Credit", icon="💳")
with page_nav[3]:
    st.page_link("pages/3_Security_Alerts.py", label="Security", icon="🔒")

page_header(
    eyebrow="Customer Intelligence · Overview",
    title="Executive Dashboard",
    subtitle="Integrated view of anomaly risk, customer segments, and credit opportunity",
    record_label="customers in view",
    record_count=f"{len(f):,} / {len(df):,}",
)

# ── KPIs ───────────────────────────────────────────────────────────────────
total = len(f)
critical_n = int((f["priority"] == "Critical").sum())
alert_n = int((f["priority"] == "Alert").sum())
avg_score = (
    f[f["anomaly_score"] > 0]["anomaly_score"].mean()
    if (f["anomaly_score"] > 0).any()
    else 0
)
avg_burst = f["burst_ratio"].mean() if "burst_ratio" in f.columns else 0
credit_hungry = int(f["credit_hungry"].sum()) if "credit_hungry" in f.columns else 0

kpi_row(
    [
        {"label": "Total Customers", "value": f"{total:,}", "accent": "navy"},
        {
            "label": "Critical Alerts",
            "value": f"{critical_n:,}",
            "accent": "red",
            "delta": f"{critical_n / total * 100:.1f}% of total" if total else "",
        },
        {
            "label": "Alert Flags",
            "value": f"{alert_n:,}",
            "accent": "amber",
            "delta": f"{alert_n / total * 100:.1f}% of total" if total else "",
        },
        {"label": "Avg Anomaly Score", "value": f"{avg_score:.4f}", "accent": "teal"},
        {"label": "Avg Burst Ratio", "value": f"{avg_burst:.2f}", "accent": "gold"},
        {"label": "Credit Hungry", "value": f"{credit_hungry:,}", "accent": "green"},
    ]
)

# Insight callout
flagged_pct = (critical_n + alert_n) / total * 100 if total else 0
if flagged_pct > 5:
    warn(
        f"<b>{flagged_pct:.1f}% of customers</b> carry an active Alert or Critical flag. "
        f"Immediate review recommended for the {critical_n} Critical accounts."
    )
else:
    insight(
        f"<b>{flagged_pct:.1f}% flagged rate</b> — within acceptable threshold. "
        f"Focus review on {critical_n} Critical-priority accounts."
    )

# ── ROW 1: Priority + Persona ──────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    chart_wrap("Alert Priority Distribution", f"{total:,} customers · filtered view")
    pri = f["priority"].value_counts().reset_index()
    pri.columns = ["priority", "count"]
    fig1 = px.pie(
        pri,
        values="count",
        names="priority",
        color="priority",
        color_discrete_map=PRIORITY_COLORS,
        hole=0.5,
    )
    fig1.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont_size=11,
        marker_line_width=2,
        marker_line_color="white",
    )
    fig1.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "showlegend": False,
            "margin": dict(t=20, b=20, l=20, r=20),
        }
    )
    st.plotly_chart(fig1, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

with c2:
    if "persona" in f.columns:
        chart_wrap("Customer Segment Composition", "By behavioral persona cluster")
        pc = f["persona"].value_counts().reset_index()
        pc.columns = ["persona", "count"]
        colors = [PERSONA_COLORS.get(p, C_TEAL) for p in pc["persona"]]
        fig2 = px.bar(
            pc,
            x="count",
            y="persona",
            orientation="h",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            text="count",
        )
        fig2.update_traces(
            textposition="outside", textfont_size=10, marker_line_width=0
        )
        fig2.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "showlegend": False,
                "xaxis_title": "Customers",
                "yaxis_title": "",
                "margin": dict(t=10, b=20, l=8, r=40),
            }
        )
        st.plotly_chart(
            fig2, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )
    else:
        chart_wrap("Rule Flags Distribution")
        rc = f["rule_flags"].value_counts().sort_index().reset_index()
        rc.columns = ["flags", "count"]
        fig2 = px.bar(
            rc, x="flags", y="count", text="count", color_discrete_sequence=[C_TEAL]
        )
        fig2.update_traces(textposition="outside", textfont_size=10)
        fig2.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "showlegend": False,
                "xaxis_title": "Rule Flags",
                "yaxis_title": "Customers",
            }
        )
        st.plotly_chart(
            fig2, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )

st.divider()

# ── ROW 2: Anomaly Score + Burst Scatter ───────────────────────────────────
section_title("Risk Signal Analysis")
c3, c4 = st.columns(2)

with c3:
    chart_wrap("Anomaly Score Distribution", "Flagged customers only (score > 0)")
    nz = f[f["anomaly_score"] > 0]
    fig3 = px.histogram(
        nz,
        x="anomaly_score",
        nbins=40,
        color="priority",
        color_discrete_map=PRIORITY_COLORS,
        barmode="overlay",
        opacity=0.85,
    )
    fig3.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "xaxis_title": "Anomaly Score",
            "yaxis_title": "Count",
            "bargap": 0.04,
        }
    )
    st.plotly_chart(fig3, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

with c4:
    chart_wrap(
        "Burst Ratio vs Anomaly Score", "Sample ≤ 2,000 points · colored by priority"
    )
    sample = f[f["anomaly_score"] > 0].sample(
        min(2000, int((f["anomaly_score"] > 0).sum())), random_state=42
    )
    fig4 = px.scatter(
        sample,
        x="anomaly_score",
        y="burst_ratio",
        color="priority",
        color_discrete_map=PRIORITY_COLORS,
        opacity=0.55,
        size_max=5,
        hover_data=["CUSTOMER_NUMBER"],
    )
    fig4.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "xaxis_title": "Anomaly Score",
            "yaxis_title": "Burst Ratio",
        }
    )
    st.plotly_chart(fig4, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

# ── ROW 3: Credit Propensity (if available) ────────────────────────────────
if "credit_propensity" in f.columns and "persona" in f.columns:
    st.divider()
    section_title("Credit Opportunity", pill="NBFO")
    c5, c6 = st.columns(2)

    with c5:
        chart_wrap("Avg Credit Propensity by Persona", "Higher = stronger product fit")
        prop = (
            f.groupby("persona")["credit_propensity"]
            .mean()
            .reset_index()
            .sort_values("credit_propensity", ascending=True)
        )
        fig5 = px.bar(
            prop,
            x="credit_propensity",
            y="persona",
            orientation="h",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            text="credit_propensity",
        )
        fig5.update_traces(
            texttemplate="%{text:.2f}", textposition="outside", textfont_size=10
        )
        fig5.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 280,
                "showlegend": False,
                "xaxis_title": "Avg Propensity",
                "yaxis_title": "",
                "xaxis_range": [0, 1],
            }
        )
        st.plotly_chart(
            fig5, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )

    with c6:
        chart_wrap(
            "Credit Propensity Distribution", "All customers with propensity score > 0"
        )
        fig6 = px.histogram(
            f[f["credit_propensity"] > 0],
            x="credit_propensity",
            nbins=30,
            color_discrete_sequence=[C_AMBER],
            opacity=0.9,
        )
        fig6.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 280,
                "xaxis_title": "Credit Propensity",
                "yaxis_title": "Count",
                "bargap": 0.04,
            }
        )
        st.plotly_chart(
            fig6, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )

# ── TOP CUSTOMERS TABLE ────────────────────────────────────────────────────
st.divider()
section_title(
    "High-Priority Account List",
    pill=f"Top {min(25, len(f[f['priority'].isin(['Critical', 'Alert'])]))} records",
)

cols = [
    "CUSTOMER_NUMBER",
    "priority",
    "anomaly_score",
    "rule_flags",
    "burst_ratio",
    "offhours_trans_rate",
]
if "persona" in f.columns:
    cols.insert(2, "persona")
if "credit_propensity" in f.columns:
    cols.append("credit_propensity")

top = (
    f[f["priority"].isin(["Critical", "Alert"])]
    .sort_values("anomaly_score", ascending=False)
    .head(25)[[c for c in cols if c in f.columns]]
    .reset_index(drop=True)
)

st.dataframe(
    top,
    width='stretch',
    height=420,
    column_config={
        "anomaly_score": st.column_config.ProgressColumn(
            "Anomaly Score", min_value=0, max_value=1, format="%.4f"
        ),
        "credit_propensity": st.column_config.ProgressColumn(
            "Credit Propensity", min_value=0, max_value=1, format="%.3f"
        ),
        "priority": st.column_config.TextColumn("Priority"),
    },
)

with st.expander("Full dataset view"):
    st.dataframe(
        f[[c for c in cols if c in f.columns]], width='stretch', height=400
    )
