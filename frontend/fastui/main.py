from fastapi import FastAPI
from fastui import PrebuiltHTML, components as c
from fastui.components.display import DisplayLookup

app = FastAPI()

@app.get("/api/", response_model=lambda: [c.Heading(text="Hello, FastUI!")], response_model_exclude_none=True)
def api():
    return [
        c.Heading(text="Hello, FastUI!", level=2),
    ]

@app.get("/{path:path}")
async def html_landing_page() -> str:
    return PrebuiltHTML(
        title="FastUI Demo",
        body=[c.Heading(text="Hello, FastUI!", level=2)],
    ).render()