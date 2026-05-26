import streamlit as st

st.set_page_config(page_title="Customer Intelligence Dashboard",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', 'Segoe UI', Roboto, sans-serif !important; }

    span[data-testid="stIconMaterial"],
    .material-icons, .material-symbols-outlined {
        font-size: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
    }

    button[data-testid="baseButton-header"] {
        position: relative !important;
    }
    button[data-testid="baseButton-header"]::after {
        content: ">>" !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        color: rgba(255,255,255,0.85) !important;
        font-weight: 700 !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
    }

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
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1); margin: 16px 0; }

    section[data-testid="stSidebar"] a {
        color: rgba(255,255,255,0.88) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-decoration: none !important;
    }
    section[data-testid="stSidebar"] a:hover {
        color: #4facfe !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"],
    section[data-testid="stSidebar"] [aria-current="page"] {
        color: #4facfe !important;
        font-weight: 700 !important;
    }

    footer { display: none; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style="padding: 16px 0 12px 0; text-align: center;">
        <div style="font-size: 20px; font-weight: 800; color: white; letter-spacing: 0.5px;">Intelligence</div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase;">Dashboard</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style="height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
                margin: 4px 0 8px 0;"></div>
""", unsafe_allow_html=True)

overview = st.Page("overview.py", title="Overview", default=True)
sales = st.Page("pages/1_Sales_Analysis.py", title="Sales Analysis")
customers = st.Page("pages/2_Customer_Insights.py", title="Customer Insights")
products = st.Page("pages/3_Product_Performance.py", title="Product Performance")

pg = st.navigation([overview, sales, customers, products])
pg.run()
