"""Base form component for Streamlit application."""

import streamlit as st
from typing import Dict, Any, Optional, List, Callable


def render_form(
    form_key: str,
    fields: List[Dict[str, Any]],
    submit_label: str = "Save",
    on_submit: Optional[Callable[[Dict[str, Any]], bool]] = None,
    initial_data: Optional[Dict[str, Any]] = None,
    cancel_url: Optional[str] = None,
) -> None:
    """
    Render a generic form with configurable fields.

    Args:
        form_key: Unique key for the form
        fields: List of field configurations
        submit_label: Label for the submit button
        on_submit: Optional callback function for form submission
        initial_data: Optional initial data to pre-fill fields
        cancel_url: Optional URL to navigate to on cancel
    """
    with st.form(form_key):
        values = {}

        for field in fields:
            field_type = field.get("type", "text")
            field_key = field.get("key")
            field_label = field.get("label", field_key)
            field_options = field.get("options", [])
            field_min = field.get("min_value", 0)
            field_max = field.get("max_value", 100)
            field_step = field.get("step", 1)
            field_placeholder = field.get("placeholder", "")
            field_help = field.get("help", "")
            field_required = field.get("required", False)
            field_height = field.get("height", 100)

            initial_value = (
                initial_data.get(field_key) if initial_data else None
            )

            if field_type == "text":
                values[field_key] = st.text_input(
                    field_label,
                    value=initial_value,
                    placeholder=field_placeholder,
                    help=field_help,
                    required=field_required,
                )
            elif field_type == "email":
                values[field_key] = st.text_input(
                    field_label,
                    value=initial_value,
                    placeholder=field_placeholder,
                    help=field_help,
                    required=field_required,
                )
            elif field_type == "password":
                values[field_key] = st.text_input(
                    field_label,
                    type="password",
                    value=initial_value,
                    placeholder=field_placeholder,
                    help=field_help,
                    required=field_required,
                )
            elif field_type == "number":
                values[field_key] = st.number_input(
                    field_label,
                    value=initial_value,
                    min_value=field_min,
                    max_value=field_max,
                    step=field_step,
                    help=field_help,
                    required=field_required,
                )
            elif field_type == "select":
                values[field_key] = st.selectbox(
                    field_label,
                    options=field_options,
                    index=field_options.index(initial_value)
                    if initial_value and initial_value in field_options
                    else 0,
                    help=field_help,
                )
            elif field_type == "multiselect":
                values[field_key] = st.multiselect(
                    field_label,
                    options=field_options,
                    default=initial_value if initial_value else [],
                    help=field_help,
                )
            elif field_type == "textarea":
                values[field_key] = st.text_area(
                    field_label,
                    value=initial_value,
                    height=field_height,
                    placeholder=field_placeholder,
                    help=field_help,
                    required=field_required,
                )
            elif field_type == "checkbox":
                values[field_key] = st.checkbox(
                    field_label,
                    value=initial_value if initial_value else False,
                    help=field_help,
                )
            elif field_type == "date":
                values[field_key] = st.date_input(
                    field_label,
                    value=initial_value,
                    help=field_help,
                    required=field_required,
                )
            elif field_type == "time":
                values[field_key] = st.time_input(
                    field_label,
                    value=initial_value,
                    help=field_help,
                    required=field_required,
                )

        # Submit and cancel buttons
        col_submit, col_cancel = st.columns(2)

        with col_submit:
            submitted = st.form_submit_button(submit_label, use_container_width=True)

            if submitted:
                if on_submit:
                    success = on_submit(values)
                    if success:
                        st.success("Saved successfully!")
                    else:
                        st.error("Failed to save")

        with col_cancel:
            if st.button("Cancel", use_container_width=True):
                if cancel_url:
                    st.switch_page(cancel_url)
                else:
                    st.session_state[f"show_{form_key}"] = False
                    st.rerun()


def render_customer_form(
    initial_data: Optional[Dict[str, Any]] = None,
    on_submit: Optional[Callable] = None,
) -> None:
    """Render a customer form with predefined fields."""
    fields = [
        {"type": "text", "key": "name", "label": "Name", "required": True},
        {"type": "email", "key": "email", "label": "Email", "required": True},
        {"type": "text", "key": "phone", "label": "Phone"},
        {
            "type": "select",
            "key": "status",
            "label": "Status",
            "options": ["Active", "Inactive", "VIP"],
        },
    ]

    render_form(
        form_key="customer_form",
        fields=fields,
        submit_label="Save Customer",
        on_submit=on_submit,
        initial_data=initial_data,
    )


def render_barber_form(
    initial_data: Optional[Dict[str, Any]] = None,
    on_submit: Optional[Callable] = None,
) -> None:
    """Render a barber form with predefined fields."""
    fields = [
        {"type": "text", "key": "name", "label": "Name", "required": True},
        {"type": "email", "key": "email", "label": "Email", "required": True},
        {"type": "text", "key": "phone", "label": "Phone"},
        {"type": "textarea", "key": "specialty", "label": "Specialty", "height": 60},
        {
            "type": "select",
            "key": "status",
            "label": "Status",
            "options": ["Active", "Inactive", "On Leave"],
        },
        {
            "type": "number",
            "key": "rating",
            "label": "Rating",
            "min_value": 0.0,
            "max_value": 5.0,
            "step": 0.1,
        },
    ]

    render_form(
        form_key="barber_form",
        fields=fields,
        submit_label="Save Barber",
        on_submit=on_submit,
        initial_data=initial_data,
    )


def render_service_form(
    initial_data: Optional[Dict[str, Any]] = None,
    on_submit: Optional[Callable] = None,
) -> None:
    """Render a service form with predefined fields."""
    fields = [
        {"type": "text", "key": "name", "label": "Service Name", "required": True},
        {"type": "textarea", "key": "description", "label": "Description", "height": 60},
        {
            "type": "select",
            "key": "category",
            "label": "Category",
            "options": ["Hair", "Beard", "Coloring", "Treatment", "Other"],
        },
        {
            "type": "number",
            "key": "price",
            "label": "Price ($)",
            "min_value": 0.0,
            "max_value": 500.0,
            "step": 5.0,
        },
        {
            "type": "number",
            "key": "duration",
            "label": "Duration (min)",
            "min_value": 5,
            "max_value": 180,
            "step": 5,
        },
        {"type": "checkbox", "key": "active", "label": "Active", "default": True},
    ]

    render_form(
        form_key="service_form",
        fields=fields,
        submit_label="Save Service",
        on_submit=on_submit,
        initial_data=initial_data,
    )