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
    p = os.path.join(DATA_DIR, "cx_persona_segments.csv")
    a = os.path.join(DATA_DIR, "alert_list_security.csv")
    n = os.path.join(DATA_DIR, "nbfo_target_list.csv")

    if not (os.path.exists(p) and os.path.getsize(p) > 10):
        st.error("cx_persona_segments.csv is empty or missing.")
        st.stop()

    df = pd.read_csv(p)
    df_a = pd.read_csv(a)
    df = df.merge(
        df_a[
            [
                "CUSTOMER_NUMBER",
                "anomaly_score",
                "priority",
                "rule_flags",
                "burst_ratio",
            ]
        ],
        on="CUSTOMER_NUMBER",
        how="left",
    )
    if os.path.exists(n) and os.path.getsize(n) > 10:
        df_n = pd.read_csv(n)[["CUSTOMER_NUMBER", "credit_propensity", "credit_hungry"]]
        df = df.merge(df_n, on="CUSTOMER_NUMBER", how="left")
    return df


df = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────────────────
st.sidebar.markdown("### Filters")
personas = sorted(df["persona"].dropna().unique().tolist())
sel_persona = st.sidebar.multiselect("Persona", personas, default=personas)
clusters = sorted(df["cluster"].dropna().unique().tolist())
sel_cluster = st.sidebar.multiselect(
    "Cluster", [int(c) for c in clusters], default=[int(c) for c in clusters]
)
am_min, am_max = int(df["active_months"].min()), int(df["active_months"].max())
sel_months = st.sidebar.slider("Active Months", am_min, am_max, (am_min, am_max))

# ── FILTER ─────────────────────────────────────────────────────────────────
f = df.copy()
if sel_persona:
    f = f[f["persona"].isin(sel_persona)]
if sel_cluster:
    f = f[f["cluster"].isin(sel_cluster)]
f = f[(f["active_months"] >= sel_months[0]) & (f["active_months"] <= sel_months[1])]

# ── HEADER ─────────────────────────────────────────────────────────────────
page_header(
    eyebrow="Customer Intelligence · Segmentation",
    title="Customer Segment Analysis",
    subtitle="Behavioral clusters, engagement metrics, and risk profiling by persona",
    record_label="customers in view",
    record_count=f"{len(f):,} / {len(df):,}",
)

# ── KPIs ───────────────────────────────────────────────────────────────────
avg_trans = f["total_trans"].mean() if "total_trans" in f.columns else 0
avg_months = f["active_months"].mean()
avg_outflow = (
    f["total_annual_outflow"].mean() / 1e6 if "total_annual_outflow" in f.columns else 0
)
avg_propensity = (
    f["credit_propensity"].mean() if "credit_propensity" in f.columns else 0
)
credit_hungry_n = int(f["credit_hungry"].sum()) if "credit_hungry" in f.columns else 0
flagged_n = (
    int((f["priority"].isin(["Alert", "Critical"])).sum())
    if "priority" in f.columns
    else 0
)

kpi_row(
    [
        {"label": "Customers", "value": f"{len(f):,}", "accent": "navy"},
        {"label": "Avg Transactions", "value": f"{avg_trans:,.0f}", "accent": "teal"},
        {"label": "Avg Active Months", "value": f"{avg_months:.1f}", "accent": "gold"},
        {
            "label": "Avg Annual Outflow",
            "value": f"{avg_outflow:.1f}M",
            "accent": "green",
        },
        {
            "label": "Avg Credit Score",
            "value": f"{avg_propensity:.3f}",
            "accent": "amber",
        },
        {"label": "Credit Hungry", "value": f"{credit_hungry_n:,}", "accent": "teal"},
    ]
)

# ── ROW 1: Segment size + Outflow ─────────────────────────────────────────
section_title("Segment Profile")
c1, c2 = st.columns(2)

with c1:
    chart_wrap("Customers by Persona", "Distribution across behavioral segments")
    pc = f["persona"].value_counts().reset_index()
    pc.columns = ["persona", "count"]
    fig1 = px.bar(
        pc.sort_values("count"),
        x="count",
        y="persona",
        orientation="h",
        color="persona",
        color_discrete_map=PERSONA_COLORS,
        text="count",
    )
    fig1.update_traces(textposition="outside", textfont_size=10, marker_line_width=0)
    fig1.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "showlegend": False,
            "xaxis_title": "Customers",
            "yaxis_title": "",
        }
    )
    st.plotly_chart(fig1, width='stretch', config={"displayModeBar": False})

with c2:
    chart_wrap(
        "Average Annual Outflow by Persona", "VND millions · proxy for customer value"
    )
    if "total_annual_outflow" in f.columns:
        out = f.groupby("persona")["total_annual_outflow"].mean().div(1e6).reset_index()
        out.columns = ["persona", "avg_outflow_M"]
        fig2 = px.bar(
            out.sort_values("avg_outflow_M"),
            x="avg_outflow_M",
            y="persona",
            orientation="h",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            text="avg_outflow_M",
        )
        fig2.update_traces(
            texttemplate="%{text:.1f}M", textposition="outside", textfont_size=10
        )
        fig2.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "showlegend": False,
                "xaxis_title": "Avg Annual Outflow (M VND)",
                "yaxis_title": "",
            }
        )
        st.plotly_chart(
            fig2, width='stretch', config={"displayModeBar": False}
        )
    else:
        st.info("total_annual_outflow column not available.")

st.divider()

# ── ROW 2: Engagement ──────────────────────────────────────────────────────
section_title("Engagement Metrics")
c3, c4 = st.columns(2)

with c3:
    chart_wrap("Login Count Distribution by Persona", "Box plot of login frequency")
    if "login_count" in f.columns:
        fig3 = px.box(
            f,
            x="persona",
            y="login_count",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            points=False,
        )
        fig3.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "showlegend": False,
                "xaxis_title": "",
                "yaxis_title": "Login Count",
            }
        )
        st.plotly_chart(
            fig3, width='stretch', config={"displayModeBar": False}
        )
    else:
        st.info("login_count not available.")

with c4:
    chart_wrap(
        "Transaction Volume Distribution", "Histogram of total_trans per customer"
    )
    if "total_trans" in f.columns:
        fig4 = px.histogram(
            f,
            x="total_trans",
            color="persona",
            nbins=40,
            color_discrete_map=PERSONA_COLORS,
            barmode="overlay",
            opacity=0.75,
        )
        fig4.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "xaxis_title": "Total Transactions",
                "yaxis_title": "Count",
                "bargap": 0.04,
            }
        )
        st.plotly_chart(
            fig4, width='stretch', config={"displayModeBar": False}
        )
    else:
        st.info("total_trans not available.")

st.divider()

# ── ROW 3: Alert rate + Credit propensity ─────────────────────────────────
section_title("Risk & Credit Overlay")
c5, c6 = st.columns(2)

with c5:
    if "priority" in f.columns:
        chart_wrap("Alert Rate by Persona", "% of customers flagged Alert or Critical")
        ar = (
            f.groupby("persona")["priority"]
            .apply(lambda x: (x.isin(["Alert", "Critical"])).mean() * 100)
            .reset_index()
        )
        ar.columns = ["persona", "alert_rate"]
        fig5 = px.bar(
            ar.sort_values("alert_rate"),
            x="alert_rate",
            y="persona",
            orientation="h",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            text="alert_rate",
        )
        fig5.update_traces(
            texttemplate="%{text:.1f}%", textposition="outside", textfont_size=10
        )
        fig5.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 280,
                "showlegend": False,
                "xaxis_title": "Flagged %",
                "yaxis_title": "",
                "xaxis_range": [0, ar["alert_rate"].max() * 1.3],
            }
        )
        st.plotly_chart(
            fig5, width='stretch', config={"displayModeBar": False}
        )
    else:
        st.info("Priority data not available.")

with c6:
    if "credit_propensity" in f.columns:
        chart_wrap(
            "Credit Propensity by Persona", "Avg score — higher = stronger credit fit"
        )
        cp = f.groupby("persona")["credit_propensity"].mean().reset_index()
        cp.columns = ["persona", "avg_propensity"]
        fig6 = px.bar(
            cp.sort_values("avg_propensity"),
            x="avg_propensity",
            y="persona",
            orientation="h",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            text="avg_propensity",
        )
        fig6.update_traces(
            texttemplate="%{text:.3f}", textposition="outside", textfont_size=10
        )
        fig6.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 280,
                "showlegend": False,
                "xaxis_title": "Avg Credit Propensity",
                "yaxis_title": "",
                "xaxis_range": [0, 1],
            }
        )
        st.plotly_chart(
            fig6, width='stretch', config={"displayModeBar": False}
        )
    else:
        st.info("credit_propensity not available.")

# ── CLUSTER SUMMARY TABLE ──────────────────────────────────────────────────
st.divider()
section_title("Cluster Summary", pill="by segment")

agg_cols = {
    "total_trans": "mean",
    "active_months": "mean",
    "total_annual_outflow": "mean",
}
agg_cols = {k: v for k, v in agg_cols.items() if k in f.columns}
if "credit_propensity" in f.columns:
    agg_cols["credit_propensity"] = "mean"

summary = (
    f.groupby(["cluster", "persona"])
    .agg({"CUSTOMER_NUMBER": "count", **agg_cols})
    .reset_index()
    .rename(columns={"CUSTOMER_NUMBER": "count"})
)
if "total_annual_outflow" in summary.columns:
    summary["total_annual_outflow"] = (summary["total_annual_outflow"] / 1e6).round(2)
    summary = summary.rename(columns={"total_annual_outflow": "outflow_M"})

st.dataframe(summary, width='stretch', height=300)

with st.expander("Full segment data"):
    st.dataframe(f, width='stretch', height=400)
