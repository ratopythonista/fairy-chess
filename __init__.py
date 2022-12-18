import os

from deta import Deta

from fairy_chess.config import PROJECT_KEY

user_base = Deta(PROJECT_KEY).Base("user")
session_base = Deta(PROJECT_KEY).Base("session")
tournament_base = Deta(PROJECT_KEY).Base("tournament")

icon_driver = Deta(PROJECT_KEY).Drive("icons")