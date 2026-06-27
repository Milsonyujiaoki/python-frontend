"""Registration page for Solara frontend."""

import solara
import asyncio
from .auth_state import set_loading, set_error, set_success_message, set_user, set_token

# Simulate register API call
def fake_register_api(email, password, full_name):
    # In a real app, this would make an HTTP request to the backend
    import time
    # Simulate network delay
    time.sleep(1.5)
    if not email or not password or not full_name:
        raise Exception("All fields are required")
    if "@" not in email:
        raise Exception("Please enter a valid email address")
    if len(password) < 6:
        raise Exception("Password must be at least 6 characters long")
    # Simulate successful registration
    return {
        "access_token": "fake-jwt-token",
        "user": {"id": 2, "email": email, "name": full_name}
    }

@solara.component
def RegisterPage():
    email, set_email = solara.use_state("")
    password, set_password = solara.use_state("")
    full_name, set_full_name = solara.use_state("")
    loading = solara.use_reactive(False)
    error_msg = solara.use_reactive(None)
    success_msg = solara.use_reactive(None)

    async def handle_register():
        if not email or not password or not full_name:
            error_msg.value = "Please fill in all fields"
            return
        loading.value = True
        error_msg.value = None
        success_msg.value = None
        try:
            # Simulate API call (run in thread to avoid blocking)
            result = await asyncio.to_thread(fake_register_api, email, password, full_name)
            # Store token and user
            set_token(result["access_token"])
            set_user(result["user"])
            set_success_message("Registration successful! You are now logged in.")
        except Exception as e:
            error_msg.value = str(e)
        finally:
            loading.value = False

    return solara.Column([
        solara.Title("Register - BarberShop"),
        solara.Markdown("# Register"),
        solara.InputText(label="Full Name", value=full_name, on_value=set_full_name, placeholder="Your full name"),
        solara.InputText(label="Email", value=email, on_value=set_email, placeholder="email@example.com"),
        solara.InputSecret(label="Password", value=password, on_value=set_password, placeholder="••••••••"),
        solara.Button(label="Register", on_click=handle_register, disabled=loading.value, color="primary"),
        solara.Error(if_value=error_msg, children=[error_msg]),
        solara.Success(if_value=success_msg, children=[success_msg]),
    ])