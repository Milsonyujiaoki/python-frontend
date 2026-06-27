import flet as ft

def main(page: ft.Page):
    page.title = "Flet Counter"
    page.add(
        ft.TextField(label="Your name"),
        ft.ElevatedButton("Say hello!", on_click=lambda e: page.add(
            ft.Text(f"Hello, {e.control.value}!")
        )),
    )

ft.app(target=main)