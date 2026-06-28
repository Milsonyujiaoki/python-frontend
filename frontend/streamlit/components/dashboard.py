"""Dashboard component for Streamlit application."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_dashboard():
    """Render the main dashboard with metrics and charts."""
    st.title("🏠 Dashboard")
    st.markdown("Welcome to BarberShop SaaS Management System")

    # Sample metrics (would come from API in production)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Customers",
            value="1,234",
            delta="12% vs last month",
            delta_color="normal",
        )

    with col2:
        st.metric(
            label="Active Barbers",
            value="8",
            delta="2 new this month",
            delta_color="normal",
        )

    with col3:
        st.metric(
            label="Services Offered",
            value="15",
            delta="3 new services",
            delta_color="normal",
        )

    with col4:
        st.metric(
            label="Appointments Today",
            value="24",
            delta="-5 vs yesterday",
            delta_color="inverse",
        )

    st.markdown("---")

    # Charts row
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📈 Revenue Overview")
        # Sample revenue data
        revenue_data = pd.DataFrame(
            {
                "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                "Revenue": [12000, 15000, 18000, 22000, 25000, 28000],
            }
        )
        fig = px.line(
            revenue_data, x="Month", y="Revenue", markers=True, title="Monthly Revenue"
        )
        fig.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("💇 Service Distribution")
        # Sample service data
        service_data = pd.DataFrame(
            {
                "Service": [
                    "Haircut",
                    "Beard Trim",
                    " coloring",
                    "Styling",
                    "Treatment",
                ],
                "Count": [45, 25, 15, 10, 5],
            }
        )
        fig = px.pie(
            service_data,
            values="Count",
            names="Service",
            title="Services Breakdown",
            hole=0.4,
        )
        fig.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Recent activity table
    st.subheader("📋 Recent Appointments")
    appointments_data = pd.DataFrame(
        {
            "Customer": ["John Doe", "Jane Smith", "Bob Wilson", "Alice Brown"],
            "Barber": ["Mike", "Sarah", "Mike", "Sarah"],
            "Service": ["Haircut", "Coloring", "Beard Trim", "Styling"],
            "Time": ["10:00", "11:30", "13:00", "14:30"],
            "Status": ["Completed", "In Progress", "Pending", "Confirmed"],
        }
    )
    st.dataframe(appointments_data, use_container_width=True, hide_index=True)

    # Quick stats
    st.markdown("---")
    st.subheader("📊 Quick Stats")

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    with stat_col1:
        st.markdown("**⭐ Top Rated Barber:** Mike (4.9★)")

    with stat_col2:
        st.markdown("**📈 Busiest Day:** Saturday (45 appointments)")

    with stat_col3:
        st.markdown("**⏰ Peak Hours:** 10:00 AM - 2:00 PM")