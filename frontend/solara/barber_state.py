"""Barber state management for Solara frontend."""

import solara

# Reactive variable for the list of barbers
barbers = solara.reactive([])

def get_barber_by_id(barber_id):
    """Get a barber by ID."""
    for b in barbers.value:
        if b.get("id") == barber_id:
            return b
    return None

def add_barber(barber):
    """Add a new barber."""
    barbers.value = [*barbers.value, barber]

def update_barber(barber):
    """Update an existing barber."""
    new_barbers = []
    for b in barbers.value:
        if b.get("id") == barber.get("id"):
            new_barbers.append(barber)
        else:
            new_barbers.append(b)
    barbers.value = new_barbers

def delete_barber(barber_id):
    """Delete a barber by ID."""
    barbers.value = [b for b in barbers.value if b.get("id") != barber_id]

def clear_barbers():
    """Clear all barbers (for testing)."""
    barbers.value = []