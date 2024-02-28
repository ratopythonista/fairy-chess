from fastapi import FastAPI 

from fairy_chess.routes.ui.user import user_router
from fairy_chess.routes.ui.contest import contest_router

def include_ui_routes(app: FastAPI):
    app.include_router(user_router, prefix="/api/ui")
    app.include_router(contest_router, prefix="/api/ui")