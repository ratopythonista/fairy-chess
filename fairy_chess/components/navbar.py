from dash import html
import dash_core_components as dcc

from fairy_chess import app
from fairy_chess.components.user import login_bar

navbar = html.Header(
    html.Div(
        [
            html.H1(
                html.A(
                    html.Img(src='/assets/logo.png', height="30px"),
                    href="/",
                    className="navbar-brand-image"
                ), className="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3"
            ),
            html.Div(
                login_bar,
                id="navbar-collapse",
                className="navbar-nav flex-row order-md-last"
            ),
        ],
        className="container-xl",
    ),
    className="navbar navbar-expand-md navbar-dark navbar-overlap d-print-none"
)