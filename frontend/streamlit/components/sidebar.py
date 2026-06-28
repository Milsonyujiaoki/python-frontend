"""Sidebar navigation component for Streamlit application."""

import streamlit as st


def render_sidebar():
    """Render the sidebar with navigation and quick actions."""

    with st.sidebar:
        # App branding
        st.title("✂️ BarberShop")
        st.markdown("---")

        # Navigation menu
        st.header("Navigation")

        # Main pages
        page = st.radio(
            "Go to",
            [
                "🏠 Dashboard",
                "👥 Customers",
                "💈 Barbers",
                "💇 Services",
                "📅 Appointments",
                "📊 Reports",
            ],
            label_visibility="collapsed",
            index=0,
        )

        # Handle navigation
        if page == "🏠 Dashboard":
            st.switch_page("main.py")
        elif page == "👥 Customers":
            st.switch_page("pages/customers.py")
        elif page == "💈 Barbers":
            st.switch_page("pages/barbers.py")
        elif page == "💇 Services":
            st.switch_page("pages/services.py")
        elif page == "📅 Appointments":
            st.info("Appointments page coming soon!")
        elif page == "📊 Reports":
            st.info("Reports page coming soon!")

        st.markdown("---")

        # Quick actions
        st.header("Quick Actions")

        if st.button("➕ New Customer", use_container_width=True):
            st.switch_page("pages/customers.py")
        if st.button("➕ New Barber", use_container_width=True):
            st.switch_page("pages/barbers.py")
        if st.button("➕ New Service", use_container_width=True):
            st.switch_page("pages/services.py")

        st.markdown("---")

        # User info
        st.header("Account")
        if st.session_state.get("authenticated", False):
            st.success(f"Logged in as {st.session_state.user_email}")
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_email = None
                st.rerun()
        else:
            st.info("Not logged in")
            if st.button("Login", use_container_width=True):
                st.switch_page("pages/login.py")