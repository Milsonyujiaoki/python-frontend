"""State management utilities for Flet application."""

import flet as ft
from typing import Any, Optional
import json
from datetime import datetime


class StateManager:
    """Manage application state with persistence."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._state = {}
        self._load_state()

    def _load_state(self):
        """Load state from session storage."""
        saved = self.page.session_get("app_state")
        if saved:
            try:
                self._state = json.loads(saved)
            except json.JSONDecodeError:
                self._state = {}

    def _save_state(self):
        """Save state to session storage."""
        self.page.session_set("app_state", json.dumps(self._state))

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from state."""
        return self._state.get(key, default)

    def set(self, key: str, value: Any):
        """Set value in state."""
        self._state[key] = value
        self._save_state()

    def delete(self, key: str):
        """Delete key from state."""
        if key in self._state:
            del self._state[key]
            self._save_state()

    def clear(self):
        """Clear all state."""
        self._state = {}
        self._save_state()

    def set_authenticated(self, email: str):
        """Set user as authenticated."""
        self.set("authenticated", True)
        self.set("user_email", email)
        self.set("login_time", datetime.now().isoformat())

    def logout(self):
        """Clear authentication."""
        self.delete("authenticated")
        self.delete("user_email")
        self.delete("login_time")

    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.get("authenticated", False)

    def get_user_email(self) -> Optional[str]:
        """Get current user email."""
        return self.get("user_email")


def init_state(page: ft.Page) -> StateManager:
    """Initialize and return state manager."""
    return StateManager(page)
