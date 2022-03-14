from aiopath import AsyncPath
from aiofile import async_open

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown import markdown

# TODO: Convert the paths to async paths using aiofiles and aiopath

static_path = AsyncPath(__file__).parent.parent / "static"
templates_path = AsyncPath(__file__).parent.parent / "templates"


# TODO: Add pages directory to contain markdown content for pages - so I don't have to write html
# The pages directory should sit under src already and contains already has a few markdown files.
pages_path = AsyncPath(__file__).parent.parent / "pages"


async def get_navbar_items(pages_path: AsyncPath) -> list[str]:
    navbar = []
    async for page in pages_path.glob("*.md"):
        navbar.append(page.stem)
    return navbar


async def render_markdown_to_html(markdown_page_path: AsyncPath) -> str:
    async with async_open(markdown_page_path) as f:
        content = await f.read()
    return markdown(content)


app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    page_title = "Home"
    content = "Hello Tokyo Python Society"
    navbar_items = await get_navbar_items(pages_path)
    return templates.TemplateResponse(
        "pages.html.j2",
        {
            "request": request,
            "content": content,
            "navbar_items": navbar_items,
            "page_title": page_title,
        },
    )


# TODO: Add a /pages/<page_name> route to serve pages from the pages directory
@app.get("/pages/{page_name}", response_class=HTMLResponse)
async def get_pages(request: Request, page_name: str):
    markdown_page = pages_path / f"{page_name}.md"
    content = await render_markdown_to_html(markdown_page)
    navbar_items = await get_navbar_items(pages_path)
    return templates.TemplateResponse(
        "pages.html.j2",
        {
            "request": request,
            "content": content,
            "navbar_items": navbar_items,
            "page_title": page_name,
        },
    )
