"""Customers management page for Streamlit application."""

import streamlit as st
import pandas as pd
from typing import Optional

from utils.session_state import get_customers, set_customers
from services.api_client import APIClient


def render_customers():
    """Render the customers management page."""
    st.title("👥 Customers")
    st.markdown("Manage your customer database")

    # Initialize API client
    api_client = APIClient()

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        search_query = st.text_input("🔍 Search", placeholder="Name or phone...")
        filter_status = st.selectbox(
            "Status", ["All", "Active", "Inactive", "VIP"]
        )

    # Main content area
    col1, col2 = st.columns([3, 1])

    with col1:
        # Fetch customers (in production, use API call)
        customers = get_customers() or []

        if not customers:
            # Sample data for demo
            customers = [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "+1234567890",
                    "status": "Active",
                    "last_visit": "2026-06-25",
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane@example.com",
                    "phone": "+1234567891",
                    "status": "VIP",
                    "last_visit": "2026-06-26",
                },
                {
                    "id": 3,
                    "name": "Bob Wilson",
                    "email": "bob@example.com",
                    "phone": "+1234567892",
                    "status": "Active",
                    "last_visit": "2026-06-20",
                },
            ]
            set_customers(customers)

        # Apply filters
        filtered_customers = customers

        if search_query:
            filtered_customers = [
                c
                for c in filtered_customers
                if search_query.lower() in c.get("name", "").lower()
                or search_query in c.get("phone", "")
            ]

        if filter_status != "All":
            filtered_customers = [
                c for c in filtered_customers if c.get("status") == filter_status
            ]

        # Display as dataframe
        if filtered_customers:
            df = pd.DataFrame(filtered_customers)
            display_cols = ["name", "email", "phone", "status", "last_visit"]
            df_display = df[display_cols].copy()
            df_display.columns = ["Name", "Email", "Phone", "Status", "Last Visit"]

            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Status": st.column_config.TextColumn(
                        "Status",
                        help="Customer status",
                    ),
                },
            )
        else:
            st.info("No customers found matching your filters.")

    with col2:
        st.header("Actions")

        if st.button("➕ Add Customer", use_container_width=True):
            st.session_state.show_add_customer = True

        if st.button("📥 Export CSV", use_container_width=True):
            if customers:
                df = pd.DataFrame(customers)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="customers.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

    # Add customer modal (simplified as expandable section)
    if st.session_state.get("show_add_customer", False):
        st.markdown("---")
        st.subheader("➕ Add New Customer")

        with st.form("add_customer_form"):
            col_name, col_email = st.columns(2)
            with col_name:
                name = st.text_input("Name *", placeholder="Full name")
            with col_email:
                email = st.text_input("Email *", placeholder="email@example.com")

            col_phone, col_status = st.columns(2)
            with col_phone:
                phone = st.text_input("Phone", placeholder="+1234567890")
            with col_status:
                status = st.selectbox("Status", ["Active", "Inactive", "VIP"])

            submitted = st.form_submit_button("Save Customer")

            if submitted:
                if name and email:
                    new_customer = {
                        "id": len(customers) + 1,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "status": status,
                        "last_visit": st.session_state.get(
                            "today", "2026-06-27"
                        ),
                    }
                    customers.append(new_customer)
                    set_customers(customers)
                    st.success(f"Customer {name} added successfully!")
                    st.session_state.show_add_customer = False
                    st.rerun()
                else:
                    st.error("Name and email are required fields.")

        if st.button("Cancel"):
            st.session_state.show_add_customer = False
            st.rerun()