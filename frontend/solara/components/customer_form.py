"""Customer form component for creating and editing customers."""

import solara
from .state import add_customer, update_customer, get_customer_by_id

@solara.component
def CustomerForm(customer_id=None):
    # If customer_id is provided, we are in edit mode
    # Otherwise, we are in create mode
    customer = None
    if customer_id is not None:
        customer = get_customer_by_id(customer_id)

    # Initialize form state
    name, set_name = solara.use_state(customer.get("name", "") if customer else "")
    email, set_email = solara.use_state(customer.get("email", "") if customer else "")
    phone, set_phone = solara.use_state(customer.get("phone", "") if customer else "")
    # We can add more fields as needed

    def handle_submit():
        # In a real app, we would validate and then call the API
        # For now, we'll just add or update in the local state
        customer_data = {
            "id": customer_id or len(customers.value) + 1,  # Simple ID generation
            "name": name,
            "email": email,
            "phone": phone,
        }
        if customer_id is not None:
            update_customer(customer_data)
        else:
            add_customer(customer_data)
        # After submission, we could clear the form or close a dialog
        # For now, we'll just show a success message (to be implemented)
        print("Customer saved:", customer_data)

    return solara.Column([
        solara.Markdown("## " + ("Edit Customer" if customer_id else "Add Customer")),
        solara.InputText(label="Name", value=name, on_value=set_name),
        solara.InputText(label="Email", value=email, on_value=set_email),
        solara.InputText(label="Phone", value=phone, on_value=set_phone),
        solara.Button(
            label="Save",
            on_click=handle_submit,
            color="primary",
        ),
    ])