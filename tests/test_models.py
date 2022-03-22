import pytest
from aiopath import AsyncPath
from tps_blog.models.content import Page, PageNotFoundError


test_page_names = ["about", "meetup", "slack"]


@pytest.fixture(scope="session")
def pages_path(tmp_path_factory):
    pages_path_directory = tmp_path_factory.mktemp("pages")
    for page in test_page_names:
        with (pages_path_directory / f"{page}.md").open(mode="x") as f:
            f.write(f"# {page} Test")
    return AsyncPath(pages_path_directory)


@pytest.mark.asyncio
async def test_create_page_from_file(pages_path: AsyncPath):
    result: Page = await Page.create(pages_path=pages_path, page_title="about")

    assert type(result) == Page
    assert result.page_title == "about"
    assert result.content == "<h1>about Test</h1>"
    assert result.navbar_items == test_page_names


@pytest.mark.asyncio
async def test_create_page_file_not_found(pages_path: AsyncPath):
    with pytest.raises(PageNotFoundError):
        result: Page = await Page.create(
            pages_path=pages_path, page_title="does_not_exist"
        )
