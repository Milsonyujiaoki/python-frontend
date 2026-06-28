"""Data visualization components for Solara frontend."""

import solara
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import List, Dict, Any

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def fig_to_base64(fig):
    """Convert a matplotlib figure to base64 string for embedding in HTML."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)  # Free memory
    return img_str


@solara.component
def RevenueChart(monthly_data: List[Dict[str, Any]]):
    """
    Display a line chart of monthly revenue.

    Args:
        monthly_data: List of dicts with 'month' and 'revenue' keys
    """
    if not monthly_data:
        return solara.Markdown("No revenue data available")

    # Extract data for plotting
    months = [item.get('month', '') for item in monthly_data]
    revenues = [float(item.get('revenue', 0)) for item in monthly_data]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(months, revenues, marker='o', linewidth=2, markersize=6)
    ax.set_title('Monthly Revenue Trend', fontsize=16, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Revenue ($)', fontsize=12)
    ax.grid(True, alpha=0.3)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert to base64 and display
    img_str = fig_to_base64(fig)
    return solara.Image(
        f"data:image/png;base64,{img_str}",
        width="100%"
    )


@solara.component
def ServicePopularityChart(service_data: List[Dict[str, Any]]):
    """
    Display a bar chart showing popular services.

    Args:
        service_data: List of dicts with 'service_name' and 'count' keys
    """
    if not service_data:
        return solara.Markdown("No service data available")

    # Extract data
    services = [item.get('service_name', 'Unknown') for item in service_data]
    counts = [int(item.get('count', 0)) for item in service_data]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(services, counts, color=plt.cm.Set3(range(len(services))))
    ax.set_title('Service Popularity', fontsize=16, fontweight='bold')
    ax.set_xlabel('Service', fontsize=12)
    ax.set_ylabel('Number of Bookings', fontsize=12)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Convert to base64 and display
    img_str = fig_to_base64(fig)
    return solara.Image(
        f"data:image/png;base64,{img_str}",
        width="100%"
    )


@solara.component
def CustomerDemographicsChart(customer_data: List[Dict[str, Any]]):
    """
    Display a pie chart of customer demographics (age groups).

    Args:
        customer_data: List of dicts with 'age_group' and 'count' keys
    """
    if not customer_data:
        return solara.Markdown("No customer data available")

    # Extract data
    labels = [item.get('age_group', 'Unknown') for item in customer_data]
    sizes = [int(item.get('count', 0)) for item in customer_data]

    # Filter out zero values
    non_zero_indices = [i for i, size in enumerate(sizes) if size > 0]
    labels = [labels[i] for i in non_zero_indices]
    sizes = [sizes[i] for i in non_zero_indices]

    if not sizes:
        return solara.Markdown("No customer demographic data available")

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1(range(len(labels)))
    )
    ax.set_title('Customer Age Distribution', fontsize=16, fontweight='bold')

    # Improve text appearance
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.tight_layout()

    # Convert to base64 and display
    img_str = fig_to_base64(fig)
    return solara.Image(
        f"data:image/png;base64,{img_str}",
        width="100%"
    )


@solara.component
def AnalyticsDashboard():
    """
    A comprehensive dashboard showing various analytics visualizations.
    In a real application, this data would come from API calls to the backend.
    """
    # Sample data - in a real app, this would come from backend API calls
    sample_revenue_data = [
        {"month": "Jan", "revenue": 4500},
        {"month": "Feb", "revenue": 5200},
        {"month": "Mar", "revenue": 4800},
        {"month": "Apr", "revenue": 6100},
        {"month": "May", "revenue": 5800},
        {"month": "Jun", "revenue": 7200},
    ]

    sample_service_data = [
        {"service_name": "Haircut", "count": 45},
        {"service_name": "Haircut & Beard", "count": 32},
        {"service_name": "Shave", "count": 18},
        {"service_name": "Hair Wash", "count": 25},
        {"service_name": "Styling", "count": 22},
    ]

    sample_customer_data = [
        {"age_group": "18-25", "count": 12},
        {"age_group": "26-35", "count": 28},
        {"age_group": "36-45", "count": 22},
        {"age_group": "46-55", "count": 15},
        {"age_group": "56+", "count": 10},
    ]

    return solara.Column([
        solara.Title("Barbershop Analytics Dashboard"),
        solara.Markdown("# Analytics Dashboard"),

        # Revenue Chart
        solara.Card(
            title="Monthly Revenue Trend",
            children=[
                RevenueChart(monthly_data=sample_revenue_data)
            ],
            style={"padding": "20px", "margin-bottom": "20px"}
        ),

        # Service Popularity and Customer Demographics side by side
        solara.Row([
            solara.Column([
                solara.Card(
                    title="Service Popularity",
                    children=[
                        ServicePopularityChart(service_data=sample_service_data)
                    ],
                    style={"padding": "20px"}
                )
            ],
            style={"flex": "1", "margin-right": "10px"}
            ),
            solara.Column([
                solara.Card(
                    title="Customer Age Distribution",
                    children=[
                        CustomerDemographicsChart(customer_data=sample_customer_data)
                    ],
                    style={"padding": "20px"}
                )
            ],
            style={"flex": "1", "margin-left": "10px"}
            )
        ])
    ])