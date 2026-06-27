"""Customer table component for displaying a list of customers."""

import solara
from .state import customers, delete_customer

@solara.component
def CustomerTable():
    customer_list = customers.value

    return solara.Column([
        solara.Markdown("### Customers"),
        solara.Table(
            [
                # Table header
                [solara.Th("ID"), solara.Th("Name"), solara.Th("Email"), solara.Th("Phone"), solara.Th("Actions")],
                # Table rows
                *[
                    [
                        solara.Td(str(c.get("id", ""))),
                        solara.Td(c.get("name", "")),
                        solara.Td(c.get("email", "")),
                        solara.Td(c.get("phone", "")),
                        solara.Td(
                            solara.Button(
                                "Delete",
                                on_click=lambda _, cid=c.get("id"): delete_customer(cid),
                                color="error",
                                text=True,
                                outline=True,
                            )
                        ),
                    ]
                    for c in customer_list
                ],
            ]
        )
    ])