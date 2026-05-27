"""
Shared McKinsey/BCG-style stylesheet for the Customer Intelligence Dashboard.
Call apply_styles() from app.py once; individual pages do NOT call it again.
"""

import streamlit as st

# ── PALETTE ────────────────────────────────────────────────────────────────
# Navy #1a2744  |  Teal  #006B7D  |  Gold   #C5933A
# Slate #4A5568 |  Light #F7F9FC  |  Border #E2E8F0
# Red   #C0392B |  Amber #E67E22  |  Green  #1A7049

_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
  @import url('https://fonts.googleapis.com/icon?family=Material+Icons+Outlined');
  @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

  /* ── RESET / BASE ────────────────────────────────────────────────── */
  *, *::before, *::after {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    box-sizing: border-box;
  }
  /* Restore Material Icons font for icon elements (prevent ligature text leak) */
  span[data-testid="stIconMaterial"],
  .material-icons,
  .material-symbols-outlined {
    font-family: 'Material Icons Outlined', 'Material Icons', 'Material Symbols Outlined' !important;
    font-size: inherit !important;
    line-height: inherit !important;
  }
  .stApp { background: #F7F9FC !important; }

  /* Strip default Streamlit chrome */
  footer, #MainMenu, header[data-testid="stHeader"] { display: none !important; }
  .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

  /* ── SIDEBAR ─────────────────────────────────────────────────────── */
  section[data-testid="stSidebar"] {
    background: #1a2744 !important;
    border-right: 1px solid #0f1d38 !important;
  }
  section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.88) !important; }
  section[data-testid="stSidebar"] label { font-size: 11px !important; font-weight: 600 !important; letter-spacing: 0.6px !important; text-transform: uppercase !important; color: rgba(255,255,255,0.55) !important; }
  section[data-testid="stSidebar"] [data-baseweb="select"] > div,
  section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 6px !important;
    font-size: 13px !important;
  }
  section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
  section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
    border-color: rgba(255,255,255,0.28) !important;
  }
  /* Multiselect chips */
  section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: rgba(0,107,125,0.5) !important;
    border-radius: 4px !important;
  }
  section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 14px 0 !important;
  }

  /* Expander - replace hidden icon with +/- indicator */
  .stExpander details summary {
    position: relative !important;
    padding-right: 28px !important;
  }
  .stExpander details summary::after {
    content: "+" !important;
    position: absolute !important;
    right: 10px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #006B7D !important;
    font-family: 'Inter', sans-serif !important;
  }
  .stExpander details[open] summary::after {
    content: "−" !important;
  }

  /* Plotly mode bar */
  .modebar {
    opacity: 0.3 !important;
    transition: opacity 0.2s !important;
  }
  .modebar:hover { opacity: 1 !important; }
  .modebar-btn { color: #4A5568 !important; }
  .modebar-btn:hover { color: #1a2744 !important; }

  /* Nav links */
  section[data-testid="stSidebar"] nav a,
  a[data-testid="stPageLink"],
  [data-testid*="PageLink"] {
    color: rgba(255,255,255,0.75) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    border-radius: 6px !important;
    padding: 6px 10px !important;
    display: block !important;
    transition: background 0.15s, color 0.15s !important;
  }
  section[data-testid="stSidebar"] nav a:hover,
  a[data-testid="stPageLink"]:hover { background: rgba(255,255,255,0.07) !important; color: white !important; }
  [aria-current="page"] { color: #5eb8c8 !important; font-weight: 700 !important; background: rgba(0,107,125,0.18) !important; }

  /* Sidebar collapse button */
  button[data-testid="baseButton-header"] span[data-testid="stIconMaterial"] {
    font-size: 0 !important; width: 0; height: 0; overflow: hidden; position: absolute;
  }
  button[data-testid="baseButton-header"]::after {
    content: "<<" !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; color: rgba(255,255,255,0.6) !important;
    font-weight: 700 !important; position: absolute !important;
    top: 50% !important; left: 50% !important;
    transform: translate(-50%, -50%) !important;
    letter-spacing: -2px !important;
  }

  /* ── PAGE HEADER BAND ─────────────────────────────────────────────── */
  .page-header {
    background: #1a2744;
    border-radius: 10px;
    padding: 22px 28px 18px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }
  .page-header-left {}
  .page-header-eyebrow {
    font-size: 10px; font-weight: 600; letter-spacing: 1.6px;
    text-transform: uppercase; color: #5eb8c8; margin-bottom: 4px;
  }
  .page-header-title {
    font-size: 22px; font-weight: 700; color: #ffffff; line-height: 1.25;
  }
  .page-header-sub {
    font-size: 13px; color: rgba(255,255,255,0.55); margin-top: 3px;
  }
  .page-header-right {
    text-align: right;
    font-size: 11px; color: rgba(255,255,255,0.4);
  }
  .page-header-right b { color: rgba(255,255,255,0.75); }

  /* ── KPI CARDS ────────────────────────────────────────────────────── */
  .kpi-row {
    display: flex; gap: 14px; margin-bottom: 26px; flex-wrap: wrap;
  }
  .kpi-card {
    flex: 1; min-width: 130px;
    background: white;
    border: 1px solid #E2E8F0;
    border-top: 3px solid #1a2744;
    border-radius: 8px;
    padding: 16px 18px 14px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .kpi-card:hover { box-shadow: 0 4px 14px rgba(0,0,0,0.09); transform: translateY(-2px); }
  .kpi-card.accent-teal  { border-top-color: #006B7D; }
  .kpi-card.accent-red   { border-top-color: #C0392B; }
  .kpi-card.accent-amber { border-top-color: #E67E22; }
  .kpi-card.accent-green { border-top-color: #1A7049; }
  .kpi-card.accent-navy  { border-top-color: #1a2744; }
  .kpi-card.accent-gold  { border-top-color: #C5933A; }
  .kpi-label {
    font-size: 10px; font-weight: 600; letter-spacing: 0.8px;
    text-transform: uppercase; color: #718096; margin-bottom: 6px;
  }
  .kpi-value {
    font-size: 28px; font-weight: 700; color: #1a2744; line-height: 1.1;
  }
  .kpi-delta {
    font-size: 11px; font-weight: 500; color: #718096; margin-top: 4px;
  }
  .kpi-delta.up   { color: #1A7049; }
  .kpi-delta.down { color: #C0392B; }

  /* ── SECTION HEADINGS ─────────────────────────────────────────────── */
  .section-title {
    font-size: 13px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.8px;
    color: #1a2744;
    padding-bottom: 8px;
    border-bottom: 2px solid #E2E8F0;
    margin-bottom: 14px; margin-top: 6px;
  }
  .section-title span.pill {
    display: inline-block;
    background: #EBF8FF; color: #006B7D;
    font-size: 10px; font-weight: 600;
    padding: 2px 8px; border-radius: 20px;
    margin-left: 8px; letter-spacing: 0.4px;
    text-transform: none;
    vertical-align: middle;
  }
  .insight-box {
    background: #EBF8FF;
    border-left: 4px solid #006B7D;
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    font-size: 12px; color: #1a2744;
    margin-bottom: 14px;
  }
  .insight-box b { color: #006B7D; }
  .warn-box {
    background: #FFF5F5;
    border-left: 4px solid #C0392B;
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    font-size: 12px; color: #742a2a;
    margin-bottom: 14px;
  }

  /* ── CHART CONTAINERS ─────────────────────────────────────────────── */
  .chart-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 18px 16px 10px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    margin-bottom: 2px;
  }
  .chart-title {
    font-size: 12px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.6px;
    color: #4A5568; margin-bottom: 2px;
  }
  .chart-sub {
    font-size: 11px; color: #A0AEC0; margin-bottom: 10px;
  }

  /* ── DATA TABLE ───────────────────────────────────────────────────── */
  .stDataFrame { border-radius: 8px !important; border: 1px solid #E2E8F0 !important; box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important; }
  .stDataFrame thead tr th { background: #F7F9FC !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; color: #4A5568 !important; }
  .stDataFrame tbody tr:hover { background: #EBF8FF !important; }

  /* ── EXPANDER ─────────────────────────────────────────────────────── */
  .stExpander { border: 1px solid #E2E8F0 !important; border-radius: 8px !important; background: white !important; }
  .stExpander:hover { border-color: #006B7D !important; }
  summary { font-size: 12px !important; font-weight: 600 !important; color: #4A5568 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }

  /* ── DIVIDER ──────────────────────────────────────────────────────── */
  hr[data-testid="stDivider"] {
    border-color: #E2E8F0 !important;
    margin: 18px 0 !important;
  }

  /* ── NAV TAB BAR ──────────────────────────────────────────────────── */
  .nav-tab-bar {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 8px 12px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    display: flex;
    gap: 6px;
    align-items: center;
  }
  .nav-tab-bar div[data-testid="column"] {
    padding: 0 !important;
    flex: 1;
  }
  .nav-tab-bar a[data-testid="stPageLink"] {
    display: block;
    text-align: center;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4A5568 !important;
    text-decoration: none !important;
    transition: all 0.15s ease !important;
    white-space: nowrap;
  }
  .nav-tab-bar a[data-testid="stPageLink"]:hover {
    background: #EBF8FF !important;
    color: #006B7D !important;
  }
  .nav-tab-bar a[aria-current="page"] {
    background: #1a2744 !important;
    color: white !important;
    font-weight: 700 !important;
  }

  /* Column cards (remove auto-padding from Streamlit columns) */
  div[data-testid="column"] {
    padding: 0 8px !important;
  }

  /* Streamlit metric widget – override with custom if needed */
  [data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 700 !important; color: #1a2744 !important; }
  [data-testid="stMetricLabel"] { font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.6px !important; color: #718096 !important; }
</style>
"""

# ── PLOTLY SHARED THEME ────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Inter, Segoe UI, system-ui", size=12, color="#4A5568"),
    title_font=dict(size=13, color="#1a2744", family="Inter", weight=600),
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
    spikedistance=1000,
)

# Palette
C_NAVY = "#1a2744"
C_TEAL = "#006B7D"
C_GOLD = "#C5933A"
C_SLATE = "#4A5568"
C_RED = "#C0392B"
C_AMBER = "#E67E22"
C_GREEN = "#1A7049"
C_BLUE = "#2980B9"
C_LIGHT = "#5eb8c8"

PRIORITY_COLORS = {"Normal": "#A0AEC0", "Alert": C_AMBER, "Critical": C_RED}
PERSONA_COLORS = {
    "Digital Native": C_TEAL,
    "Credit Seeker": C_AMBER,
    "Wealth Accumulator": C_NAVY,
    "Dormant/Churn-risk": "#718096",
}

SEQ_TEAL = ["#EBF8FF", "#BEE3F8", "#5eb8c8", C_TEAL, "#004050"]
SEQ_NAVY = ["#EDF2F7", "#CBD5E0", "#718096", "#2D3748", C_NAVY]


def apply_styles() -> None:
    """Inject shared dashboard CSS. Call once from app.py."""
    st.markdown(_CSS, unsafe_allow_html=True)


def sidebar_header(title: str = "Intelligence", subtitle: str = "Dashboard") -> None:
    """Render branded sidebar header."""
    st.sidebar.markdown(
        f"<div style='padding:18px 4px 12px 4px;text-align:center;'>"
        f"<div style='font-size:10px;font-weight:700;letter-spacing:2px;"
        f"text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:6px;'>CUSTOMER</div>"
        f"<div style='font-size:17px;font-weight:800;color:white;letter-spacing:0.3px;'>{title}</div>"
        f"<div style='font-size:10px;font-weight:500;letter-spacing:2px;"
        f"text-transform:uppercase;color:#5eb8c8;margin-top:3px;'>{subtitle}</div></div>"
        f"<div style='height:1px;background:rgba(255,255,255,0.08);margin:0 4px 12px 4px;'></div>",
        unsafe_allow_html=True,
    )


def page_header(
    eyebrow: str,
    title: str,
    subtitle: str = "",
    record_label: str = "",
    record_count: str = "",
) -> None:
    """Render the dark navy page header band."""
    right = ""
    if record_label:
        right = (
            f"<div style='text-align:right;font-size:11px;color:rgba(255,255,255,0.4);'>"
            f"<b style='color:rgba(255,255,255,0.75);font-size:18px;display:block;'>{record_count}</b>"
            f"{record_label}</div>"
        )
    sub_html = (
        f"<div style='font-size:13px;color:rgba(255,255,255,0.5);margin-top:3px;'>{subtitle}</div>"
        if subtitle
        else ""
    )
    header_style = (
        "background:#1a2744;border-radius:10px;padding:22px 28px 18px 28px;"
        "margin-bottom:24px;display:flex;align-items:flex-end;justify-content:space-between;"
    )
    eyebrow_style = (
        "font-size:10px;font-weight:600;letter-spacing:1.6px;"
        "text-transform:uppercase;color:#5eb8c8;margin-bottom:4px;"
    )
    title_style = "font-size:22px;font-weight:700;color:#ffffff;line-height:1.25;"
    st.markdown(
        f"<div style='{header_style}'>"
        f"<div>"
        f"<div style='{eyebrow_style}'>{eyebrow}</div>"
        f"<div style='{title_style}'>{title}</div>"
        f"{sub_html}</div>{right}</div>",
        unsafe_allow_html=True,
    )


_ACCENT_COLORS = {
    "navy": "#1a2744",
    "teal": "#006B7D",
    "red": "#C0392B",
    "amber": "#E67E22",
    "green": "#1A7049",
    "gold": "#C5933A",
}


def kpi_row(cards: list[dict]) -> None:
    """
    Render a row of KPI cards using st.columns.
    Each card dict: label, value, delta="", accent="navy"
    accent options: navy, teal, red, amber, green, gold
    """
    cols = st.columns(len(cards))
    for col, c in zip(cols, cards):
        accent_color = _ACCENT_COLORS.get(c.get("accent", "navy"), "#1a2744")
        label = str(c.get("label", ""))
        value = str(c.get("value", ""))

        delta_html = ""
        raw_delta = c.get("delta")
        if raw_delta:
            d = str(raw_delta)
            dc = "#1A7049" if d.startswith("+") else ("#C0392B" if d.startswith("-") else "#718096")
            delta_html = f'<div style="font-size:11px;font-weight:500;color:{dc};margin-top:4px;">{d}</div>'

        card_style = (
            f"background:white;border:1px solid #E2E8F0;border-top:3px solid {accent_color};"
            f"border-radius:8px;padding:16px 18px 14px 18px;"
            f"box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:16px;"
        )

        with col:
            st.markdown(
                f"<div style='{card_style}'>"
                f"<div style='font-size:10px;font-weight:600;letter-spacing:0.8px;"
                f"text-transform:uppercase;color:#718096;margin-bottom:6px;'>{label}</div>"
                f"<div style='font-size:28px;font-weight:700;color:#1a2744;line-height:1.1;'>{value}</div>"
                f"{delta_html}</div>",
                unsafe_allow_html=True,
            )


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
