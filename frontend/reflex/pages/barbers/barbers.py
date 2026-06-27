import reflex as rx
from state import ReflexAuthState
from components.nav import layout


class BarberState(ReflexAuthState):
    """State for barber management."""

    barbers: list = []
    loading: bool = False
    creating: bool = False
    editing: bool = False
    deleting: bool = False
    editing_barber: dict = {}

    # Form fields for create/edit
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    specialty: str = ""

    @rx.var
    def is_creating(self) -> bool:
        return self.creating

    @rx.var
    def is_editing(self) -> bool:
        return self.editing

    @rx.var
    def form_valid(self) -> bool:
        """Return True if the barber form is valid (basic validation)."""
        return bool(self.first_name and self.last_name and self.email and self.phone and self.specialty)

    def load_barbers(self):
        """Load barbers from the API."""
        self.set_loading(True)
        try:
            response = self.api_service.get("/api/v1/barbers/")
            self.barbers = response if isinstance(response, list) else []
        except Exception as e:
            self.set_error(f"Failed to load barbers: {str(e)}")
        finally:
            self.set_loading(False)

    def create_barber(self):
        """Create a new barber."""
        self.set_creating(True)
        self.clear_error()
        try:
            response = self.api_service.post(
                "/api/v1/barbers/",
                {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "phone": self.phone,
                    "specialty": self.specialty
                }
            )
            if response:
                self.barbers.append(response)
                self.clear_form()
                self.set_success("Barber created successfully!")
        except Exception as e:
            self.set_error(f"Failed to create barber: {str(e)}")
        finally:
            self.set_creating(False)

    def update_barber(self):
        """Update an existing barber."""
        if not self.editing_barber:
            return

        self.set_creating(True)
        self.clear_error()
        try:
            barber_id = self.editing_barber.get("id")
            response = self.api_service.put(
                f"/api/v1/barbers/{barber_id}",
                {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "phone": self.phone,
                    "specialty": self.specialty
                }
            )
            if response:
                # Update the barber in the list
                for i, barber in enumerate(self.barbers):
                    if barber.get("id") == barber_id:
                        self.barbers[i] = response
                        break
                self.cancel_edit()
                self.set_success("Barber updated successfully!")
        except Exception as e:
            self.set_error(f"Failed to update barber: {str(e)}")
        finally:
            self.set_creating(False)

    def delete_barber(self, barber_id: int):
        """Delete a barber."""
        self.set_deleting(True)
        self.clear_error()
        try:
            self.api_service.delete(f"/api/v1/barbers/{barber_id}")
            # Remove from list
            self.barbers = [b for b in self.barbers if b.get("id") != barber_id]
            self.set_success("Barber deleted successfully!")
        except Exception as e:
            self.set_error(f"Failed to delete barber: {str(e)}")
        finally:
            self.set_deleting(False)

    def start_edit(self, barber: dict):
        """Start editing a barber."""
        self.editing = True
        self.editing_barber = barber
        self.first_name = barber.get("first_name", "")
        self.last_name = barber.get("last_name", "")
        self.email = barber.get("email", "")
        self.phone = barber.get("phone", "")
        self.specialty = barber.get("specialty", "")

    def cancel_edit(self):
        """Cancel editing a barber."""
        self.editing = False
        self.editing_barber = {}
        self.clear_form()

    def clear_form(self):
        """Clear the form fields."""
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.specialty = ""

    def clear_messages(self):
        """Clear error and success messages."""
        self.clear_error()
        self.clear_success()

    def set_deleting(self, deleting: bool):
        """Set deleting state."""
        self.deleting = deleting


def barbers_page() -> rx.Component:
    """Barber management page component."""
    return layout(
        rx.container(
            rx.cond(
                ReflexAuthState.is_authenticated,
                rx.vstack(
                    rx.hstack(
                        rx.heading("Barber Management", size=["lg", "xl", "2xl"]),  # Responsive heading size
                        rx.spacer(),
                        rx.button(
                            rx.cond(
                                BarberState.creating | BarberState.editing,
                                rx.spinner(size="sm"),
                                "Add New Barber"
                            ),
                            on_click=lambda: BarberState.cancel_edit(),
                            color_scheme="green",
                            disabled=BarberState.creating | BarberState.editing | ~BarberState.form_valid,
                            size=["md", "lg", "lg"],  # Responsive button size
                        ),
                        width="100%",
                        align="center",
                        # Responsive padding
                        padding_x=["1em", "1.5em", "2em"],
                    ),
                    rx.cond(
                        BarberState.creating | BarberState.editing,
                        rx.card(
                            rx.vstack(
                                rx.heading(
                                    "Edit Barber" if BarberState.editing else "Add New Barber",
                                    size="lg"
                                ),
                                rx.form(
                                    rx.vstack(
                                        padding=["1em", "1.5em", "2em"],  # Responsive form padding
                                        rx.input(
                                            placeholder="First Name",
                                            value=BarberState.first_name,
                                            on_change=BarberState.set_first_name,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Last Name",
                                            value=BarberState.last_name,
                                            on_change=BarberState.set_last_name,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Email",
                                            type="email",
                                            value=BarberState.email,
                                            on_change=BarberState.set_email,
                                            required=True,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Phone",
                                            value=BarberState.phone,
                                            on_change=BarberState.set_phone,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.input(
                                            placeholder="Specialty",
                                            value=BarberState.specialty,
                                            on_change=BarberState.set_specialty,
                                            width="100%",
                                            size=["md", "lg", "lg"],  # Responsive input size
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                "Cancel",
                                                on_click=BarberState.cancel_edit,
                                                variant="outline",
                                                size=["md", "lg", "lg"],  # Responsive button size
                                            ),
                                            rx.button(
                                                rx.condition(
                                                    BarberState.editing,
                                                    "Update Barber",
                                                    "Create Barber"
                                                ),
                                                on_click=rx.condition(
                                                    BarberState.editing,
                                                    BarberState.update_barber,
                                                    BarberState.create_barber
                                                ),
                                                loading=BarberState.creating,
                                                color_scheme=rx.condition(
                                                    BarberState.editing,
                                                    "blue",
                                                    "green"
                                                ),
                                                disabled=~BarberState.form_valid,
                                                size=["md", "lg", "lg"],  # Responsive button size
                                            ),
                                            spacing="3",
                                            width="100%",
                                            justify="end",
                                        ),
                                        rx.alert(
                                            rx.alert_icon(),
                                            rx.alert_title(BarberState.error_message),
                                            status="error",
                                            is_visible=BarberState.error_message != "",
                                            mt=3,
                                        ),
                                        rx.alert(
                                            rx.alert_icon(),
                                            rx.alert_title(BarberState.success_message),
                                            status="success",
                                            is_visible=BarberState.success_message != "",
                                            mt=3,
                                        ),
                                        width="100%",
                                    ),
                                    on_submit=rx.condition(
                                        BarberState.editing,
                                        BarberState.update_barber,
                                        BarberState.create_barber
                                    ),
                                    reset_on_submit=False,
                                    width="100%",
                                ),
                                width="100%",
                                max_width="500px",
                            ),
                            rx.button(
                                "×",
                                position="absolute",
                                top="0",
                                right="0",
                                on_click=BarberState.cancel_edit,
                                variant="ghost",
                                size="1",
                            ),
                            position="relative",
                            border="1px solid",
                            border_color=rx.cond(
                                BarberState.editing,
                                "blue.300",
                                "green.300"
                            ),
                            mt=4,
                        ),
                    ),
                    rx.divider(mt=4),
                    rx.cond(
                        BarberState.loading,
                        rx.center(rx.spinner(), py=8),
                        rx.cond(
                            BarberState.barbers.length() > 0,
                            rx.table.responsive(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("First Name", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Last Name", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Email", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Phone", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Specialty", size=["sm", "md", "md"]),
                                        rx.table.column_header_cell("Actions", size=["sm", "md", "md"]),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        BarberState.barbers,
                                        lambda barber: rx.table.row(
                                            rx.table.cell(barber.get("first_name", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(barber.get("last_name", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(barber.get("email", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(barber.get("phone", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(barber.get("specialty", ""), size=["sm", "md", "md"]),
                                            rx.table.cell(
                                                rx.hstack(
                                                    rx.button(
                                                        "Edit",
                                                        on_click=lambda: BarberState.start_edit(barber),
                                                        color_scheme="blue",
                                                        size=["sm", "md", "md"],
                                                    ),
                                                    rx.button(
                                                        rx.cond(
                                                            BarberState.deleting,
                                                            rx.spinner(size="sm"),
                                                            "Delete"
                                                        ),
                                                        on_click=lambda: BarberState.delete_barber(barber.get("id")),
                                                        color_scheme="red",
                                                        size=["sm", "md", "md"],
                                                        disabled=BarberState.deleting,
                                                    ),
                                                    spacing=["2", "3", "3"],
                                                )
                                            ),
                                        )
                                    )
                                ),
                            ),
                            rx.center(
                                rx.text("No barbers found.", color="gray", py=[4, 6, 8]),
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
                    on_mount=BarberState.load_barbers,
                ),
                rx.redirect("/login")
            ),
        )
    )


# Export for import in main.py
barbers = barbers_page