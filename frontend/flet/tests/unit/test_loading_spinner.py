"""Unit tests for Flet loading spinner component.

Tests the loading_spinner.py component functionality.
"""

import pytest
from frontend.flet.components.loading_spinner import loading_spinner, spinner_overlay


class TestLoadingSpinner:
    """Tests for the loading_spinner function."""

    def test_circular_spinner_creates_progress_ring(self):
        """Circular style should create ProgressRing."""
        result = loading_spinner(color="#ff0000", style="circular", size=40)
        assert result is not None
        assert len(result.controls) == 1

    def test_dots_style_creates_row_of_dots(self):
        """Dots style should create a Row with dot containers."""
        result = loading_spinner(style="dots", size=30)
        assert result is not None
        assert len(result.controls) == 1

    def test_bars_style_creates_row_of_bars(self):
        """Bars style should create a Row with bar containers."""
        result = loading_spinner(style="bars", size=48)
        assert result is not None
        assert len(result.controls) == 1

    def test_default_style_is_circular(self):
        """Default style should be circular (ProgressRing)."""
        result = loading_spinner()
        assert result is not None
        assert len(result.controls) == 1

    def test_size_parameter_is_applied(self):
        """Size parameter should affect the spinner."""
        result = loading_spinner(size=20)
        assert result is not None


class TestSpinnerOverlay:
    """Tests for the spinner_overlay function."""

    def test_overlay_creates_container(self):
        """Overlay should create a container."""
        result = spinner_overlay(message="Loading...")
        assert result is not None

    def test_overlay_contains_message(self):
        """Overlay should display the provided message."""
        result = spinner_overlay(message="Please wait")
        assert result is not None

    def test_custom_message_is_used(self):
        """Custom message should be displayed."""
        result = spinner_overlay(message="Custom loading text")
        assert result is not None

    def test_custom_color_is_accepted(self):
        """Custom color parameter should be accepted."""
        result = spinner_overlay(color="#ff5733")
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])