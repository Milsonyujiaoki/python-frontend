"""Barber table component for displaying a list of barbers."""

import solara
from .barber_state import barbers, delete_barber

@solara.component
def BarberTable():
    barber_list = barbers.value

    return solara.Column([
        solara.Markdown("### Barbers"),
        solara.Table(
            [
                # Table header
                [solara.Th("ID"), solara.Th("Name"), solara.Th("Email"), solara.Th("Phone"), solara.Th("Actions")],
                # Table rows
                *[
                    [
                        solara.Td(str(b.get("id", ""))),
                        solara.Td(b.get("name", "")),
                        solara.Td(b.get("email", "")),
                        solara.Td(b.get("phone", "")),
                        solara.Td(
                            solara.Button(
                                "Delete",
                                on_click=lambda _, bid=b.get("id"): delete_barber(bid),
                                color="error",
                                text=True,
                                outline=True,
                            )
                        ),
                    ]
                    for b in barber_list
                ],
            ]
        )
    ])