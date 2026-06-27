"""Login page for Solara frontend."""

import solara
import asyncio
from .auth_state import set_token, set_user, set_loading, set_error, set_success_message

# Simulate login API call
def fake_login_api(email, password):
    # In a real app, this would make an HTTP request to the backend
    # For now, we'll simulate a delay and then either succeed or fail
    import time
    # Simulate network delay
    time.sleep(1)
    if email == "test@example.com" and password == "password123":
        return {
            "access_token": "fake-jwt-token",
            "user": {"id": 1, "email": email, "name": "Test User"}
        }
    else:
        raise Exception("Invalid email or password")

@solara.component
def LoginPage():
    email, set_email = solara.use_state("")
    password, set_password = solara.use_state("")
    loading = solara.use_reactive(False)
    error_msg = solara.use_reactive(None)
    success_msg = solara.use_reactive(None)

    async def handle_login():
        if not email or not password:
            error_msg.value = "Please fill in all fields"
            return
        loading.value = True
        error_msg.value = None
        success_msg.value = None
        try:
            # Simulate API call (run in thread to avoid blocking)
            result = await asyncio.to_thread(fake_login_api, email, password)
            set_token(result["access_token"])
            set_user(result["user"])
            set_success_message("Login successful!")
            # In a real app, we would redirect to dashboard
            # For now, we just show the success message
        except Exception as e:
            error_msg.value = str(e)
        finally:
            loading.value = False

    return solara.Column([
        solara.Title("Login - BarberShop"),
        solara.Markdown("# Login"),
        solara.InputText(label="Email", value=email, on_value=set_email, placeholder="email@example.com"),
        solara.InputSecret(label="Password", value=password, on_value=set_password, placeholder="••••••••"),
        solara.Button(label="Login", on_click=handle_login, disabled=loading.value, color="primary"),
        solara.Error(if_value=error_msg, children=[error_msg]),
        solara.Success(if_value=success_msg, children=[success_msg]),
    ])