"""Customer state management for Solara frontend."""

import solara

# Reactive variable for the list of customers
customers = solara.reactive([])

def get_customer_by_id(customer_id):
    """Get a customer by ID."""
    for c in customers.value:
        if c.get("id") == customer_id:
            return c
    return None

def add_customer(customer):
    """Add a new customer."""
    customers.value = [*customers.value, customer]

def update_customer(customer):
    """Update an existing customer."""
    new_customers = []
    for c in customers.value:
        if c.get("id") == customer.get("id"):
            new_customers.append(customer)
        else:
            new_customers.append(c)
    customers.value = new_customers

def delete_customer(customer_id):
    """Delete a customer by ID."""
    customers.value = [c for c in customers.value if c.get("id") != customer_id]

def clear_customers():
    """Clear all customers (for testing)."""
    customers.value = []