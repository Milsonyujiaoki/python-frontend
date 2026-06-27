import reflex as rx

config = rx.Config(
    app_name="barbershop_frontend",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV3Plugin(),
    ]
)