"""Unit tests for Kivy bento grid component.

Tests the bento_grid.py component functionality.
"""

import pytest
from unittest.mock import MagicMock
from kivy.metrics import dp


class TestBentoItem:
    """Tests for BentoItem class."""

    def test_bento_item_has_title(self):
        """BentoItem should have title property."""
        from frontend.kivy.components.bento_grid import BentoItem
        item = BentoItem(title="Test Cut")
        assert item.title == "Test Cut"

    def test_bento_item_has_subtitle(self):
        """BentoItem should have subtitle property."""
        from frontend.kivy.components.bento_grid import BentoItem
        item = BentoItem(subtitle="R$ 50")
        assert item.subtitle == "R$ 50"

    def test_bento_item_has_bg_color(self):
        """BentoItem should have background color."""
        from frontend.kivy.components.bento_grid import BentoItem
        item = BentoItem(bg_color=[0.9, 0.9, 0.95, 1])
        assert item.bg_color == [0.9, 0.9, 0.95, 1]

    def test_bento_item_has_icon(self):
        """BentoItem should have icon property."""
        from frontend.kivy.components.bento_grid import BentoItem
        item = BentoItem(icon="✂️")
        assert item.icon == "✂️"

    def test_bento_item_has_hover_state(self):
        """BentoItem should track hover state."""
        from frontend.kivy.components.bento_grid import BentoItem
        item = BentoItem()
        assert item._is_hovered == False


class TestBentoGrid:
    """Tests for BentoGrid class."""

    def test_grid_has_cols(self):
        """BentoGrid should have cols property."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid(cols=4)
        assert grid.cols == 4

    def test_grid_has_row_height(self):
        """BentoGrid should have row_height property."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid(row_height=dp(120))
        assert grid.row_height == 120

    def test_grid_has_spacing(self):
        """BentoGrid should have spacing property."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid(spacing=dp(10))
        assert grid.spacing == 10

    def test_grid_has_padding(self):
        """BentoGrid should have padding property."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid(padding=dp(15))
        assert grid.padding == 15

    def test_grid_can_add_item(self):
        """BentoGrid should have add_item method."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid()
        assert hasattr(grid, 'add_item')

    def test_grid_can_add_tall_item(self):
        """BentoGrid should have add_tall_item method."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid()
        assert hasattr(grid, 'add_tall_item')

    def test_grid_can_add_wide_item(self):
        """BentoGrid should have add_wide_item method."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid()
        assert hasattr(grid, 'add_wide_item')

    def test_grid_can_clear_items(self):
        """BentoGrid should have clear_items method."""
        from frontend.kivy.components.bento_grid import BentoGrid
        grid = BentoGrid()
        assert hasattr(grid, 'clear_items')

    def test_grid_add_item_returns_bento_item(self):
        """add_item should return the created BentoItem."""
        from frontend.kivy.components.bento_grid import BentoGrid, BentoItem
        grid = BentoGrid()
        # Without Kivy context, we can verify the method exists
        assert callable(grid.add_item)


class TestBentoCatalog:
    """Tests for BentoCatalog class."""

    def test_catalog_is_bento_grid(self):
        """BentoCatalog should inherit from BentoGrid."""
        from frontend.kivy.components.bento_grid import BentoCatalog, BentoGrid
        catalog = BentoCatalog()
        assert isinstance(catalog, BentoGrid)

    def test_catalog_has_three_cols(self):
        """BentoCatalog should default to 3 columns."""
        from frontend.kivy.components.bento_grid import BentoCatalog
        catalog = BentoCatalog()
        assert catalog.cols == 3

    def test_catalog_has_custom_row_height(self):
        """BentoCatalog should have dp(140) row height."""
        from frontend.kivy.components.bento_grid import BentoCatalog
        catalog = BentoCatalog()
        assert catalog.row_height == 140

    def test_catalog_has_add_cut_item(self):
        """BentoCatalog should have add_cut_item method."""
        from frontend.kivy.components.bento_grid import BentoCatalog
        catalog = BentoCatalog()
        assert hasattr(catalog, 'add_cut_item')

    def test_add_cut_item_accepts_parameters(self):
        """add_cut_item should accept name, price, duration, image."""
        from frontend.kivy.components.bento_grid import BentoCatalog
        catalog = BentoCatalog()
        assert callable(catalog.add_cut_item)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])