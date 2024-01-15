from fastapi import FastAPI 

from fairy_chess.routes.v1.user import user_router
from fairy_chess.routes.v1.stage import stage_router
from fairy_chess.routes.v1.contest import contest_router

def include_v1_routes(app: FastAPI):
    app.include_router(user_router, prefix="/api/v1")
    app.include_router(stage_router, prefix="/api/v1")
    app.include_router(contest_router, prefix="/api/v1")