import dash
from dash import html, dcc

from fairy_chess import app
from fairy_chess.data import db
from fairy_chess.components.navbar import navbar
from fairy_chess.resources import login_callbacks, session_callbacks, register_callbacks
from fairy_chess.config import POSTGRESS_DATA, POSTGRESS_HOST, POSTGRESS_PASS, POSTGRESS_USER


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    dash.page_container
])


login_callbacks(app)
session_callbacks(app)
register_callbacks(app)

db.bind(provider='postgres', user=POSTGRESS_USER, password=POSTGRESS_PASS, host=POSTGRESS_HOST, database=POSTGRESS_DATA)
db.generate_mapping()

app.run()