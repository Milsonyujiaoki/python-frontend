"""
Reflex-specific authentication state management.
"""
import reflex as rx
import sys
import os
from typing import Optional, Dict, Any
import requests

# Add the frontend directory to the path so we can import shared modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.auth_state import AuthStateManager
from shared.base_service import BaseApiService


class ReflexAuthState(AuthStateManager, rx.State):
    """Reflex implementation of authentication state management."""

    # Auth state variables
    is_authenticated: bool = False
    auth_token: str = ""
    current_user: dict = {}
    loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # Form state
    login_email: str = ""
    login_password: str = ""
    register_email: str = ""
    register_password: str = ""
    register_full_name: str = ""
    reset_email: str = ""

    def __init__(self):
        super().__init__()
        # Initialize the API service with the backend URL
        self.api_service = ReflexApiService("http://localhost:8000")

    @rx.var
    def is_loading(self) -> bool:
        """Return loading state."""
        return self.loading

    @rx.var
    def login_form_valid(self) -> bool:
        """Return True if login form is valid (basic validation)."""
        return bool(self.login_email and self.login_password)

    @rx.var
    def register_form_valid(self) -> bool:
        """Return True if registration form is valid (basic validation)."""
        return bool(self.register_full_name and self.register_email and self.register_password)

    @rx.var
    def forgot_password_form_valid(self) -> bool:
        """Return True if forgot password form is valid (basic validation)."""
        return bool(self.reset_email)

    @rx.var
    def get_error(self) -> str:
        """Get error message."""
        return self.error_message

    @rx.var
    def get_success(self) -> str:
        """Get success message."""
        return self.success_message

    def set_loading(self, loading: bool):
        """Set loading state."""
        self.loading = loading

    def set_error(self, message: str):
        """Set error message."""
        self.error_message = message

    def clear_error(self):
        """Clear error message."""
        self.error_message = ""

    def set_success(self, message: str):
        """Set success message."""
        self.success_message = message

    def clear_success(self):
        """Clear success message."""
        self.success_message = ""

    # Form field setters
    def set_login_email(self, email: str):
        """Set login email."""
        self.login_email = email

    def set_login_password(self, password: str):
        """Set login password."""
        self.login_password = password

    def set_register_email(self, email: str):
        """Set register email."""
        self.register_email = email

    def set_register_password(self, password: str):
        """Set register password."""
        self.register_password = password

    def set_register_full_name(self, full_name: str):
        """Set register full name."""
        self.register_full_name = full_name

    def set_reset_email(self, email: str):
        """Set reset email."""
        self.reset_email = email

    async def login(self, email: str, password: str):
        """Log in a user."""
        self.set_loading(True)
        self.clear_error()

        try:
            # Call the backend API
            response = self.api_service.post(
                "/api/v1/auth/login",
                {"email": email, "password": password}
            )

            if response and "access_token" in response:
                self.auth_token = response["access_token"]
                self.current_user = response.get("user", {})
                self.is_authenticated = True
                self.api_service.update_auth_token(self.auth_token)
                self.set_loading(False)
                return [rx.redirect("/")]
            else:
                self.set_error("Invalid email or password")
                self.set_loading(False)
                return []
        except Exception as e:
            self.set_error(f"Login failed: {str(e)}")
            self.set_loading(False)
            return []

    def logout(self) -> None:
        """Log out the current user."""
        self.auth_token = ""
        self.current_user = {}
        self.is_authenticated = False
        self.api_service.update_auth_token("")
        self.clear_error()

    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        return self.is_authenticated

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get the currently authenticated user."""
        return self.current_user if self.is_authenticated else None

    def set_auth_token(self, token: str) -> None:
        """Set the authentication token."""
        self.auth_token = token

    def get_auth_token(self) -> Optional[str]:
        """Get the authentication token."""
        return self.auth_token if self.auth_token else None

    def register(self, email: str, password: str, full_name: str) -> bool:
        """Register a new user."""
        self.set_loading(True)
        self.clear_error()

        try:
            response = self.api_service.post(
                "/api/v1/auth/register",
                {
                    "email": email,
                    "password": password,
                    "full_name": full_name
                }
            )

            if response and "access_token" in response:
                self.auth_token = response["access_token"]
                self.current_user = response.get("user", {})
                self.is_authenticated = True
                self.api_service.update_auth_token(self.auth_token)
                self.set_loading(False)
                return True
            else:
                self.set_error("Registration failed")
                self.set_loading(False)
                return False
        except Exception as e:
            self.set_error(f"Registration failed: {str(e)}")
            self.set_loading(False)
            return False

    def forgot_password(self, email: str) -> bool:
        """Request a password reset."""
        self.set_loading(True)
        self.clear_error()
        self.clear_success()

        try:
            response = self.api_service.post(
                "/api/v1/auth/forgot-password",
                {"email": email}
            )

            if response and "message" in response:
                self.set_success(response["message"])
                self.set_loading(False)
                return True
            else:
                self.set_error("Failed to send reset email")
                self.set_loading(False)
                return False
        except Exception as e:
            self.set_error(f"Password reset request failed: {str(e)}")
            self.set_loading(False)
            return False


class ReflexApiService(BaseApiService):
    """Reflex implementation of API service."""

    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.session = requests.Session()
        self.auth_token = ""

    def update_auth_token(self, token: str):
        """Update the authentication token."""
        self.auth_token = token

    def get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request."""
        url = self._build_url(endpoint)
        headers = {}

        # Add auth token if available
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        response = self.session.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict) -> dict:
        """Make a POST request."""
        url = self._build_url(endpoint)
        headers = {"Content-Type": "application/json"}

        # Add auth token if available
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        response = self.session.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict) -> dict:
        """Make a PUT request."""
        url = self._build_url(endpoint)
        headers = {"Content-Type": "application/json"}

        # Add auth token if available
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        response = self.session.put(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> dict:
        """Make a DELETE request."""
        url = self._build_url(endpoint)
        headers = {}

        # Add auth token if available
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        response = self.session.delete(url, headers=headers)
        response.raise_for_status()
        return response.json() if response.content else {}