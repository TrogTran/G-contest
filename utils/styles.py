"""
Shared design system — McKinsey/BCG dark-navy style.
"""

import streamlit as st

# ── BRAND COLORS ────────────────────────────────────────────────────────────
C_NAVY = "#1a2744"
C_TEAL = "#006B7D"
C_AMBER = "#E67E22"
C_RED = "#C0392B"
C_GREEN = "#1A7049"
C_GOLD = "#C5933A"
C_BLUE = "#006B7D"
C_LIGHT = "#f7f9fd"

SEQ_TEAL = [C_NAVY, C_TEAL, C_AMBER, C_GREEN, C_RED, "#6c757d"]
SEQ_NAVY = SEQ_TEAL

PRIORITY_COLORS = {"Normal": "#6c757d", "Alert": C_AMBER, "Critical": C_RED}
PERSONA_COLORS = {
    "Dormant/Churn-risk": "#6c757d",
    "Credit Seeker": C_TEAL,
    "Digital Native": C_NAVY,
    "Wealth Accumulator": C_AMBER,
}


# ── PLOTLY SHARED THEME ────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, Segoe UI, system-ui", size=12, color="#4A5568"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=32, b=32, l=12, r=12),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E2E8F0",
        font=dict(size=11, color="#1a2744"),
    ),
    showlegend=True,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=10),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        title=dict(text=""),
    ),
    xaxis=dict(
        gridcolor="#F0F4F8",
        linecolor="#E2E8F0",
        tickfont=dict(size=11),
        zeroline=False,
        showspikes=True,
        spikethickness=1,
        spikecolor="#E2E8F0",
    ),
    yaxis=dict(
        gridcolor="#F0F4F8",
        linecolor="#E2E8F0",
        tickfont=dict(size=11),
        zeroline=False,
        showspikes=True,
        spikethickness=1,
        spikecolor="#E2E8F0",
    ),
    dragmode="zoom",
    hoverdistance=100,
)


# ── GLOBAL CSS ─────────────────────────────────────────────────────────────
_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  }

  .stApp { background-color: #f0f2f6 !important; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
  }
  [data-testid="stSidebar"] * { color: #1a2744 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label,
  [data-testid="stSidebar"] .stSlider label { color: #718096 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }

  /* Top bar */
  header[data-testid="stHeader"] {
    background: #ffffff !important;
    border-bottom: 1px solid #e2e8f0 !important;
  }

  /* Hide footer / menu */
  #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

  /* Column padding */
  div[data-testid="column"] { padding: 0 8px !important; }

  /* Metric widget */
  [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 700 !important; color: #1a2744 !important; }
  [data-testid="stMetricLabel"] { font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.6px !important; color: #718096 !important; }

  /* Expander */
  [data-testid="stExpander"] {
    border: 1px solid #E2E8F0 !important;
    border-radius: 8px !important;
    background: white !important;
  }
</style>
"""


def apply_styles() -> None:
    """Inject shared CSS. Call once from app.py only."""
    st.markdown(_CSS, unsafe_allow_html=True)


# ── SIDEBAR HEADER ─────────────────────────────────────────────────────────
def sidebar_header(title: str = "Intelligence", subtitle: str = "Dashboard") -> None:
    """Render branded dark-navy sidebar header."""
    st.sidebar.markdown(
        f"<div style='padding:18px 12px 12px 12px;'>"
        f"<div style='font-size:10px;font-weight:700;letter-spacing:2px;"
        f"text-transform:uppercase;color:#718096;margin-bottom:4px;'>CUSTOMER</div>"
        f"<div style='font-size:17px;font-weight:800;color:#1a2744;letter-spacing:0.3px;'>{title}</div>"
        f"<div style='font-size:10px;font-weight:500;letter-spacing:2px;"
        f"text-transform:uppercase;color:#006B7D;margin-top:3px;'>{subtitle}</div></div>"
        f"<div style='height:1px;background:#e2e8f0;margin:8px 12px 12px 12px;'></div>",
        unsafe_allow_html=True,
    )


# ── PAGE HEADER ─────────────────────────────────────────────────────────────
def page_header(
    eyebrow: str,
    title: str,
    subtitle: str = "",
    record_label: str = "",
    record_count: str = "",
) -> None:
    """Render the dark navy gradient page header band."""
    right = ""
    if record_label:
        right = (
            f"<div style='text-align:right;font-size:11px;color:rgba(255,255,255,0.4);'>"
            f"<b style='color:rgba(255,255,255,0.85);font-size:20px;font-weight:700;"
            f"display:block;letter-spacing:-0.5px;'>{record_count}</b>"
            f"{record_label}</div>"
        )
    sub_html = (
        f"<div style='font-size:13px;color:rgba(255,255,255,0.5);margin-top:4px;'>{subtitle}</div>"
        if subtitle
        else ""
    )
    header_style = (
        "background:linear-gradient(135deg,#1a2744 0%,#0f1d3a 100%);"
        "border-radius:12px;padding:26px 32px 22px 32px;"
        "margin-bottom:20px;display:flex;align-items:flex-end;justify-content:space-between;"
        "box-shadow:0 4px 20px rgba(26,39,68,0.25);"
        "border-bottom:3px solid #5eb8c8;"
    )
    eyebrow_style = (
        "font-size:10px;font-weight:700;letter-spacing:2px;"
        "text-transform:uppercase;color:#5eb8c8;margin-bottom:6px;"
    )
    title_style = "font-size:24px;font-weight:800;color:#ffffff;line-height:1.2;letter-spacing:-0.3px;"
    st.markdown(
        f"<div style='{header_style}'>"
        f"<div>"
        f"<div style='{eyebrow_style}'>{eyebrow}</div>"
        f"<div style='{title_style}'>{title}</div>"
        f"{sub_html}</div>{right}</div>",
        unsafe_allow_html=True,
    )


# ── KPI ROW ────────────────────────────────────────────────────────────────
_ACCENT_COLORS = {
    "navy": {
        "border": "#1a2744",
        "bg": "linear-gradient(135deg,#f0f3fa 0%,#e8edf8 100%)",
        "icon_color": "#1a2744",
    },
    "teal": {
        "border": "#006B7D",
        "bg": "linear-gradient(135deg,#f0fafa 0%,#e0f5f7 100%)",
        "icon_color": "#006B7D",
    },
    "red": {
        "border": "#C0392B",
        "bg": "linear-gradient(135deg,#fff5f5 0%,#ffe8e8 100%)",
        "icon_color": "#C0392B",
    },
    "amber": {
        "border": "#E67E22",
        "bg": "linear-gradient(135deg,#fffaf0 0%,#fef0da 100%)",
        "icon_color": "#E67E22",
    },
    "green": {
        "border": "#1A7049",
        "bg": "linear-gradient(135deg,#f0faf5 0%,#dcf5e8 100%)",
        "icon_color": "#1A7049",
    },
    "gold": {
        "border": "#C5933A",
        "bg": "linear-gradient(135deg,#fdfaf0 0%,#faf0d4 100%)",
        "icon_color": "#C5933A",
    },
}


def kpi_row(cards: list[dict]) -> None:
    """
    Render a row of equal-height KPI metric cards in a single HTML grid.

    Each card dict supports:
      label   : str  — uppercase label
      value   : str  — big metric value
      accent  : str  — navy | teal | red | amber | green | gold
      delta   : str  — optional delta text (prefix + triggers colour)
      note    : str  — optional highlighted note below value
      icon    : str  — (ignored, kept for compat)
    """
    n = len(cards)
    cards_html = ""
    for c in cards:
        palette = _ACCENT_COLORS.get(c.get("accent", "navy"), _ACCENT_COLORS["navy"])
        border_color = palette["border"]
        bg = palette["bg"]
        label = str(c.get("label", ""))
        value = str(c.get("value", ""))

        # delta
        delta_html = ""
        raw_delta = c.get("delta")
        if raw_delta:
            d = str(raw_delta)
            if d.startswith("+"):
                dc, arrow = "#1A7049", "▲"
            elif d.startswith("-"):
                dc, arrow = "#C0392B", "▼"
            else:
                dc, arrow = "#718096", "·"
            delta_html = (
                f'<div style="font-size:11px;font-weight:600;color:{dc};margin-top:5px;">'
                f"{arrow} {d}</div>"
            )

        # note — highlighted callout below value
        note_html = ""
        raw_note = c.get("note")
        if raw_note:
            note_html = (
                f'<div style="margin-top:8px;padding:4px 8px;background:rgba(0,0,0,0.05);'
                f"border-radius:4px;font-size:10px;font-weight:600;color:{border_color};"
                f'letter-spacing:0.3px;line-height:1.4;">{raw_note}</div>'
            )

        card_style = (
            f"background:{bg};"
            f"border:1px solid rgba(0,0,0,0.06);border-left:4px solid {border_color};"
            f"border-radius:10px;padding:18px 20px 16px 20px;"
            f"box-shadow:0 2px 8px rgba(0,0,0,0.06);"
            f"display:flex;flex-direction:column;justify-content:space-between;"
            f"height:100%;box-sizing:border-box;"
        )

        cards_html += (
            f"<div style='{card_style}'>"
            f"<div style='font-size:10px;font-weight:700;letter-spacing:1px;"
            f"text-transform:uppercase;color:#8898aa;margin-bottom:8px;'>{label}</div>"
            f"<div style='font-size:28px;font-weight:800;color:#1a2744;line-height:1;letter-spacing:-0.5px;'>{value}</div>"
            f"{delta_html}{note_html}"
            f"</div>"
        )

    grid_style = (
        f"display:grid;grid-template-columns:repeat({n},1fr);"
        f"gap:12px;align-items:stretch;margin-bottom:16px;"
    )
    st.markdown(
        f"<div style='{grid_style}'>{cards_html}</div>",
        unsafe_allow_html=True,
    )


# ── SECTION TITLE ──────────────────────────────────────────────────────────
def section_title(text: str, pill: str = "") -> None:
    pill_html = (
        f'<span style="display:inline-block;background:#EBF8FF;color:#006B7D;'
        f"font-size:10px;font-weight:600;padding:2px 8px;border-radius:20px;"
        f'margin-left:8px;letter-spacing:0.4px;text-transform:none;vertical-align:middle;">{pill}</span>'
        if pill
        else ""
    )
    st.markdown(
        f'<div style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;'
        f"color:#1a2744;padding-bottom:8px;border-bottom:2px solid #E2E8F0;"
        f'margin-bottom:14px;margin-top:6px;">{text}{pill_html}</div>',
        unsafe_allow_html=True,
    )


# ── INSIGHT / WARN CALLOUTS ────────────────────────────────────────────────
def insight(text: str) -> None:
    st.markdown(
        f'<div style="background:#EBF8FF;border-left:4px solid #006B7D;border-radius:0 6px 6px 0;'
        f'padding:10px 14px;font-size:12px;color:#1a2744;margin-bottom:14px;">{text}</div>',
        unsafe_allow_html=True,
    )


def warn(text: str) -> None:
    st.markdown(
        f'<div style="background:#FFF5F5;border-left:4px solid #C0392B;border-radius:0 6px 6px 0;'
        f'padding:10px 14px;font-size:12px;color:#742a2a;margin-bottom:14px;">{text}</div>',
        unsafe_allow_html=True,
    )


# ── CHART WRAP ─────────────────────────────────────────────────────────────
def chart_wrap(title: str, subtitle: str = "") -> None:
    sub = (
        f'<div style="font-size:11px;color:#A0AEC0;margin-bottom:10px;">{subtitle}</div>'
        if subtitle
        else ""
    )
    st.markdown(
        f'<div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.6px;'
        f'color:#4A5568;margin-bottom:2px;">{title}</div>{sub}',
        unsafe_allow_html=True,
    )
