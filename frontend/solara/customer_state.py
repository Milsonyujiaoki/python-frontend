"""Customer state management for Solara frontend."""

import solara

# Reactive variables for customer state
customers = solara.reactive([])  # List of customer dictionaries
loading = solara.reactive(False)
error = solara.reactive(None)
# For pagination or filtering, we can add more state as needed

def set_customers(customer_list):
    customers.value = customer_list

def set_loading(is_loading):
    loading.value = is_loading

def set_error(err):
    error.value = err

def add_customer(customer):
    # Add a customer to the list
    customers.value = [*customers.value, customer]

def update_customer(updated_customer):
    # Update an existing customer
    new_list = []
    for c in customers.value:
        if c.get("id") == updated_customer.get("id"):
            new_list.append(updated_customer)
        else:
            new_list.append(c)
    customers.value = new_list

def delete_customer(customer_id):
    # Remove a customer by ID
    customers.value = [c for c in customers.value if c.get("id") != customer_id]

def get_customer_by_id(customer_id):
    for c in customers.value:
        if c.get("id") == customer_id:
            return c
    return None