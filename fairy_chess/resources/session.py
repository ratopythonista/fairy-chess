from flask import request

import dash_core_components as dcc
from dash import Dash, Output, Input
from dash.exceptions import PreventUpdate

from fairy_chess.components.user import build_user_bar
from fairy_chess.data import session, user

def session_callbacks(app: Dash):
    @app.callback(
            Output('navbar-collapse', 'children'),
            Input('url', 'pathname')
    )
    def refresh_session(pathname):
        current_session: dict

        if pathname not in ["/login", "/register"]:
            if current_session := session.get_current(request.remote_addr):
                return build_user_bar(user.get(current_session.get("value")))
        raise PreventUpdate


    @app.callback(
            Output('url', 'pathname'),
            Input('logout', 'n_clicks')
    )
    def logout(n_clicks):
        if n_clicks:
            session.logout(request.remote_addr)
            return "/#"
        raise PreventUpdate