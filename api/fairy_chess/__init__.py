from fastapi import FastAPI

from fairy_chess.routes.v1 import include_v1_routes
from fairy_chess.database import create_db_and_tables


app = FastAPI(
    title="Fairy Chess - Team Figth Tatics Tournament"
)

create_db_and_tables()
include_v1_routes(app)