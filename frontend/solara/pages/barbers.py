"""Barber management page for Solara frontend."""

import solara
from .components.barber_table import BarberTable
from .barber_state import add_barber, update_barber, get_barber_by_id
from .components.barber_form import BarberForm

@solara.component
def BarbersPage():
    # State for showing the form dialog
    show_form, set_show_form = solara.use_state(False)
    # State for whether we are editing or adding
    editing_barber_id, set_editing_barber_id = solara.use_state(None)
    # Form state
    form_name, set_form_name = solara.use_state("")
    form_email, set_form_email = solara.use_state("")
    form_phone, set_form_phone = solara.use_state("")

    def open_add_form():
        set_show_form(True)
        set_form_name("")
        set_form_email("")
        set_form_phone("")
        set_editing_barber_id(None)

    def open_edit_form(barber_id):
        set_show_form(True)
        barber = get_barber_by_id(barber_id)
        if barber:
            set_form_name(barber.get("name", ""))
            set_form_email(barber.get("email", ""))
            set_form_phone(barber.get("phone", ""))
        set_editing_barber_id(barber_id)

    def handle_form_submit():
        barber_data = {
            "name": form_name,
            "email": form_email,
            "phone": form_phone,
        }
        if editing_barber_id is not None:
            barber_data["id"] = editing_barber_id
            update_barber(barber_data)
        else:
            # Generate a new ID
            new_id = max([b.get("id", 0) for b in barbers.value], default=0) + 1
            barber_data["id"] = new_id
            add_barber(barber_data)
        # Close the form
        set_show_form(False)

    def handle_form_cancel():
        set_show_form(False)

    return solara.Column([
        solara.Markdown("# Barber Management"),
        solara.Button(
            label="Add New Barber",
            on_click=open_add_form,
            color="primary",
            style={"margin-bottom": "20px"},
        ),
        BarberTable(),
        # Form dialog
        solara.Column(
            style={"display": "block" if show_form else "none"},
            children=[
                solara.Card(
                    title="Edit Barber" if editing_barber_id is not None else "Add New Barber",
                    elevation=1,
                    style={"padding": "20px", "margin": "20px 0", "width": "500px"},
                    children=[
                        solara.InputText(
                            label="Name",
                            value=form_name,
                            on_value=set_form_name,
                        ),
                        solara.InputText(
                            label="Email",
                            value=form_email,
                            on_value=set_form_email,
                            placeholder="email@example.com",
                        ),
                        solara.InputText(
                            label="Phone",
                            value=form_phone,
                            on_value=set_form_phone,
                        ),
                        solara.Button(
                            label="Cancel",
                            on_click=handle_form_cancel,
                            text=True,
                        ),
                        solara.Button(
                            label="Save",
                            on_click=handle_form_submit,
                            color="primary",
                        ),
                    ]
                )
            ]
        )
    ])