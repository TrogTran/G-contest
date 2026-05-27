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
            pd.read_csv(p)[["CUSTOMER_NUMBER", "persona", "cluster"]],
            on="CUSTOMER_NUMBER",
            how="left",
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
flagged = df[df["anomaly_score"] > 0].copy()

# â”€â”€ SIDEBAR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.sidebar.markdown("### Filters")
priority_opts = ["All"] + ["Critical", "Alert", "Normal"]
sel_priority = st.sidebar.selectbox("Priority", priority_opts)
flag_vals = sorted(df["rule_flags"].dropna().unique().tolist())
sel_flags = st.sidebar.multiselect(
    "Rule Flags", flag_vals, default=[f for f in flag_vals if f > 0]
)
s_min = float(df[df["anomaly_score"] > 0]["anomaly_score"].min())
s_max = float(df["anomaly_score"].max())
sel_score = st.sidebar.slider("Anomaly Score", s_min, s_max, (s_min, s_max), step=0.005)
if "persona" in df.columns:
    p_opts = ["All"] + sorted(df["persona"].dropna().unique().tolist())
    sel_persona = st.sidebar.selectbox("Persona", p_opts)
else:
    sel_persona = "All"
show_normal = st.sidebar.checkbox("Include Normal in detail table", value=False)

# â”€â”€ FILTER â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
f = df.copy()
if sel_priority != "All":
    f = f[f["priority"] == sel_priority]
if sel_flags:
    f = f[f["rule_flags"].isin(sel_flags)]
f = f[(f["anomaly_score"] >= sel_score[0]) & (f["anomaly_score"] <= sel_score[1])]
if sel_persona != "All" and "persona" in f.columns:
    f = f[f["persona"] == sel_persona]
if not show_normal:
    f = f[f["priority"] != "Normal"]

# â”€â”€ HEADER â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
page_nav = st.columns(4)
with page_nav[0]:
    st.page_link("pages/0_Overview.py", label="Overview")
with page_nav[1]:
    st.page_link("pages/1_Customer_Segments.py", label="Segments")
with page_nav[2]:
    st.page_link("pages/2_NBFO_Credit.py", label="NBFO & Credit")
with page_nav[3]:
    st.page_link("pages/3_Security_Alerts.py", label="Security", disabled=True)

page_header(
    eyebrow="Customer Intelligence Â· Security & Fraud Risk",
    title="Security Alert Investigation",
    subtitle="Anomaly signals, transaction patterns, and high-risk account deep-dive",
    record_label="flagged records in view",
    record_count=f"{len(f):,} / {len(df):,}",
)

# â”€â”€ KPIs â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
total_flagged = int((df["priority"] != "Normal").sum())
critical_n = int((df["priority"] == "Critical").sum())
alert_n = int((df["priority"] == "Alert").sum())
avg_score_all = flagged["anomaly_score"].mean() if len(flagged) else 0
max_score = flagged["anomaly_score"].max() if len(flagged) else 0
avg_burst = flagged["burst_ratio"].mean() if len(flagged) else 0

kpi_row(
    [
        {"label": "Total Flagged", "value": f"{total_flagged:,}", "accent": "navy"},
        {
            "label": "Critical",
            "value": f"{critical_n:,}",
            "accent": "red",
            "delta": f"{critical_n / len(df) * 100:.2f}% of all customers",
        },
        {"label": "Alert", "value": f"{alert_n:,}", "accent": "amber"},
        {
            "label": "Avg Anomaly Score",
            "value": f"{avg_score_all:.4f}",
            "accent": "teal",
        },
        {"label": "Max Anomaly Score", "value": f"{max_score:.4f}", "accent": "red"},
        {"label": "Avg Burst Ratio", "value": f"{avg_burst:.2f}", "accent": "gold"},
    ]
)

if critical_n >= 50:
    warn(
        f"<b>{critical_n} Critical accounts</b> detected. Immediate investigation required â€” "
        f"these customers show anomaly scores above the critical threshold."
    )
else:
    insight(
        f"<b>{critical_n} Critical</b> and <b>{alert_n} Alert</b> accounts flagged. "
        f"Review Critical queue first; max anomaly score is {max_score:.4f}."
    )

# â”€â”€ ROW 1: Priority + Rule Flags â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
section_title("Alert Distribution")
c1, c2 = st.columns(2)

with c1:
    chart_wrap("Priority Distribution â€” All Customers")
    pri = df["priority"].value_counts().reset_index()
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
    chart_wrap(
        "Rule Flags Breakdown â€” Flagged Customers Only",
        "Number of triggered rule conditions",
    )
    rf = flagged["rule_flags"].value_counts().sort_index().reset_index()
    rf.columns = ["rule_flags", "count"]
    rf["label"] = rf["rule_flags"].astype(str) + " flag(s)"
    colors = [C_AMBER if v < 3 else C_RED for v in rf["rule_flags"]]
    fig2 = px.bar(
        rf,
        x="label",
        y="count",
        text="count",
        color="label",
        color_discrete_sequence=colors,
    )
    fig2.update_traces(
        textposition="outside", textfont_size=10, marker_line_width=0, showlegend=False
    )
    fig2.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "showlegend": False,
            "xaxis_title": "",
            "yaxis_title": "Customers",
        }
    )
    st.plotly_chart(fig2, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

st.divider()

# â”€â”€ ROW 2: Score dist + Burst scatter â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
section_title("Risk Signal Analysis")
c3, c4 = st.columns(2)

with c3:
    chart_wrap("Anomaly Score Distribution", "Flagged customers Â· colored by priority")
    fig3 = px.histogram(
        flagged,
        x="anomaly_score",
        color="priority",
        nbins=50,
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
            "bargap": 0.03,
        }
    )
    st.plotly_chart(fig3, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

with c4:
    chart_wrap("Burst Ratio vs Anomaly Score", "Sample â‰¤ 3,000 Â· size = rule flags")
    sample = flagged.sample(min(3000, len(flagged)), random_state=42)
    fig4 = px.scatter(
        sample,
        x="anomaly_score",
        y="burst_ratio",
        color="priority",
        size="rule_flags",
        color_discrete_map=PRIORITY_COLORS,
        opacity=0.55,
        hover_data=["CUSTOMER_NUMBER", "max_single_amount"],
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

st.divider()

# â”€â”€ ROW 3: Transaction amounts â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
section_title("Transaction Amount Profile")
c5, c6 = st.columns(2)

with c5:
    chart_wrap("Max Single Amount by Priority", "Log scale Â· VND")
    fig5 = px.box(
        flagged,
        x="priority",
        y="max_single_amount",
        color="priority",
        color_discrete_map=PRIORITY_COLORS,
        log_y=True,
        points=False,
    )
    fig5.update_layout(
        **{
            **PLOTLY_LAYOUT,
            "height": 300,
            "showlegend": False,
            "xaxis_title": "",
            "yaxis_title": "Max Single Amt (log VND)",
        }
    )
    st.plotly_chart(fig5, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})

with c6:
    if "persona" in flagged.columns:
        chart_wrap("Alerts by Persona", "Stacked Alert + Critical counts")
        ap = flagged.groupby(["persona", "priority"]).size().reset_index(name="count")
        fig6 = px.bar(
            ap,
            x="persona",
            y="count",
            color="priority",
            barmode="stack",
            color_discrete_map=PRIORITY_COLORS,
        )
        fig6.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "xaxis_title": "",
                "yaxis_title": "Flagged Customers",
            }
        )
        st.plotly_chart(
            fig6, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )
    else:
        chart_wrap("Off-Hours Rate vs Anomaly Score")
        s2 = flagged[flagged["offhours_trans_rate"] > 0].sample(
            min(2000, int((flagged["offhours_trans_rate"] > 0).sum())), random_state=1
        )
        fig6 = px.scatter(
            s2,
            x="offhours_trans_rate",
            y="anomaly_score",
            color="priority",
            color_discrete_map=PRIORITY_COLORS,
            opacity=0.55,
        )
        fig6.update_layout(
            **{
                **PLOTLY_LAYOUT,
                "height": 300,
                "xaxis_title": "Off-Hours Rate",
                "yaxis_title": "Anomaly Score",
            }
        )
        st.plotly_chart(
            fig6, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]}
        )

# â”€â”€ DETAIL TABLE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.divider()
section_title("Alert Detail Table", pill=f"{len(f):,} records")

sort_col = st.selectbox(
    "Sort by",
    [
        "anomaly_score",
        "burst_ratio",
        "max_single_amount",
        "max_deviation",
        "offhours_trans_rate",
    ],
    key="sort_col",
)
display_cols = [
    "CUSTOMER_NUMBER",
    "priority",
    "anomaly_score",
    "rule_flags",
    "burst_ratio",
    "offhours_trans_rate",
    "max_deviation",
    "max_single_amount",
    "avg_amount",
]
if "persona" in f.columns:
    display_cols.insert(2, "persona")
if "credit_propensity" in f.columns:
    display_cols.append("credit_propensity")

disp = (
    f[[c for c in display_cols if c in f.columns]]
    .sort_values(sort_col, ascending=False)
    .reset_index(drop=True)
)
for col in ["max_single_amount", "avg_amount"]:
    if col in disp.columns:
        disp[col + "_M"] = (disp[col] / 1e6).round(2)
        disp = disp.drop(columns=[col])

st.dataframe(
    disp,
    width='stretch',
    height=480,
    column_config={
        "anomaly_score": st.column_config.ProgressColumn(
            "Anomaly Score", min_value=0, max_value=1, format="%.4f"
        ),
        "credit_propensity": st.column_config.ProgressColumn(
            "Credit Propensity", min_value=0, max_value=1, format="%.3f"
        ),
    },
)
csv = disp.to_csv(index=False).encode("utf-8")
st.download_button("Download Alert List (CSV)", csv, "security_alerts.csv", "text/csv")

# â”€â”€ CRITICAL DEEP-DIVE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.divider()
section_title("Critical Customer Deep-Dive", pill="Interactive")

crit = df[df["priority"] == "Critical"].sort_values("anomaly_score", ascending=False)
if len(crit) == 0:
    st.info("No critical customers match current filters.")
else:
    sel_cust = st.selectbox(
        f"Select Customer ({len(crit)} critical)",
        crit["CUSTOMER_NUMBER"].tolist(),
        format_func=lambda x: f"#{x}",
    )
    row = crit[crit["CUSTOMER_NUMBER"] == sel_cust].iloc[0]

    d1, d2, d3, d4, d5, d6 = st.columns(6)
    d1.metric("Anomaly Score", f"{row['anomaly_score']:.4f}")
    d2.metric("Rule Flags", int(row["rule_flags"]))
    d3.metric("Burst Ratio", f"{row['burst_ratio']:.3f}")
    d4.metric("Off-Hours Rate", f"{row['offhours_trans_rate']:.3f}")
    d5.metric("Max Amt (M VND)", f"{row['max_single_amount'] / 1e6:.1f}")
    d6.metric("Max Deviation", f"{row['max_deviation']:.2f}x")

    if "persona" in row and not pd.isna(row.get("persona", float("nan"))):
        insight(f"<b>Persona:</b> {row['persona']}")

    metrics = {
        "Anomaly Score": min(row["anomaly_score"] / 1.0, 1.0),
        "Burst Ratio": min(row["burst_ratio"] / 5.0, 1.0),
        "Off-Hours Rate": min(row["offhours_trans_rate"] / 1.0, 1.0),
        "Rule Flags": row["rule_flags"] / 4.0,
        "Max Deviation": min(row["max_deviation"] / 200.0, 1.0),
    }
    cats = list(metrics.keys()) + [list(metrics.keys())[0]]
    vals = list(metrics.values()) + [list(metrics.values())[0]]

    fig_r = go.Figure(
        go.Scatterpolar(
            r=vals,
            theta=cats,
            fill="toself",
            fillcolor="rgba(192,57,43,0.2)",
            line=dict(color=C_RED, width=2),
        )
    )
    fig_r.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickfont_size=9),
            angularaxis=dict(tickfont_size=10),
        ),
        showlegend=False,
        height=340,
        margin=dict(t=40, b=40, l=60, r=60),
        title=dict(text=f"Risk Profile â€” Customer #{sel_cust}", font_size=12, x=0.5),
        paper_bgcolor="white",
        font=dict(family="Inter, Segoe UI, system-ui"),
    )
    st.plotly_chart(fig_r, width='stretch', config={"displaylogo": False, "modeBarButtonsToRemove": ["sendDataToCloud"], "modeBarButtonsToAdd": ["drawline", "eraseshape"]})
