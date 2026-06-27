"""Customer form component for creating and editing customers."""

import solara
from .customer_state import add_customer, update_customer, get_customer_by_id, get_entities
from .base_form import BaseForm

# Define the fields for the customer form
CUSTOMER_FIELDS = [
    {"label": "Name", "name": "name", "type": "text"},
    {"label": "Email", "name": "email", "type": "text"},
    {"label": "Phone", "name": "phone", "type": "text"},
]

@solara.component
def CustomerForm(customer_id=None):
    return BaseForm(
        title="Customer",
        fields=CUSTOMER_FIELDS,
        get_entity_by_id=get_customer_by_id,
        get_entities=get_entities,
        add_entity=add_customer,
        update_entity=update_customer,
        entity_id=customer_id,
    )