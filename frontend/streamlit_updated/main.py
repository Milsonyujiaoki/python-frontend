"""
✂️ BarberPro - Streamlit Frontend

Design Reference: Stripe Dashboard + Shopify
- Data-rich professional interface
- Clean information hierarchy
- Powerful filtering and search
- Business metrics focused

Style: Modern fintech/professional SaaS
"""
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import time

# =============================================================================
# CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="BarberPro - Dashboard",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'http://localhost:8000/docs',
        'Report a bug': "https://github.com/barberpro/app/issues",
        'About': "# BarberPro v1.0\n\nProfessional barbershop management platform."
    }
)

API_BASE_URL = "http://localhost:8000/api/v1"

# Brand colors (Stripe-inspired)
PRIMARY_COLOR = "#635bff"  # Stripe purple
SUCCESS_COLOR = "#0acf82"   # Stripe green
WARNING_COLOR = "#ffab00"
ERROR_COLOR = "#ff4136"

# Custom CSS for Stripe-like styling
st.markdown("""
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global styles */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom card styling */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 24px;
    color: white;
    box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11);
    margin: 10px 0;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
}

.metric-label {
    font-size: 14px;
    opacity: 0.9;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #635bff 0%, #5346e8 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 91, 255, 0.4);
}

/* DataFrame styling */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1c23 0%, #0d0f14 100%);
}

[data-testid="stSidebar"] .css-1d392oz {
    color: white;
}

/* Input styling */
.stTextInput > div > div > input {
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    padding: 10px 14px;
    font-size: 14px;
}

.stTextInput > div > div > input:focus {
    border-color: #635bff;
    box-shadow: 0 0 0 3px rgba(99, 91, 255, 0.15);
}

/* Success message */
.stAlert-success {
    background: linear-gradient(135deg, #0a6c2d 0%, #0a8f3a 100%);
    border: none;
    border-radius: 8px;
}

/* Metric cards in columns */
.css-1r6y92x {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# API CLIENT
# =============================================================================

@st.cache_data
def fetch_customers():
    """Fetch customers from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/customers/", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


@st.cache_data
def fetch_barbers():
    """Fetch barbers from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/barbers/", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


@st.cache_data
def fetch_services():
    """Fetch services from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/services/", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


def create_customer(data: dict) -> dict:
    """Create a new customer."""
    try:
        response = requests.post(f"{API_BASE_URL}/customers/", json=data, timeout=10)
        return response.json() if response.status_code == 201 else None
    except:
        return None


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

def render_sidebar():
    """Render sidebar navigation."""
    with st.sidebar:
        # Logo
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("✂️", unsafe_allow_html=True)
        with col2:
            st.markdown("### BarberPro")

        st.markdown("---")

        # Navigation
        menu_options = {
            "📊 Dashboard": "dashboard",
            "👥 Customers": "customers",
            "💈 Barbers": "barbers",
            "💇 Services": "services",
            "📈 Analytics": "analytics",
            "⚙️ Settings": "settings",
        }

        for label, page_key in menu_options.items():
            if st.button(
                label,
                use_container_width=True,
                key=f"nav_{page_key}",
                type="primary" if st.session_state.page == page_key else "secondary"
            ):
                st.session_state.page = page_key

        st.markdown("---")

        # User section
        if st.session_state.authenticated:
            st.markdown(f"👤 **{st.session_state.user_email}**")
            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_email = None
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()


# =============================================================================
# PAGES
# =============================================================================

def render_dashboard():
    """Dashboard page with Stripe-style metrics."""

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Dashboard")
        st.markdown("Your barbershop performance at a glance")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh"):
            st.rerun()

    # Fetch data
    customers = fetch_customers()
    barbers = fetch_barbers()
    services = fetch_services()

    # Calculate metrics
    total_customers = len(customers)
    active_barbers = len([b for b in barbers if b.get('is_active', True)])
    total_services = len(services)

    # Revenue simulation (would come from appointments in real app)
    today_revenue = 2450
    week_revenue = 15680
    revenue_growth = 18.5

    # Top row metrics - Stripe style
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="metric-label">Total Customers</div>
            <div class="metric-value">{total_customers}</div>
            <div style="font-size: 12px; margin-top: 8px; opacity: 0.8;">📈 +12% vs last week</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #0a8f3a 0%, #0a6c2d 100%);">
            <div class="metric-label">Active Barbers</div>
            <div class="metric-value">{active_barbers}</div>
            <div style="font-size: 12px; margin-top: 8px; opacity: 0.8;">💼 All on shift</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="metric-label">Services</div>
            <div class="metric-value">{total_services}</div>
            <div style="font-size: 12px; margin-top: 8px; opacity: 0.8;">🎯 5 categories</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); color: #1a1c23;">
            <div class="metric-label">Today's Revenue</div>
            <div class="metric-value" style="color: #1a1c23;">R$ {today_revenue:,}</div>
            <div style="font-size: 12px; margin-top: 8px; color: #0a6c2d;">📈 +{revenue_growth}% vs yesterday</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Second row - Charts and tables
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📅 Recent Activity")

        # Simulated appointments
        activity_data = pd.DataFrame({
            'Time': ['09:00', '10:00', '11:30', '13:00', '14:30', '16:00'],
            'Customer': ['Carlos Silva', 'André Costa', 'Bruno Lima', 'Pedro Rocha', 'Lucas Mendes', 'Rafael Souza'],
            'Barber': ['Mike', 'Sarah', 'Mike', 'Tom', 'Sarah', 'Mike'],
            'Service': ['Fade', 'Coloring', 'Beard Trim', 'Full Cut', 'Hair Cut', 'Fade'],
            'Status': ['✓ Completed', '⏳ In Progress', '⏳ Pending', '⏳ Pending', '⏳ Pending', '⏳ Pending'],
            'Value': ['R$ 40', 'R$ 80', 'R$ 20', 'R$ 45', 'R$ 35', 'R$ 40']
        })

        st.dataframe(
            activity_data,
            use_container_width=True,
            hide_index=True,
        )

    with col2:
        st.subheader("⚡ Quick Stats")

        # Progress metrics
        st.markdown("**Today's Capacity**")
        st.progress(0.75)
        st.caption("75% booked (9/12 slots)")

        st.markdown("**Weekly Goal**")
        st.progress(0.68)
        st.caption("68% of R$ 23.000 goal")

        st.markdown("**Customer Satisfaction**")
        st.progress(0.94)
        st.caption("94% positive reviews")

        # Top services
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Top Services This Week**")

        top_services = pd.DataFrame({
            'Service': ['Fade', 'Hair Cut', 'Beard Trim', 'Coloring'],
            'Bookings': [45, 38, 22, 15]
        })
        st.bar_chart(top_services.set_index('Service'))


def render_customers():
    """Customers management page."""
    st.title("👥 Customers")
    st.markdown("Manage your customer relationships")

    # Fetch data
    customers = fetch_customers()

    # Actions bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by name or email...", label_visibility="collapsed")
    with col2:
        filter_status = st.selectbox("Status", ["All", "Active", "Inactive"])
    with col3:
        add_clicked = st.button("➕ Add Customer", use_container_width=True)

    # Filter customers
    filtered = customers
    if search:
        filtered = [
            c for c in filtered
            if search.lower() in c.get('first_name', '').lower()
            or search.lower() in c.get('last_name', '').lower()
            or search.lower() in c.get('email', '').lower()
        ]

    # Display
    if filtered:
        df_data = []
        for c in filtered:
            df_data.append({
                'Name': f"{c.get('first_name', '')} {c.get('last_name', '')}",
                'Email': c.get('email', ''),
                'Phone': c.get('phone', '-') or '-',
                'Status': 'Active' if c.get('is_active', True) else 'Inactive',
                'Created': c.get('created_at', '')[:10] if c.get('created_at') else '-',
            })

        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No customers found. Add your first customer!")

    # Add customer modal simulation
    if add_clicked:
        with st.form("add_customer"):
            st.subheader("Add New Customer")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name *")
                email = st.text_input("Email *")
                phone = st.text_input("Phone")
            with col2:
                last_name = st.text_input("Last Name *")
                dob = st.date_input("Date of Birth", None)
                notes = st.text_area("Notes")

            submitted = st.form_submit_button("Create Customer", use_container_width=True)

            if submitted:
                if first_name and last_name and email:
                    result = create_customer({
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "date_of_birth": dob.isoformat() if dob else None,
                        "notes": notes,
                    })
                    if result:
                        st.success("✅ Customer created successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Failed to create customer")
                else:
                    st.error("Please fill in required fields")


def render_barbers():
    """Barbers management page."""
    st.title("💈 Barbers")
    st.markdown("Your team of professionals")

    barbers = fetch_barbers()

    # Add barber button
    if st.button("➕ Add Barber"):
        st.info("Form coming soon!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Display as cards
    for i, barber in enumerate(barbers):
        with st.container():
            col1, col2 = st.columns([1, 3])

            with col1:
                # Avatar
                initial = barber.get('first_name', '?')[0]
                st.markdown(f"""
                <div style="
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #635bff 0%, #5346e8 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                ">{initial}</div>
                """, unsafe_allow_html=True)

            with col2:
                st.subheader(f"{barber.get('first_name', '')} {barber.get('last_name', '')}")
                st.caption(f"💼 {barber.get('specialty', 'General')}")

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    status = "🟢 Active" if barber.get('is_active', True) else "🔴 Inactive"
                    st.markdown(status)
                with col_b:
                    st.markdown(f"⭐ 4.9 rating")
                with col_c:
                    if barber.get('bio'):
                        st.caption(barber.get('bio', '')[:30] + "...")

                st.markdown("---")


def render_services():
    """Services management page."""
    st.title("💇 Services")
    st.markdown("Manage your service offerings")

    services = fetch_services()

    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search services", placeholder="Search...", label_visibility="collapsed")
    with col2:
        active_only = st.checkbox("Active only", value=True)

    # Filter
    filtered = services
    if search:
        filtered = [s for s in filtered if search.lower() in s.get('name', '').lower()]
    if active_only:
        filtered = [s for s in filtered if s.get('is_active', True)]

    # Display as table
    if filtered:
        df_data = []
        for s in filtered:
            df_data.append({
                'Service': s.get('name', ''),
                'Description': s.get('description', '')[:60] + ('...' if len(s.get('description', '')) > 60 else ''),
                'Price': f"R$ {s.get('price', 0) / 100:.2f}",
                'Duration': f"{s.get('duration_minutes', 0)} min",
                'Status': '🟢 Active' if s.get('is_active', True) else '🔴 Inactive',
            })

        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        st.info("No services found.")


def render_login():
    """Login page."""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <div style="font-size: 64px;">✂️</div>
            <h1 style="color: #1a1c23;">BarberPro</h1>
            <p style="color: #888;">Professional Barbershop Management</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="demo@barberpro.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")

            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Login", use_container_width=True)
            with col2:
                demo = st.form_submit_button("Demo Login", use_container_width=True)

            if demo:
                st.session_state.authenticated = True
                st.session_state.user_email = "demo@barberpro.com"
                st.session_state.page = 'dashboard'
                st.rerun()

            if submitted:
                if email and password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("Please enter email and password")


def render_analytics():
    """Analytics page (placeholder)."""
    st.title("📈 Analytics")
    st.markdown("Deep insights into your business performance")

    st.info("🚧 Advanced analytics coming soon!")

    # Mock chart
    chart_data = pd.DataFrame({
        'Week': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Revenue': [1800, 2200, 1950, 2400, 3100, 4200, 2800],
        'Customers': [18, 22, 19, 24, 31, 42, 28]
    })

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Weekly Revenue")
        st.bar_chart(chart_data.set_index('Week')[['Revenue']])
    with col2:
        st.subheader("Daily Customers")
        st.line_chart(chart_data.set_index('Week')[['Customers']])


def render_settings():
    """Settings page (placeholder)."""
    st.title("⚙️ Settings")
    st.markdown("Customize your barbershop experience")

    with st.form("settings"):
        st.subheader("🏪 Shop Information")
        shop_name = st.text_input("Shop Name", value="BarberPro")
        shop_email = st.text_input("Email", value="contact@barberpro.com")
        shop_phone = st.text_input("Phone", value="+55 11 99999-9999")

        st.subheader("🎨 Branding")
        primary_color = st.color_picker("Primary Color", "#635bff")
        secondary_color = st.color_picker("Secondary Color", "#0a8f3a")

        st.subheader("🔔 Notifications")
        email_notifications = st.checkbox("Email notifications", value=True)
        sms_notifications = st.checkbox("SMS notifications", value=False)

        submitted = st.form_submit_button("Save Settings", use_container_width=True)

        if submitted:
            st.success("Settings saved successfully!")


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    """Main application entry point."""

    # Check authentication
    if not st.session_state.authenticated:
        if st.session_state.page == 'login':
            render_login()
        else:
            # Show landing page
            render_sidebar()
            render_dashboard()
    else:
        render_sidebar()

        # Route to page
        page = st.session_state.page
        if page == 'dashboard':
            render_dashboard()
        elif page == 'customers':
            render_customers()
        elif page == 'barbers':
            render_barbers()
        elif page == 'services':
            render_services()
        elif page == 'analytics':
            render_analytics()
        elif page == 'settings':
            render_settings()
        elif page == 'login':
            render_login()
        else:
            st.error("Page not found")


if __name__ == "__main__":
    main()