import reflex as rx
from state import ReflexAuthState
from components.nav import layout


class ServiceState(ReflexAuthState):
    """State for service management."""

    services: list = []
    loading: bool = False
    creating: bool = False
    editing: bool = False
    deleting: bool = False
    editing_service: dict = {}

    # Form fields for create/edit
    name: str = ""
    description: str = ""
    price: float = 0.0
    duration: int = 30  # minutes

    @rx.var
    def is_creating(self) -> bool:
        return self.creating

    @rx.var
    def is_editing(self) -> bool:
        return self.editing

    @rx.var
    def form_valid(self) -> bool:
        """Return True if the service form is valid (basic validation)."""
        return bool(self.name and self.description and self.price > 0 and self.duration > 0)

    def load_services(self):
        """Load services from the API."""
        self.set_loading(True)
        try:
            response = self.api_service.get("/api/v1/services/")
            self.services = response if isinstance(response, list) else []
        except Exception as e:
            self.set_error(f"Failed to load services: {str(e)}")
        finally:
            self.set_loading(False)

    def create_service(self):
        """Create a new service."""
        self.set_creating(True)
        self.clear_error()
        try:
            response = self.api_service.post(
                "/api/v1/services/",
                {
                    "name": self.name,
                    "description": self.description,
                    "price": self.price,
                    "duration": self.duration
                }
            )
            if response:
                self.services.append(response)
                self.clear_form()
                self.set_success("Service created successfully!")
        except Exception as e:
            self.set_error(f"Failed to create service: {str(e)}")
        finally:
            self.set_creating(False)

    def update_service(self):
        """Update an existing service."""
        if not self.editing_service:
            return

        self.set_creating(True)
        self.clear_error()
        try:
            service_id = self.editing_service.get("id")
            response = self.api_service.put(
                f"/api/v1/services/{service_id}",
                {
                    "name": self.name,
                    "description": self.description,
                    "price": self.price,
                    "duration": self.duration
                }
            )
            if response:
                # Update the service in the list
                for i, service in enumerate(self.services):
                    if service.get("id") == service_id:
                        self.services[i] = response
                        break
                self.cancel_edit()
                self.set_success("Service updated successfully!")
        except Exception as e:
            self.set_error(f"Failed to update service: {str(e)}")
        finally:
            self.set_creating(False)

    def delete_service(self, service_id: int):
        """Delete a service."""
        self.set_deleting(True)
        self.clear_error()
        try:
            self.api_service.delete(f"/api/v1/services/{service_id}")
            # Remove from list
            self.services = [s for s in self.services if s.get("id") != service_id]
            self.set_success("Service deleted successfully!")
        except Exception as e:
            self.set_error(f"Failed to delete service: {str(e)}")
        finally:
            self.set_deleting(False)

    def start_edit(self, service: dict):
        """Start editing a service."""
        self.editing = True
        self.editing_service = service
        self.name = service.get("name", "")
        self.description = service.get("description", "")
        self.price = float(service.get("price", 0.0))
        self.duration = int(service.get("duration", 30))

    def cancel_edit(self):
        """Cancel editing a service."""
        self.editing = False
        self.editing_service = {}
        self.clear_form()

    def clear_form(self):
        """Clear the form fields."""
        self.name = ""
        self.description = ""
        self.price = 0.0
        self.duration = 30

    def clear_messages(self):
        """Clear error and success messages."""
        self.clear_error()
        self.clear_success()

    def set_deleting(self, deleting: bool):
        """Set deleting state."""
        self.deleting = deleting

    # Form field setters - required for Reflex on_change handlers
    def set_name(self, name: str):
        """Set service name."""
        self.name = name

    def set_description(self, description: str):
        """Set service description."""
        self.description = description

    def set_price(self, price: float):
        """Set service price."""
        self.price = price

    def set_duration(self, duration: int):
        """Set service duration."""
        self.duration = duration

    def set_creating(self, creating: bool):
        """Set creating state."""
        self.creating = creating

    def set_editing(self, editing: bool):
        """Set editing state."""
        self.editing = editing


def services_page() -> rx.Component:
    """Service management page component."""
    return layout(
        rx.container(
            rx.cond(
                ReflexAuthState.is_authenticated,
                rx.vstack(
                    rx.hstack(
                        rx.heading("Service Management", size=["lg", "xl", "2xl"]),  # Responsive heading size
                        rx.spacer(),
                        rx.button(
                            rx.cond(
                                ServiceState.creating | ServiceState.editing,
                                rx.spinner(size="sm"),
                                "Add New Service"
                            ),
                            on_click=lambda: ServiceState.cancel_edit(),
                            color_scheme="green",
                            disabled=ServiceState.creating | ServiceState.editing | ~ServiceState.form_valid,
                            size=["md", "lg", "lg"],  # Responsive button size
                        ),
                        width="100%",
                        align="center",
                        # Responsive padding
                        padding_x=["1em", "1.5em", "2em"],
                    ),
                    rx.cond(
                        ServiceState.creating | ServiceState.editing,
                        rx.card(
                            rx.vstack(
                                rx.heading(
                                    "Edit Service" if ServiceState.editing else "Add New Service",
                                    size="lg"
                                ),
                                rx.form(
                                    rx.vstack(
                                        padding=["1em", "1.5em", "2em"],  # Responsive form padding
                                        rx.input(
                                            placeholder="Service Name",
                                            value=ServiceState.name,
                                            on_change=ServiceState.set_name,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.textarea(
                                            placeholder="Description",
                                            value=ServiceState.description,
                                            on_change=ServiceState.set_description,
                                            rows=3,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive textarea size
                                        ),
                                        rx.input(
                                            placeholder="Price ($)",
                                            type="number",
                                            step="0.01",
                                            value=ServiceState.price,
                                            on_change=ServiceState.set_price,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Duration (minutes)",
                                            type="number",
                                            min="5",
                                            step="5",
                                            value=ServiceState.duration,
                                            on_change=ServiceState.set_duration,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Cancel",
                                                on_click=ServiceState.cancel_edit,
                                                variant="outline",
                                                size=["md", "lg", "lg"],  # Responsive button size
                                            ),
                                            rx.button(
                                                rx.condition(
                                                    ServiceState.editing,
                                                    "Update Service",
                                                    "Create Service"
                                                ),
                                                on_click=rx.condition(
                                                    ServiceState.editing,
                                                    ServiceState.update_service,
                                                    ServiceState.create_service
                                                ),
                                                loading=ServiceState.creating,
                                                color_scheme=rx.condition(
                                                    ServiceState.editing,
                                                    "blue",
                                                    "green"
                                                ),
                                                disabled=~ServiceState.form_valid,
                                                size=["md", "lg", "lg"],  # Responsive button size
                                            ),
                                            spacing="3",
                                            width="100%",
                                            justify="end",
                                        ),
                                        rx.alert(
                                            rx.alert_icon(),
                                            rx.alert_title(ServiceState.error_message),
                                            status="error",
                                            is_visible=ServiceState.error_message != "",
                                            mt=3,
                                        ),
                                        rx.alert(
                                            rx.alert_icon(),
                                            rx.alert_title(ServiceState.success_message),
                                            status="success",
                                            is_visible=ServiceState.success_message != "",
                                            mt=3,
                                        ),
                                        width="100%",
                                    ),
                                    on_submit=rx.condition(
                                        ServiceState.editing,
                                        ServiceState.update_service,
                                        ServiceState.create_service
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
                                on_click=ServiceState.cancel_edit,
                                variant="ghost",
                                size="1",
                            ),
                            position="relative",
                            border="1px solid",
                            border_color=rx.cond(
                                ServiceState.editing,
                                "blue.300",
                                "green.300"
                            ),
                            mt=4,
                        ),
                    ),
                    rx.divider(mt=4),
                    rx.cond(
                        ServiceState.loading,
                        rx.center(rx.spinner(), py=8),
                        rx.cond(
                            ServiceState.services.length() > 0,
                            rx.table.responsive(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("Name", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Description", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Price", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Duration", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Actions", size=["sm", "md", "md"]),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        ServiceState.services,
                                        lambda service: rx.table.row(
                                            rx.table.cell(service.get("name", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(service.get("description", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(f"${float(service.get('price', 0)):.2f}", size=["sm", "md", "md"]),
                                            rx.table.cell(f"{service.get('duration', 0)} min", size=["sm", "md", "md"]),
                                            rx.table.cell(
                                                rx.hstack(
                                                    rx.button(
                                                        "Edit",
                                                        on_click=lambda: ServiceState.start_edit(service),
                                                        color_scheme="blue",
                                                        size=["sm", "md", "md"],
                                                    ),
                                                    rx.button(
                                                        rx.cond(
                                                            ServiceState.deleting,
                                                            rx.spinner(size="sm"),
                                                            "Delete"
                                                        ),
                                                        on_click=lambda: ServiceState.delete_service(service.get("id")),
                                                        color_scheme="red",
                                                        size=["sm", "md", "md"],
                                                        disabled=ServiceState.deleting,
                                                    ),
                                                    spacing=["2", "3", "3"],
                                                )
                                            ),
                                        )
                                    )
                                ),
                            ),
                            rx.center(
                                rx.text("No services found.", color="gray", py=[4, 6, 8]),
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
                    # Responsive padding
                    padding_y=["0.5em", "1em", "1.5em"],
                    on_mount=ServiceState.load_services,
                ),
                rx.redirect("/login")
            ),
        )
    )


# Export for import in main.py
services = services_page