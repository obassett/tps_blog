from aiopath import AsyncPath
from aiofile import async_open
from markdown import markdown


async def get_navbar_items(pages_path: AsyncPath) -> list[str]:
    navbar = []
    async for page in pages_path.glob("*.md"):
        navbar.append(page.stem)
    return navbar


async def render_markdown_to_html(markdown_page_path: AsyncPath) -> str:
    async with async_open(markdown_page_path) as f:
        content = await f.read()
    return markdown(content)
