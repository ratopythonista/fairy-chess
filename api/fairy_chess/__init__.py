from __future__ import annotations as _annotations

from fastapi import FastAPI
from fastui import prebuilt_html
from fastapi.responses import HTMLResponse

from fairy_chess.routes.v1 import include_v1_routes
from fairy_chess.routes.ui import include_ui_routes

from fairy_chess.database import create_db_and_tables


app = FastAPI(
    title="Fairy Chess - Team Figth Tatics Tournament"
)

create_db_and_tables()
include_v1_routes(app)
include_ui_routes(app)

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))