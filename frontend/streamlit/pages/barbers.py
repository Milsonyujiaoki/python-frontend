"""Barbers management page for Streamlit application."""

import streamlit as st
import pandas as pd
from typing import Optional

from utils.session_state import get_barbers, set_barbers
from services.api_client import APIClient


def render_barbers():
    """Render the barbers management page."""
    st.title("💈 Barbers")
    st.markdown("Manage your barber team")

    # Initialize API client
    api_client = APIClient()

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        search_query = st.text_input("🔍 Search", placeholder="Name or specialty...")
        filter_status = st.selectbox(
            "Status", ["All", "Active", "Inactive", "On Leave"]
        )

    # Main content area
    col1, col2 = st.columns([3, 1])

    with col1:
        # Fetch barbers (in production, use API call)
        barbers = get_barbers() or []

        if not barbers:
            # Sample data for demo
            barbers = [
                {
                    "id": 1,
                    "name": "Mike Johnson",
                    "email": "mike@barbershop.com",
                    "phone": "+1234567890",
                    "specialty": "Classic Cuts, Beard Trim",
                    "status": "Active",
                    "rating": 4.9,
                },
                {
                    "id": 2,
                    "name": "Sarah Williams",
                    "email": "sarah@barbershop.com",
                    "phone": "+1234567891",
                    "specialty": "Coloring, Styling",
                    "status": "Active",
                    "rating": 4.8,
                },
                {
                    "id": 3,
                    "name": "Tom Brown",
                    "email": "tom@barbershop.com",
                    "phone": "+1234567892",
                    "specialty": "Fade, Design",
                    "status": "On Leave",
                    "rating": 4.7,
                },
            ]
            set_barbers(barbers)

        # Apply filters
        filtered_barbers = barbers

        if search_query:
            filtered_barbers = [
                b
                for b in filtered_barbers
                if search_query.lower() in b.get("name", "").lower()
                or search_query.lower() in b.get("specialty", "").lower()
            ]

        if filter_status != "All":
            filtered_barbers = [
                b for b in filtered_barbers if b.get("status") == filter_status
            ]

        # Display as dataframe with custom styling
        if filtered_barbers:
            df = pd.DataFrame(filtered_barbers)

            # Display cards instead of table for better visual
            for i, barber in enumerate(filtered_barbers):
                with st.container():
                    col_avatar, col_info, col_actions = st.columns([1, 3, 1])

                    with col_avatar:
                        # Avatar placeholder
                        st.markdown(
                            f"""
                            <div style="
                                width: 60px;
                                height: 60px;
                                border-radius: 50%;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-size: 24px;
                                font-weight: bold;
                            ">
                                {barber.get('name', '?')[0]}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col_info:
                        st.markdown(f"### {barber.get('name')}")
                        st.write(f"📧 {barber.get('email')}")
                        st.write(f"📱 {barber.get('phone')}")
                        st.write(f"💈 {barber.get('specialty')}")

                    with col_actions:
                        status_emoji = (
                            "✅" if barber.get("status") == "Active" else "⏸️"
                        )
                        st.metric("Rating", f"{barber.get('rating', 0)}⭐")
                        st.caption(f"{status_emoji} {barber.get('status')}")

                    if i < len(filtered_barbers) - 1:
                        st.divider()

        else:
            st.info("No barbers found matching your filters.")

    with col2:
        st.header("Actions")

        if st.button("➕ Add Barber", use_container_width=True):
            st.session_state.show_add_barber = True

        if st.button("📊 View Schedule", use_container_width=True):
            st.info("Schedule view coming soon!")

    # Add barber modal
    if st.session_state.get("show_add_barber", False):
        st.markdown("---")
        st.subheader("➕ Add New Barber")

        with st.form("add_barber_form"):
            col_name, col_email = st.columns(2)
            with col_name:
                name = st.text_input("Name *", placeholder="Full name")
            with col_email:
                email = st.text_input("Email *", placeholder="email@barbershop.com")

            col_phone, col_specialty = st.columns(2)
            with col_phone:
                phone = st.text_input("Phone", placeholder="+1234567890")
            with col_specialty:
                specialty = st.text_area(
                    "Specialty", placeholder="e.g., Classic Cuts, Beard Trim, Coloring"
                )

            col_status, col_rating = st.columns(2)
            with col_status:
                status = st.selectbox("Status", ["Active", "Inactive", "On Leave"])
            with col_rating:
                rating = st.slider("Rating", 0.0, 5.0, 4.5, 0.1)

            submitted = st.form_submit_button("Save Barber")

            if submitted:
                if name and email:
                    new_barber = {
                        "id": len(barbers) + 1,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "specialty": specialty,
                        "status": status,
                        "rating": rating,
                    }
                    barbers.append(new_barber)
                    set_barbers(barbers)
                    st.success(f"Barber {name} added successfully!")
                    st.session_state.show_add_barber = False
                    st.rerun()
                else:
                    st.error("Name and email are required fields.")

        if st.button("Cancel"):
            st.session_state.show_add_barber = False
            st.rerun()