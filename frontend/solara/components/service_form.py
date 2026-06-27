"""Service form component for creating and editing services."""

import solara
from .service_state import add_service, update_service, get_service_by_id, get_entities
from .base_form import BaseForm

# Define the fields for the service form
SERVICE_FIELDS = [
    {"label": "Name", "name": "name", "type": "text"},
    {"label": "Description", "name": "description", "type": "text"},
    {"label": "Price", "name": "price", "type": "number"},
]

@solara.component
def ServiceForm(service_id=None):
    return BaseForm(
        title="Service",
        fields=SERVICE_FIELDS,
        get_entity_by_id=get_service_by_id,
        get_entities=get_entities,
        add_entity=add_service,
        update_entity=update_service,
        entity_id=service_id,
    )