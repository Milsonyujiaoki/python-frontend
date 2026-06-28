"""
Unit tests for FastUI components.
"""

import pytest
from fastui import components as c
from fastui.components import display


class TestNavigation:
    """Tests for navigation components."""

    def test_main_nav_has_expected_links(self):
        """Test that main navigation has all expected links."""
        from components.navigation import get_main_nav

        nav_links = get_main_nav()
        assert len(nav_links) == 5

        labels = [link.label for link in nav_links]
        assert "Dashboard" in labels
        assert "Customers" in labels
        assert "Barbers" in labels
        assert "Services" in labels
        assert "Appointments" in labels

    def test_create_page_header(self):
        """Test page header creation."""
        from components.navigation import create_page_header

        header = create_page_header("Test Title", "Test Subtitle")
        assert isinstance(header, c.PageHeader)
        assert header.title == "Test Title"
        assert header.subtitle == "Test Subtitle"

    def test_create_navbar(self):
        """Test navbar creation."""
        from components.navigation import create_navbar

        navbar = create_navbar()
        assert isinstance(navbar, c.Navbar)
        assert navbar.brand_text == "BarberShop SaaS"


class TestTables:
    """Tests for table components."""

    def test_create_table(self):
        """Test table creation."""
        from components.tables import create_table

        columns = [display.DisplayLookup(field="id", header="ID")]
        data = [{"id": 1, "name": "Test"}]

        table = create_table(
            title="Test Table",
            columns=columns,
            data=data,
        )

        assert isinstance(table, c.Table)
        assert len(table.columns) == 1

    def test_customer_columns_defined(self):
        """Test that customer columns are properly defined."""
        from components.tables import CUSTOMER_COLUMNS

        assert len(CUSTOMER_COLUMNS) == 5
        fields = [col.field for col in CUSTOMER_COLUMNS]
        assert "id" in fields
        assert "name" in fields
        assert "email" in fields


class TestForms:
    """Tests for form components."""

    def test_create_text_input(self):
        """Test text input creation."""
        from components.forms import create_text_input

        field = create_text_input("name", "Full Name", placeholder="John Doe")

        assert field["name"] == "name"
        assert field["title"] == "Full Name"
        assert field["type"] == "string"
        assert field["placeholder"] == "John Doe"

    def test_create_email_input(self):
        """Test email input creation."""
        from components.forms import create_email_input

        field = create_email_input("email", "Email Address")

        assert field["format"] == "email"
        assert field["type"] == "string"

    def test_create_password_input(self):
        """Test password input creation."""
        from components.forms import create_password_input

        field = create_password_input("password", "Password")

        assert field["format"] == "password"

    def test_create_form_model(self):
        """Test form model creation."""
        from components.forms import create_form_model, create_text_input

        form = create_form_model(
            title="Test Form",
            properties={"name": create_text_input("name", "Name")},
            required=["name"],
            submit_url="/api/submit",
        )

        assert isinstance(form, c.ModelForm)
        assert form.model["title"] == "Test Form"
        assert "name" in form.model["required"]

    def test_predefined_forms_exist(self):
        """Test that predefined forms are available."""
        from components.forms import (
            LOGIN_FORM,
            REGISTER_FORM,
            CUSTOMER_FORM,
            BARBER_FORM,
            SERVICE_FORM,
        )

        assert LOGIN_FORM is not None
        assert REGISTER_FORM is not None
        assert CUSTOMER_FORM is not None
        assert BARBER_FORM is not None
        assert SERVICE_FORM is not None