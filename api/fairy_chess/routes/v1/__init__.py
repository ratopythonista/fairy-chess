from fastapi import FastAPI 

from fairy_chess.routes.v1.user import user_router
# from fairy_chess.routes.v1.lobby import lobby_router
# from fairy_chess.routes.v1.round import round_router
# from fairy_chess.routes.v1.match import match_router
from fairy_chess.routes.v1.contest import contest_router

def include_v1_routes(app: FastAPI):
    app.include_router(user_router, prefix="/api/v1")
    # app.include_router(round_router, prefix="/api/v1")
    # app.include_router(lobby_router, prefix="/api/v1")
    # app.include_router(match_router, prefix="/api/v1")
    app.include_router(contest_router, prefix="/api/v1")