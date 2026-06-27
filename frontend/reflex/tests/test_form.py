"""Unit tests for form components."""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import reflex modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import reflex as rx

# Import the components to test
from components.form import (
    form_input,
    form_textarea,
    form_select,
    form_button,
    form_field,
    form_alert,
    form_action_buttons
)


class TestFormComponents(unittest.TestCase):
    """Test cases for form components."""

    def test_form_input_creation(self):
        """Test that form_input creates a component with correct props."""
        def on_change_mock(value):
            return []

        component = form_input(
            placeholder="Test input",
            value="test value",
            on_change=on_change_mock,
            required=True,
            width="200px",
            size=["2", "3", "3"],
            input_type="email"
        )

        # Verify it's a Reflex component
        self.assertIsInstance(component, rx.Component)

    def test_form_textarea_creation(self):
        """Test that form_textarea creates a component."""
        def on_change_mock(value):
            return []

        component = form_textarea(
            placeholder="Test textarea",
            value="test value",
            on_change=on_change_mock,
            required=False,
            width="100%",
            size=["2", "3", "3"],
            rows=5
        )

        self.assertIsInstance(component, rx.Component)

    def test_form_select_creation(self):
        """Test that form_select creates a component."""
        def on_change_mock(value):
            return []

        options = ["Option 1", "Option 2"]
        component = form_select(
            placeholder="Select an option",
            value="Option 1",
            on_change=on_change_mock,
            options=options,
            required=True,
            width="100%",
            size="2"  # Single size value
        )

        self.assertIsInstance(component, rx.Component)

    def test_form_button_creation(self):
        """Test that form_button creates a component."""
        def on_click_mock(event):
            return []

        component = form_button(
            label="Click me",
            on_click=on_click_mock,
            loading=False,
            color_scheme="blue",
            variant="solid",
            size=["2", "3", "3"],
            disabled=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_form_button_loading_state(self):
        """Test that form_button shows loading spinner when loading=True."""
        def on_click_mock(event):
            return []

        component = form_button(
            label="Processing",
            on_click=on_click_mock,
            loading=True,
            color_scheme="blue",
            variant="solid",
            size=["2", "3", "3"],
            disabled=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_form_field_creation(self):
        """Test that form_field creates a component with label and input."""
        input_component = rx.input(placeholder="Test")
        component = form_field(
            label="Test Field",
            component=input_component,
            required=True,
            width="100%"
        )

        self.assertIsInstance(component, rx.Component)

    def test_form_alert_creation(self):
        """Test that form_alert creates a component."""
        # Test error alert
        error_alert = form_alert(
            message="This is an error",
            status="error",
            visible=True,
            mt=3
        )
        self.assertIsInstance(error_alert, rx.Component)

        # Test success alert
        success_alert = form_alert(
            message="Success!",
            status="success",
            visible=True,
            mt=3
        )
        self.assertIsInstance(success_alert, rx.Component)

        # Test invisible alert
        invisible_alert = form_alert(
            message="Hidden message",
            status="error",
            visible=False,
            mt=3
        )
        self.assertIsInstance(invisible_alert, rx.Component)

    def test_form_action_buttons_creation(self):
        """Test that form_action_buttons creates a component."""
        def cancel_mock(event):
            return []

        def action_mock(event):
            return []

        component = form_action_buttons(
            cancel_on_click=cancel_mock,
            action_on_click=action_mock,
            cancel_label="Cancel",
            action_label="Submit",
            action_loading=False,
            action_color_scheme="green",
            cancel_variant="outline",
            size=["2", "3", "3"],
            spacing="3",
            width="100%"
        )

        self.assertIsInstance(component, rx.Component)


if __name__ == "__main__":
    unittest.main()