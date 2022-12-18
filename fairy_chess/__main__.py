import dash
from dash import html
import dash_core_components as dcc

from fairy_chess import app
from fairy_chess.components.navbar import navbar
from fairy_chess.resources import login_callbacks, session_callbacks, register_callbacks


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    dash.page_container
])


login_callbacks(app)
session_callbacks(app)
register_callbacks(app)

app.run()