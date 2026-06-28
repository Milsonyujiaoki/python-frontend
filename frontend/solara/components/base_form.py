"""Base form component for creating and editing entities."""

import solara
from typing import List, Dict, Any, Callable, Optional


def BaseForm(
    title: str,
    fields: List[Dict[str, Any]],
    get_entity_by_id: Callable[[int], Optional[dict]],
    get_entities: Callable[[], list],
    add_entity: Callable[[dict], None],
    update_entity: Callable[[dict], None],
    entity_id: Optional[int] = None,
    id_generator: Callable[[list], int] = lambda items: len(items) + 1,
):
    """
    A generic form for creating or editing an entity.

    Args:
        title: The title to display (e.g., "Customer")
        fields: List of field definitions. Each field is a dict with:
            - label: str, the label for the input
            - name: str, the key in the entity dictionary
            - type: str, optional, the input type (default: "text")
            - placeholder: str, optional, placeholder text
        get_entity_by_id: Function to fetch an entity by ID (for edit mode)
        get_entities: Function to get the list of all entities (for ID generation)
        add_entity: Function to add a new entity (should accept entity dict)
        update_entity: Function to update an existing entity (should accept entity dict with id)
        entity_id: The ID of the entity to edit (None for create)
        id_generator: Function to generate a new ID from the list of existing items (default: len(items) + 1)
    """
    # Determine if we are in edit mode
    is_edit = entity_id is not None
    # Fetch existing entity if in edit mode
    entity = None
    if is_edit:
        entity = get_entity_by_id(entity_id)

    # Initialize form state for each field
    form_state = {}
    for field in fields:
        field_name = field["name"]
        default_value = ""
        if entity and field_name in entity:
            # Use the value from the entity if available
            # Handle type conversion for display
            field_type = field.get("type", "string")
            if field_type == "number":
                default_value = entity[field_name]
            elif field_type == "boolean":
                default_value = entity[field_name]
            else:
                default_value = str(entity[field_name])
        elif "default" in field:
            default_value = field["default"]
        else:
            # Type-based defaults
            if field.get("type") == "number":
                default_value = 0
            elif field.get("type") == "checkbox":
                default_value = False
            else:
                default_value = ""

        form_state[field_name] = solara.use_state(default_value)

    def handle_submit():
        """Handle form submission."""
        # Collect form data
        entity_data = {}
        for field in fields:
            field_name = field["name"]
            value_tuple = form_state[field_name]
            value = value_tuple[0]  # Get the value from the use_state tuple
            field_type = field.get("type", "text")
            if field_type == "number":
                try:
                    # Convert to float if it's a string, otherwise keep as is
                    if isinstance(value, str):
                        value = float(value) if value else 0
                    else:
                        value = float(value) if value is not None else 0
                except ValueError:
                    value = 0
            elif field_type == "checkbox":
                value = bool(value)
            entity_data[field_name] = value

        # Generate ID for new entities
        if not is_edit:
            # Generate a new ID using the provided generator
            entities = get_entities()
            entity_data["id"] = id_generator(entities)
        else:
            # For updates, include the entity ID
            entity_data["id"] = entity_id

        # Call the appropriate function
        if is_edit:
            update_entity(entity_data)
        else:
            add_entity(entity_data)

    # Build the form UI
    return solara.Column([
        solara.Markdown(f"## {'Edit' if is_edit else 'Add'} {title}"),
        *[
            solara.InputText(
                label=field["label"],
                value=form_state[field["name"]][0],
                on_value=form_state[field["name"]][1],
                placeholder=field.get("placeholder", ""),
                type="number" if field.get("type") == "number" else "text",
            )
            for field in fields
        ],
        solara.Button(
            label="Save",
            on_click=handle_submit,
            color="primary",
        ),
    ])