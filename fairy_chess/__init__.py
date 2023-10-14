from fastapi import FastAPI

from fairy_chess.routes.v1 import include_v1_routes


app = FastAPI(
    title="Fairy Chess - Team Figth Tatics Tournament"
)

include_v1_routes(app)