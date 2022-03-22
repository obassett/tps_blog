from aiopath import AsyncPath
from aiofile import async_open

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown import markdown

from .utilities import get_navbar_items, render_markdown_to_html
from .models.content import Page, PageNotFoundError

# TODO: Convert the paths to async paths using aiofiles and aiopath

static_path = AsyncPath(__file__).parent.parent / "static"
templates_path = AsyncPath(__file__).parent.parent / "templates"


# TODO: Add pages directory to contain markdown content for pages - so I don't have to write html
# The pages directory should sit under src already and contains already has a few markdown files.
pages_path = AsyncPath(__file__).parent.parent / "pages"


app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    page_title = "Home"
    content = "Hello Tokyo Python Society"
    try:
        page = await Page.create(pages_path, page_title, content=content)
    except PageNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        "pages.html.j2",
        {"request": request, "page_data": page},
    )


# TODO: Add a /pages/<page_name> route to serve pages from the pages directory
@app.get("/pages/{page_name}", response_class=HTMLResponse)
async def get_pages(request: Request, page_name: str):
    try:
        page = await Page.create(pages_path, page_name)
    except PageNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        "pages.html.j2",
        {"request": request, "page_data": page},
    )
