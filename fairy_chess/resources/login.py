from flask import request

from dash import Input, Output, Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from fairy_chess.data.user import authenticate
from fairy_chess.data import session

def login_callbacks(app: Dash):
    @app.callback(
        [
            Output('message', 'children'),
            Output('login', 'n_clicks')
        ],
        [
            Input("email", "value"),
            Input("password", "value"),
            Input("login", "n_clicks"),
        ]
        
    )
    def login(email, password, login):
        if login:
            if user_id := authenticate(email, password):
                session.login(request.remote_addr, user_id)
                return dcc.Location(pathname="/", id="logged"), 0
            return dbc.Alert("invalid login or password", color="danger"), 0
        raise PreventUpdate
