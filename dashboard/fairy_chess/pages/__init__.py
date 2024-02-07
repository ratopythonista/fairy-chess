from fastapi import FastAPI 

from fairy_chess.pages.contest import contest_router

def include_routes(app: FastAPI):
    app.include_router(contest_router)