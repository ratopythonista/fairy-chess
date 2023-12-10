from fastapi import FastAPI 

from fairy_chess.routes.v1.user import user_router
from fairy_chess.routes.v1.tournment import tournment_router

def include_v1_routes(app: FastAPI):
    app.include_router(user_router, prefix="/api/v1")
    app.include_router(tournment_router, prefix="/api/v1")