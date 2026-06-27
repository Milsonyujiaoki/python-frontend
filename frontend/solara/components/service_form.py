"""Service form component for creating and editing services."""

import solara
from .service_state import add_service, update_service, get_service_by_id

@solara.component
def ServiceForm(service_id=None):
    # If service_id is provided, we are in edit mode
    # Otherwise, we are in create mode
    service = None
    if service_id is not None:
        service = get_service_by_id(service_id)

    # Initialize form state
    name, set_name = solara.use_state(service.get("name", "") if service else "")
    description, set_description = solara.use_state(service.get("description", "") if service else "")
    price, set_price = solara.use_state(str(service.get("price", "")) if service else "0.00")

    def handle_submit():
        # In a real app, we would validate and then call the API
        # For now, we'll just add or update in the local state
        try:
            price_val = float(price)
        except ValueError:
            price_val = 0.0
        service_data = {
            "id": service_id or len(services.value) + 1,  # Simple ID generation
            "name": name,
            "description": description,
            "price": price_val,
        }
        if service_id is not None:
            update_service(service_data)
        else:
            add_service(service_data)
        # After submission, we could clear the form or close a dialog
        # For now, we'll just print to console
        print("Service saved:", service_data)

    return solara.Column([
        solara.Markdown("## " + ("Edit Service" if service_id else "Add Service")),
        solara.InputText(label="Name", value=name, on_value=set_name),
        solara.InputText(label="Description", value=description, on_value=set_description),
        solara.InputText(label="Price", value=price, on_value=set_price, type="number", step="0.01"),
        solara.Button(
            label="Save",
            on_click=handle_submit,
            color="primary",
        ),
    ])