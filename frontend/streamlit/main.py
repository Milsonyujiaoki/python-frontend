"""
Streamlit Frontend Application for Barbershop SaaS.

Main application entry point with dashboard and navigation.
"""

import streamlit as st
from utils.session_state import initialize_session_state
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard

# Page configuration
st.set_page_config(
    page_title="BarberShop SaaS",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
initialize_session_state()

# Render sidebar navigation
render_sidebar()

# Main content area
st.title("📊 Dashboard")
st.markdown("Welcome to the BarberShop SaaS management system.")

# Render dashboard with metrics and charts
render_dashboard()