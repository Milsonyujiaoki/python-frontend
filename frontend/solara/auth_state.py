"""Authentication state for Solara frontend."""

import solara

# Reactive variables for authentication state
auth_token = solara.reactive(None)
user = solara.reactive({})
loading = solara.reactive(False)
error = solara.reactive(None)
success_message = solara.reactive(None)

def set_token(token):
    auth_token.value = token

def set_user(user_data):
    user.value = user_data

def set_loading(is_loading):
    loading.value = is_loading

def set_error(err):
    error.value = err

def set_success_message(msg):
    success_message.value = msg

def clear_auth_state():
    auth_token.value = None
    user.value = {}
    error.value = None
    success_message.value = None

def is_authenticated():
    return auth_token.value is not None and user.value != {}