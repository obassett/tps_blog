from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

static_path = Path(__file__).parent.parent / "static"
templates_path = Path(__file__).parent.parent / "templates"

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")

templates = Jinja2Templates(directory=templates_path)


@app.get("/")
async def root():
    response = HTMLResponse(
        content=f"""
      <!doctype html>
      <HTML lang="en">
      <head>
          <meta charset="utf-8">
          <title>Hello World!</title>
      </head>
      <body>
          <h1>Hello World</h1>
      </body>
      </HTML>
      """
    )
    return response


@app.get("/testjinja", response_class=HTMLResponse)
async def test_jinja(request: Request):
    content = "Some Content"
    items = ["YC", "Oliver", "Kaito Honda", "Lin", "大山"]
    return templates.TemplateResponse(
        "base.html",
        {"request": request, "items": items, "content": f"This is some {content}"},
    )


@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    return {"article_id": article_id}
