"""Forgot password page for Solara frontend."""

import solara
import asyncio
from .auth_state import set_loading, set_error, set_success_message

# Simulate forgot password API call
def forgot_password_api(email):
    # In a real app, this would make an HTTP request to the backend
    import time
    # Simulate network delay
    time.sleep(1.5)
    if not email:
        raise Exception("Please enter your email address")
    if "@" not in email:
        raise Exception("Please enter a valid email address")
    # Simulate sending email (always succeed for demo)
    return {"message": "If an account exists with that email, you will receive a reset link."}

@solara.component
def ForgotPasswordPage():
    email, set_email = solara.use_state("")
    loading = solara.use_reactive(False)
    error_msg = solara.use_reactive(None)
    success_msg = solara.use_reactive(None)

    async def handle_submit():
        if not email:
            error_msg.value = "Please enter your email address"
            return
        loading.value = True
        error_msg.value = None
        success_msg.value = None
        try:
            # Simulate API call
            result = await asyncio.to_thread(forgot_password_api, email)
            set_success_message(result["message"])
        except Exception as e:
            error_msg.value = str(e)
        finally:
            loading.value = False

    return solara.Column([
        solara.Title("Forgot Password - BarberShop"),
        solara.Markdown("# Forgot Password"),
        solara.Markdown("Enter your email address to receive a password reset link."),
        solara.InputText(label="Email", value=email, on_value=set_email, placeholder="email@example.com"),
        solara.Button(label="Send Reset Link", on_click=handle_submit, disabled=loading.value, color="primary"),
        solara.Error(if_value=error_msg, children=[error_msg]),
        solara.Success(if_value=success_msg, children=[success_msg]),
    ])