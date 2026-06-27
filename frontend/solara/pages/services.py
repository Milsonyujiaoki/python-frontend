"""Service management page for Solara frontend."""

import solara
from .components.service_table import ServiceTable
from .service_state import add_service, update_service, get_service_by_id
from .components.service_form import ServiceForm

@solara.component
def ServicesPage():
    # State for showing the form dialog
    show_form, set_show_form = solara.use_state(False)
    # State for whether we are editing or adding
    editing_service_id, set_editing_service_id = solara.use_state(None)
    # Form state
    form_name, set_form_name = solara.use_state("")
    form_description, set_form_description = solara.use_state("")
    form_price, set_form_price = solara.use_state("0.00")

    def open_add_form():
        set_show_form(True)
        set_form_name("")
        set_form_description("")
        set_form_price("0.00")
        set_editing_service_id(None)

    def open_edit_form(service_id):
        set_show_form(True)
        service = get_service_by_id(service_id)
        if service:
            set_form_name(service.get("name", ""))
            set_form_description(service.get("description", ""))
            set_form_price(str(service.get("price", "0.00")))
        set_editing_service_id(service_id)

    def handle_form_submit():
        service_data = {
            "name": form_name,
            "description": form_description,
            "price": float(form_price),
        }
        if editing_service_id is not None:
            service_data["id"] = editing_service_id
            update_service(service_data)
        else:
            # Generate a new ID
            new_id = max([s.get("id", 0) for s in services.value], default=0) + 1
            service_data["id"] = new_id
            add_service(service_data)
        # Close the form
        set_show_form(False)

    def handle_form_cancel():
        set_show_form(False)

    return solara.Column([
        solara.Markdown("# Service Management"),
        solara.Button(
            label="Add New Service",
            on_click=open_add_form,
            color="primary",
            style={"margin-bottom": "20px"},
        ),
        ServiceTable(),
        # Form dialog
        solara.Column(
            style={"display": "block" if show_form else "none"},
            children=[
                solara.Card(
                    title="Edit Service" if editing_service_id is not None else "Add New Service",
                    elevation=1,
                    style={"padding": "20px", "margin": "20px 0", "width": "500px"},
                    children=[
                        solara.InputText(
                            label="Name",
                            value=form_name,
                            on_value=set_form_name,
                        ),
                        solara.InputText(
                            label="Description",
                            value=form_description,
                            on_value=set_form_description,
                        ),
                        solara.InputText(
                            label="Price",
                            value=form_price,
                            on_value=set_form_price,
                            type="number",
                            step="0.01",
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
                            style={"margin-left": "10px"},
                        ),
                    ]
                )
            ]
        )
    ])