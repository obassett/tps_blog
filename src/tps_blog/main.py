from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# TODO: Convert the paths to async paths using aiofiles and aiopath

static_path = Path(__file__).parent.parent / "static"
templates_path = Path(__file__).parent.parent / "templates"

# TODO: Add pages directory to contain markdown content for pages - so I don't have to write html
# The pages directory should sit under src already and contains already has a few markdown files.

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    content = "Hello World"
    return templates.TemplateResponse(
        "base.html.j2", {"request": request, "content": content}
    )


# TODO: Add a /pages/<page_name> route to serve pages from the pages directory
