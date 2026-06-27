"""Customer management page for Solara frontend."""

import solara
from .components.customer_table import CustomerTable
from .customer_state import add_customer, update_customer, get_customer_by_id
from .components.customer_form import CustomerForm

@solara.component
def CustomersPage():
    # State for showing the form dialog
    show_form, set_show_form = solara.use_state(False)
    # State for whether we are editing or adding
    editing_customer_id, set_editing_customer_id = solara.use_state(None)
    # Form state
    form_name, set_form_name = solara.use_state("")
    form_email, set_form_email = solara.use_state("")
    form_phone, set_form_phone = solara.use_state("")

    def open_add_form():
        set_show_form(True)
        set_form_name("")
        set_form_email("")
        set_form_phone("")
        set_editing_customer_id(None)

    def open_edit_form(customer_id):
        set_show_form(True)
        customer = get_customer_by_id(customer_id)
        if customer:
            set_form_name(customer.get("name", ""))
            set_form_email(customer.get("email", ""))
            set_form_phone(customer.get("phone", ""))
        set_editing_customer_id(customer_id)

    def handle_form_submit():
        customer_data = {
            "name": form_name,
            "email": form_email,
            "phone": form_phone,
        }
        if editing_customer_id is not None:
            customer_data["id"] = editing_customer_id
            update_customer(customer_data)
        else:
            # Generate a new ID
            new_id = max([c.get("id", 0) for c in customers.value], default=0) + 1
            customer_data["id"] = new_id
            add_customer(customer_data)
        # Close the form
        set_show_form(False)

    def handle_form_cancel():
        set_show_form(False)

    return solara.Column([
        solara.Markdown("# Customer Management"),
        solara.Button(
            label="Add New Customer",
            on_click=open_add_form,
            color="primary",
            style={"margin-bottom": "20px"},
        ),
        CustomerTable(),
        # Form dialog
        solara.Column(
            style={"display": "block" if show_form else "none"},
            children=[
                solara.Card(
                    title="Edit Customer" if editing_customer_id is not None else "Add New Customer",
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
                            style={"margin-left": "10px"},
                        ),
                    ]
                )
            ]
        )
    ])