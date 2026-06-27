"""
Abstract base class for authentication state management.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class AuthStateManager(ABC):
    """Abstract base class for managing authentication state."""

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        """Log in a user."""
        pass

    @abstractmethod
    def logout(self) -> None:
        """Log out the current user."""
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        pass

    @abstractmethod
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get the currently authenticated user."""
        pass

    @abstractmethod
    def set_auth_token(self, token: str) -> None:
        """Set the authentication token."""
        pass

    @abstractmethod
    def get_auth_token(self) -> Optional[str]:
        """Get the authentication token."""
        pass