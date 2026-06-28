"""Unit tests for Flet shake animation component.

Tests the shake_animation.py component functionality.
"""

import pytest
from unittest.mock import MagicMock
import flet as ft
from frontend.flet.components.shake_animation import (
    shake_container,
    shake_on_error,
    ValidationErrorShake,
)


class TestShakeContainer:
    """Tests for the shake_container function."""

    def test_shake_container_wraps_content(self):
        """Shake container should wrap the provided content."""
        content = ft.Text("Hello")
        result = shake_container(content)
        assert result is not None

    def test_shake_container_has_border_radius(self):
        """Shake container should have border radius."""
        content = ft.Text("Hello")
        result = shake_container(content, border_radius=8)
        assert result.border_radius == 8

    def test_shake_container_has_shake_method(self):
        """Shake container should have a shake method."""
        content = ft.Text("Hello")
        result = shake_container(content)
        assert hasattr(result, 'shake')
        assert callable(result.shake)


class TestShakeOnError:
    """Tests for the shake_on_error function."""

    def test_shake_on_error_returns_textfield(self):
        """Should return a TextField."""
        tf = ft.TextField(label="Test")
        result = shake_on_error(tf)
        assert isinstance(result, ft.TextField)

    def test_shake_on_error_sets_error_text(self):
        """Should set error_text on the field."""
        tf = ft.TextField(label="Test")
        result = shake_on_error(tf, error_text="Invalid input")
        assert result.error_text == "Invalid input"

    def test_shake_on_error_adds_set_error_method(self):
        """Should add a set_error method to the field."""
        tf = ft.TextField(label="Test")
        result = shake_on_error(tf)
        assert hasattr(result, 'set_error')
        assert callable(result.set_error)


class TestValidationErrorShake:
    """Tests for the ValidationErrorShake utility class."""

    def test_validator_initializes(self):
        """Validator should initialize."""
        mock_page = MagicMock()
        validator = ValidationErrorShake(mock_page)
        assert validator.page == mock_page

    def test_validator_has_default_settings(self):
        """Validator should have default color and duration."""
        mock_page = MagicMock()
        validator = ValidationErrorShake(mock_page)
        assert validator.default_color == "#ef4444"
        assert validator.default_duration == 0.4

    def test_register_adds_container(self):
        """Should register containers for shake animations."""
        mock_page = MagicMock()
        validator = ValidationErrorShake(mock_page)
        container = ft.Container()
        validator.register(container)
        assert container in validator.shakeables

    def test_trigger_method_exists(self):
        """Validator should have trigger method."""
        mock_page = MagicMock()
        validator = ValidationErrorShake(mock_page)
        assert hasattr(validator, 'trigger')
        assert callable(validator.trigger)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])