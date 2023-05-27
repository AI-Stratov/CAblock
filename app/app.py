"""Main application file."""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import app.views as views

app = FastAPI()


@app.get("/", include_in_schema=False)
def root():
    """Redirects to the docs page."""
    return RedirectResponse(url="/docs")


app.include_router(views.router)
