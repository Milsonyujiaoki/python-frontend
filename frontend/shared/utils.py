"""
Utility functions for frontend applications.
"""

def format_currency(amount: int) -> str:
    """Format an amount in cents to a currency string."""
    dollars = amount / 100
    return f"${dollars:,.2f}"

def format_date(date_str: str) -> str:
    """Format a date string (YYYY-MM-DD) to a more readable format."""
    # This is a simple example; in practice, you might use datetime parsing
    return date_str  # Placeholder

def generate_id() -> str:
    """Generate a unique identifier."""
    import uuid
    return str(uuid.uuid4())