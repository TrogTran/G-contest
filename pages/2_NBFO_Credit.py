import os
import re
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import (
    PERSONA_COLORS,
    PLOTLY_LAYOUT,
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
    n = os.path.join(DATA_DIR, "nbfo_target_list.csv")
    if not (os.path.exists(n) and os.path.getsize(n) > 10):
        st.error("nbfo_target_list.csv is empty or missing.")
        st.stop()
    df = pd.read_csv(n)

    p = os.path.join(DATA_DIR, "cx_persona_segments.csv")
    if os.path.exists(p) and os.path.getsize(p) > 10:
        df = df.merge(
            pd.read_csv(p)[
                ["CUSTOMER_NUMBER", "persona", "cluster", "total_annual_outflow"]
            ],
            on="CUSTOMER_NUMBER",
            how="left",
        )

    a = os.path.join(DATA_DIR, "alert_list_security.csv")
    if os.path.exists(a):
        df = df.merge(
            pd.read_csv(a)[["CUSTOMER_NUMBER", "anomaly_score", "priority"]],
            on="CUSTOMER_NUMBER",
            how="left",
        )

    # Extract product type from nbfo_message
    def extract_product(msg):
        if not isinstance(msg, str):
            return "Other"
        if re.search(r"thẻ tín dụng|credit card", msg, re.I):
            return "Credit Card"
        if re.search(r"vay tiêu dùng|consumer loan|vay", msg, re.I):
            return "Consumer Loan"
        return "Other"

    if "nbfo_message" in df.columns:
        df["product_type"] = df["nbfo_message"].apply(extract_product)

    return df


df = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────────────────
st.sidebar.markdown("### Filters")
sel_hungry = st.sidebar.radio(
    "Credit Status", ["All", "Credit Hungry Only", "Non-Hungry"], index=0
)
prop_min, prop_max = (
    float(df["credit_propensity"].min()),
    float(df["credit_propensity"].max()),
)
sel_prop = st.sidebar.slider(
    "Propensity Score", prop_min, prop_max, (prop_min, prop_max), step=0.01
)
if "product_type" in df.columns:
    pt_opts = ["All"] + sorted(df["product_type"].dropna().unique().tolist())
    sel_pt = st.sidebar.selectbox("Product Type", pt_opts)
else:
    sel_pt = "All"
if "persona" in df.columns:
    p_opts = ["All"] + sorted(df["persona"].dropna().unique().tolist())
    sel_persona = st.sidebar.selectbox("Persona", p_opts)
else:
    sel_persona = "All"

# ── FILTER ─────────────────────────────────────────────────────────────────
f = df.copy()
if sel_hungry == "Credit Hungry Only":
    f = f[f["credit_hungry"] == 1]
elif sel_hungry == "Non-Hungry":
    f = f[f["credit_hungry"] == 0]
f = f[(f["credit_propensity"] >= sel_prop[0]) & (f["credit_propensity"] <= sel_prop[1])]
if sel_pt != "All" and "product_type" in f.columns:
    f = f[f["product_type"] == sel_pt]
if sel_persona != "All" and "persona" in f.columns:
    f = f[f["persona"] == sel_persona]

# ── HEADER ─────────────────────────────────────────────────────────────────
page_nav = st.columns(4)
with page_nav[0]:
    st.page_link("pages/0_Overview.py", label="Overview", icon="📊")
with page_nav[1]:
    st.page_link("pages/1_Customer_Segments.py", label="Segments", icon="👥")
with page_nav[2]:
    st.page_link("pages/2_NBFO_Credit.py", label="NBFO & Credit", icon="💳", disabled=True)
with page_nav[3]:
    st.page_link("pages/3_Security_Alerts.py", label="Security", icon="🔒")

page_header(
    eyebrow="Customer Intelligence · Next Best Financial Offer",
    title="NBFO & Credit Targeting",
    subtitle="Propensity scoring, product mix, and credit opportunity prioritization",
    record_label="customers in view",
    record_count=f"{len(f):,} / {len(df):,}",
)

# ── KPIs ───────────────────────────────────────────────────────────────────
targeted_n = len(f)
hungry_n = int(f["credit_hungry"].sum())
avg_prop = f["credit_propensity"].mean()
high_prop_n = int((f["credit_propensity"] >= 0.8).sum())
avg_ir = f["ir_query_count"].mean() if "ir_query_count" in f.columns else 0
avg_outflow_m = (
    f["total_annual_outflow"].mean() / 1e6 if "total_annual_outflow" in f.columns else 0
)

kpi_row(
    [
        {"label": "Targeted Customers", "value": f"{targeted_n:,}", "accent": "navy"},
        {
            "label": "Credit Hungry",
            "value": f"{hungry_n:,}",
            "accent": "red",
            "delta": f"{hungry_n / targeted_n * 100:.1f}% of targeted"
            if targeted_n
            else "",
        },
        {
            "label": "Avg Propensity Score",
            "value": f"{avg_prop:.3f}",
            "accent": "amber",
        },
        {
            "label": "High Propensity ≥ 0.8",
            "value": f"{high_prop_n:,}",
            "accent": "green",
        },
        {"label": "Avg IR Query Count", "value": f"{avg_ir:.1f}", "accent": "teal"},
        {
            "label": "Avg Annual Outflow",
            "value": f"{avg_outflow_m:.1f}M",
            "accent": "gold",
        },
    ]
)

if high_prop_n > 0:
    insight(
        f"<b>{high_prop_n:,} customers</b> hold propensity ≥ 0.8 — prime candidates for "
        f"immediate outreach. Of these, {int((f[f['credit_propensity'] >= 0.8]['credit_hungry'] == 1).sum()):,} "
        f"are also classified as Credit Hungry."
    )

# ── ROW 1: Propensity dist + Product mix ───────────────────────────────────
section_title("Propensity & Product Analysis")
c1, c2 = st.columns(2)

with c1:
    chart_wrap("Credit Propensity Distribution", "All customers in filtered view")
    fig1 = px.histogram(
        f,
        x="credit_propensity",
        nbins=40,
        color_discrete_sequence=[C_TEAL],
        opacity=0.9,
    )
    fig1.add_vline(
        x=0.8,
        line_dash="dash",
        line_color=C_RED,
        annotation_text="0.8 threshold",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color=C_RED,
    )
    fig1.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "xaxis_title": "Credit Propensity",
            "yaxis_title": "Count",
            "showlegend": False,
            "bargap": 0.04,
        }
    )
    st.plotly_chart(fig1, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

with c2:
    if "product_type" in f.columns:
        chart_wrap("NBFO Product Mix", "Recommended product distribution")
        pt = f["product_type"].value_counts().reset_index()
        pt.columns = ["product_type", "count"]
        fig2 = px.pie(
            pt,
            values="count",
            names="product_type",
            hole=0.45,
            color_discrete_sequence=[C_NAVY, C_TEAL, C_AMBER],
        )
        fig2.update_traces(
            textposition="outside",
            textinfo="percent+label",
            textfont_size=11,
            marker_line_width=2,
            marker_line_color="white",
        )
        fig2.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "showlegend": False,
                "margin": dict(t=20, b=20, l=20, r=20),
            }
        )
        st.plotly_chart(
            fig2, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )
    else:
        st.info("Product type data not available.")

st.divider()

# ── ROW 2: NBFO by persona + Outflow vs propensity ────────────────────────
section_title("Persona-Level Opportunity")
c3, c4 = st.columns(2)

with c3:
    if "persona" in f.columns and "product_type" in f.columns:
        chart_wrap("NBFO Recommendations by Persona", "Stacked by product type")
        stack = f.groupby(["persona", "product_type"]).size().reset_index(name="count")
        fig3 = px.bar(
            stack,
            x="count",
            y="persona",
            color="product_type",
            orientation="h",
            barmode="stack",
            color_discrete_sequence=[C_NAVY, C_TEAL, C_AMBER],
        )
        fig3.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "xaxis_title": "Customers",
                "yaxis_title": "",
            }
        )
        st.plotly_chart(
            fig3, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )
    elif "persona" in f.columns:
        chart_wrap("Avg Propensity by Persona")
        ap = f.groupby("persona")["credit_propensity"].mean().reset_index()
        fig3 = px.bar(
            ap.sort_values("credit_propensity"),
            x="credit_propensity",
            y="persona",
            orientation="h",
            color="persona",
            color_discrete_map=PERSONA_COLORS,
            text="credit_propensity",
        )
        fig3.update_traces(
            texttemplate="%{text:.3f}", textposition="outside", textfont_size=10
        )
        fig3.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "showlegend": False,
                "xaxis_title": "Avg Propensity",
                "yaxis_title": "",
                "xaxis_range": [0, 1],
            }
        )
        st.plotly_chart(
            fig3, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )

with c4:
    if "total_annual_outflow" in f.columns:
        chart_wrap(
            "Outflow Trend vs Propensity",
            "Slope = growth direction · size = propensity",
        )
        sample = f.sample(min(2000, len(f)), random_state=42)
        color_col = "persona" if "persona" in sample.columns else None
        fig4 = px.scatter(
            sample,
            x="outflow_trend_slope",
            y="credit_propensity",
            color=color_col,
            color_discrete_map=PERSONA_COLORS,
            opacity=0.55,
            hover_data=["CUSTOMER_NUMBER"],
            labels={
                "outflow_trend_slope": "Outflow Trend Slope",
                "credit_propensity": "Propensity",
            },
        )
        fig4.add_hline(
            y=0.8,
            line_dash="dash",
            line_color=C_RED,
            annotation_text="0.8 cutoff",
            annotation_font_size=9,
        )
        fig4.update_layout(**{**PLOTLY_LAYOUT, "height": 300})
        st.plotly_chart(
            fig4, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )
    else:
        st.info("Outflow trend data not available.")

# ── TOP TARGETS TABLE ──────────────────────────────────────────────────────
st.divider()
section_title(
    "Priority Target List", pill=f"Top {min(30, len(f))} · sorted by propensity"
)

show_cols = ["CUSTOMER_NUMBER", "credit_propensity", "credit_hungry", "ir_query_count"]
if "persona" in f.columns:
    show_cols.insert(1, "persona")
if "product_type" in f.columns:
    show_cols.append("product_type")
if "outflow_trend_slope" in f.columns:
    show_cols.append("outflow_trend_slope")
if "priority" in f.columns:
    show_cols.append("priority")

top = (
    f.sort_values("credit_propensity", ascending=False)
    .head(30)[[c for c in show_cols if c in f.columns]]
    .reset_index(drop=True)
)

st.dataframe(
    top,
    width='stretch',
    height=460,
    column_config={
        "credit_propensity": st.column_config.ProgressColumn(
            "Credit Propensity", min_value=0, max_value=1, format="%.3f"
        ),
        "credit_hungry": st.column_config.CheckboxColumn("Credit Hungry"),
    },
)

csv = top.to_csv(index=False).encode("utf-8")
st.download_button("Download Target List (CSV)", csv, "nbfo_targets.csv", "text/csv")
