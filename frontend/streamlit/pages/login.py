"""Login page for Streamlit application."""

import streamlit as st
from utils.session_state import set_authenticated, set_user


def render_login():
    """Render the login page."""
    st.title("🔐 Login")
    st.markdown("Sign in to your BarberShop account")

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.markdown("### Welcome Back!")

            email = st.text_input(
                "Email",
                placeholder="admin@barbershop.com",
                help="Enter your registered email",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                help="Enter your password",
            )

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button("Login", use_container_width=True)
            with col_btn2:
                st.form_submit_button("Demo", use_container_width=True, type="secondary")

            if submitted:
                if email and password:
                    # In production, validate with backend API
                    if password:  # Simplified for demo
                        set_authenticated(True)
                        set_user(email)
                        st.success(f"Welcome back, {email}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.warning("Please fill in all fields.")

            # Demo button handler
            if st.session_state.get("demo_clicked", False):
                set_authenticated(True)
                set_user("demo@barbershop.com")
                st.success("Logged in with demo account!")
                st.balloons()
                st.rerun()

        # Additional links
        st.markdown("---")
        col_forgot, col_register = st.columns(2)

        with col_forgot:
            if st.button("Forgot Password?", use_container_width=True):
                st.info("Password reset functionality coming soon!")

        with col_register:
            if st.button("Create Account", use_container_width=True):
                st.info("Registration coming soon!")

    # Info box
    with st.expander("ℹ️ Demo Credentials"):
        st.markdown("""
        **Demo Account:**
        - Email: `admin@barbershop.com`
        - Password: Any password (demo mode)

        **Features:**
        - Full access to all pages
        - Create, read, update, delete operations
        - Dashboard analytics
        """)