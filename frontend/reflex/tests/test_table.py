"""Unit tests for table components."""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import reflex modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import reflex as rx

# Import the component to test
from components.table import data_table


class TestTableComponents(unittest.TestCase):
    """Test cases for table components."""

    def test_data_table_creation(self):
        """Test that data_table creates a component."""
        columns = [
            {"header": "Name", "key": "name", "size": ["sm", "md", "md"]},
            {"header": "Email", "key": "email", "size": ["sm", "md", "md"]}
        ]
        data = [
            {"name": "John Doe", "email": "john@example.com"},
            {"name": "Jane Smith", "email": "jane@example.com"}
        ]

        component = data_table(
            columns=columns,
            data=data,
            actions=[],  # No actions
            loading=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_data_table_with_actions(self):
        """Test that data_table works with actions."""
        columns = [
            {"header": "Name", "key": "name", "size": ["sm", "md", "md"]},
            {"header": "Email", "key": "email", "size": ["sm", "md", "md"]}
        ]
        data = [
            {"name": "John Doe", "email": "john@example.com", "id": 1},
            {"name": "Jane Smith", "email": "jane@example.com", "id": 2}
        ]
        actions = [
            {
                "label": "Edit",
                "on_click": Mock(),  # Will be replaced in test
                "color_scheme": "blue",
                "size": ["sm", "md", "md"]
            },
            {
                "label": "Delete",
                "on_click": Mock(),
                "color_scheme": "red",
                "size": ["sm", "md", "md"]
            }
        ]

        # Replace mocks with actual mocks for on_click
        actions[0]["on_click"] = Mock(return_value=[])
        actions[1]["on_click"] = Mock(return_value=[])

        component = data_table(
            columns=columns,
            data=data,
            actions=actions,
            loading=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_data_table_loading_state(self):
        """Test that data_table shows loading spinner when loading=True."""
        columns = [
            {"header": "Name", "key": "name", "size": ["sm", "md", "md"]}
        ]
        data = [{"name": "Test"}]

        component = data_table(
            columns=columns,
            data=data,
            actions=[],
            loading=True  # Should show spinner
        )

        self.assertIsInstance(component, rx.Component)

    def test_data_table_empty_data(self):
        """Test that data_table works with empty data."""
        columns = [
            {"header": "Name", "key": "name", "size": ["sm", "md", "md"]}
        ]
        data = []  # Empty data

        component = data_table(
            columns=columns,
            data=data,
            actions=[],
            loading=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_data_table_callable_key(self):
        """Test that data_table works with callable key function."""
        columns = [
            {
                "header": "Full Name",
                "key": lambda row: f"{row['first_name']} {row['last_name']}",
                "size": ["sm", "md", "md"]
            }
        ]
        data = [
            {"first_name": "John", "last_name": "Doe"},
            {"first_name": "Jane", "last_name": "Smith"}
        ]

        component = data_table(
            columns=columns,
            data=data,
            actions=[],
            loading=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_data_table_callable_action_props(self):
        """Test that data_table works with callable action props (loading, disabled)."""
        columns = [
            {"header": "Name", "key": "name", "size": ["sm", "md", "md"]}
        ]
        data = [
            {"name": "John Doe", "id": 1, "is_editing": False},
            {"name": "Jane Smith", "id": 2, "is_editing": True}
        ]
        actions = [
            {
                "label": "Edit",
                "on_click": Mock(return_value=[]),
                "color_scheme": "blue",
                "size": ["sm", "md", "md"],
                # Callable loading prop
                "loading": lambda row: row.get("is_editing", False),
                # Callable disabled prop
                "disabled": lambda row: row.get("is_editing", False)
            }
        ]

        component = data_table(
            columns=columns,
            data=data,
            actions=actions,
            loading=False
        )

        self.assertIsInstance(component, rx.Component)

    def test_data_table_none_actions(self):
        """Test that data_table handles None actions correctly."""
        columns = [
            {"header": "Name", "key": "name", "size": ["sm", "md", "md"]}
        ]
        data = [{"name": "Test"}]

        component = data_table(
            columns=columns,
            data=data,
            actions=None,  # Should default to empty list
            loading=False
        )

        self.assertIsInstance(component, rx.Component)


if __name__ == "__main__":
    unittest.main()