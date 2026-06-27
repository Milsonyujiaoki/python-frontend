import reflex as rx
from state import ReflexAuthState
from components.nav import layout
from components import form_input, form_button, form_alert, data_table


class CustomerState(ReflexAuthState):
    """State for customer management."""

    customers: list = []
    loading: bool = False
    creating: bool = False
    editing: bool = False
    deleting: bool = False
    editing_customer: dict = {}

    # Form fields for create/edit
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""

    @rx.var
    def is_creating(self) -> bool:
        return self.creating

    @rx.var
    def is_editing(self) -> bool:
        return self.editing

    @rx.var
    def form_valid(self) -> bool:
        """Return True if the customer form is valid (basic validation)."""
        return bool(self.first_name and self.last_name and self.email and self.phone)

    def load_customers(self):
        """Load customers from the API."""
        self.set_loading(True)
        try:
            response = self.api_service.get("/api/v1/customers/")
            self.customers = response if isinstance(response, list) else []
        except Exception as e:
            self.set_error(f"Failed to load customers: {str(e)}")
        finally:
            self.set_loading(False)

    def create_customer(self):
        """Create a new customer."""
        self.set_creating(True)
        self.clear_error()
        try:
            response = self.api_service.post(
                "/api/v1/customers/",
                {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "phone": self.phone
                }
            )
            if response:
                self.customers.append(response)
                self.clear_form()
                self.set_success("Customer created successfully!")
        except Exception as e:
            self.set_error(f"Failed to create customer: {str(e)}")
        finally:
            self.set_creating(False)

    def update_customer(self):
        """Update an existing customer."""
        if not self.editing_customer:
            return

        self.set_creating(True)
        self.clear_error()
        try:
            customer_id = self.editing_customer.get("id")
            response = self.api_service.put(
                f"/api/v1/customers/{customer_id}",
                {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "phone": self.phone
                }
            )
            if response:
                # Update the customer in the list
                for i, customer in enumerate(self.customers):
                    if customer.get("id") == customer_id:
                        self.customers[i] = response
                        break
                self.cancel_edit()
                self.set_success("Customer updated successfully!")
        except Exception as e:
            self.set_error(f"Failed to update customer: {str(e)}")
        finally:
            self.set_creating(False)

    def delete_customer(self, customer_id: int):
        """Delete a customer."""
        self.set_deleting(True)
        self.clear_error()
        try:
            self.api_service.delete(f"/api/v1/customers/{customer_id}")
            # Remove from list
            self.customers = [c for c in self.customers if c.get("id") != customer_id]
            self.set_success("Customer deleted successfully!")
        except Exception as e:
            self.set_error(f"Failed to delete customer: {str(e)}")
        finally:
            self.set_deleting(False)

    def start_edit(self, customer: dict):
        """Start editing a customer."""
        self.editing = True
        self.editing_customer = customer
        self.first_name = customer.get("first_name", "")
        self.last_name = customer.get("last_name", "")
        self.email = customer.get("email", "")
        self.phone = customer.get("phone", "")

    def cancel_edit(self):
        """Cancel editing a customer."""
        self.editing = False
        self.editing_customer = {}
        self.clear_form()

    def clear_form(self):
        """Clear the form fields."""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""

    def clear_messages(self):
        """Clear error and success messages."""
        self.clear_error()
        self.clear_success()

    def set_deleting(self, deleting: bool):
        """Set deleting state."""
        self.deleting = deleting

    # Form field setters - required for Reflex on_change handlers
    def set_first_name(self, name: str):
        """Set first name."""
        self.first_name = name

    def set_last_name(self, name: str):
        """Set last name."""
        self.last_name = name

    def set_email(self, email: str):
        """Set email."""
        self.email = email

    def set_phone(self, phone: str):
        """Set phone."""
        self.phone = phone

    def set_creating(self, creating: bool):
        """Set creating state."""
        self.creating = creating

    def set_editing(self, editing: bool):
        """Set editing state."""
        self.editing = editing


def customers_page() -> rx.Component:
    """Customer management page component with responsive design."""
    return layout(
        rx.container(
            rx.cond(
                ReflexAuthState.is_authenticated,
                rx.vstack(
                    rx.hstack(
                        rx.heading("Customer Management", size=["lg", "xl", "2xl"]),  # Responsive heading size
                        rx.spacer(),
                        rx.button(
                            rx.cond(
                                CustomerState.creating | CustomerState.editing,
                                rx.spinner(size="sm"),
                                "Add New Customer"
                            ),
                            on_click=lambda: CustomerState.cancel_edit(),
                            color_scheme="green",
                            disabled=CustomerState.creating | CustomerState.editing | ~CustomerState.form_valid,
                            size=["md", "lg", "lg"],  # Responsive button size
                        ),
                        width="100%",
                        align="center",
                        # Responsive padding
                        padding_x=["1em", "1.5em", "2em"],
                    ),
                    rx.cond(
                        CustomerState.creating | CustomerState.editing,
                        rx.card(
                            rx.vstack(
                                rx.heading(
                                    "Edit Customer" if CustomerState.editing else "Add New Customer",
                                    size="lg"
                                ),
                                rx.form(
                                    rx.vstack(padding=["1em", "1.5em", "2em"],
                                        rx.input(
                                            placeholder="First Name",
                                            value=CustomerState.first_name,
                                            on_change=CustomerState.set_first_name,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"]  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Last Name",
                                            value=CustomerState.last_name,
                                            on_change=CustomerState.set_last_name,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"]  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Email",
                                            type="email",
                                            value=CustomerState.email,
                                            on_change=CustomerState.set_email,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"]  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Phone",
                                            value=CustomerState.phone,
                                            on_change=CustomerState.set_phone,
                                            width="100%",
                                            size=["md", "lg", "lg"]  # Responsive input size
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Cancel",
                                                on_click=CustomerState.cancel_edit,
                                                variant="outline",
                                                size=["md", "lg", "lg"],
                                            ),
                                            rx.button(
                                                rx.condition(
                                                    CustomerState.editing,
                                                    "Update Customer",
                                                    "Create Customer"
                                                ),
                                                on_click=rx.condition(
                                                    CustomerState.editing,
                                                    CustomerState.update_customer,
                                                    CustomerState.create_customer
                                                ),
                                                loading=CustomerState.creating,
                                                color_scheme=rx.condition(
                                                    CustomerState.editing,
                                                    "blue",
                                                    "green"
                                                ),
                                                disabled=~CustomerState.form_valid,
                                                size=["md", "lg", "lg"],
                                            ),
                                            spacing="3",
                                            width="100%",
                                            justify="end",
                                        ),
                                        rx.alert(
                                            rx.alert_icon(),
                                            rx.alert_title(CustomerState.error_message),
                                            status="error",
                                            is_visible=CustomerState.error_message != "",
                                            mt=3,
                                        ),
                                        rx.alert(
                                            rx.alert_icon(),
                                            rx.alert_title(CustomerState.success_message),
                                            status="success",
                                            is_visible=CustomerState.success_message != "",
                                            mt=3,
                                        ),
                                ),
                                    width="100%",
                                    on_submit=rx.condition(
                                        CustomerState.editing,
                                        CustomerState.update_customer,
                                        CustomerState.create_customer
                                    ),
                                    reset_on_submit=False
                                ),
                                width="100%",
                                max_width="500px",
                            ),
                            rx.button(
                                "×",
                                position="absolute",
                                top="0",
                                right="0",
                                on_click=CustomerState.cancel_edit,
                                variant="ghost",
                                size="1",
                            ),
                            position="relative",
                            border="1px solid",
                            border_color=rx.cond(
                                CustomerState.editing,
                                "blue.300",
                                "green.300"
                            ),
                            mt=4,
                        ),
                    ),
                    rx.divider(mt=4),
                    rx.cond(
                        CustomerState.loading,
                        rx.center(rx.spinner(), py=8),
                        rx.cond(
                            CustomerState.customers.length() > 0,
                            data_table(
                                columns=[
                                    {"header": "First Name", "key": "first_name", "size": ["sm", "md", "md"]},
                                    {"header": "Last Name", "key": "last_name", "size": ["sm", "md", "md"]},
                                    {"header": "Email", "key": "email", "size": ["sm", "md", "md"]},
                                    {"header": "Phone", "key": "phone", "size": ["sm", "md", "md"]},
                                    {"header": "Actions", "key": lambda row: "actions", "size": ["sm", "md", "md"]},  # Placeholder key for actions
                                ],
                                data=CustomerState.customers,
                                actions=[
                                    {
                                        "label": "Edit",
                                        "on_click": lambda row: CustomerState.start_edit(row),
                                        "color_scheme": "blue",
                                        "size": ["sm", "md", "md"],
                                    },
                                    {
                                        "label": "Delete",
                                        "on_click": lambda row: CustomerState.delete_customer(row.get("id")),
                                        "color_scheme": "red",
                                        "size": ["sm", "md", "md"],
                                        "loading": lambda row: CustomerState.deleting,
                                        "disabled": lambda row: CustomerState.deleting,
                                    }
                                ],
                                loading=False,  # We handle loading above
                            ),
                            rx.center(
                                rx.text("No customers found.", color="gray", py=[4, 6, 8]),
                            )
                        ),
                    ),
                    rx.spacer(),
                    rx.center(
                        rx.badge(
                            f"Logged in as: {ReflexAuthState.current_user.get('email', 'User')}",
                            color_scheme="green"
                        )
                    ),
                    spacing="5",
                    justify="center",
                    min_height="85vh",
                    on_mount=CustomerState.load_customers,
                ),
                rx.redirect("/login")
            ),
        )
    )


# Export for import in main.py
customers = customers_page