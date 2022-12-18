from flask import request

from dash import Input, Output, Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from fairy_chess.data import user

def register_callbacks(app: Dash):
    @app.callback(
        [
            Output('register-message', 'children'),
            Output('register', 'n_clicks')
        ],
        [
            Input("name", "value"),
            Input("summoner", "value"),
            Input("new-email", "value"),
            Input("new-password", "value"),
            Input("register", "n_clicks"),
        ]
        
    )
    def register(name, summoner, email, password, register):
        from loguru import logger

        logger.debug((name, summoner, email, password))
        if register:
            if user.put(name, email, password, summoner):
                return dcc.Location(pathname="/login", id="registred"), 0
            return dbc.Alert("invalid register", color="danger"), 0
        raise PreventUpdate
