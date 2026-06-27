"""Service state management for Solara frontend."""

import solara

# Reactive variable for the list of services
services = solara.reactive([])

def get_service_by_id(service_id):
    """Get a service by ID."""
    for s in services.value:
        if s.get("id") == service_id:
            return s
    return None

def add_service(service):
    """Add a new service."""
    services.value = [*services.value, service]

def update_service(service):
    """Update an existing service."""
    new_services = []
    for s in services.value:
        if s.get("id") == service.get("id"):
            new_services.append(service)
        else:
            new_services.append(s)
    services.value = new_services

def delete_service(service_id):
    """Delete a service by ID."""
    services.value = [s for s in services.value if s.get("id") != service_id]

def clear_services():
    """Clear all services (for testing)."""
    services.value = []