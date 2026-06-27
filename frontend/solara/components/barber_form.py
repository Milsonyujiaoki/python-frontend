"""Barber form component for creating and editing barbers."""

import solara
from .barber_state import add_barber, update_barber, get_barber_by_id

@solara.component
def BarberForm(barber_id=None):
    # If barber_id is provided, we are in edit mode
    # Otherwise, we are in create mode
    barber = None
    if barber_id is not None:
        barber = get_barber_by_id(barber_id)

    # Initialize form state
    name, set_name = solara.use_state(barber.get("name", "") if barber else "")
    email, set_email = solara.use_state(barber.get("email", "") if barber else "")
    phone, set_phone = solara.use_state(barber.get("phone", "") if barber else "")

    def handle_submit():
        # In a real app, we would validate and then call the API
        # For now, we'll just add or update in the local state
        barber_data = {
            "id": barber_id or len(barbers.value) + 1,  # Simple ID generation
            "name": name,
            "email": email,
            "phone": phone,
        }
        if barber_id is not None:
            update_barber(barber_data)
        else:
            add_barber(barber_data)
        # After submission, we could clear the form or close a dialog
        # For now, we'll just print to console
        print("Barber saved:", barber_data)

    return solara.Column([
        solara.Markdown("## " + ("Edit Barber" if barber_id else "Add Barber")),
        solara.InputText(label="Name", value=name, on_value=set_name),
        solara.InputText(label="Email", value=email, on_value=set_email),
        solara.InputText(label="Phone", value=phone, on_value=set_phone),
        solara.Button(
            label="Save",
            on_click=handle_submit,
            color="primary",
        ),
    ])