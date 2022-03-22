from pydantic import BaseModel
from typing import Optional
from aiopath import AsyncPath

from ..utilities import get_navbar_items, render_markdown_to_html


class PageNotFoundError(Exception):
    pass


class Page(BaseModel):
    navbar_items: list[str]
    content: str
    description: Optional[str]
    page_title: str

    @classmethod
    async def create(
        cls,
        pages_path: AsyncPath,
        page_title: str,
        description: Optional[str] = None,
        content: Optional[str] = None,
    ):
        navbar_items = await get_navbar_items(pages_path)
        page_file_path = pages_path / f"{page_title}.md"

        if content is None:
            if await page_file_path.exists():
                content = await render_markdown_to_html(page_file_path)
            else:
                raise PageNotFoundError(f"Page {page_file_path} not found")

        return cls(
            navbar_items=navbar_items,
            content=content,
            description=description,
            page_title=page_title,
        )
