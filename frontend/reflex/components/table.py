import reflex as rx

def data_table(
    columns: list,
    data: list,
    actions: list = None,
    loading: bool = False,
):
    """
    A reusable data table component.

    Args:
        columns: List of column definitions. Each dict should have:
            - header: str, the column header text
            - key: str, the key in the data dict to display (or a function that takes a row and returns the cell content)
            - size: optional, list of strings for responsive size (default: ["sm", "md", "md"])
        data: List of dictionaries representing the rows.
        actions: List of action definitions for the actions column. Each dict should have:
            - label: str, the button text
            - on_click: callable that takes a row (dict) and returns an event handler (or list of handlers)
            - color_scheme: optional, str (default: "blue" for first action, "red" for second)
            - size: optional, list of strings for responsive size (default: ["sm", "md", "md"])
            - loading: optional, bool or callable that takes a row and returns a bool (to show spinner)
            - disabled: optional, bool or callable that takes a row and returns a bool (to disable button)
        loading: bool, if True, shows a spinner instead of the table body.

    Returns:
        rx.Component: A responsive table component.
    """
    if actions is None:
        actions = []

    # Define the header row
    header_cells = []
    for col in columns:
        header_cells.append(
            rx.table.column_header_cell(col["header"], size=col.get("size", ["sm", "md", "md"]))
        )
    # Add actions column header if there are actions
    if actions:
        header_cells.append(
            rx.table.column_header_cell("Actions", size=["sm", "md", "md"])
        )

    # Define the body rows
    def get_row(row):
        cells = []
        for col in columns:
            # If key is a callable, call it with the row to get the value
            if callable(col["key"]):
                value = col["key"](row)
            else:
                value = row.get(col["key"], "")
            cells.append(
                rx.table.cell(value, size=col.get("size", ["sm", "md", "md"]))
            )

        # Add action cells
        if actions:
            action_buttons = []
            for i, action in enumerate(actions):
                # Determine button properties
                button_props = {
                    "on_click": action["on_click"](row) if callable(action["on_click"]) else action["on_click"],
                    "color_scheme": action.get("color_scheme", "blue" if i == 0 else "red"),
                    "size": action.get("size", ["sm", "md", "md"]),
                }
                # Handle loading state
                if "loading" in action:
                    loading_val = action["loading"](row) if callable(action["loading"]) else action["loading"]
                    button_props["loading"] = loading_val
                # Handle disabled state
                if "disabled" in action:
                    disabled_val = action["disabled"](row) if callable(action["disabled"]) else action["disabled"]
                    button_props["disabled"] = disabled_val

                # If loading is True, we want to show a spinner instead of the label
                if button_props.get("loading", False):
                    button_content = rx.spinner(size="sm")
                else:
                    button_content = action["label"]

                action_buttons.append(
                    rx.button(
                        button_content,
                        **button_props,
                    )
                )

            cells.append(
                rx.table.cell(
                    rx.hstack(*action_buttons, spacing=["2", "3", "3"]),
                    size=["sm", "md", "md"],
                )
            )

        return rx.table.row(*cells)

    # If loading, show a spinner
    if loading:
        return rx.center(rx.spinner(), py=8)

    return rx.table.responsive(
        rx.table.header(rx.table.row(*header_cells)),
        rx.table.body(
            rx.foreach(data, get_row)
        ),
    )