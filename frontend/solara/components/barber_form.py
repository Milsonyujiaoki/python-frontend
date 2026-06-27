"""Barber form component for creating and editing barbers."""

import solara
from .barber_state import add_barber, update_barber, get_barber_by_id, get_entities
from .base_form import BaseForm

# Define the fields for the barber form
BARBER_FIELDS = [
    {"label": "Name", "name": "name", "type": "text"},
    {"label": "Email", "name": "email", "type": "text"},
    {"label": "Phone", "name": "phone", "type": "text"},
]

@solara.component
def BarberForm(barber_id=None):
    return BaseForm(
        title="Barber",
        fields=BARBER_FIELDS,
        get_entity_by_id=get_barber_by_id,
        get_entities=get_entities,
        add_entity=add_barber,
        update_entity=update_barber,
        entity_id=barber_id,
    )