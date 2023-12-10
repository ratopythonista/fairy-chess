from fastapi import FastAPI 

from fairy_chess.routes.v1.user import user_router

def include_v1_routes(app: FastAPI):
    app.include_router(user_router, prefix="/api/v1")