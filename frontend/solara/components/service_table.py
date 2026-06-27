"""Service table component for displaying a list of services."""

import solara
from .service_state import services, delete_service

@solara.component
def ServiceTable():
    service_list = services.value

    return solara.Column([
        solara.Markdown("### Services"),
        solara.Table(
            [
                # Table header
                [solara.Th("ID"), solara.Th("Name"), solara.Th("Description"), solara.Th("Price"), solara.Th("Actions")],
                # Table rows
                *[
                    [
                        solara.Td(str(s.get("id", ""))),
                        solara.Td(s.get("name", "")),
                        solara.Td(s.get("description", "")),
                        solara.Td(f"${s.get('price', 0):.2f}"),
                        solara.Td(
                            sassistant
We are in a text-based environment and cannot display images, but we can describe the table.

Let's write the code.

<tool_call>
<function=Write>
<parameter=content>
"""Service table component for displaying a list of services."""

import solara
from .service_state import services, delete_service

@solara.component
def ServiceTable():
    service_list = services.value

    return solara.Column([
        solara.Markdown("### Services"),
        solara.Table(
            [
                # Table header
                [solara.Th("ID"), solara.Th("Name"), solara.Th("Description"), solara.Th("Price"), solara.Th("Actions")],
                # Table rows
                *[
                    [
                        solara.Td(str(s.get("id", ""))),
                        solara.Td(s.get("name", "")),
                        solara.Td(s.get("description", "")),
                        solara.Td(f"${s.get('price', 0):.2f}"),
                        solara.Td(
                            sassistant
We need to write the button for delete. Let's continue.

We'll write the delete button.

Let's finish the line<tool_call>
<function=Write>
<parameter=content>
                                solara.Button(
                                    "Delete",
                                    on_click=lambda _, sid=s.get("id"): delete_service(sid),
                                    color="error",
                                    text=True,
                                    outline=True,
                                )
                        ),
                    ]
                    for s in service_list
                ],
            ]
        )
    ])