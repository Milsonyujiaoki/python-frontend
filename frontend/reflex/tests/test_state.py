"""Unit tests for state management."""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import reflex modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import reflex as rx

# Import the state to test
from state import ReflexAuthState


class TestReflexAuthState(unittest.TestCase):
    """Test cases for ReflexAuthState."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a fresh state instance for each test
        self.state = ReflexAuthState()

    def test_initialization(self):
        """Test that state initializes with correct default values."""
        self.assertFalse(self.state.is_authenticated)
        self.assertEqual(self.state.auth_token, "")
        self.assertEqual(self.state.current_user, {})
        self.assertFalse(self.state.loading)
        self.assertEqual(self.state.error_message, "")
        self.assertEqual(self.state.success_message, "")

        # Form fields should be empty
        self.assertEqual(self.state.login_email, "")
        self.assertEqual(self.state.login_password, "")
        self.assertEqual(self.state.register_email, "")
        self.assertEqual(self.state.register_password, "")
        self.assertEqual(self.state.register_full_name, "")
        self.assertEqual(self.state.reset_email, "")

    def test_is_loading_var(self):
        """Test the is_loading computed variable."""
        self.state.loading = False
        self.assertFalse(self.state.is_loading)

        self.state.loading = True
        self.assertTrue(self.state.is_loading)

    def test_login_form_valid(self):
        """Test login form validation."""
        # Both empty - should be invalid
        self.state.login_email = ""
        self.state.login_password = ""
        self.assertFalse(self.state.login_form_valid)

        # Email only - should be invalid
        self.state.login_email = "test@example.com"
        self.state.login_password = ""
        self.assertFalse(self.state.login_form_valid)

        # Password only - should be invalid
        self.state.login_email = ""
        self.state.login_password = "password123"
        self.assertFalse(self.state.login_form_valid)

        # Both filled - should be valid
        self.state.login_email = "test@example.com"
        self.state.login_password = "password123"
        self.assertTrue(self.state.login_form_valid)

    def test_register_form_valid(self):
        """Test registration form validation."""
        # All empty - should be invalid
        self.state.register_email = ""
        self.state.register_password = ""
        self.state.register_full_name = ""
        self.assertFalse(self.state.register_form_valid)

        # Only name - should be invalid
        self.state.register_full_name = "John Doe"
        self.state.register_email = ""
        self.state.register_password = ""
        self.assertFalse(self.state.register_form_valid)

        # Only email - should be invalid
        self.state.register_full_name = ""
        self.state.register_email = "john@example.com"
        self.state.register_password = ""
        self.assertFalse(self.state.register_form_valid)

        # Only password - should be invalid
        self.state.register_full_name = ""
        self.state.register_email = ""
        self.state.register_password = "password123"
        self.assertFalse(self.state.register_form_valid)

        # Name and email - should be invalid
        self.state.register_full_name = "John Doe"
        self.state.register_email = "john@example.com"
        self.state.register_password = ""
        self.assertFalse(self.state.register_form_valid)

        # All filled - should be valid
        self.state.register_full_name = "John Doe"
        self.state.register_email = "john@example.com"
        self.state.register_password = "password123"
        self.assertTrue(self.state.register_form_valid)

    def test_forgot_password_form_valid(self):
        """Test forgot password form validation."""
        # Empty - should be invalid
        self.state.reset_email = ""
        self.assertFalse(self.state.forgot_password_form_valid)

        # Filled - should be valid
        self.state.reset_email = "test@example.com"
        self.assertTrue(self.state.forgot_password_form_valid)

    def test_set_loading(self):
        """Test set_loading method."""
        self.assertFalse(self.state.loading)
        self.state.set_loading(True)
        self.assertTrue(self.state.loading)
        self.state.set_loading(False)
        self.assertFalse(self.state.loading)

    def test_set_error(self):
        """Test set_error method."""
        self.assertEqual(self.state.error_message, "")
        self.state.set_error("Test error")
        self.assertEqual(self.state.error_message, "Test error")

    def test_clear_error(self):
        """Test clear_error method."""
        self.state.error_message = "Test error"
        self.assertEqual(self.state.error_message, "Test error")
        self.state.clear_error()
        self.assertEqual(self.state.error_message, "")

    def test_set_success(self):
        """Test set_success method."""
        self.assertEqual(self.state.success_message, "")
        self.state.set_success("Test success")
        self.assertEqual(self.state.success_message, "Test success")

    def test_clear_success(self):
        """Test clear_success method."""
        self.state.success_message = "Test success"
        self.assertEqual(self.state.success_message, "Test success")
        self.state.clear_success()
        self.assertEqual(self.state.success_message, "")

    def test_form_field_setters(self):
        """Test that form field setters work correctly."""
        # Test login email setter
        self.state.set_login_email("test@example.com")
        self.assertEqual(self.state.login_email, "test@example.com")

        # Test login password setter
        self.state.set_login_password("password123")
        self.assertEqual(self.state.login_password, "password123")

        # Test register email setter
        self.state.set_register_email("register@example.com")
        self.assertEqual(self.state.register_email, "register@example.com")

        # Test register password setter
        self.state.set_register_password("regpass123")
        self.assertEqual(self.state.register_password, "regpass123")

        # Test register full name setter
        self.state.set_register_full_name("John Doe")
        self.assertEqual(self.state.register_full_name, "John Doe")

        # Test reset email setter
        self.state.set_reset_email("reset@example.com")
        self.assertEqual(self.state.reset_email, "reset@example.com")

    def test_get_set_auth_token(self):
        """Test get and set auth token methods."""
        # Initially empty
        self.assertIsNone(self.state.get_auth_token())

        # Set token
        test_token = "test-jwt-token-123"
        self.state.set_auth_token(test_token)
        self.assertEqual(self.state.get_auth_token(), test_token)

        # Set empty token
        self.state.set_auth_token("")
        self.assertIsNone(self.state.get_auth_token())

    def test_is_authenticated_method(self):
        """Test is_authenticated method."""
        # Initially not authenticated
        self.assertFalse(self.state.is_authenticated())

        # Set auth token
        self.state.set_auth_token("test-token")
        # Note: is_authenticated method checks self.is_authenticated, not the token
        # But let's test the property directly
        self.state.is_authenticated = True
        self.assertTrue(self.state.is_authenticated())
        self.state.is_authenticated = False
        self.assertFalse(self.state.is_authenticated())

    def test_get_current_user(self):
        """Test get_current_user method."""
        # Initially no user
        self.assertIsNone(self.state.get_current_user())

        # Set user
        test_user = {"id": 1, "email": "test@example.com", "name": "Test User"}
        self.state.current_user = test_user
        self.state.is_authenticated = True
        returned_user = self.state.get_current_user()
        self.assertEqual(returned_user, test_user)

        # When not authenticated
        self.state.is_authenticated = False
        self.assertIsNone(self.state.get_current_user())

    @patch('state.ReflexApiService')
    def test_login_success(self, mock_api_service):
        """Test successful login."""
        # Mock the API service response
        mock_response = {
            "access_token": "fake-jwt-token",
            "user": {"id": 1, "email": "test@example.com"}
        }
        mock_api_service_instance = Mock()
        mock_api_service_instance.post.return_value = mock_response
        mock_api_service.return_value = mock_api_service_instance

        # Create state with mocked API service
        state = ReflexAuthState()
        state.api_service = mock_api_service_instance

        # Call login
        result = state.login("test@example.com", "password123")

        # Check that API was called
        mock_api_service_instance.post.assert_called_once_with(
            "/api/v1/auth/login",
            {"email": "test@example.com", "password": "password123"}
        )

        # Check state updates
        self.assertEqual(state.auth_token, "fake-jwt-token")
        self.assertEqual(state.current_user, {"id": 1, "email": "test@example.com"})
        self.assertTrue(state.is_authenticated)
        self.assertFalse(state.loading)  # Should be false after completion
        self.assertEqual(state.error_message, "")  # No error on success

        # Check that redirect was returned
        self.assertTrue(len(result) > 0)

    @patch('state.ReflexApiService')
    def test_login_failure(self, mock_api_service):
        """Test failed login."""
        # Mock the API service to raise an exception
        mock_api_service_instance = Mock()
        mock_api_service_instance.post.side_effect = Exception("Network error")
        mock_api_service.return_value = mock_api_service_instance

        # Create state with mocked API service
        state = ReflexAuthState()
        state.api_service = mock_api_service_instance

        # Call login
        result = state.login("test@example.com", "wrongpassword")

        # Check that API was called
        mock_api_service_instance.post.assert_called_once_with(
            "/api/v1/auth/login",
            {"email": "test@example.com", "password": "wrongpassword"}
        )

        # Check state updates
        self.assertEqual(state.auth_token, "")  # Should remain empty
        self.assertEqual(state.current_user, {})  # Should remain empty
        self.assertFalse(state.is_authenticated)  # Should remain false
        self.assertFalse(state.loading)  # Should be false after completion
        self.assertIn("Login failed", state.error_message)  # Should have error

        # Should return empty list (no redirect)
        self.assertEqual(result, [])

    def test_logout(self):
        """Test logout functionality."""
        # Set up authenticated state
        self.state.auth_token = "test-token"
        self.state.current_user = {"id": 1, "email": "test@example.com"}
        self.state.is_authenticated = True
        self.state.error_message = "Some error"

        # Mock the api_service
        mock_api_service = Mock()
        self.state.api_service = mock_api_service

        # Call logout
        self.state.logout()

        # Check that auth token was cleared
        self.assertEqual(self.state.auth_token, "")
        self.assertEqual(self.state.current_user, {})
        self.assertFalse(self.state.is_authenticated)
        self.assertEqual(self.state.error_message, "")

        # Check that api_service.update_auth_token was called with empty string
        mock_api_service.update_auth_token.assert_called_once_with("")

    def test_register_method_exists(self):
        """Test that register method exists."""
        # This test mainly checks that the method exists and has the right signature
        # Since testing the actual API call would require mocking, we'll just verify
        # the method exists and is callable
        self.assertTrue(hasattr(self.state, 'register'))
        self.assertTrue(callable(getattr(self.state, 'register')))


if __name__ == "__main__":
    unittest.main()