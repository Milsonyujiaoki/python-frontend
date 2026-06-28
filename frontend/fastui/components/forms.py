"""
Form components for FastUI frontend.

Provides reusable form components with validation and error handling.
"""

from fastui import components as c
from typing import Dict, Any, Optional, List


def create_text_input(
    name: str,
    label: str,
    placeholder: Optional[str] = None,
    required: bool = False,
    help_text: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a text input field definition."""
    field = {
        "name": name,
        "title": label,
        "type": "string",
    }
    if placeholder:
        field["placeholder"] = placeholder
    if help_text:
        field["description"] = help_text
    return field


def create_email_input(
    name: str,
    label: str,
    placeholder: Optional[str] = None,
    required: bool = True,
) -> Dict[str, Any]:
    """Create an email input field definition."""
    return {
        "name": name,
        "title": label,
        "type": "string",
        "format": "email",
        "placeholder": placeholder or "email@example.com",
    }


def create_password_input(
    name: str,
    label: str,
    placeholder: Optional[str] = None,
    required: bool = True,
) -> Dict[str, Any]:
    """Create a password input field definition."""
    return {
        "name": name,
        "title": label,
        "type": "string",
        "format": "password",
        "placeholder": placeholder or "••••••••",
    }


def create_number_input(
    name: str,
    label: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    step: Optional[float] = None,
) -> Dict[str, Any]:
    """Create a number input field definition."""
    field = {
        "name": name,
        "title": label,
        "type": "number",
    }
    if min_value is not None:
        field["minimum"] = min_value
    if max_value is not None:
        field["maximum"] = max_value
    if step is not None:
        field["step"] = step
    return field


def create_select_input(
    name: str,
    label: str,
    options: List[Dict[str, str]],
    multiple: bool = False,
) -> Dict[str, Any]:
    """Create a select dropdown field definition."""
    return {
        "name": name,
        "title": label,
        "type": "string",
        "enum": options,
        "multiple": multiple,
    }


def create_form_model(
    title: str,
    properties: Dict[str, Any],
    required: Optional[List[str]] = None,
    submit_url: str = "/api/submit",
    submit_method: str = "POST",
    display_mode: str = "inline",
) -> c.ModelForm:
    """
    Create a form model component.

    Args:
        title: Form title
        properties: Field definitions
        required: List of required field names
        submit_url: URL for form submission
        submit_method: HTTP method for submission
        display_mode: Display mode (inline, pages, etc.)
    """
    schema = {
        "title": title,
        "type": "object",
        "properties": properties,
    }
    if required:
        schema["required"] = required

    return c.ModelForm(
        model=schema,
        submit_url=submit_url,
        submit_method=submit_method,
        display_mode=display_mode,
    )


# Predefined form schemas
LOGIN_FORM = create_form_model(
    title="Login",
    properties={
        "email": create_email_input("email", "Email"),
        "password": create_password_input("password", "Password"),
    },
    required=["email", "password"],
    submit_url="/api/login/submit",
)

REGISTER_FORM = create_form_model(
    title="Register",
    properties={
        "first_name": create_text_input("first_name", "First Name", required=True),
        "last_name": create_text_input("last_name", "Last Name", required=True),
        "email": create_email_input("email", "Email"),
        "password": create_password_input("password", "Password"),
        "confirm_password": create_password_input("confirm_password", "Confirm Password"),
    },
    required=["first_name", "last_name", "email", "password"],
    submit_url="/api/register/submit",
)

CUSTOMER_FORM = create_form_model(
    title="Customer",
    properties={
        "name": create_text_input("name", "Full Name", placeholder="John Doe"),
        "email": create_email_input("email", "Email"),
        "phone": create_text_input("phone", "Phone", placeholder="(555) 123-4567"),
        "notes": create_text_input("notes", "Notes", placeholder="Additional notes..."),
    },
    required=["name", "email"],
    submit_url="/api/customers/submit",
)

BARBER_FORM = create_form_model(
    title="Barber",
    properties={
        "first_name": create_text_input("first_name", "First Name"),
        "last_name": create_text_input("last_name", "Last Name"),
        "email": create_email_input("email", "Email"),
        "phone": create_text_input("phone", "Phone"),
        "specialty": create_text_input("specialty", "Specialty", placeholder="e.g., Classic Cuts"),
    },
    required=["first_name", "last_name", "email"],
    submit_url="/api/barbers/submit",
)

SERVICE_FORM = create_form_model(
    title="Service",
    properties={
        "name": create_text_input("name", "Service Name"),
        "description": create_text_input("description", "Description"),
        "duration": create_number_input("duration", "Duration (minutes)", min_value=5, step=5),
        "price": create_number_input("price", "Price ($)", min_value=0, step=0.01),
    },
    required=["name", "duration", "price"],
    submit_url="/api/services/submit",
)