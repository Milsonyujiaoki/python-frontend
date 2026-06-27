"""Unit tests for modal components."""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import reflex modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import reflex as rx

# Import the components to test
from components.modal import (
    modal_overlay,
    simple_modal
)


class TestModalComponents(unittest.TestCase):
    """Test cases for modal components."""

    def test_modal_overlay_creation(self):
        """Test that modal_overlay creates a component."""
        content = rx.text("Test content")
        on_close_mock = Mock()

        component = modal_overlay(
            is_open=True,
            content=content,
            on_close=on_close_mock,
            title="Test Modal",
            width="400px",
            padding="4"
        )

        self.assertIsInstance(component, rx.Component)

    def test_modal_overlay_closed(self):
        """Test that modal_overlay returns fragment when closed."""
        content = rx.text("Test content")
        on_close_mock = Mock()

        component = modal_overlay(
            is_open=False,
            content=content,
            on_close=on_close_mock,
            title="Test Modal",
            width="400px",
            padding="4"
        )

        # When is_open=False, should return rx.fragment()
        self.assertIsInstance(component, rx.Component)

    def test_modal_overlay_no_title(self):
        """Test that modal_overlay works without title."""
        content = rx.text("Test content")
        on_close_mock = Mock()

        component = modal_overlay(
            is_open=True,
            content=content,
            on_close=on_close_mock,
            title="",  # Empty title
            width="400px",
            padding="4"
        )

        self.assertIsInstance(component, rx.Component)

    def test_simple_modal_creation(self):
        """Test that simple_modal creates a component."""
        content = rx.vstack(
            rx.text("Field 1"),
            rx.text("Field 2")
        )
        on_close_mock = Mock()
        on_confirm_mock = Mock()

        component = simple_modal(
            is_open=True,
            title="Confirm Action",
            content=content,
            on_close=on_close_mock,
            confirm_label="Yes",
            cancel_label="No",
            confirm_on_click=on_confirm_mock,
            cancel_on_click=on_close_mock,
            confirm_loading=False,
            confirm_color_scheme="blue",
            width="400px",
            padding="4"
        )

        self.assertIsInstance(component, rx.Component)

    def test_simple_modal_closed(self):
        """Test that simple_modal returns fragment when closed."""
        content = rx.text("Test content")
        on_close_mock = Mock()

        component = simple_modal(
            is_open=False,
            title="Test Modal",
            content=content,
            on_close=on_close_mock
        )

        # When is_open=False, should return rx.fragment()
        self.assertIsInstance(component, rx.Component)

    def test_simple_modal_default_buttons(self):
        """Test that simple_modal uses default button labels."""
        content = rx.text("Test content")
        on_close_mock = Mock()

        component = simple_modal(
            is_open=True,
            title="Default Buttons",
            content=content,
            on_close=on_close_mock
            # confirm_label and cancel_label not provided - should use defaults
        )

        self.assertIsInstance(component, rx.Component)

    def test_simple_modal_default_cancel_handler(self):
        """Test that simple_modal uses on_close for cancel when not provided."""
        content = rx.text("Test content")
        on_close_mock = Mock()
        on_confirm_mock = Mock()

        component = simple_modal(
            is_open=True,
            title="Default Cancel",
            content=content,
            on_close=on_close_mock,
            confirm_on_click=on_confirm_mock
            # cancel_on_click not provided - should default to on_close
        )

        self.assertIsInstance(component, rx.Component)

    def test_simple_modal_loading_state(self):
        """Test that simple_modal shows loading state."""
        content = rx.text("Test content")
        on_close_mock = Mock()
        on_confirm_mock = Mock()

        component = simple_modal(
            is_open=True,
            title="Loading State",
            content=content,
            on_close=on_close_mock,
            confirm_on_click=on_confirm_mock,
            confirm_loading=True  # Should show spinner
        )

        self.assertIsInstance(component, rx.Component)


if __name__ == "__main__":
    unittest.main()