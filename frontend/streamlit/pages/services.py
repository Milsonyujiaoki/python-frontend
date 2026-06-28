"""Services management page for Streamlit application."""

import streamlit as st
import pandas as pd
from typing import Optional

from utils.session_state import get_services, set_services
from services.api_client import APIClient


def render_services():
    """Render the services management page."""
    st.title("💇 Services")
    st.markdown("Manage your service offerings")

    # Initialize API client
    api_client = APIClient()

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        search_query = st.text_input("🔍 Search", placeholder="Service name...")
        filter_category = st.selectbox(
            "Category", ["All", "Hair", "Beard", "Coloring", "Treatment", "Other"]
        )
        min_price = st.slider("Min Price ($)", 0, 100, 0, 5)
        max_price = st.slider("Max Price ($)", 0, 200, 200, 10)

    # Main content area
    col1, col2 = st.columns([3, 1])

    with col1:
        # Fetch services (in production, use API call)
        services = get_services() or []

        if not services:
            # Sample data for demo
            services = [
                {
                    "id": 1,
                    "name": "Classic Haircut",
                    "description": "Traditional haircut with scissor over comb",
                    "price": 35.00,
                    "duration": 30,
                    "category": "Hair",
                    "active": True,
                },
                {
                    "id": 2,
                    "name": "Beard Trim & Shape",
                    "description": "Professional beard trimming and shaping",
                    "price": 20.00,
                    "duration": 20,
                    "category": "Beard",
                    "active": True,
                },
                {
                    "id": 3,
                    "name": "Full Color",
                    "description": "Complete hair coloring service",
                    "price": 80.00,
                    "duration": 90,
                    "category": "Coloring",
                    "active": True,
                },
                {
                    "id": 4,
                    "name": "Hair Treatment",
                    "description": "Deep conditioning and scalp treatment",
                    "price": 50.00,
                    "duration": 45,
                    "category": "Treatment",
                    "active": True,
                },
                {
                    "id": 5,
                    "name": "Fade Cut",
                    "description": "Modern fade with design options",
                    "price": 40.00,
                    "duration": 40,
                    "category": "Hair",
                    "active": True,
                },
            ]
            set_services(services)

        # Apply filters
        filtered_services = services

        if search_query:
            filtered_services = [
                s
                for s in filtered_services
                if search_query.lower() in s.get("name", "").lower()
                or search_query.lower() in s.get("description", "").lower()
            ]

        if filter_category != "All":
            filtered_services = [
                s for s in filtered_services if s.get("category") == filter_category
            ]

        filtered_services = [
            s
            for s in filtered_services
            if min_price <= s.get("price", 0) <= max_price
        ]

        # Display as interactive table
        if filtered_services:
            df = pd.DataFrame(filtered_services)
            display_cols = ["name", "category", "price", "duration", "active"]
            df_display = df[display_cols].copy()
            df_display.columns = ["Service", "Category", "Price", "Duration (min)", "Active"]

            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Price": st.column_config.NumberColumn(
                        "Price", format="$%.2f"
                    ),
                    "Active": st.column_config.CheckboxColumn(
                        "Active",
                        help="Service availability",
                    ),
                },
            )

            # Summary stats
            st.markdown("---")
            stat_col1, stat_col2, stat_col3 = st.columns(3)

            with stat_col1:
                st.metric(
                    "Total Services",
                    len(filtered_services),
                    help="Number of services matching filters",
                )

            with stat_col2:
                avg_price = sum(s.get("price", 0) for s in filtered_services) / len(
                    filtered_services
                )
                st.metric("Average Price", f"${avg_price:.2f}")

            with stat_col3:
                avg_duration = sum(
                    s.get("duration", 0) for s in filtered_services
                ) / len(filtered_services)
                st.metric("Avg Duration", f"{avg_duration:.0f} min")
        else:
            st.info("No services found matching your filters.")

    with col2:
        st.header("Actions")

        if st.button("➕ Add Service", use_container_width=True):
            st.session_state.show_add_service = True

        if st.button("📊 Analytics", use_container_width=True):
            st.info("Service analytics coming soon!")

    # Add service modal
    if st.session_state.get("show_add_service", False):
        st.markdown("---")
        st.subheader("➕ Add New Service")

        with st.form("add_service_form"):
            col_name, col_category = st.columns(2)
            with col_name:
                name = st.text_input("Service Name *", placeholder="e.g., Classic Cut")
            with col_category:
                category = st.selectbox(
                    "Category",
                    ["Hair", "Beard", "Coloring", "Treatment", "Other"],
                )

            description = st.text_area(
                "Description",
                placeholder="Describe the service...",
                height=60,
            )

            col_price, col_duration = st.columns(2)
            with col_price:
                price = st.number_input(
                    "Price ($)", min_value=0.0, max_value=500.0, value=30.0, step=5.0
                )
            with col_duration:
                duration = st.number_input(
                    "Duration (min)",
                    min_value=5,
                    max_value=180,
                    value=30,
                    step=5,
                )

            active = st.checkbox("Active", value=True)

            submitted = st.form_submit_button("Save Service")

            if submitted:
                if name:
                    new_service = {
                        "id": len(services) + 1,
                        "name": name,
                        "description": description,
                        "price": price,
                        "duration": duration,
                        "category": category,
                        "active": active,
                    }
                    services.append(new_service)
                    set_services(services)
                    st.success(f"Service '{name}' added successfully!")
                    st.session_state.show_add_service = False
                    st.rerun()
                else:
                    st.error("Service name is required.")

        if st.button("Cancel"):
            st.session_state.show_add_service = False
            st.rerun()