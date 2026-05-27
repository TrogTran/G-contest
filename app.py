import sys
import os

import streamlit as st

# Ensure repo root is on sys.path so all pages can import 'utils'
sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import apply_styles, sidebar_header

st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()
sidebar_header("Customer Intelligence", "Dashboard")

overview = st.Page("pages/0_Overview.py", title="Overview", default=True)
segments = st.Page("pages/1_Customer_Segments.py", title="Customer Segments")
nbfo = st.Page("pages/2_NBFO_Credit.py", title="NBFO & Credit Targeting")
security = st.Page("pages/3_Security_Alerts.py", title="Security Alerts")

pg = st.navigation([overview, segments, nbfo, security])
pg.run()
